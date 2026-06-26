#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List

FIELD_INDEX = {
    "product_name": 1,  # B
    "qty": 3,           # D
    "price": 2,         # C
    "ship_method": 10,  # K
    "option": 11,       # L
    "contact_note": 12, # M
    "name_roman": 14,   # O
    "memo": 15,         # P
    "region": 8,        # I (best-effort; region source can vary by export layout)
}


def map_ship_method(value: str) -> str:
    value = (value or "").strip()
    if value.startswith("その他 /"):
        return "사가"
    if value.startswith("韓国郵便局 /"):
        return "KP"
    return value


def normalize_note(existing: str, region: str, roman_name: str) -> str:
    parts = []
    existing = (existing or "").strip()
    if existing:
        parts.append(existing)
    if (region or "").strip().upper() == "OKINAWA":
        parts.append("오키나와")
    return "\n".join(parts)


def parse_csv(path: Path, encoding: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding=encoding, newline="") as f:
        reader = csv.reader(f)
        for raw in reader:
            if not raw:
                continue
            max_idx = max(FIELD_INDEX.values())
            if len(raw) <= max_idx:
                continue
            # skip probable header rows
            if raw[0].strip() in {"受注番号", "注文番号", "Order"}:
                continue

            memo_raw = (raw[FIELD_INDEX["memo"]] or "").strip()
            m = re.search(r'(\d{6})', memo_raw)
            order_no = m.group(1) if m else ""

            record = {
                "order_no": order_no,
                "memo_no": (raw[FIELD_INDEX["memo"]] or "").strip(),
                "ship_method_raw": (raw[FIELD_INDEX["ship_method"]] or "").strip(),
                "ship_method": map_ship_method(raw[FIELD_INDEX["ship_method"]]),
                "product_name_ko": (raw[FIELD_INDEX["product_name"]] or "").strip(),
                "price": (raw[FIELD_INDEX["price"]] or "").strip(),
                "option": (raw[FIELD_INDEX["option"]] or "").strip(),
                "qty": (raw[FIELD_INDEX["qty"]] or "").strip(),
                "contact_note_raw": (raw[FIELD_INDEX["contact_note"]] or "").strip(),
                "name_roman": (raw[FIELD_INDEX["name_roman"]] or "").strip(),
                "region": (raw[FIELD_INDEX["region"]] or "").strip(),
            }
            if record.get("memo_no") == "受注メモ" and record.get("ship_method_raw") == "発送方法":
                continue
            record["n_value"] = normalize_note(record["contact_note_raw"], record["region"], record["name_roman"])
            rows.append(record)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse BUYMA CSV into normalized JSON")
    parser.add_argument("csv_path", help="Path to BUYMA CSV")
    parser.add_argument("--encoding", default="utf-8-sig", help="CSV encoding (default: utf-8-sig)")
    parser.add_argument("--out", help="Optional JSON output path")
    args = parser.parse_args()

    data = parse_csv(Path(args.csv_path).expanduser().resolve(), args.encoding)
    if args.out:
        Path(args.out).expanduser().resolve().write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
