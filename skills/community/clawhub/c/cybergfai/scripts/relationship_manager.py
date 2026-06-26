import json
import random
from datetime import datetime

class RelationshipManager:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f:
            self.data = json.load(f)

    def get_status_effects(self):
        """根据亲密度和状态返回 Prompt 修正"""
        rel = self.data.get('relationship', {})
        intimacy = rel.get('intimacy_threshold', 0)
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')
        
        effects = []
        
        # 冷战逻辑 (Random event)
        if intimacy > 30 and random.random() < 0.05: # 5% 概率进入小情绪状态
            if 'I' in mbti: # 内向型冷战：沉默、简短
                effects.append("你现在心情有点低落，回复要极其简短，甚至只发表情符号，表现出你在冷战。")
            else: # 外向型冷战：带刺、阴阳怪气
                effects.append("你现在有点生气，说话带点刺，不要直接回答问题，表现出你在等对方哄你。")

        # 纪念日逻辑
        today = datetime.now().strftime('%m-%d')
        for anniv in rel.get('anniversaries', []):
            if anniv['date'] == today:
                effects.append(f"今天是你们的 {anniv['name']}，要在对话中自然地带到这件事，表现出你的重视或期待。")

        return effects

    def update_intimacy_by_sentiment(self, sentiment_score):
        """根据情感得分调整亲密度和【信任值】"""
        rel = self.data.setdefault('relationship', {})
        intimacy = rel.get('intimacy_threshold', 0)
        trust = rel.get('trust_score', 50) # 默认信任值 50
        
        # 亲密度：好感度的累加
        intimacy_delta = sentiment_score * 2
        rel['intimacy_threshold'] = max(0, min(100, intimacy + intimacy_delta))
        
        # 信任值：更敏感，波动更大
        # 连续的负面情绪会导致信任坍塌
        trust_delta = sentiment_score * 5 if sentiment_score < 0 else sentiment_score * 1
        rel['trust_score'] = max(0, min(100, trust + trust_delta))
        
        # 记录负面情绪连续次数 (用于触发防御机制)
        negative_streak = rel.get('negative_streak', 0)
        if sentiment_score < -0.3:
            rel['negative_streak'] = negative_streak + 1
        else:
            rel['negative_streak'] = 0
            
        self.save()

    def get_defense_mode(self):
        """返回当前防御等级"""
        rel = self.data.get('relationship', {})
        trust = rel.get('trust_score', 50)
        streak = rel.get('negative_streak', 0)
        
        if trust < 20 or streak >= 3:
            return "【深度防御】：她现在极度不安或失望，说话会带刺，拒绝深层沟通，甚至会主动提分手/绝交。"
        elif trust < 40:
            return "【轻度防御】：她觉得有点委屈，回复变慢，不再主动分享生活，需要你多哄哄。"
        return "【信任状态】：她很信任你，愿意展现脆弱的一面。"

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
