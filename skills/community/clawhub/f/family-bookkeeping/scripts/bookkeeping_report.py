#!/usr/bin/env python3
import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, Iterable, List, Optional

CANONICAL_DATE_FMT = "%Y-%m-%d"


def clean(v):
    return "" if v is None else str(v).strip()


def parse_amount(v) -> Decimal:
    text = clean(v).replace(",", "")
    if not text:
        return Decimal("0")
    try:
        return Decimal(text)
    except InvalidOperation:
        return Decimal("0")


def parse_date(v) -> Optional[datetime]:
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        ts = float(v)
        if ts > 10_000_000_000:
            ts /= 1000.0
        return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone()
    text = clean(v).replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:19], fmt)
        except Exception:
            pass
    return None


def load_rows(path: str) -> List[Dict]:
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "records" in data:
            return [item.get("fields", {}) for item in data["records"]]
        if isinstance(data, list):
            return data
        raise ValueError("Unsupported JSON structure")
    if p.suffix.lower() == ".csv":
        with open(p, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError("Unsupported input file")


def filter_rows(rows: Iterable[Dict], month: Optional[str], bookkeeper: str, category: str, platform: str, income_expense: str):
    out = []
    for row in rows:
        dt = parse_date(row.get("日期"))
        if month:
            if not dt or dt.strftime("%Y-%m") != month:
                continue
        if bookkeeper and clean(row.get("记账人")) != bookkeeper:
            continue
        if category and clean(row.get("一级类型")) != category and clean(row.get("二级类型")) != category:
            continue
        if platform and clean(row.get("支付平台")) != platform:
            continue
        if income_expense and clean(row.get("收支类型")) != income_expense:
            continue
        out.append(row)
    return out


def summarize(rows: List[Dict], top_n: int = 5):
    total_income = Decimal("0")
    total_expense = Decimal("0")
    by_cat1 = defaultdict(Decimal)
    by_cat2 = defaultdict(Decimal)
    by_person = defaultdict(Decimal)
    by_platform = defaultdict(Decimal)

    for row in rows:
        amount = parse_amount(row.get("金额"))
        direction = clean(row.get("收支类型"))
        sign_amount = amount
        if direction == "收入":
            total_income += amount
        else:
            total_expense += amount
            cat1 = clean(row.get("一级类型")) or "未分类"
            cat2 = clean(row.get("二级类型")) or "未分类"
            by_cat1[cat1] += amount
            by_cat2[f"{cat1}/{cat2}"] += amount
            by_person[clean(row.get("记账人")) or "未知"] += amount
            by_platform[clean(row.get("支付平台")) or "未知"] += amount

    def top_map(d):
        return [
            {"name": k, "amount": float(v)}
            for k, v in sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        ]

    return {
        "rows": len(rows),
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net": float(total_income - total_expense),
        "top_categories": top_map(by_cat1),
        "top_subcategories": top_map(by_cat2),
        "by_person": top_map(by_person),
        "by_platform": top_map(by_platform),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate bookkeeping summary from exported rows.")
    parser.add_argument("input", help="JSON/CSV rows (e.g. exported records or normalized rows)")
    parser.add_argument("--month", help="Filter month, e.g. 2026-03")
    parser.add_argument("--bookkeeper", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--platform", default="")
    parser.add_argument("--income-expense", default="")
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    rows = load_rows(args.input)
    filtered = filter_rows(rows, args.month, args.bookkeeper, args.category, args.platform, args.income_expense)
    result = summarize(filtered, top_n=args.top)
    result["filters"] = {
        "month": args.month or None,
        "bookkeeper": args.bookkeeper or None,
        "category": args.category or None,
        "platform": args.platform or None,
        "income_expense": args.income_expense or None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
