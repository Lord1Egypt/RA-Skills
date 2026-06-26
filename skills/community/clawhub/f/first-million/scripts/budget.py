#!/usr/bin/env python3
"""
Manage budget settings and check spending against budget.
Usage: python3 budget.py --set <category>:<amount>|total:<amount>
       python3 budget.py --check [--period month]
"""

import argparse
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.expanduser("~/.openclaw/workspace"), "first-million", "ledger.json")
BUDGET_FILE = os.path.join(os.path.expanduser("~/.openclaw/workspace"), "first-million", "budget.json")

def load_ledger():
    """Load existing ledger data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"transactions": []}

def load_budget():
    """Load budget settings."""
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            return json.load(f)
    return {"categories": {}, "total": None}

def save_budget(budget):
    """Save budget settings."""
    os.makedirs(os.path.dirname(BUDGET_FILE), exist_ok=True)
    with open(BUDGET_FILE, 'w') as f:
        json.dump(budget, f, indent=2, ensure_ascii=False)

def set_budget(category, amount):
    """Set budget for category or total."""
    budget = load_budget()

    if category == "total":
        budget["total"] = float(amount)
    else:
        budget["categories"][category] = float(amount)

    save_budget(budget)
    print(f"✓ Budget set: {category} = ¥{amount}")

def check_budget(period="month"):
    """Check spending against budget."""
    ledger = load_ledger()
    budget = load_budget()

    # Filter transactions for current period
    now = datetime.now()
    start_date = now.replace(day=1) if period == "month" else now

    expenses = [
        t for t in ledger["transactions"]
        if t["type"] == "expense" and t["date"] >= start_date.strftime("%Y-%m-%d")
    ]

    # Calculate spending by category
    spending = {}
    for t in expenses:
        cat = t["category"]
        spending[cat] = spending.get(cat, 0) + t["amount"]

    total_spent = sum(spending.values())

    # Build report
    report = []
    report.append(f"📋 预算检查报告 ({period})")
    report.append("=" * 40)

    if budget["total"]:
        remaining = budget["total"] - total_spent
        pct = (total_spent / budget["total"]) * 100
        status = "✅" if remaining >= 0 else "⚠️"
        report.append(f"{status} 总预算: ¥{total_spent:.2f} / ¥{budget['total']:.2f} ({pct:.1f}%)")
        if remaining >= 0:
            report.append(f"   剩余: ¥{remaining:.2f}")
        else:
            report.append(f"   超支: ¥{abs(remaining):.2f}")
        report.append("")

    # Check category budgets
    if budget["categories"]:
        report.append("分类预算:")
        for cat, limit in budget["categories"].items():
            spent = spending.get(cat, 0)
            remaining = limit - spent
            pct = (spent / limit) * 100
            status = "✅" if remaining >= 0 else "⚠️"
            report.append(f"  {status} {cat}: ¥{spent:.2f} / ¥{limit:.2f} ({pct:.1f}%)")

    return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage budget")
    parser.add_argument("--set", help="Set budget (e.g., 'food:2000' or 'total:5000')")
    parser.add_argument("--check", action="store_true", help="Check budget status")
    parser.add_argument("--period", default="month", help="Period for budget check")

    args = parser.parse_args()

    if args.set:
        if ":" not in args.set:
            print("Error: --set format should be 'category:amount' or 'total:amount'")
        else:
            category, amount = args.set.split(":", 1)
            set_budget(category, amount)
    elif args.check:
        print(check_budget(args.period))
    else:
        print("Error: Please specify --set or --check")
