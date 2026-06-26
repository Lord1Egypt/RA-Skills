#!/usr/bin/env python3
"""
EV Calculator for football betting.
Usage:
  echo '<json>' | python3 ev_calculator.py --stdin --min-ev 2.0 --bankroll 10000
  python3 ev_calculator.py --stdin < odds.json --min-ev 2.0
"""
import sys, json, argparse
from typing import Optional

# Bookmakers to exclude from EV targets (per SKILL.md)
EXCLUDED_BOOKMAKERS = {"matchbook", "betfair_ex", "williamhill", "betonlineag"}
# Pinnacle is the sharp benchmark for fair probability
PINNACLE_KEY = "pinnacle"

def implied_prob(decimal_odds):
    return 1.0 / decimal_odds

def no_vig_prob(odds_list):
    raw = [implied_prob(o) for o in odds_list]
    total = sum(raw)
    return [p / total for p in raw]

def ev_percent(fair_prob, decimal_odds):
    return fair_prob * (decimal_odds - 1) - (1 - fair_prob)

def kelly_fraction(fair_prob, decimal_odds):
    b = decimal_odds - 1
    q = 1 - fair_prob
    k = (fair_prob * b - q) / b
    return max(0.0, k)

def _get_pinnacle_fair_probs(game, market_key):
    """Extract Pinnacle odds for a market and return de-vigged fair probs.
    Returns dict {outcome_name: fair_prob} or None if Pinnacle not available."""
    for bm in game.get("bookmakers", []):
        if bm["key"] != PINNACLE_KEY:
            continue
        for market in bm.get("markets", []):
            if market["key"] != market_key:
                continue
            outcomes = market["outcomes"]
            if len(outcomes) < 2:
                return None
            names = [o["name"] for o in outcomes]
            odds = [o["price"] for o in outcomes]
            probs = no_vig_prob(odds)
            return dict(zip(names, probs))
    return None

def analyze_game(game, min_ev=0.0):
    home, away = game["home_team"], game["away_team"]
    results = []
    market_odds = {}
    bm_odds_map = {}

    for bm in game.get("bookmakers", []):
        bk = bm["key"]
        bm_odds_map[bk] = {}
        for market in bm.get("markets", []):
            mk = market["key"]
            bm_odds_map[bk][mk] = {}
            if mk not in market_odds:
                market_odds[mk] = {}
            for o in market["outcomes"]:
                name, price = o["name"], o["price"]
                bm_odds_map[bk][mk][name] = price
                market_odds[mk].setdefault(name, []).append(price)

    for mk, outcome_map in market_odds.items():
        outcome_names = list(outcome_map.keys())
        if len(outcome_names) < 2:
            continue

        # Prefer Pinnacle fair probs; fall back to market average if unavailable
        pinnacle_probs = _get_pinnacle_fair_probs(game, mk)
        if pinnacle_probs:
            fair_prob_map = pinnacle_probs
        else:
            avg_odds = {n: sum(p)/len(p) for n, p in outcome_map.items()}
            fair_probs = no_vig_prob([avg_odds[n] for n in outcome_names])
            fair_prob_map = dict(zip(outcome_names, fair_probs))

        for bk, bk_markets in bm_odds_map.items():
            # Skip excluded bookmakers
            if bk in EXCLUDED_BOOKMAKERS:
                continue
            # Never compute EV for Pinnacle vs Pinnacle (per SKILL.md)
            if bk == PINNACLE_KEY and pinnacle_probs:
                continue
            if mk not in bk_markets:
                continue
            for name in outcome_names:
                if name not in bk_markets[mk]:
                    continue
                if name not in fair_prob_map:
                    continue
                price = bk_markets[mk][name]
                fp = fair_prob_map.get(name, 0)
                if fp <= 0:
                    continue
                ev = ev_percent(fp, price)
                kelly = kelly_fraction(fp, price)
                if ev >= min_ev:
                    if mk == "h2h":
                        label = f"1X2 → {name}"
                    elif mk == "spreads":
                        pt = next((o.get("point") for bm2 in game["bookmakers"]
                            if bm2["key"]==bk
                            for mkt in bm2["markets"] if mkt["key"]=="spreads"
                            for o in mkt["outcomes"] if o["name"]==name), None)
                        label = f"亚盘 → {name} {pt:+.1f}" if pt else f"亚盘 → {name}"
                    elif mk == "totals":
                        pt = next((o.get("point") for bm2 in game["bookmakers"]
                            if bm2["key"]==bk
                            for mkt in bm2["markets"] if mkt["key"]=="totals"
                            for o in mkt["outcomes"] if o["name"]==name), None)
                        label = f"大小球 → {name} {pt}" if pt else f"大小球 → {name}"
                    else:
                        label = f"{mk} → {name}"
                    results.append({
                        "match": f"{home} vs {away}",
                        "commence": game["commence_time"],
                        "bookmaker": bk, "market": mk,
                        "outcome": name, "label": label,
                        "odds": price, "fair_prob": fp,
                        "ev_pct": ev * 100, "kelly": kelly,
                    })
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true",
                        help="从 stdin 读取 JSON（替代文件参数）")
    parser.add_argument("odds_file", nargs="?", default=None,
                        help="赔率 JSON 文件路径（若未指定 --stdin）")
    parser.add_argument("--min-ev", type=float, default=2.0)
    parser.add_argument("--bankroll", type=float, default=10000)
    parser.add_argument("--kelly-fraction", type=float, default=0.25)
    args = parser.parse_args()

    # 从 stdin 或文件读取 JSON
    if args.stdin:
        raw = sys.stdin.read()
    elif args.odds_file:
        with open(args.odds_file) as f:
            raw = f.read()
    else:
        print("ERROR: 请指定 --stdin 或提供 odds_file 路径", file=sys.stderr)
        sys.exit(1)

    games = json.loads(raw)

    print(f"\n🎯 EV分析 — 最低EV: {args.min_ev:.1f}% | 资金池: ¥{args.bankroll:,.0f}")
    print("="*70)

    all_bets = []
    for game in games:
        all_bets.extend(analyze_game(game, min_ev=args.min_ev/100))

    if not all_bets:
        print(f"\n❌ 未找到 EV ≥ {args.min_ev}% 的机会，尝试降低 --min-ev")
        return

    all_bets.sort(key=lambda x: x["ev_pct"], reverse=True)
    print(f"\n📊 找到 {len(all_bets)} 个正EV机会:\n")

    max_stake_pct = 0.20  # 单注上限: 资金池 20% (SKILL.md 风控硬性上限)
    total_stake = 0
    for bet in all_bets:
        kelly_stake = args.bankroll * min(bet["kelly"], args.kelly_fraction)
        stake = round(min(kelly_stake, args.bankroll * max_stake_pct), 0)
        print(f"⚽ {bet['match']}")
        print(f"   📌 {bet['label']}  |  BK: {bet['bookmaker']}")
        print(f"   💰 赔率: {bet['odds']:.2f} | 公平概率: {bet['fair_prob']*100:.1f}%")
        print(f"   📈 EV: +{bet['ev_pct']:.1f}% | Kelly: {bet['kelly']*100:.1f}%")
        print(f"   💵 建议注额: ¥{stake:,.0f}")
        print()
        total_stake += stake

    print("="*70)
    print(f"合计建议注额: ¥{total_stake:,.0f}（占资金池 {total_stake/args.bankroll*100:.1f}%）")

if __name__ == "__main__":
    main()
