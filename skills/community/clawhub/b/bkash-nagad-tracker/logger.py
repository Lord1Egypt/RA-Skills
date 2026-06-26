#!/usr/bin/env python3
"""
logger.py — Transaction storage and retrieval
Stores data locally as JSON — no cloud, no database
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# Store data in skill's own directory
DATA_DIR = Path(os.environ.get(
    "BKASH_DATA_DIR",
    Path.home() / ".openclaw" / "bkash-nagad-tracker"
))
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"


METHOD_EMOJI = {
    "bkash":  "🔴",
    "nagad":  "🟠",
    "rocket": "🟣",
    "cash":   "💵",
    "other":  "💰",
}


def ensure_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TRANSACTIONS_FILE.exists():
        TRANSACTIONS_FILE.write_text("[]", encoding="utf-8")


def load() -> list:
    ensure_storage()
    with open(TRANSACTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save(transactions: list):
    ensure_storage()
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)


def current_week() -> str:
    return datetime.now().strftime("%Y-W%W")


def cmd_log(args):
    """Save a new transaction"""
    if not args.amount or args.amount <= 0:
        print("❌ Error: amount must be a positive number")
        sys.exit(1)

    transactions = load()

    entry = {
        "id":        len(transactions) + 1,
        "amount":    float(args.amount),
        "currency":  "BDT",
        "method":    args.method.lower(),
        "category":  args.category.lower(),
        "note":      args.note or "",
        "timestamp": datetime.now().isoformat(),
        "week":      current_week(),
        "date":      datetime.now().strftime("%Y-%m-%d"),
    }

    transactions.append(entry)
    save(transactions)

    emoji = METHOD_EMOJI.get(args.method.lower(), "💰")
    print(f"✅ Logged: {args.amount:.0f}৳ — "
          f"{args.category.title()} {emoji}")


def cmd_undo(args):
    """Delete last transaction"""
    transactions = load()

    if not transactions:
        print("❌ No transactions to undo.")
        return

    removed = transactions.pop()
    save(transactions)

    emoji = METHOD_EMOJI.get(removed["method"], "💰")
    print(f"✅ Deleted: {removed['amount']:.0f}৳ — "
          f"{removed['category'].title()} {emoji} "
          f"({removed['date']})")


def cmd_recent(args):
    """Show N most recent transactions"""
    transactions = load()

    if not transactions:
        print("No transactions logged yet.")
        return

    n = getattr(args, "n", 5)
    recent = transactions[-n:][::-1]  # newest first

    lines = []
    for t in recent:
        emoji = METHOD_EMOJI.get(t["method"], "💰")
        date = t["date"][5:]  # MM-DD
        note = f" ({t['note']})" if t.get("note") else ""
        lines.append(
            f"{date} {emoji} {t['amount']:.0f}৳ "
            f"{t['category'].title()}{note}"
        )

    print("\n".join(lines))


def cmd_export(args):
    """Export all transactions as JSON to stdout"""
    transactions = load()
    print(json.dumps(transactions, indent=2, ensure_ascii=False))


def cmd_stats(args):
    """Quick stats for current week (used by summarizer)"""
    transactions = load()
    week = current_week()
    this_week = [t for t in transactions if t.get("week") == week]

    if not this_week:
        print(json.dumps({"count": 0, "total": 0,
                          "by_category": {}, "by_method": {}}))
        return

    total = sum(t["amount"] for t in this_week)
    by_category: dict = {}
    by_method: dict = {}

    for t in this_week:
        cat = t["category"]
        method = t["method"]
        by_category[cat] = by_category.get(cat, 0) + t["amount"]
        by_method[method] = by_method.get(method, 0) + t["amount"]

    print(json.dumps({
        "count":       len(this_week),
        "total":       total,
        "week":        week,
        "by_category": by_category,
        "by_method":   by_method,
        "transactions": this_week,
    }, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="bKash/Nagad transaction logger"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # log
    p_log = sub.add_parser("log")
    p_log.add_argument("--amount",   type=float, required=True)
    p_log.add_argument("--method",   default="bkash")
    p_log.add_argument("--category", default="other")
    p_log.add_argument("--note",     default="")

    # undo
    sub.add_parser("undo")

    # recent
    p_recent = sub.add_parser("recent")
    p_recent.add_argument("--n", type=int, default=5)

    # export
    sub.add_parser("export")

    # stats (used internally by summarizer)
    sub.add_parser("stats")

    args = parser.parse_args()

    commands = {
        "log":    cmd_log,
        "undo":   cmd_undo,
        "recent": cmd_recent,
        "export": cmd_export,
        "stats":  cmd_stats,
    }
    commands[args.command](args)
