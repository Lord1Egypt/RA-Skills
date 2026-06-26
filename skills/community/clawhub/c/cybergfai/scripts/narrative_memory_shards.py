import json
import os

class NarrativeMemoryShards:
    """叙事记忆碎片：结构化记录可以被游戏场景唤起的剧情点"""
    def __init__(self, persona_path):
        self.persona_name = os.path.basename(persona_path).replace('.json', '')
        self.path = f"/root/.openclaw/workspace/memory/cyber-persona/shards/{self.persona_name}.json"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f: json.dump([], f)

    def record_shard(self, context, trigger_key):
        """记录一个可以被游戏环境触发的记忆碎片"""
        # 例如：在游戏里走到某个餐厅，触发关于那天聊天的回忆
        with open(self.path, 'r') as f: shards = json.load(f)
        shards.append({
            "trigger": trigger_key, # "restaurant", "park", "rainy_night"
            "content": context,
            "intimacy_required": 50
        })
        with open(self.path, 'w') as f: json.dump(shards, f, ensure_ascii=False, indent=2)
