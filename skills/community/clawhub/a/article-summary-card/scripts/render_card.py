#!/usr/bin/env python3
import argparse
import html
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
]

MAPLE_CANDIDATES = [
    "/Users/qingyang/Library/Fonts/MapleMono-NF-CN-Regular.ttf",
    "/Users/qingyang/Library/Fonts/MapleMono-NF-CN-Medium.ttf",
    "/Users/qingyang/Library/Fonts/MapleMono-NF-CN.ttf",
    "/Users/qingyang/Library/Fonts/Maple Mono NF CN.ttf",
    "/Library/Fonts/MapleMono-NF-CN-Regular.ttf",
    "/Library/Fonts/MapleMono-NF-CN-Medium.ttf",
]

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_HEAVY = "/System/Library/Fonts/STHeiti Light.ttc"
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "templates"
HTML_TEMPLATE_PATH = TEMPLATE_DIR / "mobile-card.html"
CSS_TEMPLATE_PATH = TEMPLATE_DIR / "mobile-card.css"
SCREEN_RATIO = 3
BASE_SCREEN_WIDTH = 375
PAGE_WIDTH = BASE_SCREEN_WIDTH * SCREEN_RATIO
RENDER_OVERSCAN = 180
BASE_PAGE_PADDING = 24
BASE_TITLE_FONT_SIZE = 26
BASE_SOURCE_FONT_SIZE = 14
BASE_SECTION_FONT_SIZE = 16
BASE_BODY_FONT_SIZE = 14
BASE_FOOTER_FONT_SIZE = 14


def resolve_browser():
    for candidate in CHROME_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path
    return None


def choose_font(preferred_paths, fallback_path, size):
    for path in preferred_paths:
        candidate = Path(path)
        if candidate.exists():
            try:
                return ImageFont.truetype(str(candidate), size)
            except OSError:
                continue
    return ImageFont.truetype(fallback_path, size)


def line_height(font, extra=0):
    ascent, descent = font.getmetrics()
    return ascent + descent + extra


def wrap_text(draw, text, font, width_px):
    lines = []
    current = ""
    for ch in text:
        candidate = current + ch
        if draw.textlength(candidate, font=font) <= width_px:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def estimate_page_height(summary):
    width = PAGE_WIDTH
    page_padding = BASE_PAGE_PADDING * SCREEN_RATIO
    content_width = width - page_padding * 2
    measure_image = Image.new("RGB", (width, 100), "#fff")
    draw = ImageDraw.Draw(measure_image)

    title_font = choose_font(MAPLE_CANDIDATES, FONT_HEAVY, int(BASE_TITLE_FONT_SIZE * SCREEN_RATIO))
    source_font = ImageFont.truetype(FONT_REGULAR, int(BASE_SOURCE_FONT_SIZE * SCREEN_RATIO))
    section_font = choose_font(MAPLE_CANDIDATES, FONT_HEAVY, int(BASE_SECTION_FONT_SIZE * SCREEN_RATIO))
    body_font = ImageFont.truetype(FONT_HEAVY, int(BASE_BODY_FONT_SIZE * SCREEN_RATIO))
    footer_font = ImageFont.truetype(FONT_REGULAR, int(BASE_FOOTER_FONT_SIZE * SCREEN_RATIO))

    title_lines = wrap_text(draw, summary["title"], title_font, content_width)
    title_height = len(title_lines) * line_height(title_font, 8)
    source_height = line_height(source_font, 6)
    summary_lines = wrap_text(draw, summary["one_sentence"], body_font, content_width - 68)
    summary_height = len(summary_lines) * line_height(body_font, 12)

    sections = summary.get("sections", [])
    sections_height = 0
    for section in sections[:4]:
        heading_lines = wrap_text(draw, section.get("heading", ""), section_font, content_width)
        heading_height = max(1, len(heading_lines)) * line_height(section_font, 6)

        section_summary = section.get("summary", "")
        section_summary_lines = wrap_text(draw, section_summary, body_font, content_width)
        section_summary_height = max(1, len(section_summary_lines)) * line_height(body_font, 12) if section_summary else 0

        points_height = 0
        for point in section.get("points", [])[:3]:
            lines = wrap_text(draw, point, body_font, content_width - 112)
            points_height += len(lines) * line_height(body_font, 12) + 52 + 18

        sections_height += 34 + heading_height
        if section_summary_height:
            sections_height += 14 + section_summary_height
        if points_height:
            sections_height += 18 + points_height
        sections_height += 12

    closing_lines = wrap_text(draw, summary.get("closing_takeaway", ""), body_font, content_width - 124)
    closing_height = max(1, len(closing_lines)) * line_height(body_font, 12)
    tags = [str(tag).strip() for tag in summary.get("tags", []) if str(tag).strip()]
    tags_height = 0
    if tags:
        tag_font = choose_font(MAPLE_CANDIDATES, FONT_HEAVY, int(12 * SCREEN_RATIO))
        row_height = int(28 * SCREEN_RATIO)
        gap = int(4 * SCREEN_RATIO)
        current_width = 0
        rows = 1
        for tag in tags:
            tag_width = int(draw.textlength(tag, font=tag_font) + 20 * SCREEN_RATIO)
            if current_width and current_width + gap + tag_width > content_width:
                rows += 1
                current_width = tag_width
            else:
                current_width = tag_width if current_width == 0 else current_width + gap + tag_width
        tags_height = 34 + line_height(section_font) + 18 + rows * row_height + max(0, rows - 1) * gap + 20

    total = 32 + 32
    total += 32 + title_height + 12 + source_height
    total += 28
    total += 34 + line_height(section_font) + 18 + summary_height + 34
    total += 28
    total += sections_height + 20
    total += 28
    total += 34 + line_height(section_font) + 18 + closing_height + 24
    if tags_height:
        total += tags_height
    total += 24 + line_height(footer_font) + 32
    return max(total, 1200)


def render_list_items(items, class_name, bullet=False):
    parts = []
    for item in items:
        text = html.escape(item)
        bullet_html = '<span class="list-bullet" aria-hidden="true"></span>' if bullet else ""
        parts.append(f'<li class="{class_name}">{bullet_html}<span class="list-text">{text}</span></li>')
    return "\n".join(parts)


def build_section_blocks(summary):
    sections = summary.get("sections", [])
    section_html = []
    for section in sections[:4]:
        heading = html.escape(section.get("heading", ""))
        section_summary = html.escape(section.get("summary", ""))
        points = render_list_items(section.get("points", [])[:3], "point-card")
        summary_block = f'<p class="summary-text section-summary">{section_summary}</p>' if section_summary else ""
        points_block = f'<ul class="points-list">{points}</ul>' if points else ""
        section_html.append(
            f"""<section class="card section-card">
        <h2 class="section-title">{heading}</h2>
        {summary_block}
        {points_block}
      </section>"""
        )
    return "".join(section_html)


def build_tags_block(summary):
    tags = [str(tag).strip() for tag in summary.get("tags", []) if str(tag).strip()]
    if not tags:
        return ""
    chips = "".join(f'<span class="tag-chip">{html.escape(tag)}</span>' for tag in tags[:12])
    return f"""<section class="card section-card tags-card">
        <h2 class="section-title">标签</h2>
        <div class="tags-wrap">{chips}</div>
      </section>"""


def build_html(summary, html_template_path: Path, css_path: Path):
    template = html_template_path.read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}": html.escape(summary["title"]),
        "{{SOURCE}}": html.escape(summary.get("source", "")),
        "{{ONE_SENTENCE}}": html.escape(summary["one_sentence"]),
        "{{SECTION_BLOCKS}}": build_section_blocks(summary),
        "{{CLOSING_TAKEAWAY}}": html.escape(summary.get("closing_takeaway", "")),
        "{{TAGS_BLOCK}}": build_tags_block(summary),
        "{{CSS_HREF}}": css_path.resolve().as_uri(),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def measure_page_height(browser_path: Path, html_path: Path):
    command = [
        str(browser_path),
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--dump-dom",
        "--virtual-time-budget=1500",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    match = re.search(r'data-render-height="(\d+)"', result.stdout)
    if not match:
        return None
    return int(match.group(1))


def render_png(browser_path: Path, html_path: Path, out_path: Path, viewport_height: int):
    command = [
        str(browser_path),
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--screenshot={out_path}",
        f"--window-size={PAGE_WIDTH},{viewport_height}",
        f"--virtual-time-budget=1500",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def crop_to_canvas(image_path: Path, target_height: int | None = None, target_width: int = PAGE_WIDTH):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    crop_width = min(width, target_width)
    crop_height = height if target_height is None else min(height, target_height)
    if crop_width < width or crop_height < height:
        image.crop((0, 0, crop_width, crop_height)).save(image_path, quality=95)


def crop_bottom_whitespace(image_path: Path, bottom_padding=56):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    sample_step = max(1, width // 180)
    cutoff_y = None

    for y in range(height - 1, -1, -1):
        samples = [image.getpixel((x, y)) for x in range(0, width, sample_step)]
        channel_span = max(max(pixel) for pixel in samples) - min(min(pixel) for pixel in samples)
        if channel_span > 18:
            cutoff_y = y
            break

    if cutoff_y is None:
        return

    crop_height = min(height, cutoff_y + bottom_padding)
    if crop_height < height:
        image.crop((0, 0, width, crop_height)).save(image_path, quality=95)
    crop_to_canvas(image_path)


def main():
    parser = argparse.ArgumentParser(description="Render a summary JSON file into HTML and PNG.")
    parser.add_argument("--summary", required=True, help="Path to summary JSON")
    parser.add_argument("--out", required=True, help="Path to output PNG")
    parser.add_argument("--html-out", help="Optional path to generated HTML")
    args = parser.parse_args()

    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    out_path = Path(args.out)
    html_out = Path(args.html_out) if args.html_out else out_path.with_suffix(".html")
    css_path = CSS_TEMPLATE_PATH

    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(build_html(summary, HTML_TEMPLATE_PATH, css_path), encoding="utf-8")
    print(html_out)

    browser_path = resolve_browser()
    if browser_path is None:
        raise SystemExit("No supported browser found for HTML screenshot rendering.")

    page_height = measure_page_height(browser_path, html_out)
    used_dom_height = page_height is not None
    if page_height is None:
        page_height = estimate_page_height(summary)
    viewport_height = page_height + RENDER_OVERSCAN if used_dom_height else page_height
    render_png(browser_path, html_out, out_path, viewport_height)
    if used_dom_height:
        crop_to_canvas(out_path, target_height=page_height)
    else:
        crop_bottom_whitespace(out_path)
    print(out_path)


if __name__ == "__main__":
    main()
