#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度热搜榜 - web_fetch 版本
通过 OpenClaw web_fetch 工具获取数据
"""

import sys
import json
from datetime import datetime

def process_web_fetch_result(html_content):
    """处理 web_fetch 返回的 HTML"""
    
    import re
    from html import unescape
    
    results = []
    html = unescape(html_content)
    
    # 从 HTML 中提取热点
    # 查找所有热点行
    
    lines = html.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 查找热点特征
        if any(kw in line for kw in ['热搜', '热', '新']):
            # 清理 HTML
            clean = re.sub(r'<[^>]+>', '', line).strip()
            
            # 跳过无效行
            if len(clean) < 10 or len(clean) > 100:
                continue
            if 'http' in clean or 'href' in clean:
                continue
            if clean.startswith('SECURITY NOTICE'):
                continue
            
            # 确定标记
            mark = ""
            if '热' in clean:
                mark = "🔥"
            elif '新' in clean:
                mark = "🆕"
            
            results.append({
                'rank': len(results) + 1,
                'title': clean[:80],
                'mark': mark
            })
        
        if len(results) >= 50:
            break
    
    return results


def format_output(results, top_n=10):
    """格式化输出"""
    
    if not results:
        print("❌ 未获取到热榜数据")
        return
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    actual_count = min(top_n, len(results))
    
    print(f"\n🔥 百度热搜榜 Top {actual_count} ({now})\n")
    print("=" * 70)
    
    for item in results[:actual_count]:
        rank = item['rank']
        title = item['title']
        mark = item.get('mark', '')
        
        mark_str = f" {mark}" if mark else ""
        print(f"{rank:2d}. {title}{mark_str}")
    
    print("=" * 70)
    print(f"\n📊 共获取 {len(results)} 条热点")
    print(f"📡 数据来源：https://top.baidu.com/board")


def main():
    """主函数"""
    
    top_n = 10
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.lower() == 'all':
            top_n = 50
        else:
            try:
                top_n = int(arg)
            except ValueError:
                print("用法：python3 baidu_fetch.py [10|20|50|all]")
                sys.exit(1)
    
    # 从 stdin 读取 web_fetch 结果
    print("请粘贴 web_fetch 返回的 HTML 内容（以 EOF 结束）：")
    html_content = sys.stdin.read()
    
    if not html_content:
        print("❌ 未接收到数据")
        sys.exit(1)
    
    # 处理数据
    results = process_web_fetch_result(html_content)
    
    # 输出
    format_output(results, top_n)


if __name__ == "__main__":
    main()
