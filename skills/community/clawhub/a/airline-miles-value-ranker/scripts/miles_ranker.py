#!/usr/bin/env python3
"""Airline miles / points redemption ranker.

Evaluates redemption options as cents-per-point (CPP), ranks them
against per-currency anchor bands, and issues BURN / HOARD / NEVER
verdicts. Pure stdlib. State in scripts/data/miles_log.json.

Commands:
  evaluate  --label S --points N --realistic-fare $ --ceiling-fare $
             [--copay $] [--currency chase|amex|citi|cap1|bilt|
              united|delta|american|flying-blue|lifemiles|ana|
              alaska|avios] [--expiring-days N]
  compare                 ranked table of saved options + verdicts
  sweet-spots             known good redemption patterns to check
  clear                   wipe the saved option list
"""
import argparse
import json
import sys
import time
from pathlib import Path

DATA = Path(__file__).parent / "data" / "miles_log.json"

# (name, floor_cents, fair_lo, fair_hi, good_lo, good_hi, excellent_lo)
CURRENCIES = {
    "chase":       ("Chase UR",          1.0, 1.0, 1.25, 1.25, 1.8, 1.8),
    "amex":        ("Amex MR",           1.0, 1.0, 1.25, 1.25, 1.8, 1.8),
    "citi":        ("Citi ThankYou",     1.0, 1.0, 1.25, 1.25, 1.7, 1.7),
    "cap1":        ("Capital One",       1.0, 1.0, 1.2,  1.2,  1.5, 1.5),
    "bilt":        ("Bilt",              1.0, 1.0, 1.25, 1.25, 1.8, 1.8),
    "united":      ("United MileagePlus", 0.0, 0.8, 1.2, 1.2, 1.6, 1.6),
    "delta":       ("Delta SkyMiles",    0.0, 0.8, 1.2, 1.2, 1.5, 1.5),
    "american":    ("American AAdvantage", 0.0, 0.8, 1.2, 1.2, 1.6, 1.6),
    "flying-blue": ("Air France Flying Blue", 0.0, 0.8, 1.2, 1.2, 1.6, 1.6),
    "lifemiles":   ("Avianca LifeMiles", 0.0, 0.9, 1.3, 1.3, 1.7, 1.7),
    "ana":         ("ANA Mileage Club",  0.0, 1.0, 1.4, 1.4, 2.0, 2.0),
    "alaska":      ("Alaska Mileage Plan", 0.0, 0.9, 1.3, 1.3, 1.8, 1.8),
    "avios":       ("British Airways Avios", 0.0, 0.8, 1.2, 1.2, 1.6, 1.6),
}

SWEET_SPOTS = [
    ("Domestic short-haul via distance charts", "Avios / LifeMiles",
     "5,000-7,500 pts for 650-mile hops; cash often $150-250", "2-4c"),
    ("Partner business to Europe", "Star/oneworld partners",
     "55k-70k one-way vs $2,500-4,000 fares; watch YQ surcharges", "1.5-3c"),
    ("Round-trip Japan premium via ANA", "ANA (transfer from Amex)",
     "75k-90k business ROUND TRIP; surcharges near zero", "3-5c"),
    ("Off-peak economy on dated charts", "AA Oct-Apr to Europe",
     "22.5k each way historically vs $600-900 cash", "2-3c"),
    ("West Coast to Hawaii / C.America", "Alaska partner charts",
     "Per-partner pricing keeps floors stable", "1.5-2.5c"),
    ("Transfer bonuses 25-40%", "MR->Avianca/BA, Citi->various",
     "Multiplies CPP of an already-good plan; never rescues a bad one",
     "+25-40%"),
    ("Surcharge escape routing", "Book LH via Aeroplan not M&M",
     "Booking partner sets YQ, not the metal you fly", "saves $300-600"),
]


def load():
    if DATA.exists():
        return json.loads(DATA.read_text())
    return {"options": []}


def save(state):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(state, indent=2))


def band_label(cpp, cur):
    name, floor, fair_lo, fair_hi, good_lo, good_hi, exc_lo = CURRENCIES[cur]
    if cpp < fair_lo:
        return "WEAK"
    if cpp <= fair_hi:
        return "FAIR"
    if cpp <= good_hi:
        return "GOOD"
    return "EXCELLENT"


def verdict(cpp, cur, expiring_days):
    name, floor, fair_lo, fair_hi, good_lo, good_hi, exc_lo = CURRENCIES[cur]
    # never redeem transferable points below the program's cash-out floor
    if floor > 0 and cpp < floor:
        if expiring_days is not None and expiring_days <= 90 and cpp >= 0.5:
            return "BURN (expiring - below floor but value beats $0)"
        return "NEVER (below cash-out floor - take the cash rate instead)"
    if cpp >= good_lo:
        return "BURN"
    if cpp >= fair_lo:
        if expiring_days is not None and expiring_days <= 90:
            return "BURN (expiring soon - fair value beats zero)"
        return "HOARD (fair, not urgent - better uses exist)"
    if expiring_days is not None and expiring_days <= 90:
        return "BURN (expiring - weak value beats expiration)"
    return "NEVER (weak - points are worth more held or cashed out)"


def fmt_money(x):
    return f"${x:,.0f}" if x >= 100 else f"${x:,.2f}"


def cmd_evaluate(a):
    if a.points <= 0:
        sys.exit("--points must be > 0")
    if a.realistic_fare <= 0:
        sys.exit("--realistic-fare must be > 0")
    if a.currency not in CURRENCIES:
        sys.exit(f"unknown currency {a.currency!r}; choices: "
                 + ", ".join(CURRENCIES))
    copay = a.copay or 0.0
    net_real = a.realistic_fare - copay
    net_ceil = max(a.ceiling_fare or a.realistic_fare, a.realistic_fare) - copay
    cpp_real = net_real / a.points * 100
    cpp_ceil = net_ceil / a.points * 100
    cur_name = CURRENCIES[a.currency][0]
    band = band_label(cpp_real, a.currency)
    v = verdict(cpp_real, a.currency, a.expiring_days)

    st = load()
    st["options"].append({
        "label": a.label, "currency": a.currency,
        "points": a.points, "copay": copay,
        "realistic_fare": a.realistic_fare,
        "ceiling_fare": a.ceiling_fare or a.realistic_fare,
        "cpp_realistic": round(cpp_real, 2),
        "cpp_ceiling": round(cpp_ceil, 2),
        "band": band, "verdict": v, "ts": int(time.time()),
    })
    save(st)

    print(f"\n=== {a.label} ({cur_name}) ===")
    print(f"  points: {a.points:,}   copay: {fmt_money(copay)}")
    print(f"  realistic: {fmt_money(a.realistic_fare)} -> "
          f"{cpp_real:.2f} c/pt  [{band}]")
    if a.ceiling_fare and a.ceiling_fare != a.realistic_fare:
        print(f"  ceiling:   {fmt_money(a.ceiling_fare)} -> "
              f"{cpp_ceil:.2f} c/pt  (vanity metric)")
    print(f"  VERDICT: {v}\n")
    return v


def cmd_compare(_a=None):
    st = load()
    opts = st.get("options", [])
    if not opts:
        sys.exit("no options saved - run evaluate first")
    print(f"\n{'OPTION':<34}{'CUR':<10}{'PTS':>9}{'CPP':>7}  "
          f"{'BAND':<10}VERDICT")
    print("-" * 100)
    ranked = sorted(opts, key=lambda o: o["cpp_realistic"], reverse=True)
    for o in ranked:
        print(f"{o['label'][:33]:<34}{o['currency']:<10}"
              f"{o['points']:>9,}{o['cpp_realistic']:>6.2f}c  "
              f"{o['band']:<10}{o['verdict']}")
    print()
    burn = [o for o in ranked if o["verdict"].startswith("BURN")]
    if burn:
        print(f"BEST BURN NOW: {burn[0]['label']} at "
              f"{burn[0]['cpp_realistic']:.2f}c/pt")
    else:
        print("No BURN-worthy option yet - hold transferable points, "
              "check sweet-spots for better plans.")


def cmd_sweet(_a=None):
    print("\nKNOWN SWEET SPOTS (verify charts before booking)\n")
    print(f"{'PATTERN':<38}{'PROGRAM':<28}{'WHY':<44}{'CPP'}")
    print("-" * 118)
    for name, prog, why, cpp in SWEET_SPOTS:
        print(f"{name[:37]:<38}{prog[:27]:<28}{why[:43]:<44}{cpp}")
    print()


def cmd_clear(_a=None):
    save({"options": []})
    print("cleared saved options")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.
                                 RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("evaluate", help="score one redemption option")
    e.add_argument("--label", required=True)
    e.add_argument("--points", type=float, required=True)
    e.add_argument("--realistic-fare", type=float, required=True,
                   help="cash fare you'd actually pay, same cabin")
    e.add_argument("--ceiling-fare", type=float, default=None,
                   help="retail premium-cabin fare (optional)")
    e.add_argument("--copay", type=float, default=None,
                   help="taxes/fees paid in cash on the award")
    e.add_argument("--currency", default="chase", choices=sorted(CURRENCIES))
    e.add_argument("--expiring-days", type=int, default=None,
                   help="points expire in N days (shifts verdicts)")
    e.set_defaults(func=cmd_evaluate)

    c = sub.add_parser("compare", help="ranked table of saved options")
    c.set_defaults(func=cmd_compare)

    s = sub.add_parser("sweet-spots", help="list known good redemptions")
    s.set_defaults(func=cmd_sweet)

    x = sub.add_parser("clear", help="wipe saved options")
    x.set_defaults(func=cmd_clear)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
