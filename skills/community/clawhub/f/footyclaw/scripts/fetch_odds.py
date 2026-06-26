#!/usr/bin/env python3
"""
Fetch odds from The Odds API for a given sport/league.
Usage: python3 fetch_odds.py <sport_key> [regions] [markets]
Example: python3 fetch_odds.py soccer_epl eu h2h,spreads,totals

输出：人类可读赛事信息到 stdout，可通过 --json 参数输出原始 JSON。
零本地文件写入。
"""
import sys, os, json, urllib.request, urllib.parse
from datetime import datetime, timezone

API_KEY = os.environ.get("ODDS_API_KEY", "")
BASE_URL = "https://api.the-odds-api.com/v4"

def fetch_odds(sport_key, regions="eu", markets="h2h,spreads,totals"):
    if not API_KEY:
        print("ERROR: ODDS_API_KEY not set", file=sys.stderr)
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
            used = resp.headers.get("x-requests-used", "?")
            print(f"# API quota: {remaining} remaining / {used} used", file=sys.stderr)
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

def format_game(game):
    now = datetime.now(timezone.utc)
    commence = datetime.fromisoformat(game["commence_time"].replace("Z", "+00:00"))
    hours_until = (commence - now).total_seconds() / 3600
    home, away = game["home_team"], game["away_team"]
    lines = [f"\n{'='*60}"]
    lines.append(f"🆔 {game['id']}")
    lines.append(f"⚽ {home} vs {away}")
    lines.append(f"🕐 {commence.strftime('%Y-%m-%d %H:%M UTC')} ({hours_until:.1f}h away)")
    lines.append("="*60)

    for bm in game.get("bookmakers", []):
        bk = bm["key"]
        for market in bm.get("markets", []):
            mk, outcomes = market["key"], market["outcomes"]
            if mk == "h2h":
                s = " | ".join(f"{o['name']}: {o['price']:.2f}" for o in outcomes)
                lines.append(f"  [{bk}] 1X2: {s}")
            elif mk == "spreads":
                s = " | ".join(f"{o['name']} {o['point']:+.1f}: {o['price']:.2f}" for o in outcomes)
                lines.append(f"  [{bk}] AH:  {s}")
            elif mk == "totals":
                s = " | ".join(f"{o['name']} {o['point']}: {o['price']:.2f}" for o in outcomes)
                lines.append(f"  [{bk}] O/U: {s}")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_odds.py <sport_key> [regions] [markets] [--json]")
        print("sport_key: soccer_epl / soccer_spain_la_liga / soccer_germany_bundesliga")
        print("           soccer_italy_serie_a / soccer_france_ligue_one")
        print("           soccer_uefa_champs_league / soccer_uefa_europa_league")
        print("  --json   输出原始 JSON 到 stdout（供管道传给 ev_calculator）")
        sys.exit(1)

    # 解析 --json 标志
    raw_args = [a for a in sys.argv[1:] if a != "--json"]
    json_mode = "--json" in sys.argv

    sport_key = raw_args[0]
    regions = raw_args[1] if len(raw_args) > 1 else "eu"
    markets = raw_args[2] if len(raw_args) > 2 else "h2h,spreads,totals"
    games = fetch_odds(sport_key, regions, markets)

    if json_mode:
        # 纯 JSON 输出，方便管道传递
        print(json.dumps(games, indent=2))
    else:
        # 人类可读格式
        print(f"\n📋 {sport_key} — {len(games)} upcoming matches")
        for g in games:
            print(format_game(g))
