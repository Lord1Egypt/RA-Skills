#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3:4 竖版封面生成器。

本脚本不包含固定账号、水印、推广或发布动作。CTA 仅在调用者显式传入
--cta 时绘制，默认关闭。
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
THEMES = {
    "dark": {
        "bg": (23, 27, 34),
        "card": (30, 36, 47),
        "line": (52, 60, 76),
        "txt": (255, 255, 255),
        "gray": (168, 176, 192),
        "yellow": (255, 201, 60),
        "blue": (79, 140, 255),
        "orange": (255, 159, 69),
        "warnbg": (51, 38, 20),
        "warn_txt": (226, 205, 176),
        "warn_icon": (35, 28, 18),
    },
    "light": {
        "bg": (255, 255, 255),
        "card": (242, 244, 248),
        "line": (217, 222, 232),
        "txt": (26, 34, 51),
        "gray": (107, 118, 136),
        "yellow": (228, 148, 10),
        "blue": (47, 107, 255),
        "orange": (219, 84, 12),
        "warnbg": (255, 244, 229),
        "warn_txt": (166, 92, 33),
        "warn_icon": (255, 255, 255),
    },
}
BADGE_FILL = {
    "blue": "blue",
    "yellow": "yellow",
    "orange": "orange",
    "red": (231, 76, 60),
    "gray": None,
}
FONT_SETS = [
    (
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        2,
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        0,
    ),
    (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        2,
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        2,
    ),
    (
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
        2,
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        2,
    ),
    ("C:/Windows/Fonts/msyhbd.ttc", 0, "C:/Windows/Fonts/msyh.ttc", 0),
]


def _pick_fonts():
    for bold_path, bold_index, regular_path, regular_index in FONT_SETS:
        if os.path.exists(bold_path) and os.path.exists(regular_path):
            return bold_path, bold_index, regular_path, regular_index
    raise SystemExit("未找到可用中文字体")


_BPATH, _BIDX, _RPATH, _RIDX = _pick_fonts()


def f_bold(size):
    return ImageFont.truetype(_BPATH, size, index=_BIDX)


def f_reg(size):
    return ImageFont.truetype(_RPATH, size, index=_RIDX)


def text_width(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def center(draw, y, text, font, fill, cx=W // 2):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text(
        (cx - (box[2] - box[0]) / 2 - box[0], y), text, font=font, fill=fill
    )


def pill(draw, cx, cy, text, font, pad_x, text_fill, bg, outline=None):
    box = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = box[2] - box[0], box[3] - box[1]
    width, height = text_w + pad_x * 2, text_h + 16
    x0, y0 = cx - width / 2, cy - height / 2
    if bg:
        draw.rounded_rectangle(
            [x0, y0, x0 + width, y0 + height], radius=height / 2, fill=bg
        )
    if outline:
        draw.rounded_rectangle(
            [x0, y0, x0 + width, y0 + height],
            radius=height / 2,
            outline=outline,
            width=2,
        )
    draw.text(
        (x0 + pad_x - box[0], cy - text_h / 2 - box[1] - 2),
        text,
        font=font,
        fill=text_fill,
    )
    return width


def parse_badge(value, default_color):
    parts = value.split("|")
    return parts[0], parts[1] if len(parts) > 1 else default_color


def compute_body_layout(images, mode, col_w, pad_x, gap):
    available_width = W - pad_x * 2
    if mode == "single":
        image = images[0]
        width = col_w or available_width
        height = round(image.height * width / image.width)
        return [[image.resize((width, height), Image.LANCZOS)]], height
    left_count = (len(images) + 1) // 2
    columns = [images[:left_count], images[left_count:]]
    col_w = col_w or (available_width - gap) // 2
    scaled = [
        [
            image.resize(
                (col_w, round(image.height * col_w / image.width)), Image.LANCZOS
            )
            for image in column
        ]
        for column in columns
    ]
    body_height = max(
        sum(image.height for image in column) + gap * (len(column) - 1)
        for column in scaled
        if column
    )
    return scaled, body_height


def main(argv=None):
    parser = argparse.ArgumentParser(description="3:4 竖版封面生成器")
    parser.add_argument("--out", required=True)
    parser.add_argument("--theme", default="dark", choices=["dark", "light"])
    parser.add_argument("--top-badge")
    parser.add_argument("--badges", nargs="*", default=[])
    parser.add_argument("--title", default="")
    parser.add_argument("--sub", default="")
    parser.add_argument("--body", nargs="*", default=[])
    parser.add_argument("--points", nargs="+", default=[])
    parser.add_argument("--warn", nargs="*", default=[])
    parser.add_argument(
        "--cta",
        default="",
        help="可选推广/引导语；默认关闭，仅在明确确认具体文案后传入",
    )
    parser.add_argument("--pad-x", type=int, default=28)
    parser.add_argument("--gap", type=int, default=14)
    parser.add_argument("--col-w", type=int, default=None)
    args = parser.parse_args(argv)
    if args.pad_x < 0 or args.gap < 0 or (args.col_w is not None and args.col_w <= 0):
        raise SystemExit("尺寸参数无效")

    theme = THEMES[args.theme]
    image = Image.new("RGB", (W, H), theme["bg"])
    draw = ImageDraw.Draw(image)
    y = 56
    badges = []
    if args.top_badge:
        badges.append(parse_badge(args.top_badge, "blue"))
    badges.extend(parse_badge(value, "gray") for value in args.badges)
    if badges:
        font = f_bold(26)
        widths = [text_width(draw, text, font) + 44 for text, _ in badges]
        cx = (W - sum(widths) - 14 * (len(widths) - 1)) / 2
        for (text, color_key), width in zip(badges, widths):
            key = BADGE_FILL.get(color_key)
            fill = theme.get(key) if isinstance(key, str) else key
            if color_key == "gray":
                color = theme["gray"] if args.theme == "dark" else theme["txt"]
                pill(
                    draw,
                    cx + width / 2,
                    y + 26,
                    text,
                    font,
                    22,
                    color,
                    theme["card"],
                    theme["line"],
                )
            else:
                pill(
                    draw,
                    cx + width / 2,
                    y + 26,
                    text,
                    font,
                    22,
                    (255, 255, 255),
                    fill,
                )
            cx += width + 14
        y += 84
    if args.title:
        center(draw, y, args.title, f_bold(62), theme["txt"])
        y += 108
    if args.sub:
        center(draw, y, args.sub, f_reg(30), theme["gray"])
        y += 62

    available_width = W - args.pad_x * 2
    non_body = y + 60
    if args.points:
        non_body += 158
    if args.warn:
        non_body += 138
    if args.cta:
        non_body += 46
    budget = H - non_body
    body_images = [Image.open(path).convert("RGB") for path in args.body]
    if body_images:
        mode = "single" if len(body_images) == 1 else "multi"
        col_w = args.col_w if mode == "multi" else available_width
        scaled, body_height = compute_body_layout(
            body_images, mode, col_w, args.pad_x, args.gap
        )
        if body_height > budget:
            ratio = budget / body_height
            col_w = max(200, int((col_w or available_width) * ratio))
            scaled, body_height = compute_body_layout(
                body_images, mode, col_w, args.pad_x, args.gap
            )
        if mode == "single":
            body = scaled[0][0]
            image.paste(body, ((W - body.width) // 2, y))
        else:
            x = args.pad_x
            for column in scaled:
                yy = y
                for body in column:
                    image.paste(body, (x, yy))
                    yy += body.height + args.gap
                x += column[0].width + args.gap
        y += body_height + 34

    if args.points:
        points = [
            (value.split("|")[0], value.split("|")[1] if "|" in value else "")
            for value in args.points
        ]
        card_width = (
            available_width - args.gap * (len(points) - 1)
        ) // len(points)
        for index, (big, small) in enumerate(points):
            x0 = args.pad_x + index * (card_width + args.gap)
            draw.rounded_rectangle(
                [x0, y, x0 + card_width, y + 128],
                radius=18,
                fill=theme["card"],
                outline=theme["line"],
            )
            center(draw, y + 14, big, f_bold(46), theme["yellow"], x0 + card_width // 2)
            if small:
                center(draw, y + 84, small, f_reg(24), theme["gray"], x0 + card_width // 2)
        y += 158
    if args.warn:
        lines = args.warn[:2]
        draw.rounded_rectangle(
            [args.pad_x, y, W - args.pad_x, y + 108],
            radius=18,
            fill=theme["warnbg"],
            outline=theme["orange"],
        )
        draw.text(
            (args.pad_x + 32, y + 18),
            lines[0],
            font=f_bold(28),
            fill=theme["orange"],
        )
        if len(lines) > 1:
            draw.text(
                (args.pad_x + 32, y + 60),
                lines[1],
                font=f_reg(26),
                fill=theme["warn_txt"],
            )
        y += 138
    if args.cta:
        center(draw, y, args.cta, f_reg(27), theme["gray"])
    image.save(args.out, optimize=True)
    print(f"OK {args.out}: {image.size} theme={args.theme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
