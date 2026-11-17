# -*- coding: utf-8 -*-
"""采样 sample_ssc/P*.png 的尺寸与关键配色。"""
import os
from collections import Counter

from PIL import Image

# Source image dir: override with env var SAMPLE_SSC_SRC; default is a
# "sample_ssc" folder next to this script (no absolute author paths).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SAMPLE_SSC_SRC", os.path.join(SCRIPT_DIR, "sample_ssc"))
if not os.path.isdir(SRC):
    raise SystemExit("Source dir not found: %s (set SAMPLE_SSC_SRC)" % SRC)


def top_colors(im, n=14, q=8):
    small = im.convert("RGB").resize((160, 140))
    px = list(small.getdata())
    px = [(r // q * q, g // q * q, b // q * q) for r, g, b in px]
    return [("#%02X%02X%02X" % c, cnt) for c, cnt in Counter(px).most_common(n)]


def at(im, nx, ny):
    w, h = im.size
    x, y = min(w - 1, int(nx * w)), min(h - 1, int(ny * h))
    r, g, b = im.convert("RGB").getpixel((x, y))
    return "#%02X%02X%02X" % (r, g, b)


for name in ["P6", "P1", "P2", "P3", "P4", "P5"]:
    im = Image.open(os.path.join(SRC, name + ".png"))
    print("\n=== %s  size=%s ===" % (name, im.size))
    print("  top:", top_colors(im))
    print("  pts: TL=%s TR=%s C=%s BL=%s BR=%s" % (
        at(im, 0.03, 0.05), at(im, 0.97, 0.05), at(im, 0.5, 0.5),
        at(im, 0.03, 0.95), at(im, 0.97, 0.95)))
