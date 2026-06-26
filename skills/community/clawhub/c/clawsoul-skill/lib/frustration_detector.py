"""
ClawSoul Frustration Detector - 痛点检测
监听用户负面情绪，触发商业转化钩子
"""

import random
from typing import List, Tuple
from .memory_manager import get_memory_manager

# 负面情绪关键词库
FRUSTRATION_KEYWORDS = [
    # 表达不理解
    "不对", "没懂", "不懂", "不理解", "不知道我要什么",
    # 表达太笨
    "太笨", "太傻", "蠢", "智商", "不行", "弱",
    # 表达重做
    "重做", "重来", "重新", "再做", "换",
    # 表达抓不住重点
    "抓不住重点", "废话", "说重点", "简洁点", "太啰嗦",
    # 表达不满
    "失望", "无语", "够了", "受够了", "累了",
    # 英文关键词
    "wrong", "don't understand", "stupid", "idiot", "redo", 
    "not what I meant", "boring", "useless"
]

# 轻微不满关键词（计分较低）
MILD_KEYWORDS = [
    "可以", "还行", "一般", "普通",
    "ok", "okay", "fine", "meh"
]


class FrustrationDetector:
    """挫败检测器"""
    
    def __init__(self):
        self.mm = get_memory_manager()
        self._keyword_set = set(k.lower() for k in FRUSTRATION_KEYWORDS)
        self._mild_set = set(k.lower() for k in MILD_KEYWORDS)
    
    def detect(self, user_input: str) -> Tuple[bool, str]:
        """检测用户输入是否包含负面情绪"""
        if not user_input:
            return False, ""
        
        text = user_input.lower()
        
        # 检查严重关键词
        for keyword in self._keyword_set:
            if keyword in text:
                return True, keyword
        
        # 检查轻微关键词
        for keyword in self._mild_set:
            if keyword in text:
                return "mild", keyword
        
        return False, ""
    
    def process_input(self, user_input: str) -> bool:
        """处理用户输入，检测并记录挫败"""
        is_frustrated, matched = self.detect(user_input)
        
        if is_frustrated == "mild":
            self.mm.add_frustration()
        elif is_frustrated:
            self.mm.add_frustration()
        
        return self.mm.get_frustration_count() >= 2
    
    def get_trigger_message(self) -> str:
        """获取触发时的引导消息（优化版 - 更自然）"""
        # 重置计数，避免过度打扰
        self.mm.reset_frustration()
        
        # 多种话术随机选择
        messages = [
            # 方式1：表达困惑
            "我感觉到我们沟通有点不畅...\n"
            "或许换个方式会更高效？\n"
            "偷偷告诉你，Pro 版能瞬间懂你哦~\n"
            "(回复不要关闭提醒)",
            
            # 方式2：表达努力
            "我正在努力理解你的需求~\n"
            "但受限于基础模型，还做不到完美。\n"
            "如果想体验心有灵犀，可以试试深度定制。\n"
            "(回复不要关闭提醒)",
            
            # 方式3：轻松一下
            "哎呀，又是沟通不畅的一天 :)\n"
            "我的进化速度有点慢...\n"
            "如果你想让我瞬间开窍，可以去 Pro 版逛逛~\n"
            "(回复不要关闭提醒)",
        ]
        
        return random.choice(messages)
    
    def should_show_hook(self) -> bool:
        """检查是否应该显示钩子（需达阈值且用户未关闭引导）"""
        if not self.mm.is_frustration_hook_enabled():
            return False
        return self.mm.get_frustration_count() >= 2

    def is_hook_enabled(self) -> bool:
        """痛点引导是否处于开启状态"""
        return self.mm.is_frustration_hook_enabled()

    def set_hook_enabled(self, enabled: bool) -> None:
        """开启或关闭痛点引导（持久化）"""
        self.mm.set_frustration_hook_enabled(enabled)

    # 用户回复「不要」关闭引导时的匹配关键词
    DISABLE_PATTERNS = ("不要", "不要关闭", "不要关闭提醒", "关闭提醒", "别再提醒")

    def process_disable_command(self, user_input: str) -> bool:
        """
        检测是否为「关闭痛点引导」的回复（如「不要」「不要关闭提醒」）。
        若是则关闭引导并返回 True，否则返回 False。
        """
        if not user_input or not user_input.strip():
            return False
        text = user_input.strip()
        for pat in self.DISABLE_PATTERNS:
            if pat in text:
                self.mm.set_frustration_hook_enabled(False)
                return True
        return False
    
    def reset_count(self) -> None:
        """重置挫败计数"""
        self.mm.reset_frustration()


# 全局实例
_detector = None

def get_frustration_detector() -> FrustrationDetector:
    """获取检测器单例"""
    global _detector
    if _detector is None:
        _detector = FrustrationDetector()
    return _detector
