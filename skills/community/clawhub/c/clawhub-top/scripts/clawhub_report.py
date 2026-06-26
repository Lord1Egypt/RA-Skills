#!/usr/bin/env python3
"""
ClawHub Skills Reporter
获取 Top 20 + 最新 20 技能 - 行业动态
"""

import json
import subprocess
import sys
import textwrap
from datetime import datetime

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    lines = output.strip().split('\n')
    filtered = [l for l in lines if not l.startswith('- Fetching')]
    return '\n'.join(filtered)

def print_section(title, items):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)
    print(f"{'排名':<4} | {'技能名称':<20} | {'下载':<8} | {'评分':<6} | 简介")
    print('-'*80)
    
    for i, item in enumerate(items, 1):
        name = (item.get('displayName', '')[:19] + ' ')[:20]
        downloads = item.get('stats', {}).get('downloads', 0)
        stars = item.get('stats', {}).get('stars', 0)
        summary = (item.get('summary', '')[:40] + ' ')[:40]
        
        print(f"{i:<4} | {name:<20} | {downloads:<8} | ⭐{stars:<5} | {summary}")

def main():
    print("="*80)
    print(f"  ClawHub 行业动态 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("="*80)
    
    # 1. 最热门 (按总安装量)
    print("\n📥 正在获取热门技能...")
    cmd = 'clawhub explore --limit 20 --sort installsAllTime --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_section("🔥 热门技能 Top 20 (按下载量)", items)
    except Exception as e:
        print(f"❌ 获取热门失败: {e}")
    
    # 2. 最新发布
    print("\n🆕 正在获取最新技能...")
    cmd = 'clawhub explore --limit 20 --sort newest --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_section("🆕 最新发布 Top 20", items)
    except Exception as e:
        print(f"❌ 获取最新失败: {e}")
    
    # 3. Trending
    print("\n📈 正在获取趋势技能...")
    cmd = 'clawhub explore --limit 20 --sort trending --json 2>/dev/null'
    try:
        output = run_cmd(cmd)
        data = json.loads(output)
        items = data.get('items', [])
        print_section("📈 趋势上升 Top 20", items)
    except Exception as e:
        print(f"❌ 获取趋势失败: {e}")
    
    print("\n" + "="*80)
    print("✅ 获取完成！")
    print("="*80)
    print("\n📌 安装命令:")
    print("   clawhub install <技能名>")
    print("="*80)

if __name__ == '__main__':
    main()
