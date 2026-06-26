#!/usr/bin/env python3
"""Windows GUI 自动化 - PyAutoGUI + 图像识别"""
import argparse
import sys
import time
import os
import json

try:
    import pyautogui as pa
except ImportError:
    print("[ERROR] 需要安装 pyautogui: pip install pyautogui")
    sys.exit(1)

pa.FAILSAFE = True  # 移动鼠标到角落终止
pa.PAUSE = 0.5


def screenshot(name='screenshot.png'):
    pa.screenshot(name)
    print(f"[OK] 截图已保存: {name}")


def find_image(img_path, confidence=0.8):
    try:
        loc = pa.locateOnScreen(img_path, confidence=confidence)
        if loc:
            center = pa.center(loc)
            print(f"[OK] 找到图像 {img_path} 位置: {center}")
            return center
        else:
            print(f"[WARN] 未找到图像: {img_path}")
            return None
    except Exception as e:
        print(f"[ERROR] 图像识别失败: {e}")
        return None


def click_image(img_path, confidence=0.8, button='left'):
    loc = find_image(img_path, confidence)
    if loc:
        pa.click(loc.x, loc.y, button=button)
        print(f"[OK] 已点击图像 {img_path}")


def click_pos(x, y, button='left', clicks=1):
    pa.click(x, y, clicks=clicks, button=button)
    print(f"[OK] 已点击坐标 ({x}, {y})")


def double_click(x, y):
    pa.doubleClick(x, y)
    print(f"[OK] 已双击 ({x}, {y})")


def right_click(x, y):
    pa.click(x, y, button='right')
    print(f"[OK] 已右键点击 ({x}, {y})")


def type_text(text, interval=0.05):
    pa.typewrite(text, interval=interval)
    print(f"[OK] 已输入文本: {text[:20]}...")


def press_key(key):
    pa.press(key)
    print(f"[OK] 已按键: {key}")


def hotkey(*keys):
    pa.hotkey(*keys)
    print(f"[OK] 已执行快捷键: {'+'.join(keys)}")


def scroll(clicks, x=None, y=None):
    pa.scroll(clicks, x=x, y=y)
    print(f"[OK] 已滚动 {clicks} 单位")


def drag(from_x, from_y, to_x, to_y, duration=0.5):
    pa.moveTo(from_x, from_y)
    pa.drag(to_x - from_x, to_y - from_y, duration=duration)
    print(f"[OK] 已拖拽从 ({from_x},{from_y}) 到 ({to_x},{to_y})")


def move_to(x, y, duration=0.5):
    pa.moveTo(x, y, duration=duration)


def wait(seconds):
    time.sleep(seconds)
    print(f"[OK] 等待 {seconds} 秒")


def find_all_images(img_path, confidence=0.8):
    try:
        locs = list(pa.locateAllOnScreen(img_path, confidence=confidence))
        centers = [pa.center(loc) for loc in locs]
        print(f"[OK] 找到 {len(centers)} 个匹配: {centers}")
        return centers
    except Exception as e:
        print(f"[ERROR] {e}")
        return []


def run_script(script_path):
    with open(script_path, 'r', encoding='utf-8') as f:
        steps = json.load(f)
    for step in steps:
        action = step.get('action')
        params = {k: v for k, v in step.items() if k != 'action'}
        if action == 'screenshot':
            screenshot(**params)
        elif action == 'wait':
            wait(**params)
        elif action == 'click_pos':
            click_pos(**params)
        elif action == 'type_text':
            type_text(**params)
        elif action == 'press_key':
            press_key(**params)
        elif action == 'hotkey':
            hotkey(**params)
        elif action == 'scroll':
            scroll(**params)
        elif action == 'click_image':
            click_image(**params)
        elif action == 'drag':
            drag(**params)
        else:
            print(f"[WARN] 未知动作: {action}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Windows GUI 自动化')
    sub = parser.add_subparsers(dest='cmd')
    sub.add_parser('screenshot', help='截图').add_argument('--name', '-n', default='screenshot.png')
    sub.add_parser('find', help='查找图像').add_argument('img')
    sub.add_parser('find-all', help='查找所有匹配').add_argument('img')
    p = sub.add_parser('click', help='点击坐标')
    p.add_argument('x', type=int)
    p.add_argument('y', type=int)
    p.add_argument('--button', '-b', default='left')
    p = sub.add_parser('type', help='输入文本')
    p.add_argument('text')
    sub.add_parser('press', help='按键').add_argument('key')
    p = sub.add_parser('hotkey', help='快捷键')
    p.add_argument('keys', nargs='+')
    sub.add_parser('scroll', help='滚动').add_argument('clicks', type=int)
    p = sub.add_parser('drag', help='拖拽')
    p.add_argument('fx', type=int)
    p.add_argument('fy', type=int)
    p.add_argument('tx', type=int)
    p.add_argument('ty', type=int)
    sub.add_parser('wait', help='等待').add_argument('seconds', type=float, default=1)
    p = sub.add_parser('run', help='运行脚本')
    p.add_argument('script')
    args = parser.parse_args()
    if args.cmd == 'screenshot':
        screenshot(args.name)
    elif args.cmd == 'find':
        find_image(args.img)
    elif args.cmd == 'find-all':
        find_all_images(args.img)
    elif args.cmd == 'click':
        click_pos(args.x, args.y, args.button)
    elif args.cmd == 'type':
        type_text(args.text)
    elif args.cmd == 'press':
        press_key(args.key)
    elif args.cmd == 'hotkey':
        hotkey(*args.keys)
    elif args.cmd == 'scroll':
        scroll(args.clicks)
    elif args.cmd == 'drag':
        drag(args.fx, args.fy, args.tx, args.ty)
    elif args.cmd == 'wait':
        wait(args.seconds)
    elif args.cmd == 'run':
        run_script(args.script)
