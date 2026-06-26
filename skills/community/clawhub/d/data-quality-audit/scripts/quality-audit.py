#!/usr/bin/env python3
"""
quality-audit.py — helper for the data-quality-audit skill.

Mode:

    quality-audit.py --parse-only <data-provenance.md>
        Parse a data-provenance markdown table into a structured JSON array.
        One entry per hard-number row; the agent can then pick each entry
        and fire an independent MCP cross-check.

The agent owns the actual cross-source fetch loop (it has the MCP tool list);
this script is just a deterministic parser so agents don't have to guess at
the provenance-table format.

Provenance-table convention (from cn-client-investigation/references/
data-sources.md template):

    | 指标 | 数值 | 单位 | 期间 | Tier | 源 | URL/工具 | 取数时间 | 交叉验证状态 |

The parser is tolerant of:
- Leading/trailing | on rows
- Extra whitespace around cells
- Header rows (first row with "指标" + "数值", separator "---" below)
- Blank lines between sections
- Chinese + English column headers on the same row (first occurrence wins)
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys


HEADER_HINT = re.compile(r"指\s*标|metric", re.IGNORECASE)
SEPARATOR_LINE = re.compile(r"^\|?\s*-{3,}")


def parse_provenance(text: str) -> list[dict]:
    """Parse a data-provenance markdown file into a list of dict entries.

    Each entry: {metric, value, unit, period, tier, source, url_tool,
                 fetched_at, status}.
    """
    entries: list[dict] = []
    # Split into rough table blocks by blank lines, but most provenance files
    # are one big table — the simpler scan is line-by-line.
    lines = text.splitlines()
    header_cols: list[str] = []
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        # skip section headings (# xxx)
        if line.startswith("#"):
            continue
        # split on | ignoring leading/trailing empty cells
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        # separator row  | --- | --- |
        if all(SEPARATOR_LINE.match("|" + c) or set(c) <= {"-", ":", " "} for c in cells):
            continue
        # first non-separator row with a "指标" / "metric" cell → header
        if not header_cols and any(HEADER_HINT.search(c) for c in cells):
            header_cols = cells
            continue
        # data row: only accept if it has at least (metric, value) columns
        if len(cells) < 2:
            continue
        entry = {}
        if header_cols:
            for i, cell in enumerate(cells):
                if i >= len(header_cols):
                    break
                key = normalise_col(header_cols[i])
                entry[key] = cell
        else:
            # fallback positional (unnamed)
            keys = [
                "metric", "value", "unit", "period",
                "tier", "source", "url_tool", "fetched_at", "status",
            ]
            for i, cell in enumerate(cells):
                if i >= len(keys):
                    break
                entry[keys[i]] = cell
        # require at least a metric and value with something in them
        if (entry.get("metric") or "").strip() and (entry.get("value") or "").strip():
            entries.append(entry)
    return entries


def normalise_col(col: str) -> str:
    col = col.strip().lower()
    # Chinese → canonical English key
    mapping = {
        "指标": "metric",
        "数值": "value",
        "单位": "unit",
        "期间": "period",
        "tier": "tier",
        "源": "source",
        "来源": "source",
        "url": "url_tool",
        "url/工具": "url_tool",
        "工具": "url_tool",
        "取数时间": "fetched_at",
        "交叉验证": "status",
        "交叉验证状态": "status",
        "状态": "status",
    }
    for k, v in mapping.items():
        if k in col:
            return v
    # Fall back to a slug of the header cell (best-effort)
    return re.sub(r"[^a-z0-9_]+", "_", col).strip("_") or "col"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="data-quality-audit helper (skill: lead-discovery / data-quality-audit)"
    )
    ap.add_argument(
        "--parse-only",
        action="store_true",
        help="Parse a data-provenance markdown into JSON and print to stdout.",
    )
    ap.add_argument(
        "provenance",
        help="Path to data-provenance.md",
    )
    args = ap.parse_args()

    p = pathlib.Path(args.provenance)
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8", errors="replace")

    entries = parse_provenance(text)

    if args.parse_only:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0

    # Non-parse-only mode currently just reports count; the agent runs the
    # actual cross-fetch loop (it has the MCP tools).
    print(
        f"parsed {len(entries)} hard-number entries from {p}; "
        f"invoke the data-quality-audit skill's agent workflow to cross-check each.",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
