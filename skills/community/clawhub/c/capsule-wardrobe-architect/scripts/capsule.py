#!/usr/bin/env python3
"""Capsule Wardrobe Architect — wardrobe math: cost-per-wear, outfit
combinatorics with compatibility, laundry-cycle sufficiency, lifestyle
allocation gaps. Stdlib only."""
import argparse
import sys

# ─── 1. Cost-per-wear ───
def cmd_cpw(a):
    realized = a.price / a.worn if a.worn else float("inf")
    projected = a.price / a.lifetime if a.lifetime else float("inf")
    print(f"COST-PER-WEAR — ${a.price:.2f} item, worn {a.worn}x so far, "
          f"{a.lifetime} expected lifetime wears")
    print(f"  realized CPW (so far):   ${realized:.2f}/wear")
    print(f"  projected CPW (lifetime): ${projected:.2f}/wear")
    if a.worn >= 3 and realized > 3 * projected:
        print("  NOTE: wearing pace suggests lifetime estimate is optimistic;")
        print("        the realized number is trending worse than projected.")
    if projected <= 1.0:
        v = "EXCELLENT — workhorse territory"
    elif projected <= 3.0:
        v = "GOOD — fair price for a frequently-worn item"
    elif projected <= 8.0:
        v = "MARGINAL — fine only if you love it and will keep it"
    else:
        v = "EXPENSIVE PER WEAR — rental/borrow candidate, not a buy"
    print(f"  verdict: {v}")
    # break-even wears to hit target CPW
    for tgt in (1.0, 3.0):
        need = a.price / tgt
        print(f"  to reach ${tgt:.0f}/wear you must wear it {need:.0f} times")


# ─── 2. Outfit combinatorics ───
def cmd_outfits(a):
    base = a.tops * a.bottoms
    real = base * a.compatible
    layer_looks = int(real * a.layers * 0.7) if a.layers else 0
    print(f"OUTFIT MATH — {a.tops} tops x {a.bottoms} bottoms x {a.layers} layers")
    print(f"  base pairs:               {base}")
    print(f"  compatible ({a.compatible:.0%}):        ~{real:.0f} real base outfits")
    if a.layers:
        print(f"  + layers (70% coverage):  +{layer_looks} looks")
    print(f"  distinct daily outfits:    ~{real:.0f} (layers restyle looks,")
    print(f"                              they don't create new base outfits)")
    if real < 14:
        print("VERDICT: WARDROBE POVERTY — weekly repetition is structural.")
        print("  Fix compatibility FIRST (replace oddball singles with")
        print("  neutrals that pair with most bottoms) — adding more")
        print("  non-pairing items makes it worse.")
    elif real <= 40:
        print("VERDICT: FUNCTIONAL CORE — 20-40 distinct outfits covers a")
        print("  month without visible repetition. Volume is not the problem.")
    else:
        print("VERDICT: DIMINISHING RETURNS — >40 outfits; new items add")
        print("  clutter, not looks. Only replace, never add.")
    print(f"  target compatibility: >=0.7 — each point of compatibility is")
    print(f"  worth more than an extra item:")
    better = a.tops * a.bottoms * 0.8
    print(f"    at 0.80 compat: ~{better:.0f} outfits from the SAME items")


# ─── 3. Laundry-cycle sufficiency ───
def cmd_laundry(a):
    wears_needed = a.items * a.wears_per_item
    # a role survives if total wears available >= wears in cycle + spare
    need_wears = a.cycle_days  # 1 wear/day assumption for role-specific wear
    have = wears_needed
    print(f"LAUNDRY CYCLE — role '{a.role}': {a.items} items, "
          f"{a.wears_per_item} wear(s) each, {a.cycle_days}-day cycle")
    print(f"  wears available:  {have}  (before the wash is done)")
    print(f"  wears needed:     {need_wears} + 1 in the wash + 1 spill buffer")
    required = need_wears + 2
    print(f"  items required:   {required / a.wears_per_item:.0f} "
          f"(at {a.wears_per_item} wear/item)")
    if have >= required:
        spare = have - required
        print(f"  OK — {spare} spare wear(s). You are never 'behind on laundry'")
        print(f"  because of this role.")
    else:
        short = required - have
        print(f"  SHORT by {short} wear(s) — this is why you feel behind.")
        print(f"  BUY {max(1, -(-short // a.wears_per_item))} more "
              f"'{a.role}' item(s) — or wash more often. This is a")
        print(f"  queueing problem; no styling fix exists.")


# ─── 4. Lifestyle-allocation gaps ───
def cmd_gaps(a):
    alloc = {"work": a.work, "casual": a.casual, "active": a.active,
             "dressup": a.dressup, "home": a.home}
    items = {"work": a.work_items, "casual": a.casual_items,
             "active": a.active_items, "dressup": a.dressup_items,
             "home": a.home_items}
    total_items = sum(items.values())
    if total_items == 0:
        sys.exit("no items recorded")
    if abs(sum(alloc.values()) - 1.0) > 0.02:
        print(f"  (lifestyle shares normalized to 100%)")
        s = sum(alloc.values())
        alloc = {k: v / s for k, v in alloc.items()}
    print(f"LIFESTYLE vs CLOSET ({total_items} daily-rotation items)")
    rows = []
    for role in ("work", "casual", "active", "dressup", "home"):
        share = alloc[role]
        owned = items[role] / total_items
        gap = share - owned
        rows.append((role, share, owned, gap))
    deficit_rows, surplus_rows = [], []
    for role, share, owned, gap in sorted(rows, key=lambda r: r[3]):
        pct = lambda v: f"{v * 100:5.1f}%"
        line = (f"  {role:<8} {pct(share)} of life  "
                f"{items[role]:>3}/{total_items} items ({pct(owned)})  "
                f"-> {'DEFICIT ' if gap > 0.03 else 'SURPLUS ' if gap < -0.03 else 'about right':<14}"
                f"{gap * 100:+.0f} pts")
        print(line)
        if gap > 0.03:
            deficit_rows.append((role, gap, items[role]))
        elif gap < -0.03:
            surplus_rows.append((role, gap, items[role]))
    print()
    if not deficit_rows:
        print("ALLOCATION OK — no structural gap. Do not shop; improve")
        print("compatibility or laundry depth instead (see other commands).")
        return
    print("BUY LIST (max 3 roles):", end=" ")
    buys = []
    for role, gap, cur in sorted(deficit_rows, key=lambda r: -r[1])[:3]:
        n = max(1, round(gap * total_items))
        buys.append(f"{n} {role} item(s)")
    print("; ".join(buys) + ".")
    for role, gap, cur in sorted(deficit_rows, key=lambda r: -r[1])[:3]:
        print(f"  - {role}: choose NEUTRAL basics that pair with >=4 existing")
        print(f"    bottoms/tops — leverage = outfits added, not items added.")
    if surplus_rows:
        print("DONATE CANDIDATES:", end=" ")
        d = []
        for role, gap, cur in surplus_rows:
            n = max(1, round(-gap * total_items))
            d.append(f"{n}x {role}")
        print("; ".join(d) + " (duplicates past CPW threshold).")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("cpw", help="cost per wear")
    s.add_argument("--price", type=float, required=True)
    s.add_argument("--worn", type=int, default=0)
    s.add_argument("--lifetime", type=int, required=True)
    s.set_defaults(fn=cmd_cpw)

    s = sub.add_parser("outfits", help="real outfit count")
    s.add_argument("--tops", type=int, required=True)
    s.add_argument("--bottoms", type=int, required=True)
    s.add_argument("--layers", type=int, default=0)
    s.add_argument("--compatible", type=float, default=0.5,
                   help="fraction of top-bottom pairs that actually work (0-1)")
    s.set_defaults(fn=cmd_outfits)

    s = sub.add_parser("laundry", help="laundry cycle sufficiency")
    s.add_argument("--items", type=int, required=True)
    s.add_argument("--wears-per-item", type=int, default=1)
    s.add_argument("--cycle-days", type=int, required=True)
    s.add_argument("--role", default="work")
    s.set_defaults(fn=cmd_laundry)

    s = sub.add_parser("gaps", help="lifestyle allocation audit")
    for r in ("work", "casual", "active", "dressup", "home"):
        s.add_argument(f"--{r}", type=float, required=True,
                       help=f"share of waking hours in {r} wear (0-1)")
    for r in ("work", "casual", "active", "dressup", "home"):
        s.add_argument(f"--{r}-items", type=int, required=True)
    s.set_defaults(fn=cmd_gaps)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
