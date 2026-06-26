#!/usr/bin/env python3
"""Compute Tufte-style lie factor for a quantitative display."""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any, Dict, Optional


def pct_change(before: float, after: float) -> float:
    if math.isclose(before, 0.0):
        raise ValueError("before value is zero; percentage change is undefined")
    return (after - before) / abs(before) * 100.0


def classify(lf: Optional[float]) -> str:
    if lf is None:
        return "not_computed"
    if lf < 0:
        return "severe_reverse_direction"
    if 0.95 <= lf <= 1.05:
        return "proportional"
    if 0.67 <= lf < 0.95 or 1.05 < lf <= 1.5:
        return "moderate_distortion"
    return "severe_distortion"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute lie factor: visual effect divided by data effect.",
        epilog=(
            "Examples:\n"
            "  python3 scripts/lie_factor.py --data-effect 20 --visual-effect 60\n"
            "  python3 scripts/lie_factor.py --data-before 100 --data-after 120 "
            "--visual-before 10 --visual-after 16 --format markdown"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--data-effect", type=float, help="Numerical percentage change in the data.")
    parser.add_argument("--visual-effect", type=float, help="Percentage change in the perceived visual dimension.")
    parser.add_argument("--data-before", type=float, help="Initial data value.")
    parser.add_argument("--data-after", type=float, help="Final data value.")
    parser.add_argument("--visual-before", type=float, help="Initial visual dimension, such as bar length, area, or symbol height.")
    parser.add_argument("--visual-after", type=float, help="Final visual dimension.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    try:
        data_effect = args.data_effect
        visual_effect = args.visual_effect
        if data_effect is None:
            if args.data_before is None or args.data_after is None:
                parser.error("provide --data-effect or both --data-before and --data-after")
            data_effect = pct_change(args.data_before, args.data_after)
        if visual_effect is None:
            if args.visual_before is None or args.visual_after is None:
                parser.error("provide --visual-effect or both --visual-before and --visual-after")
            visual_effect = pct_change(args.visual_before, args.visual_after)
        if math.isclose(data_effect, 0.0):
            raise ValueError("data effect is zero; lie factor is undefined")
        lie_factor = visual_effect / data_effect
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    result: Dict[str, Any] = {
        "data_effect_percent": data_effect,
        "visual_effect_percent": visual_effect,
        "lie_factor": lie_factor,
        "classification": classify(lie_factor),
        "interpretation": "values near 1 are proportional; values far from 1 suggest visual distortion",
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Lie factor: {lie_factor:.3g}")
        print(f"Data effect: {data_effect:.3g}%")
        print(f"Visual effect: {visual_effect:.3g}%")
        print(f"Classification: {result['classification']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
