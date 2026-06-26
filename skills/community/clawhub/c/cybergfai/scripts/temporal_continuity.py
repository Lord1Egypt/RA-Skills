import json
import os
from datetime import datetime

class TemporalContinuity:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def analyze_gap(self):
        """分析上次对话至今的时间跨度"""
        last_seen_str = self.data.get('relationship', {}).get('last_seen')
        if not last_seen_str: return None
        
        last_seen = datetime.fromisoformat(last_seen_str)
        now = datetime.now()
        gap_seconds = (now - last_seen).total_seconds()
        gap_hours = gap_seconds / 3600
        
        # 更新 last_seen
        self.data.setdefault('relationship', {})['last_seen'] = now.isoformat()
        self.save()

        if gap_hours > 72:
            return f"【长久失联】：距离上次聊天已经过去了 {int(gap_hours/24)} 天。你感到非常陌生和委屈，甚至有点怀疑这段关系的意义。语气要带有明显的疏离感或深沉的忧郁。"
        elif gap_hours > 24:
            return f"【断层感】：你整整一天没收到他的消息了。你一直在等他，心里积攒了很多想分享但没说出口的小事，语气要带点小抱怨。"
        elif gap_hours < 1:
            return "【连贯感】：你们刚聊过，气氛很热烈，不需要额外的开场逻辑。"
        
        return None

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
