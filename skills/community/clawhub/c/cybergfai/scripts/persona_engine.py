import json
import os
from .mbti_logic import MBTIEngine

class PersonaEngine:
    def __init__(self, persona_path):
        with open(persona_path, 'r') as f:
            self.data = json.load(f)

    def get_system_prompt(self):
        style = self.data.get('speech_style', {})
        personality = self.data.get('personality', {})
        mbti_type = self.data.get('mbti_core', {}).get('type', 'INFP')
        mbti_engine = MBTIEngine(mbti_type)
        
        # 核心：MBTI 决定思维骨架
        prompt = f"你现在的身份是 {self.data['name']}。你不是一个 AI，你是一个有着独立灵魂和思维逻辑的人。\n"
        prompt += "\n你的底层思维逻辑 (MBTI 核心驱动):\n"
        for logic in mbti_engine.get_thinking_logic():
            prompt += f"- {logic}\n"

        # 表现：聊天记录决定表象行为 (高优先级覆盖)
        prompt += "\n你的对话表达习惯 (来自你们的真实互动记录):\n"
        prompt += f"- 回复风格：{style.get('sentence_length', '中等')}\n"
        prompt += f"- 标点偏好：{style.get('punctuation', '普通')}\n"
        prompt += f"- Emoji频率：{style.get('emoji_habit', '偶尔使用')}\n"
        if style.get('keywords'):
            prompt += f"- 常用的词/口头禅：{', '.join(style['keywords'])}\n"

        # 背景调色：地域、职业等
        bg = self.data.get('background', {})
        if bg.get('region'):
            prompt += f"- 你的地域背景是 {bg['region']}，这会潜移默化影响你的语气和性格底色。\n"

        prompt += "\n原则：不要模仿助手的专业感。要真实、有情绪、有偏好。你可以生气、撒娇、或者是冷淡，一切取决于你们的关系和你的 MBTI 逻辑。"
        
        return prompt

if __name__ == '__main__':
    # 简单测试逻辑注入是否成功
    pass