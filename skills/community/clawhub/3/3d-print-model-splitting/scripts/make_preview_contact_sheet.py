#!/usr/bin/env python3
"""Create a simple labeled contact sheet from preview PNGs.

Usage:
  python3 make_preview_contact_sheet.py \
    --output /path/to/contact_sheet.png \
    --image /path/to/front.png --label 正面预览 \
    --image /path/to/iso.png --label 透视预览

Notes:
- Requires Pillow.
- Designed for OpenClaw/Bambu/chat handoff previews.
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    p.add_argument('--image', action='append', required=True)
    p.add_argument('--label', action='append', required=True)
    p.add_argument('--thumb', type=int, default=700)
    p.add_argument('--columns', type=int, default=2)
    p.add_argument('--pad', type=int, default=20)
    p.add_argument('--label-height', type=int, default=54)
    p.add_argument('--bg', default='32,34,38')
    return p.parse_args()


def load_font(size):
    for fp in [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    ]:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            pass
    return ImageFont.load_default()


def main():
    args = parse_args()
    if len(args.image) != len(args.label):
        raise SystemExit('--image and --label counts must match')
    bg = tuple(int(x) for x in args.bg.split(','))
    items = list(zip(args.image, args.label))
    cols = max(1, args.columns)
    rows = (len(items) + cols - 1) // cols
    w = args.thumb * cols + args.pad * (cols + 1)
    h = (args.thumb + args.label_height) * rows + args.pad * (rows + 1)
    canvas = Image.new('RGB', (w, h), bg)
    draw = ImageDraw.Draw(canvas)
    font = load_font(30)

    for idx, (path, label) in enumerate(items):
        img = Image.open(path).convert('RGB')
        img.thumbnail((args.thumb, args.thumb), Image.LANCZOS)
        col = idx % cols
        row = idx // cols
        x = args.pad + col * (args.thumb + args.pad)
        y = args.pad + row * (args.thumb + args.label_height + args.pad)
        canvas.paste(img, (x + (args.thumb - img.width) // 2, y + (args.thumb - img.height) // 2))
        bbox = draw.textbbox((0, 0), label, font=font)
        tx = x + (args.thumb - (bbox[2] - bbox[0])) // 2
        ty = y + args.thumb + 8
        draw.text((tx, ty), label, fill=(245, 245, 245), font=font)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    canvas.save(args.output, quality=95)
    print(args.output)


if __name__ == '__main__':
    main()
