#!/usr/bin/env python3
"""diaper_stock_calculator.py - diaper stock-run calculator.

Modes:
  plan   - how many diapers of each size to buy for a date range
  usage  - days of stock left from a plan file + current count
  burn   - one-off burn-rate and box-lifespan estimate

Zero dependencies (Python 3.8+ stdlib). Plans are saved to ./data/.
"""
import argparse
import json
import math
import os
import sys
from datetime import date, datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# size, kg_min, kg_max, typical_days_in_size@p50, changes/day min, max
BANDS = [
    ("N", 0.0, 4.5, 21, 8, 12),
    ("1", 4.0, 6.5, 42, 7, 10),
    ("2", 6.0, 8.5, 56, 6, 9),
    ("3", 8.0, 11.5, 70, 5, 8),
    ("4", 10.0, 14.5, 140, 4, 7),
    ("5", 13.0, 18.5, 180, 4, 6),
    ("6", 16.0, 23.0, 210, 4, 6),
    ("7", 20.0, 30.0, 240, 3, 5),
]

PACK_COST_PER_DIAPER = {"economy": 0.24, "standard": 0.31, "premium": 0.45}


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def fmt_d(d):
    return d.strftime("%Y-%m-%d")


def size_index_for_age(age_days):
    """Map age (days) to size band by cumulative p50 days-in-size."""
    cum = 0
    for i, band in enumerate(BANDS):
        cum += band[3]
        if age_days < cum:
            return i
    return None


def changes_per_day(idx, frac):
    """Usage tapers inside a size: start at max, end near min."""
    cmin, cmax = BANDS[idx][4], BANDS[idx][5]
    return cmax - (cmax - cmin) * frac


def build_spans(start, end, birthday):
    """Walk day by day; return per-size day counts and avg changes/day."""
    spans = []  # dicts: size, days, cpd_sum
    day = start
    while day <= end:
        age = (day - birthday).days
        idx = size_index_for_age(age)
        if idx is None:
            break
        # fraction through this band
        cum = sum(b[3] for b in BANDS[:idx])
        frac = min(max((age - cum) / max(BANDS[idx][3], 1), 0.0), 1.0)
        cpd = changes_per_day(idx, frac)
        if spans and spans[-1]["size"] == BANDS[idx][0]:
            spans[-1]["days"] += 1
            spans[-1]["cpd_sum"] += cpd
        else:
            spans.append({"size": BANDS[idx][0], "days": 1, "cpd_sum": cpd})
        day += timedelta(days=1)
    return spans


def cmd_plan(args):
    start = parse_date(args.from_)
    end = parse_date(args.to)
    if end <= start:
        sys.exit("error: --to must be after --from")
    birthday = parse_date(args.birthday)
    if start < birthday:
        sys.exit("error: --from is before the birthday")

    spans = build_spans(start, end, birthday)
    if not spans:
        sys.exit("error: child is past size 7 - congratulations, no diapers needed")

    total_days = sum(s["days"] for s in spans)
    print("Diaper stock-up plan  %s -> %s" % (fmt_d(start), fmt_d(end)))
    print("Birthday: %s   Coverage: %d days" % (args.birthday, total_days))
    print()
    hdr = "{:<6}{:>6}{:>12}{:>8}{:>8}".format("size", "days", "chg/day", "need", "buy")
    print(hdr)
    print("-" * len(hdr))
    grand = 0
    plan = {"from": fmt_d(start), "to": fmt_d(end), "birthday": args.birthday,
            "generated": fmt_d(date.today()), "sizes": []}
    for s in spans:
        avg_cpd = s["cpd_sum"] / s["days"]
        need = int(math.ceil(s["days"] * avg_cpd))
        buy = int(math.ceil(need / 20.0) * 20)
        grand += buy
        print("{:<6}{:>6}{:>12.1f}{:>8}{:>8}".format(s["size"], s["days"], avg_cpd, need, buy))
        plan["sizes"].append({"size": s["size"], "days": s["days"],
                              "avg_changes_per_day": round(avg_cpd, 2),
                              "need": need, "buy": buy})
    print("-" * len(hdr))
    print("{:<6}{:>6}{:>12}{:>8}{:>8}".format("TOTAL", total_days, "", "", grand))
    plan["total_buy"] = grand
    plan["total_days"] = total_days

    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, "plan_%s.json" % fmt_d(start))
    with open(path, "w") as f:
        json.dump(plan, f, indent=2)
    print("\nSaved: %s" % path)
    return 0


def cmd_usage(args):
    if not os.path.exists(args.file):
        sys.exit("error: no plan file at %s - run `plan` first" % args.file)
    with open(args.file) as f:
        log = json.load(f)
    if "sizes" not in log:
        sys.exit("error: not a plan file (missing 'sizes')")
    sizes = log["sizes"]
    total_qty = sum(s["need"] for s in sizes)
    total_days = sum(s["days"] for s in sizes)
    if total_days == 0:
        sys.exit("error: zero-day plan")
    avg_cpd = total_qty / float(total_days)
    print("Plan file: %s" % args.file)
    print("Planned usage: %d diapers over %d days = %.1f/day"
          % (total_qty, total_days, avg_cpd))
    if args.stock is None:
        return 0
    if avg_cpd <= 0:
        sys.exit("error: bad plan (zero usage)")
    dl = args.stock / avg_cpd
    run_out = date.today() + timedelta(days=int(dl))
    print("Current stock: %d diapers" % args.stock)
    print("Days of stock left: %.1f  (at planned usage)" % dl)
    print("Projected run-out: %s" % fmt_d(run_out))
    if dl < 7:
        print("VERDICT: ORDER NOW - under one week of stock")
    elif dl < 14:
        print("VERDICT: Order within a few days")
    else:
        print("VERDICT: Stocked - next order in ~%d days" % int(dl - 14))
    return 0


def cmd_burn(args):
    keys = [b[0] for b in BANDS]
    if args.size.upper() not in keys:
        sys.exit("error: unknown size %r (use N,1..7)" % args.size)
    b = BANDS[keys.index(args.size.upper())]
    lo, hi, cmin, cmax = b[1], b[2], b[4], b[5]
    unit = "kg"
    if args.lbs:
        lo, hi = lo * 2.20462, hi * 2.20462
        unit = "lbs"
    cpd = (cmin + cmax) / 2.0
    print("Size %s: weight band %.1f-%.1f %s" % (b[0], lo, hi, unit))
    print("Typical usage: %d-%d changes/day (avg %.1f)" % (cmin, cmax, cpd))
    tier = PACK_COST_PER_DIAPER.get(args.tier, 0.31)
    print("Cost tier %s: ~$%.2f/diaper" % (args.tier, tier))
    for pack in (30, 60, 120, 240):
        days = pack / cpd
        print("  %3d-count box -> ~%2.0f days  (~$%.0f)" % (pack, days, pack * tier))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)

    sp = sub.add_parser("plan", help="diapers to buy for a date range")
    sp.add_argument("--from", dest="from_", required=True, help="YYYY-MM-DD")
    sp.add_argument("--to", dest="to", required=True, help="YYYY-MM-DD")
    sp.add_argument("--birthday", required=True, help="YYYY-MM-DD")
    sp.set_defaults(func=cmd_plan)

    sp = sub.add_parser("usage", help="days of stock left")
    sp.add_argument("--file", default=os.path.join(DATA_DIR, "plan_default.json"),
                    help="plan JSON from `plan`")
    sp.add_argument("--stock", type=int, default=None,
                    help="diapers currently on hand")
    sp.set_defaults(func=cmd_usage)

    sp = sub.add_parser("burn", help="burn-rate for one size")
    sp.add_argument("--size", required=True, help="N,1,2,...,7")
    sp.add_argument("--lbs", action="store_true", help="show pounds")
    sp.add_argument("--tier", default="standard",
                    choices=sorted(PACK_COST_PER_DIAPER), help="price tier")
    sp.set_defaults(func=cmd_burn)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
