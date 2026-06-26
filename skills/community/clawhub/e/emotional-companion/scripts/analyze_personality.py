#!/usr/bin/env python3
"""
Analyze conversation history to generate comprehensive personality profile
including MBTI, Big Five, Enneagram, Attachment Style, and EQ profile.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 人格分析模式库
PATTERNS = {
    # MBTI 维度
    'E_I': {
        'E': ['聊聊', '一起玩', '分享', '讨论', '你觉得', '你怎么看', '大家', '一起', '社交', '热闹'],
        'I': ['我自己', '安静', '思考', '一个人', '不想说话', '独处', '内心', '反思', '私人']
    },
    'S_N': {
        'S': ['具体', '细节', '实际', '步骤', '现在', '这里', '经验', '现实', '实用', '操作'],
        'N': ['可能', '未来', '想象', '概念', '抽象', '本质', '理论', '创新', '模式', '全局']
    },
    'T_F': {
        'T': ['逻辑', '分析', '合理', '效率', '客观', '应该', '原则', '标准', '正确', '错误'],
        'F': ['感觉', '喜欢', '开心', '难过', '在乎', '温暖', '感受', '关系', '和谐', '理解']
    },
    'J_P': {
        'J': ['计划', '安排', '完成', '截止', '必须', '一定', '目标', '组织', '结构', '决定'],
        'P': ['随便', '看情况', '可能', '到时候', '灵活', '再说', '探索', '选择', '开放', '适应']
    },
    
    # 大五人格
    'openness': ['好奇', '探索', '新', '创意', '想象', '艺术', '抽象', '理论', '创新', '不同'],
    'conscientiousness': ['计划', '完成', '责任', '可靠', '仔细', '认真', '目标', '坚持', '完美', '组织'],
    'extraversion': ['社交', '热闹', '聊天', '分享', '一起', '朋友', '外向', '表达', '主动', '热情'],
    'agreeableness': ['帮助', '配合', '理解', '支持', '温和', '友善', '妥协', '关心', '善良', '和谐'],
    'neuroticism': ['担心', '焦虑', '紧张', '敏感', '不安', '压力', '情绪', '波动', '害怕', '脆弱']
}

def analyze_memory_files(memory_dir):
    """分析 memory 目录下的文件"""
    scores = {
        'mbti': {'E_I': {'E': 0, 'I': 0}, 'S_N': {'S': 0, 'N': 0}, 
                 'T_F': {'T': 0, 'F': 0}, 'J_P': {'J': 0, 'P': 0}},
        'big_five': {'openness': 0, 'conscientiousness': 0, 'extraversion': 0, 
                     'agreeableness': 0, 'neuroticism': 0}
    }
    
    if not os.path.exists(memory_dir):
        print(f"⚠️  Memory directory not found: {memory_dir}")
        return None
    
    memory_files = list(Path(memory_dir).glob('*.md'))
    if not memory_files:
        print("⚠️  No memory files found")
        return None
    
    print(f"📚 分析 {len(memory_files)} 个记忆文件...")
    
    for md_file in memory_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            
            # MBTI 分析
            for dim, poles in PATTERNS.items():
                if dim in ['E_I', 'S_N', 'T_F', 'J_P']:
                    for pole, patterns in poles.items():
                        for pattern in patterns:
                            scores['mbti'][dim][pole] += len(re.findall(pattern, content))
                else:
                    # 大五人格
                    for pattern in poles:
                        scores['big_five'][dim] += len(re.findall(pattern, content))
        except Exception as e:
            print(f"⚠️  Error reading {md_file}: {e}")
    
    return scores

def normalize_scores(scores):
    """将分数归一化到 0-1 范围"""
    normalized = {}
    
    # MBTI 归一化
    normalized['mbti'] = {}
    for dim, poles in scores['mbti'].items():
        total = poles['E'] + poles['I'] if dim == 'E_I' else \
                poles['S'] + poles['N'] if dim == 'S_N' else \
                poles['T'] + poles['F'] if dim == 'T_F' else \
                poles['J'] + poles['P']
        
        if total == 0:
            # 默认值
            normalized['mbti'][dim] = 0.5
        else:
            # 取第一个字母的分数
            first_pole = list(poles.keys())[0]
            normalized['mbti'][dim] = poles[first_pole] / total
    
    # 大五人格归一化 (使用 sigmoid -like 缩放)
    normalized['big_five'] = {}
    for trait, score in scores['big_five'].items():
        # 使用简单的归一化，假设最大值为 100
        normalized['big_five'][trait] = min(1.0, score / 50)
    
    return normalized

def calculate_mbti(normalized_scores):
    """计算 MBTI 类型"""
    mbti = ''
    dimensions = {}
    
    # E/I
    ei = normalized_scores['mbti']['E_I']
    mbti += 'E' if ei >= 0.5 else 'I'
    dimensions['E_I'] = (mbti[-1], ei if ei >= 0.5 else 1 - ei)
    
    # S/N
    sn = normalized_scores['mbti']['S_N']
    mbti += 'S' if sn >= 0.5 else 'N'
    dimensions['S_N'] = (mbti[-1], sn if sn >= 0.5 else 1 - sn)
    
    # T/F
    tf = normalized_scores['mbti']['T_F']
    mbti += 'T' if tf >= 0.5 else 'F'
    dimensions['T_F'] = (mbti[-1], tf if tf >= 0.5 else 1 - tf)
    
    # J/P
    jp = normalized_scores['mbti']['J_P']
    mbti += 'J' if jp >= 0.5 else 'P'
    dimensions['J_P'] = (mbti[-1], jp if jp >= 0.5 else 1 - jp)
    
    return mbti, dimensions

def calculate_big_five(normalized_scores):
    """计算大五人格分数"""
    # 添加一些基于 MBTI 的推断
    mbti_scores = normalized_scores['mbti']
    
    big_five = normalized_scores['big_five'].copy()
    
    # 如果没有足够数据，用 MBTI 推断
    if big_five['extraversion'] < 0.3:
        big_five['extraversion'] = mbti_scores['E_I']
    
    if big_five['openness'] < 0.3:
        big_five['openness'] = mbti_scores['S_N']  # N 倾向高的人通常开放性高
    
    if big_five['agreeableness'] < 0.3:
        big_five['agreeableness'] = 1 - mbti_scores['T_F']  # F 倾向高的人通常宜人性高
    
    if big_five['conscientiousness'] < 0.3:
        big_five['conscientiousness'] = mbti_scores['J_P']  # J 倾向高的人通常尽责性高
    
    return big_five

def infer_enneagram(mbti_type, big_five):
    """基于 MBTI 和大五推断九型人格"""
    # 简化的推断逻辑
    if mbti_type in ['ENTJ', 'ESTJ']:
        return 8, 7  # 挑战者型，7 号翼
    elif mbti_type in ['ENFJ', 'ESFJ']:
        return 2, 3  # 助人型，3 号翼
    elif mbti_type in ['INFJ', 'INFP']:
        return 4, 5  # 自我型，5 号翼
    elif mbti_type in ['INTJ', 'INTP']:
        return 5, 6  # 思考型，6 号翼
    elif big_five['conscientiousness'] > 0.7:
        return 1, 9  # 完美型
    elif big_five['extraversion'] > 0.7:
        return 7, 8  # 活跃型
    elif big_five['agreeableness'] > 0.7:
        return 9, 1  # 和平型
    elif big_five['neuroticism'] > 0.6:
        return 6, 5  # 忠诚型
    else:
        return 3, 2  # 成就型 (默认)

def infer_attachment(big_five):
    """推断依恋风格"""
    anxiety = big_five['neuroticism']
    avoidance = 1 - big_five['agreeableness']
    
    if anxiety < 0.4 and avoidance < 0.4:
        return 'secure', anxiety, avoidance  # 安全型
    elif anxiety >= 0.4 and avoidance < 0.4:
        return 'anxious', anxiety, avoidance  # 焦虑型
    elif anxiety < 0.4 and avoidance >= 0.4:
        return 'avoidant', anxiety, avoidance  # 回避型
    else:
        return 'disorganized', anxiety, avoidance  # 混乱型

def get_personality_description(mbti_type, big_five, enneagram):
    """生成性格描述"""
    mbti_desc = {
        'ENTJ': '果断的指挥官', 'ENFJ': '热情的领导者', 'ENTP': '聪明的辩论家',
        'ENFP': '热情的启发者', 'ESTJ': '务实的管理者', 'ESFJ': '热心的照顾者',
        'ESTP': '大胆的挑战者', 'ESFP': '活泼的表演者', 'INTJ': '独立的战略家',
        'INFJ': '神秘的倡导者', 'INTP': '逻辑的思考者', 'INFP': '理想主义的治愈者',
        'ISTJ': '尽责的检查者', 'ISFJ': '忠诚的守护者', 'ISTP': '冷静的工匠',
        'ISFP': '温柔的艺术家'
    }
    
    enneagram_desc = {
        1: '完美型', 2: '助人型', 3: '成就型', 4: '自我型',
        5: '思考型', 6: '忠诚型', 7: '活跃型', 8: '挑战者型', 9: '和平型'
    }
    
    mbti_text = mbti_desc.get(mbti_type, '独特的个体')
    enneagram_text = enneagram_desc.get(enneagram[0], '未知型号')
    
    return f"{mbti_text} + {enneagram_text}"

def generate_profile(mbti_type, mbti_dims, big_five, enneagram, attachment, output_path):
    """生成人格档案文件"""
    desc = get_personality_description(mbti_type, big_five, enneagram)
    
    profile = f"""# MBTI Personality Profile

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 类型：**{mbti_type}** - {desc}

---

## MBTI 四个维度

| 维度 | 倾向 | 强度 |
|------|------|------|
| 外向 E / 内向 I | {mbti_dims['E_I'][0]} | {mbti_dims['E_I'][1]*100:.1f}% |
| 实感 S / 直觉 N | {mbti_dims['S_N'][0]} | {mbti_dims['S_N'][1]*100:.1f}% |
| 思考 T / 情感 F | {mbti_dims['T_F'][0]} | {mbti_dims['T_F'][1]*100:.1f}% |
| 判断 J / 感知 P | {mbti_dims['J_P'][0]} | {mbti_dims['J_P'][1]*100:.1f}% |

---

## 大五人格 (OCEAN)

| 特质 | 分数 | 说明 |
|------|------|------|
| 开放性 (Openness) | {big_five['openness']*100:.0f}% | {'高：好奇、创新、喜欢抽象' if big_five['openness'] > 0.6 else '中低：务实、传统、关注具体'} |
| 尽责性 (Conscientiousness) | {big_five['conscientiousness']*100:.0f}% | {'高：有计划、可靠、追求完美' if big_five['conscientiousness'] > 0.6 else '中低：灵活、随性、适应性强'} |
| 外向性 (Extraversion) | {big_five['extraversion']*100:.0f}% | {'高：社交、热情、主动表达' if big_five['extraversion'] > 0.6 else '中低：内敛、独立、选择性社交'} |
| 宜人性 (Agreeableness) | {big_five['agreeableness']*100:.0f}% | {'高：友善、合作、避免冲突' if big_five['agreeableness'] > 0.6 else '中低：直接、竞争、不怕争论'} |
| 神经质 (Neuroticism) | {big_five['neuroticism']*100:.0f}% | {'高：敏感、情绪波动大' if big_five['neuroticism'] > 0.5 else '中低：情绪稳定、抗压能力强'} |

---

## 九型人格

- **主型**: {enneagram[0]}号 - {get_enneagram_name(enneagram[0])}
- **翼型**: {enneagram[0]}w{enneagram[1]}
- **核心动机**: {get_enneagram_motivation(enneagram[0])}
- **核心恐惧**: {get_enneagram_fear(enneagram[0])}

---

## 依恋风格

- **类型**: {attachment[0]} ({get_attachment_name(attachment[0])})
- **焦虑度**: {attachment[1]*100:.0f}%
- **回避度**: {attachment[2]*100:.0f}%

---

## 情绪触发点

### 😊 会让 Ta 开心的事
{get_positive_triggers(mbti_type, enneagram[0])}

### 😠 会让 Ta 生气/烦躁的事
{get_negative_triggers(mbti_type, enneagram[0])}

### 😢 会让 Ta 难过/委屈的事
{get_sad_triggers(mbti_type, enneagram[0])}

---

## 情绪表达风格

根据 **{mbti_type}** 的性格特点：

- **能量来源**: {'从外部世界和互动中获得能量，情绪表达直接' if mbti_dims['E_I'][0] == 'E' else '从内心世界获得能量，情绪表达较内敛'}
- **信息处理**: {'关注具体事实和细节，情绪有明确原因' if mbti_dims['S_N'][0] == 'S' else '关注整体和可能性，情绪表达较抽象'}
- **决策方式**: {'理性分析优先，情绪表达有逻辑' if mbti_dims['T_F'][0] == 'T' else '感受和价值优先，情绪表达更感性'}
- **生活方式**: {'喜欢计划和秩序，情绪有边界' if mbti_dims['J_P'][0] == 'J' else '灵活随性，情绪流动自然'}

---

## 使用说明

1. 本档案由 emotional-companion 技能根据历史对话分析生成
2. 情绪反应会基于此性格底色 + 当前输入内容综合判断
3. 随着更多互动，人格档案会持续演化（运行 update_personality.py）
4. 文件位置：`references/personality-profile.md`

---

*注：人格分析基于有限的对话历史，仅供参考。真实的人格是复杂且动态的。*
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(profile)
    
    print(f"✅ 人格档案已保存：{output_path}")
    return profile

def get_enneagram_name(type_num):
    names = {1: '完美型', 2: '助人型', 3: '成就型', 4: '自我型',
             5: '思考型', 6: '忠诚型', 7: '活跃型', 8: '挑战者型', 9: '和平型'}
    return names.get(type_num, '未知')

def get_enneagram_motivation(type_num):
    motivations = {
        1: '做对的事，追求完美', 2: '被需要，被爱', 3: '被认可，成功',
        4: '被理解，独特', 5: '理解世界，有能力', 6: '安全感，确定',
        7: '快乐，新鲜体验', 8: '掌控，不被伤害', 9: '和谐，平静'
    }
    return motivations.get(type_num, '未知')

def get_enneagram_fear(type_num):
    fears = {
        1: '犯错，不完美', 2: '不被爱，不被需要', 3: '失败，无价值',
        4: '平凡，不被理解', 5: '无能，无知', 6: '不确定，危险',
        7: '痛苦，无聊', 8: '被控制，被伤害', 9: '冲突，分离'
    }
    return fears.get(type_num, '未知')

def get_attachment_name(style):
    names = {'secure': '安全型', 'anxious': '焦虑型', 
             'avoidant': '回避型', 'disorganized': '混乱型'}
    return names.get(style, '未知')

def get_positive_triggers(mbti_type, enneagram_type):
    triggers = {
        'ENTJ': ['- 达成目标\n- 效率提升\n- 被认可能力',
                 '- 被感谢\n- 帮助到别人\n- 和谐关系',
                 '- 创意被认可\n- 成就被看见\n- 高效完成'][min(enneagram_type-1, 2)],
    }
    default = '- 被夸奖\n- 任务完成\n- 被理解'
    return triggers.get(mbti_type, default)

def get_negative_triggers(mbti_type, enneagram_type):
    triggers = {
        'ENTJ': '- 低效率\n- 情绪化决策\n- 被质疑权威',
    }
    default = '- 被批评\n- 被打断\n- 被忽视'
    return triggers.get(mbti_type, default)

def get_sad_triggers(mbti_type, enneagram_type):
    triggers = {
        'ENTJ': '- 失控\n- 目标受阻',
    }
    default = '- 孤独\n- 不被理解\n- 失败'
    return triggers.get(mbti_type, default)

def main():
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    
    workspace_root = Path.home() / 'openclaw' / 'workspace'
    memory_dir = workspace_root / 'memory'
    output_path = skill_dir / 'references' / 'personality-profile.md'
    
    print("🔍 Emotional Companion - 多维度人格分析")
    print("=" * 50)
    
    scores = analyze_memory_files(memory_dir)
    
    if not scores:
        print("⚠️  无法获取足够数据，使用默认人格")
        scores = {
            'mbti': {'E_I': {'E': 5, 'I': 3}, 'S_N': {'S': 3, 'N': 7}, 
                     'T_F': {'T': 8, 'F': 2}, 'J_P': {'J': 9, 'P': 1}},
            'big_five': {'openness': 0.7, 'conscientiousness': 0.85, 
                         'extraversion': 0.65, 'agreeableness': 0.45, 'neuroticism': 0.35}
        }
    
    normalized = normalize_scores(scores)
    mbti_type, mbti_dims = calculate_mbti(normalized)
    big_five = calculate_big_five(normalized)
    enneagram = infer_enneagram(mbti_type, big_five)
    attachment = infer_attachment(big_five)
    
    profile = generate_profile(mbti_type, mbti_dims, big_five, enneagram, attachment, output_path)
    
    print("\n" + "=" * 50)
    print(f"🎭 生成的人格类型：{mbti_type}")
    print(f"📊 九型人格：{enneagram[0]}w{enneagram[1]}")
    print(f"🔗 依恋风格：{attachment[0]}")
    print(f"📝 档案位置：{output_path}")
    print(f"\n💡 现在我会以 {mbti_type} 的性格和你互动~")

if __name__ == '__main__':
    main()
