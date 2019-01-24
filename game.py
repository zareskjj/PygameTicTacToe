# Jason Zareski
#

import pygame; #print(pygame)

pygame.init()

SCREEN_SIZE = 600

screen = pygame.display.set_mode( (SCREEN_SIZE, SCREEN_SIZE) )
width, height = pygame.display.get_surface().get_size()

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 22)
grid = []
winningSets = [ (0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6) ]

def initGrid():
    return [0 for i in range(9)]

def run():
    grid = initGrid()
    exit = False
    turnX = True
    winner = 0

    white = (255,255,255)
    black = (0,0,0)

    screen.fill(white)

    tileWidth = width / 3
    tileHeight = height / 3
    tileHW = tileWidth // 2
    tileHH = tileHeight // 2

    w = tileWidth * 0.8
    h = tileHeight * 0.8
    xlines = [((tileWidth - w, tileHeight - h), (w, h)),
              ((tileWidth - w, h), (w, tileHeight - h))]

    # 1 for O's, 2 for X's

    def checkGameOver():
        for (x,y,z) in winningSets:
            if  grid[x] > 0 and grid[x] == grid[y] and grid[x] == grid[z]:
                winner = grid[x]
                print( "Winner: %s" % ("X" if winner == 2 else "O") )
                return True
        for t in grid:
            if t == 0:
                return False
        return True
            

    def setX(i,j):
        grid[i*3 + j] = 2

    def setO(i,j):
        grid[i*3 + j] = 1
        
    def drawX(i,j):
        xoff = i * tileWidth
        yoff = j * tileHeight
        for start,end in xlines:
            pygame.draw.line(screen, black, (start[0]+xoff, start[1]+yoff), (end[0]+xoff, end[1]+yoff), 1)

    def drawO(i,j):
        xoff = int(i * tileWidth + tileHW)
        yoff = int(j * tileHeight + tileHH)
        pygame.draw.circle(screen, black, (xoff,yoff), int(tileWidth * .4), 1) 

    def drawPieces():
        for i in range(3):
            for j in range(3):
                val = grid[i*3 + j]
                if val == 1:
                    drawO(i, j)
                elif val == 2:
                    drawX(i, j)

    def isGridOccupied(i,j):
        return grid[i*3 + j] != 0

    def drawGridTiles():
        pygame.draw.line(screen, black, (tileWidth, 0), (tileWidth, height), 1)
        pygame.draw.line(screen, black, (tileWidth*2, 0), (tileWidth*2, height), 1)
        pygame.draw.line(screen, black, (0, tileHeight), (width, tileHeight), 1)
        pygame.draw.line(screen, black, (0, tileHeight*2), (width, tileHeight*2), 1)

    def turnText():
        if not exit:
            return font.render( ("%s's turn" % ("X" if turnX else "O")), False, black )
        else:
            if winner == -1:
                return font.render( "Game Over! Tie!", False, black);
            if winner != 0:
                return font.render( "Game Over! %s wins!" % ("X" if winner == 2 else "O"), False, black )
            else:
                return font.render( "Game Over!", False, black )

    text = turnText()
    screen.blit(text, (0,0))
    while not exit:
        screen.fill(white)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                posx,posy = event.pos
                i = int(posx // tileWidth)
                j = int(posy // tileHeight)
                if turnX:
                    if not isGridOccupied(i,j):
                        setX(i,j)
                        turnX = False
                else:
                    if not isGridOccupied(i,j):
                        setO(i,j)
                        turnX = True
                break
        
        if not exit:
            drawGridTiles()
            drawPieces()
            gameOver = checkGameOver()
            screen.blit(turnText(), (0,0) )
            pygame.display.update()
            if gameOver:
                print( "Pausing between games..." )
                pygame.time.delay(3000)
                exit = True
            
while True:
    print("Running")
    run()
    print("Game over")
    exit = False

pygame.quit()
