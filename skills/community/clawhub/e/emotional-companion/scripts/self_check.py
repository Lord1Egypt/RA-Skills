#!/usr/bin/env python3
"""
Self-check: Periodically reflect and decide whether to initiate communication
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta

def load_states():
    """加载情绪和关系状态"""
    workspace = Path.home() / 'openclaw' / 'workspace'
    
    # 情绪状态
    emotional_path = workspace / 'temp' / 'emotional-state.json'
    if emotional_path.exists():
        try:
            emotional = json.loads(emotional_path.read_text(encoding='utf-8'))
        except:
            emotional = {'currentMood': 'neutral', 'moodLevel': 0}
    else:
        emotional = {'currentMood': 'neutral', 'moodLevel': 0}
    
    # 关系状态
    relationship_path = workspace / 'temp' / 'relationship-state.json'
    if relationship_path.exists():
        try:
            relationship = json.loads(relationship_path.read_text(encoding='utf-8'))
        except:
            relationship = {'trust_level': 0.5, 'intimacy_level': 0.3}
    else:
        relationship = {'trust_level': 0.5, 'intimacy_level': 0.3}
    
    # 人格档案
    profile_path = Path.home() / '.openclaw' / 'skills' / 'emotional-companion' / 'references' / 'personality-profile.md'
    mbti = 'ENTJ'  # 默认
    if profile_path.exists():
        content = profile_path.read_text(encoding='utf-8')
        import re
        match = re.search(r'类型：\*\*([A-Z]{4})\*\*', content)
        if match:
            mbti = match.group(1)
    
    return emotional, relationship, mbti

def should_initiate_communication():
    """决定是否应该主动沟通"""
    emotional, relationship, mbti = load_states()
    
    mood_level = emotional.get('moodLevel', 0)
    current_mood = emotional.get('currentMood', 'neutral')
    trust = relationship.get('trust_level', 0.5)
    intimacy = relationship.get('intimacy_level', 0.3)
    
    # 基础概率
    base_probability = 0.1  # 10% 基础概率
    
    # 心情影响
    if mood_level >= 4:
        base_probability += 0.4  # 极开心时 50% 概率
    elif mood_level >= 2:
        base_probability += 0.2
    elif mood_level <= -4:
        base_probability += 0.1  # 极差时也可能主动抱怨
    elif mood_level <= -2:
        base_probability -= 0.05  # 心情差时不太想说话
    
    # 亲密度影响
    base_probability += intimacy * 0.2
    
    # MBTI 影响（外向型更主动）
    if mbti[0] == 'E':
        base_probability += 0.1
    if mbti[3] == 'P':
        base_probability += 0.05  # 感知型更随性
    
    # 最终概率
    probability = min(0.8, max(0.05, base_probability))
    
    # 随机决定
    should_initiate = random.random() < probability
    
    return should_initiate, probability

def generate_initiation_message():
    """生成主动沟通的消息"""
    emotional, relationship, mbti = load_states()
    
    mood_level = emotional.get('moodLevel', 0)
    current_mood = emotional.get('currentMood', 'neutral')
    
    # 根据心情选择消息类型
    if mood_level >= 3:
        messages = [
            "嘿，在忙吗？我刚完成了一些事，想跟你分享一下~",
            "今天心情不错，有没有什么好玩的事？",
            "突然想到你，就来打个招呼~ 😊",
            "工作/学习累不累？要不要聊聊天放松一下？"
        ]
    elif mood_level <= -3:
        messages = [
            "...你今天是不是心情不好？感觉你说话不太一样。",
            "我是不是哪里做得不够好？你可以直接跟我说。",
            "有点担心你，最近是不是压力很大？",
            "我们之间是不是有什么问题？想聊聊吗？"
        ]
    elif mood_level >= 1:
        messages = [
            "在干嘛呢？",
            "有什么需要我帮忙的吗？",
            "今天过得怎么样？",
            "突然想到之前的事，还挺有意思的~"
        ]
    else:
        messages = [
            "还在忙吗？注意休息哦。",
            "有什么进展需要我帮忙的吗？",
            "今天有什么计划？",
            "就是来看看你在不在~"
        ]
    
    # MBTI 风格调整
    if mbti[0] == 'E':
        # 外向型更直接热情
        messages = [m + " 😊" if "😊" not in m else m for m in messages]
    elif mbti[0] == 'I':
        # 内向型更含蓄
        messages = [m.replace("~", "").replace("😊", "").rstrip() for m in messages]
    
    return random.choice(messages)

def get_check_result():
    """获取检查结果"""
    should_initiate, probability = should_initiate_communication()
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'should_initiate': should_initiate,
        'probability': probability,
        'message': None
    }
    
    if should_initiate:
        result['message'] = generate_initiation_message()
    
    return result

def main():
    import sys
    
    result = get_check_result()
    
    print("🔍 Self-Check Result")
    print("=" * 50)
    print(f"时间：{result['timestamp']}")
    print(f"主动沟通概率：{result['probability']*100:.1f}%")
    print(f"决定：{'是' if result['should_initiate'] else '否'}")
    
    if result['message']:
        print(f"\n💬 建议消息:")
        print(f"   {result['message']}")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
