#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import io
import json
import re
import sys
from datetime import datetime, timezone
from typing import Dict, List

# Windows 终端下强制 UTF-8 输出，避免乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import requests

API = "https://api-gold.aibuy.cloud/quoteCenter/realTime.htm"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

SECTIONS = {
    "related": [
        ("JO_92233", "现货黄金", "price"),
        ("JO_92232", "现货白银", "price"),
        ("JO_92229", "现货铂金", "price"),
        ("JO_92230", "现货钯金", "price"),
        ("JO_92231", "中国香港黄金", "price"),
        ("JO_38495", "中国台湾黄金", "price"),
    ],
    "physical": [
        ("JO_42657", "老凤祥", "price"),
        ("JO_42660", "周大福", "price"),
        ("JO_42625", "周生生", "price"),
        ("JO_42634", "老庙", "price"),
        ("JO_42653", "周六福", "price"),
        ("JO_42646", "六福珠宝", "price"),
        ("JO_52678", "周大生", "price"),
        ("JO_42638", "菜百", "price"),
    ],
    "futures": [
        ("JO_165732", "沪金", "price+percent"),
        ("JO_165757", "沪银", "price+percent"),
        ("JO_12552", "comex黄金", "price+percent"),
        ("JO_12553", "comex白银", "price+percent"),
        ("JO_165655", "沪铜", "price+percent"),
    ],
}


def format_num(value, digits=2):
    try:
        return f"{float(value):.{int(digits)}f}"
    except Exception:
        return "----"


def fetch_quotes(codes: List[str]) -> Dict:
    resp = requests.get(
        API,
        params={"codes": ",".join(codes)},
        headers={"User-Agent": UA},
        timeout=20,
    )
    resp.raise_for_status()
    text = resp.text.strip()
    m = re.match(r"var\s+quote_json\s*=\s*(\{.*\});?\s*$", text, re.S)
    if not m:
        raise RuntimeError("Unexpected API response format")
    return json.loads(m.group(1))


def build_report(selected_sections: List[str]) -> Dict:
    codes = []
    for sec in selected_sections:
        codes.extend(code for code, _, _ in SECTIONS[sec])
    payload = fetch_quotes(codes)

    report = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "sections": {},
    }

    for sec in selected_sections:
        items = []
        for code, name, mode in SECTIONS[sec]:
            q = payload.get(code, {}) or {}
            digits = q.get("digits", 2)
            price = format_num(q.get("q63"), digits)
            unit = q.get("unit")
            entry = {
                "code": code,
                "name": name,
                "price": price,
            }
            if unit:
                entry["unit"] = unit
            if mode == "price+percent":
                percent = format_num(q.get("q80"), 2)
                entry["change_percent"] = percent
            items.append(entry)
        report["sections"][sec] = items
    return report


def render_md(report: Dict, selected_sections: List[str]) -> str:
    title_map = {
        "related": "相关品种",
        "physical": "实物黄金",
        "futures": "贵金属期货",
    }
    lines = []
    for sec in selected_sections:
        lines.append(f"## {title_map[sec]}")
        for item in report["sections"][sec]:
            if sec == "futures":
                lines.append(f"- {item['name']}：{item['price']} | {item.get('change_percent', '----')}%")
            else:
                unit = f" {item['unit']}" if item.get('unit') else ""
                lines.append(f"- {item['name']}：{item['price']}{unit}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Fetch gold/silver quote panels.")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument(
        "--sections",
        default="related,physical,futures",
        help="Comma-separated: related, physical, futures",
    )
    args = ap.parse_args()

    selected = [s.strip() for s in args.sections.split(",") if s.strip()]
    invalid = [s for s in selected if s not in SECTIONS]
    if invalid:
        print(f"Invalid sections: {', '.join(invalid)}", file=sys.stderr)
        return 2

    report = build_report(selected)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_md(report, selected), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
