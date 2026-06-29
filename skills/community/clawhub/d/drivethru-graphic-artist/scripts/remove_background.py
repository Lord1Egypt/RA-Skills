#!/usr/bin/env python3
"""Strip the background from an image using rembg (U²-Net segmentation).

Used to clean decoration images before composing them onto a blank.
Discriminative segmentation only — no generative model is involved.

Usage:
    python3 scripts/remove_background.py \
        --input /tmp/logo.jpg --output /tmp/logo.png

If the input is already RGBA with meaningful transparency (i.e. at
least one non-opaque pixel), the file is copied through unchanged and
the script prints ``{"skipped": true, ...}`` to stdout.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def _has_transparency(path: Path) -> bool:
    from PIL import Image

    with Image.open(path) as img:
        if img.mode not in ("RGBA", "LA"):
            return False
        alpha = img.getchannel("A")
        return alpha.getextrema()[0] < 255


def _remove_background(input_path: Path, output_path: Path, model: str) -> None:
    from rembg import new_session, remove

    session = new_session(model)
    with input_path.open("rb") as f:
        data = f.read()
    result = remove(data, session=session)
    output_path.write_bytes(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove the background from an image")
    parser.add_argument("--input", required=True, help="Path to the source image")
    parser.add_argument("--output", required=True, help="Path to write the RGBA PNG to")
    parser.add_argument(
        "--model",
        default="u2net",
        help="rembg model name (default: u2net; downloaded + cached on first use)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run rembg even if the input already has transparency",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not args.force and _has_transparency(input_path):
        # Copy through so callers can always treat --output as the RGBA result.
        if input_path.resolve() != output_path.resolve():
            shutil.copyfile(input_path, output_path)
        print(json.dumps({"skipped": True, "reason": "input already has alpha", "output": str(output_path)}))
        return

    try:
        _remove_background(input_path, output_path, args.model)
    except Exception as e:
        print(f"ERROR: background removal failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps({"skipped": False, "model": args.model, "output": str(output_path)}))


if __name__ == "__main__":
    main()
