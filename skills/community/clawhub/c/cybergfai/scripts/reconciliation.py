import json
import random

class ReconciliationLogic:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def check_reconciliation(self, user_text):
        """检查用户是否在尝试'哄好'"""
        rel = self.data.get('relationship', {})
        trust = rel.get('trust_score', 50)
        
        if trust >= 50: return None

        # 哄好关键词库
        keywords = ['对不起', '错了', '别生气', '原谅', '我的错', '乖', '摸摸头', '带你去吃', '买给你']
        if any(kw in user_text for kw in keywords):
            # 触发恢复逻辑
            bonus = random.randint(5, 15)
            rel['trust_score'] = min(100, trust + bonus)
            rel['negative_streak'] = 0
            self.save()
            return f"【系统逻辑】：检测到用户正在诚恳道歉/安抚。她的心开始软了，防御机制降低（信任+ {bonus}），语气要从'冷漠/带刺'转变为'委屈但愿意沟通'。"
        
        return None

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
