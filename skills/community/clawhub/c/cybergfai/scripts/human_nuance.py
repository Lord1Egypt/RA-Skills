import json
import random
from datetime import datetime

class HumanNuance:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f:
            self.data = json.load(f)

    def get_nuance_effects(self):
        """返回增加真实感的小细节"""
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')
        now = datetime.now()
        effects = []

        # 1. 模拟撤回/纠错逻辑 (1% 概率)
        if random.random() < 0.01:
            effects.append("你待会儿发完消息，故意发一条带星号的纠错内容，比如 '*打错了'，模拟真实打字错误。")

        # 2. 回复延迟建议 (J型慢，P型快且碎)
        is_j = 'J' in mbti
        delay_min = 10 if is_j else 3
        delay_max = 30 if is_j else 10
        effects.append(f"模拟真实回复延迟：你现在打字需要大约 {random.randint(delay_min, delay_max)} 秒，不要秒回。")

        # 3. 28天情绪周期逻辑 (Mood Swing)
        day_of_cycle = now.day % 28
        if 13 <= day_of_cycle <= 15: # 周期波动期
            if 'F' in mbti:
                effects.append("你今天情绪特别敏感，容易胡思乱想，需要对方多关注你。")
            else:
                effects.append("你今天有点莫名的烦躁，不想多说话，回复要更冷淡一些。")

        return effects

if __name__ == '__main__':
    nuance = HumanNuance('/root/.openclaw/workspace/memory/cyber-persona/lam.json')
    print(nuance.get_nuance_effects())
