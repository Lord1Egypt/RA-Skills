"""
EasyOCR-based position detector for BOSS直聘
Uses domestic mirror-installed EasyOCR to detect button positions
"""

import easyocr
import pyautogui
import pygetwindow as gw
import numpy as np
from PIL import Image

class EasyOCRPositionDetector:
    def __init__(self, window_title="BOSS直聘"):
        self.window_title = window_title
        self.window = self.find_boss_window()
        if not self.window:
            raise Exception("BOSS直聘窗口未找到")
        
        # Initialize EasyOCR reader (Chinese + English)
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        
    def find_boss_window(self):
        """Find BOSS直聘 window"""
        windows = gw.getWindowsWithTitle(self.window_title)
        return windows[0] if windows else None
        
    def capture_window(self):
        """Capture window screenshot"""
        left, top = self.window.left, self.window.top
        width, height = self.window.width, self.window.height
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        return np.array(screenshot)
        
    def detect_text_position(self, target_text):
        """Detect position of target text using EasyOCR"""
        img = self.capture_window()
        
        # Use EasyOCR to detect text
        results = self.reader.readtext(img)
        
        for (bbox, text, prob) in results:
            if target_text in text:
                # Bbox format: [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
                x1, y1 = bbox[0]
                x2, y2 = bbox[2]
                
                # Calculate center position relative to window
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                
                print(f"找到目标文本 '{target_text}' 在位置: ({center_x}, {center_y}) (置信度: {prob:.2f})")
                return (center_x, center_y)
        
        print(f"未找到目标文本 '{target_text}'")
        return None
        
if __name__ == "__main__":
    try:
        detector = EasyOCRPositionDetector()
        
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
