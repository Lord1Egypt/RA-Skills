"""
鼠标控制
"""

import pyautogui
import time
from typing import List, Tuple, Optional

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

class MouseController:
    """鼠标控制器"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        
        # 牌的位置配置（需要根据游戏调整）
        self.card_positions = {
            'my_cards_base': (500, 750),  # 我的第一张牌位置
            'card_spacing': 40,            # 牌间距
            'play_button': (960, 780),     # 出牌按钮
            'pass_button': (800, 780),     # 不出按钮
        }
    
    def move_to(self, x: int, y: int, duration: float = 0.2):
        """移动鼠标"""
        pyautogui.moveTo(x, y, duration=duration)
    
    def click(self, x: int = None, y: int = None, clicks: int = 1):
        """点击"""
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks)
        else:
            pyautogui.click(clicks=clicks)
    
    def select_cards(self, card_indices: List[int]):
        """
        选择牌
        card_indices: 牌的索引列表（从左到右0开始）
        """
        base_x, base_y = self.card_positions['my_cards_base']
        spacing = self.card_positions['card_spacing']
        
        for idx in card_indices:
            x = base_x + idx * spacing
            self.click(x, base_y)
            time.sleep(0.1)
    
    def click_play(self):
        """点击出牌"""
        x, y = self.card_positions['play_button']
        self.click(x, y)
    
    def click_pass(self):
        """点击不出"""
        x, y = self.card_positions['pass_button']
        self.click(x, y)
    
    def play_cards(self, card_indices: List[int]):
        """选择并出牌"""
        if not card_indices:
            self.click_pass()
            return
        
        self.select_cards(card_indices)
        time.sleep(0.2)
        self.click_play()
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取鼠标位置"""
        return pyautogui.position()
    
    def calibrate(self):
        """
        校准工具
        帮助设置牌的位置
        """
        print("=== 鼠标校准工具 ===")
        print("请按照提示操作...\n")
        
        positions = {}
        
        # 第一张牌
        input("将鼠标移到第一张牌位置，按回车...")
        positions['my_cards_base'] = self.get_mouse_position()
        print(f"第一张牌位置: {positions['my_cards_base']}")
        
        # 第二张牌
        input("将鼠标移到第二张牌位置，按回车...")
        pos2 = self.get_mouse_position()
        positions['card_spacing'] = pos2[0] - positions['my_cards_base'][0]
        print(f"牌间距: {positions['card_spacing']}")
        
        # 出牌按钮
        input("将鼠标移到出牌按钮位置，按回车...")
        positions['play_button'] = self.get_mouse_position()
        print(f"出牌按钮: {positions['play_button']}")
        
        # 不出按钮
        input("将鼠标移到不出按钮位置，按回车...")
        positions['pass_button'] = self.get_mouse_position()
        print(f"不出按钮: {positions['pass_button']}")
        
        self.card_positions = positions
        print("\n校准完成！")
        print(f"配置: {positions}")
        
        return positions


class AutoPlayer:
    """自动出牌（辅助功能）"""
    
    def __init__(self, controller: MouseController):
        self.controller = controller
        self.enabled = False
    
    def enable(self):
        """启用自动出牌"""
        self.enabled = True
        print("自动出牌已启用")
    
    def disable(self):
        """禁用自动出牌"""
        self.enabled = False
        print("自动出牌已禁用")
    
    def auto_play(self, card_indices: List[int], delay: float = 1.0):
        """自动出牌"""
        if not self.enabled:
            print("自动出牌未启用")
            return
        
        time.sleep(delay)
        self.controller.play_cards(card_indices)


if __name__ == "__main__":
    # 测试/校准
    mc = MouseController()
    mc.calibrate()
