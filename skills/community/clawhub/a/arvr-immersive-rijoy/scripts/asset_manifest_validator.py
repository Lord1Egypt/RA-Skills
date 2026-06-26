#!/usr/bin/env python3
"""
Validate 3D/AR asset manifest (CSV or JSON Lines) for minimum required fields and naming rules.

Use cases:
- Give growth/content/3D vendors a single "delivery manifest spec"
- Catch missing fields, format drift, and bad file extensions before modeling/export

Single responsibility: static validation and report only; does not parse 3D file contents.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


REQUIRED_FIELDS = [
    "product_id",
    "variant_id",
    "title",
    "format",  # glb/usdz (comma-separated ok)
    "file_name",
    "unit",  # mm/cm/m
    "width",
    "height",
    "depth",
]

ALLOWED_UNITS = {"mm", "cm", "m"}
ALLOWED_FORMATS = {"glb", "usdz"}

FILENAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{2,}\.(glb|usdz)$", re.IGNORECASE)


@dataclass(frozen=True)
class Issue:
    row: int
    field: str
    message: str


def iter_rows_csv(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {k: (v or "").strip() for k, v in row.items()}


def iter_rows_jsonl(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if not isinstance(obj, dict):
                continue
            yield {k: str(v).strip() for k, v in obj.items()}


def parse_number(value: str) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def validate_rows(rows: Iterable[dict]) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    count = 0
    for idx, row in enumerate(rows, start=2):  # csv header is line 1
        count += 1
        for field in REQUIRED_FIELDS:
            if not row.get(field):
                issues.append(Issue(row=idx, field=field, message="Missing required field"))

        unit = (row.get("unit") or "").lower()
        if unit and unit not in ALLOWED_UNITS:
            issues.append(Issue(row=idx, field="unit", message=f"Invalid unit: {unit} (allowed: mm/cm/m)"))

        fmt = (row.get("format") or "").lower()
        if fmt:
            parts = [p.strip() for p in fmt.split(",") if p.strip()]
            bad = [p for p in parts if p not in ALLOWED_FORMATS]
            if bad:
                issues.append(Issue(row=idx, field="format", message=f"Invalid format: {', '.join(bad)} (allowed: glb/usdz)"))

        file_name = row.get("file_name") or ""
        if file_name and not FILENAME_RE.match(file_name):
            issues.append(
                Issue(
                    row=idx,
                    field="file_name",
                    message="File name does not match suggested rule (lowercase/digits/underscore/hyphen, ending .glb or .usdz)",
                )
            )

        for dim in ("width", "height", "depth"):
            v = row.get(dim) or ""
            if not v:
                continue
            n = parse_number(v)
            if n is None or n <= 0:
                issues.append(Issue(row=idx, field=dim, message=f"Dimension must be a positive number: {v}"))

    return issues, count


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate 3D/AR asset manifest (CSV/JSONL) fields and naming.")
    ap.add_argument("input", type=Path, help="Manifest file path: .csv or .jsonl")
    ap.add_argument(
        "--format",
        choices=["csv", "jsonl", "auto"],
        default="auto",
        help="Input format (default: auto)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output report JSON path (default: print to stdout)",
    )
    args = ap.parse_args()

    path = args.input.resolve()
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2

    fmt = args.format
    if fmt == "auto":
        fmt = "jsonl" if path.suffix.lower() == ".jsonl" else "csv"

    try:
        rows = list(iter_rows_jsonl(path)) if fmt == "jsonl" else list(iter_rows_csv(path))
    except Exception as e:
        print(f"Error: read failed: {e}", file=sys.stderr)
        return 2

    issues, total = validate_rows(rows)
    report = {
        "total_rows": total,
        "issue_count": len(issues),
        "issues": [{"row": i.row, "field": i.field, "message": i.message} for i in issues],
    }

    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)

    return 0 if len(issues) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
