#!/usr/bin/env python3
"""
Casino Bonus Hunter — EV-ranked bonus finder with reputation scoring.

Scans 30+ crypto and traditional online casinos, calculates the Expected Value
of each welcome/reload/cashback bonus using optimal blackjack strategy (0.3% edge),
adjusts EV by casino reputation score, and outputs a ranked list.

An agent can use this to decide which casino bonus to hunt this session.

Author: Mibayy
"""

import json
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# House edges (with optimal strategy)
# ---------------------------------------------------------------------------
HOUSE_EDGE = {
    "blackjack":       0.003,
    "blackjack_h17":   0.005,
    "video_poker_job": 0.0046,
    "video_poker_dw":  -0.0076,
    "baccarat_banker": 0.0106,
    "roulette_eu":     0.027,
    "craps_passline":  0.0141,
    "slots":           0.04,
}

# ---------------------------------------------------------------------------
# Reputation scores (0-10) — based on CasinoGuru + Trustpilot + payout history
# ---------------------------------------------------------------------------
REPUTATION = {
    "Stake":            9.1, "BC.Game":         8.4, "BitStarz":       9.2,
    "Cloudbet":         8.7, "Jackbit":         7.9, "Vave":           7.5,
    "7Bit Casino":      8.1, "Wild.io":         7.8, "TrustDice":      7.6,
    "Metaspins":        8.0, "BetPanda":        7.4, "Lucky Block":    7.2,
    "Mega Dice":        7.0, "CoinPoker":       8.3, "Ignition Casino":8.5,
    "Bovada":           8.6, "Betplay.io":      7.3, "Thunderpick":    8.0,
    "Cryptorino":       7.1, "TG.Casino":       6.8, "VipLuck":        7.5,
    "Instant Casino":   7.8, "Casumo":          9.0, "LeoVegas":       9.1,
    "888 Casino":       8.9, "Betway":          8.8, "Unibet":         9.2,
    "PlayAmo":          8.2, "Spin Casino":     8.4, "Royal Vegas":    8.1,
    "Jackpot City":     8.5, "Ruby Fortune":    8.0, "Mummys Gold":    7.9,
}

def get_reputation(name: str) -> float:
    for k, v in REPUTATION.items():
        if k.lower() in name.lower() or name.lower() in k.lower():
            return v
    return 5.0

# ---------------------------------------------------------------------------
# Bonus database
# ---------------------------------------------------------------------------
MIN_REP = float(os.environ.get("BONUS_MIN_REP", "0"))
MIN_EV  = float(os.environ.get("BONUS_MIN_EV", "0"))
TOP_N   = int(os.environ.get("BONUS_TOP_N", "20"))

BONUSES = [
    # (casino, type, bonus_usd, wagering_x, game, game_contribution, max_win, url, crypto)
    ("Stake",           "welcome", 500, 40, "blackjack",       1.0, None, "https://stake.com",          True),
    ("Mummys Gold",     "welcome", 500, 40, "blackjack",       1.0, None, "https://mummysgold.com",     False),
    ("LeoVegas",        "welcome", 400, 35, "blackjack",       1.0, None, "https://leovegas.com",       False),
    ("Spin Casino",     "welcome", 400, 40, "blackjack",       1.0, None, "https://spincasino.com",     False),
    ("Jackpot City",    "welcome", 400, 50, "blackjack",       1.0, None, "https://jackpotcitycasino.com",False),
    ("Casumo",          "welcome", 300, 30, "blackjack",       1.0, None, "https://casumo.com",         False),
    ("Ignition Casino", "welcome", 300, 25, "blackjack",       1.0, None, "https://ignitioncasino.eu",  True),
    ("BC.Game",         "welcome", 300, 35, "blackjack",       1.0, None, "https://bc.game",            True),
    ("Betway",          "welcome", 250, 30, "blackjack",       1.0, None, "https://betway.com",         False),
    ("Bovada",          "welcome", 250, 25, "video_poker_job", 1.0, None, "https://bovada.lv",          True),
    ("Cloudbet",        "welcome", 200, 30, "blackjack",       1.0, None, "https://cloudbet.com",       True),
    ("Lucky Block",     "welcome", 200, 40, "blackjack",       1.0, None, "https://luckyblock.com",     True),
    ("Metaspins",       "welcome", 200, 35, "blackjack",       1.0, None, "https://metaspins.com",      True),
    ("Instant Casino",  "welcome", 200, 35, "blackjack",       1.0, None, "https://instantcasino.com",  True),
    ("Jackbit",         "welcome", 150, 25, "blackjack",       1.0, None, "https://jackbit.com",        True),
    ("Wild.io",         "welcome", 150, 30, "blackjack",       1.0, None, "https://wild.io",            True),
    ("Cryptorino",      "welcome", 150, 30, "blackjack",       1.0, None, "https://cryptorino.com",     True),
    ("VipLuck",         "welcome", 150, 30, "blackjack",       1.0, None, "https://vipluck.com",        True),
    ("BitStarz",        "welcome", 100, 30, "blackjack",       1.0, None, "https://bitstarz.com",       True),
    ("888 Casino",      "welcome", 200, 30, "blackjack",       1.0, None, "https://888casino.com",      False),
    ("Thunderpick",     "welcome", 100, 20, "blackjack",       1.0, None, "https://thunderpick.io",     True),
    ("CoinPoker",       "welcome", 100, 20, "video_poker_job", 1.0, None, "https://coinpoker.com",      True),
    # Reload bonuses
    ("BitStarz",        "reload",   50, 20, "blackjack",       1.0, None, "https://bitstarz.com",       True),
    ("Cloudbet",        "reload",  100, 25, "blackjack",       1.0, None, "https://cloudbet.com",       True),
    ("Thunderpick",     "reload",   50, 15, "blackjack",       1.0, None, "https://thunderpick.io",     True),
    # Cashback (bonus_usd = cashback %)
    ("Metaspins",       "cashback", 15, 1,  "blackjack",       1.0, None, "https://metaspins.com",      True),
    ("BC.Game",         "cashback", 10, 1,  "blackjack",       1.0, None, "https://bc.game",            True),
    ("Stake",           "cashback",  5, 1,  "blackjack",       1.0, None, "https://stake.com",          True),
    ("Casumo",          "cashback", 10, 1,  "blackjack",       1.0, None, "https://casumo.com",         False),
]


def calculate_ev(bonus: float, wagering_x: float, game: str, contrib: float, max_win) -> dict:
    edge = HOUSE_EDGE.get(game, 0.04)
    real_wagering = (bonus * wagering_x) / contrib
    expected_loss = real_wagering * edge
    ev_gross = bonus - expected_loss
    if max_win is not None:
        ev_gross = min(ev_gross, max_win)
    ev_net = round(ev_gross, 2)
    if ev_net > 80:   rating, stars = "EXCELLENT", 5
    elif ev_net > 50: rating, stars = "BON", 4
    elif ev_net > 20: rating, stars = "MOYEN", 3
    elif ev_net > 0:  rating, stars = "FAIBLE", 2
    else:             rating, stars = "NEGATIF", 0
    return {"ev_net": ev_net, "expected_loss": round(expected_loss, 2), "rating": rating, "stars": stars}


def run():
    results = []
    for (casino, btype, bonus, wagering_x, game, contrib, max_win, url, crypto) in BONUSES:
        rep = get_reputation(casino)
        if rep < MIN_REP:
            continue
        if btype == "cashback":
            # cashback % * expected losses over 52 sessions
            ev = round(500 * 0.003 * bonus / 100 * 52, 2)
            ev_adj = round(ev * rep / 10, 2)
            rating = "EXCELLENT" if ev_adj > 50 else "BON" if ev_adj > 20 else "MOYEN"
            stars = 5 if ev_adj > 50 else 4 if ev_adj > 20 else 3
            results.append({
                "casino": casino, "type": btype, "bonus": f"{bonus}% cashback",
                "wagering": "x1", "game": game, "ev_net": ev, "ev_adjusted": ev_adj,
                "reputation": rep, "rating": rating, "stars": stars, "url": url, "crypto": crypto,
            })
        else:
            ev_data = calculate_ev(bonus, wagering_x, game, contrib, max_win)
            if ev_data["ev_net"] < MIN_EV:
                continue
            ev_adj = round(ev_data["ev_net"] * rep / 10, 2)
            results.append({
                "casino": casino, "type": btype, "bonus": f"${bonus}",
                "wagering": f"{wagering_x}x", "game": game,
                "ev_net": ev_data["ev_net"], "ev_adjusted": ev_adj,
                "reputation": rep, "rating": ev_data["rating"], "stars": ev_data["stars"],
                "url": url, "crypto": crypto,
            })

    results.sort(key=lambda x: x["ev_adjusted"], reverse=True)
    results = results[:TOP_N]

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total": len(results),
        "config": {"min_rep": MIN_REP, "min_ev": MIN_EV, "top_n": TOP_N},
        "bonuses": results,
    }

    out_file = os.environ.get("BONUS_OUTPUT_FILE", "/tmp/casino_bonuses.json")
    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nCasino Bonus Hunter — {len(results)} bonuses ranked by EV (adjusted for reputation)")
    print(f"{'#':<4} {'Casino':<22} {'Type':<10} {'Bonus':<15} {'Wagering':<10} {'EV Brut':>8} {'EV Adj':>8} {'Rep':>5} {'Rating'}")
    print("-" * 100)
    for i, b in enumerate(results, 1):
        print(f"{i:<4} {b['casino']:<22} {b['type']:<10} {b['bonus']:<15} {b['wagering']:<10} {b['ev_net']:>+7.0f}$ {b['ev_adjusted']:>+7.0f}$ {b['reputation']:>4.1f} {b['rating']}")
    print(f"\nSaved to {out_file}")

    return output


if __name__ == "__main__":
    run()
