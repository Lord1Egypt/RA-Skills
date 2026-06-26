#!/usr/bin/env python3
"""Render a newspaper-style daily poster from a JSON spec into SVG."""

from __future__ import annotations

import base64
from datetime import timedelta
from functools import lru_cache
import json
import mimetypes
import os
import re
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urlparse
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape, quoteattr

from holiday_countdown import HOLIDAYS_2026, Holiday, build_countdown_items, holidays_from_schedule, parse_base_date
from lunar_calendar import format_lunar_text
from poster_runtime import run_renderer_cli

DEFAULT_FONT_STACK = '"PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif'
REFERENCE_DIR = Path(__file__).resolve().parent.parent / "references"
CACHE_DIR = REFERENCE_DIR / "cache"
POSTER_TYPE = "daily"
DEFAULT_OUTPUT_SCALE = 1.0
DEFAULT_OUTPUT_BACKGROUND = "#ffffff"
BASE_THEME = {
    "paper": "#f3e7d2",
    "panel": "#f8f0e2",
    "accent": "#bc3b24",
    "ink": "#2d261f",
    "muted": "#75685b",
    "line": "#3b3129",
    "soft": "#d7c4a9",
    "stamp": "#d68a1e",
    "font_family": DEFAULT_FONT_STACK,
}
THEME = BASE_THEME.copy()
WEEKDAY_LABELS = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
DEFAULT_PLAN_ROWS = [
    {"time": "09:00", "text": "上班打卡"},
    {"time": "09:30", "text": "整理消息"},
    {"time": "10:00", "text": "重点推进"},
    {"time": "10:40", "text": "开会摸鱼"},
    {"time": "14:00", "text": "继续收尾"},
    {"time": "18:00", "text": "准点下班"},
]
DEFAULT_PROMO_LINES = [
    "资深摸鱼艺术家，擅长在复杂需求里保住下班时间。",
    "不讲大道理，只负责把日报排好。",
]


def dig(data: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def listify(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def clean_text_lines(value: Any, *, limit: int | None = None) -> list[str]:
    lines = [str(item).strip() for item in listify(value) if str(item).strip()]
    return lines[:limit] if limit is not None else lines


def char_units(char: str) -> float:
    if char.isspace():
        return 0.35
    if unicodedata.east_asian_width(char) in {"W", "F"}:
        return 1.0
    if char in "ilI1|.,'`":
        return 0.32
    if char in "mwMW@#%&":
        return 0.9
    return 0.58


def text_width(text: str, font_size: float) -> float:
    return sum(char_units(ch) for ch in text) * font_size


def fit_single_line_font_size(text: str, *, max_width: float, max_height: float, max_size: float, min_size: float = 28) -> float:
    content = str(text or "").strip()
    if not content:
        return min_size
    unit_width = max(text_width(content, 1), 0.1)
    width_size = max_width / unit_width
    height_size = max_height
    return max(min_size, min(max_size, width_size, height_size))


def split_quote_text_source(text: str) -> tuple[str, str]:
    content = str(text or "").strip()
    if not content:
        return "", ""

    match = re.match(r"^(?P<body>.+?)\s*(?:—{2,}|-{2,})\s*(?P<suffix>.+)$", content)
    if not match:
        return content, ""

    body = match.group("body").strip()
    suffix = match.group("suffix").strip()
    return body, suffix


def wrap_text(text: str, max_width: float, font_size: float) -> list[str]:
    text = str(text or "")
    if not text.strip():
        return []
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph.strip():
            lines.append("")
            continue
        line = ""
        for char in paragraph.rstrip():
            probe = f"{line}{char}"
            if line and text_width(probe, font_size) > max_width:
                lines.append(line.rstrip())
                line = char.lstrip()
            else:
                line = probe
        if line:
            lines.append(line.rstrip())
    return lines


def trim_lines(lines: list[str], limit: int) -> list[str]:
    if len(lines) <= limit:
        return lines
    clipped = lines[:limit]
    tail = clipped[-1].rstrip()
    clipped[-1] = f"{tail[:-1]}..." if len(tail) > 1 else f"{tail}..."
    return clipped


def wrap_with_prefix(prefix: str, text: str, max_width: float, font_size: float) -> list[str]:
    first_width = max_width - text_width(prefix, font_size)
    hanging = " " * max(2, len(prefix) + 1)
    hanging_width = max_width - text_width(hanging, font_size)
    first = wrap_text(text, first_width, font_size)
    if not first:
        return [prefix]
    result = [f"{prefix}{first[0]}"]
    remainder = text[len(first[0]) :]
    if remainder:
        result.extend(f"{hanging}{line}" for line in wrap_text(remainder, hanging_width, font_size))
    return result


def rect(x: float, y: float, w: float, h: float, *, fill: str = "none", stroke: str = "none", stroke_width: float = 0, rx: float = 0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}" rx="{rx:.1f}" ry="{rx:.1f}" />'


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str, stroke_width: float) -> str:
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{stroke_width:.1f}" />'


def circle(cx: float, cy: float, r: float, *, fill: str, stroke: str, stroke_width: float) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}" />'


def text_block(x: float, y: float, lines_: list[str], *, font_size: float, fill: str, anchor: str = "start", weight: int = 400, line_height: float | None = None, letter_spacing: float = 0) -> str:
    if not lines_:
        return ""
    step = line_height or font_size * 1.36
    font_family = str(THEME.get("font_family", DEFAULT_FONT_STACK) or DEFAULT_FONT_STACK)
    font_family_attr = quoteattr(font_family)
    spans = []
    for index, value in enumerate(lines_):
        dy = "0" if index == 0 else f"{step:.1f}"
        spans.append(f'<tspan x="{x:.1f}" dy="{dy}" xml:space="preserve">{escape(value) if value else "&#160;"}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{font_size:.1f}" font-weight="{weight}" font-family={font_family_attr} text-anchor="{anchor}" letter-spacing="{letter_spacing:.1f}">{"".join(spans)}</text>'


def resolve_image(path_value: str | None, base_dir: Path) -> Path | None:
    if not path_value:
        return None
    raw = Path(os.path.expandvars(path_value)).expanduser()
    candidate = raw if raw.is_absolute() else base_dir / raw
    return candidate.resolve() if candidate.exists() else None


@lru_cache(maxsize=32)
def fetch_binary_payload(url: str, *, timeout: float = 8.0) -> tuple[str, bytes] | None:
    request = Request(url, headers={"User-Agent": "daily-poster/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = response.read()
            mime = response.headers.get_content_type()
            if not mime or mime == "application/octet-stream":
                guessed, _ = mimetypes.guess_type(urlparse(url).path)
                mime = guessed or "image/png"
            return mime, payload
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        return None


def load_image_asset(path_value: str | None, *, base_dir: Path) -> tuple[str, bytes] | None:
    source = str(path_value or "").strip()
    if not source:
        return None
    if source.startswith(("http://", "https://")):
        return fetch_binary_payload(source)
    path = resolve_image(source, base_dir)
    if path is None:
        return None
    mime, _ = mimetypes.guess_type(str(path))
    return (mime or "image/png", path.read_bytes())


def cache_remote_image(url: str, *, cache_key: str) -> Path | None:
    asset = fetch_binary_payload(url)
    if asset is None:
        return None

    mime, payload = asset
    suffix = mimetypes.guess_extension(mime or "") or Path(urlparse(url).path).suffix or ".img"
    if suffix == ".jpe":
        suffix = ".jpg"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{cache_key}{suffix}"
    cache_path.write_bytes(payload)
    return cache_path


def find_cached_image(cache_key: str) -> Path | None:
    if not CACHE_DIR.exists():
        return None
    matches = sorted(CACHE_DIR.glob(f"{cache_key}.*"), key=lambda item: item.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


class Svg:
    def __init__(self, width: int, height: int, background: str) -> None:
        self.width = width
        self.height = height
        self.background = background
        self.defs: list[str] = []
        self.items: list[str] = []
        self.counter = 0

    def add(self, value: str) -> None:
        if value:
            self.items.append(value)

    def image(self, path_value: str | None, *, base_dir: Path, x: float, y: float, w: float, h: float, mode: str = "cover", label: str = "图片", stroke: str = THEME["line"], stroke_width: float = 2) -> None:
        asset = load_image_asset(path_value, base_dir=base_dir)
        if asset is None:
            self.add(rect(x, y, w, h, fill="#efe0c8", stroke=stroke, stroke_width=stroke_width, rx=8))
            self.add(line(x + 14, y + 14, x + w - 14, y + h - 14, stroke="#b79f84", stroke_width=2))
            self.add(line(x + w - 14, y + 14, x + 14, y + h - 14, stroke="#b79f84", stroke_width=2))
            self.add(text_block(x + w / 2, y + h / 2 + 6, [label], font_size=24, fill="#7f6d59", anchor="middle", weight=700))
            return
        self.counter += 1
        clip_id = f"clip-{self.counter}"
        self.defs.append(f'<clipPath id="{clip_id}">{rect(x, y, w, h, rx=8)}</clipPath>')
        mime, payload = asset
        data = base64.b64encode(payload).decode("ascii")
        fit = "xMidYMid slice" if mode == "cover" else "xMidYMid meet"
        self.add(f'<g clip-path="url(#{clip_id})"><image href="data:{mime};base64,{data}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="{fit}" /></g>')
        self.add(rect(x, y, w, h, fill="none", stroke=stroke, stroke_width=stroke_width, rx=8))

    def render(self) -> str:
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">{rect(0, 0, self.width, self.height, fill=self.background)}{defs}{"".join(self.items)}</svg>'


def panel_title(svg: Svg, title: str, *, x: float, y: float, w: float, size: float) -> None:
    svg.add(text_block(x + w / 2, y, [title], font_size=size, fill=THEME["ink"], anchor="middle", weight=800))


def compute_lunar_text(date_text: str) -> str:
    try:
        current_date = parse_base_date(date_text)
        return format_lunar_text(current_date)
    except (TypeError, ValueError):
        return ""


def resolve_base_date(spec: dict[str, Any], section: dict[str, Any] | None = None):
    if isinstance(section, dict):
        raw_value = section.get("base_date")
        if str(raw_value or "").strip():
            return parse_base_date(raw_value)
    return parse_base_date(spec.get("base_date"))


def load_json_payload(data_path: str, *, base_dir: Path) -> dict[str, Any]:
    path_text = str(data_path or "").strip()
    if not path_text:
        return {}
    source_path = Path(path_text)
    source_path = source_path if source_path.is_absolute() else (base_dir / source_path)
    source_path = source_path.resolve()
    if not source_path.exists():
        return {}
    return json.loads(source_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=8)
def fetch_json_payload(url: str, *, timeout: float = 6.0) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "daily-poster/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
        return {}


def resolve_holiday_schedule(spec: dict[str, Any], section: dict[str, Any] | None, *, base_dir: Path) -> tuple[list[Holiday], dict[str, Any]]:
    section = section if isinstance(section, dict) else {}
    loaded_payload = load_json_payload(str(section.get("data_path", "")), base_dir=base_dir)
    if not loaded_payload:
        countdown = spec.get("countdown", {})
        if isinstance(countdown, dict):
            loaded_payload = load_json_payload(str(countdown.get("data_path", "")), base_dir=base_dir)

    raw_schedule = spec.get("holiday_schedule")
    if not isinstance(raw_schedule, list):
        raw_schedule = loaded_payload.get("holiday_schedule")
    if not isinstance(raw_schedule, list):
        raw_schedule = section.get("holiday_schedule")
    return holidays_from_schedule(raw_schedule) or list(HOLIDAYS_2026), loaded_payload


def active_holiday(holidays: list[Holiday], current_date) -> Holiday | None:
    for holiday in holidays:
        if holiday.start <= current_date <= holiday.end:
            return holiday
    return None


def build_holiday_plan_rows(holiday: Holiday, *, current_date, limit: int = 6) -> list[dict[str, str]]:
    all_days = [holiday.start + timedelta(days=index) for index in range((holiday.end - holiday.start).days + 1)]
    if len(all_days) <= limit:
        visible_days = all_days
    else:
        current_index = max(0, min((current_date - holiday.start).days, len(all_days) - 1))
        window_start = min(max(current_index - 2, 0), len(all_days) - limit)
        visible_days = all_days[window_start : window_start + limit]

    rows: list[dict[str, str]] = []
    for index, day in enumerate(all_days, start=1):
        if day not in visible_days:
            continue
        if day == current_date:
            text = f"今天放假 · 第{index}天"
        elif day < current_date:
            text = f"已放假 · 第{index}天"
        else:
            text = f"放假 · 第{index}天"
        rows.append({"time": day.strftime("%m-%d"), "text": text})
    return rows


def resolve_header(spec: dict[str, Any]) -> dict[str, Any]:
    raw_header = spec.get("header", {})
    if not isinstance(raw_header, dict):
        return {}

    header = dict(raw_header)
    title = str(header.get("title", "")).strip()
    if title and not str(header.get("masthead", "")).strip():
        header["masthead"] = title
    auto_date = bool(header.get("auto_date")) or str(header.get("base_date", spec.get("base_date", ""))).strip().lower() in {"today", "auto"}
    if auto_date:
        current_date = resolve_base_date(spec, header)
        header["year_month"] = f"{current_date.year}年{current_date.month}月"
        header["day"] = str(current_date.day)
        header["weekday"] = WEEKDAY_LABELS[current_date.weekday()]
        auto_lunar = bool(header.get("auto_lunar")) or not str(header.get("lunar", "")).strip()
        if auto_lunar:
            header["lunar"] = compute_lunar_text(current_date.isoformat()) or str(header.get("lunar", "")).strip()
    return header


def resolve_personal_info(spec: dict[str, Any]) -> dict[str, Any]:
    raw_info = spec.get("personal_info", {})
    if not isinstance(raw_info, dict):
        return {}

    info = dict(raw_info)
    title = str(info.get("title", "")).strip() or str(info.get("name", "")).strip() or str(info.get("role", "")).strip()
    if title:
        info["title"] = title

    raw_text_lines = clean_text_lines(info.get("text_lines"), limit=2)
    if raw_text_lines:
        info["text_lines"] = raw_text_lines
    if "text_lines" not in info:
        bio_lines = clean_text_lines(info.get("bio_lines"), limit=2)
        bio = str(info.get("bio", "")).strip()
        signature = str(info.get("signature", "")).strip()
        if signature and not bio and not bio_lines:
            bio = signature
        if bio and not bio_lines:
            bio_lines = [bio]
        if bio_lines:
            info["text_lines"] = bio_lines
    return info


def normalize_daily_spec(spec: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    del base_dir
    normalized = dict(spec)
    normalized["poster_type"] = POSTER_TYPE

    if "header" in normalized and isinstance(normalized.get("header"), dict):
        header = normalized.get("header", {})
        header = dict(header)
        title = str(header.get("title", "")).strip()
        if title and not str(header.get("masthead", "")).strip():
            header["masthead"] = title
        normalized["header"] = header

    personal_info = normalized.get("personal_info", {})
    if isinstance(personal_info, dict):
        personal_info = dict(personal_info)
        signature = str(personal_info.get("signature", "")).strip()
        has_text = bool(personal_info.get("bio")) or bool(personal_info.get("bio_lines")) or bool(personal_info.get("text_lines"))
        if signature and not has_text:
            personal_info["bio"] = signature
        normalized["personal_info"] = personal_info

    return normalized


def apply_default_sections(spec: dict[str, Any]) -> dict[str, Any]:
    spec = dict(spec)
    if "header" not in spec:
        spec["header"] = {
            "auto_date": True,
            "auto_lunar": True,
            "masthead": "摸鱼日报",
            "show_issue_line": False,
        }
    if "lead_story" not in spec:
        spec["lead_story"] = {
            "auto_hot36kr": True,
            "title": "今日热点",
            "limit": 10,  # Increased to fill more content
            "intro": "",
            "stamp": "36氪热榜",
        }
    if "sidebar_note" not in spec:
        spec["sidebar_note"] = {
            "auto_heisi": True,
            "image_label": "今日黑丝",
        }
    if "plan_table" not in spec:
        spec["plan_table"] = {
            "auto_holiday": True,
            "title": "摸鱼计划表",
            "rows": list(DEFAULT_PLAN_ROWS),
        }
    if "countdown" not in spec:
        spec["countdown"] = {
            "data_path": str(REFERENCE_DIR / "holiday-countdown-2026.json"),
        }
    if "spotlight" not in spec:
        spec["spotlight"] = {
            "auto_horoscope": True,
            "title": "今日星座运势",
            "name": "水瓶座",
            "subtitle": "今日运势",
            "ratings": [
                {"label": "整体运势", "stars": 5},
                {"label": "爱情运势", "stars": 4},
                {"label": "事业运势", "stars": 4},
                {"label": "健康运势", "stars": 3},
                {"label": "财富运势", "stars": 4},
            ],
            "badges": ["摸鱼 八卦", "加班 熬夜"],
        }
    promo_defaults = {
        "title": "智普虾🦐",
        "text_lines": list(DEFAULT_PROMO_LINES),
    }
    personal_info = resolve_personal_info(spec)
    current_promo = spec.get("promo_card", {})
    if not isinstance(current_promo, dict):
        current_promo = {}
    spec["promo_card"] = {**promo_defaults, **personal_info, **current_promo}
    if "quote_card" not in spec:
        spec["quote_card"] = {
            "title": "",
            "auto_quote_api": True,
            "text": "人间凑数接口不可用时，会回退到这里的占位文案。",
            "source": "",
        }
    return spec


def resolve_lead_story(spec: dict[str, Any], *, base_dir: Path) -> dict[str, Any]:
    raw_story = spec.get("lead_story", {})
    if not isinstance(raw_story, dict):
        return {}

    story = dict(raw_story)
    auto_hot36kr = bool(story.get("auto_hot36kr"))
    auto_60s = bool(story.get("auto_60s"))
    if not auto_hot36kr and not auto_60s:
        return story

    default_url = "https://v2.xxapi.cn/api/hot36kr" if auto_hot36kr else "https://60s.viki.moe/v2/60s"
    api_url = str(story.get("api_url", default_url)).strip()
    payload = fetch_json_payload(api_url) if api_url else {}
    try:
        default_limit = 10 if auto_hot36kr else 6
        limit = int(story.get("limit", default_limit) or default_limit)
    except (TypeError, ValueError):
        limit = 10 if auto_hot36kr else 6
    limit = max(limit, 0)

    if auto_hot36kr:
        data = payload.get("data", []) if isinstance(payload, dict) else []
        if isinstance(data, list):
            news_items: list[str] = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                material = item.get("templateMaterial", {})
                if not isinstance(material, dict):
                    continue
                title = str(material.get("widgetTitle", "")).strip()
                if title:
                    news_items.append(title)
            if news_items:
                story["title"] = str(story.get("title", "")).strip() or "今日热点"
                story["bullets"] = news_items[:limit]
                story["intro"] = str(story.get("intro", "")).strip()
                story["stamp"] = str(story.get("stamp", "")).strip() or "36氪热榜"
        return story

    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    if not isinstance(data, dict):
        data = {}
    news_items = [str(item).strip() for item in listify(data.get("news")) if str(item).strip()]
    if news_items:
        story["title"] = str(story.get("title", "")).strip() or "每日60秒"
        story["bullets"] = news_items[:limit]
        tip = str(data.get("tip", "")).strip()
        response_date = str(data.get("date", "")).strip()
        response_weekday = str(data.get("day_of_week", "")).strip()
        fallback_intro = " · ".join(part for part in (response_date, response_weekday) if part)
        story["intro"] = tip or fallback_intro or str(story.get("intro", "")).strip()
        story["source"] = str(data.get("link", "")).strip()
    return story


def resolve_sidebar_note(spec: dict[str, Any]) -> dict[str, Any]:
    raw_note = spec.get("sidebar_note", {})
    if not isinstance(raw_note, dict):
        return {}

    note = dict(raw_note)
    cache_key = str(note.get("cache_key", "heisi-latest")).strip() or "heisi-latest"
    cached_image = find_cached_image(cache_key)
    if not bool(note.get("auto_heisi")):
        if not str(note.get("image_path", "")).strip() and cached_image is not None:
            note["image_path"] = str(cached_image)
        return note

    api_url = str(note.get("api_url", "https://v2.xxapi.cn/api/heisi")).strip()
    payload = fetch_json_payload(api_url) if api_url else {}
    if not isinstance(payload, dict):
        if cached_image is not None:
            note["image_path"] = str(cached_image)
        return note

    image_url = str(payload.get("data", "")).strip()
    if image_url:
        cached_path = cache_remote_image(image_url, cache_key=cache_key)
        note["image_path"] = str(cached_path) if cached_path is not None else image_url
    elif cached_image is not None:
        note["image_path"] = str(cached_image)
    note["title"] = str(note.get("title", "")).strip() or "三天打鱼两天晒网"
    return note


def resolve_quote_card(spec: dict[str, Any]) -> dict[str, Any]:
    raw_quote = spec.get("quote_card", {})
    if not isinstance(raw_quote, dict):
        return {}

    quote = dict(raw_quote)
    auto_quote_api = bool(quote.get("auto_quote_api")) or bool(quote.get("auto_renjian")) or bool(quote.get("auto_dujitang"))
    if not auto_quote_api:
        return quote

    api_url = str(quote.get("api_url", "https://v2.xxapi.cn/api/renjian")).strip()

    # Try to fetch quote, retry if text is too long (more than 4 lines)
    max_retries = 3
    for attempt in range(max_retries):
        payload = fetch_json_payload(api_url) if api_url else {}
        if not isinstance(payload, dict):
            break

        data = payload.get("data")
        text = str(data).strip() if isinstance(data, str) else ""
        if text:
            text, source_suffix = split_quote_text_source(text)
            # Check if text is too long (more than 4 lines when wrapped)
            wrapped = wrap_text(text, 680, 26)
            if len(wrapped) <= 4 or attempt == max_retries - 1:
                if source_suffix:
                    quote["source_suffix"] = source_suffix
                quote["text"] = text
                break
            # Text too long, retry with new quote
            continue

    source = str(quote.get("source", "")).strip()
    quote["source"] = "" if source == "摸鱼办" else source
    return quote


def resolve_spotlight(spec: dict[str, Any]) -> dict[str, Any]:
    raw_card = spec.get("spotlight", {})
    if not isinstance(raw_card, dict):
        return {}

    card = dict(raw_card)
    if not bool(card.get("auto_horoscope")):
        return card

    api_url = str(card.get("api_url", "")).strip()
    if not api_url:
        query = urlencode(
            {
                "type": str(card.get("type", "aquarius")).strip() or "aquarius",
                "time": str(card.get("time", "today")).strip() or "today",
            }
        )
        api_url = f"https://v2.xxapi.cn/api/horoscope?{query}"

    payload = fetch_json_payload(api_url) if api_url else {}
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    if not isinstance(data, dict):
        return card

    fortune = data.get("fortune", {})
    todo = data.get("todo", {})
    if not isinstance(fortune, dict):
        fortune = {}
    if not isinstance(todo, dict):
        todo = {}

    card["title"] = str(card.get("title", "")).strip() or "今日星座运势"
    card["name"] = str(data.get("title", "")).strip() or str(card.get("name", "")).strip() or "水瓶座"

    time_text = str(data.get("time", "")).strip()
    short_comment = str(data.get("shortcomment", "")).strip()
    subtitle = " · ".join(part for part in (time_text, short_comment) if part)
    card["subtitle"] = subtitle or str(card.get("subtitle", "")).strip()

    rating_order = [
        ("整体运势", "all"),
        ("爱情运势", "love"),
        ("事业运势", "work"),
        ("健康运势", "health"),
        ("财富运势", "money"),
    ]
    ratings: list[dict[str, Any]] = []
    for label, key in rating_order:
        try:
            stars = int(fortune.get(key, 0) or 0)
        except (TypeError, ValueError):
            stars = 0
        ratings.append({"label": label, "stars": max(0, min(stars, 5))})
    if any(item["stars"] > 0 for item in ratings):
        card["ratings"] = ratings

    yi_text = str(todo.get("yi", "")).strip().removeprefix("宜")
    ji_text = str(todo.get("ji", "")).strip().removeprefix("忌")
    badges = [value for value in (yi_text, ji_text) if value]
    if badges:
        card["badges"] = badges[:2]
    return card


def resolve_countdown(spec: dict[str, Any], *, base_dir: Path) -> dict[str, Any]:
    raw_countdown = spec.get("countdown", {})
    if not isinstance(raw_countdown, dict):
        return {}

    countdown = dict(raw_countdown)
    holidays, loaded_payload = resolve_holiday_schedule(spec, countdown, base_dir=base_dir)
    loaded_countdown = loaded_payload.get("countdown", {})
    if isinstance(loaded_countdown, dict):
        countdown = {**loaded_countdown, **countdown}

    auto_update = bool(countdown.get("auto_update")) or str(countdown.get("base_date", spec.get("base_date", ""))).strip().lower() in {"today", "auto"}
    if auto_update:
        try:
            limit = int(countdown.get("limit", 4) or 4)
        except (TypeError, ValueError):
            limit = 4
        countdown["items"] = build_countdown_items(holidays, base_date=resolve_base_date(spec, countdown), limit=limit)
    return countdown


def resolve_plan(spec: dict[str, Any], *, base_dir: Path) -> dict[str, Any]:
    raw_plan = spec.get("plan_table", {})
    if not isinstance(raw_plan, dict):
        return {}

    plan = dict(raw_plan)
    auto_holiday = bool(plan.get("auto_holiday"))
    if not auto_holiday:
        return plan

    holidays, _ = resolve_holiday_schedule(spec, plan, base_dir=base_dir)
    current_date = resolve_base_date(spec, plan)
    holiday = active_holiday(holidays, current_date)
    if holiday is None:
        return plan

    plan["title"] = f"{holiday.name}安排"
    plan["rows"] = build_holiday_plan_rows(holiday, current_date=current_date)
    return plan


def draw_header(svg: Svg, spec: dict[str, Any], width: int) -> None:
    header = spec.get("header", {})
    subtitle = str(header.get("subtitle", "")).strip()
    has_subtitle = bool(subtitle)
    show_issue_line = bool(header.get("show_issue_line"))
    date_x = width - 280
    masthead_x = 50
    masthead_y = 70 if has_subtitle else 38
    masthead_w = max(540, date_x - masthead_x - 24)
    masthead_h = 156 if has_subtitle else 188
    subtitle_size = 20
    subtitle_y = 48

    svg.add(rect(36, 30, width - 72, svg.height - 66, fill="none", stroke=THEME["line"], stroke_width=4))
    if has_subtitle:
        svg.add(
            text_block(
                52,
                subtitle_y,
                [subtitle],
                font_size=subtitle_size,
                fill=THEME["ink"],
                weight=600,
            )
        )
    masthead_text = str(header.get("masthead", "摸鱼日报"))
    masthead_font_size = fit_single_line_font_size(
        masthead_text,
        max_width=masthead_w - 44,
        max_height=masthead_h - 26,
        max_size=168,
        min_size=96,
    )
    # Approximate the optical center of a single-line headline inside the red block.
    masthead_text_y = masthead_y + masthead_h / 2 + masthead_font_size * 0.31
    svg.add(rect(masthead_x, masthead_y, masthead_w, masthead_h, fill=THEME["accent"], stroke=THEME["line"], stroke_width=3, rx=4))
    svg.add(
        text_block(
            masthead_x + masthead_w / 2,
            masthead_text_y,
            [masthead_text],
            font_size=masthead_font_size,
            fill="#fff8eb",
            anchor="middle",
            weight=800,
            letter_spacing=1,
        )
    )
    svg.add(rect(date_x, 38, 210, 188, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    svg.add(text_block(date_x + 105, 72, [str(header.get("year_month", ""))], font_size=26, fill=THEME["ink"], anchor="middle", weight=800))
    svg.add(line(date_x + 20, 86, date_x + 190, 86, stroke=THEME["soft"], stroke_width=2))
    weekday = str(header.get("weekday", "")).strip()
    day_text = str(header.get("day", "")).strip()
    weekday_lines = [weekday] if weekday else []
    if weekday.startswith("星期") and len(weekday) >= 3:
        weekday_lines = ["星期", weekday[-1]]
    svg.add(text_block(date_x + 60, 152, [day_text], font_size=74, fill=THEME["ink"], anchor="middle", weight=800))
    if len(weekday_lines) == 2:
        svg.add(
            text_block(
                date_x + 155,
                118,
                weekday_lines,
                font_size=24,
                fill=THEME["ink"],
                anchor="middle",
                weight=700,
                line_height=32,
            )
        )
    else:
        svg.add(text_block(date_x + 155, 144, weekday_lines, font_size=22, fill=THEME["ink"], anchor="middle", weight=700))
    svg.add(line(date_x + 20, 172, date_x + 190, 172, stroke=THEME["soft"], stroke_width=2))
    svg.add(text_block(date_x + 105, 202, [str(header.get("lunar", ""))], font_size=22, fill=THEME["ink"], anchor="middle", weight=700))
    if show_issue_line:
        issue = str(header.get("issue", "总第 137 期")).strip()
        tags = "  ·  ".join(str(item) for item in listify(header.get("tags") or ["专业版", "打工摸鱼"]))
        meta_text = f"{issue}  ·  {tags}".strip(" ·")
        if meta_text:
            svg.add(line(58, 204, 818, 204, stroke=THEME["line"], stroke_width=2))
            svg.add(text_block(438, 224, [meta_text], font_size=22, fill=THEME["ink"], anchor="middle", weight=700))
    divider_y = 242 if show_issue_line else 236
    svg.add(line(48, divider_y, width - 48, divider_y, stroke=THEME["line"], stroke_width=4))


def draw_lead(svg: Svg, spec: dict[str, Any], base_dir: Path) -> None:
    story = spec.get("lead_story", {})
    x, y, w, h = 54, 268, 760, 690
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    panel_title(svg, str(story.get("title", "今日热点")), x=x, y=y + 74, w=w, size=58)

    # Lead Body without images
    text_left = x + 40
    text_right = x + w - 40
    max_width = text_right - text_left
    cursor_y = y + 134
    intro = str(story.get("intro", "")).strip()
    if intro:
        intro_lines = trim_lines(wrap_text(intro, max_width, 28), 3)
        svg.add(text_block(text_left, cursor_y, intro_lines, font_size=28, fill=THEME["ink"], weight=700, line_height=38))
        cursor_y += len(intro_lines) * 38 + 14

    for index, bullet in enumerate(listify(story.get("bullets")), start=1):
        bullet_lines = trim_lines(wrap_with_prefix(f"{index}. ", str(bullet), max_width, 27), 8)
        svg.add(text_block(text_left, cursor_y, bullet_lines, font_size=27, fill=THEME["ink"], weight=500, line_height=39))
        cursor_y += len(bullet_lines) * 39 + 18
        if cursor_y > y + h - 48:
            break


def draw_note(svg: Svg, spec: dict[str, Any], base_dir: Path) -> None:
    note = spec.get("sidebar_note", {})
    x, y, w, h = 838, 268, 350, 360
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    title = str(note.get("title", "三天打鱼两天晒网")).replace("\n", " ")
    svg.image(
        note.get("image_path"),
        base_dir=base_dir,
        x=x + 10,
        y=y + 10,
        w=w - 20,
        h=h - 20,
        mode=str(note.get("image_mode", "cover")),
        label=str(note.get("image_label", title or "摸鱼图鉴")),
    )


def draw_plan(svg: Svg, spec: dict[str, Any]) -> None:
    plan = spec.get("plan_table", {})
    x, y, w, h = 838, 648, 350, 308
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    panel_title(svg, str(plan.get("title", "摸鱼计划表")), x=x, y=y + 42, w=w, size=30)
    split = x + 110
    top = y + 94
    svg.add(line(split, top - 10, split, y + h - 24, stroke=THEME["soft"], stroke_width=2))
    for index, row in enumerate(listify(plan.get("rows"))[:6]):
        row_y = top + index * 37
        if index > 0:
            svg.add(line(split + 18, row_y - 14, x + w - 24, row_y - 14, stroke=THEME["soft"], stroke_width=1.5))
        svg.add(text_block(x + 54, row_y + 4, [str(row.get("time", ""))], font_size=22, fill=THEME["ink"], anchor="middle", weight=800, line_height=22))
        detail = trim_lines(wrap_text(str(row.get("text", "")), w - 156, 19), 1)
        svg.add(text_block(split + 34, row_y + 2, detail, font_size=20, fill=THEME["ink"], weight=700, line_height=20))


def draw_countdown(svg: Svg, spec: dict[str, Any]) -> None:
    countdown = spec.get("countdown", {})
    x, y, w, h = 838, 982, 350, 230
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    panel_title(svg, str(countdown.get("title", "假期倒计时")), x=x, y=y + 44, w=w, size=32)
    cursor = y + 92
    for item in listify(countdown.get("items"))[:4]:
        svg.add(text_block(x + 24, cursor, [str(item.get("label", ""))], font_size=21, fill=THEME["muted"], weight=700))
        svg.add(text_block(x + w - 24, cursor, [str(item.get("value", ""))], font_size=25, fill=THEME["ink"], anchor="end", weight=800))
        cursor += 34


def draw_spotlight(svg: Svg, spec: dict[str, Any], base_dir: Path) -> None:
    card = spec.get("spotlight", {})
    x, y, w, h = 54, 982, 760, 230
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    
    # Left partition line
    svg.add(line(x + 230, y + 16, x + 230, y + h - 16, stroke=THEME["soft"], stroke_width=2))
    
    # Left partition text
    svg.add(text_block(x + 115, y + 50, [str(card.get("title", "今日最佳星座"))], font_size=26, fill=THEME["ink"], anchor="middle", weight=800))
    svg.add(text_block(x + 115, y + 140, [str(card.get("name", "金牛座"))], font_size=48, fill=THEME["ink"], anchor="middle", weight=800))
    svg.add(text_block(x + 115, y + 184, [str(card.get("subtitle", "4月20日 - 5月20日"))], font_size=16, fill=THEME["muted"], anchor="middle", weight=700))
    
    # Right partition line for Almanac
    svg.add(line(x + w - 160, y + 16, x + w - 160, y + h - 16, stroke=THEME["soft"], stroke_width=2))

    # Ratings in the middle
    rate_y = y + 42
    for item in listify(card.get("ratings"))[:5]:
        stars = max(0, min(int(item.get("stars", 4)), 5))
        svg.add(text_block(x + 270, rate_y, [str(item.get("label", ""))], font_size=20, fill=THEME["ink"], weight=700))
        svg.add(text_block(x + 390, rate_y, ["★" * stars + "☆" * (5 - stars)], font_size=20, fill=THEME["stamp"], weight=800))
        rate_y += 36
        
    # Badges on the right
    badge_y = y + 60
    for index, badge in enumerate(listify(card.get("badges") or ["摸鱼 八卦", "加班 熬夜"])[:2]):
        bg_color = THEME["ink"] if index == 0 else "#efdebf"
        text_color = "#fff8eb" if index == 0 else THEME["ink"]
        label = "宜" if index == 0 else "忌"
        svg.add(circle(x + w - 80, badge_y, 28, fill=bg_color, stroke=THEME["line"], stroke_width=2))
        svg.add(text_block(x + w - 80, badge_y + 8, [label], font_size=24, fill=text_color, anchor="middle", weight=800))
        badge_lines = trim_lines(wrap_text(str(badge), 46, 15), 2)
        svg.add(text_block(x + w - 80, badge_y + 44, badge_lines, font_size=15, fill=THEME["ink"], anchor="middle", weight=800, line_height=17))
        badge_y += 100


def draw_promo(svg: Svg, spec: dict[str, Any], base_dir: Path) -> None:
    promo = spec.get("promo_card", {})
    x, y, w = 838, 1226, 350  # Moved below spotlight
    h = 140  # Smaller height for more content but fits in layout
    title = str(promo.get("title", "智普虾🦐")).strip()
    body: list[str] = []
    for item in listify(promo.get("text_lines")):
        body.extend(wrap_text(str(item), 280, 18))
    body_lines = trim_lines(body, 4)  # Allow up to 4 lines

    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    svg.add(rect(x + 12, y + 12, w - 24, h - 24, fill="none", stroke=THEME["soft"], stroke_width=2))
    if title:
        svg.add(text_block(x + w / 2, y + 36, [title], font_size=26, fill=THEME["accent"], anchor="middle", weight=800, line_height=28))
        svg.add(line(x + 32, y + 50, x + w - 32, y + 50, stroke=THEME["line"], stroke_width=2))
    if body_lines:
        svg.add(text_block(x + w / 2, y + 72, body_lines, font_size=17, fill=THEME["ink"], anchor="middle", weight=600, line_height=24))



def draw_quote(svg: Svg, spec: dict[str, Any], base_dir: Path) -> None:
    quote = spec.get("quote_card", {})
    x, y, w = 54, 1226, 760  # Below spotlight
    h = 140  # Smaller height
    title = str(quote.get("title", "")).strip()
    quote_text, inline_suffix = split_quote_text_source(str(quote.get("text", "一句大字文案。")))
    main_lines = trim_lines(wrap_text(quote_text, 680, 26), 2)  # Max 2 lines
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    text_y = y + 70
    if title:
        svg.add(text_block(x + w / 2, y + 36, [title], font_size=30, fill=THEME["ink"], anchor="middle", weight=800))
        text_y = y + 72

    if main_lines:
        svg.add(text_block(x + w / 2, text_y, main_lines, font_size=24, fill=THEME["ink"], anchor="middle", weight=700, line_height=32))
    source = str(quote.get("source", "")).strip()
    if source == "摸鱼办":
        source = ""
    source_suffix = str(quote.get("source_suffix", "")).strip() or inline_suffix
    source_line = " ".join(part for part in (source, source_suffix) if part)
    if source_line:
        svg.add(text_block(x + w - 24, y + h - 16, [source_line], font_size=16, fill=THEME["muted"], anchor="end", weight=700))


def draw_footer(svg: Svg, spec: dict[str, Any]) -> None:
    footer = spec.get("footer", {})
    x, y, w, h = 838, 1236, 350, 170
    svg.add(rect(x, y, w, h, fill=THEME["panel"], stroke=THEME["line"], stroke_width=3))
    
    # Title Section
    title_text = str(footer.get("title", "自律3650天挑战"))
    svg.add(text_block(x + 50, y + 36, [f"📢 {title_text}"], font_size=24, fill=THEME["ink"], weight=800))
    svg.add(line(x + 18, y + 54, x + w - 18, y + 54, stroke=THEME["soft"], stroke_width=2))
    
    # Project Section
    project_label = str(footer.get("project_label", "项目：打工"))
    svg.add(text_block(x + w / 2, y + 96, [project_label], font_size=26, fill=THEME["ink"], anchor="middle", weight=800))
    svg.add(line(x + 18, y + 120, x + w - 18, y + 120, stroke=THEME["soft"], stroke_width=2))
    
    # Checkbox Section
    summary = str(footer.get("summary", "打卡第 137 天"))
    svg.add(text_block(x + 24, y + 152, [summary], font_size=28, fill=THEME["ink"], weight=800))
    
    check_y = y + 138
    for index, item in enumerate(listify(footer.get("checklist") or [{"label": "成功", "checked": True}, {"label": "失败", "checked": False}])[:2]):
        box_x = x + 280
        row_y = check_y + (index * 20)
        svg.add(rect(box_x, row_y - 12, 14, 14, fill="#fff8eb", stroke=THEME["line"], stroke_width=2, rx=2))
        if bool(item.get("checked", False)):
            svg.add(text_block(box_x + 7, row_y - 2, ["✓"], font_size=14, fill=THEME["accent"], anchor="middle", weight=900))
        svg.add(text_block(box_x - 6, row_y, [str(item.get("label", ""))], font_size=16, fill=THEME["ink"], anchor="end", weight=700))


def draw_decorations(svg: Svg, spec: dict[str, Any], base_dir: Path) -> None:
    for item in listify(spec.get("decorations")):
        svg.image(
            item.get("image_path"),
            base_dir=base_dir,
            x=float(item.get("x", 0)),
            y=float(item.get("y", 0)),
            w=float(item.get("width", 84)),
            h=float(item.get("height", 84)),
            mode=str(item.get("mode", "contain")),
            label=str(item.get("label", "贴图")),
            stroke="none",
            stroke_width=0,
        )
    svg.add(line(54, 972, 1188, 972, stroke=THEME["line"], stroke_width=2))
    svg.add(line(54, 1380, 1188, 1380, stroke=THEME["line"], stroke_width=2))


def render_poster(spec: dict[str, Any], *, base_dir: Path) -> str:
    spec = apply_default_sections(spec)
    if "header" in spec:
        spec = {**spec, "header": resolve_header(spec)}
    if "lead_story" in spec:
        spec = {**spec, "lead_story": resolve_lead_story(spec, base_dir=base_dir)}
    if "sidebar_note" in spec:
        spec = {**spec, "sidebar_note": resolve_sidebar_note(spec)}
    if "spotlight" in spec:
        spec = {**spec, "spotlight": resolve_spotlight(spec)}
    if "quote_card" in spec:
        spec = {**spec, "quote_card": resolve_quote_card(spec)}
    if "plan_table" in spec:
        spec = {**spec, "plan_table": resolve_plan(spec, base_dir=base_dir)}
    if "countdown" in spec:
        spec = {**spec, "countdown": resolve_countdown(spec, base_dir=base_dir)}
    width = int(dig(spec, "canvas.width", 1242))
    height = int(dig(spec, "canvas.height", 1446))
    THEME.clear()
    THEME.update(BASE_THEME)
    THEME.update(spec.get("theme", {}))
    svg = Svg(width, height, THEME["paper"])
    draw_header(svg, spec, width)
    draw_lead(svg, spec, base_dir)
    draw_note(svg, spec, base_dir)
    draw_plan(svg, spec)
    draw_countdown(svg, spec)
    draw_spotlight(svg, spec, base_dir)
    if isinstance(spec.get("promo_card"), dict) and spec.get("promo_card"):
        draw_promo(svg, spec, base_dir)
    draw_quote(svg, spec, base_dir)
    if isinstance(spec.get("footer"), dict) and spec.get("footer") and not bool(spec.get("footer", {}).get("hidden")):
        draw_footer(svg, spec)
    draw_decorations(svg, spec, base_dir)
    return svg.render()


def main() -> None:
    run_renderer_cli(
        poster_type=POSTER_TYPE,
        description="Render a newspaper-style poster from JSON and optionally convert it to image formats.",
        render_svg=render_poster,
        default_scale=DEFAULT_OUTPUT_SCALE,
        default_background=DEFAULT_OUTPUT_BACKGROUND,
        prepare_spec=normalize_daily_spec,
    )


if __name__ == "__main__":
    main()
