#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional

PREFERRED_EXTS = (".xlsx", ".xlsm", ".xls")


def latest_excel(path: Path) -> Optional[Path]:
    if not path.exists():
        return None
    candidates = [p for p in path.iterdir() if p.is_file() and p.suffix.lower() in PREFERRED_EXTS]
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def select_base(root: Path) -> Path:
    incoming = latest_excel(root / "orders" / "incoming")
    if incoming:
        return incoming
    current = latest_excel(root / "orders" / "current")
    if current:
        return current
    template = root / "templates" / "tmazonORDERLIST_template.xlsx"
    if template.exists():
        return template
    raise FileNotFoundError("No base workbook found in incoming/current/templates")


def main() -> None:
    parser = argparse.ArgumentParser(description="Select BUYMA base workbook")
    parser.add_argument("--root", required=True, help="buyma_order root path")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    print(select_base(root))


if __name__ == "__main__":
    main()
