#!/usr/bin/env python3
"""Prepare a print-ready DTF production PNG from a decoration's real artwork.

Deterministic image manipulation only — **no model-generated pixels**. Takes the
actual decoration thumbnail, scales it (aspect-locked) to the largest size that
fits the decoration *location's* max print box, stamps the file at the target DPI
(300 by default), and writes a transparency-preserving PNG at exactly
``width_in * dpi`` × ``height_in * dpi`` pixels.

The print size in inches is derived from the art's own aspect ratio fitted into
the location max box (from Odoo ``decoration_location.max_width``/``max_height``,
falling back to the skill's ``references/location_dimensions.json``). Pass an
explicit ``--target-width-in`` / ``--target-height-in`` to override the fit.

Usage:
    python3 scripts/prepare_dtf_production.py \
        --input /tmp/logo.png \
        --max-width-in 13 --max-height-in 9 \
        [--dpi 300] \
        [--target-width-in 8 --target-height-in 5] \
        [--output /tmp/dtf_production.png]

Prints a JSON receipt with the actual print inches (feed these back to
``decoration_update_fields`` as size_width/size_height) and the output pixel size.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _bootstrap  # noqa: E402

_bootstrap.ensure(_bootstrap.IMAGING, _bootstrap.IMAGING_MODS)


def _fit_inches(src_w_px, src_h_px, max_w_in, max_h_in, tgt_w_in, tgt_h_in):
    """Return (width_in, height_in, fit_axis) preserving the art aspect ratio."""
    aspect = src_w_px / src_h_px  # width / height

    # Explicit target wins (still aspect-locked to the given width if both set
    # would distort — we honor width and derive height, or vice versa).
    if tgt_w_in and tgt_h_in:
        return round(tgt_w_in, 4), round(tgt_h_in, 4), "explicit"
    if tgt_w_in:
        return round(tgt_w_in, 4), round(tgt_w_in / aspect, 4), "explicit-width"
    if tgt_h_in:
        return round(tgt_h_in * aspect, 4), round(tgt_h_in, 4), "explicit-height"

    # Fit into whichever of the max dimensions are provided.
    if max_w_in and max_h_in:
        w_in = max_w_in
        h_in = w_in / aspect
        if h_in > max_h_in:
            h_in = max_h_in
            w_in = h_in * aspect
            axis = "height"
        else:
            axis = "width"
        return round(w_in, 4), round(h_in, 4), axis
    if max_w_in:
        return round(max_w_in, 4), round(max_w_in / aspect, 4), "width"
    if max_h_in:
        return round(max_h_in * aspect, 4), round(max_h_in, 4), "height"
    raise ValueError("Provide --max-width-in and/or --max-height-in "
                     "(or explicit --target-*-in).")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scale artwork to a location's print box and stamp it at target DPI")
    parser.add_argument("--input", required=True, help="Path to the source artwork")
    parser.add_argument("--max-width-in", type=float, default=0.0,
                        help="Location max print width in inches")
    parser.add_argument("--max-height-in", type=float, default=0.0,
                        help="Location max print height in inches")
    parser.add_argument("--target-width-in", type=float, default=0.0,
                        help="Explicit print width in inches (overrides fit)")
    parser.add_argument("--target-height-in", type=float, default=0.0,
                        help="Explicit print height in inches (overrides fit)")
    parser.add_argument("--dpi", type=int, default=300, help="Output DPI (default 300)")
    parser.add_argument("--output", default="", help="Output PNG path")
    args = parser.parse_args()

    from PIL import Image

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(input_path)
    # Preserve transparency; give everything an alpha channel to be safe.
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    src_w, src_h = img.size
    if src_w == 0 or src_h == 0:
        print("ERROR: source image has zero dimension", file=sys.stderr)
        sys.exit(2)

    try:
        w_in, h_in, axis = _fit_inches(
            src_w, src_h,
            args.max_width_in or 0.0, args.max_height_in or 0.0,
            args.target_width_in or 0.0, args.target_height_in or 0.0)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    out_w = max(1, int(round(w_in * args.dpi)))
    out_h = max(1, int(round(h_in * args.dpi)))
    resized = img.resize((out_w, out_h), Image.LANCZOS)

    output_path = Path(args.output) if args.output else (
        input_path.with_name(input_path.stem + "_dtf300.png"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    resized.save(output_path, format="PNG", dpi=(args.dpi, args.dpi))

    # Flag if the fitted print exceeds the max box (only possible via explicit
    # targets) so the caller can warn the operator.
    warnings = []
    if args.max_width_in and w_in > args.max_width_in + 1e-6:
        warnings.append(f"width {w_in}in exceeds location max {args.max_width_in}in")
    if args.max_height_in and h_in > args.max_height_in + 1e-6:
        warnings.append(f"height {h_in}in exceeds location max {args.max_height_in}in")

    print(json.dumps({
        "output": str(output_path),
        "source_px": [src_w, src_h],
        "print_inches": {"width": w_in, "height": h_in},
        "dpi": args.dpi,
        "output_px": [out_w, out_h],
        "max_box_in": [args.max_width_in or None, args.max_height_in or None],
        "fit_axis": axis,
        "warnings": warnings,
    }))


if __name__ == "__main__":
    main()
