#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 内容降味脚本 - 将 AI 生成的内容改写为更自然的人类风格

用法:
    python remove_ai_flavor.py --input "ai_text.txt" --output "human_text.txt"
    python remove_ai_flavor.py --input "article.txt" --style casual --intensity 4
"""

import argparse
import re
import random


# AI 味特征词库
AI_CONNECTORS = [
    "首先，", "其次，", "再次，", "最后，",
    "综上所述，", "总而言之，", "总的来说，",
    "值得注意的是，", "需要强调的是，", "值得一提的是，",
    "从...角度来看，", "基于以上分析，", "由此可见，",
]

AI_PATTERNS = [
    (r'总之，', ''),
    (r'综上所述，', ''),
    (r'总而言之，', ''),
    (r'总的来说，', ''),
    (r'值得注意的是，', '要说的是，'),
    (r'需要强调的是，', '特别要提的是，'),
    (r'值得一提的是，', '有趣的是，'),
    (r'首先，', ''),
    (r'其次，', '另外，'),
    (r'再次，', '还有，'),
    (r'最后，', '最后说说，'),
    (r'让我们', '咱们'),
    (r'我们可以', '咱可以'),
    (r'你应该', '你可以'),
]

# 口语化替换
CASUAL_REPLACEMENTS = {
    '因此': '所以',
    '然而': '不过',
    '此外': '还有',
    '例如': '比如说',
    '即': '就是',
    '皆': '都',
    '亦': '也',
    '甚': '很',
    '颇': '挺',
    '极为': '特别',
    '十分': '特别',
    '非常': '特别',
}

# 语气词
MOOD_PARTICLES = ['吧', '呢', '啊', '嘛', '咯', '哈', '啦']


def remove_ai_connectors(text: str) -> str:
    """移除 AI 连接词"""
    result = text
    for connector in AI_CONNECTORS:
        result = result.replace(connector, '')
    return result


def replace_ai_patterns(text: str) -> str:
    """替换 AI 句式"""
    result = text
    for pattern, replacement in AI_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result


def add_casual_tone(text: str, intensity: int = 3) -> str:
    """添加口语化语气"""
    if intensity < 3:
        return text
    
    result = text
    
    # 替换正式词汇为口语
    for formal, casual in CASUAL_REPLACEMENTS.items():
        # 避免过度替换
        if random.random() < 0.3 * (intensity / 5):
            result = result.replace(formal, casual)
    
    # 在句尾添加语气词（适度）
    sentences = re.split('([。！？!?])', result)
    processed = []
    for i, sentence in enumerate(sentences):
        processed.append(sentence)
        # 在陈述句末尾偶尔加语气词
        if sentence and sentence[-1] in '。！' and random.random() < 0.15 * (intensity / 5):
            particle = random.choice(MOOD_PARTICLES)
            processed.append(particle)
    
    return ''.join(processed)


def add_personal_touch(text: str, style: str = 'casual') -> str:
    """添加个人化表达"""
    result = text
    
    # 添加一些个人化表达
    personal_phrases = {
        'casual': [
            ('我觉得', '我个人觉得'),
            ('我认为', '我个人认为'),
            ('可以说', '说实话'),
        ],
        'professional': [
            ('根据经验', '根据我的经验'),
            ('通常', '我通常会'),
            ('建议', '我个人的建议是'),
        ],
        'story': [
            ('记得', '我记得有一次'),
            ('曾经', '我之前遇到过'),
            ('比如', '我跟你讲个例子'),
        ],
    }
    
    phrases = personal_phrases.get(style, personal_phrases['casual'])
    for original, replacement in phrases:
        if original in result and random.random() < 0.3:
            result = result.replace(original, replacement, 1)
    
    return result


def vary_sentence_structure(text: str) -> str:
    """变化句式结构"""
    paragraphs = text.split('\n\n')
    processed = []
    
    for para in paragraphs:
        sentences = re.split('([。！？!?])', para)
        
        # 合并短句
        new_sentences = []
        buffer = []
        for s in sentences:
            if s and s.strip():
                buffer.append(s)
                if s[-1] in '。！？!?':
                    combined = ''.join(buffer)
                    if len(combined) < 20 and len(new_sentences) > 0:
                        # 短句合并到前一句
                        new_sentences[-1] = new_sentences[-1][:-1] + '，' + combined.lstrip()
                    else:
                        new_sentences.append(combined)
                    buffer = []
        
        processed.append(''.join(new_sentences))
    
    return '\n\n'.join(processed)


def remove_ai_flavor(text: str, style: str = 'casual', intensity: int = 3) -> str:
    """
    主函数：将 AI 内容改写为人类风格
    
    参数:
        text: AI 生成的原始内容
        style: 风格选项 (casual/professional/story)
        intensity: 降味强度 (1-5)
    
    返回:
        处理后的人类风格内容
    """
    result = text
    
    # 步骤 1: 移除 AI 连接词
    result = remove_ai_connectors(result)
    
    # 步骤 2: 替换 AI 句式
    result = replace_ai_patterns(result)
    
    # 步骤 3: 添加口语化语气
    if intensity >= 2:
        result = add_casual_tone(result, intensity)
    
    # 步骤 4: 添加个人化表达
    if intensity >= 3:
        result = add_personal_touch(result, style)
    
    # 步骤 5: 变化句式结构
    if intensity >= 4:
        result = vary_sentence_structure(result)
    
    return result


def main():
    parser = argparse.ArgumentParser(description='AI 内容降味工具 - 让 AI 生成内容更自然')
    parser.add_argument('--input', required=True, help='输入文件路径')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--style', default='casual', 
                        choices=['casual', 'professional', 'story'],
                        help='输出风格 (默认：casual)')
    parser.add_argument('--intensity', type=int, default=3, choices=[1, 2, 3, 4, 5],
                        help='降味强度 (1-5, 默认：3)')
    
    args = parser.parse_args()
    
    # 读取输入文件
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.input}")
        return
    except Exception as e:
        print(f"错误：{e}")
        return
    
    # 处理内容
    print(f"正在处理：{args.input}")
    print(f"风格：{args.style}, 强度：{args.intensity}/5")
    
    processed = remove_ai_flavor(content, args.style, args.intensity)
    
    # 写入输出文件
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(processed)
        print(f"[OK] 处理完成！已保存到：{args.output}")
        
        # 显示统计
        original_len = len(content)
        processed_len = len(processed)
        change_rate = abs(processed_len - original_len) / original_len * 100
        print(f"  原文：{original_len} 字")
        print(f"  处理后：{processed_len} 字")
        print(f"  变化：{change_rate:.1f}%")
        
    except Exception as e:
        print(f"错误：{e}")


if __name__ == '__main__':
    main()
