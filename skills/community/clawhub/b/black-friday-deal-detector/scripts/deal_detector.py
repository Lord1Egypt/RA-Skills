#!/usr/bin/env python3
"""Black Friday Deal Detector — real discount vs price theater.

Scores a claimed deal ("was $MSRP, now $SALE") against today's street price
and the 12-month low, detects anchor-inflation theater, adjusts for
gift-card-back and membership gates, and issues WAIT / OK DEAL / GREAT /
PRICE THEATER verdicts. Optionally compares two competing claims.

stdlib only. No network.
"""
import argparse
import json
import sys

# Real annual-low behavior by category (typical BF delta vs street price)
CATEGORY_FLOORS = {
    "tv": {"note": "derivative-SKU risk high; check panel specs", "real_floor_pct": 0.30},
    "apple": {"note": "cash discounts rare; gift-card-back is the norm", "real_floor_pct": 0.10},
    "laptop": {"note": "verify CPU generation on 'exclusive' SKUs", "real_floor_pct": 0.25},
    "mattress": {"note": "list price is fiction; compare coupon floors", "real_floor_pct": 0.50},
    "power-tools": {"note": "two real windows/yr: June + BF", "real_floor_pct": 0.30},
    "appliances-small": {"note": "BF is usually the true annual low", "real_floor_pct": 0.40},
    "ssd": {"note": "cyclical; check controller tier", "real_floor_pct": 0.30},
    "toys": {"note": "big items often cheaper early Dec", "real_floor_pct": 0.35},
    "games": {"note": "catalog titles discount hard digitally", "real_floor_pct": 0.50},
    "apparel": {"note": "compare vs outlet price", "real_floor_pct": 0.35},
}


def analyze(msrp, sale, street, low, gift_card_back=0.0, membership_cost=0.0,
            category=None, label="item"):
    # --- sanity ---
    if min(msrp, sale, street, low) <= 0:
        return {"error": "all prices must be > 0"}
    if sale > street * 1.5:
        pass  # not impossible (clearance elsewhere), let it through flagged

    anchor_discount = (msrp - sale) / msrp            # the theater number
    real_discount = (street - sale) / street          # vs today's street
    low_gap = (sale - low) / low                      # vs 12-month low

    # effective price after honest gift-card valuation (50%) and membership
    eff_price = sale - 0.5 * gift_card_back
    if membership_cost:
        eff_price += membership_cost * 0.3  # amortized: you'll likely use it for more than this one deal; conservative 30%
    eff_real_discount = (street - eff_price) / street
    theater_gap = anchor_discount - real_discount

    flags = []
    if theater_gap > 0.15:
        flags.append(f"PRICE THEATER: claimed {anchor_discount:.0%} off but only {real_discount:.0%} off today's street price")
    if street > msrp * 0.98:
        flags.append("street price ≈ claimed MSRP — anchor looks honest")
    if low_gap > 0.15:
        flags.append(f"sale is {low_gap:.0%} ABOVE the 12-month low ({low:.2f}) — better windows exist")
    if gift_card_back > 0:
        flags.append(f"gift card valued at 50%: effective price {eff_price:.2f} (not {sale:.2f})")
    if membership_cost > 0:
        flags.append(f"membership amortized at 30% adds {membership_cost*0.3:.2f} to effective price")

    # --- verdict logic (price-beats-history wins over anchor theater) ---
    if eff_price <= low * 0.98:
        verdict = "GREAT"
        strategy = "Buy now — effective price beats the 12-month low."
    elif theater_gap > 0.15 and eff_real_discount < 0.10:
        verdict = "PRICE THEATER"
        strategy = "Don't buy. Note the street price; the 'discount' is anchor inflation."
    elif abs(eff_price - low) / low <= 0.05:
        verdict = "OK DEAL"
        strategy = "Within 5% of the annual low — buy if you need it."
    elif low_gap > 0.05:
        verdict = "WAIT"
        strategy = f"Set an alert at {low*1.02:.0f} — history says this dips further."
    else:
        verdict = "OK DEAL"
        strategy = "Reasonable; not the annual floor."

    cat_note = None
    if category:
        c = CATEGORY_FLOORS.get(category)
        if c:
            cat_note = f"{category}: a real BF floor is ~{c['real_floor_pct']:.0%} below street — {c['note']}"
            if eff_real_discount >= c["real_floor_pct"]:
                cat_note += " | this deal MEETS the category floor test"
            else:
                cat_note += " | this deal is MILDER than the typical category floor"

    return {
        "label": label,
        "msrp": msrp, "sale": sale, "street": street, "low": low,
        "anchor_discount_pct": round(anchor_discount * 100, 1),
        "real_discount_pct": round(real_discount * 100, 1),
        "effective_price": round(eff_price, 2),
        "effective_real_discount_pct": round(eff_real_discount * 100, 1),
        "low_gap_pct": round(low_gap * 100, 1),
        "theater_gap_pct": round(theater_gap * 100, 1),
        "verdict": verdict,
        "strategy": strategy,
        "flags": flags,
        "category_note": cat_note,
    }


def parse_claim(spec):
    """'TV-A:1299:799:749:699' -> label, msrp, sale, street, low"""
    parts = spec.split(":")
    if len(parts) != 5:
        sys.exit(f"--compare spec must be label:msrp:sale:street:low — got '{spec}'")
    return parts[0], float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])


def render(r, brief=False):
    if "error" in r:
        print(f"ERROR: {r['error']}")
        return
    print(f"\n=== {r['label']} ===")
    print(f"  claimed: {r['msrp']:.2f} -> {r['sale']:.2f}   ({r['anchor_discount_pct']:.0f}% 'off')")
    print(f"  vs street today {r['street']:.2f}: real discount {r['real_discount_pct']:.0f}%")
    print(f"  vs 12-month low {r['low']:.2f}: gap {r['low_gap_pct']:+.0f}%")
    if abs(r['effective_price'] - r['sale']) > 0.01:
        print(f"  effective price (gift card 50%, membership 30% amortized): {r['effective_price']:.2f}")
    print(f"  theater gap (anchor - real): {r['theater_gap_pct']:.0f} pts")
    print(f"  VERDICT: {r['verdict']}")
    print(f"  strategy: {r['strategy']}")
    for f in r["flags"]:
        print(f"  ! {f}")
    if r.get("category_note"):
        print(f"  cat: {r['category_note']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--msrp", type=float, help="claimed list/was price")
    ap.add_argument("--sale", type=float, help="advertised sale price")
    ap.add_argument("--street", type=float, help="today's price at major retailers")
    ap.add_argument("--low", type=float, help="12-month tracked low")
    ap.add_argument("--gift-card-back", type=float, default=0.0)
    ap.add_argument("--membership-cost", type=float, default=0.0)
    ap.add_argument("--category", choices=list(CATEGORY_FLOORS))
    ap.add_argument("--label", default="item")
    ap.add_argument("--compare", nargs=2, metavar="SPEC",
                    help="two claims: label:msrp:sale:street:low")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.compare:
        results = []
        for spec in args.compare:
            lbl, m, s, t, l = parse_claim(spec)
            results.append(analyze(m, s, t, l, label=lbl))
        if args.json:
            print(json.dumps(results, indent=2))
            return 0
        for r in results:
            render(r)
        best = min(results, key=lambda r: r.get("effective_price", 1e18))
        print(f"\n>>> LOWER EFFECTIVE PRICE: {best['label']} @ {best['effective_price']:.2f} ({best['verdict']})")
        return 0

    if None in (args.msrp, args.sale, args.street, args.low):
        ap.error("--msrp --sale --street --low required (or --compare)")

    r = analyze(args.msrp, args.sale, args.street, args.low,
                args.gift_card_back, args.membership_cost,
                args.category, args.label)
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        render(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
