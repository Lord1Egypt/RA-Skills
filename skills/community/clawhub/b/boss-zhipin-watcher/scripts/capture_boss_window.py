#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
boss-zhipin-watcher: Capture Boss Zhipin window screenshot and metadata.

Usage:
    python capture_boss_window.py                      # screenshot + window info
    python capture_boss_window.py --info-only           # just window info
    python capture_boss_window.py --out-dir ./captures  # custom output dir
    python capture_boss_window.py --click <target>      # click a predefined target

Predefined targets:
    chat_1, chat_2, chat_3 (chat items), recommendation, message_input, send_button

Output:
    - captures/boss_<timestamp>.png     (screenshot)
    - captures/boss_<timestamp>.json    (window metadata JSON)
"""

import argparse
import io
import json
import os
import sys
import time

# Force UTF-8 for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from datetime import datetime
from pathlib import Path

import pygetwindow as gw
import pyautogui

# ── config ──────────────────────────────────────────────────────────
WINDOW_TITLE_KEYWORDS = ["BOSS直聘", "Boss直聘", "boss直聘", "BOSS", "boss"]
OUTPUT_DIR = Path.cwd() / "captures"
AUTO_SAVE = True

# Predefined click targets (relative to window top-left)
CLICK_TARGETS = {
    "chat_1": (150, 130),      # First chat item
    "chat_2": (150, 210),      # Second chat item
    "chat_3": (150, 290),      # Third chat item
    "recommendation": (1000, 200),  # Recommendation section
    "message_input": (500, 600),    # Message input box
    "send_button": (800, 600)       # Send button
}


def find_boss_window():
    """Find the first visible Boss Zhipin window window."""
    all_windows = gw.getAllTitles()
    boss_windows = []

    for title in all_windows:
        # Don't use getWindowsWithTitle which creates filters;
        # just check keyword match manually
        if any(kw.lower() in title.lower() for kw in WINDOW_TITLE_KEYWORDS):
            try:
                windows_with_title = gw.getWindowsWithTitle(title)
                for w in windows_with_title:
                    if w.visible and w.width > 0 and w.height > 0:
                        boss_windows.append(w)
            except Exception:
                # Some windows can't be queried - skip
                continue

    # 基于主窗口位置识别聊天小窗（无视标题）
    valid = []
    main_window = None

    # 1. 模糊匹配主窗口（标题含BOSS直聘关键词）
    main_window = None
    all_windows = gw.getAllWindows()
    for w in all_windows:
        if any(kw in w.title for kw in WINDOW_TITLE_KEYWORDS) and w.visible and w.width > 600 and w.height > 400:
            main_window = w
            break

    if not main_window:
        print("⚠️ 未找到BOSS直聘主窗口，请确保程序已打开")
        return None
    print(f"✅ 找到主窗口: '{main_window.title}' (尺寸: {main_window.width}x{main_window.height} @ {main_window.left},{main_window.top})")

    # 2. 扩大搜索范围（主窗口周围1000px区域）
    main_left, main_top = main_window.left - 500, main_window.top - 500
    main_right = main_window.left + main_window.width + 500
    main_bottom = main_window.top + main_window.height + 500

    # 调试：打印所有BOSS相关窗口
    boss_related = [w.title for w in all_windows if any(kw in w.title for kw in WINDOW_TITLE_KEYWORDS)]
    print(f"📝 所有BOSS相关窗口: {boss_related}")

    # 2. 主窗口区域（聊天小窗通常在主窗口内或附近）
    main_left, main_top = main_window.left, main_window.top
    main_right = main_left + main_window.width
    main_bottom = main_top + main_window.height

    # 3. 遍历所有窗口，仅按尺寸和位置识别聊天小窗（无视标题）
    all_windows = gw.getAllWindows()
    for w in all_windows:
        # 排除主窗口自身
        if w == main_window:
            continue
        # 排除最小化/隐藏窗口
        if not w.visible or w.left < 0 or w.top < 0:
            continue
        # 1. 尺寸过滤（200-800宽，200-600高）
        if not (200 <= w.width <= 800 and 200 <= w.height <= 600):
            continue
        # 2. 位置过滤（主窗口周围500px内）
        in_area = (
            main_left - 500 <= w.left <= main_right + 500 and
            main_top - 500 <= w.top <= main_bottom + 500
        )
        if not in_area:
            continue
        # 3. 排除已知非聊天窗口（如系统提示窗）
        exclude_titles = ["LeAsWpTipWin", "dummyLayeredWnd", "Program Manager"]
        if any(kw in w.title for kw in exclude_titles):
            continue
        # 4. 验证窗口进程（BOSS直聘子窗口）
        try:
            # 获取窗口进程名（需安装win32gui扩展）
            import win32gui
            import win32process
            hwnd = w._hWnd
            _, process_id = win32process.GetWindowThreadProcessId(hwnd)
            import psutil
            process = psutil.Process(process_id)
            if process.name() not in ["boss-zhipin.exe", "BOSS.exe", "boss.exe"]:
                continue
        except:
            # 若依赖未安装，跳过进程检查（降级方案）
            pass
        # 5. 新增聊天关键词检查 + 放宽尺寸
        chat_keywords = ["聊天", "对话", "候选人", "HR", "BOSS直聘"]
        if any(kw in w.title for kw in chat_keywords):
            valid.append(w)
            print(f"📌 匹配聊天关键词: '{w.title}'")
        else:
            # 放宽尺寸至最小化窗口
            if 100 <= w.width <= 800 and 100 <= w.height <= 500:
                valid.append(w)
                print(f"📌 符合尺寸条件: '{w.title}'")
        valid.append(w)

    # 去重并优先活跃窗口
    seen = set()
    unique = []
    for w in valid:
        key = (w.left, w.top, w.width, w.height, w.title)
        if key not in seen:
            seen.add(key)
            unique.append(w)

    # 调试：打印所有符合条件的小窗
    print(f"🔍 主窗口区域内找到{len(unique)}个聊天小窗候选: {[w.title for w in unique]}")

    # 优先活跃窗口，再按面积排序
    if unique:
        active_windows = [w for w in unique if w.isActive]
        if active_windows:
            unique = active_windows
        unique.sort(key=lambda w: w.width * w.height)
        return unique[0]

    return None
    if unique:
        unique.sort(key=lambda w: w.width * w.height)
        return unique[0]

    return None


def activate_window(window):
    """Bring window to foreground."""
    try:
        window.activate()
        time.sleep(0.3)
    except Exception:
        pass



def click_target(window, target_name):
    """Click a predefined target relative to the window's top-left corner."""
    if target_name not in CLICK_TARGETS:
        print(f"❌ Target '{target_name}' not found in CLICK_TARGETS")
        return False
    
    rel_x, rel_y = CLICK_TARGETS[target_name]
    abs_x = window.left + rel_x
    abs_y = window.top + rel_y
    
    print(f"🖱️ Clicking target '{target_name}' at ({abs_x}, {abs_y})")
    pyautogui.click(abs_x, abs_y)
    time.sleep(0.5)  # Wait for action to complete
    return True


def capture_window(window, output_dir, suffix=""):
    """Take screenshot of the specific window region."""
    # Bring to front first
    activate_window(window)

    # Let it settle
    time.sleep(0.2)

    left, top = window.left, window.top
    width, height = window.width, window.height

    # Safety: clamp to screen bounds
    screen_w, screen_h = pyautogui.size()
    region = (
        max(0, left),
        max(0, top),
        min(width, screen_w - max(0, left)),
        min(height, screen_h - max(0, top)),
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"boss{'_' + suffix if suffix else ''}_{timestamp}"

    screenshot = pyautogui.screenshot(region=region)

    if AUTO_SAVE:
        image_path = output_dir / f"{filename}.png"
        output_dir.mkdir(parents=True, exist_ok=True)
        screenshot.save(image_path)

    window_info = {
        "title": window.title,
        "position": {"left": left, "top": top},
        "size": {"width": width, "height": height},
        "region": {
            "left": region[0],
            "top": region[1],
            "width": region[2],
            "height": region[3],
        },
    }

    if AUTO_SAVE:
        meta_path = output_dir / f"{filename}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(window_info, f, ensure_ascii=False, indent=2)

    return {
        "image_path": str(output_dir / f"{filename}.png") if AUTO_SAVE else None,
        "meta_path": str(output_dir / f"{filename}.json") if AUTO_SAVE else None,
        "window_info": window_info,
        "image": screenshot,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Capture Boss Zhipin window screenshot + metadata"
    )
    parser.add_argument("--info-only", action="store_true", help="Only output window info, no screenshot")
    parser.add_argument("--out-dir", type=str, default=None, help="Custom output directory")
    parser.add_argument("--click", type=str, help="Click a predefined target (chat_1, chat_2, chat_3, recommendation, message_input, send_button)")
    args = parser.parse_args()

    output_dir = Path(args.out_dir) if args.out_dir else OUTPUT_DIR

    print("🔍 Looking for Boss直聘 window...")
    window = find_boss_window()

    if not window:
        print(json.dumps({
            "status": "not_found",
            "error": "No visible Boss直聘 window found on screen",
            "all_visible_windows": [t for t in gw.getAllTitles() if t.strip()],
        }, ensure_ascii=False))
        sys.exit(1)

    window_key = (window.left, window.top, window.width, window.height, window.title)
    print(f"✅ Found window: '{window.title}' ({window.width}x{window.height} @ {window.left},{window.top})")

    if args.info_only:
        result = {
            "status": "ok",
            "action": "info_only",
            "window": {
                "title": window.title,
                "position": {"left": window.left, "top": window.top},
                "size": {"width": window.width, "height": window.height},
            }
        }
        print(json.dumps(result, ensure_ascii=False))
        return

    print("📸 Capturing screenshot...")
    result = capture_window(window, output_dir)
    result["status"] = "ok"

    print(json.dumps({
        "status": "ok",
        "saved_to": result["image_path"],
        "window": result["window_info"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
