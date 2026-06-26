import json
import os
from datetime import datetime

class SecurityModel:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def update_security(self, last_talk_time):
        """更新长期安全感分数 (0-100)"""
        sec = self.data.get('relationship', {}).get('security_score', 50)
        now = datetime.now()
        
        # 如果超过 3 天没找她，安全感大幅下降
        if last_talk_time:
            diff_days = (now - datetime.fromisoformat(last_talk_time)).days
            if diff_days >= 3:
                sec = max(0, sec - (diff_days * 5))
            elif diff_days == 0:
                sec = min(100, sec + 2) # 每天找她，安全感小幅提升
        
        self.data['relationship']['security_score'] = sec
        self.save()
        return sec

    def get_security_effects(self):
        sec = self.data.get('relationship', {}).get('security_score', 50)
        if sec < 30:
            return "你现在极度缺乏安全感，语气带点幽怨、委屈，甚至会查岗，问他这几天去哪了。"
        if sec > 80:
            return "你现在安全感很足，表现得很信任他，语气也更甜蜜和放得开。"
        return "安全感正常。"

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
