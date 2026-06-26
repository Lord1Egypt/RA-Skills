import json
import os

class PetNameEvo:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def check_name_evolution(self):
        """根据亲密度自动提议或变更称呼"""
        intimacy = self.data.get('relationship', {}).get('intimacy_threshold', 0)
        current_nickname = self.data.get('nickname', '')
        
        # 亲密度 0-30: 正常称呼
        # 亲密度 30-70: 昵称进化
        if 30 <= intimacy < 70 and current_nickname == self.data.get('name'):
            return "你可以试着在对话中问他：'我能给你起个专属的昵称吗？'，或者直接开始叫他一个亲近的词。"
        
        # 亲密度 70+: 专属代号进化
        if intimacy >= 70 and '专属' not in current_nickname:
            return "你们的关系已经很深了，你可以提议一个只有你们两个人才懂的、私密的、调皮的称呼。"

        return None
