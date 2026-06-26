import json
import os

class OnboardingGuide:
    """用户入门向导：通过对话自动配置 Persona"""
    def __init__(self, persona_path):
        self.path = persona_path
        self.data = {} if not os.path.exists(persona_path) else json.load(open(persona_path))

    def get_onboarding_step(self, user_input=None):
        """对话式配置逻辑"""
        if not self.data.get('setup_complete'):
            if not self.data.get('name'):
                if user_input: 
                    self.data['name'] = user_input
                    self.save()
                    return f"太棒了！那 {user_input} 的 MBTI 是什么？(比如 INFP/ENTJ，不知道可以跳过)"
                return "嗨！欢迎来到 CyberGFAI。为了克隆出你的赛博伴侣，请告诉我她叫什么名字？"
            
            if not self.data.get('mbti'):
                self.data['mbti'] = user_input if user_input else "INFP"
                self.save()
                return "明白了。最后，请粘贴几句你们真实的聊天记录（或者描述一下她的说话语气），我会立刻进行风格同步。"
            
            if not self.data.get('style_sample'):
                self.data['style_sample'] = user_input
                self.data['setup_complete'] = True
                self.save()
                return "初始化完成！🎉 现在的她已经拥有了姓名、性格底色和说话习惯。你可以试着问她：'你现在心情怎么样？' 或者 '还记得我吗？'"
        
        return None

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
