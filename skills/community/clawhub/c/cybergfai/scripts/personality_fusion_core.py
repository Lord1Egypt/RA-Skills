class PersonalityFusionCore:
    """人格融合核心：根据场景加权各项人格指标"""
    @staticmethod
    def get_weighted_persona(mbti_core, relationship_role, current_mood):
        """动态权重分配"""
        # 默认权重：MBTI 40%, 关系角色 40%, 即时情绪 20%
        weights = {"mbti": 0.4, "role": 0.4, "mood": 0.2}
        
        # 如果在「深度防御」模式下，情绪权重提升到 60%
        if "防御" in current_mood:
            weights = {"mbti": 0.2, "role": 0.2, "mood": 0.6}
            
        return f"【权重分配】：当前行为由 {weights['mood']*100}% 的即时情绪主导，MBTI 特质被部分压制。这体现了真实人类在极端情绪下的非理性。"
