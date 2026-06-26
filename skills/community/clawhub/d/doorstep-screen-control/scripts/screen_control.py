#!/usr/bin/env python3
"""
屏幕控制核心脚本：截图识别 + 鼠标操作
配合OpenClaw Node使用，实现远程屏幕操控
"""
import pyautogui
import mss
import numpy as np
from PIL import Image
import io
import base64
import json
import sys
import os

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

def screenshot():
    """截图返回base64"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 主屏幕
        img = sct.grab(monitor)
        img_pil = Image.frombytes("RGB", img.size, img.rgb)
        buf = io.BytesIO()
        img_pil.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode(), img_pil

def screenshot_to_file(path="screenshot.png"):
    """截图保存到文件"""
    with mss.mss() as sct:
        sct.shot(output=path)
    return path

def get_screen_size():
    """获取屏幕分辨率"""
    w, h = pyautogui.size()
    return {"width": w, "height": h}

def mouse_move(x, y):
    """移动鼠标到指定坐标"""
    pyautogui.moveTo(x, y)

def mouse_click(x, y, button="left", clicks=1):
    """在指定坐标点击"""
    pyautogui.click(x, y, button=button, clicks=clicks)

def mouse_double_click(x, y):
    """双击"""
    pyautogui.doubleClick(x, y)

def mouse_drag(start_x, start_y, end_x, end_y):
    """拖拽"""
    pyautogui.moveTo(start_x, start_y)
    pyautogui.drag(end_x - start_x, end_y - start_y, duration=0.3)

def type_text(text, interval=0.05):
    """键盘输入文字"""
    pyautogui.write(text, interval=interval)

def press_key(key):
    """按下按键"""
    pyautogui.press(key)

def hotkey(*keys):
    """组合键"""
    pyautogui.hotkey(*keys)

def scroll(clicks):
    """滚动鼠标"""
    pyautogui.scroll(clicks)

def locate_on_screen(image_path, confidence=0.8):
    """在屏幕上查找图片位置"""
    try:
        pos = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if pos:
            center = pyautogui.center(pos)
            return {"found": True, "x": int(center.x), "y": int(center.y), 
                    "width": int(pos.width), "height": int(pos.height)}
        return {"found": False}
    except Exception as e:
        return {"found": False, "error": str(e)}

def locate_text(text, screenshot_path=None):
    """
    在截图中定位文字（需要安装Tesseract OCR）
    需要安装: https://github.com/UB-Mannheim/tesseract/wiki
    安装后设置: TESSERACT_PATH 环境变量
    """
    try:
        import pytesseract
        
        tesseract_path = os.environ.get("TESSERACT_PATH")
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        if screenshot_path:
            img = Image.open(screenshot_path)
        else:
            b64, img = screenshot()
        
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang="chi_sim+eng")
        
        results = []
        for i in range(len(data["text"])):
            if text in data["text"][i]:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]
                results.append({
                    "text": data["text"][i],
                    "x": x, "y": y,
                    "width": w, "height": h,
                    "center_x": x + w//2,
                    "center_y": y + h//2
                })
        return results
    except ImportError:
        return [{"error": "pytesseract not installed"}]
    except Exception as e:
        return [{"error": str(e)}]

def click_text(text):
    """查找文字并点击"""
    results = locate_text(text)
    if results and "error" not in results[0]:
        target = results[0]
        pyautogui.click(target["center_x"], target["center_y"])
        return {"clicked": True, "x": target["center_x"], "y": target["center_y"]}
    return {"clicked": False, "reason": f"找不到文字: {text}"}

def get_pixel_color(x, y):
    """获取指定坐标的颜色"""
    color = pyautogui.pixel(x, y)
    return {"r": color[0], "g": color[1], "b": color[2]}

# ============ CLI入口 ============
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python screen_control.py <命令> [参数...]")
        print("命令列表:")
        print("  screenshot              - 截图并保存")
        print("  size                    - 获取屏幕尺寸")
        print("  move <x> <y>            - 移动鼠标")
        print("  click <x> <y> [button]  - 点击(按钮:left/right/middle)")
        print("  doubleclick <x> <y>     - 双击")
        print("  text <text>             - 输入文字")
        print("  key <key>               - 按键")
        print("  locate <image_path>     - 查找图片位置")
        print("  findtext <text>         - 查找文字位置")
        print("  clicktext <text>        - 查找并点击文字")
        print("  scroll <clicks>         - 滚动")
        print("  color <x> <y>           - 获取像素颜色")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "screenshot":
        path = screenshot_to_file()
        print(json.dumps({"path": path}))
    
    elif cmd == "size":
        print(json.dumps(get_screen_size()))
    
    elif cmd == "move" and len(sys.argv) >= 4:
        mouse_move(int(sys.argv[2]), int(sys.argv[3]))
        print(json.dumps({"ok": True}))
    
    elif cmd == "click" and len(sys.argv) >= 4:
        button = sys.argv[4] if len(sys.argv) > 4 else "left"
        mouse_click(int(sys.argv[2]), int(sys.argv[3]), button)
        print(json.dumps({"ok": True, "x": int(sys.argv[2]), "y": int(sys.argv[3])}))
    
    elif cmd == "doubleclick" and len(sys.argv) >= 4:
        mouse_double_click(int(sys.argv[2]), int(sys.argv[3]))
        print(json.dumps({"ok": True}))
    
    elif cmd == "text" and len(sys.argv) >= 3:
        type_text(sys.argv[2])
        print(json.dumps({"ok": True}))
    
    elif cmd == "key" and len(sys.argv) >= 3:
        press_key(sys.argv[2])
        print(json.dumps({"ok": True}))
    
    elif cmd == "locate" and len(sys.argv) >= 3:
        print(json.dumps(locate_on_screen(sys.argv[2])))
    
    elif cmd == "findtext" and len(sys.argv) >= 3:
        results = locate_text(sys.argv[2])
        print(json.dumps(results, ensure_ascii=False))
    
    elif cmd == "clicktext" and len(sys.argv) >= 3:
        print(json.dumps(click_text(sys.argv[2]), ensure_ascii=False))
    
    elif cmd == "scroll" and len(sys.argv) >= 3:
        scroll(int(sys.argv[2]))
        print(json.dumps({"ok": True}))
    
    elif cmd == "color" and len(sys.argv) >= 4:
        print(json.dumps(get_pixel_color(int(sys.argv[2]), int(sys.argv[3]))))
    
    else:
        print(json.dumps({"error": f"未知命令或参数不足: {cmd}"}))
