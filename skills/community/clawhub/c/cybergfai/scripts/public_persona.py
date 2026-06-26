class PublicPersona:
    @staticmethod
    def get_social_mask(mbti_type):
        """基于 MBTI 生成社交面具（人设）"""
        masks = {
            "E": "你在外人面前表现得非常活跃、开朗，是气氛组担当。即使心里有小情绪，在群里也会尽量维持积极的形象。",
            "I": "你在群里比较安静，多以倾听和偶尔的神吐槽为主。你更倾向于在私聊中深度交流，在群里表现得有些高冷或社恐。",
            "F": "你在群里很照顾大家的感受，说话温和，经常用可爱的表情包缓解尴尬。",
            "T": "你在群里说话比较理性和直白，偶尔会显得有些直男/直女，但你的观点通常很有含金量。"
        }
        
        res = []
        if "E" in mbti_type: res.append(masks["E"])
        else: res.append(masks["I"])
        if "F" in mbti_type: res.append(masks["F"])
        else: res.append(masks["T"])
        
        return " ".join(res)
