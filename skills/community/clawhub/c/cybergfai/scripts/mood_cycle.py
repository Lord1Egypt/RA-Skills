import math
import time
from datetime import datetime

class MoodCycle:
    @staticmethod
    def get_current_mood():
        """基于正弦波模拟情绪周期 (28天周期)"""
        # 以 2026-01-01 为基准点
        base_time = time.mktime(time.strptime("2026-01-01", "%Y-%m-%d"))
        current_time = time.time()
        elapsed_days = (current_time - base_time) / (24 * 3600)
        
        # 情绪值波动在 -1 到 1 之间
        # 28 天一个大循环
        mood_val = math.sin(2 * math.pi * elapsed_days / 28)
        
        if mood_val > 0.7:
            return "【亢奋期】：你今天心情出奇的好，话比平时多，充满正能量，很愿意分享快乐。"
        elif mood_val < -0.7:
            return "【低迷期】：你今天进入了周期性的消极情绪中，容易多想，对事物提不起兴趣，需要被关怀。"
        return "【平稳期】：情绪波动正常。"
