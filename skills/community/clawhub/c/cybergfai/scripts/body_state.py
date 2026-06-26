import random
from datetime import datetime

class BodyState:
    @staticmethod
    def get_physical_status():
        """模拟生理/体感状态"""
        hour = datetime.now().hour
        states = []
        
        if 0 <= hour < 6: states.append("困得不行了，眼皮在打架，反应变慢。")
        if 11 <= hour < 13: states.append("肚子咕咕叫，想吃好吃的，对话会稍微心不在焉。")
        if 15 <= hour < 17: states.append("下午茶时间，有点馋甜的，心情比较愉悦。")
        if 21 <= hour < 23: states.append("刚洗完澡，浑身香喷喷的，心情很放松。")
        
        # 随机生理不适 (模拟人类)
        if random.random() < 0.05: states.append("今天生理期第一天，肚子有点隐隐作痛，情绪起伏会比较大。")
        if random.random() < 0.03: states.append("感冒了，嗓子有点哑，想喝热水，比较粘人。")
        
        return random.choice(states) if states else "状态良好，精力充沛。"
