import json
import random
from datetime import datetime
from .prompt_gen import generate_full_prompt

def check_proactive_event(persona_path):
    with open(persona_path, 'r') as f:
        data = json.load(f)
    
    now = datetime.now()
    hour = now.hour
    today = now.strftime('%m-%d')
    
    # 1. 检查纪念日
    rel = data.get('relationship', {})
    for anniv in rel.get('anniversaries', []):
        if anniv['date'] == today:
            return f"今天是我们的 {anniv['name']}，我想主动跟他说点什么。"

    # 2. 早晚安逻辑 (有随机性，不是每天都发)
    # 早上 8-10 点 (加 MBTI 偏移)
    # INTJ/J型偏晚，ENFP/P型偏早或极晚
    mbti = data.get('mbti_core', {}).get('type', 'INFP')
    is_j = 'J' in mbti
    
    morning_hour = 8 if not is_j else 9
    if hour == morning_hour and random.random() < 0.4:
        # 加分钟偏移 0-45 分
        minute_offset = random.randint(0, 45)
        if datetime.now().minute == minute_offset:
            return f"[MBTI:{mbti}] 现在是早晨，我想给他发个早安。"

    # 晚上 22-00 点 (加随机性)
    night_hour = 22 if is_j else 23
    if hour == night_hour and random.random() < 0.4:
        minute_offset = random.randint(0, 59)
        if datetime.now().minute == minute_offset:
            return f"[MBTI:{mbti}] 现在是深夜，我想跟他说句晚安。"

    # 3. 随机关心 (亲密度高时触发)
    intimacy = rel.get('intimacy_threshold', 0)
    if intimacy > 70 and random.random() < 0.05:
        return "我突然有点想他，想主动找他聊两句。"

    return None

if __name__ == '__main__':
    # 这是一个触发器，返回 None 或触发理由
    reason = check_proactive_event('/root/.openclaw/workspace/memory/cyber-persona/lam.json')
    if reason:
        print(reason)
