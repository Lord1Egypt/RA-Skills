#!/usr/bin/env python3
"""Extract the dominant colors from artwork as ``#RRGGBB`` values + coverage.

Deterministic (Pillow median-cut quantization) — used to populate a DTF
decoration's color list. Transparent pixels are ignored; near-white pixels can
optionally be dropped as background. The output hex colors are fed to the
``decoration_match_colors`` MCP tool, which maps each to the nearest PMS /
``color`` library record (CIEDE2000) server-side — so PMS matching stays in
Odoo where the color library and the approximate PANTONE table live.

Usage:
    python3 scripts/extract_colors.py \
        --input /tmp/logo.png \
        [--max-colors 6] [--min-coverage 0.02] [--ignore-white]

Prints JSON: {colors: [{rgb_hex, coverage_pct}], ...} sorted by coverage desc.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _bootstrap  # noqa: E402

_bootstrap.ensure(_bootstrap.IMAGING, _bootstrap.IMAGING_MODS)

_SAMPLE_MAX = 200  # downscale longest edge to this before sampling


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract dominant colors from an image")
    parser.add_argument("--input", required=True, help="Path to the artwork")
    parser.add_argument("--max-colors", type=int, default=6,
                        help="Max distinct colors to return (default 6)")
    parser.add_argument("--min-coverage", type=float, default=0.02,
                        help="Drop colors below this fraction of sampled pixels (default 0.02)")
    parser.add_argument("--ignore-white", action="store_true",
                        help="Treat near-white pixels as background and exclude them")
    parser.add_argument("--alpha-threshold", type=int, default=128,
                        help="Ignore pixels with alpha below this (default 128)")
    args = parser.parse_args()

    from PIL import Image

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(input_path).convert("RGBA")
    # Downscale for a fast, stable sample.
    long_edge = max(img.size)
    if long_edge > _SAMPLE_MAX:
        scale = _SAMPLE_MAX / long_edge
        img = img.resize((max(1, int(img.width * scale)),
                          max(1, int(img.height * scale))), Image.LANCZOS)

    opaque = []
    for r, g, b, a in img.getdata():
        if a < args.alpha_threshold:
            continue
        if args.ignore_white and min(r, g, b) >= 245:
            continue
        opaque.append((r, g, b))

    # Fall back to including near-white if filtering removed everything.
    if not opaque and args.ignore_white:
        opaque = [(r, g, b) for r, g, b, a in img.getdata() if a >= args.alpha_threshold]

    if not opaque:
        print(json.dumps({"input": str(input_path), "total_sampled": 0, "colors": [],
                          "note": "no opaque pixels found"}))
        return

    # Median-cut quantize the collected pixels.
    strip = Image.new("RGB", (len(opaque), 1))
    strip.putdata(opaque)
    n = max(1, min(args.max_colors, 256))
    quant = strip.quantize(colors=n, method=Image.MEDIANCUT)
    palette = quant.getpalette()
    total = len(opaque)

    colors = []
    for count, idx in quant.getcolors() or []:
        r, g, b = palette[idx * 3: idx * 3 + 3]
        coverage = count / total
        if coverage < args.min_coverage:
            continue
        colors.append({
            "rgb_hex": "#{:02X}{:02X}{:02X}".format(r, g, b),
            "coverage_pct": round(coverage * 100, 2),
        })
    colors.sort(key=lambda c: c["coverage_pct"], reverse=True)

    print(json.dumps({
        "input": str(input_path),
        "total_sampled": total,
        "max_colors": args.max_colors,
        "min_coverage": args.min_coverage,
        "colors": colors,
    }))


if __name__ == "__main__":
    main()
