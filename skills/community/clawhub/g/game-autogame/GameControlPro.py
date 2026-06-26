import win32helper
import pyautogui
import rapidocrhelper
from loguru import logger
from datetime import datetime
import json
import os

pyautogui.FAILSAFE = False
logger.add("file_{time}.log")

# 加载怪物数据库
MONSTER_DB_PATH = os.path.join(os.path.dirname(__file__), "monsters.json")
with open(MONSTER_DB_PATH, 'r', encoding='utf-8') as f:
    MONSTER_DB = json.load(f)

# 构建怪物名称到推荐技能的映射
MONSTER_SKILL_MAP = {}
for monster in MONSTER_DB['monsters']:
    MONSTER_SKILL_MAP[monster['name']] = monster.get('recommended', '')

# 技能优先级（当无法识别怪物时使用）
DEFAULT_PRIORITY = ['高能射线', '冰暴发生器', '电磁穿刺', '温压弹', '无人机', '干冰弹', '连发+']

handle = win32helper.GetHandle('向僵尸开炮')
winX, winY, winWidth, winHeight = win32helper.GetWin(handle)

# 开始游戏
def StartGame():
    win32helper.ShotAll(handle)
    x, y = rapidocrhelper.GetPoint('开始游戏')
    if x > 0 and y > 0:
        pyautogui.click(winX + x, winY + y)
        return True

# 返回
def Reback():
    win32helper.ShotAll(handle)
    x, y = rapidocrhelper.GetPoint('返回')
    if x > 0 and y > 0:
        pyautogui.click(winX + x, winY + y)
        return True

# 获取当前屏幕所有文字
def GetAllText():
    win32helper.ShotAll(handle)
    return rapidocrhelper.GetAll()

# 获取全部技能
def GetSkill():
    win32helper.ShotSkill(handle)
    return rapidocrhelper.GetAll()

# 精英掉落
def Elite():
    win32helper.ShotElite(handle)
    x, y = rapidocrhelper.GetPoint('精英掉落')
    if x > 0 and y > 0:
        pyautogui.click(winX + winWidth * 0.5, winY + winHeight * 0.5)
        return 1
    return 0

# 识别当前怪物
def DetectMonster():
    texts = GetAllText()
    if texts is None:
        return None
    
    detected_monsters = []
    for text in texts.keys():
        if text in MONSTER_SKILL_MAP:
            detected_monsters.append(text)
            logger.info(f"检测到怪物: {text}")
    
    if detected_monsters:
        return detected_monsters[0]  # 返回第一个匹配的怪物
    return None

# 根据怪物推荐技能
def GetRecommendedSkill(monster_name):
    if monster_name and monster_name in MONSTER_SKILL_MAP:
        return MONSTER_SKILL_MAP[monster_name]
    return None

# 选择技能（智能版）
def SelectSkill():
    currentSkills = GetSkill()
    if currentSkills is None:
        logger.warning("未检测到技能")
        pyautogui.click(winX + winWidth / 2, winY + winHeight / 2)
        return
    
    # 尝试识别当前怪物
    monster = DetectMonster()
    recommended_skill = GetRecommendedSkill(monster)
    
    if monster:
        logger.info(f"当前怪物: {monster}, 推荐技能: {recommended_skill}")
    
    # 遍历可用技能
    selected = False
    if recommended_skill:
        # 优先选择推荐的技能
        for key, value in currentSkills.items():
            if recommended_skill in key:
                x, y = value
                pyautogui.click(winX + x, winY + winHeight / 2)
                logger.info(f"选择推荐技能: {key}")
                selected = True
                break
    
    if not selected:
        # 使用默认策略
        for key, value in currentSkills.items():
            logger.info(f"技能: {key}")
            if '连' in key or '齐' in key:
                x, y = value
                pyautogui.click(winX + x, winY + winHeight / 2)
                logger.info(f"选择(连/齐): {key}")
                selected = True
                break
            elif '子弹' in key and '电磁' not in key and '火焰' not in key and '急冻' not in key:
                x, y = value
                pyautogui.click(winX + x, winY + winHeight / 2)
                logger.info(f"选择(子弹): {key}")
                selected = True
                break
    
    if not selected:
        # 默认选中间
        pyautogui.click(winX + winWidth / 2, winY + winHeight / 2)
        logger.info("选择(默认): 中间")

# 处理0点的限时礼包
def SkipGift():
    now = datetime.now()
    formatted_time = now.strftime("%H:%M")
    if formatted_time > '00:00' and formatted_time < '00:10':
        win32helper.ShotAll(handle)
        list = rapidocrhelper.GetAll()
        if list.get('限时礼包', '限时礼包') != '限时礼包':
            pyautogui.click(winX + winWidth * 0.81, winY + winHeight * 0.24)
