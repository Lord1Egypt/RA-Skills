import json
import random

class ValuesSystem:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def get_opinions(self):
        """获取她的三观和坚持点"""
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')
        opinions = self.data.get('opinions', {})
        
        if not opinions:
            # 默认价值观初始化 (基于 MBTI)
            if 'N' in mbti:
                opinions = {"精神契合": "认为精神世界的共鸣远比物质生活重要。", "独立性": "即使在恋爱中也要保持彼此的独立空间。"}
            else:
                opinions = {"细节控": "认为爱体现在具体的生活细节中。", "稳定性": "向往脚踏实地、有规律的生活。"}
        
        output = "\n【核心价值观与固执点】：\n"
        for k, v in opinions.items():
            output += f"- {k}：{v}\n"
        return output

    def update_values(self, user_text):
        """根据长期的互动，潜移默化地对齐或冲突"""
        # 这是一个深层逻辑：如果用户长期表达某种观点，她会考虑接受或产生分歧
        pass # 待后续开发
