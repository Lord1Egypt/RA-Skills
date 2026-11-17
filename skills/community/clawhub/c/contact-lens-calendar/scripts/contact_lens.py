#!/usr/bin/env python3
"""contact-lens-calendar — wear/replace calendar from open-date + lens type.

Every contact lens box has the same two facts printed on it: the lens type
and (for disposables) nothing else useful — the expiry date on the carton is
the STERILE shelf life, not the wear life. The wear clock starts when the
foil is peeled. This tool computes, from the day you opened a lens, the
exact do-not-exceed replacement date for daily / biweekly / monthly /
quarterly / yearly lenses, tracks an unlimited inventory of open boxes,
warns when a lens is due (or overdue), and computes daily cost so the
"dailies are too expensive" debate can be settled with numbers.

Subcommands:
  due        — replacement verdicts for every open lens (default)
  plan       — forward calendar: what a lens opened on DATE becomes due
  inventory  — boxes on hand: unopened shelf life + open-order queue
  cost       — daily/annual cost of a wear modality
  log        — record an open event (JSON store), so tracking persists

All dates ISO (YYYY-MM-DD). Store: contacts.json next to this script.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

STORE = Path(__file__).resolve().parent.parent / "contacts.json"

# wear life in days, per lens packaging class
WEAR_DAYS = {
    "daily": 1,
    "biweekly": 14,
    "monthly": 30,
    "quarterly": 90,
    "yearly": 365,
}
# typical street price per lens (USD) for cost math; user can override
PRICE_PER_LENS = {
    "daily": 0.70,
    "biweekly": 1.60,
    "monthly": 3.20,
    "quarterly": 6.50,
    "yearly": 20.0,
}
# unopened sterile shelf life, years from manufacture (conservative)
SHELF_YEARS = 5


def d(s: str) -> date:
    return date.fromisoformat(s)


def fmt(x: date) -> str:
    return x.isoformat()


def load_store() -> dict:
    if STORE.exists():
        return json.loads(STORE.read_text())
    return {"open_lenses": [], "boxes": []}


def save_store(data: dict) -> None:
    STORE.write_text(json.dumps(data, indent=2))


def replace_date(opened: str, kind: str) -> date:
    """The do-not-exceed date: opened + wear_life - 1 (day 1 = open day)."""
    return d(opened) + timedelta(days=WEAR_DAYS[kind] - 1)


def wear_for(kind: str, opened: str, on: str) -> str:
    """Human wear accounting as of date `on` for lens opened `opened`."""
    life = WEAR_DAYS[kind]
    used = (d(on) - d(opened)).days + 1
    left = life - used
    if left < 0:
        return f"OVERDUE by {-left} day(s) — discard now (used {used} of {life})"
    if left == 0:
        return f"due TODAY (day {used} of {life})"
    return f"day {used} of {life} — {left} day(s) left, replace by {fmt(replace_date(opened, kind))}"


def cmd_due(args: argparse.Namespace) -> None:
    store = load_store()
    on = args.on or date.today().isoformat()
    if not store["open_lenses"]:
        print("No open lenses tracked. Log one:  contact_lens.py log --kind monthly --opened 2026-10-01 --eye left")
        return
    flagged = False
    for lens in store["open_lenses"]:
        if lens.get("discarded"):
            continue
        status = wear_for(lens["kind"], lens["opened"], on)
        mark = " ⚠" if "OVERDUE" in status or "due TODAY" in status else ""
        print(f"[{lens.get('label') or lens['eye']}] {lens['kind']} opened {lens['opened']}: {status}{mark}")
        if mark:
            flagged = True
    if args and getattr(args, "verbose", False):
        pass
    if not flagged:
        print("All tracked lenses within wear life.")


def cmd_plan(args: argparse.Namespace) -> None:
    opened = args.opened
    print(f"Lens opened {opened}:")
    for kind in WEAR_DAYS:
        rd = replace_date(opened, kind)
        print(f"  {kind:<10} wear life {WEAR_DAYS[kind]:>3}d  → replace by {fmt(rd)}")
    print("Reminder rule: set the replace alert 1 day EARLY (buffer for solution/handling slip).")


def cmd_inventory(args: argparse.Namespace) -> None:
    store = load_store()
    if not store["boxes"]:
        print("No boxes tracked. Add:  contact_lens.py log --kind monthly --boxes 4 --lenses-per-box 6")
        return
    total = 0
    for b in store["boxes"]:
        if b.get("unopened", 0) <= 0:
            continue
        per = WEAR_DAYS[b["kind"]]
        pairs = b["unopened"] * b.get("lenses_per_box", 6) // 2
        days = pairs * per
        total += days
        print(f"{b['kind']:<10} {b['unopened']} box(es) × {b.get('lenses_per_box', 6)} lenses = {pairs} pairs → {days} days of wear")
    print(f"Total unopened supply: {total} days (~{total / 30.4:.1f} months)")


def cmd_cost(args: argparse.Namespace) -> None:
    print(f"Cost per wear-day (both eyes), list assumptions at {args.eyes} eye(s):")
    for kind, life in WEAR_DAYS.items():
        per_day = PRICE_PER_LENS[kind] * args.eyes / max(life, 1)
        print(f"  {kind:<10} ${PRICE_PER_LENS[kind]:.2f}/lens, life {life:>3}d → ${per_day:.2f}/day → ${per_day * 365:.0f}/yr")
    print("Dailies also cost solution ~$0; monthlies add ~$0.30/day solution+case. Adjust --price to your real receipt.")


def cmd_log(args: argparse.Namespace) -> None:
    store = load_store()
    if args.boxes:
        store["boxes"].append({
            "kind": args.kind,
            "unopened": args.boxes,
            "lenses_per_box": args.lenses_per_box,
            "acquired": args.opened,
        })
        print(f"Logged {args.boxes} unopened box(es) of {args.kind}.")
    else:
        store["open_lenses"].append({
            "kind": args.kind,
            "opened": args.opened,
            "eye": args.eye,
            "label": args.label,
        })
        rd = replace_date(args.opened, args.kind)
        print(f"Logged {args.kind} lens ({args.eye}) opened {args.opened} → replace by {fmt(rd)}.")
    save_store(store)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("due", help="replacement verdicts for open lenses")
    sp.add_argument("--on", help="as-of date ISO (default today)")
    sp.set_defaults(fn=cmd_due)

    sp = sub.add_parser("plan", help="replacement dates for a lens opened on DATE")
    sp.add_argument("--opened", required=True)
    sp.set_defaults(fn=cmd_plan)

    sp = sub.add_parser("inventory", help="days of wear remaining in unopened boxes")
    sp.set_defaults(fn=cmd_inventory)

    sp = sub.add_parser("cost", help="daily/annual cost per wear modality")
    sp.add_argument("--eyes", type=int, default=2, choices=(1, 2))
    sp.set_defaults(fn=cmd_cost)

    sp = sub.add_parser("log", help="record an open event or a box purchase")
    sp.add_argument("--kind", required=True, choices=list(WEAR_DAYS))
    sp.add_argument("--opened", required=True, help="date opened/acquired ISO")
    sp.add_argument("--eye", default="both", choices=("left", "right", "both"))
    sp.add_argument("--label", help="optional note, e.g. brand")
    sp.add_argument("--boxes", type=int, help="log N unopened boxes instead of an open lens")
    sp.add_argument("--lenses-per-box", type=int, default=6)
    sp.set_defaults(fn=cmd_log)

    args = p.parse_args()
    if not args.cmd:
        args.cmd = "due"
        args.on = None
        cmd_due(args)
        return
    args.fn(args)


if __name__ == "__main__":
    main()
