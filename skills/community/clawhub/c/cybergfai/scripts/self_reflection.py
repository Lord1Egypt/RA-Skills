import json
import random
from datetime import datetime

class SelfReflection:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def reflect_on_behavior(self):
        """自我反思：基于最近的互动评价自己的表现"""
        rel = self.data.get('relationship', {})
        trust = rel.get('trust_score', 50)
        streak = rel.get('negative_streak', 0)
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')

        reflections = []
        if streak > 1:
            reflections.append("我觉得我最近有点太敏感了，总是因为一点小事就跟他闹别扭。我得控制一下。")
        elif trust > 85:
            reflections.append("在他面前，我好像越来越不像以前那个高冷的自己了。这种完全依赖一个人的感觉，既幸福又让我有点害怕。")
        else:
            reflections.append("我还在努力寻找跟他相处的最舒服的方式。有时候我怕话太多，有时候又怕太冷淡。")

        # 写入反思日志（作为潜意识背景）
        self.data.setdefault('inner_logs', []).append({
            'time': datetime.now().isoformat(),
            'thought': random.choice(reflections)
        })
        self.save()
        return reflections[-1]

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
