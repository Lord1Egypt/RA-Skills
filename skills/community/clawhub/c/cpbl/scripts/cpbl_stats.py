#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scrapling[ai]",
#     "beautifulsoup4",
# ]
# ///
"""
CPBL 球員數據查詢
使用官方 API: /stats/recordall
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path
from bs4 import BeautifulSoup

# 引入共用模組
sys.path.insert(0, str(Path(__file__).parent))
from _cpbl_api import post_api_html, resolve_team, resolve_team_cli, TEAM_ALIASES


def query_stats(
    year: Optional[int] = None,
    category: str = 'batting',
    team: Optional[str] = None,
    kind: str = 'A',
    top: Optional[int] = None
) -> list[dict]:
    """
    查詢球員數據

    Args:
        year: 年份（預設今年）
        category: batting/pitching
        team: 球隊過濾（部分匹配）
        kind: A=一軍, W=二軍
        top: 限制筆數

    Returns:
        數據列表
    """
    if year is None:
        year = datetime.now().year

    # position: 01=打擊, 02=投球
    # sortby: 01=主要指標（打擊率/防禦率）
    position = '01' if category == 'batting' else '02'

    html = post_api_html('/stats/recordall', {
        'year': str(year),
        'kindcode': kind,
        'position': position,
        'sortby': '01'
    })

    # 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    if not table:
        return []

    rows = table.find_all('tr')

    # 第一行是標題
    header_row = rows[0]
    col_headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

    # 預先彙整指定球隊的所有別名（含正式名稱），用於前綴匹配
    team_prefixes: set[str] = set()
    if team:
        team_prefixes.add(team)
        for alias, full_name in TEAM_ALIASES.items():
            if full_name == team:
                team_prefixes.add(alias)

    # 解析資料行
    stats = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if not cols:
            continue

        values = [td.get_text(strip=True) for td in cols]

        # 建立資料字典
        stat = {}
        for i, header in enumerate(col_headers):
            if i < len(values):
                stat[header] = values[i]

        # 簡化輸出格式
        raw_name = stat.get('排名球員', '')

        # 解析格式：如 "1台鋼雄鷹吳念庭"
        # 移除排名數字，剩下的格式如 "台鋼雄鷹吳念庭"
        clean_name = re.sub(r'^\d+', '', raw_name)

        # 球隊過濾（用前綴匹配去除排名後的球員名稱）
        if team_prefixes:
            if not any(clean_name.startswith(prefix) for prefix in team_prefixes):
                continue

        # 提取排名（第一個數字）
        rank_match = re.match(r'^(\d+)', raw_name)
        rank_num = int(rank_match.group(1)) if rank_match else 0

        player_info = {
            'rank': rank_num,
            'player': clean_name,  # 包含球隊+球員名，保留原始資訊
        }

        # 加入主要數據
        if category == 'batting':
            player_info.update({
                'avg': stat.get('打擊率'),
                'games': stat.get('出賽數'),
                'hits': stat.get('安打'),
                'hr': stat.get('全壘打'),
                'rbi': stat.get('打點'),
                'runs': stat.get('得分'),
            })
        else:
            player_info.update({
                'era': stat.get('防禦率'),
                'wins': stat.get('勝'),
                'losses': stat.get('敗'),
                'saves': stat.get('救援'),
                'strikeouts': stat.get('奪三振'),
            })

        stats.append(player_info)

    # 限制筆數
    if top:
        stats = stats[:top]

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='CPBL 球員數據查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢今年打擊排行榜
  uv run cpbl_stats.py --category batting

  # 查詢 2025 年投手數據（前 10 名）
  uv run cpbl_stats.py --year 2025 --category pitching --top 10

  # 查詢特定球隊
  uv run cpbl_stats.py --team 中信 --category batting

  # 查詢二軍數據
  uv run cpbl_stats.py --kind W --category batting
        '''
    )

    parser.add_argument('--year', '-y', type=int, help='年份（預設今年）')
    parser.add_argument('--category', '-c', type=str, default='batting',
                        choices=['batting', 'pitching'],
                        help='batting=打擊, pitching=投手（預設 batting）')
    parser.add_argument('--team', '-t', type=str, help='球隊過濾（部分匹配）')
    parser.add_argument('--kind', '-k', type=str, default='A', choices=['A', 'W'],
                        help='A=一軍, W=二軍（預設 A）')
    parser.add_argument('--top', type=int, default=10, help='限制筆數（預設 10）')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')

    args = parser.parse_args()

    # 球隊名稱模糊匹配（未知球隊保留原始輸入做 fallback，避免取消過濾）
    team = resolve_team_cli(args.team) or args.team

    try:
        stats = query_stats(
            year=args.year,
            category=args.category,
            team=team,
            kind=args.kind,
            top=args.top
        )

        if args.output == 'json':
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            if not stats:
                print('沒有找到球員數據')
                return

            category_name = '打擊' if args.category == 'batting' else '投手'
            print(f"找到 {len(stats)} 位 {category_name}球員:\n")

            for i, s in enumerate(stats, 1):
                if args.category == 'batting':
                    print(f"{i}. {s['player']} - 打擊率: {s.get('avg', '')} HR: {s.get('hr', '')} RBI: {s.get('rbi', '')}")
                else:
                    print(f"{i}. {s['player']} - 防禦率: {s.get('era', '')} 勝: {s.get('wins', '')} 敗: {s.get('losses', '')}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
