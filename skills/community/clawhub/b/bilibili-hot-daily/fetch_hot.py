#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站热点日报 v2.0 - 自动抓取哔哩哔哩热门视频排行榜
作者: 小天🦞
版本: 2.0.0
"""

import argparse
import json
import csv
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# B站API地址
POPULAR_API = "https://api.bilibili.com/x/web-interface/popular"


class BilibiliHotFetcher:
    """B站热门视频抓取器 v2.0"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
            'Accept': 'application/json, text/plain, */*'
        }

    def fetch_hot(self, top: int = 20) -> List[Dict]:
        """获取热门视频"""
        url = f"{POPULAR_API}?ps={top}"

        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            if data.get('code') != 0:
                print(f"[ERROR] API错误: {data.get('message', '未知错误')}", file=sys.stderr)
                return []

            videos = data.get('data', {}).get('list', [])[:top]
            return [self._parse_video(v, i+1) for i, v in enumerate(videos)]

        except Exception as e:
            print(f"[ERROR] 获取失败: {e}", file=sys.stderr)
            return []

    def _parse_video(self, video: Dict, rank: int) -> Dict:
        """解析视频数据"""
        stat = video.get('stat', {})
        owner = video.get('owner', {})

        return {
            'rank': rank,
            'title': video.get('title', ''),
            'bvid': video.get('bvid', ''),
            'url': f"https://b23.tv/{video.get('bvid', '')}",
            'up': owner.get('name', ''),
            'up_mid': owner.get('mid', 0),
            'category': video.get('tname', ''),
            'views': stat.get('view', 0),
            'likes': stat.get('like', 0),
            'coins': stat.get('coin', 0),
            'favorites': stat.get('favorite', 0),
            'replies': stat.get('reply', 0),
            'danmaku': stat.get('danmaku', 0),
            'shares': stat.get('share', 0),
            'duration': video.get('duration', 0),
            'pubdate': video.get('pubdate', 0),
            'desc': video.get('desc', '')[:100] + '...' if len(video.get('desc', '')) > 100 else video.get('desc', '')
        }


def format_number(num: int) -> str:
    """格式化数字"""
    if num >= 100000000:
        return f"{num/100000000:.1f}亿"
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return str(num)


def format_duration(seconds: int) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{seconds}秒"
    minutes = seconds // 60
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}分{secs}秒"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}时{mins}分"


def generate_summary(videos: List[Dict]) -> str:
    """生成摘要"""
    if not videos:
        return "暂无数据"

    categories = {}
    total_views = 0
    total_likes = 0

    for v in videos:
        cat = v['category']
        categories[cat] = categories.get(cat, 0) + 1
        total_views += v['views']
        total_likes += v['likes']

    top_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
    cat_str = "、".join([c[0] for c in top_cats])

    return (
        f"[SUMMARY] B站热门视频日报\n"
        f"共 {len(videos)} 个热门视频\n"
        f"总播放：{format_number(total_views)}\n"
        f"总点赞：{format_number(total_likes)}\n"
        f"热门分区：{cat_str}\n"
        f"Top 1：{videos[0]['title']}\n"
        f"播放量：{format_number(videos[0]['views'])} | 点赞：{format_number(videos[0]['likes'])}"
    )


def output_json(videos: List[Dict], output_file: str, summary: str = ""):
    """输出JSON"""
    result = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'total': len(videos),
        'summary': summary,
        'videos': videos
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] 已保存到 {output_file}")


def output_csv(videos: List[Dict], output_file: str):
    """输出CSV"""
    if not videos:
        print("[ERROR] 没有数据")
        return

    fieldnames = ['rank', 'title', 'up', 'category', 'views', 'likes', 'coins', 'favorites', 'duration', 'url']

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for v in videos:
            row = {k: v.get(k, '') for k in fieldnames}
            row['duration'] = format_duration(v.get('duration', 0))
            writer.writerow(row)

    print(f"[OK] 已保存到 {output_file}")


def print_table(videos: List[Dict]):
    """打印表格"""
    if not videos:
        print("[ERROR] 没有数据")
        return

    print("")
    print("=" * 70)
    print(f"[HOT] B站热门视频日报 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    for v in videos:
        print("")
        print(f"#{v['rank']} {v['title']}")
        print(f"   UP主: {v['up']} | 分区: {v['category']} | 时长: {format_duration(v['duration'])}")
        print(f"   播放: {format_number(v['views'])} | 点赞: {format_number(v['likes'])} | 投币: {format_number(v['coins'])} | 收藏: {format_number(v['favorites'])}")
        if v.get('desc'):
            print(f"   简介: {v['desc'][:60]}...")
        print(f"   链接: {v['url']}")

    print("")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description='[HOT] B站热门视频日报 v2.0')
    parser.add_argument('--top', type=int, default=20, help='获取数量 (默认: 20)')
    parser.add_argument('--summary', action='store_true', help='生成摘要')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='输出格式')
    parser.add_argument('--quiet', action='store_true', help='静默模式')

    args = parser.parse_args()

    # 抓取数据
    fetcher = BilibiliHotFetcher()
    videos = fetcher.fetch_hot(top=args.top)

    if not videos:
        print("[ERROR] 未获取到数据")
        sys.exit(1)

    # 生成摘要
    summary = ""
    if args.summary:
        summary = generate_summary(videos)

    # 输出
    if not args.quiet:
        print_table(videos)
        if summary:
            print(f"\n{summary}")

    # 保存文件
    if args.output:
        if args.format == 'csv':
            output_csv(videos, args.output)
        else:
            output_json(videos, args.output, summary)

    return videos


if __name__ == '__main__':
    main()
