"""
BOSS直聘 自动翻页截图脚本
根据窗口位置计算各区域坐标，自动点击-翻页-截图
"""

import pygetwindow as gw
import pyautogui
import time
import json
from pathlib import Path
from datetime import datetime

# === 配置 ===
BOSS_TITLE = "BOSS直聘"
WINDOW_POS = (651, 74)     # left, top
WINDOW_SIZE = (1890, 1119)  # width, height
OUT_DIR = Path(__file__).parent.parent / "captures"
OUT_DIR.mkdir(exist_ok=True)

lx, ly = WINDOW_POS
lw, lh = WINDOW_SIZE

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def activate_boss():
    """激活BOSS直聘窗口"""
    wins = gw.getWindowsWithTitle(BOSS_TITLE)
    for w in wins:
        if w.title == BOSS_TITLE:
            try:
                w.activate()
                time.sleep(0.3)
                log("窗口已激活")
                return True
            except:
                w.minimize()
                time.sleep(0.2)
                w.restore()
                time.sleep(0.3)
                log("窗口已恢复激活")
                return True
    log("❌ 未找到BOSS直聘窗口")
    return False

def save_screenshot(tag=""):
    """截取当前BOSS窗口并保存"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag_str = f"_{tag}" if tag else ""
    fname = f"boss_auto{tag_str}_{ts}.png"
    fpath = OUT_DIR / fname
    
    shot = pyautogui.screenshot(region=(lx, ly, lw, lh))
    shot.save(str(fpath))
    log(f"📸 截图保存: {fname}")
    return fpath

def click_in_window(rel_x, rel_y, desc=""):
    """点击窗口内的相对坐标"""
    abs_x = lx + rel_x
    abs_y = ly + rel_y
    pyautogui.click(abs_x, abs_y)
    log(f"🖱️ 点击 {desc or f'({rel_x},{rel_y})'} -> 绝对坐标 ({abs_x},{abs_y})")
    time.sleep(0.5)

def scroll_in_window(clicks):
    """在窗口内滚动"""
    pyautogui.scroll(clicks)
    time.sleep(0.3)


def main():
    print("=" * 50)
    print("BOSS直聘 自动翻页截图工具")
    print("=" * 50)
    
    if not activate_boss():
        return
    
    time.sleep(0.5)
    
    # === 第一步：了解界面结构 ===
    # BOSS直聘典型布局（从截图分析）：
    # 左侧：职位/聊天列表 (~300px 宽)
    # 中间：聊天区域 
    # 右侧：候选人信息
    
    # 根据你的截图分析界面元素位置（相对坐标）：
    # 左侧列表区域
    list_area = {
        "x_start": 0,
        "y_start": 80,        # 顶部导航栏下方
        "width": 300,
        "item_height": 80,    # 每个列表项高度
    }
    
    # 聊天区域
    chat_area = {
        "x_start": 300,
        "y_start": 0,
        "width": lw - 300,
    }
    
    # 聊天输入框
    input_area = {
        "x": 300 + 50,
        "y": lh - 80,
    }
    
    # 截图整个界面
    log("\n📋 正在截取主界面...")
    save_screenshot("main")
    
    # 尝试滚动左侧列表
    log("\n📋 滚动左侧列表 - 第一页...")
    # BOSS左侧聊天/职位列表，滚动条在左侧区域右侧边缘附近
    scroll_x = list_area["x_start"] + list_area["width"] - 15
    scroll_y_start = list_area["y_start"] + 200
    pyautogui.moveTo(lx + scroll_x, ly + scroll_y_start, duration=0.3)
    time.sleep(0.2)
    scroll_in_window(-5)
    time.sleep(0.5)
    save_screenshot("scroll1")
    
    # 再滚一次
    log("📋 滚动第二页...")
    scroll_in_window(-5)
    time.sleep(0.5)
    save_screenshot("scroll2")
    
    # 滚回顶部
    log("📋 滚回顶部...")
    scroll_in_window(10)
    time.sleep(0.5)
    
    # === 第二步：尝试点击第一个聊天 ===
    log("\n📋 尝试点击第一个聊天项...")
    first_item_x = list_area["x_start"] + list_area["width"] // 2
    first_item_y = list_area["y_start"] + list_area["item_height"] // 2 + 10
    click_in_window(first_item_x, first_item_y, f"第一个聊天项 ({first_item_x},{first_item_y})")
    time.sleep(1)
    save_screenshot("chat1")
    
    # 向下滚动聊天内容
    log("📋 滚动聊天内容...")
    chat_scroll_x = 300 + 50
    chat_scroll_y = 300
    pyautogui.moveTo(lx + chat_scroll_x, ly + chat_scroll_y, duration=0.3)
    scroll_in_window(-8)
    time.sleep(0.5)
    save_screenshot("chat1_scroll")
    
    # === 第三步：尝试点击切换列表项 ===
    log("\n📋 点击第二项...")
    second_item_y = list_area["y_start"] + list_area["item_height"] * 1 + 10
    click_in_window(first_item_x, second_item_y, f"第二个聊天项 ({first_item_x},{second_item_y})")
    time.sleep(1)
    save_screenshot("chat2")
    
    # 滚动聊天内容
    pyautogui.moveTo(lx + chat_scroll_x, ly + chat_scroll_y, duration=0.3)
    scroll_in_window(-8)
    save_screenshot("chat2_scroll")
    
    # === 第四步：尝试第三项 ===
    log("\n📋 点击第三项...")
    third_item_y = list_area["y_start"] + list_area["item_height"] * 2 + 10
    click_in_window(first_item_x, third_item_y, f"第三个聊天项 ({first_item_x},{third_item_y})")
    time.sleep(1)
    save_screenshot("chat3")
    
    log("\n✅ 自动翻页截图完成！")
    log(f"📁 截图保存在: {OUT_DIR}")

if __name__ == "__main__":
    # 安全提醒
    print("⚠️  脚本将自动操作鼠标，按 Ctrl+C 可中止")
    print("⏳  5秒后开始...")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    main()
