#!/usr/bin/env python3
"""
微信聊天记录风格特征提取器
输入：导出的聊天记录（txt/csv）
输出：style_features.json（只提取风格，不存原文）
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def parse_txt(content: str, target_name: str = None):
    """解析微信导出的 txt 格式，支持多种常见格式"""
    lines = content.strip().split('\n')
    messages = []

    # 格式1：微信官方导出 2024-01-01 12:00:00  发送者:\n内容
    pattern_official = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)$')
    # 格式2：简单格式 发送者: 内容
    pattern_simple = re.compile(r'^([^:：]+)[:\：]\s*(.+)$')

    i = 0
    found_official = any(pattern_official.match(l) for l in lines[:20])

    while i < len(lines):
        if found_official:
            m = pattern_official.match(lines[i])
            if m:
                sender = m.group(2).rstrip(':')
                content_lines = []
                i += 1
                while i < len(lines) and not pattern_official.match(lines[i]):
                    content_lines.append(lines[i])
                    i += 1
                text = ' '.join(content_lines).strip()
                if text and (target_name is None or target_name in sender):
                    messages.append(text)
            else:
                i += 1
        else:
            m = pattern_simple.match(lines[i])
            if m:
                sender = m.group(1).strip()
                text = m.group(2).strip()
                if text and (target_name is None or target_name in sender):
                    messages.append(text)
            i += 1

    return messages


def parse_csv(content: str, target_name: str = None):
    """解析 CSV 格式"""
    import csv
    import io
    messages = []
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        sender = row.get('sender', row.get('nickname', row.get('talker', '')))
        text = row.get('content', row.get('message', row.get('text', '')))
        if text and (target_name is None or target_name in sender):
            if not text.startswith('[') and len(text) > 1:  # 过滤系统消息
                messages.append(text)
    return messages


def extract_features(messages: list) -> dict:
    """从消息列表提取风格特征，不存储原始内容"""
    if not messages:
        return {}
    
    total = len(messages)
    
    # 句子长度
    lengths = [len(m) for m in messages]
    avg_len = sum(lengths) / total
    if avg_len < 10:
        sentence_length = "极短，碎碎念"
    elif avg_len < 20:
        sentence_length = "短句为主"
    elif avg_len < 50:
        sentence_length = "中等长度"
    else:
        sentence_length = "喜欢长文"
    
    # 标点习惯
    all_text = ' '.join(messages)
    punct_features = []
    if all_text.count('...') + all_text.count('……') > total * 0.1:
        punct_features.append('喜欢用省略号')
    if all_text.count('！') + all_text.count('!') > total * 0.15:
        punct_features.append('感叹号多')
    if all_text.count('？') + all_text.count('?') > total * 0.1:
        punct_features.append('爱用问号')
    # 不加标点
    no_punct = sum(1 for m in messages if m and m[-1] not in '。！？.!?…')
    if no_punct / total > 0.6:
        punct_features.append('经常不加句尾标点')
    punctuation = '，'.join(punct_features) if punct_features else '标点使用普通'
    
    # emoji 习惯
    emoji_pattern = re.compile(
        u'[\U00010000-\U0010ffff]|'
        u'[\u2600-\u2764]|[\u2702-\u27B0]',
        re.UNICODE
    )
    emoji_msgs = sum(1 for m in messages if emoji_pattern.search(m))
    emoji_ratio = emoji_msgs / total
    if emoji_ratio < 0.05:
        emoji_habit = "几乎不用 emoji"
    elif emoji_ratio < 0.2:
        emoji_habit = "偶尔用 emoji"
    elif emoji_ratio < 0.5:
        emoji_habit = "常用 emoji"
    else:
        emoji_habit = "emoji 控"
    
    # 高频词提取（过滤停用词）
    stopwords = set('的了我你他她它是在有和就都很了吗呢啊哦嗯哈好的啦呀吧么这那')
    words = re.findall(r'[\u4e00-\u9fff]{2,4}', all_text)
    word_freq = Counter(w for w in words if not any(c in stopwords for c in w))
    keywords = [w for w, _ in word_freq.most_common(20)]
    
    # 回复风格
    short_replies = sum(1 for m in messages if len(m) <= 5)
    if short_replies / total > 0.5:
        reply_style = "惜字如金，短回复多"
    elif short_replies / total > 0.3:
        reply_style = "长短混合"
    else:
        reply_style = "喜欢展开说"
    
    # 口头禅检测
    catchphrases = []
    for phrase in ['哈哈', '哈哈哈', '好的', '嗯嗯', '对对', '不是', '就是', '然后', '其实', '感觉']:
        count = all_text.count(phrase)
        if count > total * 0.1:
            catchphrases.append(phrase)
    
    return {
        "sentence_length": sentence_length,
        "punctuation": punctuation,
        "emoji_habit": emoji_habit,
        "reply_style": reply_style,
        "keywords": keywords[:15],
        "catchphrases": catchphrases,
        "sample_size": total,
        "wechat_derived": True
    }


def main():
    parser = argparse.ArgumentParser(description='微信聊天记录风格提取')
    parser.add_argument('--input', required=True, help='聊天记录文件路径')
    parser.add_argument('--output', default='/tmp/style_features.json', help='输出路径')
    parser.add_argument('--target', default=None, help='目标人物名字（只分析她的消息）')
    parser.add_argument('--format', default='auto', choices=['auto', 'txt', 'csv'], help='文件格式')
    args = parser.parse_args()
    
    path = Path(args.input)
    if not path.exists():
        print(f'文件不存在: {args.input}')
        exit(1)
    
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    # 自动判断格式
    fmt = args.format
    if fmt == 'auto':
        fmt = 'csv' if path.suffix.lower() == '.csv' else 'txt'
    
    print(f'解析格式: {fmt}, 目标: {args.target or "全部"}')
    
    if fmt == 'csv':
        messages = parse_csv(content, args.target)
    else:
        messages = parse_txt(content, args.target)
    
    print(f'找到消息: {len(messages)} 条')
    
    if not messages:
        print('没有找到消息，请检查文件格式或目标人物名字')
        exit(1)
    
    features = extract_features(messages)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(features, ensure_ascii=False, indent=2))
    
    print(f'\n风格特征已提取到: {args.output}')
    print(json.dumps(features, ensure_ascii=False, indent=2))
    print('\n原始聊天记录未被存储。')


if __name__ == '__main__':
    main()
