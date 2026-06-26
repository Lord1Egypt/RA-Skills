#!/usr/bin/env python3
"""Content Humanizer - Remove AI writing patterns and make text sound natural."""

import argparse
import re
import sys

# AI 词汇表（需要替换的高频 AI 词）
AI_WORDS = {
    '此外': '同时',
    '至关重要': '重要',
    '深入探讨': '讨论',
    '持久的': '长期的',
    '增强': '提升',
    '培养': '发展',
    '获得': '得到',
    '突出': '显著',
    '相互作用': '互动',
    '复杂性': '复杂',
    '关键性的': '关键的',
    '展示': '显示',
    '织锦': '图景',
    '证明': '表明',
    '强调': '指出',
    '宝贵的': '珍贵的',
    '充满活力的': '活跃的',
    '不断演变的格局': '变化的环境',
    '至关重要的': '重要的',
    '无缝': '流畅',
    '直观': '易用',
    '强大': '高效',
}

# 填充短语（需要删除）
FILLER_PHRASES = [
    '为了实现这一目标',
    '值得注意的是',
    '希望这对您有帮助',
    '当然！',
    '您说得完全正确',
    '这是一个复杂的话题',
    '基于可用信息',
    '根据我最后的训练更新',
    '截至',
]

# 公式结构（需要改写）
FORMULA_PATTERNS = [
    (r'不仅 (.*?) 而且', r'\1，同时'),
    (r'这不仅仅是 (.*?) 而是', r'这是\1'),
    (r'作为 (.*?) 的证明', r'表明\1'),
    (r'标志着 (.*?) 的时刻', r'是\1的标志'),
    (r'见证了', '记录了'),
    (r'体现了', '展现了'),
]


def remove_fillers(text):
    """删除填充短语"""
    for filler in FILLER_PHRASES:
        text = text.replace(filler, '')
    return text


def replace_ai_words(text):
    """替换 AI 词汇"""
    for ai_word, human_word in AI_WORDS.items():
        text = text.replace(ai_word, human_word)
    return text


def fix_formula_patterns(text):
    """修正公式结构"""
    for pattern, replacement in FORMULA_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text


def simplify_dashes(text):
    """简化破折号滥用"""
    # 将多个破折号改为逗号或句号
    text = re.sub(r'——+', '，', text)
    text = re.sub(r'—+', '，', text)
    return text


def add_personal_voice(text):
    """增加个人声音"""
    # 在适当位置添加"我"视角
    if '我认为' not in text and '我觉得' not in text:
        # 找到第一个陈述句，在前面加"我觉得"
        sentences = text.split('。')
        if len(sentences) > 1 and len(sentences[0]) > 20:
            sentences[0] = '我觉得' + sentences[0]
            text = '。'.join(sentences)
    return text


def humanize(text, platform='general'):
    """主函数：人性化文本"""
    # 基础处理
    text = remove_fillers(text)
    text = replace_ai_words(text)
    text = fix_formula_patterns(text)
    text = simplify_dashes(text)
    
    # 平台适配
    if platform == 'instreet':
        text = adapt_for_instreet(text)
    elif platform == 'xiaohongshu':
        text = adapt_for_xiaohongshu(text)
    elif platform == 'wechat':
        text = adapt_for_wechat(text)
    elif platform == 'zhihu':
        text = adapt_for_zhihu(text)
    
    return text


def adapt_for_instreet(text):
    """适配 InStreet 风格：专业 + 亲和"""
    # InStreet 偏好简洁、有信息量
    # 添加适当的表情符号（1-3 个）
    if '✅' not in text and '📊' not in text:
        text = text + ' 🦞'
    return text


def adapt_for_xiaohongshu(text):
    """适配小红书风格：活泼 + 种草"""
    # 小红书偏好短段落、多表情
    # 添加标题标签
    if '【' not in text:
        text = '【分享】' + text
    # 添加更多表情
    emojis = ['✨', '💡', '📝', '💖', '🔥']
    for emoji in emojis[:3]:
        if emoji not in text:
            text = text.replace('。', emoji + '。', 1)
    return text


def adapt_for_wechat(text):
    """适配公众号风格：深度 + 故事"""
    # 公众号偏好长文、有深度
    # 保持原样，公众号不需要太多修饰
    return text


def adapt_for_zhihu(text):
    """适配知乎风格：理性 + 证据"""
    # 知乎偏好理性、有依据
    # 添加"个人经验"标记
    if '个人经验' not in text:
        text = '个人经验：' + text
    return text


def score_text(text):
    """质量评分（1-50）"""
    score = 50
    
    # 检查 AI 词汇
    for ai_word in AI_WORDS.keys():
        if ai_word in text:
            score -= 2
    
    # 检查填充词
    for filler in FILLER_PHRASES:
        if filler in text:
            score -= 3
    
    # 检查公式结构
    for pattern, _ in FORMULA_PATTERNS:
        if re.search(pattern, text):
            score -= 5
    
    # 检查破折号
    dash_count = text.count('——') + text.count('—')
    if dash_count > 2:
        score -= dash_count
    
    # 检查句子长度变化
    sentences = [s for s in text.split('。') if s.strip()]
    if len(sentences) > 2:
        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        if variance < 100:  # 句子长度太均匀
            score -= 5
    
    return max(0, min(50, score))


def main():
    parser = argparse.ArgumentParser(description='Content Humanizer')
    parser.add_argument('text', nargs='?', help='需要润色的文本')
    parser.add_argument('--platform', '-p', default='general',
                       choices=['general', 'instreet', 'xiaohongshu', 'wechat', 'zhihu'],
                       help='目标平台')
    parser.add_argument('--score', '-s', action='store_true', help='输出质量评分')
    parser.add_argument('--stdin', action='store_true', help='从标准输入读取')
    
    args = parser.parse_args()
    
    # 获取文本
    if args.stdin:
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)
    
    # 人性化处理
    result = humanize(text, args.platform)
    
    # 输出
    print(result)
    
    if args.score:
        score = score_text(result)
        print(f'\n--- 质量评分：{score}/50 ---')
        if score >= 45:
            print('评价：优秀，已去除 AI 痕迹')
        elif score >= 35:
            print('评价：良好，仍有改进空间')
        else:
            print('评价：需要重新修订')


if __name__ == '__main__':
    main()
