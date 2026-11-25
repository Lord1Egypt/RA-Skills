#!/usr/bin/env python3
"""Chest Freezer Inventory — FIFO discipline for the frozen black hole.

Chest freezers stratify: new food goes in the top, old food sinks, and
in two years nobody remembers what's under the venison. This tool keeps
a layer-aware inventory (top/middle/bottom), ages every item against
USDA-quality shelf-life clocks, and answers the two questions that
matter: "what should we eat first?" and "what do I have to dig past?"

Commands (store = freezer_inventory.json next to you):
  add   --item "chili" --class cooked-dishes --qty 3 --date 2026-09-14 \
        --layer top --value 12
  list [--layer top] [--old-first]
  dig   [--class cooked-dishes] [--count 2]     -> tonight's retrieval list
  plan  --days 7                                  -> FIFO week menu + dig map
  use   --id 3 [--qty 2]                          -> mark consumed
  stats                                          -> value at risk, burn report

stdlib only. Quality clocks per USDA Freezing and Food Safety guidance
(frozen food stays SAFE indefinitely; the clock is quality, not safety).
"""
import argparse
import json
import sys
from datetime import date

SHELF_LIFE_DAYS = {   # USDA quality windows, days
    "ground-meat": 120, "chops": 180, "roasts": 300, "steaks": 240,
    "whole-poultry": 365, "poultry-parts": 270, "bacon": 30,
    "sausage": 60, "cooked-dishes": 90, "soups-broth": 90,
    "casseroles": 90, "bread": 90, "baked-goods": 60, "fruit": 300,
    "vegetables": 300, "fish-lean": 180, "fish-fatty": 90,
    "shellfish": 120, "butter": 270, "cheese": 180, "milk-frozen": 90,
    "ice-cream": 60, "nuts-flour": 180, "herbs": 180, "coffee": 90,
    "other": 180,
}
LAYERS = ["top", "middle", "bottom"]


def default_store():
    return "freezer_inventory.json"


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return data
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        raise SystemExit(f"error: {path} is corrupted — fix or delete it")
    return {"items": [], "next_id": 1}


def save(path, db):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(db, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def parse_date(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise SystemExit(f"error: bad date '{s}' — use YYYY-MM-DD")


def today_s(args_today):
    return parse_date(args_today) if args_today else date.today()


def age_days(item, ref):
    return (ref - parse_date(item["date"])).days


def verdict(item, ref):
    life = SHELF_LIFE_DAYS.get(item["class"], SHELF_LIFE_DAYS["other"])
    age = age_days(item, ref)
    pct = age / life if life else 1
    days_left = life - age
    if age < 0:
        return "FUTURE-DATE?", 0
    if pct > 1.0:
        return f"BURN RISK ({abs(days_left)}d past quality window)", 4
    if pct > 0.75:
        return f"USE-FIRST ({days_left}d left)", 3
    if pct > 0.50:
        return f"FADING ({days_left}d left)", 2
    return f"PRIME ({days_left}d left)", 1


def money(x):
    return f"${x:,.0f}" if x is not None else "—"


def hr(t):
    print("\n" + "=" * 60)
    print(t)
    print("=" * 60)


def norm_class(s):
    c = s.strip().lower()
    if c in SHELF_LIFE_DAYS:
        return c
    close = [k for k in SHELF_LIFE_DAYS if c and (c in k or k in c)]
    if len(close) == 1:
        return close[0]
    print(f"note: class '{s}' not in catalog -> using 'other' (180d).")
    print(f"      classes: {', '.join(sorted(SHELF_LIFE_DAYS))}")
    return "other"


# ---------------- commands ----------------

def cmd_add(a):
    db = load(a.store)
    layer = a.layer if a.layer in LAYERS else "top"
    db["items"].append({
        "id": db["next_id"], "item": a.item,
        "class": norm_class(a.class_), "qty": a.qty,
        "date": a.date, "layer": layer, "value": a.value,
    })
    db["next_id"] += 1
    save(a.store, db)
    ref = today_s(a.today)
    v, _ = verdict(db["items"][-1], ref)
    print(f"added #{db['next_id'] - 1}: {a.qty} × {a.item} "
          f"[{db['items'][-1]['class']}] {a.date} → {layer} layer")
    print(f"  clock: {v}")


def cmd_list(a):
    db = load(a.store)
    ref = today_s(a.today)
    items = [i for i in db["items"] if i["qty"] > 0]
    if a.layer:
        items = [i for i in items if i["layer"] == a.layer]
    rows = [(i, verdict(i, ref)) for i in items]
    rows.sort(key=lambda r: ({"top": 0, "middle": 1, "bottom": 2}[r[0]["layer"]],
                             -age_days(r[0], ref)))
    hr("FREEZER — DEPTH MAP")
    for layer in LAYERS:
        got = [i for i in items if i["layer"] == layer]
        names = [f"{i['item']}×{i['qty']}" for i in got] or ["(empty)"]
        print(f"{layer.upper():7s} " + " | ".join(names))
    hr("ITEMS (oldest-first within layer)")
    for i, (v, _) in rows:
        print(f"#{i['id']:<3d} {i['date']}  {i['qty']:>2d} × {i['item']:<24.24s}"
              f" [{i['class']:<14.14s}] {v}")
    if not rows:
        print("(freezer empty — add with 'add')")


def cmd_dig(a):
    db = load(a.store)
    ref = today_s(a.today)
    items = [i for i in db["items"] if i["qty"] > 0]
    if a.class_:
        cls = norm_class(a.class_)
        items = [i for i in items if i["class"] == cls]
    items.sort(key=lambda i: parse_date(i["date"]))   # strict FIFO: oldest first
    picks = items[:a.count]
    hr(f"DIG LIST — retrieve {len(picks)} (FIFO, oldest first)")
    for i in picks:
        v, _ = verdict(i, ref)
        above = [x["item"] for x in db["items"]
                 if x["qty"] > 0 and LAYERS.index(x["layer"])
                 < LAYERS.index(i["layer"])]
        print(f"#{i['id']:<3d} {i['qty']} × {i['item']} — {i['layer']} layer, "
              f"frozen {i['date']}")
        print(f"     {v}")
        if above:
            print(f"     dig past: {', '.join(sorted(set(above)))}")
        else:
            print("     nothing on top of it — easy grab")
    if picks:
        print("\nWhile you're in there: pull anything tagged USE-FIRST/")
        print("BURN RISK within reach. Mark consumed with 'use --id N'.")
    else:
        print("(nothing matched)")


def cmd_plan(a):
    db = load(a.store)
    ref = today_s(a.today)
    items = [i for i in db["items"] if i["qty"] > 0]
    if not items:
        raise SystemExit("freezer empty — nothing to plan")
    # FIFO week: oldest-first, max 2 picks per class for variety
    per_class = {}
    ranked = sorted(items, key=lambda i: parse_date(i["date"]))
    menu = []
    for i in ranked:
        c = i["class"]
        if per_class.get(c, 0) >= 2:
            continue
        per_class[c] = per_class.get(c, 0) + min(i["qty"], 2)
        menu.append(i)
        if sum(1 for m in menu if m) >= a.days:
            break
    menu = [m for m in menu if m][:a.days]
    hr(f"FIFO WEEK PLAN — {len(menu)} dinners from the bottom of time")
    for n, i in enumerate(menu, 1):
        d = ref.fromordinal(ref.toordinal() + n - 1)
        v, _ = verdict(i, ref)
        print(f"{d.isoformat()}  {i['qty']} × {i['item']:24.24s} {v}")
    moved = [i["item"] for i in menu if i["layer"] != "top"]
    if moved:
        print("\nMove to the fridge the night before; these need a thaw:")
        print("  " + ", ".join(sorted(set(moved))))
    value = sum((i["value"] or 0) * min(i["qty"], 2) for i in menu)
    print(f"\nWeek's frozen stock consumed ≈ {money(value)} you didn't")


def cmd_use(a):
    db = load(a.store)
    hit = next((i for i in db["items"] if i["id"] == a.id), None)
    if not hit:
        raise SystemExit(f"no item #{a.id} — run 'list'")
    take = min(a.qty or hit["qty"], hit["qty"])
    hit["qty"] -= take
    save(a.store, db)
    left = hit["qty"]
    print(f"used {take} × {hit['item']} (#{a.id}); "
          + (f"{left} left" if left else "entry finished"))


def cmd_stats(a):
    db = load(a.store)
    ref = today_s(a.today)
    items = [i for i in db["items"] if i["qty"] > 0]
    if not items:
        raise SystemExit("freezer empty")
    total_qty = sum(i["qty"] for i in items)
    total_val = sum((i["value"] or 0) * i["qty"] for i in items)
    risk_val = sum((i["value"] or 0) * i["qty"] for i in items
                   if verdict(i, ref)[1] >= 3)
    over = [i for i in items if verdict(i, ref)[1] == 4]
    from collections import Counter
    classes = Counter()
    for i in items:
        classes[i["class"]] += i["qty"]
    hr("FREEZER STATS")
    print(f"Entries active ........ {len(items)}  ({total_qty} units)")
    print(f"Estimated value ....... {money(total_val)}")
    print(f"Value in USE-FIRST/BURN {money(risk_val)} "
          f"({(risk_val / total_val * 100) if total_val else 0:.0f}% of stock)")
    hr("STOCK BY CLASS")
    for c, n in classes.most_common():
        life = SHELF_LIFE_DAYS.get(c, 180)
        print(f"  {c:<15.15s} {n:>2d} units   (quality window {life}d)")
    if over:
        hr("BURN REPORT (past quality window)")
        for i in over:
            v, _ = verdict(i, ref)
            print(f"  #{i['id']} {i['qty']} × {i['item']}: {v}")
        print("\nQuality, not safety: still SAFE if it stayed frozen —")
        print("expect flat flavors, dry textures. Use in spiced/braised")
        print("dishes, or discard if freezer-burned through packaging.")
    oldest = min(items, key=lambda i: parse_date(i["date"]))
    print(f"\nOldest resident: {oldest['qty']} × {oldest['item']} "
          f"(frozen {oldest['date']}, {oldest['layer']} layer)")
    if len(items) >= 10 and len(over) / len(items) > 0.3:
        print("DEFROST DAY: >30% of entries are past their quality window.")
        print("  Schedule the annual defrost + re-inventory (eat down,")
        print("  empty, dry, seal-check, restart the clock).")


def main():
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    p.add_argument("--store", default=default_store())
    p.add_argument("--today", default=None, help="override today YYYY-MM-DD")

    sp = sub.add_parser("add")
    sp.add_argument("--item", required=True)
    sp.add_argument("--class", dest="class_", required=True)
    sp.add_argument("--qty", type=int, default=1)
    sp.add_argument("--date", required=True, help="freeze date YYYY-MM-DD")
    sp.add_argument("--layer", choices=LAYERS, default="top")
    sp.add_argument("--value", type=float, default=None,
                    help="replacement $ per unit")
    sp.set_defaults(fn=cmd_add)

    sp = sub.add_parser("list")
    sp.add_argument("--layer", choices=LAYERS)
    sp.set_defaults(fn=cmd_list)

    sp = sub.add_parser("dig")
    sp.add_argument("--class", dest="class_")
    sp.add_argument("--count", type=int, default=3)
    sp.set_defaults(fn=cmd_dig)

    sp = sub.add_parser("plan")
    sp.add_argument("--days", type=int, default=7)
    sp.set_defaults(fn=cmd_plan)

    sp = sub.add_parser("use")
    sp.add_argument("--id", type=int, required=True)
    sp.add_argument("--qty", type=int, default=None)
    sp.set_defaults(fn=cmd_use)

    sp = sub.add_parser("stats")
    sp.set_defaults(fn=cmd_stats)

    a = p.parse_args()
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
