#!/usr/bin/env python3
"""
thought-digger: 从 thoughts.md 中挖掘价值

分析想法日记，提取：
1. 反复出现的主题
2. 未完成的待办
3. 值得吸收的洞察
4. 想研究但没做的事
"""

import re
import json
import os
import sys
from datetime import datetime
from collections import Counter

# Configurable paths - override via environment variables or command-line args
WORKSPACE = os.environ.get('OPENCLAW_WORKSPACE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
THOUGHTS_FILE = os.path.join(WORKSPACE, "memory", "thoughts.md")
DIGEST_FILE = os.path.join(WORKSPACE, "memory", "thought-digest.json")

def parse_entries(content):
    """Parse thoughts.md into entries by ## headers."""
    entries = []
    current = None
    for line in content.split('\n'):
        if line.startswith('## '):
            if current:
                entries.append(current)
            current = {'header': line, 'body': [], 'date': '', 'time': '', 'tag': ''}
            # Extract date/time from header
            m = re.search(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})', line)
            if m:
                current['date'] = m.group(1)
                current['time'] = m.group(2)
            # Extract tags like [自审]
            m = re.search(r'\[(.+?)\]', line)
            if m:
                current['tag'] = m.group(1)
        elif current:
            current['body'].append(line)
    if current:
        entries.append(current)
    return entries

def extract_themes(entries):
    """Find recurring themes across entries using jieba segmentation."""
    import jieba
    jieba.setLogLevel(20)
    
    stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都',
                  '一', '上', '也', '很', '到', '说', '要', '去', '你', '会',
                  '着', '没有', '看', '好', '自己', '这', '被', '从', '把', '让',
                  '用', '给', '做', '什么', '怎么', '可以', '没', '想', '还', '能',
                  '对', '但是', '因为', '所以', '如果', '然后', '但是', '或者', '而且',
                  '不过', '已经', '只是', '还是', '一个', '这个', '那个', '不是',
                  '怎么', '这么', '那么', '这样', '那样', '一些', '一下', '一直',
                  '一样', '东西', '事情', '时候', '现在', '以后', '之前', '今天',
                  'before', 'after', 'about', 'just', 'like', 'would', 'could',
                  'should', 'have', 'been', 'this', 'that', 'with', 'from',
                  'they', 'were', 'will', 'what', 'when', 'where', 'which',
                  'there', 'their', 'them', 'then', 'than', 'some', 'into'}
    
    words = Counter()
    for entry in entries:
        text = ' '.join(entry['body'])
        # Use jieba for proper Chinese word segmentation
        tokens = jieba.cut(text)
        for token in tokens:
            token = token.strip()
            if len(token) >= 2 and token not in stop_words:
                # Filter out pure punctuation and numbers
                if not re.match(r'^[\d\s\W]+$', token) and token.lower() not in ('md', 'json', 'txt', 'sh', 'py', 'log'):
                    words[token] += 1
    
    return words.most_common(20)

def find_todos(entries):
    """Find mentioned but not completed action items."""
    todos = []
    todo_patterns = [
        r'可以[做搞弄](.+?)(?:。|$)',
        r'应该(.+?)(?:。|$)',
        r'下次(.+?)(?:。|$)',
        r'以后(.+?)(?:。|$)',
        r'值得(.+?)(?:。|$)',
        r'应该找(.+?)(?:。|$)',
        r'不急[，,](.+?)(?:。|$)',
        r'留到(.+?)(?:。|$)',
    ]
    for entry in entries:
        text = ' '.join(entry['body'])
        for pat in todo_patterns:
            matches = re.findall(pat, text)
            for m in matches:
                if len(m) > 3 and len(m) < 50:
                    todos.append({
                        'action': m.strip(),
                        'source': entry['date'] + ' ' + entry['time'],
                        'header': entry['header']
                    })
    return todos

def find_insights(entries):
    """Find entries with [自审] tag or key insight markers."""
    insights = []
    for entry in entries:
        if entry['tag'] in ('自审', '洞察', '发现', '顿悟'):
            insights.append({
                'tag': entry['tag'],
                'date': entry['date'],
                'summary': entry['header'].strip('# '),
                'body_preview': ' '.join(entry['body'])[:200]
            })
    return insights

def main():
    with open(THOUGHTS_FILE, 'r') as f:
        content = f.read()
    
    entries = parse_entries(content)
    print(f"📊 分析 {len(entries)} 条想法记录")
    
    themes = extract_themes(entries)
    todos = find_todos(entries)
    insights = find_insights(entries)
    
    digest = {
        'analyzed_at': datetime.now().isoformat(),
        'total_entries': len(entries),
        'top_themes': themes[:10],
        'pending_todos': todos[:10],
        'key_insights': insights[:10],
    }
    
    with open(DIGEST_FILE, 'w') as f:
        json.dump(digest, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n🔥 热门主题:")
    for word, count in themes[:5]:
        print(f"  {word} ({count}次)")
    
    print(f"\n📋 待办事项 ({len(todos)}个):")
    for t in todos[:5]:
        print(f"  [{t['source']}] {t['action']}")
    
    print(f"\n💡 关键洞察 ({len(insights)}个):")
    for i in insights[:5]:
        print(f"  [{i['tag']}] {i['summary']}")
    
    print(f"\n✅ 完整摘要已保存到 {DIGEST_FILE}")

if __name__ == '__main__':
    main()
