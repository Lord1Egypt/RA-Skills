class RhythmController:
    @staticmethod
    def get_rhythm_hint(user_text, history_len):
        """根据用户输入的密度决定回复节奏"""
        text_len = len(user_text)
        
        # 语义密度分析 (简单逻辑)
        if text_len > 100:
            return "对方发了一长串话，你也要认真回复，字数控制在 50-100 字，分段表达。"
        elif text_len < 5:
            return "对方回复很敷衍，你也可以稍微冷淡一点，或者发个表情包敷衍回去。"
        elif history_len > 10:
            return "聊得比较久了，可以适当引导结束话题或者换个轻松的姿势聊天。"
        
        return "保持正常的对话节奏，像真人一样自然。"