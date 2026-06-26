#!/usr/bin/env python3
"""
ClawHub Top Skills Scraper
获取排名前20的技能 - 带完整介绍
"""

import json
import subprocess
import sys
import textwrap

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    lines = output.strip().split('\n')
    filtered = [l for l in lines if not l.startswith('- Fetching')]
    return '\n'.join(filtered)

def wrap_text(text, width=70):
    """文本换行"""
    return '\n'.join(textwrap.wrap(text, width=width))

def print_detailed_table(title, items, sort_key=None):
    print(f"\n{'='*90}")
    print(f"  {title}")
    print('='*90)
    
    for i, item in enumerate(items, 1):
        name = item.get('displayName', 'N/A')
        slug = item.get('slug', '')
        summary = item.get('summary', 'No description')
        stats = item.get('stats', {})
        downloads = stats.get('downloads', 0)
        installs_all = stats.get('installsAllTime', 0)
        stars = stats.get('stars', 0)
        comments = stats.get('comments', 0)
        
        print(f"\n{'─'*90}")
        print(f"#{i:2d}  {name}")
        print(f"     Slug: {slug}")
        print(f"     📥 下载: {downloads:,} | 📦 总安装: {installs_all:,} | ⭐ 评分: {stars} | 💬 评论: {comments}")
        print(f"     简介: {summary}")
        
        # 显示标签
        tags = item.get('tags', {})
        if tags:
            tag_str = ', '.join([f"{k}:{v}" for k,v in tags.items()])
            print(f"     标签: {tag_str}")
    
    print(f"\n{'='*90}")

def print_compact_table(title, items):
    print(f"\n{'='*120}")
    print(f"  {title}")
    print('='*120)
    print(f"{'排名':<4} | {'技能名称':<25} | {'下载':<10} | {'评分':<8} | 简介")
    print('-'*120)
    
    for i, item in enumerate(items, 1):
        name = (item.get('displayName', '')[:24] + ' ')[:25]
        downloads = item.get('stats', {}).get('downloads', 0)
        stars = item.get('stats', {}).get('stars', 0)
        summary = (item.get('summary', '')[:50] + ' ')[:50]
        
        print(f"{i:<4} | {name:<25} | {downloads:<10} | ⭐{stars:<7} | {summary}")

def main():
    print("="*120)
    print("  ClawHub Top 20 Skills - 完整介绍")
    print("="*120)
    
    # 1. 按总安装量 - 详细版
    print("\n📥 正在获取 Top 20 (按总下载量)...")
    cmd = 'clawhub explore --limit 20 --sort installsAllTime --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_detailed_table("📥 按总下载量排序 (Top 20)", items)
    except Exception as e:
        print(f"❌ 获取失败: {e}")
    
    # 2. 按评分 - 详细版
    print("\n⭐ 正在获取 Top 20 (按评分)...")
    cmd = 'clawhub explore --limit 20 --sort rating --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_detailed_table("⭐ 按评分排序 (Top 20)", items)
    except Exception as e:
        print(f"❌ 获取失败: {e}")
    
    # 3. Trending - 详细版
    print("\n🔥 正在获取 Top 20 (Trending)...")
    cmd = 'clawhub explore --limit 20 --sort trending --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_detailed_table("🔥 Trending (Top 20)", items)
    except Exception as e:
        print(f"❌ 获取失败: {e}")
    
    # 4. 紧凑表格汇总
    print("\n📊 汇总表格...")
    cmd = 'clawhub explore --limit 20 --sort installsAllTime --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_compact_table("📊 一览表 (Top 20)", items)
    except Exception as e:
        print(f"❌ 获取失败: {e}")
    
    print("\n" + "="*120)
    print("✅ 完成！")
    print("="*120)
    print("\n📌 安装命令示例:")
    print("   clawhub install gog          # Google Workspace")
    print("   clawhub install weather      # 天气查询")
    print("   clawhub install summarize    # 网页/文件摘要")
    print("   clawhub install github       # GitHub 操作")
    print("="*120)

if __name__ == '__main__':
    main()
