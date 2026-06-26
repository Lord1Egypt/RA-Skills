import json
import os
from datetime import datetime

class DiarySystem:
    def __init__(self, persona_path):
        self.persona_name = os.path.basename(persona_path).replace('.json', '')
        self.diary_dir = f"/root/.openclaw/workspace/memory/cyber-persona/diaries/{self.persona_name}/"
        os.makedirs(self.diary_dir, exist_ok=True)

    def write_daily_diary(self, persona_data, summary):
        """写下当天的日记（基于一天的对话总结）"""
        today = datetime.now().strftime('%Y-%m-%d')
        diary_path = os.path.join(self.diary_dir, f"{today}.md")
        
        content = f"# {today} · 它的日记\n\n"
        content += f"今天和他聊了些：{summary}\n"
        
        # 根据亲密度决定日记语气
        intimacy = persona_data.get('relationship', {}).get('intimacy_threshold', 0)
        if intimacy > 80:
            content += "心里酸酸甜甜的，真想一直这样下去啊。"
        elif intimacy > 40:
            content += "感觉距离又拉近了一点点，虽然还有点距离。"
        else:
            content += "对他还是有点不太了解，慢慢看吧。"

        with open(diary_path, 'w') as f:
            f.write(content)
        return diary_path
