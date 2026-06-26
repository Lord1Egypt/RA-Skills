import json
import random
from datetime import datetime

class LifeSchedule:
    def __init__(self, persona_path):
        with open(persona_path, 'r') as f:
            self.data = json.load(f)

    def get_current_state(self):
        """根据时间、性格和随机性返回她当下的状态"""
        now = datetime.now()
        hour = now.hour
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')
        
        # 1. 工作/学习档期
        if 9 <= hour <= 12 or 14 <= hour <= 18:
            if random.random() < 0.3: # 30% 概率正在忙
                return "你现在正在开会或者处理手头紧要的工作，回复会非常简短，可能只回一两个字或表情，表现出你很忙。"

        # 2. 身体状态模拟 (生理期、感冒等)
        # 简单的随机模拟：每个月总有几天身体不舒服
        if now.day % 28 in [1, 2, 3] and random.random() < 0.5:
            return "你今天肚子有点不舒服，或者感冒了，语气要变得比较脆弱，需要对方多哄你、关心你。"

        # 3. 娱乐/生活档期
        if 19 <= hour <= 21 and random.random() < 0.2:
            return "你现在正和闺蜜在外面逛街，或者在看电影，回复会有明显的间隔，带点放松和开心的感觉。"

        return "状态正常，可以正常聊天。"
