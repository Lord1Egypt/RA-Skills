#!/usr/bin/env python3
"""Detect the garment's bounding box inside a blank product photo.

Runs rembg on the blank, finds the tight bounding box of non-transparent
pixels, and prints the result as JSON. If rembg can't isolate a
foreground (e.g. the input is a flat solid color or already transparent
everywhere), the script falls back to the image's full bounding box so
the mockup pipeline always has something to anchor to.

Usage:
    python3 scripts/detect_garment_bbox.py /path/to/blank.png
    python3 scripts/detect_garment_bbox.py /path/to/blank.png --model u2net
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path


_MIN_FRACTION = 0.05  # reject bbox if it covers less than this fraction of the image area


def detect_bbox(image_path: Path, model: str = "u2net") -> dict:
    """Return ``{"left", "top", "width", "height", "source"}`` for the garment.

    ``source`` is ``"rembg"`` if the segmentation produced a believable bbox,
    otherwise ``"full_image"`` when we fell back to the whole frame.
    """
    from PIL import Image
    from rembg import new_session, remove

    with Image.open(image_path) as img:
        full_w, full_h = img.size
        full_bbox = {
            "left": 0,
            "top": 0,
            "width": full_w,
            "height": full_h,
            "source": "full_image",
        }

        session = new_session(model)
        with image_path.open("rb") as f:
            data = f.read()
        try:
            cut = remove(data, session=session)
        except Exception:
            return full_bbox

        cut_img = Image.open(io.BytesIO(cut)).convert("RGBA")
        alpha = cut_img.getchannel("A")
        bbox = alpha.getbbox()
        if bbox is None:
            return full_bbox

        left, top, right, bottom = bbox
        width = right - left
        height = bottom - top
        if full_w * full_h == 0:
            return full_bbox
        coverage = (width * height) / float(full_w * full_h)
        if coverage < _MIN_FRACTION:
            return full_bbox

        return {
            "left": int(left),
            "top": int(top),
            "width": int(width),
            "height": int(height),
            "source": "rembg",
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect the garment bbox inside a blank image")
    parser.add_argument("image", help="Path to the blank product image")
    parser.add_argument(
        "--model",
        default="u2net",
        help="rembg model name (default: u2net; downloaded + cached on first use)",
    )
    args = parser.parse_args()

    path = Path(args.image)
    if not path.exists():
        print(f"ERROR: image not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = detect_bbox(path, model=args.model)
    except Exception as e:
        print(f"ERROR: bbox detection failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
