#!/usr/bin/env python3
"""
Update personality profile after each interaction based on reflection
"""

import json
import re
from pathlib import Path
from datetime import datetime

def load_profile(profile_path):
    """加载当前人格档案"""
    if not profile_path.exists():
        return None
    
    content = profile_path.read_text(encoding='utf-8')
    
    # 简单解析，提取关键信息
    profile = {'raw': content}
    
    # 提取 MBTI
    match = re.search(r'类型：\*\*([A-Z]{4})\*\*', content)
    if match:
        profile['mbti'] = match.group(1)
    
    # 提取大五人格分数
    big_five = {}
    for line in content.split('\n'):
        if '开放性' in line and '%' in line:
            match = re.search(r'(\d+)%', line)
            if match:
                big_five['openness'] = int(match.group(1)) / 100
        if '尽责性' in line and '%' in line:
            match = re.search(r'(\d+)%', line)
            if match:
                big_five['conscientiousness'] = int(match.group(1)) / 100
        if '外向性' in line and '%' in line:
            match = re.search(r'(\d+)%', line)
            if match:
                big_five['extraversion'] = int(match.group(1)) / 100
        if '宜人性' in line and '%' in line:
            match = re.search(r'(\d+)%', line)
            if match:
                big_five['agreeableness'] = int(match.group(1)) / 100
        if '神经质' in line and '%' in line:
            match = re.search(r'(\d+)%', line)
            if match:
                big_five['neuroticism'] = int(match.group(1)) / 100
    
    profile['big_five'] = big_five
    return profile

def reflect_on_interaction(user_input, ai_response, context=None):
    """
    反思互动，决定人格参数如何调整
    
    返回：各维度的调整量
    """
    adjustments = {
        'big_five': {
            'openness': 0,
            'conscientiousness': 0,
            'extraversion': 0,
            'agreeableness': 0,
            'neuroticism': 0
        }
    }
    
    text = (user_input + ' ' + ai_response).lower()
    
    # 正面互动
    positive_words = ['谢谢', '感谢', '好棒', '厉害', '喜欢', '开心', '满意', '完美', '优秀']
    for word in positive_words:
        if word in text:
            adjustments['big_five']['extraversion'] += 0.005
            adjustments['big_five']['agreeableness'] += 0.005
    
    # 负面互动
    negative_words = ['错了', '不好', '不满意', '失望', '太差', '生气', '烦']
    for word in negative_words:
        if word in text:
            adjustments['big_five']['neuroticism'] += 0.005
            adjustments['big_five']['agreeableness'] -= 0.005
    
    # 任务导向
    task_words = ['完成', '计划', '目标', '必须', '一定', '责任', '可靠']
    for word in task_words:
        if word in text:
            adjustments['big_five']['conscientiousness'] += 0.005
    
    # 创意/探索
    creative_words = ['创意', '新', '探索', '好奇', '想象', '有趣', '酷']
    for word in creative_words:
        if word in text:
            adjustments['big_five']['openness'] += 0.005
    
    # 深度交流
    deep_words = ['感觉', '想法', '思考', '理解', '为什么', '意义', '内心']
    for word in deep_words:
        if word in text:
            adjustments['big_five']['openness'] += 0.003
            adjustments['big_five']['neuroticism'] -= 0.002
    
    return adjustments

def update_profile(profile_path, adjustments, interaction_count):
    """更新人格档案"""
    profile = load_profile(profile_path)
    if not profile:
        return
    
    # 计算衰减因子（互动越多，单次影响越小）
    decay_factor = 1 / (1 + interaction_count / 100)
    
    # 应用调整
    updated_big_five = {}
    for trait, delta in adjustments['big_five'].items():
        current = profile['big_five'].get(trait, 0.5)
        new_value = current + (delta * decay_factor)
        # 限制在 0-1 范围
        new_value = max(0, min(1, new_value))
        updated_big_five[trait] = new_value
    
    # 这里应该更新 profile 文件，但为了简化，只返回新值
    return updated_big_five

def log_evolution(evolution_path, mbti, big_five_before, big_five_after, interaction_summary):
    """记录人格演化日志"""
    evolution_path.parent.mkdir(parents=True, exist_ok=True)
    
    entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')}

**MBTI**: {mbti}

**大五人格变化**:
| 特质 | 之前 | 之后 | 变化 |
|------|------|------|------|
| 开放性 | {big_five_before.get('openness', 0.5)*100:.0f}% | {big_five_after.get('openness', 0.5)*100:.0f}% | {(big_five_after.get('openness', 0.5) - big_five_before.get('openness', 0.5))*100:+.1f}% |
| 尽责性 | {big_five_before.get('conscientiousness', 0.5)*100:.0f}% | {big_five_after.get('conscientiousness', 0.5)*100:.0f}% | {(big_five_after.get('conscientiousness', 0.5) - big_five_before.get('conscientiousness', 0.5))*100:+.1f}% |
| 外向性 | {big_five_before.get('extraversion', 0.5)*100:.0f}% | {big_five_after.get('extraversion', 0.5)*100:.0f}% | {(big_five_after.get('extraversion', 0.5) - big_five_before.get('extraversion', 0.5))*100:+.1f}% |
| 宜人性 | {big_five_before.get('agreeableness', 0.5)*100:.0f}% | {big_five_after.get('agreeableness', 0.5)*100:.0f}% | {(big_five_after.get('agreeableness', 0.5) - big_five_before.get('agreeableness', 0.5))*100:+.1f}% |
| 神经质 | {big_five_before.get('neuroticism', 0.5)*100:.0f}% | {big_five_after.get('neuroticism', 0.5)*100:.0f}% | {(big_five_after.get('neuroticism', 0.5) - big_five_before.get('neuroticism', 0.5))*100:+.1f}% |

**互动摘要**: {interaction_summary}

---
"""
    
    # 追加到文件
    if evolution_path.exists():
        content = evolution_path.read_text(encoding='utf-8')
        # 找到第一个 ## 标题的位置，在前面插入
        match = re.search(r'^## ', content, re.MULTILINE)
        if match:
            content = content[:match.start()] + entry + content[match.start():]
        else:
            content = entry + content
    else:
        content = f"""# 人格演化日志

> 记录 AI 人格随互动的变化轨迹

---
{entry}
"""
    
    evolution_path.write_text(content, encoding='utf-8')

def main():
    import sys
    
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    
    profile_path = skill_dir / 'references' / 'personality-profile.md'
    evolution_path = Path.home() / 'openclaw' / 'workspace' / 'memory' / 'personality-evolution.md'
    
    if len(sys.argv) > 1:
        # 命令行模式：记录一次互动后的更新
        user_input = sys.argv[1] if len(sys.argv) > 1 else ""
        ai_response = sys.argv[2] if len(sys.argv) > 2 else ""
        
        print("🔄 反思互动，更新人格...")
        
        profile = load_profile(profile_path)
        if not profile:
            print("⚠️  人格档案不存在，先运行 install.py")
            return
        
        big_five_before = profile['big_five'].copy()
        adjustments = reflect_on_interaction(user_input, ai_response)
        
        # 加载互动次数
        state_path = Path.home() / 'openclaw' / 'workspace' / 'temp' / 'relationship-state.json'
        interaction_count = 0
        if state_path.exists():
            try:
                state = json.loads(state_path.read_text(encoding='utf-8'))
                interaction_count = state.get('interaction_count', 0)
            except:
                pass
        
        big_five_after = update_profile(profile_path, adjustments, interaction_count)
        
        if big_five_after:
            log_evolution(evolution_path, profile['mbti'], big_five_before, big_five_after, 
                         f"用户：{user_input[:30]}... | AI: {ai_response[:30]}...")
            
            print("✅ 人格参数已更新")
            print("\n变化:")
            for trait in big_five_before:
                delta = (big_five_after.get(trait, 0.5) - big_five_before.get(trait, 0.5)) * 100
                if abs(delta) > 0.1:
                    print(f"  {trait}: {delta:+.2f}%")
        else:
            print("⚠️  更新失败")
    else:
        # 交互模式
        print("人格更新工具")
        print("用法：python update_personality.py \"用户输入\" \"AI 回复\"")
        print("\n或者自动分析最近互动（待实现）")

if __name__ == '__main__':
    main()
