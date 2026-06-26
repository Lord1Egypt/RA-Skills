#!/usr/bin/env python3
"""style_scan.py — 文字表述一致性扫描 (WARN-level)。

扫描一份 banker markdown 对如下风格失误:

1. 同一数值指标在不同段落精度不一致 (如 `1.34` vs `1.340` vs `1.3` 指代同一字段)
2. 货币单位混用 (同段同时 `亿元` 和 `万元` 且不给显式换算括号)
3. 期间术语混用 (同段同时 `Q3` 和 `三季度` 指代同一期间)
4. 同比增速术语混用 (同段同时 `YoY` 和 `同比`)
5. 日期格式不一 (同份文档同时 `2024-10-27` / `2024/10/27` / `2024年10月27日`)

加 `--warn-only` 则命中任意 WARN 也 exit 0 (便于 CI / validate-delivery 非阻塞调用)。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _shared import find_precision_drift

# hard number pattern: 1.34元/股, 1,088亿元, 22.9% etc.
HARD_NUMBER = re.compile(
    r"(?<![0-9A-Za-z\u4e00-\u9fa5])"
    r"([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)"
    r"\s*"
    r"(亿元|万元|百万元|千万元|%|元/股|元|RMB|USD|CNY|HKD|bps)"
)

DATE_FORMATS = [
    (re.compile(r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b"), "YYYY-MM-DD"),
    (re.compile(r"\b(20\d{2})/(\d{1,2})/(\d{1,2})\b"), "YYYY/MM/DD"),
    (re.compile(r"(20\d{2})年(\d{1,2})月(\d{1,2})日"), "YYYY年MM月DD日"),
]

Q_EN = re.compile(r"\bQ[1-4]\b")
Q_CN = re.compile(r"[一二三四]季度")
YOY_EN = re.compile(r"\bYoY\b", re.IGNORECASE)
YOY_CN = re.compile(r"同比")
YI_YUAN = re.compile(r"亿元")
WAN_YUAN = re.compile(r"(?<!亿)万元")  # avoid double-match on 亿元


def scan_precision_drift(text: str) -> list[str]:
    """Thin wrapper: delegate to _shared.find_precision_drift using this
    script's HARD_NUMBER regex (which covers style-scan-specific units)."""
    return find_precision_drift(text, HARD_NUMBER)


def scan_currency_unit_mix(text: str) -> list[str]:
    """Same paragraph contains both 亿元 and 万元 without a bracketed conversion → WARN."""
    warnings = []
    for i, para in enumerate(re.split(r"\n\s*\n", text), start=1):
        has_yi = bool(YI_YUAN.search(para))
        has_wan = bool(WAN_YUAN.search(para))
        if has_yi and has_wan:
            # tolerate explicit conversion like "(折合 XX 亿元)" / "（约 Y 万元）"
            if re.search(r"[（(][^）)]*(亿元|万元)[^）)]*[）)]", para):
                continue
            warnings.append(
                f"paragraph {i}: mixes 亿元 and 万元 without explicit conversion"
            )
    return warnings


def scan_quarter_term_mix(text: str) -> list[str]:
    warnings = []
    for i, para in enumerate(re.split(r"\n\s*\n", text), start=1):
        if Q_EN.search(para) and Q_CN.search(para):
            warnings.append(
                f"paragraph {i}: mixes Q1-4 (EN) with 一/二/三/四季度 (CN) terms"
            )
    return warnings


def scan_yoy_mix(text: str) -> list[str]:
    warnings = []
    for i, para in enumerate(re.split(r"\n\s*\n", text), start=1):
        if YOY_EN.search(para) and YOY_CN.search(para):
            warnings.append(f"paragraph {i}: mixes YoY (EN) with 同比 (CN)")
    return warnings


def scan_date_format_drift(text: str) -> list[str]:
    seen: set[str] = set()
    for pattern, label in DATE_FORMATS:
        if pattern.search(text):
            seen.add(label)
    if len(seen) >= 2:
        return [f"date format drift: document mixes {' / '.join(sorted(seen))}"]
    return []


def run_all(text: str) -> dict[str, list[str]]:
    return {
        "precision": scan_precision_drift(text),
        "currency": scan_currency_unit_mix(text),
        "quarter": scan_quarter_term_mix(text),
        "yoy": scan_yoy_mix(text),
        "date": scan_date_format_drift(text),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Style consistency scanner for CN banker deliverables.")
    ap.add_argument("path", help="analysis.md (or other MD) to scan")
    ap.add_argument(
        "--warn-only",
        action="store_true",
        help="always exit 0, only print WARN report (recommended for CI).",
    )
    args = ap.parse_args()

    p = Path(args.path)
    if not p.is_file():
        print(f"ERROR: not a file: {p}", file=sys.stderr)
        return 2

    text = p.read_text(encoding="utf-8")
    results = run_all(text)
    total = sum(len(v) for v in results.values())

    if total == 0:
        print(f"OK (style_scan): clean — {p.name} no style drift detected.")
        return 0

    print(f"WARN (style_scan): {total} style issue(s) in {p.name}")
    for category, items in results.items():
        if not items:
            continue
        print(f"  [{category}]")
        for line in items:
            print(f"    - {line}")

    return 0 if args.warn_only else 1


if __name__ == "__main__":
    raise SystemExit(main())
