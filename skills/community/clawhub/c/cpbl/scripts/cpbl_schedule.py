#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scrapling[ai]",
# ]
# ///
"""
CPBL 賽程查詢
使用官方隱藏 API: /schedule/getgamedatas
只顯示還沒打的比賽
"""

import argparse
import json
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# 引入共用模組
sys.path.insert(0, str(Path(__file__).parent))
from _cpbl_api import fetch_game_datas, KIND_NAMES, resolve_team_cli, validate_date, validate_month


def query_schedule(
    year: Optional[int] = None,
    month: Optional[str] = None,
    date_filter: Optional[str] = None,
    team: Optional[str] = None,
    kind: str = 'A',
    limit: Optional[int] = None,
    include_completed: bool = False
) -> list[dict]:
    """
    查詢賽程
    
    Args:
        year: 年份（預設今年）
        month: 月份過濾 (YYYY-MM)
        date_filter: 特定日期 (YYYY-MM-DD)
        team: 球隊名過濾（部分匹配）
        kind: 賽事類型代碼（預設 A）
        limit: 限制筆數
        include_completed: 是否包含已完成的比賽
    
    Returns:
        賽程列表
    """
    if year is None:
        year = datetime.now().year
    
    # 呼叫共用函式取得整年資料（含 TTL 快取）
    raw_games = fetch_game_datas(year, kind)
    
    # 今日日期（用於過濾未來賽程）
    today = date.today()
    
    # 過濾與轉換資料
    schedule = []
    for g in raw_games:
        game_date_str = g.get('GameDate', '')[:10]
        game_date = datetime.strptime(game_date_str, '%Y-%m-%d').date()
        
        # 日期過濾
        if date_filter and game_date_str != date_filter:
            continue
        
        # 月份過濾
        if month and not game_date_str.startswith(month):
            continue
        
        # 球隊過濾（用正式名稱匹配）
        if team:
            away = g.get('VisitingTeamName', '')
            home = g.get('HomeTeamName', '')
            if team not in away and team not in home:
                continue
        
        # 檢查是否已完成
        away_score = g.get('VisitingScore')
        home_score = g.get('HomeScore')
        is_play_ball = g.get('IsPlayBall') == 'Y'
        has_result = bool(g.get('GameResult'))
        has_nonzero_score = (
            away_score is not None and home_score is not None
            and (away_score != 0 or home_score != 0)
        )
        is_completed = is_play_ball or has_result or has_nonzero_score
        
        # 預設只顯示未來賽程
        if not include_completed and is_completed:
            continue
        
        # 轉換格式
        game_data = {
            'date': game_date_str,
            'weekday': ['一', '二', '三', '四', '五', '六', '日'][game_date.weekday()],
            'time': g.get('GameDateTimeS', '')[11:16] if g.get('GameDateTimeS') else '',
            'away_team': g.get('VisitingTeamName'),
            'home_team': g.get('HomeTeamName'),
            'venue': g.get('FieldAbbe'),
        }
        
        # 如果已完成，加入比分
        if is_completed:
            game_data['away_score'] = away_score
            game_data['home_score'] = home_score
        
        schedule.append(game_data)
    
    # 排序（從舊到新）
    schedule.sort(key=lambda x: x['date'])
    
    # 限制筆數
    if limit:
        schedule = schedule[:limit]
    
    return schedule


def main():
    parser = argparse.ArgumentParser(
        description='CPBL 賽程查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢今年所有未來賽程
  uv run cpbl_schedule.py
  
  # 查詢特定日期
  uv run cpbl_schedule.py --date 2025-03-29
  
  # 查詢整月
  uv run cpbl_schedule.py --month 2025-03
  
  # 查詢特定球隊
  uv run cpbl_schedule.py --team 中信
  
  # 查詢二軍賽程
  uv run cpbl_schedule.py --kind W
  
  # 包含已完成的比賽
  uv run cpbl_schedule.py --all
        '''
    )
    
    parser.add_argument('--year', '-y', type=int, help='年份（預設今年）')
    parser.add_argument('--month', '-m', type=str, help='月份 (YYYY-MM)')
    parser.add_argument('--date', '-d', type=str, help='特定日期 (YYYY-MM-DD)')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援簡稱如：兄弟、獅、悍將）')
    parser.add_argument('--kind', '-k', type=str, default='A',
                        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'X'],
                        help='賽事類型（預設 A）。A=一軍例行賽 B=明星賽 C=總冠軍 D=二軍例行賽 E=季後挑戰賽 F=二軍總冠軍 G=一軍熱身賽 H=未來之星 X=國際交流賽')
    parser.add_argument('--limit', '-l', type=int, help='限制筆數')
    parser.add_argument('--all', '-a', action='store_true', dest='include_completed',
                        help='包含已完成的比賽')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')
    
    args = parser.parse_args()
    
    # 球隊名稱模糊匹配
    team = resolve_team_cli(args.team)

    # 驗證日期/月份格式
    if args.date:
        validate_date(args.date)
    if args.month:
        validate_month(args.month)

    # 顯示賽事類型
    kind_name = KIND_NAMES.get(args.kind, '未知')
    print(f'✅ 賽事類型：{kind_name} ({args.kind})', file=sys.stderr)
    
    try:
        schedule = query_schedule(
            year=args.year,
            month=args.month,
            date_filter=args.date,
            team=team,
            kind=args.kind,
            limit=args.limit,
            include_completed=args.include_completed
        )
        
        # 空結果預警
        if not schedule:
            query_year = args.year if args.year else datetime.now().year
            if query_year > datetime.now().year:
                print(f'⚠️ 該年份球季尚未開始', file=sys.stderr)
            else:
                print(f'⚠️ 目前沒有符合條件的賽事資料', file=sys.stderr)
        
        if args.output == 'json':
            print(json.dumps(schedule, ensure_ascii=False, indent=2))
        else:
            if not schedule:
                print('沒有找到賽程資料')
                return
            
            print(f"找到 {len(schedule)} 場賽程:\n")
            for g in schedule:
                if g.get('away_score') is not None:
                    print(f"[{g['date']}({g['weekday']})] {g['away_team']} {g['away_score']}:{g['home_score']} {g['home_team']} @ {g['venue']}")
                else:
                    print(f"[{g['date']}({g['weekday']}) {g['time']}] {g['away_team']} vs {g['home_team']} @ {g['venue']}")
    
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
