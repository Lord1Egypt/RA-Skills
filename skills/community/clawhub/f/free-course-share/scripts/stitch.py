#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""截图拼图：两列或单行排列，不添加水印、推广文字或发布动作。"""
import argparse
import sys

from PIL import Image

BG_DARK = (23, 27, 34)
BG_LIGHT = (255, 255, 255)


def detect_bg(first_img):
    pixel = first_img.convert("RGB").getpixel((5, 5))
    return BG_DARK if sum(pixel) / 3 < 128 else BG_LIGHT


def two_col(paths, out, col_w, gap_v, gap_h, margin, bg):
    images = [Image.open(path).convert("RGB") for path in paths]
    count = len(images)
    left_count = (count + 1) // 2
    columns = [images[:left_count], images[left_count:]]
    scaled = []
    for column in columns:
        scaled.append(
            [
                image.resize(
                    (col_w, round(image.height * col_w / image.width)),
                    Image.LANCZOS,
                )
                for image in column
            ]
        )
    total_height = max(
        sum(image.height for image in column) + gap_v * (len(column) - 1)
        for column in scaled
        if column
    )
    canvas = Image.new(
        "RGB",
        (col_w * 2 + gap_h + margin * 2, total_height + margin * 2),
        bg,
    )
    x = margin
    for column in scaled:
        y = margin
        for image in column:
            canvas.paste(image, (x, y))
            y += image.height + gap_v
        x += col_w + gap_h
    canvas.save(out, optimize=True)
    print(f"OK {out}: {canvas.size[0]}x{canvas.size[1]}")


def one_row(paths, out, gap, margin, bg):
    images = [Image.open(path).convert("RGB") for path in paths]
    height = min(image.height for image in images)
    resized = [
        image.resize(
            (round(image.width * height / image.height), height), Image.LANCZOS
        )
        for image in images
    ]
    width = sum(image.width for image in resized) + gap * (len(resized) - 1)
    canvas = Image.new("RGB", (width + margin * 2, height + margin * 2), bg)
    x = margin
    for image in resized:
        canvas.paste(image, (x, margin))
        x += image.width + gap
    canvas.save(out, optimize=True)
    print(f"OK {out}: {canvas.size[0]}x{canvas.size[1]}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="截图拼图")
    parser.add_argument("mode", choices=["two-col", "one-row"])
    parser.add_argument("images", nargs="+", help="图片路径，顺序即排列顺序")
    parser.add_argument("-o", "--out", required=True)
    parser.add_argument("--col-w", type=int, default=880)
    parser.add_argument("--gap", type=int, default=14)
    parser.add_argument("--margin", type=int, default=30)
    parser.add_argument("--bg", default="auto", choices=["auto", "white", "dark"])
    args = parser.parse_args(argv)
    if len(args.images) == 1:
        raise SystemExit("只有一张图，无需拼接")
    if args.col_w <= 0 or args.gap < 0 or args.margin < 0:
        raise SystemExit("尺寸参数无效")
    probe = Image.open(args.images[0]).convert("RGB")
    bg = (
        detect_bg(probe)
        if args.bg == "auto"
        else BG_LIGHT
        if args.bg == "white"
        else BG_DARK
    )
    if args.mode == "two-col":
        two_col(args.images, args.out, args.col_w, args.gap, args.gap, args.margin, bg)
    else:
        one_row(args.images, args.out, args.gap, args.margin, bg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
