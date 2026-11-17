#!/usr/bin/env python3
"""
qa_poster.py — Pixel-zone verification for canvas-exported posters.

Verifies: (1) PNG signature, (2) expected dimensions, (3) sampled pixel
colors at known coordinates (with tolerance for antialiasing).

Usage:
  # Coordinates in export pixels, exact dimension check:
  python3 qa_poster.py poster_4x.png --expect 3600x5092 \
      --sample 240:480:#000814 --sample 1800:400:#00b4d8

  # Coordinates in LOGICAL design units (W×H), auto-multiplied by scale:
  python3 qa_poster.py poster_4x.png --scale 4 --sample 60:120:#000814

  # Tolerance (0-255 per channel, default 12):
  python3 qa_poster.py poster.png --sample 60:120:#000814 --tol 20

Exit code 0 = all checks passed; 1 = any failure. Prints PASS/FAIL per check.
"""
import argparse
import sys


def parse_color(s: str):
    s = s.lstrip('#')
    if len(s) != 6:
        raise ValueError(f"Color must be RRGGBB, got: {s}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def parse_sample(s: str):
    x_y_color = s.split(':')
    if len(x_y_color) != 3:
        raise ValueError(f"Sample must be x:y:#RRGGBB, got: {s}")
    return int(x_y_color[0]), int(x_y_color[1]), parse_color(x_y_color[2])


def main():
    ap = argparse.ArgumentParser(description="Verify exported poster pixels")
    ap.add_argument("image", help="PNG file to verify")
    ap.add_argument("--expect", help="Expected dimensions, e.g. 3600x5092")
    ap.add_argument("--sample", action="append", default=[],
                    help="x:y:#RRGGBB (repeatable)")
    ap.add_argument("--scale", type=int, default=1,
                    help="Multiply sample coords by this (logical→export px)")
    ap.add_argument("--tol", type=int, default=12,
                    help="Per-channel tolerance, default 12")
    args = ap.parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("FAIL: PIL/Pillow not installed. Run: pip install Pillow")
        sys.exit(1)

    failures = 0

    # 1. PNG signature
    with open(args.image, "rb") as f:
        header = f.read(8)
    if header == b"\x89PNG\r\n\x1a\n":
        print(f"PASS  PNG signature: {args.image}")
    else:
        print(f"FAIL  PNG signature: bad header {header!r}")
        failures += 1

    # 2. Open + dimensions
    img = Image.open(args.image).convert("RGB")
    print(f"INFO  Actual size: {img.width}x{img.height}")
    if args.expect:
        ew, eh = (int(v) for v in args.expect.lower().split("x"))
        if (img.width, img.height) == (ew, eh):
            print(f"PASS  Dimensions match {ew}x{eh}")
        else:
            print(f"FAIL  Dimensions: expected {ew}x{eh}, got {img.width}x{img.height}")
            failures += 1

    # 3. Pixel samples
    for spec in args.sample:
        x, y, color = parse_sample(spec)
        x, y = x * args.scale, y * args.scale
        if not (0 <= x < img.width and 0 <= y < img.height):
            print(f"FAIL  ({x},{y}) outside image bounds")
            failures += 1
            continue
        actual = img.getpixel((x, y))
        diff = max(abs(a - b) for a, b in zip(actual, color))
        if diff <= args.tol:
            print(f"PASS  ({x},{y}) = rgb{actual} ≈ #{'%02x%02x%02x' % color} (diff {diff})")
        else:
            print(f"FAIL  ({x},{y}) = rgb{actual}, expected #{'%02x%02x%02x' % color} (diff {diff} > {args.tol})")
            failures += 1

    if failures:
        print(f"\n{failures} check(s) FAILED")
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
