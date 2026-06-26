#!/usr/bin/env python3
"""
source_authenticity_check.py — catch fabricated source labels in banker
deliverable `data-provenance.md` tables.

Context — 2026-04-20 multi-company real-test found that MiniMax-host agents
produced provenance tables citing "Wind (2026-04-17)" and "同花顺 F10" as
sources for market data even though neither is an installed MCP nor an
accessible tool on macmini. The upstream `verify_intelligence.py` gate only
runs on `*intelligence*.md` (lead-discovery workflow) and never sees these
banker provenance tables. This script fills that gap.

What it does:
    1. Parse every markdown table in data-provenance.md
    2. Find the column most likely to hold source labels
       (header matches /source|来源|源/ case-insensitive)
    3. For every non-header row, classify the source cell against:
       - MCP_TOOL_ANCHORS   (aigroup-market-mcp / PrimeMatrixData / Tianyancha) — authoritative, installed
       - OFFICIAL_ANCHORS   (巨潮 / 交易所 / SEC / 招股书 / 年报 / 季报 / 中报 / 公告 / URL) — primary filings
       - MEDIA_ANCHORS      (新闻 / 东方财富 / 财新 / …) — secondary, OK for context
       - FORBIDDEN_ANCHORS  (Wind / 万得 / 同花顺) — labels that point to tools NOT installed

Modes:
    Default      → FAIL on FORBIDDEN; warn on rows with no recognisable anchor.
    --strict-mcp → additionally FAIL when a row's source is media-only (banker
                   hard numbers under strict mode must come from MCP or official
                   filing, not from aggregator sites).

Usage:
    python3 source_authenticity_check.py <data-provenance.md>
    python3 source_authenticity_check.py --strict-mcp <data-provenance.md>
"""
from __future__ import annotations
import argparse
import pathlib
import re
import sys

MCP_TOOL_ANCHORS = (
    "aigroup-market-mcp",
    # CamelCase (as invoked) and lowercase (as raw-data filename stems) variants
    # both appear in Source cells: the filename convention is `-primematrix-` /
    # `-tianyancha-` while the tool invocation is `PrimeMatrixData__` /
    # `Tianyancha__`. Accept both.
    "PrimeMatrixData", "primematrix", "prime-matrix", "prime_matrix",
    "Tianyancha", "tianyancha", "tyc",
    # bare tool names as a softer match for tables that don't spell out the MCP prefix
    "__basic_info",
    "__stock_data",
    "__company_performance",
    "__companyBaseInfo",
    "__risk",
)

OFFICIAL_ANCHORS = (
    "招股书", "年报", "季报", "半年报", "中报",
    "公司公告", "公告",
    "巨潮", "cninfo", "CNINFO",
    "上交所", "深交所", "港交所", "SSE", "SZSE", "HKEX",
    "国家企业信用", "gsxt.gov.cn", "gsxt",
    "sec.gov", "EDGAR",
    "招股说明书", "募集说明书",
    "http://", "https://",
)

MEDIA_ANCHORS = (
    "东方财富", "Choice",
    "财新", "21世纪", "第一财经", "中证", "上证", "财联社", "澎湃",
    "新浪财经", "新浪",
    "证券之星", "stockstar",
    "金融界", "jrj.com",
    "华尔街见闻", "wallstreetcn",
    "中国基金报", "chnfund",
    "界面新闻", "jiemian",
    "中鹏信评", "中诚信", "联合资信", "大公国际",
    "上海证券报", "证券日报", "证券时报",
    "雪球", "xueqiu", "派财经", "时代周报",
    "乘联会",
)

FORBIDDEN_ANCHORS = (
    "Wind",
    "万得",
    "同花顺",  # matches "同花顺 F10" as well
)

SOURCE_HEADER_PATTERN = re.compile(r"(?i)(source|来源|源|数据来源)")


def parse_tables(text: str) -> list[tuple[int, list[str], list[list[str]]]]:
    """Return [(start_line, headers, rows_as_cells), ...] for each markdown table.

    A markdown table is a contiguous run of pipe-prefixed lines where one of
    the first two lines matches the `-+-` separator pattern.
    """
    lines = text.splitlines()
    tables: list[tuple[int, list[str], list[list[str]]]] = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines):
            sep = lines[i + 1].lstrip()
            if re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", sep):
                headers = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows: list[list[str]] = []
                j = i + 2
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    row = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    rows.append(row)
                    j += 1
                tables.append((i + 1, headers, rows))
                i = j
                continue
        i += 1
    return tables


def find_source_column(headers: list[str]) -> int | None:
    """Return the index of the first source-like column, or None."""
    for idx, h in enumerate(headers):
        if SOURCE_HEADER_PATTERN.search(h):
            return idx
    return None


def classify(cell: str) -> str:
    """Return 'mcp' | 'official' | 'media' | 'forbidden' | 'none'."""
    if any(a in cell for a in FORBIDDEN_ANCHORS):
        return "forbidden"
    if any(a in cell for a in MCP_TOOL_ANCHORS):
        return "mcp"
    if any(a in cell for a in OFFICIAL_ANCHORS):
        return "official"
    if any(a in cell for a in MEDIA_ANCHORS):
        return "media"
    if "Tushare" in cell or "tushare" in cell:
        return "mcp"
    return "none"


def scan(
    text: str, strict_mcp: bool = False
) -> tuple[list[tuple[int, str, str, str]], list[tuple[int, str, str, str]]]:
    """Return (failures, warnings).

    failures: rows that hard-fail under current mode
    warnings: rows that are soft-OK but flagged for reviewer attention
    """
    failures: list[tuple[int, str, str, str]] = []
    warnings: list[tuple[int, str, str, str]] = []
    tables = parse_tables(text)
    for table_start, headers, rows in tables:
        src_idx = find_source_column(headers)
        if src_idx is None:
            continue  # table has no source column — not our concern
        for row_offset, row in enumerate(rows, start=1):
            if src_idx >= len(row):
                continue
            cell = row[src_idx]
            if not cell:
                continue
            verdict = classify(cell)
            first_cell = row[0] if row else ""
            line_no = table_start + 1 + row_offset  # header + sep + row
            if verdict == "forbidden":
                failures.append(
                    (line_no, first_cell[:60], cell[:80], "forbidden source (tool not installed)"),
                )
            elif verdict == "none":
                warnings.append(
                    (line_no, first_cell[:60], cell[:80], "unrecognised source anchor"),
                )
            elif strict_mcp and verdict == "media":
                failures.append(
                    (line_no, first_cell[:60], cell[:80],
                     "media-only under --strict-mcp; want MCP tool or official filing"),
                )
    return failures, warnings


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("provenance_md", type=pathlib.Path)
    ap.add_argument(
        "--strict-mcp",
        action="store_true",
        help="fail on media-only citations in addition to forbidden labels",
    )
    args = ap.parse_args(argv[1:])

    if not args.provenance_md.exists():
        print(f"file not found: {args.provenance_md}", file=sys.stderr)
        return 2
    text = args.provenance_md.read_text(encoding="utf-8", errors="replace")

    failures, warnings = scan(text, strict_mcp=args.strict_mcp)
    mode = "strict-mcp" if args.strict_mcp else "default"

    if warnings:
        print(
            f"WARN [{mode}]: {len(warnings)} row(s) with unrecognised source anchor in "
            f"{args.provenance_md}:",
            file=sys.stderr,
        )
        for lineno, metric, cell, reason in warnings[:30]:
            print(f"  L{lineno:>4}: {metric!r} — source={cell!r}", file=sys.stderr)
        if len(warnings) > 30:
            print(f"  ...and {len(warnings) - 30} more truncated.", file=sys.stderr)

    if failures:
        print(
            f"FAIL [{mode}]: {len(failures)} row(s) with disallowed source in "
            f"{args.provenance_md}:",
            file=sys.stderr,
        )
        for lineno, metric, cell, reason in failures[:30]:
            print(f"  L{lineno:>4}: {metric!r} — source={cell!r} — {reason}",
                  file=sys.stderr)
        if len(failures) > 30:
            print(f"  ...and {len(failures) - 30} more truncated.", file=sys.stderr)
        return 1

    print(f"OK: source_authenticity [{mode}] clean on {args.provenance_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
