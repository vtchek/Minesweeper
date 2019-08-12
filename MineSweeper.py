import pygame
import random
import time
from queue import Queue

pygame.init()


w = 656
h = 656
MINE = 40

RED = pygame.Color("red")
WHITE = pygame.Color("white")
BLUE = pygame.Color("blue")
BLACK = pygame.Color("black")
YELLOW = pygame.Color("yellow")
GREEN = pygame.Color("green")
GREY = (185,185,185)

LEFT = 1
RIGHT = 3

ROW = 16
COL = 16


size = (w,h)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
bomb_image = pygame.image.load("Images/bomb.png")
zero = pygame.image.load("Images/0.png")
one = pygame.image.load("Images/1.png")
two = pygame.image.load("Images/2.png")
three = pygame.image.load("Images/3.png")
four= pygame.image.load("Images/4.png")
five = pygame.image.load("Images/5.png")
six = pygame.image.load("Images/6.png")
seven = pygame.image.load("Images/7.png")
eight = pygame.image.load("Images/8.png")
covered = pygame.image.load("Images/facingDown.png")
flag = pygame.image.load("Images/flagged.png")
dead_bomb = pygame.image.load("Images/dead_bomb.png")



class Square:
    def __init__(self,x,y,size,color):
        self._x = x
        self._y = y
        self._size = size
        self._color = color 
        self._is_mine = False
        self._is_flagged = False
        self._is_visible = True 
        self._mine_around = 0 #number of surounding
        self._is_first_line = False # True = all cells surrounding an empty cell
        self._as_number = False      

    def draw_square(self,color):
        pygame.draw.rect(screen, self._color, (self._x, self._y, self._size, self._size))

class Grid:
    def __init__(self,distance,size,color):
        self._squares = []
        self._distance = distance 
        self._size = size 
        self._color = color 
        self._block_size = self._distance + self._size 
        self._lost = False #to forbid click
        self._opened_cells = 0

        for loop in range(ROW):
            self._squares.append([0] * COL)

        x = 0
        for i in range(ROW):
            y = 0
            for j in range(COL):
                self._squares[i][j] = Square(x,y,self._size,self._color)
                y+= self._block_size
            x += self._block_size
   
    def draw_grid(self,color):
        for i in range(COL):
            for j in range(ROW):
                self._squares[i][j].color = color
                self._squares[i][j].draw_square(color)
                if self._squares[i][j]._is_mine == True:
                    screen.blit(bomb_image,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 1:
                    screen.blit(one,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 2:
                    screen.blit(two,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 3:
                    screen.blit(three,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 4:
                    screen.blit(four,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 5:
                    screen.blit(five,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 6:
                    screen.blit(six,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 7:
                    screen.blit(seven,(self.get_xy(i,j)))
                elif self._squares[i][j]._mine_around == 8:
                    screen.blit(eight,(self.get_xy(i,j)))
     
    def position(self,x,y):
        for i in range(ROW):
            for j in range(COL):
                if self._squares[i][j]._x == x and self._squares[i][j]._y == y:
                    return (i,j)
    def get_xy(self,i,j):
        return (self._squares[i][j]._x, self._squares[i][j]._y)

                

def load_mines(number):

    count = number
    coord_poss = []
    for x in range(ROW):
        coord_poss.append(x*grid._block_size)     
    while count > 0:  
        (mine_x,mine_y) = (random.choice(coord_poss),random.choice(coord_poss))
        for i in range(COL):
            for j in range(ROW):
                if grid._squares[i][j]._is_mine == False and grid._squares[i][j]._x == mine_x and grid._squares[i][j]._y == mine_y:
                    grid._squares[i][j]._is_mine = True
                    count -=1

def check_cell():
    for row in range(0,ROW): 
        for col in range(0,COL):
            for rowOff in range(row-1, row+2): #offset to cover surrounding
                for colOff in range(col-1,col+2): 
                    if (rowOff >=0 and rowOff < ROW and colOff >= 0 and colOff < COL and grid._squares[row][col]._is_mine == False):#exclude self and stay in the matrix
                        if grid._squares[rowOff][colOff]._is_mine == True: #cell we are looking at
                            grid._squares[rowOff][colOff]._mine_around = -1 #will help with uncovering
                            grid._squares[row][col]._mine_around +=1 #actual cell
                            grid._squares[row][col]._as_number = True


     
def set_fist_line(row,col): #determine if a cell is a "first line cell or not"
    if grid._squares[row][col]._mine_around == 0:
        for rowOff in range(row-1, row+2): #position where looking
            for colOff in range(col-1,col+2): #position where looking
                if (rowOff >=0 and rowOff < ROW and colOff >= 0 and colOff < COL):#exclude self and stay in the matrix
                        if grid._squares[rowOff][colOff]._as_number == True:
                            grid._squares[rowOff][colOff]._is_first_line = True #cell looking at
    
    

#A cell is valid (to be uncovered) if its empty or in first line and if it is not a mine and not visible and in the array boundaries
def check_cell_validity(i,j):
    if i >= 0 and i < ROW and j >= 0 and j < COL and \
         (grid._squares[i][j]._mine_around == 0 \
            or  grid._squares[i][j]._is_first_line == True) \
                    and grid._squares[i][j]._is_visible == False \
                        and grid._squares[i][j]._is_mine == False:
        return True 
    else:
        return False



def draw_number(x,y,value):
    if value == 0:
        grid._opened_cells+=1
        screen.blit(zero,(x,y))
    elif value == 1:
        grid._opened_cells+=1
        screen.blit(one,(x,y))
    elif value == 2:
        grid._opened_cells+=1
        screen.blit(two,(x,y))
    elif value == 3:
        grid._opened_cells+=1
        screen.blit(three,(x,y))
    elif value == 4:
        grid._opened_cells+=1
        screen.blit(four,(x,y))
    elif value == 5:
        grid._opened_cells+=1
        screen.blit(five,(x,y))
    elif value == 6:
        grid._opened_cells+=1
        screen.blit(six,(x,y))
    elif value == 7:
        grid._opened_cells+=1
        screen.blit(seven,(x,y))
    elif value == 8:  
        grid._opened_cells+=1
        screen.blit(eight,(x,y))


def uncover_empty_cells(i,j): #Flood fill algo to uncover_empty_cells empty cell (from pseudo code wikipedia)
    set_fist_line(i,j) 

    q = Queue()
    q.put((i,j))
    while not (q.empty()):     
        new_index = q.get(i,j)
        i1 = new_index[0]
        j1 = new_index[1]

        (x,y) = grid.get_xy(i1,j1)
    
        if check_cell_validity(i1,j1):
            draw_number(x,y,grid._squares[i1][j1]._mine_around)
            grid._squares[i1][j1]._is_visible = True  #(si False le truc des nombres marche, changer en haut aussi)   
        if check_cell_validity(i1+1,j1):
            set_fist_line(i1+1,j1)
            q.put((i1+1, j1))
        if check_cell_validity(i1-1,j1):
            set_fist_line(i1-1,j1)
            q.put((i1-1, j1))
        if check_cell_validity(i1,j1+1):
            set_fist_line(i1,j1+1)
            q.put((i1, j1+1))
        if check_cell_validity(i1,j1-1):
            set_fist_line(i1,j1-1)
            q.put((i1, j1-1))
    

def cover_board():
    for i in range(ROW):
        for j in range(COL):
            screen.blit(covered,(grid._squares[i][j]._x,grid._squares[i][j]._y))
            grid._squares[i][j]._is_visible = False
        
           

def play():
    global run 
    global grid
    pos = pygame.mouse.get_pos()
    x = (pos[0] // grid._size) * grid._block_size
    y = (pos[1] // grid._size) * grid._block_size
   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if grid._lost == False:
                ###FLAG ON RIGHT CLICK###
                if event.button == RIGHT: 
                    k = grid.position(x,y)[0]
                    l = grid.position(x,y)[1]

                    cell = grid._squares[k][l]

                    if cell._is_flagged == False and cell._is_visible == False: #flagging
                        cell._is_flagged = True
                        screen.blit(flag,(x,y))                       
                    elif cell._is_flagged == True and cell._is_visible == False: #onflagging
                        cell._is_flagged = False
                        screen.blit(covered,(x,y))
                                 
                ###OTHER ACTIONS####
                elif event.button == LEFT:
                    k = grid.position(x,y)[0]
                    l = grid.position(x,y)[1]
                    cell = grid._squares[k][l]
                                    
                    if cell._is_flagged == False: #can't left click on flagged cell
                        if cell._mine_around == 0 and cell._is_mine == False: #if empty cell               
                            uncover_empty_cells(k,l)

                        elif cell._mine_around == 1:
                            cell._is_visible = True
                            draw_number(x,y,1)
                        elif cell._mine_around == 2:
                            cell._is_visible = True
                            draw_number(x,y,2)
                        elif cell._mine_around == 3:
                            cell._is_visible = True
                            draw_number(x,y,3)
                        elif cell._mine_around == 4:
                            cell._is_visible = True
                            draw_number(x,y,4)
                        elif cell._mine_around == 5:
                            cell._is_visible = True
                            draw_number(x,y,5)
                        elif cell._mine_around == 6:
                            cell._is_visible = True
                            draw_number(x,y,6)
                        elif cell._mine_around == 7:
                            cell._is_visible = True
                            draw_number(x,y,7)
                        elif cell._mine_around == 8:
                            cell._is_visible = True
                            draw_number(x,y,8)
                        elif cell._is_mine == True:
                            grid._lost = True
                            lost = font.render("You lost !!",True, BLACK)
                            screen.blit(dead_bomb,(x,y))
                            screen.blit(lost,(205,246))
                            
                            # grid = Grid(1,40,GREY) #for restart?
                            # main()
            
    check_win()
                   
            
def check_win():
    if grid._opened_cells == (ROW*COL) - MINE:
        win = font.render("You won !!",True,BLACK)   
        screen.blit(win,(205,164))
    

grid = Grid(1,40,GREY) 
load_mines(MINE)
check_cell()
grid.draw_grid(grid._color)
cover_board()
font = pygame.font.SysFont("Arial Black",50)
 

run = True 
while run:
    play()  
    pygame.display.update()
pygame.quit()

    