#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scrapling[ai]",
#     "beautifulsoup4",
# ]
# ///
"""
CPBL 戰績排名查詢
使用官方 API: /standings/seasonaction
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
from _cpbl_api import post_api_html


TABLE_KEY_MAP = {
    '球隊對戰戰績': 'versus',
    '團隊投球成績': 'pitching',
    '團隊打擊成績': 'batting',
    '團隊守備成績': 'fielding',
}

KIND_LABELS = {
    'A': '一軍',
    'D': '二軍',
}


def clean_cell_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.replace('\xa0', ' ').strip())


def parse_cell(cell) -> str:
    return clean_cell_text(cell.get_text(' ', strip=True))


def parse_versus_first_cell(cell) -> tuple[Optional[int], str]:
    rank_el = cell.select_one('.rank')
    team_el = cell.select_one('.team-w-trophy a, .team-w-trophy')

    rank = None
    if rank_el:
        rank_text = clean_cell_text(rank_el.get_text())
        if rank_text.isdigit():
            rank = int(rank_text)

    team = parse_cell(team_el) if team_el else parse_cell(cell)
    if rank is not None and team.startswith(str(rank)):
        team = team[len(str(rank)):].strip()

    return rank, team


def parse_table(caption: str, table) -> list[dict]:
    rows = table.find_all('tr')
    if not rows:
        return []

    headers = [parse_cell(th) for th in rows[0].find_all(['th', 'td'])]
    data = []

    for row in rows[1:]:
        cols = row.find_all('td')
        if not cols:
            continue

        values = [parse_cell(td) for td in cols]
        item = {}

        if caption == '球隊對戰戰績':
            rank, team = parse_versus_first_cell(cols[0])
            item['排名'] = rank
            item['球隊'] = team
            start_idx = 1
            header_slice = headers[1:]
            value_slice = values[1:]
        else:
            start_idx = 0
            header_slice = headers
            value_slice = values
            if value_slice:
                item['球隊'] = value_slice[0]

        for idx, header in enumerate(header_slice):
            if idx < len(value_slice):
                item[header] = value_slice[idx]

        if caption != '球隊對戰戰績' and '球隊' in item:
            item['球隊'] = value_slice[0] if value_slice else ''

        data.append(item)

    return data


def query_standings(
    year: Optional[int] = None,
    kind: str = 'A'
) -> dict:
    """查詢球隊戰績與團隊成績表。"""
    if year is None:
        year = datetime.now().year

    try:
        html = post_api_html('/standings/seasonaction', {
            'year': str(year),
            'kindCode': kind
        })

        soup = BeautifulSoup(html, 'html.parser')
        wraps = soup.select('.RecordTableWrap')
        result = {
            'year': year,
            'kind': kind,
            'kind_label': KIND_LABELS.get(kind, kind),
            'source': 'api',
            'url': f'https://cpbl.com.tw/standings?KindCode={kind}',
            'data': {},
        }

        for wrap in wraps:
            caption_el = wrap.select_one('.record_table_caption')
            table = wrap.find('table')
            if not caption_el or not table:
                continue

            caption = parse_cell(caption_el)
            key = TABLE_KEY_MAP.get(caption)
            if not key:
                continue

            result['data'][key] = parse_table(caption, table)

        if not result['data']:
            result['source'] = 'api_limited'
            result['message'] = '戰績頁回傳內容異常或沒有可解析表格'
            result['data'] = {
                'versus': [],
                'pitching': [],
                'batting': [],
                'fielding': [],
            }

        return result

    except Exception as e:
        return {
            'year': year,
            'kind': kind,
            'kind_label': KIND_LABELS.get(kind, kind),
            'source': 'error',
            'error': str(e),
            'message': '無法取得戰績資料',
            'url': f'https://cpbl.com.tw/standings?KindCode={kind}',
            'data': {
                'versus': [],
                'pitching': [],
                'batting': [],
                'fielding': [],
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description='CPBL 戰績排名查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢今年一軍戰績
  uv run cpbl_standings.py

  # 查詢 2025 年戰績
  uv run cpbl_standings.py --year 2025

  # 查詢二軍戰績
  uv run cpbl_standings.py --kind D --output text
        '''
    )

    parser.add_argument('--year', '-y', type=int, help='年份（預設今年）')
    parser.add_argument('--kind', '-k', type=str, default='A', choices=['A', 'D'],
                        help='A=一軍 D=二軍（預設 A）')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')

    args = parser.parse_args()

    try:
        standings = query_standings(year=args.year, kind=args.kind)

        if args.output == 'json':
            print(json.dumps(standings, ensure_ascii=False, indent=2))
        else:
            versus = standings['data'].get('versus', [])
            print(f"年份: {standings['year']}")
            print(f"軍種: {standings.get('kind_label', standings['kind'])}")
            print(f"來源: {standings['source']}")
            print()

            if not versus:
                print(standings.get('message', '沒有找到戰績資料'))
                print(f"\n官網連結: {standings['url']}")
                return

            print('球隊對戰戰績')
            print('────────────────────────────────────────')
            for row in versus:
                print(
                    f"{row.get('排名', '-')}. {row.get('球隊', '')}  "
                    f"{row.get('勝-和-敗', '')}  "
                    f"勝率 {row.get('勝率', '')}  "
                    f"勝差 {row.get('勝差', '')}  "
                    f"近十場 {row.get('近十場戰績', '')}"
                )

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
