#!/usr/bin/env python3
"""Copy A-share theme mapping files into the CN market-tape local cache."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


REQUIRED_DATA_KEYS = {"market", "code", "theme", "weight"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_theme_data(path: Path) -> None:
    data = load_json(path)
    rows = data.get("rows") if isinstance(data, dict) else data
    if not isinstance(rows, list) or not rows:
        raise SystemExit(f"{path} must contain a non-empty list or a dict with rows[]")
    sample = next((row for row in rows if isinstance(row, dict)), None)
    if sample is None:
        raise SystemExit(f"{path} does not contain object rows")
    missing = REQUIRED_DATA_KEYS - set(sample)
    if missing:
        raise SystemExit(f"{path} is missing required fields: {', '.join(sorted(missing))}")


def validate_labels(path: Path) -> None:
    labels = load_json(path)
    if not isinstance(labels, dict) or not labels:
        raise SystemExit(f"{path} must contain a non-empty object")
    has_zh = any(isinstance(value, dict) and value.get("zh") for value in labels.values())
    if not has_zh:
        raise SystemExit(f"{path} must contain at least one zh label")


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy theme mapping JSON files into the local skill cache.")
    parser.add_argument("source_dir", type=Path, help="Path to a public theme mapping source directory")
    args = parser.parse_args()

    source_dir = args.source_dir.expanduser().resolve()
    source_data = source_dir / "theme-data.json"
    source_labels = source_dir / "theme-label-i18n.json"

    validate_theme_data(source_data)
    validate_labels(source_labels)

    target_dir = Path(__file__).resolve().parents[1] / "assets" / "themes"
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_data, target_dir / "theme-data.json")
    shutil.copy2(source_labels, target_dir / "theme-label-i18n.json")

    print(f"refreshed {target_dir / 'theme-data.json'}")
    print(f"refreshed {target_dir / 'theme-label-i18n.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
