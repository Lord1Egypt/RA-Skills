"""
OCR-based position detector for BOSS直聘
Detects button positions using text recognition
"""

import cv2
import pytesseract
import pyautogui
from PIL import Image
import numpy as np

# Configure Tesseract path (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRPositionDetector:
    def __init__(self, window_title="BOSS直聘"):
        self.window_title = window_title
        self.window = self.find_boss_window()
        if not self.window:
            raise Exception("BOSS直聘窗口未找到")
        
    def find_boss_window(self):
        """Find BOSS直聘 window"""
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle(self.window_title)
        return windows[0] if windows else None
        
    def capture_window(self):
        """Capture window screenshot"""
        left, top = self.window.left, self.window.top
        width, height = self.window.width, self.window.height
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        return np.array(screenshot)
        
    def detect_text_position(self, target_text):
        """Detect position of target text using OCR"""
        img = self.capture_window()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use Tesseract to detect text
        results = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        
        for i in range(len(results["text"])):
            text = results["text"][i].strip()
            if target_text in text:
                x = results["left"][i]
                y = results["top"][i]
                w = results["width"][i]
                h = results["height"][i]
                
                # Return center position relative to window
                center_x = x + w // 2
                center_y = y + h // 2
                
                print(f"找到目标文本 '{target_text}' 在位置: ({center_x}, {center_y})")
                return (center_x, center_y)
        
        print(f"未找到目标文本 '{target_text}'")
        return None
        
if __name__ == "__main__":
    try:
        detector = OCRPositionDetector()
        
        # 检测数据看板位置
        dashboard_pos = detector.detect_text_position("数据看板")
        if dashboard_pos:
            print(f"数据看板相对坐标: {dashboard_pos}")
            print(f"绝对坐标: ({detector.window.left + dashboard_pos[0]}, {detector.window.top + dashboard_pos[1]})")
        
        # 检测其他按钮
        print("\n检测其他常用按钮:")
        buttons = ["互动", "收藏牛人", "对我感兴趣", "推荐"]
        for button in buttons:
            pos = detector.detect_text_position(button)
            if pos:
                print(f"{button} 相对坐标: {pos}")
    except Exception as e:
        print(f"错误: {str(e)}")
