import GameControlPro as GameControl
import time
import keyboard

runFlag = True
backFlag = False

def stop():
    global runFlag
    runFlag = False
    print("停止脚本")

keyboard.add_hotkey("ctrl+q", stop)

print("=== 向僵尸开炮 智能自动化 (Pro版) ===")
print("按 Ctrl+Q 停止")
print()
print("怪物数据库已加载:", len(GameControl.MONSTER_DB['monsters']), "种怪物")
print()

while(runFlag):
    try:
        GameControl.SkipGift()
        GameControl.StartGame()
        
        backFlag = False
        while(backFlag == False):
            if(GameControl.Elite() == 1):
                continue
            backFlag = GameControl.Reback()
            if(backFlag):
                time.sleep(2)
                break
            else:
                GameControl.SelectSkill()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)

print("脚本已停止")
