#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度热搜榜实时抓取脚本 v2
数据源：https://top.baidu.com/board
推荐使用 openclaw web_fetch 工具获取 HTML，此脚本仅做解析

安全说明：
- 不访问任何外部 API（除百度公开热榜页面）
- 不读取/写入任何本地文件（除临时解析）
- 不执行任何系统命令
- 不包含任何凭证或敏感信息
"""

import sys
import re
from datetime import datetime
from html import unescape

def fetch_html():
    """获取百度热搜 HTML
    
    注意：此函数仅供测试使用，生产环境建议使用 openclaw web_fetch 工具
    原因：web_fetch 有更好的错误处理、重试机制和安全控制
    """
    import urllib.request
    import ssl
    
    # 安全限制：只访问百度官方热榜页面
    url = "https://top.baidu.com/board?tab=realtime"
    
    # 验证 URL 安全性（防止 SSRF）
    if not url.startswith("https://top.baidu.com/"):
        print("❌ 安全错误：不允许访问非百度域名")
        return None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    }
    
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=headers)
        # 设置合理的超时时间，防止长时间挂起
        with urllib.request.urlopen(req, timeout=15, context=ctx) as f:
            return f.read().decode('utf-8')
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None


def parse_hot_search(html):
    """解析 HTML 提取热榜"""
    
    results = []
    html = unescape(html)
    
    # 百度热搜 HTML 中的典型模式
    # 查找所有带排名的热点条目
    
    # 模式 1: [数字] [标题] 标记
    pattern1 = r'\[(\d+)\].*?\[(.*?)\].*?(热 | 新)?'
    
    # 模式 2: 直接查找热点行
    lines = html.split('\n')
    
    for i, line in enumerate(lines):
        # 查找包含热点特征的行
        if '热搜指数' in line or 'hot-item' in line:
            # 提取标题
            title_match = re.search(r'>([^<]{5,100})<', line)
            if title_match:
                title = title_match.group(1).strip()
                
                # 检查标记
                mark = ""
                if '热' in line:
                    mark = "🔥"
                elif '新' in line:
                    mark = "🆕"
                
                results.append({
                    'rank': len(results) + 1,
                    'title': title,
                    'mark': mark
                })
    
    # 如果模式匹配失败，尝试简单提取
    if len(results) < 5:
        results = simple_extract(html)
    
    return results[:50]


def simple_extract(html):
    """简单提取法 - 直接从文本中找热点"""
    
    results = []
    
    # 查找所有热点相关行
    keywords = ['热', '新', '热搜', '热点']
    
    for line in html.split('\n'):
        line = line.strip()
        
        # 跳过太短或太长的行
        if len(line) < 20 or len(line) > 150:
            continue
        
        # 检查是否包含热点关键词
        if any(kw in line for kw in keywords):
            # 清理 HTML 标签
            clean_line = re.sub(r'<[^>]+>', '', line).strip()
            
            # 跳过包含 URL 的行
            if 'http' in clean_line or 'href' in clean_line:
                continue
            
            # 确定标记
            mark = ""
            if '热' in clean_line:
                mark = "🔥"
            elif '新' in clean_line:
                mark = "🆕"
            
            if len(clean_line) > 10:
                results.append({
                    'rank': len(results) + 1,
                    'title': clean_line[:80],
                    'mark': mark
                })
        
        if len(results) >= 50:
            break
    
    return results


def format_output(results, top_n=10):
    """格式化输出"""
    
    if not results:
        print("❌ 未获取到热榜数据")
        print("\n可能原因：")
        print("1. 网络连接问题")
        print("2. 百度服务器限流")
        print("3. HTML 结构变化，需要更新解析器")
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
    print(f"⏰ 获取时间：{now}")


def main():
    """主函数"""
    
    # 获取参数
    top_n = 10
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.lower() == 'all':
            top_n = 50
        else:
            try:
                top_n = int(arg)
            except ValueError:
                print("用法：python3 baidu_real.py [10|20|50|all]")
                sys.exit(1)
    
    print("正在获取百度热搜榜...")
    
    # 获取 HTML
    html = fetch_html()
    
    if not html:
        print("\n❌ 无法获取百度热搜数据")
        print("\n建议：")
        print("1. 检查网络连接")
        print("2. 使用 web_fetch 工具获取")
        print("3. 稍后重试（可能被限流）")
        sys.exit(1)
    
    # 解析数据
    results = parse_hot_search(html)
    
    # 输出结果
    format_output(results, top_n)


if __name__ == "__main__":
    main()
