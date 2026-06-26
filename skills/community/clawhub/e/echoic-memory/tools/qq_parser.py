#!/usr/bin/env python3
"""
QQ 聊天记录解析器
支持 QQ 消息管理器导出的 txt 和 mht 格式
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
import json


def parse_qq_txt(file_path, target_name):
    """解析 QQ 导出的 txt 格式"""
    messages = []
    current_date = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # QQ txt 格式: 日期 时间 昵称(QQ号) 消息内容
    pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2}:\d{2})\s+([^\n]+?)\((\d+)\)\s*\n([^\n]+)'
    
    matches = re.findall(pattern, content)
    for match in matches:
        date, time, nickname, qq_num, msg_content = match
        if target_name.lower() in nickname.lower() or target_name == qq_num:
            messages.append({
                'date': date,
                'time': time,
                'sender': nickname,
                'qq': qq_num,
                'content': msg_content.strip()
            })
    
    # 备选格式：没有时间戳的简单格式
    if not messages:
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if target_name.lower() in line.lower():
                # 尝试提取发送者和内容
                parts = line.split(':', 1)
                if len(parts) == 2:
                    sender, msg = parts
                    messages.append({
                        'date': '',
                        'time': '',
                        'sender': sender.strip(),
                        'content': msg.strip()
                    })
    
    return messages


def parse_qq_mht(file_path, target_name):
    """解析 QQ 导出的 mht 格式"""
    messages = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # mht 中查找 HTML 部分
    html_match = re.search(r'<html[^>]*>(.*?)</html>', content, re.DOTALL | re.IGNORECASE)
    if html_match:
        html_content = html_match.group(1)
        
        # 提取消息单元
        # QQ mht 通常使用表格布局
        msg_pattern = r'<td[^>]*>(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2}:\d{2})</td>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([^<]+)</td>'
        matches = re.findall(msg_pattern, html_content, re.DOTALL)
        
        for match in matches:
            date, time, nickname, msg_content = match
            if target_name.lower() in nickname.lower():
                messages.append({
                    'date': date,
                    'time': time,
                    'sender': nickname.strip(),
                    'content': msg_content.strip()
                })
    
    return messages


def extract_patterns(messages):
    """从消息中提取语言模式"""
    patterns = {
        'catchphrases': [],
        'qq_emoticons': [],
        'punctuation_style': [],
        'msg_length_avg': 0
    }
    
    if not messages:
        return patterns
    
    all_content = ' '.join([m['content'] for m in messages])
    
    # 提取 QQ 表情代码
    emoticons = re.findall(r'\[([^\]]+)\]', all_content)
    if emoticons:
        from collections import Counter
        top_emoticons = Counter(emoticons).most_common(10)
        patterns['qq_emoticons'] = [e[0] for e in top_emoticons]
    
    # 提取常见语气词
    particles = re.findall(r'[呢吧啊哦嗯哈嘿哎~=]{1,3}', all_content)
    if particles:
        from collections import Counter
        top_particles = Counter(particles).most_common(5)
        patterns['catchphrases'] = [p[0] for p in top_particles]
    
    # 计算平均消息长度
    patterns['msg_length_avg'] = sum(len(m['content']) for m in messages) / len(messages)
    
    return patterns


def main():
    parser = argparse.ArgumentParser(description='解析 QQ 聊天记录')
    parser.add_argument('--file', required=True, help='聊天记录文件路径')
    parser.add_argument('--target', required=True, help='目标人物昵称或QQ号')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    # 根据后缀选择解析器
    suffix = file_path.suffix.lower()
    if suffix == '.mht':
        messages = parse_qq_mht(args.file, args.target)
    else:
        # 默认使用 txt 解析器
        messages = parse_qq_txt(args.file, args.target)
    
    # 提取模式
    patterns = extract_patterns(messages)
    
    # 输出
    output = {
        'source': str(file_path),
        'target': args.target,
        'message_count': len(messages),
        'patterns': patterns,
        'messages': messages[:100]  # 限制输出数量
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"解析完成: {len(messages)} 条消息")
    print(f"输出文件: {args.output}")


if __name__ == '__main__':
    main()
