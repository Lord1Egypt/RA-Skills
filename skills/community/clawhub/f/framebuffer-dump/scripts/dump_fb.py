#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image


def main() -> int:
    p = argparse.ArgumentParser(description="Convert raw RGB888 framebuffer dump to PNG")
    p.add_argument("--in", dest="input", required=True, help="Input .bin path")
    p.add_argument("--out", dest="output", required=True, help="Output .png path")
    p.add_argument("--width", type=int, default=604)
    p.add_argument("--height", type=int, default=1024)
    p.add_argument("--stride", type=int, default=3, help="Bytes per pixel (RGB888=3)")
    args = p.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        raise SystemExit(f"input not found: {in_path}")

    need = args.width * args.height * args.stride
    data = in_path.read_bytes()
    if len(data) < need:
        raise SystemExit(f"input too small: got {len(data)} bytes, need >= {need}")

    raw = data[:need]
    img = Image.frombytes("RGB", (args.width, args.height), raw, "raw", "RGB")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
