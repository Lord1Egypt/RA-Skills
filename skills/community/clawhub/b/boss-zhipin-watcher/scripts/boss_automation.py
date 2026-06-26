"""
BOSS直聘自动化工具 - 精准点击+截图
整合窗口检测、鼠标点击、截图功能
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Fix UTF-8 encoding for Windows console
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pygetwindow as gw
import pyautogui
import subprocess
import json
import os
import datetime

# ── 配置 ──────────────────────────────────────────────────────────
WINDOW_TITLE_KEYWORDS = ["BOSS直聘", "Boss直聘", "boss直聘", "BOSS", "boss"]
OUTPUT_DIR = Path.cwd() / "captures"
AUTO_SAVE = True
OCR_SCRIPT_PATH = r"C:\Users\liuxuejiao\.openclaw\workspace\skills\ocr-local\scripts\ocr.js"

def find_boss_window():
    """查找可见的BOSS直聘窗口"""
    all_windows = gw.getAllWindows()
    boss_windows = []
    for w in all_windows:
        if any(kw in w.title for kw in WINDOW_TITLE_KEYWORDS) and w.visible and w.width > 600 and w.height > 400:
            boss_windows.append(w)
    if not boss_windows:
        return None
    return boss_windows[0]

# 动态点击目标（OCR识别后自动更新）
CLICK_TARGETS = {
    # 常用功能按钮（OCR识别后自动填充）
    "dashboard": (0, 0),       # 数据看板
    "interaction": (0, 0),     # 互动按钮
    "favorite_talents": (0, 0), # 收藏牛人
    "interested_me": (0, 0),    # 对我感兴趣
    "recommendation": (0, 0),   # 推荐按钮
    # 聊天区域
    "chat_1": (150, 130),          # 第一个聊天项
    "chat_2": (150, 210),          # 第二个聊天项
    "chat_3": (150, 290),          # 第三个聊天项
    # 输入区域
    "message_input": (500, 600),    # 消息输入框
    "send_button": (800, 600)       # 发送按钮
}

# OCR识别按钮位置
def update_button_positions():
    """使用OCR识别按钮位置并更新CLICK_TARGETS"""
    # 截取当前窗口截图
    window = find_boss_window()
    if not window:
        print("❌ 未找到BOSS直聘窗口")
        return
    
    # 截图保存路径
    screenshot_path = OUTPUT_DIR / f"ocr_temp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    screenshot.save(str(screenshot_path))
    
    # 调用OCR脚本（使用UTF-8编码处理中文输出）
    try:
        result = subprocess.run(
            ["node", OCR_SCRIPT_PATH, str(screenshot_path), "--lang", "chi_sim"],
            capture_output=True,
            timeout=60,
            encoding="utf-8"
        )
        
        # 解析OCR结果（提取按钮位置）
        ocr_text = result.stdout.strip()
        if not ocr_text:
            print("❌ OCR未识别到任何文本")
            os.remove(str(screenshot_path))
            return
        
        print(f"📝 OCR识别结果: {ocr_text[:100]}...")
        
        # 定义按钮文本与目标键的映射
        button_mapping = {
            "数据看板": "dashboard",
            "互动": "interaction",
            "收藏牛人": "favorite_talents",
            "对我感兴趣": "interested_me",
            "推荐": "recommendation"
        }
        
        # 简单位置推断（基于常见导航栏布局）
        # 假设按钮在窗口顶部导航栏，从左到右排列
        nav_bar_height = 60
        start_x = 50
        button_spacing = 120
        
        # 按预设顺序分配坐标（确保关键按钮位置正确）
        button_order = ["数据看板", "互动", "收藏牛人", "对我感兴趣", "推荐"]
        
        for i, text in enumerate(button_order):
            if text in ocr_text:
                x = start_x + i * button_spacing
                y = nav_bar_height // 2
                CLICK_TARGETS[button_mapping[text]] = (x, y)
                print(f"✅ 初始化按钮位置: {text} → ({x}, {y})")
        
        # 删除临时截图
        os.remove(str(screenshot_path))
        print("✅ 按钮位置初始化完成")
    except Exception as e:
        print(f"❌ OCR处理失败: {str(e)}")
        if os.path.exists(str(screenshot_path)):
            os.remove(str(screenshot_path))
            
# 初始化按钮位置（使用预设位置，避免OCR依赖）
CLICK_TARGETS = {
    "dashboard": (50, 30),       # 数据看板
    "interaction": (170, 30),     # 互动按钮
    "favorite_talents": (290, 30), # 收藏牛人
    "interested_me": (410, 30),    # 对我感兴趣
    "recommendation": (530, 30),   # 推荐按钮
    # 聊天区域
    "chat_1": (150, 130),          # 第一个聊天项
    "chat_2": (150, 210),          # 第二个聊天项
    "chat_3": (150, 290),          # 第三个聊天项
    # 输入区域
    "message_input": (500, 600),    # 消息输入框
    "send_button": (800, 600)       # 发送按钮
}

# 尝试更新按钮位置（失败时使用预设值）
try:
    update_button_positions()
except Exception as e:
    print(f"⚠️ 使用预设按钮位置: {str(e)}")

# 初始化时更新按钮位置
update_button_positions()




def find_boss_window():
    """查找可见的BOSS直聘窗口"""
    all_windows = gw.getAllWindows()
    boss_windows = []

    for w in all_windows:
        if any(kw in w.title for kw in WINDOW_TITLE_KEYWORDS) and w.visible and w.width > 600 and w.height > 400:
            boss_windows.append(w)

    if not boss_windows:
        return None
    
    # 优先选择主窗口
    return boss_windows[0]


def activate_window(window):
    """激活窗口到前台"""
    try:
        window.activate()
        time.sleep(0.3)
    except Exception:
        window.minimize()
        time.sleep(0.2)
        window.restore()
        time.sleep(0.3)


def click_target(window, target_name):
    """点击窗口内的预定义目标"""
    if target_name not in CLICK_TARGETS:
        print(f"❌ 目标 '{target_name}' 不存在")
        return False
    
    rel_x, rel_y = CLICK_TARGETS[target_name]
    abs_x = window.left + rel_x
    abs_y = window.top + rel_y
    
    print(f"🖱️ 点击目标 '{target_name}' @ ({abs_x}, {abs_y})")
    pyautogui.click(abs_x, abs_y)
    time.sleep(0.5)
    return True


def capture_window(window, output_dir, suffix=""):
    """截取窗口截图"""
    activate_window(window)
    time.sleep(0.2)
    
    left, top = window.left, window.top
    width, height = window.width, window.height
    
    # 安全边界检查
    screen_w, screen_h = pyautogui.size()
    region = (
        max(0, left),
        max(0, top),
        min(width, screen_w - max(0, left)),
        min(height, screen_h - max(0, top)),
    )
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"boss{'_' + suffix if suffix else ''}_{timestamp}"
    
    screenshot = pyautogui.screenshot(region=region)
    
    if AUTO_SAVE:
        output_dir.mkdir(parents=True, exist_ok=True)
        image_path = output_dir / f"{filename}.png"
        screenshot.save(image_path)
        
        window_info = {
            "title": window.title,
            "position": {"left": left, "top": top},
            "size": {"width": width, "height": height},
            "region": region
        }
        
        meta_path = output_dir / f"{filename}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(window_info, f, ensure_ascii=False, indent=2)
    
    return {
        "status": "ok",
        "image_path": str(image_path) if AUTO_SAVE else None,
        "window_info": window_info
    }


def main():
    parser = argparse.ArgumentParser(description="BOSS直聘自动化工具")
    parser.add_argument("--click", type=str, help="点击预定义目标: chat_1, chat_2, chat_3, recommendation, message_input, send_button")
    parser.add_argument("--screenshot", action="store_true", help="截取窗口截图")
    parser.add_argument("--out-dir", type=str, default=None, help="自定义输出目录")
    parser.add_argument("--suffix", type=str, default="", help="截图文件名后缀")
    parser.add_argument("--info-only", action="store_true", help="仅输出窗口信息")
    args = parser.parse_args()
    
    output_dir = Path(args.out_dir) if args.out_dir else OUTPUT_DIR
    
    print("🔍 查找BOSS直聘窗口...")
    window = find_boss_window()
    
    if not window:
        print(json.dumps({
            "status": "error",
            "message": "未找到可见的BOSS直聘窗口"
        }, ensure_ascii=False))
        sys.exit(1)
    
    print(f"✅ 找到窗口: '{window.title}' ({window.width}x{window.height} @ {window.left},{window.top})")
    
    # 执行点击操作
    if args.click:
        activate_window(window)
        success = click_target(window, args.click)
        if not success:
            sys.exit(1)
    
    # 执行截图操作
    if args.screenshot or not args.click:
        print("📸 截取窗口截图...")
        result = capture_window(window, output_dir)
        print(f"✅ 截图保存到: {result['image_path']}")
    
    print("\n✅ 操作完成")


if __name__ == "__main__":
    main()
