#!/usr/bin/env python3
"""
Phase 1 — preparation: validate CSV corpus and show column / text preview.
Full synthesis uses synthesize_qa.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Inspect corpus CSV (headers, row count, text preview)")
    p.add_argument("input_csv", type=Path)
    p.add_argument("--text-column", default=None)
    p.add_argument("--preview-chars", type=int, default=200)
    p.add_argument("--max-preview-rows", type=int, default=2)
    args = p.parse_args()

    if not args.input_csv.is_file():
        print(f"Error: file not found: {args.input_csv}", file=sys.stderr)
        return 2

    with args.input_csv.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("Error: empty or headerless CSV", file=sys.stderr)
            return 2
        fields = list(reader.fieldnames)
        col = args.text_column
        if col is None:
            for name in fields:
                if name and name.lower() in ("text", "content", "body", "正文", "文本"):
                    col = name
                    break
            if col is None:
                col = fields[0]

        rows = list(reader)

    previews: list[dict[str, str]] = []
    for i, row in enumerate(rows[: args.max_preview_rows]):
        text = (row.get(col) or "").strip()
        previews.append(
            {
                "row": str(i),
                "text_preview": text[: args.preview_chars] + ("…" if len(text) > args.preview_chars else ""),
            }
        )

    report = {
        "path": str(args.input_csv),
        "row_count": len(rows),
        "columns": fields,
        "detected_text_column": col,
        "previews": previews,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
