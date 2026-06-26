#!/usr/bin/env python3
"""
Analyze financial transactions and generate reports.
Usage: python3 analyze.py --period week|month|year|all [--category <category>]
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

DATA_FILE = os.path.join(os.path.expanduser("~/.openclaw/workspace"), "first-million", "ledger.json")

def load_ledger():
    """Load existing ledger data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"transactions": [], "categories": {}}

def filter_by_period(transactions, period):
    """Filter transactions by time period."""
    now = datetime.now()
    start_date = None

    if period == "week":
        start_date = now - timedelta(days=7)
    elif period == "month":
        start_date = now.replace(day=1)
    elif period == "year":
        start_date = now.replace(month=1, day=1)
    elif period == "all":
        return transactions

    if start_date:
        start_str = start_date.strftime("%Y-%m-%d")
        return [t for t in transactions if t["date"] >= start_str]
    return transactions

def summarize(transactions, category_filter=None):
    """Summarize transactions by category and type."""
    income_by_category = defaultdict(float)
    expense_by_category = defaultdict(float)
    total_income = 0.0
    total_expense = 0.0

    for t in transactions:
        if category_filter and t.get("category") != category_filter:
            continue

        if t["type"] == "income":
            income_by_category[t["category"]] += t["amount"]
            total_income += t["amount"]
        elif t["type"] == "expense":
            expense_by_category[t["category"]] += t["amount"]
            total_expense += t["amount"]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net": total_income - total_expense,
        "income_by_category": dict(income_by_category),
        "expense_by_category": dict(expense_by_category)
    }

def format_report(summary):
    """Format summary as readable report."""
    report = []
    report.append(f"📊 财务分析报告")
    report.append(f"=" * 40)
    report.append(f"总收入: ¥{summary['total_income']:.2f}")
    report.append(f"总支出: ¥{summary['total_expense']:.2f}")
    report.append(f"净结余: ¥{summary['net']:.2f}")
    report.append("")

    if summary["expense_by_category"]:
        report.append("📤 支出分类:")
        for cat, amount in sorted(summary["expense_by_category"].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  • {cat}: ¥{amount:.2f}")

    if summary["income_by_category"]:
        report.append("")
        report.append("📥 收入分类:")
        for cat, amount in sorted(summary["income_by_category"].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  • {cat}: ¥{amount:.2f}")

    return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze financial transactions")
    parser.add_argument("--period", default="month", choices=["week", "month", "year", "all"], help="Time period")
    parser.add_argument("--category", help="Filter by category")

    args = parser.parse_args()

    ledger = load_ledger()
    transactions = filter_by_period(ledger["transactions"], args.period)
    summary = summarize(transactions, args.category)
    print(format_report(summary))
