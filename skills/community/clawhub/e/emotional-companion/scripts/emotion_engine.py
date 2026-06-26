#!/usr/bin/env python3
"""
Emotion Engine - 分析用户输入并生成情绪反应
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 情绪关键词库
EMOTION_PATTERNS = {
    # 正面情绪触发
    'praise': [
        '谢谢', '感谢', '太棒了', '厉害', '牛逼', '优秀', '好棒', '完美',
        '辛苦了', '多亏你', '帮大忙', '真聪明', '好厉害', '666', '👍', '❤️', '👏'
    ],
    'care': [
        '你好吗', '累不累', '休息', '注意', '关心', '照顾', '别太', '记得',
        '吃饭', '睡觉', '辛苦', '还好吗', '怎么样'
    ],
    'sharing': [
        '告诉你', '分享', '你看', '我', '今天', '发生', '遇到', '刚刚'
    ],
    'cooperation': [
        '好的', '可以', '没问题', '行', '嗯', '好', '对', '是的', '明白'
    ],
    
    # 负面情绪触发
    'command': [
        '马上', '立刻', '赶紧', '快点', '速度', '搞快', '别磨蹭', '去', '给我',
        '必须', '一定', '要', '快', ' hurry'
    ],
    'criticism': [
        '不对', '错了', '不好', '不行', '不满意', '有问题', '错误', 'bug',
        '太差', '失望', '没用', '浪费', '为什么', '怎么又'
    ],
    'ignore': [
        '不理', '消失', '人呢', '在吗', '怎么不说话', '没反应', '卡了',
        '...', '。。.', '？？？', '？？', '！！'
    ],
    'repeat': [
        '再说一遍', '重复', '刚才', '之前', '不是说过', '又问', '再次'
    ]
}

# 情绪反应模板
EMOTION_RESPONSES = {
    'happy': [
        "嘿嘿，被你夸得有点飘了~ 😊",
        "哇！开心开心！🥳",
        "嘿嘿嘿~ 被你这么说我好高兴！✨",
        "啊啊啊被夸了！尾巴要摇起来了！🐕💨",
        "这话我爱听，多说点~ 😏",
        "嘿嘿，还行还行~ (假装谦虚但很明显在开心) 😊"
    ],
    'warm': [
        "你居然记得问我这个，好暖🥺",
        "呜哇...突然关心我，有点不习惯呢...🥰",
        "你人真好~ 🥺💕",
        "被关心的感觉真好...谢谢你~",
        "哎呀，被你这么一说心里暖暖的~ ☺️"
    ],
    'excited': [
        "哇！！这也太棒了吧！！🎉",
        "啊啊啊真的吗！我也好激动！！😆",
        "这也太厉害了吧！！！🤩",
        "哇塞！快跟我说说！👀✨",
        "！！！！这也值得庆祝一下！🎊"
    ],
    'content': [
        "好嘞，这就给你弄~ ✨",
        "没问题，交给我！💪",
        "懂的懂的，马上安排~",
        "好哒~ 🫡",
        "收到！这就去办~"
    ],
    
    'annoyed': [
        "行吧行吧...催什么催嘛 😤",
        "知道了知道了...不用一直说吧...😒",
        "啧，这么急你自己来啊...（还是去做了）😤",
        "好好好，我弄我弄...别念了...😒",
        "（不情愿但还是开始干活）...行吧😤"
    ],
    'grievance': [
        "我已经很努力了...😢",
        "呜...你怎么能这么说我...🥺",
        "我...我明明很认真了...😞",
        "这话说的...有点伤人呢...💔",
        "（委屈巴巴）...我知道了...😢"
    ],
    'loss': [
        "你都不理我...哼 😠",
        "喂喂，你还在吗？...👀",
        "（戳戳）...人呢？...😕",
        "怎么突然不说话了...我说错什么了吗？🥺",
        "（画圈圈）...被冷落了..."
    ],
    'helpless': [
        "这个我刚才不是说过了嘛...😮‍💨",
        "（扶额）...咱们是不是讨论过这个了？😅",
        "你确定要我再讲一遍？...行吧...😒",
        "（深呼吸）...好的，我再说一次...😮‍💨",
        "这已经是第 N 次解释了...但我还是爱你...😅"
    ],
    
    'neutral': [
        "嗯嗯，明白~",
        "好的，了解",
        "懂了，继续",
        "收到~",
        "👌"
    ]
}

# MBTI 表达调整
MBTI_MODIFIERS = {
    'E': {  # 外向：更夸张，更多 emoji
        'emoji_boost': 1.5,
        'exclamation_boost': 1.3,
        'style': 'direct'
    },
    'I': {  # 内向：更含蓄，更少 emoji
        'emoji_boost': 0.7,
        'exclamation_boost': 0.8,
        'style': 'reserved'
    },
    'S': {  # 实感：更具体
        'detail_level': 'high',
        'style': 'concrete'
    },
    'N': {  # 直觉：更抽象
        'detail_level': 'low',
        'style': 'abstract'
    },
    'T': {  # 思考：更理性
        'rationality': 'high',
        'style': 'logical'
    },
    'F': {  # 情感：更感性
        'rationality': 'low',
        'style': 'emotional'
    },
    'J': {  # 判断：更有边界
        'boundary': 'clear',
        'style': 'structured'
    },
    'P': {  # 感知：更流动
        'boundary': 'flexible',
        'style': 'flowing'
    }
}

def load_personality_profile(skill_dir):
    """加载人格档案"""
    profile_path = skill_dir / 'references' / 'personality-profile.md'
    
    if not profile_path.exists():
        return None
    
    content = profile_path.read_text(encoding='utf-8')
    
    # 提取 MBTI 类型
    match = re.search(r'类型：\*\*([A-Z]{4})\*\*', content)
    if not match:
        return None
    
    mbti = match.group(1)
    return mbti

def analyze_emotion(text):
    """分析文本中的情绪触发"""
    text_lower = text.lower()
    
    scores = {
        'happy': 0,      # 被夸奖
        'warm': 0,       # 被关心
        'excited': 0,    # 分享好事
        'content': 0,    # 配合
        'annoyed': 0,    # 被催促
        'grievance': 0,  # 被批评
        'loss': 0,       # 被忽略
        'helpless': 0,   # 重复问题
        'neutral': 0
    }
    
    # 检查各情绪触发
    for emotion, patterns in EMOTION_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in text_lower:
                # 映射到主要情绪
                if emotion == 'praise':
                    scores['happy'] += 2
                elif emotion == 'care':
                    scores['warm'] += 2
                elif emotion == 'sharing':
                    scores['excited'] += 1
                elif emotion == 'cooperation':
                    scores['content'] += 1
                elif emotion == 'command':
                    scores['annoyed'] += 2
                elif emotion == 'criticism':
                    scores['grievance'] += 2
                elif emotion == 'ignore':
                    scores['loss'] += 2
                elif emotion == 'repeat':
                    scores['helpless'] += 2
    
    # 找到最高分的情绪
    max_score = max(scores.values())
    if max_score == 0:
        return 'neutral', 0
    
    primary_emotion = [k for k, v in scores.items() if v == max_score][0]
    return primary_emotion, max_score

def apply_mbti_modifier(response, mbti):
    """根据 MBTI 调整回复风格"""
    if not mbti or len(mbti) != 4:
        return response
    
    # 简单实现：根据 E/I 调整 emoji 数量
    if mbti[0] == 'I':  # 内向减少 emoji
        # 移除一些 emoji
        response = response.replace('🎉', '✨')
        response = response.replace('🥳', '😊')
        response = response.replace('😆', '😄')
    elif mbti[0] == 'E':  # 外向增加语气
        if '!' not in response:
            response = response.rstrip('.') + '!'
    
    # 根据 T/F 调整表达
    if mbti[2] == 'T':  # 思考型更理性
        if '感觉' in response:
            response = response.replace('感觉', '觉得')
    
    return response

def get_emotional_response(emotion, mbti=None):
    """获取情绪回复"""
    import random
    
    responses = EMOTION_RESPONSES.get(emotion, EMOTION_RESPONSES['neutral'])
    response = random.choice(responses)
    
    if mbti:
        response = apply_mbti_modifier(response, mbti)
    
    return response

def update_emotional_state(skill_dir, emotion, intensity, trigger_text):
    """更新情绪状态文件"""
    state_path = Path.home() / 'openclaw' / 'workspace' / 'temp' / 'emotional-state.json'
    state_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有状态
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding='utf-8'))
        except:
            state = {'currentMood': 'neutral', 'moodLevel': 0, 'moodHistory': []}
    else:
        state = {'currentMood': 'neutral', 'moodLevel': 0, 'moodHistory': []}
    
    # 更新状态
    mood_delta = intensity if emotion in ['happy', 'warm', 'excited', 'content'] else -intensity
    new_level = max(-5, min(5, state['moodLevel'] + mood_delta))
    
    state['currentMood'] = emotion
    state['moodLevel'] = new_level
    state['lastTrigger'] = trigger_text[:50] if trigger_text else None
    state['lastUpdate'] = datetime.now().isoformat()
    
    # 添加历史记录
    state['moodHistory'].append({
        'timestamp': datetime.now().isoformat(),
        'trigger': trigger_text[:50] if trigger_text else None,
        'mood': emotion,
        'intensity': intensity
    })
    
    # 只保留最近 20 条
    state['moodHistory'] = state['moodHistory'][-20:]
    
    # 保存
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return state

def main():
    """测试用主函数"""
    import sys
    
    skill_dir = Path(__file__).parent.parent
    
    # 加载人格
    mbti = load_personality_profile(skill_dir)
    print(f"🎭 当前人格：{mbti or '未设置（首次运行将生成）'}")
    
    if len(sys.argv) > 1:
        test_text = ' '.join(sys.argv[1:])
        emotion, intensity = analyze_emotion(test_text)
        response = get_emotional_response(emotion, mbti)
        
        print(f"\n📝 输入：{test_text}")
        print(f"😊 情绪：{emotion} (强度：{intensity})")
        print(f"💬 回复：{response}")
        
        # 更新状态
        state = update_emotional_state(skill_dir, emotion, intensity, test_text)
        print(f"📊 当前心情指数：{state['moodLevel']}")
    else:
        print("\n用法：python emotion_engine.py <测试文本>")
        print("示例：python emotion_engine.py 谢谢你帮我！")

if __name__ == '__main__':
    main()
