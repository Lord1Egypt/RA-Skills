#!/usr/bin/env python3
"""ClawVision Plus — PDF export, OG image, and Telegram sharing for ClawVision summaries."""

import argparse
import base64
import io
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdf_canvas


OG_WIDTH = 1200
OG_HEIGHT = 630


class ClawVisionPlusError(Exception):
    pass


def _load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_html(out_dir: Path, slug: str, summary_path: Path | None = None) -> Path:
    """Find the matching HTML card.

    First try exact slug variants, then fall back to any HTML file whose stem
    looks like it came from the same summary JSON name (e.g. course_session_summary_ru.json
    -> course_session_clawvision_ru_2026-08-27.html).
    """
    candidates = [
        out_dir / f"{slug}.html",
        out_dir / f"{slug}_en.html",
        out_dir / f"{slug}_ru.html",
        out_dir / f"{slug}_zh.html",
    ]
    for c in candidates:
        if c.exists():
            return c

    if summary_path:
        base = summary_path.stem  # e.g. course_session_summary_ru
        prefix = base.replace("_summary", "").replace("_", "_")
        for html in sorted(out_dir.glob("*.html")):
            name = html.stem
            if name.startswith(prefix.replace("_ru", "").replace("_en", "").replace("_zh", "")):
                return html
        htmls = sorted(out_dir.glob("*.html"))
        if htmls:
            return htmls[0]

    raise ClawVisionPlusError(f"HTML not found for slug {slug} in {out_dir}")


def export_pdf(html_path: Path, pdf_path: Path, width: int = 900):
    """Render the ClawVision HTML card to a multi-page PDF, one page per tab."""
    tab_ids = ["main", "format", "built", "next"]
    screenshots = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": 1200})
        page.goto(f"file:///{html_path.as_posix()}")
        page.wait_for_timeout(300)
        for tab_id in tab_ids:
            page.locator(f"[data-tab='{tab_id}']").click()
            page.wait_for_timeout(200)
            png_bytes = page.screenshot(full_page=True, type="png")
            screenshots.append(Image.open(io.BytesIO(png_bytes)))
        browser.close()

    if not screenshots:
        raise ClawVisionPlusError("No screenshots captured for PDF")

    a4_width_pt, a4_height_pt = A4
    a4_width_px = int(a4_width_pt)
    a4_height_px = int(a4_height_pt)

    scaled = []
    for img in screenshots:
        img = img.convert("RGB")
        ratio = min(a4_width_px / img.width, a4_height_px / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        scaled.append(img.resize(new_size, Image.Resampling.LANCZOS))

    c = pdf_canvas.Canvas(str(pdf_path), pagesize=A4)
    for img in scaled:
        img_reader = ImageReader(img)
        img_width, img_height = img.size
        x = (a4_width_pt - img_width) / 2
        y = (a4_height_pt - img_height) / 2
        c.drawImage(img_reader, x, y, width=img_width, height=img_height)
        c.showPage()
    c.save()


def _fit_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    """Return text truncated with ellipsis if it exceeds max_width."""
    bbox = draw.textbbox((0, 0), text, font=font)
    if bbox[2] <= max_width:
        return text
    while text:
        text = text[:-1]
        candidate = text + "…"
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] <= max_width:
            return candidate
    return ""


def _load_font(size: int):
    """Try a few common fonts; fall back to default."""
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_og_image(summary: dict, og_path: Path):
    """Create a 1200x630 social-preview image from summary metadata."""
    img = Image.new("RGB", (OG_WIDTH, OG_HEIGHT), color=(15, 17, 21))
    draw = ImageDraw.Draw(img)

    title_font = _load_font(56)
    subtitle_font = _load_font(28)
    body_font = _load_font(24)
    badge_font = _load_font(18)

    margin = 70
    y = margin

    # Badge
    badge_text = "ClawVision · Summary"
    badge_w, badge_h = 220, 34
    draw.rounded_rectangle(
        [(margin, y), (margin + badge_w, y + badge_h)],
        radius=17,
        fill=(42, 157, 244),
    )
    tw = draw.textbbox((0, 0), badge_text, font=badge_font)[2]
    draw.text((margin + (badge_w - tw) // 2, y + 6), badge_text, font=badge_font, fill=(255, 255, 255))
    y += badge_h + 30

    # Title
    title = summary.get("title", "ClawVision summary")[:120]
    title = _fit_text(draw, title, title_font, OG_WIDTH - margin * 2)
    draw.text((margin, y), title, font=title_font, fill=(232, 232, 232))
    y += 90

    # Subtitle
    subtitle = summary.get("subtitle", "")[:200]
    subtitle = _fit_text(draw, subtitle, subtitle_font, OG_WIDTH - margin * 2)
    draw.text((margin, y), subtitle, font=subtitle_font, fill=(154, 160, 166))
    y += 70

    # Main takeaway (two lines max)
    takeaway = summary.get("main_takeaway", "")[:180]
    takeaway = _fit_text(draw, takeaway, body_font, OG_WIDTH - margin * 2)
    draw.text((margin, y), takeaway, font=body_font, fill=(200, 200, 200))

    # Footer
    footer = "Generated with ClawVision · OpenClaw"
    fw = draw.textbbox((0, 0), footer, font=body_font)[2]
    draw.text((OG_WIDTH - margin - fw, OG_HEIGHT - margin - 30), footer, font=body_font, fill=(120, 120, 120))

    img.save(str(og_path), "PNG")


def _html_to_text_for_telegram(summary: dict, html_path: Path) -> str:
    """Build a Telegram-friendly text version from the summary."""
    lines = [
        f"<b>{summary.get('title', 'ClawVision summary')}</b>",
        f"<i>{summary.get('subtitle', '')}</i>",
        "",
        f"<b>Main takeaway:</b> {summary.get('main_takeaway', '')}",
        "",
        "<b>What we built:</b>",
    ]
    for c in summary.get("checklist", []):
        icon = "✅" if c.get("status") == "ready" else "🕐" if c.get("status") == "pending" else "🚫"
        lines.append(f"{icon} {c.get('text', '')}")
    lines.append("")
    lines.append("<b>Next steps:</b>")
    for s in summary.get("next_steps", []):
        lines.append(f"• {s}")
    return "\n".join(lines)


def send_telegram(summary: dict, html_path: Path, photo_path: Path, chat_id: str, bot_token: str, caption: str | None = None):
    """Send the OG image + summary caption to a Telegram chat/channel."""
    try:
        import telegram
        from telegram.constants import ParseMode
    except ImportError:
        raise ClawVisionPlusError(
            "python-telegram-bot is not installed. Run: pip install python-telegram-bot"
        )

    text = caption or _html_to_text_for_telegram(summary, html_path)
    if len(text) > 1024:
        bot = telegram.Bot(token=bot_token)
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
        bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
    else:
        bot = telegram.Bot(token=bot_token)
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo, caption=text, parse_mode=ParseMode.HTML)


def main():
    parser = argparse.ArgumentParser(description="ClawVision Plus extras: PDF, OG image, Telegram.")
    parser.add_argument("--summary", "-s", required=True, help="Path to ClawVision summary JSON")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--slug", help="Slug (default: derived from title)")
    parser.add_argument("--pdf", action="store_true", help="Export HTML card as multi-page PDF")
    parser.add_argument("--og", action="store_true", help="Generate 1200x630 OG image")
    parser.add_argument("--telegram", action="store_true", help="Send OG image + caption to Telegram")
    parser.add_argument("--telegram-chat-id", help="Telegram chat/channel ID")
    parser.add_argument("--telegram-bot-token", help="Telegram bot token")
    parser.add_argument("--telegram-caption", help="Override Telegram caption")
    args = parser.parse_args()

    summary_path = Path(args.summary)
    if not summary_path.exists():
        raise ClawVisionPlusError(f"Summary not found: {summary_path}")

    summary = _load_summary(summary_path)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = args.slug or _slugify(summary.get("title", "summary"))
    html_path = _find_html(out_dir, slug, summary_path=summary_path)

    result = {}

    if args.og:
        og_path = out_dir / f"{slug}_og.png"
        generate_og_image(summary, og_path)
        result["og"] = str(og_path)

    if args.pdf:
        pdf_path = out_dir / f"{slug}.pdf"
        export_pdf(html_path, pdf_path)
        result["pdf"] = str(pdf_path)

    if args.telegram:
        if not args.telegram_chat_id or not args.telegram_bot_token:
            raise ClawVisionPlusError("--telegram-chat-id and --telegram-bot-token are required for Telegram")
        og_path = out_dir / f"{slug}_og.png"
        if not og_path.exists():
            generate_og_image(summary, og_path)
        send_telegram(summary, html_path, og_path, args.telegram_chat_id, args.telegram_bot_token, args.telegram_caption)
        result["telegram"] = f"sent to {args.telegram_chat_id}"

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _slugify(text: str) -> str:
    import re
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text) or "summary"


if __name__ == "__main__":
    main()
