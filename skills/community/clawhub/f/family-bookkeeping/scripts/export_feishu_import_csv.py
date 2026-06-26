#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

CANONICAL_OUT_FIELDS = [
    "家庭记账",
    "日期",
    "金额",
    "记账人",
    "一级类型",
    "二级类型",
    "备注",
    "收支类型",
    "支付平台",
    "导入来源",
    "流水号",
]


def clean(v):
    return "" if v is None else str(v).strip()


def primary_title(row):
    date = clean(row.get("日期"))[:10]
    direction = clean(row.get("收支类型")) or "交易"
    amount = clean(row.get("金额"))
    note = clean(row.get("备注"))
    category = "/".join([x for x in [clean(row.get("一级类型")), clean(row.get("二级类型"))] if x])

    tail = note or category or clean(row.get("支付平台")) or "账目"
    if len(tail) > 30:
        tail = tail[:30] + "…"
    return " ".join(x for x in [date, direction, amount, tail] if x)


def load_input(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list of normalized rows")
        return data
    if suffix == ".csv":
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError("Unsupported input type. Expected normalized .json or .csv")


def convert(rows):
    out = []
    for row in rows:
        item = {
            "家庭记账": primary_title(row),
            "日期": clean(row.get("日期")),
            "金额": clean(row.get("金额")),
            "记账人": clean(row.get("记账人")),
            "一级类型": clean(row.get("一级类型")),
            "二级类型": clean(row.get("二级类型")),
            "备注": clean(row.get("备注")),
            "收支类型": clean(row.get("收支类型")),
            "支付平台": clean(row.get("支付平台")),
            "导入来源": clean(row.get("导入来源")),
            "流水号": clean(row.get("流水号")),
        }
        out.append(item)
    return out


def write_csv(rows, output):
    with open(output, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_OUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Convert normalized bookkeeping rows into a Feishu-importable CSV.")
    parser.add_argument("input", help="Normalized .json or .csv produced by normalize_bills.py")
    parser.add_argument("--output", required=True, help="Path to output CSV for Feishu import")
    args = parser.parse_args()

    rows = load_input(args.input)
    out = convert(rows)
    write_csv(out, args.output)
    print(f"Wrote {len(out)} rows to {args.output}")


if __name__ == "__main__":
    main()
