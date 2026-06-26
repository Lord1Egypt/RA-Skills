#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scrapling[ai]",
# ]
# ///
"""
CPBL 比賽結果查詢
使用官方隱藏 API: /schedule/getgamedatas
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

# 引入共用模組
sys.path.insert(0, str(Path(__file__).parent))
from _cpbl_api import post_api, fetch_game_datas, KIND_NAMES, resolve_team_cli, validate_date, validate_month


def fetch_box_summary(year: str, kind: str, game_sno: str) -> dict:
    """
    從 /box/getlive 補抓已完賽詳細資料
    
    重用共用 CSRF token（透過 post_api），不再對每場比賽發 GET 請求取 token。
    """
    try:
        payload = post_api('/box/getlive', {
            'GameSno': str(game_sno),
            'KindCode': kind,
            'Year': str(year),
            'PrevOrNext': '',
            'PresentStatus': '',
        })
    except Exception as e:
        print(f'⚠️ box/getlive 呼叫失敗 (game_sno={game_sno}): {e}', file=sys.stderr)
        return {}

    if not payload.get('Success'):
        return {}

    summary: dict = {}
    curt = json.loads(payload.get('CurtGameDetailJson') or '{}')
    batting = json.loads(payload.get('BattingJson') or '[]')
    pitching = json.loads(payload.get('PitchingJson') or '[]')

    attendance = curt.get('AudienceCntBackend') or curt.get('AudienceCnt')
    if attendance is not None:
        summary['attendance'] = int(attendance)

    homeruns = []
    for b in batting:
        hr = int(b.get('HomeRunCnt') or 0)
        if hr > 0:
            item = {
                'player': b.get('HitterName'),
                'team': 'away' if str(b.get('VisitingHomeType')) == '1' else 'home',
                'count': hr,
            }
            if int(b.get('GrandSlamHomerunCnt') or 0) > 0:
                item['grand_slam'] = True
            homeruns.append(item)
    if homeruns:
        summary['home_runs'] = homeruns

    holds = []
    saves = []
    closer_name = curt.get('CloserPitcherName')
    for p in pitching:
        rp = int(p.get('ReliefPointCnt') or 0)
        sp = int(p.get('SavePointCnt') or 0)
        team_side = 'away' if str(p.get('VisitingHomeType')) == '1' else 'home'
        if rp > 0:
            holds.append({'player': p.get('PitcherName'), 'team': team_side, 'count': rp})
        is_real_save = str(p.get('IsSaveOK')) == '1' or (closer_name and p.get('PitcherName') == closer_name and sp > 0)
        if is_real_save:
            saves.append({'player': p.get('PitcherName'), 'team': team_side, 'count': max(sp, 1)})
    if holds:
        summary['holds'] = holds
    if saves:
        summary['saves'] = saves

    return summary


def query_games(
    year: Optional[int] = None,
    month: Optional[str] = None,
    date: Optional[str] = None,
    team: Optional[str] = None,
    kind: str = 'A',
    limit: Optional[int] = None
) -> list[dict]:
    """
    查詢比賽結果
    
    Args:
        year: 年份（預設今年）
        date: 特定日期 (YYYY-MM-DD)
        team: 球隊名過濾（部分匹配）
        kind: 賽事類型代碼（預設 A）
        limit: 限制筆數
    
    Returns:
        比賽列表
    """
    if year is None:
        year = datetime.now().year
    
    # 呼叫共用函式取得整年資料（含 TTL 快取）
    raw_games = fetch_game_datas(year, kind)
    
    # 過濾與轉換資料（不含 box detail）
    games = []
    for g in raw_games:
        game_date_str = g.get('GameDate', '')[:10]
        
        # 日期過濾
        if date and game_date_str != date:
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
        
        away_score = g.get('VisitingScore')
        home_score = g.get('HomeScore')
        has_score = away_score is not None and home_score is not None

        # 只保留已完賽場次 CPBL 的 PresentStatus 不可靠 已完賽常常也標 1
        game_end = g.get('GameDateTimeE')
        ended_by_time = False
        if game_end:
            try:
                ended_by_time = datetime.fromisoformat(game_end) <= datetime.now()
            except ValueError:
                ended_by_time = False
        if not (has_score and ended_by_time):
            continue

        # 轉換成統一格式
        game_data = {
            'date': g.get('GameDate', '')[:10],
            'game_sno': g.get('GameSno'),
            'away_team': g.get('VisitingTeamName'),
            'home_team': g.get('HomeTeamName'),
            'away_score': int(away_score) if has_score else None,
            'home_score': int(home_score) if has_score else None,
            'venue': g.get('FieldAbbe'),
            'duration': g.get('GameDuringTime') or None,
            'box_url': f"https://cpbl.com.tw/box/index?year={g.get('Year', year)}&kindCode={g.get('KindCode', kind)}&gameSno={g.get('GameSno')}",
            'live_url': f"https://cpbl.com.tw/box/live?year={g.get('Year', year)}&kindCode={g.get('KindCode', kind)}&gameSno={g.get('GameSno')}",
            '_year': str(g.get('Year', year)),
            '_kind': g.get('KindCode', kind),
        }

        if g.get('WinningPitcherName'):
            game_data['winning_pitcher'] = g.get('WinningPitcherName')
        if g.get('LoserPitcherName'):
            game_data['losing_pitcher'] = g.get('LoserPitcherName')
        if g.get('CloserName'):
            game_data['save_pitcher'] = g.get('CloserName')
        if g.get('MvpName'):
            game_data['mvp'] = g.get('MvpName')

        games.append(game_data)
    
    # 先排序（最新在前），再限制筆數，最後才批次抓取 box detail
    games.sort(key=lambda x: x['date'], reverse=True)
    if limit:
        games = games[:limit]

    # 並行抓取 box summary（ThreadPoolExecutor）
    def _fetch_detail(idx_game):
        idx, g = idx_game
        extra = fetch_box_summary(g['_year'], g['_kind'], str(g['game_sno']))
        return idx, extra

    with ThreadPoolExecutor(max_workers=min(6, len(games) or 1)) as executor:
        futures = {executor.submit(_fetch_detail, (i, g)): i for i, g in enumerate(games)}
        for future in as_completed(futures):
            try:
                idx, extra = future.result()
                games[idx].update(extra)
            except Exception as e:
                games[futures[future]]['detail_fetch_error'] = str(e)

    # 清理內部欄位
    for g in games:
        g.pop('_year', None)
        g.pop('_kind', None)
    
    return games


def main():
    parser = argparse.ArgumentParser(
        description='CPBL 比賽結果查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢 2025 年所有比賽（前 10 場）
  uv run cpbl_games.py --year 2025 --limit 10
  
  # 查詢特定日期
  uv run cpbl_games.py --date 2025-03-29
  
  # 查詢特定球隊
  uv run cpbl_games.py --team 中信 --year 2025
  
  # 查詢二軍比賽
  uv run cpbl_games.py --year 2025 --kind W
        '''
    )
    
    parser.add_argument('--year', '-y', type=int, help='年份（預設今年）')
    parser.add_argument('--month', '-M', type=str, help='月份過濾 (YYYY-MM)')
    parser.add_argument('--date', '-d', type=str, help='特定日期 (YYYY-MM-DD)')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援簡稱如：兄弟、獅、悍將）')
    parser.add_argument('--kind', '-k', type=str, default='A',
                        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'X'],
                        help='賽事類型（預設 A）。A=一軍例行賽 B=明星賽 C=總冠軍 D=二軍例行賽 E=季後挑戰賽 F=二軍總冠軍 G=一軍熱身賽 H=未來之星 X=國際交流賽')
    parser.add_argument('--limit', '-l', type=int, help='限制筆數')
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
        games = query_games(
            year=args.year,
            month=args.month,
            date=args.date,
            team=team,
            kind=args.kind,
            limit=args.limit
        )
        
        # 空結果預警
        if not games:
            query_year = args.year if args.year else datetime.now().year
            if query_year > datetime.now().year:
                print(f'⚠️ 該年份球季尚未開始', file=sys.stderr)
            else:
                print(f'⚠️ 目前沒有符合條件的賽事資料', file=sys.stderr)
        
        if args.output == 'json':
            print(json.dumps(games, ensure_ascii=False, indent=2))
        else:
            # 文字格式
            if not games:
                print('沒有找到比賽資料')
                return
            
            print(f"找到 {len(games)} 場比賽:\n")
            for g in games:
                if g.get('away_score') is not None:
                    score = f"{g['away_score']}:{g['home_score']}"
                    print(f"[{g['date']}] {g['away_team']} {score} {g['home_team']} @ {g['venue']}")
                    details = []
                    if g.get('winning_pitcher'):
                        details.append(f"勝 {g['winning_pitcher']}")
                    if g.get('losing_pitcher'):
                        details.append(f"敗 {g['losing_pitcher']}")
                    if g.get('save_pitcher'):
                        details.append(f"救援 {g['save_pitcher']}")
                    if g.get('mvp'):
                        details.append(f"MVP {g['mvp']}")
                    if g.get('attendance') is not None:
                        details.append(f"觀眾 {g['attendance']}")
                    if details:
                        print("  " + " | ".join(details))
                    if g.get('home_runs'):
                        hr_text = ' '.join(f"{x['player']} {x['count']}轟" + (' 滿貫' if x.get('grand_slam') else '') for x in g['home_runs'])
                        print(f"  全壘打: {hr_text}")
                    if g.get('holds'):
                        hold_text = ' '.join(f"{x['player']} {x['count']}H" for x in g['holds'])
                        print(f"  中繼點: {hold_text}")
                    if g.get('saves'):
                        save_text = ' '.join(f"{x['player']} {x['count']}SV" for x in g['saves'])
                        print(f"  救援點: {save_text}")
                else:
                    print(f"[{g['date']}] {g['away_team']} vs {g['home_team']} @ {g['venue']}")
    
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
