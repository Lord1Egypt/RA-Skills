#!/usr/bin/env python3
"""
Expense Tracker — Export Script
Supports CSV (UTF-8 BOM for Excel China, plain UTF-8 for US Excel) and JSON export.
Run: python3 export.py <format> [json_args]
"""

import json
import sys
import csv
import re
from datetime import datetime, date
from pathlib import Path

LEDGER_FILE = Path.home() / ".qclaw" / "workspace" / "expense-ledger" / "ledger.json"
CATEGORY_ZH = {
    "food": "餐饮", "shopping": "购物", "housing": "住房", "transport": "交通",
    "comm": "通讯", "medical": "医疗", "social": "人情", "entertain": "娱乐",
    "education": "学习", "childcare": "育儿", "travel": "旅行",
    "investment": "投资", "other": "其他",
}
CATEGORY_EN = {
    "food": "Food & Dining", "shopping": "Shopping", "housing": "Housing",
    "transport": "Transport", "comm": "Communication", "medical": "Medical",
    "social": "Social", "entertain": "Entertainment", "education": "Education",
    "childcare": "Childcare", "travel": "Travel", "investment": "Investment",
    "other": "Other",
}


def load_entries(args: dict) -> list:
    with open(LEDGER_FILE, encoding="utf-8") as f:
        ledger = json.load(f)
    entries = ledger.get("entries", [])

    # Filter
    start = args.get("start")
    end = args.get("end")
    if start:
        entries = [e for e in entries if e["date"] >= start]
    if end:
        entries = [e for e in entries if e["date"] <= end]
    cat = args.get("category")
    if cat:
        entries = [e for e in entries if e["category"] == cat]
    acc = args.get("account")
    if acc:
        entries = [e for e in entries if e.get("account") == acc]

    return entries


def _fmt_cat(cat_id: str, lang: str = "zh") -> str:
    if lang == "en":
        return CATEGORY_EN.get(cat_id, cat_id)
    return CATEGORY_ZH.get(cat_id, cat_id)


def export_csv(args: dict) -> dict:
    entries = load_entries(args)
    bom = not args.get("no_bom", False)
    lang = args.get("lang", "zh")

    if not entries:
        return {"ok": False, "error": "No entries found / 没有找到记录"}

    # Build CSV in memory
    import io
    output = io.StringIO()

    if bom:
        # Prepend BOM — for Chinese Excel
        output.write('\ufeff')

    cols = [
        "Date", "Category", "Subcategory",
        "Amount", "Currency",
        "Account", "Member", "Note",
        "Tags", "Raw Input", "Created At"
    ] if lang == "en" else [
        "日期", "主分类", "子分类",
        "金额", "货币",
        "账户", "成员", "备注",
        "标签", "原始输入", "记录时间"
    ]

    writer = csv.writer(output)
    writer.writerow(cols)

    for e in sorted(entries, key=lambda x: x["date"]):
        writer.writerow([
            e["date"],
            _fmt_cat(e["category"], lang),
            e.get("subcategory", ""),
            f"{e['amount']:.2f}",
            e.get("currency", "CNY"),
            e.get("account", "default"),
            e.get("member", ""),
            e.get("note", ""),
            ",".join(e.get("tags", [])),
            e.get("raw", ""),
            e.get("created_at", ""),
        ])

    csv_text = output.getvalue()

    # Write to file
    out_dir = Path.home() / ".qclaw" / "workspace" / "expense-ledger" / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "cn" if bom else "us"
    out_path = out_dir / f"expenses_{ts}_{suffix}.csv"
    with open(out_path, "w", encoding="utf-8-sig" if bom else "utf-8") as f:
        f.write(csv_text)

    return {
        "ok": True,
        "format": "csv",
        "bom": bom,
        "path": str(out_path),
        "count": len(entries),
        "preview": csv_text[:800],
        "download_ready": True,
    }


def export_json(args: dict) -> dict:
    entries = load_entries(args)
    if not entries:
        return {"ok": False, "error": "No entries found"}

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.home() / ".qclaw" / "workspace" / "expense-ledger" / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"expenses_{ts}.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    return {
        "ok": True,
        "format": "json",
        "path": str(out_path),
        "count": len(entries),
    }


def export_excel(args: dict) -> dict:
    """Generate Excel-compatible CSV with proper formatting."""
    # CSV with BOM is the most portable "Excel" export without openpyxl dependency
    return export_csv({**args, "bom": True})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: export.py <csv|json|excel> [json_args]"}))
        sys.exit(1)

    fmt = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    handlers = {
        "csv": export_csv,
        "json": export_json,
        "excel": export_excel,
    }

    if fmt not in handlers:
        print(json.dumps({"error": f"Unknown format: {fmt}. Use csv|json|excel"}))
        sys.exit(1)

    result = handlers[fmt](args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
