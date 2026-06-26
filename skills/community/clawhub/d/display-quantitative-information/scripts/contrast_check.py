#!/usr/bin/env python3
"""Check WCAG-style contrast ratios for chart labels and annotations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def parse_hex(color: str) -> Tuple[float, float, float]:
    m = HEX_RE.match(color.strip())
    if not m:
        raise ValueError(f"invalid hex color: {color!r}; expected #RRGGBB")
    raw = m.group(1)
    return tuple(int(raw[i:i+2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[return-value]


def linearize(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(color: str) -> float:
    r, g, b = parse_hex(color)
    rl, gl, bl = linearize(r), linearize(g), linearize(b)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(foreground: str, background: str) -> float:
    l1, l2 = luminance(foreground), luminance(background)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def classify(ratio: float, large_text: bool = False) -> Dict[str, Any]:
    aa_threshold = 3.0 if large_text else 4.5
    aaa_threshold = 4.5 if large_text else 7.0
    return {"passes_AA": ratio >= aa_threshold, "passes_AAA": ratio >= aaa_threshold, "AA_threshold": aa_threshold, "AAA_threshold": aaa_threshold}


def check_pair(fg: str, bg: str, label: str = "pair", large_text: bool = False) -> Dict[str, Any]:
    ratio = contrast_ratio(fg, bg)
    return {"label": label, "foreground": fg, "background": bg, "contrast_ratio": ratio, "large_text": large_text, **classify(ratio, large_text)}


def load_pairs(path: Path) -> List[Dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Error: palette file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: invalid JSON in {path}: {exc}")
    if isinstance(data, dict) and "pairs" in data:
        pairs = data["pairs"]
    elif isinstance(data, list):
        pairs = data
    else:
        raise SystemExit("Error: palette JSON must be a list or an object with a 'pairs' list.")
    if not isinstance(pairs, list):
        raise SystemExit("Error: 'pairs' must be a list.")
    return pairs


def print_markdown(results: List[Dict[str, Any]]) -> None:
    for item in results:
        status = "PASS" if item["passes_AA"] else "FAIL"
        print(f"- {status} {item['label']}: {item['foreground']} on {item['background']} ratio {item['contrast_ratio']:.2f}:1 (AA threshold {item['AA_threshold']}:1)")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check color contrast for chart text, labels, and annotation colors.")
    parser.add_argument("--foreground", help="Foreground/text color as #RRGGBB.")
    parser.add_argument("--background", help="Background color as #RRGGBB.")
    parser.add_argument("--label", default="pair", help="Label for a single color pair.")
    parser.add_argument("--large-text", action="store_true", help="Use large-text contrast thresholds.")
    parser.add_argument("--palette", type=Path, help="JSON file with pairs: [{label, foreground, background, large_text}].")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    try:
        if args.palette:
            results = [check_pair(str(p["foreground"]), str(p["background"]), str(p.get("label", "pair")), bool(p.get("large_text", False))) for p in load_pairs(args.palette)]
        else:
            if not args.foreground or not args.background:
                parser.error("provide --foreground and --background, or --palette palette.json")
            results = [check_pair(args.foreground, args.background, args.label, args.large_text)]
    except (KeyError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps({"results": results}, indent=2))
    else:
        print_markdown(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
