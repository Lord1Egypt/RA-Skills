#!/usr/bin/env python3
"""
Daily Match Scanner - Find all today's matches across major leagues.
Fetches from The Odds API, filters upcoming matches, pipes JSON to
ev_calculator via stdin — zero local file writes.

Usage: python3 daily_scanner.py [--bankroll 8674] [--min-ev 2.0]
"""
import sys
import os
import json
import urllib.request
import urllib.parse
import subprocess
from datetime import datetime, timezone, timedelta

API_KEY = os.environ.get("ODDS_API_KEY", "")
BASE_URL = "https://api.the-odds-api.com/v4"

LEAGUES = {
    "英超": "soccer_epl",
    "西甲": "soccer_spain_la_liga",
    "德甲": "soccer_germany_bundesliga",
    "意甲": "soccer_italy_serie_a",
    "法甲": "soccer_france_ligue_one",
    "欧冠": "soccer_uefa_champs_league",
    "欧联": "soccer_uefa_europa_league",
    "欧协联": "soccer_uefa_europa_conference_league",
}


def fetch_odds(sport_key, regions="eu", markets="h2h,spreads,totals"):
    if not API_KEY:
        print("ERROR: ODDS_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    params = {
        "apiKey": API_KEY,
        "regions": regions,
        "markets": markets,
        "dateFormat": "iso",
        "oddsFormat": "decimal",
    }
    url = f"{BASE_URL}/sports/{sport_key}/odds?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            remaining = resp.headers.get("x-requests-remaining", "?")
            print(f"  [{sport_key}] quota remaining: {remaining}", file=sys.stderr)
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 422:
            return []
        print(f"  [{sport_key}] HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  [{sport_key}] Error: {e}", file=sys.stderr)
        return []


def filter_today(games, hours_ahead=36):
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(hours=hours_ahead)
    return [g for g in games
            if now <= datetime.fromisoformat(
                g["commence_time"].replace("Z", "+00:00")) <= cutoff]


def beijing_time(utc_str):
    dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    return (dt + timedelta(hours=8)).strftime("%m-%d %H:%M")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bankroll", type=float, default=10000)
    parser.add_argument("--min-ev", type=float, default=2.0)
    parser.add_argument("--hours-ahead", type=float, default=36)
    parser.add_argument("--leagues", nargs="+", default=list(LEAGUES.keys()))
    args = parser.parse_args()

    print(f"\n🔍 扫描未来 {args.hours_ahead:.0f}h 内的赛事...")
    print(f"💰 资金池: ¥{args.bankroll:,.0f} | 最低EV: {args.min_ev:.1f}%\n")

    all_games = []

    for name, key in LEAGUES.items():
        if name not in args.leagues:
            continue
        games = fetch_odds(key)
        today_games = filter_today(games, args.hours_ahead)
        if today_games:
            print(f"  ✅ {name}: {len(today_games)} 场")
            for g in today_games:
                g["_league"] = name
                g["_league_key"] = key
                all_games.append(g)
        else:
            print(f"  ⭕ {name}: 无比赛")

    if not all_games:
        print("\n❌ 无比赛")
        sys.exit(0)

    print(f"\n📋 共 {len(all_games)} 场，开始EV分析...\n")

    # 通过 stdin 管道把 JSON 传给 ev_calculator，零文件写入
    ev_script = str(((__import__('pathlib')).Path(__file__).parent / "ev_calculator.py"))
    proc = subprocess.run(
        [sys.executable, ev_script, "--stdin",
         "--min-ev", str(args.min_ev),
         "--bankroll", str(args.bankroll)],
        input=json.dumps(all_games),
        text=True,
    )

    print(f"\n{'=' * 60}")
    print("📅 今日赛程 (北京时间):")
    print(f"{'=' * 60}")
    for g in sorted(all_games, key=lambda x: x["commence_time"]):
        print(f"  {beijing_time(g['commence_time'])}  "
              f"[{g['_league']}]  {g['home_team']} vs {g['away_team']}")


if __name__ == "__main__":
    main()
