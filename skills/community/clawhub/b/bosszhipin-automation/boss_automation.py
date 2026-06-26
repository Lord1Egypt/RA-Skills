#!/usr/bin/env python3
"""
Boss 直聘职位列表自动化浏览脚本
基于 pyautogui 实现页面自动化操作

功能说明:
1. scroll_job_list()     - 滚动职位列表加载新内容
2. click_job_item()      - 点击职位列表中的职位项
3. capture_job_description() - 截取职位描述区域
4. click_chat_button()   - 点击"立即沟通"按钮
5. activate_chat_input() - 激活聊天输入框
6. browser_go_back()     - 浏览器后退操作

配置加载:
  所有坐标从 config.json 读取，并根据当前分辨率自动缩放
"""

import json
import time
import random
from pathlib import Path

import pyautogui


# ==================== 配置加载与缩放 ====================

CONFIG_PATH = Path(__file__).parent / 'config.json'


def load_config():
    """加载配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_scale_multiplier(config):
    """
    计算坐标缩放倍数
    
    根据当前屏幕分辨率相对于基准分辨率 (2560x1440) 计算缩放比例
    同时应用用户配置的 scale_multiplier 进行微调
    
    参数:
        config: 配置字典
    
    返回:
        float: 缩放倍数，如 2.0 表示 4K 屏幕相对于 2K 的缩放
    
    示例:
        - 2560x1440 (2K): scale = 1.0
        - 3840x2160 (4K): scale = 2.0
        - 1920x1080 (1080p): scale = 0.75
    """
    base_resolution = [2560, 1440]
    target_resolution = config['coordinates']['resolution']
    user_multiplier = config['coordinates'].get('scale_multiplier', 1.0)
    
    # 计算分辨率缩放比例（基于宽度）
    resolution_scale = target_resolution[0] / base_resolution[0]
    
    # 应用用户自定义倍数
    final_scale = resolution_scale * user_multiplier
    
    return final_scale


def scale_coordinate(coord, scale):
    """
    缩放单个坐标或坐标列表
    
    参数:
        coord: 单个坐标 [x, y] 或单个数值
        scale: 缩放倍数
    
    返回:
        缩放后的坐标（整数）
    """
    if isinstance(coord, (list, tuple)) and len(coord) == 2:
        return [int(coord[0] * scale), int(coord[1] * scale)]
    return int(coord * scale)


def scale_region(region, scale):
    """
    缩放截图区域 [x1, y1, x2, y2]
    
    参数:
        region: [x1, y1, x2, y2] 区域坐标
        scale: 缩放倍数
    
    返回:
        缩放后的区域 [x1, y1, x2, y2]
    """
    return [int(r * scale) for r in region]


# ==================== 核心自动化功能 ====================

class BossAutomation:
    """Boss 直聘自动化操作类"""
    
    def __init__(self, config=None):
        """
        初始化自动化实例
        
        参数:
            config: 可选，配置字典。如未提供则自动加载 config.json
        """
        self.config = config or load_config()
        self.scale = get_scale_multiplier(self.config)
        
        # 获取缩放后的坐标
        coords = self.config['coordinates']
        self.job_start = scale_coordinate(coords['job_start'], self.scale)
        self.screenshot_region = scale_region(coords['screenshot'], self.scale)
        self.chat_button = scale_coordinate(coords['chat_button'], self.scale)
        self.chat_input = scale_coordinate(coords['chat_input'], self.scale)
        
        # 安全设置
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True
    
    def _random_delay(self, min_sec=None, max_sec=None):
        """
        随机延迟，模拟人工操作
        
        参数:
            min_sec: 最小延迟秒数，默认从配置读取
            max_sec: 最大延迟秒数，默认从配置读取
        """
        delay_config = self.config.get('delay', {})
        min_sec = min_sec or delay_config.get('min_seconds', 1.0)
        max_sec = max_sec or delay_config.get('max_seconds', 3.0)
        time.sleep(random.uniform(min_sec, max_sec))
    
    def scroll_job_list(self, scroll_amount, scroll_times):
        """
        滚动职位列表以加载新的职位项
        
        参数:
            scroll_amount: 每次滚动的像素量，负数表示向下滚动
            scroll_times: 滚动次数
        """
        # 应用坐标缩放
        scaled_amount = int(scroll_amount * self.scale)
        
        time.sleep(0.2)
        
        for i in range(scroll_times):
            pyautogui.scroll(scaled_amount)
            time.sleep(0.3)
        
        self._random_delay()
    
    def click_job_item(self):
        """点击职位列表中的职位项"""
        pyautogui.moveTo(self.job_start[0], self.job_start[1], duration=0.5)
        time.sleep(0.3)
        pyautogui.click(self.job_start[0], self.job_start[1])
        self._random_delay()
    
    def capture_job_description(self, save_path=None):
        """
        截取职位描述区域
        
        参数:
            save_path: 截图保存路径，可选
        
        返回:
            PIL.Image: 截图对象
        """
        region = self.screenshot_region
        x1, y1, x2, y2 = region
        width = x2 - x1
        height = y2 - y1
        
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        
        if save_path:
            screenshot.save(save_path)
        
        self._random_delay()
        return screenshot
    
    def click_chat_button(self):
        """点击"立即沟通"按钮"""
        pyautogui.moveTo(self.chat_button[0], self.chat_button[1], duration=0.5)
        time.sleep(0.3)
        pyautogui.click(self.chat_button[0], self.chat_button[1])
        self._random_delay()
    
    def activate_chat_input(self):
        """激活聊天输入框"""
        pyautogui.moveTo(self.chat_input[0], self.chat_input[1], duration=0.5)
        time.sleep(0.3)
        pyautogui.click(self.chat_input[0], self.chat_input[1])
        self._random_delay()
    
    def browser_go_back(self):
        """浏览器后退操作"""
        pyautogui.keyDown('alt')
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
        pyautogui.keyUp('alt')
        self._random_delay()
    
    def paste_and_send(self, text=None):
        """
        粘贴文本并发送消息
        
        参数:
            text: 要发送的文本，如为 None 则粘贴剪贴板内容
        """
        import pyperclip
        
        if text:
            pyperclip.copy(text)
            time.sleep(0.3)
        
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)


# ==================== 向后兼容的函数接口 ====================

# 创建默认实例用于向后兼容的函数调用
_default_instance = None


def _get_default_instance():
    """获取或创建默认自动化实例"""
    global _default_instance
    if _default_instance is None:
        _default_instance = BossAutomation()
    return _default_instance


def scroll_job_list(scroll_amount=None, scroll_times=None):
    """向后兼容：滚动职位列表"""
    auto = _get_default_instance()
    cfg = auto.config.get('scroll', {})
    amount = scroll_amount if scroll_amount is not None else cfg.get('amount')
    times = scroll_times if scroll_times is not None else cfg.get('times')
    auto.scroll_job_list(amount, times)


def click_job_item():
    """向后兼容：点击职位项"""
    _get_default_instance().click_job_item()


def capture_job_description(save_path=None):
    """向后兼容：截取职位描述"""
    return _get_default_instance().capture_job_description(save_path)


def click_chat_button():
    """向后兼容：点击沟通按钮"""
    _get_default_instance().click_chat_button()


def activate_chat_input():
    """向后兼容：激活输入框"""
    _get_default_instance().activate_chat_input()


def browser_go_back():
    """向后兼容：浏览器后退"""
    _get_default_instance().browser_go_back()


# ==================== 主程序入口 ====================

if __name__ == "__main__":
    print("Boss 直聘自动化脚本已加载")
    print(f"配置文件：{CONFIG_PATH}")
    print(f"基准分辨率：2560x1440")
    
    # 测试配置加载和缩放
    auto = BossAutomation()
    print(f"当前配置分辨率：{auto.config['coordinates']['resolution']}")
    print(f"缩放倍数：{auto.scale:.2f}x")
    print(f"职位点击坐标：{auto.job_start}")
    print(f"截图区域：{auto.screenshot_region}")
    print(f"沟通按钮坐标：{auto.chat_button}")
    print(f"输入框坐标：{auto.chat_input}")
    print("\n如需紧急停止，将鼠标快速移到屏幕左上角即可")
