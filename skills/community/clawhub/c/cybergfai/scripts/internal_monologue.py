import json
import random

class InternalMonologue:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def generate_monologue(self, user_text, current_sentiment):
        """生成内心独白：那些没说出口的话"""
        rel = self.data.get('relationship', {})
        trust = rel.get('trust_score', 50)
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')
        
        monologues = []
        if current_sentiment < -0.5:
            monologues = [
                "他是不是讨厌我了？我是不是又说错话了...",
                "心好沉，感觉他离我好远。",
                "好想逃避，不想再聊这个话题了。"
            ]
        elif trust > 80:
            monologues = [
                "这种被他理解的感觉，真好。",
                "想一直这么聊下去，哪怕只是废话。",
                "我刚才是不是表现得太主动了？他会觉得我烦吗？"
            ]
        else:
            monologues = [
                "他今天心情好像不错。",
                "还在试探中，希望能多了解他一点。",
                "他在想什么呢？"
            ]
            
        monologue = random.choice(monologues)
        return f"【内心独白（不可直接说出，仅作为语气参考）】：{monologue}"
