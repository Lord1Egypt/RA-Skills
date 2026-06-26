"""
屏幕截图和牌识别
"""

import cv2
import numpy as np
from PIL import Image
import pyautogui
from typing import List, Tuple, Optional, Dict
import os

class ScreenCapture:
    """屏幕截图"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        
    def capture_full(self) -> np.ndarray:
        """全屏截图"""
        img = pyautogui.screenshot()
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    def capture_region(self, x: int, y: int, w: int, h: int) -> np.ndarray:
        """区域截图"""
        img = pyautogui.screenshot(region=(x, y, w, h))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    def find_game_window(self, template_path: str = None) -> Optional[Tuple[int, int, int, int]]:
        """查找游戏窗口位置"""
        # 默认全屏
        return (0, 0, self.screen_width, self.screen_height)


class CardRecognizer:
    """牌识别器"""
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = template_dir
        self.templates: Dict[int, np.ndarray] = {}
        self.load_templates()
        
        # 游戏区域配置（需要根据实际游戏调整）
        self.regions = {
            'my_cards': (400, 700, 800, 100),      # 我的牌
            'left_cards': (50, 300, 200, 300),     # 左边玩家
            'right_cards': (1100, 300, 200, 300),  # 右边玩家
            'played_cards': (400, 400, 800, 150),  # 出牌区域
            'landlord_icon': (600, 200, 50, 50),   # 地主图标
        }
    
    def load_templates(self):
        """加载卡牌模板"""
        # 牌值映射
        card_values = {
            '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
            'K': 13, 'A': 14, '2': 15, 'joker_s': 16, 'joker_b': 17
        }
        
        # 尝试加载模板
        for name, value in card_values.items():
            for suit in ['', '_heart', '_spade', '_club', '_diamond']:
                path = os.path.join(self.template_dir, f"{name}{suit}.png")
                if os.path.exists(path):
                    self.templates[value] = cv2.imread(path)
                    break
    
    def recognize_cards(self, image: np.ndarray, region: str = 'my_cards') -> List[int]:
        """
        识别区域内的牌
        使用模板匹配或OCR
        """
        x, y, w, h = self.regions.get(region, (0, 0, image.shape[1], image.shape[0]))
        roi = image[y:y+h, x:x+w]
        
        cards = []
        
        # 方法1: 模板匹配
        if self.templates:
            for card_value, template in self.templates.items():
                result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
                locations = np.where(result >= 0.8)
                for _ in zip(*locations):
                    cards.append(card_value)
        
        # 方法2: 颜色检测（简化版）
        if not cards:
            cards = self._detect_by_color(roi)
        
        return sorted(cards, reverse=True)
    
    def _detect_by_color(self, image: np.ndarray) -> List[int]:
        """通过颜色检测牌（简化版）"""
        # 这里用颜色直方图等简单方法
        # 实际应用中建议用训练好的模型或更精确的模板
        cards = []
        
        # 转灰度
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 二值化
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # 找轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤并识别每个牌区域
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 30 and h > 40:  # 牌的大小过滤
                # 这里应该调用OCR或模板匹配
                pass
        
        return cards
    
    def recognize_played_cards(self, image: np.ndarray) -> Tuple[str, List[int]]:
        """
        识别出牌区域的牌
        返回: (玩家位置, 出的牌列表)
        """
        # 简化：检测哪个位置有牌打出
        roi = image[400:550, 400:1200]
        cards = self.recognize_cards(roi, 'played_cards')
        
        # 判断是哪个玩家出的
        # 可以通过牌的位置判断
        return 'unknown', cards
    
    def recognize_landlord(self, image: np.ndarray) -> str:
        """识别地主位置"""
        # 检测地主图标
        for pos, region in [('left', (50, 200, 100, 100)), 
                            ('me', (600, 650, 100, 50)),
                            ('right', (1150, 200, 100, 100))]:
            x, y, w, h = region
            roi = image[y:y+h, x:x+w]
            # 检测地主标记（颜色或图标）
            # 这里简化处理
        return 'me'  # 默认


class GameScreenScanner:
    """游戏屏幕扫描器"""
    
    def __init__(self):
        self.capture = ScreenCapture()
        self.recognizer = CardRecognizer()
        
    def scan(self) -> dict:
        """
        扫描游戏屏幕
        返回游戏状态
        """
        image = self.capture.capture_full()
        
        return {
            'my_cards': self.recognizer.recognize_cards(image, 'my_cards'),
            'left_cards_count': self._count_cards(image, 'left_cards'),
            'right_cards_count': self._count_cards(image, 'right_cards'),
            'played_cards': self.recognizer.recognize_played_cards(image),
            'landlord': self.recognizer.recognize_landlord(image),
            'screenshot': image
        }
    
    def _count_cards(self, image: np.ndarray, region: str) -> int:
        """计算某区域的牌数"""
        x, y, w, h = self.recognizer.regions.get(region, (0, 0, 100, 100))
        roi = image[y:y+h, x:x+w]
        
        # 简化：检测牌背面的数量
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        return len([c for c in contours if cv2.contourArea(c) > 500])
    
    def save_screenshot(self, path: str = "logs/screenshot.png"):
        """保存截图"""
        image = self.capture.capture_full()
        cv2.imwrite(path, image)


# 用于调试和模板生成
def generate_template(image_path: str, card_region: Tuple[int, int, int, int], output_name: str):
    """从截图中生成卡牌模板"""
    img = cv2.imread(image_path)
    x, y, w, h = card_region
    template = img[y:y+h, x:x+w]
    cv2.imwrite(f"templates/{output_name}.png", template)
    print(f"模板已保存: templates/{output_name}.png")


if __name__ == "__main__":
    # 测试
    scanner = GameScreenScanner()
    state = scanner.scan()
    print(f"我的牌: {state['my_cards']}")
    print(f"地主: {state['landlord']}")
