#!/usr/bin/env python3
"""Offline font-metrics generator (P4).

Measures real glyph advances with PIL and writes compact per-family JSON
tables into engine/metrics/. These shipped tables are what the engine uses
at compile time — PIL is never a runtime dependency, so the same repo
checkout measures text identically on every machine (D9 determinism).

Usage:
  python3 scripts/generate_font_metrics.py --font /path/to/Font.ttc [--index 0]
  python3 scripts/generate_font_metrics.py --scan   # measure common system fonts

Table format (em units, relative to point size):
  {"family": "...", "ascii": [95 widths for U+0020..U+007E],
   "cjk": <ideograph advance>, "fallback_wide": ..., "fallback_narrow": ...,
   "measured_from": "<file>#<index>"}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import ImageFont

OUT_DIR = Path(__file__).resolve().parents[1] / "engine" / "metrics"
SAMPLE_SIZE = 1000

SCAN_CANDIDATES = [
    ("/System/Library/Fonts/Helvetica.ttc", 0),
    ("/System/Library/Fonts/PingFang.ttc", 0),
    ("/System/Library/Fonts/Supplemental/Songti.ttc", 0),
    ("/System/Library/Fonts/SFNS.ttf", 0),
    ("/Library/Fonts/Arial Unicode.ttf", 0),
]


def measure(path: str, index: int) -> dict | None:
    try:
        font = ImageFont.truetype(path, SAMPLE_SIZE, index=index)
    except OSError as exc:
        print(f"skip {path}#{index}: {exc}", file=sys.stderr)
        return None
    family, _ = font.getname()
    ascii_widths = [round(font.getlength(chr(cp)) / SAMPLE_SIZE, 4)
                    for cp in range(0x20, 0x7F)]
    def adv(char: str, default: float) -> float:
        try:
            value = font.getlength(char) / SAMPLE_SIZE
            return round(value, 4) if value > 0 else default
        except OSError:
            return default
    return {
        "family": family,
        "ascii": ascii_widths,
        "cjk": adv("中", 1.0),
        "fallback_wide": adv("Ｗ", 1.0),
        "fallback_narrow": adv("·", 0.35),
        "measured_from": f"{path}#{index}",
    }


def write_table(table: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = "".join(c.lower() if c.isalnum() else "-" for c in table["family"]).strip("-")
    out = OUT_DIR / f"{slug}.json"
    out.write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font")
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()

    jobs = SCAN_CANDIDATES if args.scan else [(args.font, args.index)]
    if not args.scan and not args.font:
        parser.error("--font or --scan required")
    written = []
    for path, index in jobs:
        if not Path(path).is_file():
            continue
        table = measure(path, index)
        if table:
            written.append(write_table(table))
            print(f"{table['family']}: cjk={table['cjk']} -> {written[-1].name}")
    if not written:
        print("no fonts measured", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
