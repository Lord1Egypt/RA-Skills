#!/usr/bin/env python3
"""Declutter Pilot — physics-based decluttering planner.

Volume-first decluttering: greedy sorties ranked by volume per decision-
difficulty, container math, decision rules with cost-of-keeping, and
disposition manifests. Local state in declutter.json (or --db).
"""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

DB = Path("declutter.json")

BAG_L = 60          # liters per full trash bag
BOX_L = 60          # liters per standard moving box
CAR_L = 800         # liters per hatchback/station-wagon load
SPACE_COST_PER_M3_YEAR = 180  # $/m³/yr storage value (rent-based estimate)
SORTIE_MIN = 20     # minutes per sortie
LITERS_PER_MIN_EASY = 25      # easy decision throughput


def load(db=None):
    p = Path(db) if db else DB
    if p.exists():
        try:
            data = json.loads(p.read_text())
            data.setdefault("items", [])
            data.setdefault("log", [])
            return data
        except Exception:
            pass
    return {"items": [], "log": []}


def save(data, db=None):
    p = Path(db) if db else DB
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def now_iso():
    return dt.datetime.now().isoformat(timespec="minutes")


# ---------------------------------------------------------------- items
def cmd_item(a):
    data = load(a.db)
    if a.action == "list":
        items = [i for i in data["items"] if not i.get("done")]
        if not items:
            print("No active items. Add: declutter.py item add \"Old monitor\" --room office --volume 30 --difficulty 2")
            return 0
        print(f"{'item':32}{'room':10}{'L':>5}{'diff':>5}  decision")
        for i in sorted(items, key=lambda x: -x["volume"]):
            print(f"{i['name'][:31]:32}{i['room'][:9]:10}{i['volume']:>5}{i['difficulty']:>5}  {i.get('decision', '?')}")
        tot = sum(i["volume"] for i in items)
        print(f"\n{len(items)} items, {tot} L ({tot/1000:.1f} m³) waiting")
        return 0
    # add
    if not a.name or a.volume is None:
        print("[!] need item name and --volume (liters)")
        return 1
    if a.difficulty is None or not (1 <= a.difficulty <= 5):
        print("[!] --difficulty 1 (easy toss) … 5 (heirloom) required")
        return 1
    data["items"].append({
        "name": a.name, "room": a.room or "?", "volume": a.volume,
        "difficulty": a.difficulty, "decision": a.decision or "undecided",
        "value": a.value or 0, "added": now_iso(), "done": False,
    })
    save(data, a.db)
    print(f"added: {a.name} ({a.volume} L, diff {a.difficulty}, {a.decision or 'undecided'})")
    return 0


def cmd_rm(a):
    data = load(a.db)
    before = len(data["items"])
    data["items"] = [i for i in data["items"] if i["name"].lower() != a.name.lower()]
    save(data, a.db)
    print(f"removed {before - len(data['items'])} item(s)")
    return 0


# ---------------------------------------------------------------- plan
def cmd_plan(a):
    data = load(a.db)
    active = [i for i in data["items"] if not i.get("done")]
    if not active:
        print("Nothing to plan. Add items first (item add).")
        return 0
    # greedy: volume per difficulty, descending
    active = [i for i in active if i.get("decision") != "keep"]
    ranked = sorted(active, key=lambda i: i["volume"] / i["difficulty"], reverse=True)
    print("DECLUTTER PLAN — biggest volume per decision-effort first\n" + "=" * 58)
    sortie_no, mins, liters, count = 1, 0, 0, 0
    print(f"\nSORTIE 1 (~{SORTIE_MIN} min):")
    for i in ranked:
        t = i["volume"] / LITERS_PER_MIN_EASY * i["difficulty"]  # est minutes
        if mins + t > SORTIE_MIN and count > 0:
            print(f"  → sortie total: {count} items, {liters} L ≈ {math.ceil(liters/BAG_L)} bags, ~{mins:.0f} min")
            sortie_no += 1
            mins = liters = count = 0
            print(f"\nSORTIE {sortie_no} (~{SORTIE_MIN} min):")
        mins += t
        liters += i["volume"]
        count += 1
        print(f"  [ ] {i['name'][:38]:38} {i['volume']:>4}L  diff{i['difficulty']}  {i['room'][:8]:8} → {i.get('decision','?')}")
    print(f"  → sortie total: {count} items, {liters} L ≈ {math.ceil(liters/BAG_L)} bags, ~{mins:.0f} min")
    tot = sum(i["volume"] for i in active)
    print(f"\nPROJECT: {len(active)} items, {tot} L ({tot/1000:.1f} m³) ≈ {math.ceil(tot/BAG_L)} bags "
          f"or {tot/CAR_L:.1f} car-loads, {sortie_no} sorties")
    hard = [i for i in active if i["difficulty"] >= 4]
    if hard:
        print(f"\nNote: {len(hard)} high-difficulty items (sentiment) scheduled last on purpose —")
        print("      do them when momentum exists, not first.")
    return 0


# ---------------------------------------------------------------- sortie
def cmd_sortie(a):
    data = load(a.db)
    if a.action == "start":
        active = [i for i in data["items"] if not i.get("done")]
        active = [i for i in active if i.get("decision") != "keep"]
        ranked = sorted(active, key=lambda i: i["volume"] / i["difficulty"], reverse=True)
        picked, liters = [], 0
        for i in ranked:
            t = i["volume"] / LITERS_PER_MIN_EASY * i["difficulty"]
            if liters + i["volume"] > 0 and len(picked) >= 1:
                # keep sortie to ~20 min of work
                est = sum(x["volume"] / LITERS_PER_MIN_EASY * x["difficulty"] for x in picked)
                if est + t > SORTIE_MIN:
                    break
            picked.append(i)
            liters += i["volume"]
        print(f"SORTIE START {now_iso()}")
        if picked:
            room = picked[0]["room"]
            print(f"Target zone: {room}")
            for i in picked:
                print(f"  → {i['name']} ({i['volume']} L, diff {i['difficulty']}) → {i.get('decision','decide on site')}")
            print(f"Container: {math.ceil(liters/BAG_L)} bag(s) | timer: {SORTIE_MIN} min | "
                  f"exit condition: items out of the room")
        else:
            print("No active items — registry empty. Add items first.")
        print("\nRules: no maybe pile (decide or 30-day box), no re-organizing kept items,")
        print("bags leave the room the moment they fill.")
        return 0
    # done
    if a.bags is None:
        print("[!] sortie done --bags N (how many bags left the room)")
        return 1
    active_before = [i for i in data["items"] if not i.get("done")]
    active_before = [i for i in active_before if i.get("decision") != "keep"]
    ranked = sorted(active_before, key=lambda i: i["volume"] / i["difficulty"], reverse=True)
    picked, liters = [], 0
    for i in ranked:
        t = i["volume"] / LITERS_PER_MIN_EASY * i["difficulty"]
        if picked:
            est = sum(x["volume"] / LITERS_PER_MIN_EASY * x["difficulty"] for x in picked)
            if est + t > SORTIE_MIN:
                break
        picked.append(i)
        liters += i["volume"]
    for i in picked:
        i["done"] = True
        i["removed"] = now_iso()
    data["log"].append({"at": now_iso(), "bags": a.bags, "liters": liters,
                        "items": [i["name"] for i in picked]})
    save(data, a.db)
    done_items = [i for i in data["items"] if i.get("done")]
    freed = sum(i["volume"] for i in done_items)
    pending = sum(i["volume"] for i in data["items"] if not i.get("done") and i.get("decision") != "keep")
    total = freed + pending
    pct = 100 * freed / total if total else 100
    print(f"SORTIE DONE: {len(picked)} items out, {liters} L freed ({a.bags} bags).")
    print(f"Progress: {freed} L of {total} L = {pct:.0f}%")
    remain = [i for i in data["items"] if not i.get("done") and i.get("decision") != "keep"]
    if remain:
        print(f"Next sortie: {remain[0]['room']} — run 'sortie start' when ready.")
    else:
        print("REGISTRY CLEAR. Run 'manifest' for the disposal run.")
    return 0


def cmd_status(a):
    data = load(a.db)
    done = [i for i in data["items"] if i.get("done")]
    active = [i for i in data["items"] if not i.get("done")]
    freed = sum(i["volume"] for i in done)
    pend = sum(i["volume"] for i in active)
    print(f"Declutter status — {now_iso()}")
    print(f"  freed : {freed:6.0f} L ({freed/1000:.1f} m³) across {len(done)} items, {len(data['log'])} sorties")
    print(f"  pending: {pend:6.0f} L across {len(active)} items")
    if data["log"]:
        print("\nsortie log:")
        for e in data["log"]:
            print(f"  {e['at']}  {e['bags']} bag(s), {e['liters']} L")
    return 0


# ---------------------------------------------------------------- bags
def cmd_bags(a):
    data = load(a.db)
    liters = a.liters
    if liters is None:
        liters = sum(i["volume"] for i in data["items"] if not i.get("done"))
    if liters <= 0:
        print("Nothing pending.")
        return 0
    print(f"{liters} L of pending items =")
    print(f"  {math.ceil(liters/BAG_L)} × 60L trash bags")
    print(f"  {math.ceil(liters/BOX_L)} × moving boxes")
    print(f"  {liters/CAR_L:.1f} hatchback loads")
    print(f"  {liters/1000:.2f} m³ of living space back")
    print(f"  ≈ ${liters/1000*SPACE_COST_PER_M3_YEAR:.0f}/yr of storage value freed")
    return 0


# ---------------------------------------------------------------- decide
def cmd_decide(a):
    data = load(a.db)
    match = next((i for i in data["items"] if i["name"].lower() == a.name.lower()), None)
    if match is None:
        print(f"[!] no item named {a.name!r} in registry")
        return 1
    i = match
    print(f"DECISION WORKUP: {i['name']} ({i['volume']} L, diff {i['difficulty']}, value ${i.get('value',0)})\n")
    answers = []
    if a.used_months is not None:
        answers.append(("12-month test", a.used_months <= 12, f"last used {a.used_months} months ago"))
    if a.replace_cost is not None:
        answers.append(("replacement test", a.replace_cost > 30, f"replaces for ${a.replace_cost}"))
    if answers:
        for name, keep, detail in answers:
            print(f"  [{('keep' if keep else 'TOSS'):>4}] {name}: {detail}")
    cost_keep = i["volume"] / 1000 * SPACE_COST_PER_M3_YEAR
    print(f"\n  cost of keeping: ${cost_keep:.0f}/yr in space "
          f"(+ attention, + guilt — unpriced but real)")
    if i.get("value", 0):
        print(f"  sellable value : ${i['value']} — decays ~40%/yr for electronics, ~15%/yr furniture")
        print(f"  sunk cost      : whatever was paid is spent; keeping ≠ refund")
    print("\nVERDICT:", end=" ")
    fails = [n for n, k, _ in answers if not k]
    if not answers:
        print("insufficient answers — rerun with --used-months N --replace-cost $N")
    elif len(fails) >= len(answers) - 0 and len(fails) > 0 and len(answers) > 1 and len(fails) == len(answers):
        print("TOSS/DONATE — fails every keep-test you ran")
    elif fails:
        print(f"lean TOSS/DONATE (failed: {', '.join(fails)}) — gift yourself the space")
    else:
        print("KEEP — passes the tests you gave it")
    if i["difficulty"] >= 4:
        print("\n(sentiment item: photograph it, keep the photo, let the object go —")
        print(" or schedule a 30-day box and decide once, with a deadline)")
    return 0


# ---------------------------------------------------------------- manifest
def cmd_manifest(a):
    data = load(a.db)
    done = [i for i in data["items"] if i.get("done")]
    if not done:
        print("No removed items yet. Run sorties first.")
        return 0
    batches = {}
    for i in done:
        disp = {"toss": "trash"}.get(i.get("decision", "trash"), i.get("decision", "trash"))
        batches.setdefault(disp, []).append(i)
    print("DISPOSITION MANIFEST — " + now_iso())
    print("=" * 58)
    for disp in ("sell", "donate", "recycle", "trash", "undecided"):
        items = batches.get(disp)
        if not items:
            continue
        liters = sum(i["volume"] for i in items)
        print(f"\n{disp.upper()} — {len(items)} items, {liters} L ≈ {math.ceil(liters/BAG_L)} bags")
        for i in items:
            line = f"  - {i['name'][:40]}"
            if disp == "sell" and i.get("value"):
                line += f"  list ${i['value']:.0f}"
            if disp == "donate":
                dv = max(5, min(60, i["volume"] * 0.5))
                line += f"  est. donation value ${dv:.0f}"
            print(line)
    print("\nDISPOSAL RUN:")
    if batches.get("sell"):
        n = len(batches["sell"])
        keep = [i for i in batches["sell"] if (i.get("value") or 0) >= 25]
        print(f"  [ ] sell: list {len(keep)} items worth ≥$25 (rule of thirds — donate the rest,")
        print(f"      listing 40 things at $8 is a part-time job)")
    if batches.get("donate"):
        print(f"  [ ] donate: one drop-off run, get the receipt (tax paper trail)")
    if batches.get("recycle"):
        print(f"  [ ] recycle: electronics → e-waste point; metal → scrap (paid by weight)")
    if batches.get("trash"):
        t = sum(i["volume"] for i in batches["trash"])
        print(f"  [ ] trash: {math.ceil(t/BAG_L)} bags — heavy/bulky items may need a booked pickup")
    print("=" * 58)
    return 0


# ----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("item", help="add/list items")
    p.add_argument("action", nargs="?", default="list", choices=["add", "list"])
    p.add_argument("name", nargs="?", default=None)
    p.add_argument("--room", default=None)
    p.add_argument("--volume", type=float, default=None, help="liters")
    p.add_argument("--difficulty", type=int, default=None, help="1 easy … 5 heirloom")
    p.add_argument("--decision", choices=["keep", "toss", "donate", "sell", "recycle"], default=None)
    p.add_argument("--value", type=float, default=None, help="estimated resell value $")
    p.set_defaults(fn=cmd_item)

    p = sub.add_parser("rm", help="remove an item from the registry")
    p.add_argument("name")
    p.set_defaults(fn=cmd_rm)

    p = sub.add_parser("plan", help="greedy sortie plan, big wins first")
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("sortie", help="run a 20-minute session")
    p.add_argument("action", choices=["start", "done", "status"], nargs="?", default="start")
    p.add_argument("--bags", type=int, default=None)
    p.set_defaults(fn=lambda a: cmd_sortie(a) if a.action != "status" else cmd_status(a))

    p = sub.add_parser("status", help="progress summary")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("bags", help="liters → bags/boxes/car-loads")
    p.add_argument("--liters", type=float, default=None)
    p.set_defaults(fn=cmd_bags)

    p = sub.add_parser("decide", help="decision workup for one item")
    p.add_argument("name")
    p.add_argument("--used-months", type=int, default=None)
    p.add_argument("--replace-cost", type=float, default=None)
    p.set_defaults(fn=cmd_decide)

    p = sub.add_parser("manifest", help="disposition batches + disposal run")
    p.set_defaults(fn=cmd_manifest)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
