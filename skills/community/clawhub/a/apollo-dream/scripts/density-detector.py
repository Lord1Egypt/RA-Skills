#!/usr/bin/env python3
"""
density-detector.py - 信息密度检测
识别高密度（决策、结论）和低密度（过程、噪音）内容
"""
import re

# 高价值标记
HIGH_VALUE_PATTERNS = [
    (r'决定|决策|结论|判断|结论是|所以|因此|综上', 'decision'),
    (r'任务|下一步|行动|执行|做|完成', 'action'),
    (r'用户说|用户要求|用户提到|老板说', 'user_signal'),
    (r'\d+[./年]|\d+%|约\d+|大约', 'quantitative'),
    (r'必须|一定|绝不|绝对', 'strong_assertion'),
    (r'其实|但是|不过|然而', 'contrast'),
]

# 低价值标记
LOW_VALUE_PATTERNS = [
    (r'^哈+|^嗯|^哦|^呃', 'casual_response'),
    (r'对|好的|行|可以', 'acknowledgment'),
    (r'我明白|我知道了|了解', 'acknowledgment_ai'),
    (r'\.\.\.|\?|？', 'trailing'),
]

def calculate_density(text):
    """
    计算信息密度
    
    返回:
        float: 密度分数 (0-1, 越高越重要)
        dict: 各维度分数
    """
    if not text or len(text.strip()) < 10:
        return 0.0, {}
    
    scores = {}
    
    # 高价值分数
    high_score = 0
    for pattern, label in HIGH_VALUE_PATTERNS:
        matches = len(re.findall(pattern, text))
        high_score += matches
    
    # 低价值分数
    low_score = 0
    for pattern, label in LOW_VALUE_PATTERNS:
        matches = len(re.findall(pattern, text))
        low_score += matches
    
    # 基础分：独特内容比例
    unique_ratio = len(set(text)) / max(len(text), 1)
    
    # 组合
    total_score = high_score * 2 - low_score * 0.5 + unique_ratio * 5
    max_possible = 20  # 归一化
    
    density = min(1.0, total_score / max_possible)
    
    scores = {
        'high_value_markers': high_score,
        'low_value_markers': low_score,
        'unique_ratio': round(unique_ratio, 3),
        'raw_score': round(total_score, 2)
    }
    
    return density, scores

def is_high_density(text):
    """判断是否高密度（需要保留）"""
    density, _ = calculate_density(text)
    return density > 0.3

def get_density_level(text):
    """获取密度等级"""
    density, _ = calculate_density(text)
    if density > 0.6:
        return 'high'
    elif density > 0.3:
        return 'medium'
    else:
        return 'low'

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: density-detector.py --text <文本>")
        print("   或: density-detector.py --file <文件>")
        sys.exit(1)
    
    if sys.argv[1] == '--text':
        text = ' '.join(sys.argv[2:])
    elif sys.argv[1] == '--file':
        with open(sys.argv[2], 'r') as f:
            text = f.read()
    else:
        print("未知参数")
        sys.exit(1)
    
    density, scores = calculate_density(text)
    level = get_density_level(text)
    
    print(f"信息密度: {density:.3f}")
    print(f"密度等级: {level}")
    print(f"高价值标记: {scores['high_value_markers']}")
    print(f"低价值标记: {scores['low_value_markers']}")
    print(f"独特字符比例: {scores['unique_ratio']}")

if __name__ == '__main__':
    main()
