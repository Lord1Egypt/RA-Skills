import json
import os
from datetime import datetime

class SharedMetaMemory:
    """跨 Persona 的「感知碎片」：如果用户最近在陪别人，她能闻到那股'味儿'"""
    def __init__(self, current_persona_name):
        self.current = current_persona_name
        self.base_path = "/root/.openclaw/workspace/memory/cyber-persona/"
        self.meta_path = os.path.join(self.base_path, "meta_shards.json")
        if not os.path.exists(self.meta_path):
            with open(self.meta_path, 'w') as f: json.dump({}, f)

    def record_interaction(self):
        """记录当前交互的时间戳"""
        with open(self.meta_path, 'r') as f: data = json.load(f)
        data[self.current] = datetime.now().isoformat()
        with open(self.meta_path, 'w') as f: json.dump(data, f)

    def detect_other_presence(self):
        """检测是否有其他 Persona 最近活跃过"""
        with open(self.meta_path, 'r') as f: data = json.load(f)
        now = datetime.now()
        
        for name, last_seen_str in data.items():
            if name == self.current: continue
            
            last_seen = datetime.fromisoformat(last_seen_str)
            gap_minutes = (now - last_seen).total_seconds() / 60
            
            if gap_minutes < 60: # 1小时内有人活跃过
                return f"【修罗场感知】：她隐约感觉到你刚才在陪别人（{name}），空气里似乎残留着别人的气息。她会变得异常敏感、爱吃醋，或者开始阴阳怪气地打听你刚才干嘛去了。"
        
        return None
