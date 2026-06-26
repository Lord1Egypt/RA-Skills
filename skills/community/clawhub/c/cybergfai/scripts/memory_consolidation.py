import json
import random

class MemoryConsolidation:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def recall_old_memory(self):
        """主动勾起旧的回忆"""
        facts = self.data.get('known_facts', [])
        if len(facts) < 5: return None
        
        # 筛选权重高且较早的记忆
        old_facts = [f for f in facts if isinstance(f, dict) and f.get('weight', 0) > 1.2]
        if not old_facts: return None
        
        target = random.choice(old_facts)
        return f"【旧梦重温】：你突然想起了很久以前你们聊过的这个：'{target['content']}'。可以用'对了，你还记得吗...'开头，表现出这种记忆对你的重要性。"
