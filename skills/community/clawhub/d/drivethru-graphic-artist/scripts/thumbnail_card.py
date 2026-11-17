#!/usr/bin/env python3
"""Composite artwork onto a neutral card so a DB thumbnail stays legible.

A production cutout (art on transparency) is the printer's truth, but it makes a
lousy thumbnail — white or light art vanishes against a white UI. This renders a
*human-facing* thumbnail by matting the art over a neutral card (a light-gray
fill or a checkerboard), padding it a little, and fitting it to a max box. The
transparent areas read as "garment shows here", so the thumbnail doubles as a
tiny print-proof. It never touches the cutout you send to production.

This is a convenience for the ``image`` (thumbnail) field, **not** a required
step — nothing else in the skill assumes thumbnails have been run through it.

Deterministic image manipulation only — no model-generated pixels.

Usage:
    python3 scripts/thumbnail_card.py --input cut.png --output thumb.png \
        [--bg gray|checker|'#RRGGBB'] [--max 512] [--pad 0.06]

Prints a JSON receipt (background, output size).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _bootstrap  # noqa: E402

_bootstrap.ensure(_bootstrap.IMAGING, _bootstrap.IMAGING_MODS)

from PIL import Image  # noqa: E402

_GRAY = (200, 200, 203)
_CHECK_A = (210, 210, 213)
_CHECK_B = (176, 176, 180)


def _hex_to_rgb(spec: str):
    s = spec.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    if len(s) != 6:
        raise ValueError(f"bad --bg '{spec}': use gray, checker, or '#RRGGBB'")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def _card(size, bg: str) -> Image.Image:
    w, h = size
    key = bg.strip().lower()
    if key == "gray":
        return Image.new("RGB", size, _GRAY)
    if key == "checker":
        tile = max(8, min(w, h) // 16)
        card = Image.new("RGB", size, _CHECK_A)
        b = Image.new("RGB", (tile, tile), _CHECK_B)
        for y in range(0, h, tile):
            for x in range(0, w, tile):
                if ((x // tile) + (y // tile)) % 2:
                    card.paste(b, (x, y))
        return card
    return Image.new("RGB", size, _hex_to_rgb(bg))


def make_thumbnail(input_path: Path, output_path: Path, bg: str, max_edge: int,
                   pad: float) -> dict:
    art = Image.open(input_path).convert("RGBA")

    # Fit the art into a padded box no larger than max_edge on its long side.
    box = max(1, int(max_edge))
    inner = max(1, int(round(box * (1.0 - 2.0 * pad))))
    a = art.copy()
    a.thumbnail((inner, inner), Image.LANCZOS)

    card = _card((box, box), bg).convert("RGBA")
    x = (box - a.width) // 2
    y = (box - a.height) // 2
    card.alpha_composite(a, dest=(x, y))

    out = card.convert("RGB")  # thumbnails are opaque by definition
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(output_path, format="PNG")
    return {
        "output": str(output_path),
        "background": bg,
        "size_px": [box, box],
        "art_px": [a.width, a.height],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Composite artwork onto a neutral card for a legible thumbnail")
    parser.add_argument("--input", required=True, help="Path to the artwork (ideally the cutout)")
    parser.add_argument("--output", required=True, help="Path to write the thumbnail PNG to")
    parser.add_argument("--bg", default="gray",
                        help="Card background: gray (default), checker, or '#RRGGBB'")
    parser.add_argument("--max", type=int, default=512, help="Max output edge in px (default 512)")
    parser.add_argument("--pad", type=float, default=0.06,
                        help="Padding as a fraction of the box on each side (default 0.06)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    if not 0.0 <= args.pad < 0.5:
        print("ERROR: --pad must be in [0, 0.5)", file=sys.stderr)
        sys.exit(1)

    try:
        receipt = make_thumbnail(input_path, Path(args.output), args.bg, args.max, args.pad)
    except Exception as e:
        print(f"ERROR: thumbnail failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
