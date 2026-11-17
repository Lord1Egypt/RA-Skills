#!/usr/bin/env python3
"""Break-Even Analysis

Computes the break-even analysis number from the values the user supplies.

Parameters for this build:
{
  "formula": "contribution_margin = price_per_unit - variable_cost_per_unit; break_even_units = fixed_costs / contribution_margin; break_even_revenue = break_even_units * price_per_unit; headroom = (units_planned - break_even_units) * contribution_margin",
  "fields": [
    "price_per_unit",
    "variable_cost_per_unit",
    "fixed_costs",
    "units_planned"
  ]
}

Usage:
    python3 break-even_analysis.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Break-Even Analysis"


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


FIELDS = ["price_per_unit", "variable_cost_per_unit", "fixed_costs", "units_planned"]
FORMULA = 'contribution_margin = price_per_unit - variable_cost_per_unit; break_even_units = fixed_costs / contribution_margin; break_even_revenue = break_even_units * price_per_unit; headroom = (units_planned - break_even_units) * contribution_margin'


def run(input_path, out_dir):
    data = read_flat(input_path)
    values = {}
    for field in FIELDS:
        raw = str(data.get(field, "") or "0").replace(",", "").replace("$", "").replace("%", "")
        try:
            values[field] = float(raw)
        except ValueError:
            values[field] = 0.0
    report = [f"# {TITLE}", "", f"source: {input_path}", ""]
    for field, value in values.items():
        report.append(f"- {field}: {value:g}")
    report.append("")
    report.append(f"formula: {FORMULA or 'documented in the skill'}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never treat the break-even number as a forecast or as a promise of profit.", "Never leave out a fixed cost to make the break-even point look reachable.", "Never present the result as accounting advice; the accountant confirms the treatment."]:
        report.append(f"- {rule}")
    write_out(out_dir, "calculation.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
