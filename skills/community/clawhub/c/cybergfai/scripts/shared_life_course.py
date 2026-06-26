import json
import os
from datetime import datetime

class SharedLifeCourse:
    def __init__(self, persona_path):
        self.persona_name = os.path.basename(persona_path).replace('.json', '')
        self.path = f"/root/.openclaw/workspace/memory/cyber-persona/life_course/{self.persona_name}.json"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f: json.dump([], f)

    def add_plan(self, plan_text):
        """记录共同的计划或目标"""
        with open(self.path, 'r') as f: plans = json.load(f)
        plan_entry = {
            "content": plan_text,
            "created_at": datetime.now().isoformat(),
            "status": "planned" # planned, ongoing, completed
        }
        plans.append(plan_entry)
        with open(self.path, 'w') as f: json.dump(plans, f, ensure_ascii=False, indent=2)

    def get_upcoming_plans(self):
        """获取正在计划中的共同事项"""
        with open(self.path, 'r') as f: plans = json.load(f)
        planned = [p for p in plans if p['status'] == 'planned']
        if not planned: return None
        
        import random
        target = random.choice(planned)
        return f"【共同生命历程】：你突然想起了你们之前计划过的这件事：'{target['content']}'。你要表现出对这件事的期待，或者问问他什么时候开始准备。这让你们的关系有了'未来感'。"
