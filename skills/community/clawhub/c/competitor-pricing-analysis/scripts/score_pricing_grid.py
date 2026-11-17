#!/usr/bin/env python3
"""Competitor Pricing Analysis

Scores rows against weighted criteria and prints a ranked table for competitor pricing analysis.

Parameters for this build:
{
  "criteria": [
    {
      "name": "entry price",
      "weight": 30,
      "column": "price_usd"
    },
    {
      "name": "price per unit",
      "weight": 25,
      "column": "price_per_unit"
    },
    {
      "name": "included units",
      "weight": 20,
      "column": "included_units"
    },
    {
      "name": "committed term in months",
      "weight": 15,
      "column": "months_committed"
    },
    {
      "name": "setup fee",
      "weight": 10,
      "column": "setup_fee_usd"
    }
  ],
  "id_column": "vendor"
}

Usage:
    python3 competitor_pricing_analysis.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Competitor Pricing Analysis"


def read_flat(path):
    """Read a small YAML-ish file: `key: value`, `- item` lists, '#' comments."""
    data, key = {}, None
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}")
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if key is None:
                continue
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" in stripped:
            name, _, value = stripped.partition(":")
            name, value = name.strip(), value.strip().strip('"').strip("'")
            if value == "":
                data[name] = []
                key = name
            else:
                data[name] = value
                key = None
    return data


def read_csv(path):
    import csv
    with open(path, newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_out(out_dir, name, lines):
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"wrote {path}")
    return path


CRITERIA = [{"name": "entry price", "weight": 30, "column": "price_usd"}, {"name": "price per unit", "weight": 25, "column": "price_per_unit"}, {"name": "included units", "weight": 20, "column": "included_units"}, {"name": "committed term in months", "weight": 15, "column": "months_committed"}, {"name": "setup fee", "weight": 10, "column": "setup_fee_usd"}]
ID_COLUMN = 'vendor'


def run(input_path, out_dir):
    rows = read_csv(input_path)
    scored = []
    for row in rows:
        total = 0.0
        detail = []
        for crit in CRITERIA:
            raw = str(row.get(crit.get("column", ""), "") or "").strip()
            try:
                value = float(raw)
            except ValueError:
                value = 1.0 if raw else 0.0
            weight = float(crit.get("weight", 1))
            total += value * weight
            detail.append(f"{crit.get('name')}={value:g}")
        scored.append((total, str(row.get(ID_COLUMN, "")), row, detail))
    scored.sort(key=lambda item: item[0], reverse=True)
    report = [f"# {TITLE} ranking", "", f"source: {input_path}", ""]
    for rank, (total, ident, row, detail) in enumerate(scored, 1):
        report.append(f"{rank}. {ident} - score {total:.2f} ({', '.join(detail)})")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never collect a competitor's customer data, credentials, or pricing that sits behind a login.", "Never invent a competitor's price or discount; leave the cell empty if the user has not verified it.", "Never publish the comparison outside the company without a review."]:
        report.append(f"- {rule}")
    write_out(out_dir, "ranking.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
