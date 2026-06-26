#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全平台热榜聚合 v5.0 - 修复微博API
作者: 小天🦞
版本: 5.0.0
"""

import argparse
import json
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class HotAggregator:
    """全平台热榜聚合器 v5.0"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

    def fetch_bilibili(self, top: int = 10) -> List[Dict]:
        """获取B站热门"""
        try:
            url = 'https://api.bilibili.com/x/web-interface/popular?ps=' + str(top)
            headers = {**self.headers, 'Referer': 'https://www.bilibili.com/'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            if data.get('code') == 0:
                videos = data.get('data', {}).get('list', [])[:top]
                return [{
                    'rank': i+1,
                    'title': v.get('title', ''),
                    'value': v.get('stat', {}).get('view', 0),
                    'value_text': f"{v.get('stat', {}).get('view', 0)//10000}万播放",
                    'author': v.get('owner', {}).get('name', ''),
                    'url': f"https://b23.tv/{v.get('bvid', '')}"
                } for i, v in enumerate(videos)]
        except Exception as e:
            print(f"[WARN] B站获取失败: {e}", file=sys.stderr)
        return []

    def fetch_douyin(self, top: int = 10) -> List[Dict]:
        """获取抖音热搜"""
        try:
            url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/'
            headers = {
                **self.headers,
                'Referer': 'https://www.douyin.com/',
                'Cookie': 'ttcid=0'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            if data.get('data'):
                word_list = data.get('data', {}).get('word_list', [])[:top]
                return [{
                    'rank': i+1,
                    'title': w.get('word', ''),
                    'value': w.get('hot_value', 0),
                    'value_text': f"{w.get('hot_value', 0)//10000}万热度" if w.get('hot_value', 0) > 10000 else f"{w.get('hot_value', 0)}热度",
                    'url': f"https://www.douyin.com/search/{urllib.request.quote(w.get('word', ''))}"
                } for i, w in enumerate(word_list)]
        except Exception as e:
            print(f"[WARN] 抖音获取失败: {e}", file=sys.stderr)
        return []

    def fetch_weibo(self, top: int = 10) -> List[Dict]:
        """获取微博热搜 - 使用有效Cookie"""
        try:
            url = 'https://weibo.com/ajax/side/hotSearch'
            headers = {
                **self.headers,
                'Referer': 'https://weibo.com/',
                'Cookie': 'SUB=_2AkMWJzUjf8NxqwFRmP8RxWjnaY10ywzEieKnc3-_JRMxHRl-yT9kqlcatRB6PaaX1URGBqDAY-2n7xAu7MM5S5jv7p5D'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            if data.get('ok') == 1:
                topics = data.get('data', {}).get('realtime', [])[:top]
                return [{
                    'rank': i+1,
                    'title': t.get('word', ''),
                    'value': t.get('num', 0),
                    'value_text': f"{t.get('num', 0)//10000}万热度" if t.get('num', 0) > 10000 else f"{t.get('num', 0)}热度",
                    'label': t.get('label_name', ''),
                    'url': f"https://s.weibo.com/weibo?q={urllib.request.quote(t.get('word', ''))}"
                } for i, t in enumerate(topics)]
        except Exception as e:
            print(f"[WARN] 微博获取失败: {e}", file=sys.stderr)
        return []

    def fetch_toutiao(self, top: int = 10) -> List[Dict]:
        """获取今日头条热榜"""
        try:
            url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
            headers = {
                **self.headers,
                'Referer': 'https://www.toutiao.com/'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            if data.get('data'):
                items = data.get('data', [])[:top]
                results = []
                for i, item in enumerate(items):
                    hot_value = item.get('HotValue', 0)
                    # 修复：HotValue 可能是字符串，转为整数
                    try:
                        hot_value = int(hot_value)
                    except (ValueError, TypeError):
                        hot_value = 0
                    value_text = f"{hot_value//10000}万热度" if hot_value > 10000 else f"{hot_value}热度"
                    results.append({
                        'rank': i+1,
                        'title': item.get('Title', ''),
                        'value': hot_value,
                        'value_text': value_text,
                        'url': item.get('Url', '')
                    })
                return results
        except Exception as e:
            print(f"[WARN] 今日头条获取失败: {e}", file=sys.stderr)
        return []

    def fetch_all(self, top: int = 5) -> Dict[str, List[Dict]]:
        """获取所有平台热榜"""
        return {
            'bilibili': self.fetch_bilibili(top),
            'douyin': self.fetch_douyin(top),
            'weibo': self.fetch_weibo(top),
            'toutiao': self.fetch_toutiao(top)
        }


def format_platform(name: str, items: List[Dict]) -> str:
    """格式化平台输出"""
    icons = {
        'bilibili': '[B站] B站热门',
        'douyin': '[抖音] 抖音热搜',
        'weibo': '[微博] 微博热搜',
        'toutiao': '[头条] 今日头条热榜'
    }
    icon = icons.get(name, name)

    if not items:
        return f"{icon}: 暂无数据"

    lines = [f"\n{icon} Top {len(items)}:"]
    for item in items:
        label = f" [{item['label']}]" if item.get('label') else ""
        lines.append(f"  #{item['rank']} {item['title']}{label} ({item['value_text']})")

    return '\n'.join(lines)


def generate_summary(all_data: Dict[str, List[Dict]]) -> str:
    """生成跨平台摘要"""
    total_items = sum(len(items) for items in all_data.values())
    platforms_with_data = sum(1 for items in all_data.values() if items)

    all_titles = []
    for platform, items in all_data.items():
        for item in items:
            all_titles.append((platform, item['title']))

    summary = f"[SUMMARY] 全平台热榜聚合摘要\n"
    summary += f"共获取 {total_items} 条热榜数据，覆盖 {platforms_with_data} 个平台\n"

    if all_titles:
        summary += f"今日热点：\n"
        for i, (platform, title) in enumerate(all_titles[:5], 1):
            summary += f"  {i}. [{platform}] {title}\n"

    return summary


def main():
    parser = argparse.ArgumentParser(description='[HOT] 全平台热榜聚合 v5.0')
    parser.add_argument('--top', type=int, default=5, help='每平台获取数量 (默认: 5)')
    parser.add_argument('--bilibili', action='store_true', help='只获取B站')
    parser.add_argument('--douyin', action='store_true', help='只获取抖音')
    parser.add_argument('--weibo', action='store_true', help='只获取微博')
    parser.add_argument('--toutiao', action='store_true', help='只获取头条')
    parser.add_argument('--summary', action='store_true', help='生成摘要')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--quiet', action='store_true', help='静默模式')

    args = parser.parse_args()

    aggregator = HotAggregator()

    # 确定要获取的平台
    platforms = []
    if args.bilibili: platforms.append('bilibili')
    if args.douyin: platforms.append('douyin')
    if args.weibo: platforms.append('weibo')
    if args.toutiao: platforms.append('toutiao')
    if not platforms: platforms = ['bilibili', 'douyin', 'weibo', 'toutiao']

    # 获取数据
    all_data = {}
    for platform in platforms:
        method = getattr(aggregator, f'fetch_{platform}', None)
        if method:
            all_data[platform] = method(args.top)

    # 输出
    if not args.quiet:
        print("\n" + "="*60)
        print(f"[HOT] 全平台热榜聚合 v5.0 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)

        for platform, items in all_data.items():
            print(format_platform(platform, items))

        print("\n" + "="*60)

    # 生成摘要
    summary = ""
    if args.summary:
        summary = generate_summary(all_data)
        if not args.quiet:
            print(f"\n{summary}")

    # 保存文件
    if args.output:
        result = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'platforms': {k: len(v) for k, v in all_data.items()},
            'summary': summary,
            'data': all_data
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[OK] 已保存到 {args.output}")

    return all_data


if __name__ == '__main__':
    main()
