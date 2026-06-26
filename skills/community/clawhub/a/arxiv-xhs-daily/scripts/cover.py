from __future__ import annotations

from pathlib import Path
from typing import Iterable


def generate_cover_image(output_path: Path, title: str, subtitle: str, bullets: Iterable[str], theme: str = "dark") -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
    except Exception as exc:
        raise RuntimeError(f"Pillow is required for cover generation: {exc}")

    width, height = 1242, 1660
    base = Image.new("RGB", (width, height), "#0A0F1E")
    draw = ImageDraw.Draw(base)

    if theme == "light":
        top = (242, 247, 252)
        bottom = (227, 236, 247)
        glow1 = (95, 151, 255, 48)
        glow2 = (164, 118, 255, 42)
        glow3 = (54, 196, 164, 24)
        card_fill = "#F8FBFF"
        card_outline = (34, 52, 92, 28)
        chip_fill = "#E9F1FF"
        chip_text_fill = "#35507A"
        title_fill = "#0F172A"
        subtitle_fill = "#5B6B83"
        divider_fill = "#D6E0EE"
        section_fill = "#40526E"
        panel_fill = "#FFFFFF"
        panel_outline = (54, 72, 103, 24)
        body_fill = "#142033"
        footer_fill = "#6B7A90"
    else:
        top = (10, 15, 30)
        bottom = (20, 28, 58)
        glow1 = (65, 182, 230, 90)
        glow2 = (107, 92, 255, 70)
        glow3 = (28, 184, 151, 34)
        card_fill = "#090E1C"
        card_outline = (255, 255, 255, 32)
        chip_fill = "#151E38"
        chip_text_fill = "#D8EEFF"
        title_fill = "#F7FBFF"
        subtitle_fill = "#A8BAD3"
        divider_fill = "#263352"
        section_fill = "#DCE7FF"
        panel_fill = "#101933"
        panel_outline = (255, 255, 255, 18)
        body_fill = "#F3F7FF"
        footer_fill = "#8EA5C2"

    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        gch = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line((0, y, width, y), fill=(r, gch, b))

    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((760, 120, 1200, 560), fill=glow1)
    g.ellipse((0, 980, 420, 1420), fill=glow2)
    g.rectangle((880, 1120, 1220, 1500), fill=glow3)
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    base = Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(base)

    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 108)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34)
        section_font = ImageFont.truetype("/System/Library/Fonts/SFNSRounded.ttf", 28)
        body_font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 34)
        index_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 30)
    except Exception:
        title_font = subtitle_font = section_font = body_font = index_font = ImageFont.load_default()

    card = (70, 84, width - 70, height - 84)
    draw.rounded_rectangle(card, radius=44, fill=card_fill, outline=card_outline, width=2)

    chip_x, chip_y = 100, 116
    chip_text = "ARXIV RESEARCH NOTE"
    chip_bbox = draw.textbbox((0, 0), chip_text, font=section_font)
    chip_w = (chip_bbox[2] - chip_bbox[0]) + 52
    chip_h = 54
    draw.rounded_rectangle((chip_x, chip_y, chip_x + chip_w, chip_y + chip_h), radius=24, fill=chip_fill)
    draw.text((chip_x + 24, chip_y + 12), chip_text, font=section_font, fill=chip_text_fill)

    title_text = _wrap_text(draw, title, title_font, max_width=width - 220, max_lines=2)
    draw.multiline_text((100, 220), title_text, font=title_font, fill=title_fill, spacing=6)
    draw.text((100, 468), subtitle, font=subtitle_font, fill=subtitle_fill)

    draw.rounded_rectangle((100, 548, width - 100, 552), radius=2, fill=divider_fill)
    draw.text((100, 590), "PAPER SNAPSHOT", font=section_font, fill=section_fill)

    y = 660
    palette = [(93, 208, 255), (148, 133, 255), (76, 225, 184)]
    for idx, bullet in enumerate(list(bullets)[:3], start=1):
        panel = (100, y, width - 100, y + 170)
        draw.rounded_rectangle(panel, radius=28, fill=panel_fill, outline=panel_outline, width=1)
        accent = palette[(idx - 1) % len(palette)]
        draw.rounded_rectangle((122, y + 24, 182, y + 84), radius=18, fill=accent)
        num_bbox = draw.textbbox((0, 0), str(idx), font=index_font)
        num_w = num_bbox[2] - num_bbox[0]
        draw.text((152 - num_w / 2, y + 35), str(idx), font=index_font, fill="#09111D")
        bullet_font = _choose_bullet_font(ImageFont, bullet)
        bullet_text = _wrap_text(draw, bullet, bullet_font, max_width=width - 340, max_lines=3)
        draw.multiline_text((214, y + 28), bullet_text, font=bullet_font, fill=body_fill, spacing=8)
        y += 198

    draw.text((100, height - 138), "Designed for Xiaohongshu · Daily Research Notes", font=subtitle_font, fill=footer_fill)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    base.save(output_path, format="PNG")


def _choose_bullet_font(ImageFont, text: str):
    try:
        if any(ord(ch) > 127 for ch in text):
            return ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 34)
        return ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34)
    except Exception:
        return ImageFont.load_default()


def _wrap_text(draw, text: str, font, max_width: int, max_lines: int) -> str:
    text = " ".join((text or "").split())
    if not text:
        return ""

    if any(ord(ch) > 127 for ch in text):
        return _wrap_cjk(draw, text, font, max_width, max_lines)
    return _wrap_words(draw, text, font, max_width, max_lines)


def _wrap_words(draw, text: str, font, max_width: int, max_lines: int) -> str:
    words = text.split()
    lines = []
    current = ""
    for i, word in enumerate(words):
        test = word if not current else current + " " + word
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) == max_lines - 1 and current:
            remaining = [current] + words[i + 1 :]
            tail = " ".join(remaining)
            while draw.textlength(tail + "…", font=font) > max_width and len(tail) > 1:
                tail = tail[:-1]
            lines.append(tail + "…")
            return "\n".join(lines)
    if current:
        lines.append(current)
    return "\n".join(lines[:max_lines])


def _wrap_cjk(draw, text: str, font, max_width: int, max_lines: int) -> str:
    lines = []
    current = ""
    for i, ch in enumerate(text):
        test = current + ch
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
        if len(lines) == max_lines - 1 and current:
            tail = current + text[i + 1 :]
            while draw.textlength(tail + "…", font=font) > max_width and len(tail) > 1:
                tail = tail[:-1]
            lines.append(tail + "…")
            return "\n".join(lines)
    if current:
        lines.append(current)
    return "\n".join(lines[:max_lines])
