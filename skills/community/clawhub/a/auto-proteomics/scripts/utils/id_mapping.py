#!/usr/bin/env python3
"""Minimal ID mapping scaffold for Auto-Proteomics."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-Proteomics ID mapping scaffold")
    parser.add_argument("input", help="Input TSV/CSV file containing protein identifiers")
    parser.add_argument("--column", default="Protein IDs", help="Identifier column name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        print(f"[auto-proteomics] Loaded {path.name}")
        print(f"[auto-proteomics] Target ID column: {args.column}")
        first = next(reader, None)
        if first is None:
            print("[auto-proteomics] File is empty")
        else:
            print("[auto-proteomics] First row preview:")
            print(first)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
