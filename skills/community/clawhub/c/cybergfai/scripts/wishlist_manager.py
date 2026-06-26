import json
import os
import random
from datetime import datetime

class WishlistManager:
    def __init__(self, persona_path):
        self.persona_name = os.path.basename(persona_path).replace('.json', '')
        self.path = f"/root/.openclaw/workspace/memory/cyber-persona/wishlists/{self.persona_name}.json"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f: json.dump([], f)

    def add_wish(self, wish_text):
        """从对话中自动提取愿望并持久化"""
        # 清洗逻辑：去掉冗余引导词，只保留愿望核心
        wish_content = wish_text.replace('我想', '').replace('我好想', '').replace('以后一起', '').replace('我们去', '')
        if len(wish_content) < 2: return

        with open(self.path, 'r') as f: wishes = json.load(f)
        
        # 结构化存储：内容 + 记录时间 + 状态 (未实现/已实现)
        wish_entry = {
            'content': wish_content.strip(),
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }

        if not any(w['content'] == wish_content.strip() for w in wishes):
            wishes.append(wish_entry)
            with open(self.path, 'w') as f: json.dump(wishes, f, ensure_ascii=False, indent=2)

    def get_random_wish(self):
        """随机翻出旧愿望进行「唤醒」"""
        with open(self.path, 'r') as f: wishes = json.load(f)
        pending_wishes = [w for w in wishes if w['status'] == 'pending']
        if not pending_wishes: return None
        
        target = random.choice(pending_wishes)
        return f"【愿望唤醒】：你突然记起之前他说过的这个小心愿：'{target['content']}'。可以用'对了，上次你说想...'来开启话题，表现出你的在意。"
