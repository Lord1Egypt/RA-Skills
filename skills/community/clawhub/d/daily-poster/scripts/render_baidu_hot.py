#!/usr/bin/env python3
"""Render a Baidu Hot Search poster styled after the official top.baidu.com page."""

from __future__ import annotations

import base64
import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape, quoteattr

from holiday_countdown import parse_base_date
from lunar_calendar import format_lunar_text
from poster_runtime import run_renderer_cli

DEFAULT_FONT_STACK = '"PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif'
WEEKDAY_LABELS = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
POSTER_TYPE = "baidu_hot"
DEFAULT_OUTPUT_SCALE = 2.0

BAIDU_API_URL = "https://v2.xxapi.cn/api/baiduhot"
DEFAULT_HEADER_TITLE = "百度热搜榜"
DEFAULT_HEADER_SUBTITLE = "实时热点  一手掌握"
DEFAULT_CONTENT_LIMIT = 10

# Embedded to avoid runtime PNG file dependencies in deployment targets such as Clawhub.
BAIDU_LOGO_DATA_URI = (
    "data:image/png;base64,"
    "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"
)

# --- Official Baidu style palette ---
THEME = {
    "page_bg": "#f5f5f6",
    "card_bg": "#ffffff",
    "header_bg": "#ffffff",
    "title_color": "#222222",
    "subtitle_color": "#9195a3",
    "text_primary": "#333333",
    "text_desc": "#626675",
    "hot_color": "#ff4e4e",
    "rank_1_bg": "#f73131",
    "rank_2_bg": "#ff7f29",
    "rank_3_bg": "#ffaa20",
    "rank_normal_color": "#9195a3",
    "divider": "#ebebeb",
    "baidu_blue": "#306cff",
    "font_family": DEFAULT_FONT_STACK,
}


def _char_units(char: str) -> float:
    import unicodedata
    if char.isspace():
        return 0.35
    if unicodedata.east_asian_width(char) in {"W", "F"}:
        return 1.0
    if char in "ilI1|.,'`":
        return 0.32
    if char in "mwMW@#%&":
        return 0.9
    return 0.58


def _text_width(text: str, font_size: float) -> float:
    return sum(_char_units(ch) for ch in text) * font_size


def _truncate_text(text: str, max_width: float, font_size: float) -> str:
    if _text_width(text, font_size) <= max_width:
        return text
    result = ""
    for ch in text:
        if _text_width(result + ch + "...", font_size) > max_width:
            return result + "..."
        result += ch
    return result


def _escape(text: str) -> str:
    return escape(str(text))


def _listify(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _resolve_base_date(spec: dict[str, Any]) -> date:
    raw_value = str(spec.get("base_date", "")).strip()
    if not raw_value:
        return date.today()
    return parse_base_date(raw_value)


def _resolve_lunar_text(current_date: date) -> str:
    try:
        return format_lunar_text(current_date)
    except (TypeError, ValueError):
        return ""


def _resolve_personal_lines(personal: dict[str, Any]) -> list[str]:
    text_lines = [str(item).strip() for item in _listify(personal.get("text_lines")) if str(item).strip()]
    if text_lines:
        return text_lines[:2]

    bio_lines = [str(item).strip() for item in _listify(personal.get("bio_lines")) if str(item).strip()]
    if bio_lines:
        return bio_lines[:2]

    bio = str(personal.get("bio", "")).strip()
    signature = str(personal.get("signature", "")).strip()
    merged = bio or signature
    return [merged] if merged else []


def normalize_baidu_hot_spec(spec: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    del base_dir
    normalized = dict(spec)
    normalized["poster_type"] = POSTER_TYPE

    normalized["header"] = {
        "title": DEFAULT_HEADER_TITLE,
        "subtitle": DEFAULT_HEADER_SUBTITLE,
    }
    normalized["content"] = {
        "api_url": BAIDU_API_URL,
        "limit": DEFAULT_CONTENT_LIMIT,
    }

    personal = normalized.get("personal_info", {})
    if not isinstance(personal, dict):
        personal = {}
    personal = dict(personal)
    if not str(personal.get("name", "")).strip() and str(personal.get("title", "")).strip():
        personal["name"] = str(personal.get("title", "")).strip()
    if not str(personal.get("signature", "")).strip():
        lines = _resolve_personal_lines(personal)
        if lines:
            personal["signature"] = " ".join(lines)
    normalized["personal_info"] = personal

    return normalized


def _load_logo_base64() -> str | None:
    return BAIDU_LOGO_DATA_URI


def _download_image_base64(url: str, *, timeout: float = 6.0) -> str | None:
    """Download an image URL and return as data URI, or None on failure."""
    if not url:
        return None
    try:
        req = Request(url, headers={"User-Agent": "daily-poster/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        b64 = base64.b64encode(data).decode("ascii")
        content_type = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        return f"data:{content_type};base64,{b64}"
    except Exception:
        return None


def _format_hot_number(hot: str) -> str:
    """Format hot number: e.g. 4962498 -> 496万"""
    try:
        num = int(hot.replace(",", "").replace("万", "0000").strip())
    except (ValueError, AttributeError):
        return hot
    if num >= 10000:
        return f"{num // 10000}万"
    return str(num)


def _fetch_baidu_hot(api_url: str, *, timeout: float = 8.0) -> list[dict[str, Any]]:
    request = Request(api_url, headers={"User-Agent": "daily-poster/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            payload = json.loads(response.read().decode(charset))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
        return []
    if not isinstance(payload, dict):
        return []
    data = payload.get("data", [])
    return data if isinstance(data, list) else []


def render_baidu_hot_poster(spec: dict[str, Any], base_dir: Path | None = None) -> str:
    del base_dir
    header = spec.get("header", {})
    header = header if isinstance(header, dict) else {}
    content = spec.get("content", {})
    content = content if isinstance(content, dict) else {}

    api_url = str(content.get("api_url", BAIDU_API_URL)).strip() or BAIDU_API_URL
    items = _fetch_baidu_hot(api_url)
    try:
        limit = int(content.get("limit", DEFAULT_CONTENT_LIMIT) or DEFAULT_CONTENT_LIMIT)
    except (TypeError, ValueError):
        limit = DEFAULT_CONTENT_LIMIT
    items = [it for it in items if isinstance(it, dict)][:limit]

    # Pre-download all item images
    img_cache: dict[int, str | None] = {}
    for i, item in enumerate(items):
        img_url = str(item.get("img", "")).strip()
        img_cache[i] = _download_image_base64(img_url)

    today = _resolve_base_date(spec)
    weekday = WEEKDAY_LABELS[today.weekday()]
    date_str = f"{today.year}年{today.month}月{today.day}日"
    lunar_text = _resolve_lunar_text(today)
    date_meta_parts = [date_str, weekday]
    if lunar_text:
        date_meta_parts.append(lunar_text)
    date_meta_text = "  ".join(part for part in date_meta_parts if part)

    logo_data_uri = _load_logo_base64()
    title_text = str(header.get("title", "")).strip() or DEFAULT_HEADER_TITLE
    subtitle = str(header.get("subtitle", DEFAULT_HEADER_SUBTITLE)).strip()

    width = 1080
    margin_x = 48
    card_w = width - margin_x * 2

    # Layout measurements
    header_h = 140
    item_h = 136
    card_padding_top = 16
    card_padding_bottom = 16
    card_header_h = 56
    content_h = card_header_h + card_padding_top + len(items) * item_h + card_padding_bottom
    footer_h = 52
    gap = 24
    height = header_h + gap + content_h + gap + footer_h

    font_family = quoteattr(THEME["font_family"])
    parts: list[str] = []

    # SVG open
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
        f' width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )

    # Defs: shadow filter + image clip paths
    parts.append("<defs>")
    parts.append(
        '<filter id="card-shadow" x="-4%" y="-2%" width="108%" height="110%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="8" flood-color="#000" flood-opacity="0.06"/>'
        '</filter>'
    )
    # Clip paths for rounded images (one per item)
    img_w, img_h, img_r = 160, 100, 8
    for i in range(len(items)):
        parts.append(
            f'<clipPath id="img-clip-{i}"><rect x="0" y="0" width="{img_w}" height="{img_h}" rx="{img_r}" ry="{img_r}"/></clipPath>'
        )
    parts.append("</defs>")

    # ====================== PAGE BACKGROUND ======================
    parts.append(f'<rect width="{width}" height="{height}" fill="{THEME["page_bg"]}"/>')

    # ====================== HEADER CARD ======================
    hdr_x = margin_x
    hdr_y = 24
    hdr_w = card_w
    hdr_h = header_h - 24

    parts.append(
        f'<rect x="{hdr_x}" y="{hdr_y}" width="{hdr_w}" height="{hdr_h}"'
        f' rx="16" ry="16" fill="{THEME["header_bg"]}" filter="url(#card-shadow)"/>'
    )

    # Baidu logo
    logo_y = hdr_y + 22
    if logo_data_uri:
        parts.append(
            f'<image x="{hdr_x + 36}" y="{logo_y}" width="120" height="42"'
            f' href="{logo_data_uri}" preserveAspectRatio="xMidYMid meet"/>'
        )
    else:
        parts.append(
            f'<text x="{hdr_x + 36}" y="{logo_y + 32}" fill="{THEME["baidu_blue"]}" font-size="30"'
            f' font-weight="800" font-family={font_family}>百度</text>'
        )

    # "热搜" badge
    badge_x = hdr_x + 168
    badge_y = logo_y + 8
    parts.append(
        f'<rect x="{badge_x}" y="{badge_y}" width="56" height="28" rx="4" ry="4" fill="{THEME["hot_color"]}"/>'
    )
    parts.append(
        f'<text x="{badge_x + 28}" y="{badge_y + 20}" fill="#ffffff" font-size="16"'
        f' font-weight="700" font-family={font_family} text-anchor="middle">热搜</text>'
    )

    # Date on the right
    parts.append(
        f'<text x="{hdr_x + hdr_w - 36}" y="{logo_y + 24}" fill="{THEME["subtitle_color"]}" font-size="18"'
        f' font-weight="400" font-family={font_family} text-anchor="end">'
        f'{_escape(date_meta_text)}</text>'
    )

    # Personal info
    personal = spec.get("personal_info", {})
    if isinstance(personal, dict):
        p_name = str(personal.get("name", "")).strip()
        personal_lines = _resolve_personal_lines(personal)
        if p_name:
            parts.append(
                f'<text x="{hdr_x + hdr_w - 36}" y="{logo_y + 48}" fill="{THEME["title_color"]}" font-size="15"'
                f' font-weight="600" font-family={font_family} text-anchor="end">{_escape(p_name)}</text>'
            )
        if personal_lines:
            sig_y = logo_y + (66 if p_name else 48)
            for index, line in enumerate(personal_lines[:2]):
                parts.append(
                    f'<text x="{hdr_x + hdr_w - 36}" y="{sig_y + index * 18}" fill="{THEME["subtitle_color"]}" font-size="13"'
                    f' font-weight="400" font-family={font_family} text-anchor="end">{_escape(line)}</text>'
                )

    # Subtitle
    if subtitle:
        parts.append(
            f'<text x="{hdr_x + 36}" y="{logo_y + 68}" fill="{THEME["subtitle_color"]}" font-size="15"'
            f' font-weight="400" font-family={font_family} letter-spacing="2">{_escape(subtitle)}</text>'
        )

    # ====================== CONTENT CARD ======================
    card_x = margin_x
    card_y = header_h + gap
    card_r = 16

    parts.append(
        f'<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{content_h}"'
        f' rx="{card_r}" ry="{card_r}" fill="{THEME["card_bg"]}" filter="url(#card-shadow)"/>'
    )

    # Card header
    ch_y = card_y + 40
    parts.append(
        f'<text x="{card_x + 36}" y="{ch_y}" fill="{THEME["title_color"]}" font-size="22"'
        f' font-weight="700" font-family={font_family}>{_escape(title_text)}</text>'
    )
    parts.append(
        f'<text x="{card_x + card_w - 36}" y="{ch_y}" fill="{THEME["subtitle_color"]}" font-size="14"'
        f' font-weight="400" font-family={font_family} text-anchor="end">TOP {len(items)}</text>'
    )

    # Divider below card header
    div_ch_y = card_y + card_header_h
    parts.append(
        f'<line x1="{card_x}" y1="{div_ch_y}" x2="{card_x + card_w}" y2="{div_ch_y}"'
        f' stroke="{THEME["divider"]}" stroke-width="1"/>'
    )

    # --- List items ---
    list_start_y = div_ch_y + card_padding_top
    text_area_w = card_w - 36 - 60 - 24 - img_w - 36  # left_pad + rank_area + gap + img + right_pad

    for i, item in enumerate(items):
        row_y = list_start_y + i * item_h
        rank = int(item.get("index", i + 1))
        title = str(item.get("title", "")).strip()
        hot = str(item.get("hot", "")).strip()
        desc = str(item.get("desc", "")).strip()

        # Row background (alternating)
        if i % 2 == 0:
            parts.append(
                f'<rect x="{card_x + 1}" y="{row_y}" width="{card_w - 2}" height="{item_h}"'
                f' fill="#fafbfc"/>'
            )

        # --- Left side: rank + text ---
        # Rank badge
        rank_cx = card_x + 56
        rank_cy = row_y + 32
        if rank <= 3:
            colors = [THEME["rank_1_bg"], THEME["rank_2_bg"], THEME["rank_3_bg"]]
            parts.append(
                f'<rect x="{rank_cx - 15}" y="{rank_cy - 15}" width="30" height="30"'
                f' rx="6" ry="6" fill="{colors[rank - 1]}"/>'
            )
            parts.append(
                f'<text x="{rank_cx}" y="{rank_cy + 7}" fill="#ffffff" font-size="17"'
                f' font-weight="700" font-family={font_family} text-anchor="middle">{rank}</text>'
            )
        else:
            parts.append(
                f'<text x="{rank_cx}" y="{rank_cy + 7}" fill="{THEME["rank_normal_color"]}" font-size="20"'
                f' font-weight="600" font-family={font_family} text-anchor="middle">{rank}</text>'
            )

        # Title
        title_x = card_x + 96
        title_y = row_y + 36
        title_fs = 20 if rank <= 3 else 18
        title_weight = "700" if rank <= 3 else "500"
        max_tw = text_area_w
        display_title = _truncate_text(title, max_tw, title_fs)
        parts.append(
            f'<text x="{title_x}" y="{title_y}" fill="{THEME["title_color"]}" font-size="{title_fs}"'
            f' font-weight="{title_weight}" font-family={font_family}>{_escape(display_title)}</text>'
        )

        # Description (two lines max)
        if desc:
            desc_y = row_y + 60
            desc_fs = 13
            max_dw = text_area_w
            line1 = _truncate_text(desc, max_dw, desc_fs)
            remaining = desc[len(line1.rstrip(".")):].lstrip(".").strip() if line1.endswith("...") else ""
            parts.append(
                f'<text x="{title_x}" y="{desc_y}" fill="{THEME["text_desc"]}" font-size="{desc_fs}"'
                f' font-weight="400" font-family={font_family}>{_escape(line1)}</text>'
            )
            if remaining:
                line2 = _truncate_text(remaining, max_dw, desc_fs)
                parts.append(
                    f'<text x="{title_x}" y="{desc_y + 18}" fill="{THEME["text_desc"]}" font-size="{desc_fs}"'
                    f' font-weight="400" font-family={font_family}>{_escape(line2)}</text>'
                )

        # Hot value (below title, left side)
        hot_display = _format_hot_number(hot)
        hot_y = row_y + (96 if desc else 64)
        hot_label_color = THEME["hot_color"] if rank <= 3 else THEME["subtitle_color"]
        parts.append(
            f'<text x="{title_x}" y="{hot_y}" fill="{hot_label_color}" font-size="13"'
            f' font-weight="500" font-family={font_family}>热度 {_escape(hot_display)}</text>'
        )

        # --- Right side: image ---
        img_data = img_cache.get(i)
        img_x = card_x + card_w - 36 - img_w
        img_y = row_y + (item_h - img_h) // 2
        if img_data:
            parts.append(
                f'<g transform="translate({img_x},{img_y})" clip-path="url(#img-clip-{i})">'
                f'<image x="0" y="0" width="{img_w}" height="{img_h}"'
                f' href="{img_data}" preserveAspectRatio="xMidYMid slice"/>'
                f'</g>'
            )
            # Subtle border around image
            parts.append(
                f'<rect x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}"'
                f' rx="{img_r}" ry="{img_r}" fill="none" stroke="{THEME["divider"]}" stroke-width="1"/>'
            )
        else:
            # Placeholder
            parts.append(
                f'<rect x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}"'
                f' rx="{img_r}" ry="{img_r}" fill="#f0f0f0"/>'
            )

        # Row divider
        if i < len(items) - 1:
            div_y = row_y + item_h
            parts.append(
                f'<line x1="{card_x + 36}" y1="{div_y}" x2="{card_x + card_w - 36}" y2="{div_y}"'
                f' stroke="{THEME["divider"]}" stroke-width="0.5"/>'
            )

    # ====================== FOOTER ======================
    footer_y = card_y + content_h + gap
    parts.append(
        f'<text x="{width // 2}" y="{footer_y + 28}" fill="{THEME["subtitle_color"]}" font-size="14"'
        f' font-weight="400" font-family={font_family} text-anchor="middle"'
        f' letter-spacing="1">数据来源：百度热搜  |  {_escape(date_str)}</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    run_renderer_cli(
        poster_type=POSTER_TYPE,
        description="Render a Baidu Hot Search poster from JSON spec.",
        render_svg=render_baidu_hot_poster,
        default_scale=DEFAULT_OUTPUT_SCALE,
        default_background=THEME["page_bg"],
        prepare_spec=normalize_baidu_hot_spec,
    )


if __name__ == "__main__":
    main()
