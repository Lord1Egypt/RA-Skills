#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pad an image with a blank margin so an AI editor's watermark lands in the
margin, not on the content. Pair with crop_margin.py to drop it afterward.

Self-developed technique: "先多生成留白再裁掉" — add whitespace before the AI
edit, crop it off after, watermark gone deterministically.
"""
import argparse
import sys
from PIL import Image


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


def add_margin(src, dst, percent, side, color):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    c = parse_color(color)
    mw = int(w * percent / 100) if side in ("left", "right", "uniform") else 0
    mh = int(h * percent / 100) if side in ("top", "bottom", "uniform") else 0
    if side == "uniform":
        canvas = Image.new("RGB", (w + 2 * mw, h + 2 * mh), c)
        canvas.paste(im, (mw, mh))
    elif side == "bottom":
        canvas = Image.new("RGB", (w, h + mh), c)
        canvas.paste(im, (0, 0))
    elif side == "top":
        canvas = Image.new("RGB", (w, h + mh), c)
        canvas.paste(im, (0, mh))
    elif side == "left":
        canvas = Image.new("RGB", (w + mw, h), c)
        canvas.paste(im, (mw, 0))
    elif side == "right":
        canvas = Image.new("RGB", (w + mw, h), c)
        canvas.paste(im, (0, 0))
    else:
        raise SystemExit("bad --side: %s" % side)
    canvas.save(dst)
    print("padded  : %s -> %s  (%dx%d, +%d/%d margin, %s)" %
          (src, dst, canvas.width, canvas.height, mw, mh, side))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--percent", type=float, default=10)
    ap.add_argument("--side", default="bottom",
                    choices=["bottom", "top", "left", "right", "uniform"])
    ap.add_argument("--color", default="white")
    a = ap.parse_args()
    add_margin(a.src, a.dst, a.percent, a.side, a.color)


if __name__ == "__main__":
    main()
