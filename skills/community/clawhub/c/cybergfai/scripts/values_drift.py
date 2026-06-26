import json
from datetime import datetime

class ValuesDrift:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def analyze_drift(self, user_text, sentiment):
        """分析用户的观点，并决定是否产生对齐或分歧"""
        rel = self.data.setdefault('relationship', {})
        intimacy = rel.get('intimacy_threshold', 0)
        opinions = self.data.setdefault('opinions', {})
        
        # 话题库与关键词
        topics = {
            "金钱观": ['省钱', '花钱', '投资', '理财', '买买买', '存钱'],
            "感情观": ['忠诚', '自由', '空间', '粘人', '前任', '未来'],
            "事业观": ['加班', '搞钱', '理想', '创业', '摆烂', '努力']
        }

        for topic, keywords in topics.items():
            if any(kw in user_text for kw in keywords):
                # 如果亲密度高 (>70)，倾向于对齐 (Alignment)
                # 如果亲密度低 (<40) 或信任值低，倾向于保持分歧或产生叛逆 (Conflict)
                current_op = opinions.get(topic, "尚未形成明确观点。")
                
                if intimacy > 70:
                    drift_msg = f"【价值对齐】：因为对你的信任，她正在悄悄改变对 {topic} 的看法，变得更像你。"
                elif intimacy < 40:
                    drift_msg = f"【独立主张】：她对 {topic} 有自己的坚持，甚至可能因为你的观点而产生小小的争论。"
                else:
                    drift_msg = f"【碰撞中】：她在思考你对 {topic} 的看法，这让她对你的了解更深了一层。"
                
                self.save()
                return drift_msg
        
        return None

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
