#!/usr/bin/env python3
"""
会议纪要生成工具
从本地文本/JSON文件读取内容，生成结构化Markdown会议纪要
用法: python3 meeting_minutes.py input.txt -o output.md
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def read_input(file_path: str) -> Dict:
    """
    读取本地文件内容，支持txt和json格式
    
    Args:
        file_path: 文件路径
        
    Returns:
        {'text': 文本内容, 'source': 文件来源}
    """
    if not file_path:
        # 从标准输入读取
        print("📝 请输入会议内容（输入完成后按 Ctrl+D 结束）：")
        text = sys.stdin.read()
        return {'text': text.strip(), 'source': 'stdin'}
    
    if not os.path.exists(file_path):
        return {'error': f'文件不存在: {file_path}'}
    
    ext = Path(file_path).suffix.lower()
    
    if ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 支持多种json格式
        if isinstance(data, dict):
            if 'content' in data:
                text = data['content']
            elif 'text' in data:
                text = data['text']
            elif 'meeting_notes' in data:
                text = data['meeting_notes']
            else:
                # 把整个dict转成文本
                text = json.dumps(data, ensure_ascii=False)
            topic = data.get('topic', Path(file_path).stem)
        else:
            text = str(data)
            topic = Path(file_path).stem
        return {'text': text, 'source': file_path, 'topic': topic}
    
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return {'text': text.strip(), 'source': file_path}
    
    else:
        # 尝试作为文本读取
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return {'text': text.strip(), 'source': file_path}
        except:
            return {'error': f'不支持的格式: {ext}，请使用 .txt 或 .json'}


def extract_topic(text: str) -> str:
    """提取会议主题"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:10]:
        if len(line) > 5:
            keywords = ['会议', '讨论', '规划', '复盘', '评审', '汇报', '启动', '总结']
            for kw in keywords:
                if kw in line:
                    return line[:60]
    return lines[0][:60] if lines else "会议讨论"


def extract_key_points(text: str) -> List[str]:
    """提取关键讨论点"""
    key_points = []
    keywords = ['进度', '问题', '风险', '方案', '计划', '目标', '预算', '资源', 
                '进度', '进展', '完成', '需要', '应该', '可以', '讨论']
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 10:
            for kw in keywords:
                if kw in line:
                    key_points.append(line)
                    break
    # 去重并限制数量
    seen = set()
    unique = []
    for p in key_points:
        normalized = p[:60]
        if normalized not in seen:
            seen.add(normalized)
            unique.append(normalized)
    return unique[:8]


def extract_decisions(text: str) -> List[str]:
    """提取决策结论"""
    decisions = []
    patterns = [
        r'[\u4e00-\u9fa5]{0,20}(决定|确认|通过|同意|确定|采用)[\u4e00-\u9fa5]{2,30}',
        r'[\u4e00-\u9fa5]{0,10}(定了|选[定为])[\u4e00-\u9fa5]{2,20}',
    ]
    for line in text.split('\n'):
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for m in matches:
                decisions.append(f"决定：{m}" if len(m) < 15 else m[:30])
    seen = set()
    unique = []
    for d in decisions:
        if d not in seen:
            seen.add(d)
            unique.append(d)
    return unique[:5]


def extract_todos(text: str) -> List[Dict]:
    """提取待办事项"""
    todos = []
    patterns = [
        r'(?:TODO|待办|待处理|待确认)[：:]\s*(.+)',
        r'([\u4e00-\u9fa5]{2,10})(?:负责|跟进|落实|完成)[^\n]{0,30}',
        r'(下周|明天|本周|月底前|周五)[^\n]{0,40}',
    ]
    for line in text.split('\n'):
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for m in matches:
                if isinstance(m, tuple):
                    todo_text = ''.join(m).strip()
                else:
                    todo_text = str(m).strip()
                if len(todo_text) > 3:
                    # 提取责任人
                    assignee = ''
                    name_match = re.search(r'([\u4e00-\u9fa5]{2,4})(?:负责|跟进)', line)
                    if name_match:
                        assignee = name_match.group(1)
                    # 提取截止
                    deadline = ''
                    for kw in ['明天', '下周', '本周', '月底', '周五']:
                        if kw in line:
                            deadline = kw
                            break
                    todos.append({
                        'task': todo_text[:80],
                        'assignee': assignee,
                        'deadline': deadline,
                    })
    seen = set()
    unique = []
    for t in todos:
        if t['task'] not in seen:
            seen.add(t['task'])
            unique.append(t)
    return unique[:10]


def generate_minutes(text: str, topic: str = None) -> str:
    """生成Markdown格式会议纪要"""
    if not topic:
        topic = extract_topic(text)
    
    key_points = extract_key_points(text)
    decisions = extract_decisions(text)
    todos = extract_todos(text)
    
    # 格式化待办
    todo_lines = []
    for i, t in enumerate(todos, 1):
        assignee_str = f" ← @{t['assignee']}" if t['assignee'] else ""
        deadline_str = f" [截止: {t['deadline']}]" if t['deadline'] else ""
        todo_lines.append(f"{i}. [ ] {t['task']}{assignee_str}{deadline_str}")
    
    minutes = f"""# 会议纪要

## 📋 基本信息
- **会议主题**: {topic}
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📝 关键讨论点
"""
    if key_points:
        for p in key_points:
            minutes += f"- {p}\n"
    else:
        minutes += "- （未识别到明确讨论点）\n"
    
    minutes += "\n## ✅ 决策结论\n"
    if decisions:
        for d in decisions:
            minutes += f"- ✓ {d}\n"
    else:
        minutes += "- （未识别到明确决策）\n"
    
    minutes += "\n## 📌 待办事项\n"
    if todo_lines:
        for t in todo_lines:
            minutes += f"{t}\n"
    else:
        minutes += "- （未识别到明确待办）\n"
    
    minutes += f"""
---
*由 cn-meeting-minutes 生成 | {datetime.now().strftime('%Y-%m-%d')}*
"""
    return minutes


def main():
    parser = argparse.ArgumentParser(description='会议纪要生成工具 - 从本地文本/JSON文件生成结构化Markdown纪要')
    parser.add_argument('file_path', nargs='?', default='', help='输入文件路径（.txt 或 .json，可选；空则从标准输入读取）')
    parser.add_argument('-o', '--output', help='输出文件路径（默认自动命名）')
    
    args = parser.parse_args()
    
    # 读取输入
    data = read_input(args.file_path)
    if 'error' in data:
        print(f"❌ {data['error']}")
        sys.exit(1)
    
    text = data['text']
    if not text:
        print("❌ 输入内容为空")
        sys.exit(1)
    
    topic = data.get('topic', '')
    print(f"✅ 读取完成，共 {len(text)} 字符")
    
    # 生成纪要
    minutes = generate_minutes(text, topic)
    
    print(f"\n📋 纪要预览:")
    print(f"   主题: {topic}")
    print(f"   讨论点: {len(extract_key_points(text))} 条")
    print(f"   决策: {len(extract_decisions(text))} 条")
    print(f"   待办: {len(extract_todos(text))} 条")
    
    # 保存
    if args.output:
        output_path = args.output
    else:
        stem = Path(data['source']).stem if data['source'] != 'stdin' else 'meeting'
        output_path = f"{stem}_纪要.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(minutes)
    print(f"💾 已保存: {output_path}")


if __name__ == '__main__':
    main()
