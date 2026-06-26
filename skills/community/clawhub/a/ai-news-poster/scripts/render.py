#!/usr/bin/env python3
"""Render a fixed 5-item AI news poster to PNG.

Usage:
  python scripts/render.py examples/input.sample.json output.png
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: python -m pip install pillow"
    ) from exc


WIDTH = 1080
HEIGHT = 1350
MARGIN = 64
CARD_GAP = 16

BG_TOP = (112, 166, 230)
BG_BOTTOM = (96, 195, 240)
WHITE = (255, 255, 255)
TITLE_MAIN = (28, 70, 145)
TITLE_SUB = (48, 93, 171)
HEADLINE = (39, 81, 152)
SUMMARY = (49, 90, 163)
META = (72, 121, 192)
FOOTER = (221, 237, 255)
ACCENT = (109, 191, 242)
CARD_BORDER = (196, 224, 255, 255)
CARD_FILL = (250, 252, 255, 244)


@dataclass(frozen=True)
class NewsItem:
    headline: str
    summary: str
    source: str
    tag: str


@dataclass(frozen=True)
class PosterData:
    date: str
    title: str
    news: list[NewsItem]
    footer: str
    brand: str


def _safe_str(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"'{field}' must be a string")
    text = value.strip()
    if not text:
        raise ValueError(f"'{field}' cannot be empty")
    return text


def load_input(path: Path) -> PosterData:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Input root must be an object")

    date = _safe_str(raw.get("date"), "date")
    title = _safe_str(raw.get("title"), "title")
    footer = _safe_str(raw.get("footer"), "footer")
    brand = _safe_str(raw.get("brand"), "brand")

    items = raw.get("news")
    if not isinstance(items, list):
        raise ValueError("'news' must be a list")
    if len(items) != 5:
        raise ValueError("'news' must contain exactly 5 items")

    news: list[NewsItem] = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"news[{idx}] must be an object")
        news.append(
            NewsItem(
                headline=_safe_str(item.get("headline"), f"news[{idx}].headline"),
                summary=_safe_str(item.get("summary"), f"news[{idx}].summary"),
                source=_safe_str(item.get("source"), f"news[{idx}].source"),
                tag=_safe_str(item.get("tag"), f"news[{idx}].tag"),
            )
        )

    return PosterData(date=date, title=title, news=news, footer=footer, brand=brand)


def pick_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for font_path in candidates:
        try:
            return ImageFont.truetype(font_path, size=size, index=0)
        except OSError:
            continue
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
    return draw.textlength(text, font=font)


def truncate_to_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> str:
    if text_width(draw, text, font) <= max_width:
        return text
    ellipsis = "..."
    low, high = 0, len(text)
    while low < high:
        mid = (low + high + 1) // 2
        trial = text[:mid].rstrip() + ellipsis
        if text_width(draw, trial, font) <= max_width:
            low = mid
        else:
            high = mid - 1
    return text[:low].rstrip() + ellipsis


def make_gradient(width: int, height: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    image = Image.new("RGB", (width, height), top)
    px = image.load()
    for y in range(height):
        t = y / (height - 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(width):
            px[x, y] = (r, g, b)
    return image


def draw_tech_background(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    # Soft grid and glow to mimic a light-tech poster style.
    for x in range(0, width, 54):
        draw.line((x, 0, x, height), fill=(180, 224, 255, 22), width=1)
    for y in range(0, height, 54):
        draw.line((0, y, width, y), fill=(180, 224, 255, 18), width=1)

    draw.ellipse((-180, -220, 460, 380), fill=(255, 255, 255, 64))
    draw.ellipse((width - 420, -180, width + 120, 320), fill=(175, 230, 255, 75))
    draw.ellipse((width - 260, height - 260, width + 120, height + 120), fill=(120, 210, 255, 54))

    # Decorative tiny stars.
    for x, y in ((64, 210), (180, 1150), (980, 240), (950, 1120), (820, 84)):
        draw.line((x - 6, y, x + 6, y), fill=(230, 245, 255, 180), width=2)
        draw.line((x, y - 6, x, y + 6), fill=(230, 245, 255, 180), width=2)


def wrap_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
    max_lines: int,
) -> list[str]:
    if not text:
        return [""]
    lines: list[str] = []
    current = ""
    for ch in text:
        trial = current + ch
        if text_width(draw, trial, font) <= max_width:
            current = trial
            continue
        if current:
            lines.append(current)
        current = ch
        if len(lines) >= max_lines:
            break
    if len(lines) < max_lines and current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    if lines and len(lines) == max_lines and text_width(draw, lines[-1], font) > max_width:
        lines[-1] = truncate_to_width(draw, lines[-1], font, max_width)
    if len(lines) == max_lines and "".join(lines) != text:
        lines[-1] = truncate_to_width(draw, lines[-1] + "...", font, max_width)
    return lines


def draw_section_header(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, text: str, font: ImageFont.ImageFont) -> None:
    draw.rounded_rectangle((x, y, x + w, y + 46), radius=12, fill=(97, 183, 238, 255))
    tw = text_width(draw, text, font)
    draw.text((x + (w - tw) / 2, y + 8), text, font=font, fill=(230, 248, 255))


def draw_news_card(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    idx: int,
    item: NewsItem,
    number_font: ImageFont.ImageFont,
    headline_font: ImageFont.ImageFont,
    summary_font: ImageFont.ImageFont,
    meta_font: ImageFont.ImageFont,
) -> None:
    draw.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=CARD_FILL, outline=CARD_BORDER, width=2)
    draw.text((x + 26, y + 20), f"{idx:02d}", font=number_font, fill=(44, 95, 170))

    text_x = x + 110
    text_w = w - 134
    headline_lines = wrap_lines(draw, item.headline, headline_font, text_w, max_lines=2)
    summary_lines = wrap_lines(draw, item.summary, summary_font, text_w, max_lines=3)
    meta_line = truncate_to_width(draw, f"#{item.tag} | {item.source}", meta_font, text_w)

    ty = y + 16
    for line in headline_lines:
        draw.text((text_x, ty), line, font=headline_font, fill=HEADLINE)
        ty += 34
    ty += 4
    for line in summary_lines:
        draw.text((text_x, ty), line, font=summary_font, fill=SUMMARY)
        ty += 28
    draw.text((text_x, y + h - 34), meta_line, font=meta_font, fill=META)


def render_poster(data: PosterData, output_path: Path, width: int = WIDTH, height: int = HEIGHT) -> None:
    base = make_gradient(width, height, BG_TOP, BG_BOTTOM).convert("RGBA")
    draw = ImageDraw.Draw(base, "RGBA")
    draw_tech_background(draw, width, height)

    title_font = pick_font(74, bold=True)
    sub_font = pick_font(30)
    section_font = pick_font(34, bold=True)
    number_font = pick_font(34, bold=True)
    headline_font = pick_font(30, bold=True)
    summary_font = pick_font(24)
    meta_font = pick_font(22)
    footer_font = pick_font(20)

    # Top title zone (close to reference style)
    draw.text((MARGIN + 48, 72), "科创中心", font=title_font, fill=TITLE_MAIN)
    draw.text((MARGIN + 48, 154), "AI热点速报", font=title_font, fill=TITLE_MAIN)
    draw.text((MARGIN + 58, 246), f"{data.date} 发布", font=sub_font, fill=TITLE_SUB)

    # Simple AI badge illustration on the right
    badge_x, badge_y = width - 300, 52
    draw.rounded_rectangle((badge_x, badge_y, badge_x + 210, badge_y + 220), radius=36, fill=(173, 226, 255, 95), outline=(226, 245, 255, 180), width=3)
    draw.rounded_rectangle((badge_x + 20, badge_y + 18, badge_x + 190, badge_y + 198), radius=30, fill=(195, 237, 255, 110), outline=(237, 250, 255, 190), width=2)
    draw.text((badge_x + 72, badge_y + 88), "AI", font=pick_font(62, bold=True), fill=(58, 122, 204))

    content_x = MARGIN
    content_w = width - MARGIN * 2

    # One section only: all five items
    y = 318
    draw_section_header(draw, content_x + 30, y, content_w - 60, "热点资讯", section_font)
    y += 60
    card_h = 158
    for idx in range(5):
        draw_news_card(
            draw,
            content_x,
            y,
            content_w,
            card_h,
            idx + 1,
            data.news[idx],
            number_font,
            headline_font,
            summary_font,
            meta_font,
        )
        y += card_h + CARD_GAP

    footer_y = height - 38
    draw.text((MARGIN, footer_y), data.footer, font=footer_font, fill=FOOTER)
    brand_w = text_width(draw, data.brand, footer_font)
    draw.text((width - MARGIN - brand_w, footer_y), data.brand, font=footer_font, fill=FOOTER)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(output_path, format="PNG")


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python scripts/render.py <input.json> <output.png>", file=sys.stderr)
        return 1
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        data = load_input(input_path)
        render_poster(data, output_path)
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Poster generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
