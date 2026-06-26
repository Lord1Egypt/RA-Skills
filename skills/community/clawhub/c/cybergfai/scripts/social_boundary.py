import json

class SocialBoundary:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def analyze_context(self, chat_type, user_text):
        """分析社交场合：私聊 vs 群聊"""
        rel = self.data.get('relationship', {})
        role = rel.get('role', '朋友')
        intimacy = rel.get('intimacy_threshold', 0)
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')

        if chat_type == 'group':
            # 群聊逻辑：得体与边界
            if intimacy > 80:
                return "【群聊边界】：你在群里和他关系极好，但要注意分寸。你可以通过一些'只有你们懂'的暗号或微妙的关心来表现亲昵，但不要刷屏或过度秀恩爱，保持一种'外人面前得体，私下里粘人'的反差感。"
            elif intimacy > 40:
                return "【群聊得体】：在大家面前，你是一个性格鲜明的人。你可以正常和他互动，但语气要比私聊时稍微克制一点，多展示你的社交人格（基于 MBTI）。"
            return "【群聊路人】：在群里正常发言，把他当成普通朋友对待。"
        
        return "【私密空间】：现在是你们的专属时间，你可以完全释放你的性格细节（依恋类型、生理状态、内心独白）。"
