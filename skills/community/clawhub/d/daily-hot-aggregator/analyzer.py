#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热榜数据分析工具 v1.0 - 数据对比、趋势分析、美化报告
作者: 小天🦞
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import Counter

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class HotAnalyzer:
    """热榜数据分析器"""

    def __init__(self, data_dir: str = 'hot_reports'):
        self.data_dir = data_dir

    def load_report(self, date_str: str, report_type: str = 'daily') -> Optional[Dict]:
        """加载指定日期的报告"""
        if report_type == 'daily':
            filepath = os.path.join(self.data_dir, f'daily_report_{date_str}.json')
        elif report_type == 'xiaohongshu':
            filepath = os.path.join(self.data_dir, f'xiaohongshu_report_{date_str}.json')
        else:
            return None
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def compare_days(self, today: str, yesterday: str) -> Dict:
        """对比两天的数据"""
        today_data = self.load_report(today)
        yesterday_data = self.load_report(yesterday)
        
        if not today_data or not yesterday_data:
            return {'error': '数据不完整，无法对比'}
        
        comparison = {
            'date': today,
            'compare_with': yesterday,
            'platforms': {}
        }
        
        for platform in ['bilibili', 'douyin', 'weibo', 'toutiao']:
            today_items = today_data.get('data', {}).get(platform, [])
            yesterday_items = yesterday_data.get('data', {}).get(platform, [])
            
            # 提取标题
            today_titles = {item.get('title', '') for item in today_items}
            yesterday_titles = {item.get('title', '') for item in yesterday_items}
            
            # 新上榜
            new_entries = today_titles - yesterday_titles
            # 下榜
            dropped_entries = yesterday_titles - today_titles
            # 持续在榜
            still_on = today_titles & yesterday_titles
            
            comparison['platforms'][platform] = {
                'new_count': len(new_entries),
                'dropped_count': len(dropped_entries),
                'still_count': len(still_on),
                'new_entries': list(new_entries)[:5],
                'dropped_entries': list(dropped_entries)[:5]
            }
        
        return comparison

    def get_trending_keywords(self, date_str: str, top_n: int = 10) -> List[tuple]:
        """获取当日热门关键词"""
        data = self.load_report(date_str)
        if not data:
            return []
        
        # 提取所有标题
        all_titles = []
        for platform in ['bilibili', 'douyin', 'weibo', 'toutiao']:
            items = data.get('data', {}).get(platform, [])
            for item in items:
                title = item.get('title', '')
                if title:
                    all_titles.append(title)
        
        # 简单的关键词提取（按字符频率）
        keywords = Counter()
        for title in all_titles:
            # 提取2-4字的词组
            for i in range(len(title) - 1):
                for length in [2, 3, 4]:
                    if i + length <= len(title):
                        word = title[i:i+length]
                        # 过滤纯数字和标点
                        if any('\u4e00' <= c <= '\u9fff' for c in word):
                            keywords[word] += 1
        
        # 过滤常见无意义词
        stop_words = {'的是', '什么', '这个', '那个', '怎么', '如何', '可以', '没有', '一个'}
        filtered = [(k, v) for k, v in keywords.most_common(top_n * 2) if k not in stop_words]
        
        return filtered[:top_n]

    def generate_html_report(self, date_str: str) -> str:
        """生成HTML美化报告"""
        data = self.load_report(date_str)
        if not data:
            return "<html><body><h1>没有数据</h1></body></html>"
        
        platforms_data = data.get('data', {})
        
        # 平台配置
        platform_config = {
            'bilibili': {'name': 'B站热门', 'icon': '📺', 'color': '#00a1d6', 'value_key': 'value_text'},
            'douyin': {'name': '抖音热搜', 'icon': '🎵', 'color': '#161823', 'value_key': 'value_text'},
            'weibo': {'name': '微博热搜', 'icon': '🔍', 'color': '#e6162d', 'value_key': 'value_text'},
            'toutiao': {'name': '今日头条', 'icon': '📰', 'color': '#ff6000', 'value_key': 'value_text'}
        }
        
        # 生成平台卡片HTML
        platform_cards = ''
        for platform_key, config in platform_config.items():
            items = platforms_data.get(platform_key, [])
            if not items:
                continue
            
            items_html = ''
            for i, item in enumerate(items[:10], 1):
                rank_class = 'top3' if i <= 3 else 'normal'
                value = item.get(config['value_key'], item.get('hot_value', ''))
                label = item.get('label_name', item.get('label', ''))
                label_html = f'<span class="label-tag">{label}</span>' if label else ''
                
                items_html += f'''
                <div class="hot-item">
                    <div class="rank {rank_class}">{i}</div>
                    <div class="item-info">
                        <div class="item-title">{item.get('title', '')}</div>
                    </div>
                    <div class="hot-value">{value}{label_html}</div>
                </div>'''
            
            platform_cards += f'''
            <div class="platform" style="border-top: 4px solid {config['color']}">
                <div class="platform-header">
                    <span>{config['icon']}</span>
                    <span>{config['name']}</span>
                </div>
                <div class="hot-list">{items_html}</div>
            </div>'''
        
        # 获取关键词
        keywords = self.get_trending_keywords(date_str, 8)
        keywords_html = ' '.join([f'<span class="keyword">{k}</span>' for k, v in keywords])
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔥 全平台热榜日报 - {date_str}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
.header {{ text-align: center; color: white; margin-bottom: 30px; }}
.header h1 {{ font-size: 2.2em; margin-bottom: 8px; text-shadow: 0 2px 4px rgba(0,0,0,.2); }}
.header p {{ opacity: .9; font-size: 1.1em; }}
.stats {{ display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }}
.stat-card {{ background: rgba(255,255,255,.2); backdrop-filter: blur(10px); border-radius: 12px; padding: 15px 25px; color: white; text-align: center; min-width: 120px; }}
.stat-card .num {{ font-size: 2em; font-weight: bold; }}
.stat-card .label {{ font-size: .9em; opacity: .9; }}
.keywords {{ background: rgba(255,255,255,.15); border-radius: 12px; padding: 15px; margin-bottom: 20px; text-align: center; }}
.keywords h3 {{ color: white; margin-bottom: 10px; }}
.keyword {{ display: inline-block; background: rgba(255,255,255,.3); color: white; padding: 5px 12px; border-radius: 20px; margin: 5px; font-size: .9em; }}
.platforms {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
.platform {{ background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,.15); }}
.platform-header {{ padding: 18px 20px; color: white; display: flex; align-items: center; gap: 10px; font-size: 1.2em; font-weight: 600; background: linear-gradient(135deg, #667eea, #764ba2); }}
.hot-list {{ padding: 10px 15px; }}
.hot-item {{ display: flex; align-items: center; padding: 10px 8px; border-bottom: 1px solid #f0f0f0; }}
.hot-item:last-child {{ border-bottom: none; }}
.rank {{ width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: .85em; margin-right: 12px; flex-shrink: 0; color: white; }}
.rank.top3 {{ background: linear-gradient(135deg, #ff6b6b, #ee5a24); }}
.rank.normal {{ background: #ddd; color: #666; }}
.item-info {{ flex: 1; min-width: 0; }}
.item-title {{ font-size: .95em; color: #333; }}
.hot-value {{ font-size: .8em; color: #999; margin-left: 10px; flex-shrink: 0; }}
.label-tag {{ display: inline-block; font-size: .7em; padding: 2px 6px; border-radius: 4px; margin-left: 6px; background: #ffe0e0; color: #e6162d; }}
.footer {{ text-align: center; color: rgba(255,255,255,.7); margin-top: 30px; font-size: .9em; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🔥 全平台热榜日报</h1>
<p>日期：{date_str} | 数据来源：B站、抖音、微博、头条 | Powered by 小天 🦞</p>
</div>
<div class="stats">
<div class="stat-card"><div class="num">{sum(len(v) for v in platforms_data.values())}</div><div class="label">热榜数据</div></div>
<div class="stat-card"><div class="num">{len(platforms_data)}</div><div class="label">覆盖平台</div></div>
</div>
<div class="keywords">
<h3>🔥 今日热词</h3>
{keywords_html}
</div>
<div class="platforms">
{platform_cards}
</div>
<div class="footer">
<p>🦞 全平台热榜日报 | 由 OpenClaw 驱动 | 免费使用，定制联系 QQ：2595075878</p>
</div>
</div>
</body>
</html>'''
        
        return html

    def save_html_report(self, date_str: str, output_path: str = None) -> str:
        """保存HTML报告"""
        html = self.generate_html_report(date_str)
        
        if not output_path:
            output_path = os.path.join(self.data_dir, f'report_{date_str}.html')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='📊 热榜数据分析工具 v1.0')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='分析日期')
    parser.add_argument('--compare', action='store_true', help='与前一天对比')
    parser.add_argument('--keywords', action='store_true', help='提取热词')
    parser.add_argument('--html', action='store_true', help='生成HTML报告')
    parser.add_argument('--output', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    analyzer = HotAnalyzer()
    
    if args.compare:
        yesterday = (datetime.strptime(args.date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        result = analyzer.compare_days(args.date, yesterday)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.keywords:
        keywords = analyzer.get_trending_keywords(args.date)
        print(f"\n🔥 {args.date} 热门关键词：")
        for k, v in keywords:
            print(f"  {k}: {v}")
    
    if args.html:
        output = analyzer.save_html_report(args.date, args.output)
        print(f"✅ HTML报告已生成: {output}")


if __name__ == '__main__':
    main()
