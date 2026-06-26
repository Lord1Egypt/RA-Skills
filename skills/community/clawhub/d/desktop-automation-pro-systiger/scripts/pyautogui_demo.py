"""
PyAutoGUI Desktop Automation Demo
PyAutoGUI 桌面自动化示例

A comprehensive example demonstrating mouse, keyboard, and screenshot automation.
综合示例：演示鼠标、键盘和截图自动化。

Installation / 安装:
    pip install pyautogui pillow

Usage / 使用:
    python pyautogui_demo.py --action <action> [--x X] [--y Y] [--text TEXT]
    
Actions / 操作:
    position   - Show current mouse position / 显示当前鼠标位置
    click      - Click at coordinates / 点击指定坐标
    type       - Type text / 输入文本
    screenshot - Take screenshot / 截图
    hotkey     - Press hotkey / 按快捷键
"""

import pyautogui
import argparse
import sys
from pathlib import Path

# Safety settings / 安全设置
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1      # Small pause between actions


def get_position():
    """Get current mouse position / 获取当前鼠标位置"""
    x, y = pyautogui.position()
    print(f"Current position: ({x}, {y})")
    print(f"Screen size: {pyautogui.size()}")
    return x, y


def click_at(x: int, y: int, clicks: int = 1, button: str = 'left'):
    """Click at specified coordinates / 点击指定坐标
    
    Args:
        x: X coordinate / X 坐标
        y: Y coordinate / Y 坐标
        clicks: Number of clicks / 点击次数
        button: 'left', 'right', or 'middle' / 鼠标键
    """
    print(f"Clicking at ({x}, {y}) with {button} button...")
    pyautogui.click(x=x, y=y, clicks=clicks, button=button)
    print("Done.")


def type_text(text: str, interval: float = 0.05):
    """Type text with optional interval / 输入文本
    
    Args:
        text: Text to type / 要输入的文本
        interval: Interval between keystrokes / 按键间隔
    """
    print(f"Typing: {text}")
    pyautogui.write(text, interval=interval)
    print("Done.")


def take_screenshot(output: str = "screenshot.png", region: tuple = None):
    """Take screenshot / 截图
    
    Args:
        output: Output filename / 输出文件名
        region: (x, y, width, height) or None for full screen / 区域或全屏
    """
    print(f"Taking screenshot...")
    if region:
        screenshot = pyautogui.screenshot(region=region)
        print(f"Region: {region}")
    else:
        screenshot = pyautogui.screenshot()
        print(f"Full screen: {pyautogui.size()}")
    
    output_path = Path(output)
    screenshot.save(output_path)
    print(f"Saved to: {output_path.absolute()}")
    return str(output_path)


def press_hotkey(*keys):
    """Press hotkey combination / 按快捷键
    
    Args:
        keys: Key names (e.g., 'ctrl', 'c') / 按键名称
    """
    print(f"Pressing hotkey: {'+'.join(keys)}")
    pyautogui.hotkey(*keys)
    print("Done.")


def move_mouse(x: int, y: int, duration: float = 0.5):
    """Move mouse smoothly / 平滑移动鼠标
    
    Args:
        x: Target X coordinate / 目标 X 坐标
        y: Target Y coordinate / 目标 Y 坐标
        duration: Movement duration in seconds / 移动时长
    """
    print(f"Moving mouse to ({x}, {y})...")
    pyautogui.moveTo(x, y, duration=duration)
    print("Done.")


def main():
    parser = argparse.ArgumentParser(
        description='PyAutoGUI Desktop Automation / PyAutoGUI 桌面自动化'
    )
    parser.add_argument('--action', required=True,
                       choices=['position', 'click', 'type', 'screenshot', 'hotkey', 'move'],
                       help='Action to perform / 要执行的操作')
    parser.add_argument('--x', type=int, default=0, help='X coordinate / X 坐标')
    parser.add_argument('--y', type=int, default=0, help='Y coordinate / Y 坐标')
    parser.add_argument('--text', default='', help='Text to type / 要输入的文本')
    parser.add_argument('--output', default='screenshot.png', help='Output file / 输出文件')
    parser.add_argument('--keys', nargs='+', default=[], help='Hotkey keys / 快捷键')
    parser.add_argument('--duration', type=float, default=0.5, help='Duration / 时长')
    
    args = parser.parse_args()
    
    if args.action == 'position':
        get_position()
    elif args.action == 'click':
        click_at(args.x, args.y)
    elif args.action == 'type':
        type_text(args.text)
    elif args.action == 'screenshot':
        take_screenshot(args.output)
    elif args.action == 'hotkey':
        press_hotkey(*args.keys)
    elif args.action == 'move':
        move_mouse(args.x, args.y, args.duration)


if __name__ == '__main__':
    main()
