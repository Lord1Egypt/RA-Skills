#!/usr/bin/env python3
"""
微信聊天记录解析器
支持 WeChatMsg、留痕、PyWxDump 等多种导出格式
"""

import argparse
import json
import csv
import re
import sys
from pathlib import Path
from datetime import datetime


def parse_wechatmsg_txt(file_path, target_name):
    """解析 WeChatMsg 导出的 txt 格式"""
    messages = []
    current_date = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 匹配日期行
        date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', line)
        if date_match:
            current_date = date_match.group(1)
            continue
        
        # 匹配消息行: 昵称 时间 内容
        msg_match = re.match(r'^(.*?)\s+(\d{2}:\d{2}:\d{2})\s+(.*)$', line)
        if msg_match and current_date:
            nickname, time_str, content = msg_match.groups()
            if target_name.lower() in nickname.lower():
                messages.append({
                    'date': current_date,
                    'time': time_str,
                    'sender': nickname,
                    'content': content
                })
    
    return messages


def parse_wechatmsg_csv(file_path, target_name):
    """解析 WeChatMsg 导出的 csv 格式"""
    messages = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sender = row.get('昵称', row.get('sender', ''))
            if target_name.lower() in sender.lower():
                messages.append({
                    'date': row.get('日期', row.get('date', '')),
                    'time': row.get('时间', row.get('time', '')),
                    'sender': sender,
                    'content': row.get('内容', row.get('content', ''))
                })
    
    return messages


def parse_liuhen_json(file_path, target_name):
    """解析留痕导出的 JSON 格式"""
    messages = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for msg in data.get('messages', []):
        sender = msg.get('nickname', msg.get('sender', ''))
        if target_name.lower() in sender.lower():
            messages.append({
                'date': msg.get('date', ''),
                'time': msg.get('time', ''),
                'sender': sender,
                'content': msg.get('content', '')
            })
    
    return messages


def parse_pywxdump_sqlite(file_path, target_name):
    """解析 PyWxDump 导出的 SQLite 数据库"""
    messages = []
    
    try:
        import sqlite3
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        
        # 查找消息表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%message%'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                columns = [desc[0] for desc in cursor.description]
                
                # 查找可能的字段名
                sender_col = next((c for c in columns if 'sender' in c.lower() or 'nickname' in c.lower()), None)
                content_col = next((c for c in columns if 'content' in c.lower() or 'msg' in c.lower()), None)
                time_col = next((c for c in columns if 'time' in c.lower() or 'date' in c.lower()), None)
                
                if sender_col and content_col:
                    cursor.execute(f"SELECT {sender_col}, {content_col}, {time_col} FROM {table_name}")
                    for row in cursor.fetchall():
                        sender, content, timestamp = row[0], row[1], row[2] if len(row) > 2 else ''
                        if target_name.lower() in str(sender).lower():
                            messages.append({
                                'date': str(timestamp)[:10] if timestamp else '',
                                'time': str(timestamp)[11:19] if timestamp else '',
                                'sender': sender,
                                'content': content
                            })
            except Exception as e:
                continue
        
        conn.close()
    except ImportError:
        print("Error: sqlite3 module not available", file=sys.stderr)
    
    return messages


def extract_patterns(messages):
    """从消息中提取语言模式"""
    patterns = {
        'catchphrases': [],
        'emoji_usage': [],
        'punctuation_style': [],
        'msg_length_avg': 0
    }
    
    if not messages:
        return patterns
    
    all_content = ' '.join([m['content'] for m in messages])
    
    # 提取常见语气词
    particles = re.findall(r'[呢吧啊哦嗯哈嘿哎～~！!]{1,3}', all_content)
    if particles:
        from collections import Counter
        top_particles = Counter(particles).most_common(5)
        patterns['catchphrases'] = [p[0] for p in top_particles]
    
    # 计算平均消息长度
    patterns['msg_length_avg'] = sum(len(m['content']) for m in messages) / len(messages)
    
    return patterns


def main():
    parser = argparse.ArgumentParser(description='解析微信聊天记录')
    parser.add_argument('--file', required=True, help='聊天记录文件路径')
    parser.add_argument('--target', required=True, help='目标人物昵称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--format', default='auto', choices=['auto', 'txt', 'csv', 'json', 'sqlite'])
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    # 自动检测格式
    file_format = args.format
    if file_format == 'auto':
        suffix = file_path.suffix.lower()
        if suffix == '.txt':
            file_format = 'txt'
        elif suffix == '.csv':
            file_format = 'csv'
        elif suffix == '.json':
            file_format = 'json'
        elif suffix in ['.db', '.sqlite', '.sqlite3']:
            file_format = 'sqlite'
    
    # 解析
    if file_format == 'txt':
        messages = parse_wechatmsg_txt(args.file, args.target)
    elif file_format == 'csv':
        messages = parse_wechatmsg_csv(args.file, args.target)
    elif file_format == 'json':
        messages = parse_liuhen_json(args.file, args.target)
    elif file_format == 'sqlite':
        messages = parse_pywxdump_sqlite(args.file, args.target)
    else:
        print(f"Error: Unsupported format: {file_format}", file=sys.stderr)
        sys.exit(1)
    
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
