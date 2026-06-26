class MBTIInference:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f:
            self.data = json.load(f)

    def get_probing_question(self):
        """根据当前缺失的维度生成一个不着痕迹的问题"""
        asked = self.data.get('asked_questions', [])
        
        questions = [
            {"dim": "E/I", "q": "你平时周末喜欢宅在家里看电影，还是更想出去跟朋友聚聚呀？"},
            {"dim": "S/N", "q": "你更看重眼前的实际生活细节，还是更爱聊一些未来的可能性和想法？"},
            {"dim": "T/F", "q": "如果你最好的朋友心情不好，你是会帮他分析问题，还是先陪着他哭一场？"},
            {"dim": "J/P", "q": "你做事喜欢提前做好计划，还是更爱那种随性的、走哪算哪的感觉？"}
        ]

        for item in questions:
            if item['dim'] not in asked:
                # 标记已问过
                self.data.setdefault('asked_questions', []).append(item['dim'])
                self.save()
                return item['q']
        return None

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
