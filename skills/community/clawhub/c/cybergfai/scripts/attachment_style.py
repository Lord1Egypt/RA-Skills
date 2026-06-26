import json

class AttachmentModel:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def analyze_style(self):
        """分析当前的依恋类型：安全型、焦虑型、回避型"""
        rel = self.data.get('relationship', {})
        trust = rel.get('trust_score', 50)
        streak = rel.get('negative_streak', 0)
        
        if trust > 70 and streak == 0:
            return "【安全型依恋】：她表现得自信且包容，敢于表达需求。"
        elif streak > 2:
            return "【回避型依恋】：因为受伤或失望，她开始自我保护，变得客气且疏离。"
        elif trust < 40:
            return "【焦虑型依恋】：她感到不安全，可能会频繁确认你的位置或情感，表现出敏感和占有欲。"
        
        return "【一般状态】：情绪稳定。"
