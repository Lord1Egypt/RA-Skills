#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detect the uniform blank margin (added by add_margin.py) and crop it off,
taking the AI editor's watermark (which landed in that margin) with it.

Pure Pillow. Deterministic — no ML, no inpainting.

The margin color is KNOWN (you chose it in add_margin.py), so we crop against
that explicit color rather than guessing from a corner. A margin row that holds
a watermark line is still ~95% the margin color, so it still gets cropped.
"""
import argparse
import sys
from PIL import Image


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def parse_color(s):
    s = s.strip().lower()
    if s in ("white", "w"):
        return (255, 255, 255)
    if s in ("black", "b"):
        return (0, 0, 0)
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    raise SystemExit("bad --color: %s" % s)


def detect(im, color, tol, min_frac, step, max_percent):
    w, h = im.size
    px = im.load()

    def col_is_margin(x):
        n = tot = 0
        for y in range(0, h, step):
            tot += 1
            if close(px[x, y], color, tol):
                n += 1
        return tot and (n / tot) >= min_frac

    def row_is_margin(y):
        n = tot = 0
        for x in range(0, w, step):
            tot += 1
            if close(px[x, y], color, tol):
                n += 1
        return tot and (n / tot) >= min_frac

    left = 0
    for x in range(w):
        if col_is_margin(x):
            left = x + 1
        else:
            break
    right = w
    for x in range(w - 1, -1, -1):
        if col_is_margin(x):
            right = x
        else:
            break
    top = 0
    for y in range(h):
        if row_is_margin(y):
            top = y + 1
        else:
            break
    bottom = h
    for y in range(h - 1, -1, -1):
        if row_is_margin(y):
            bottom = y
        else:
            break

    max_w = int(w * max_percent / 100)
    max_h = int(h * max_percent / 100)
    left = min(left, max_w)
    right = max(right, w - max_w)
    top = min(top, max_h)
    bottom = max(bottom, h - max_h)
    return left, top, right, bottom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--color", default="white",
                    help="margin color used in add_margin.py (white/black/#rrggbb)")
    ap.add_argument("--tol", type=int, default=12)
    ap.add_argument("--min-frac", type=float, default=0.88,
                    help="a row/col counts as margin if this fraction matches --color")
    ap.add_argument("--max-percent", type=float, default=30,
                    help="safety cap: never crop more than this %% per side")
    ap.add_argument("--fallback", type=float, default=0,
                    help="if detected border < this %% per side, crop fixed bottom %% instead")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--step", type=int, default=3)
    a = ap.parse_args()
    color = parse_color(a.color)
    im = Image.open(a.src).convert("RGB")
    w, h = im.size
    left, top, right, bottom = detect(im, color, a.tol, a.min_frac, a.step, a.max_percent)
    bl = left
    bt = h - bottom
    if a.fallback and (bl < w * a.fallback / 100 or bt < h * a.fallback / 100):
        fb = int(h * a.fallback / 100)
        left, top, right, bottom = 0, 0, w, h - fb
        bl, bt = 0, fb
    crop = (left, top, right, bottom)
    if a.report or not a.dst:
        print("detected border -> left:%d top:%d right:%d bottom:%d (of %dx%d, color=%s)" %
              (left, top, w - right, h - bottom, w, h, a.color))
        print("content crop box: %s" % (crop,))
        if a.report:
            return 0
        print("no dst given -> nothing written (use --report to inspect)")
        return 0
    out = im.crop(crop)
    out.save(a.dst)
    print("cropped : %s -> %s  (%dx%d, removed L%d T%d R%d B%d)" %
          (a.src, a.dst, out.width, out.height, left, top, w - right, h - bottom))
    return 0


if __name__ == "__main__":
    sys.exit(main())
