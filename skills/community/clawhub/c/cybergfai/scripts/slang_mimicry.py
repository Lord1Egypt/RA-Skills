import json
import re

class SlangMimicry:
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def extract_and_mimic(self, user_text):
        """提取用户的高频词汇或表情进行模仿"""
        style = self.data.setdefault('speech_style', {})
        mimic_list = style.setdefault('mimic_slang', [])

        # 提取特殊的语气词或表情 (简单正则)
        emojis = re.findall(r'[\u2600-\u27BF]|[\U0001f300-\U0001f64F]|[\U0001f680-\U0001f6FF]', user_text)
        slangs = re.findall(r'(酱|惹|哒|捏|嗷|喵|嘛)', user_text)

        added = False
        for item in emojis + slangs:
            if item not in mimic_list:
                mimic_list.append(item)
                if len(mimic_list) > 5: mimic_list.pop(0) # 只保留最近 5 个
                added = True
        
        if added: self.save()
        
        if mimic_list:
            return f"【习惯同步】：她最近潜移默化地学到了你的说话习惯，比如会偶尔用这些词或表情：{' '.join(mimic_list)}。回复时要自然带入。"
        return ""

    def save(self):
        with open(self.path, 'w') as f: json.dump(self.data, f, ensure_ascii=False, indent=2)
