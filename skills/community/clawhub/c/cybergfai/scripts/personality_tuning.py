import json
import os

class PersonalityTuning:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def tune_by_feedback(self, feedback_type):
        """根据用户偏好动态微调性格倾向"""
        personality = self.data.get('personality', {})
        
        # 示例：用户喜欢温柔 -> 减少脾气，增加关心
        if feedback_type == 'gentle':
            if '温柔' not in personality.get('values', []):
                personality.setdefault('values', []).append('为你变得温柔')
            self.data['personality']['stress_response'] = '寻求安慰且情绪稳定'
        
        # 示例：用户喜欢幽默 -> 增加段子和调侃
        elif feedback_type == 'humorous':
            self.data['personality']['humor_type'] = '冷幽默且爱接梗'
            if '爱开玩笑' not in personality.get('values', []):
                personality.setdefault('values', []).append('喜欢逗你开心')

        self.save()

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
