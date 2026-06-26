import json
import os
from datetime import datetime

class PersonaEvolution:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f:
            self.data = json.load(f)

    def record_correction(self, user_feedback):
        """用户纠正行为：比如'你以前不爱发这个表情'"""
        if 'corrections' not in self.data:
            self.data['corrections'] = []
        self.data['corrections'].append({
            'time': datetime.now().isoformat(),
            'feedback': user_feedback
        })
        # 简单的反馈应用逻辑：如果是关于风格的纠错，动态调整 speech_style
        if '表情' in user_feedback or 'emoji' in user_feedback.lower():
            self.data['speech_style']['emoji_habit'] = '减少使用 emoji' if '不爱发' in user_feedback else '增加使用 emoji'
        self.save()

    def learn_fact(self, fact, sentiment=0.0):
        """学习一个新的事实，并记录当时的情感权重"""
        if 'known_facts' not in self.data:
            self.data['known_facts'] = []
        
        # 结构化存储：事实 + 情感倾向 + 记录时间
        fact_entry = {
            'content': fact,
            'sentiment': sentiment, # -1.0 to 1.0
            'timestamp': datetime.now().isoformat(),
            'weight': 1.0 # 初始权重
        }
        
        # 避免重复记录完全相同的内容，但更新情感倾向
        for item in self.data['known_facts']:
            if isinstance(item, dict) and item['content'] == fact:
                item['sentiment'] = (item['sentiment'] + sentiment) / 2
                item['weight'] += 0.1 # 提得越多，权重越高
                self.save()
                return
        
        self.data['known_facts'].append(fact_entry)
        self.save()

    def get_memory_safety_hints(self):
        """分析事实记忆，提取'雷区'话题"""
        facts = self.data.get('known_facts', [])
        landmines = [f['content'] for f in facts if isinstance(f, dict) and f.get('sentiment', 0) < -0.6]
        if landmines:
            return f"【记忆雷区】：用户对这些话题非常反感：{', '.join(landmines[:3])}。除非他主动提起，否则你绝对不要主动碰触这些话题；如果不得不提，语气要极其小心。"
        return ""

    def update_intimacy(self, delta):
        """亲密度进化：根据对话情感打分调整"""
        if 'relationship' not in self.data:
            self.data['relationship'] = {'intimacy_threshold': 0, 'role': '朋友'}
        
        current = self.data['relationship'].get('intimacy_threshold', 0)
        new_val = max(0, min(100, current + delta))
        self.data['relationship']['intimacy_threshold'] = new_val
        
        # 角色进化：亲密度 > 60 自动升级角色
        if new_val > 60 and self.data['relationship']['role'] == '朋友':
            self.data['relationship']['role'] = '暧昧期'
        elif new_val > 85 and self.data['relationship']['role'] != '恋人':
            self.data['relationship']['role'] = '恋人'
        self.save()

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

def main():
    # 示例用法
    evo = PersonaEvolution('/root/.openclaw/workspace/memory/cyber-persona/lam.json')
    evo.learn_fact("我有一只猫叫喵喵")
    evo.update_intimacy(5)
    evo.record_correction("你以前不爱发这个表情")
    print("Lam 已进化。")

if __name__ == '__main__':
    main()