#!/usr/bin/env python3
"""Validate and render a campus morning brief using only the Python standard library."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys
from typing import Any


AGE_GROUPS = {"primary-school", "middle-school", "high-school", "college"}
REQUIRED_TOP_LEVEL = {
    "date",
    "profile",
    "weather",
    "quote",
    "general_news",
    "interest_news",
    "study_tip",
    "action_anchor",
}


class BriefValidationError(ValueError):
    pass


def require_text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BriefValidationError(f"{path} must be a non-empty string")
    return value.strip()


def require_date(value: Any, path: str) -> str:
    text = require_text(value, path)
    try:
        dt.date.fromisoformat(text)
    except ValueError as exc:
        raise BriefValidationError(f"{path} must use YYYY-MM-DD") from exc
    return text


def require_url(value: Any, path: str) -> str:
    text = require_text(value, path)
    if not re.fullmatch(r"https?://[^\s/?#]+(?:[^\s]*)?", text, flags=re.IGNORECASE):
        raise BriefValidationError(f"{path} must be an absolute HTTP(S) URL")
    return text


def require_number(value: Any, path: str) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BriefValidationError(f"{path} must be a number")
    return value


def validate_news(items: Any, path: str) -> list[dict[str, Any]]:
    if not isinstance(items, list) or not items:
        raise BriefValidationError(f"{path} must be a non-empty array")
    validated: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            raise BriefValidationError(f"{item_path} must be an object")
        clean = dict(item)
        for key in ("title", "summary", "publisher"):
            clean[key] = require_text(item.get(key), f"{item_path}.{key}")
        clean["published_date"] = require_date(item.get("published_date"), f"{item_path}.published_date")
        clean["url"] = require_url(item.get("url"), f"{item_path}.url")
        if "category" in clean:
            clean["category"] = require_text(clean["category"], f"{item_path}.category")
        validated.append(clean)
    return validated


def validate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise BriefValidationError("root must be a JSON object")
    missing = sorted(REQUIRED_TOP_LEVEL - payload.keys())
    if missing:
        raise BriefValidationError(f"missing required fields: {', '.join(missing)}")

    clean = dict(payload)
    clean["date"] = require_date(payload["date"], "date")

    profile = payload["profile"]
    if not isinstance(profile, dict):
        raise BriefValidationError("profile must be an object")
    clean_profile = dict(profile)
    for key in ("display_name", "city", "language"):
        clean_profile[key] = require_text(profile.get(key), f"profile.{key}")
    age_group = require_text(profile.get("age_group"), "profile.age_group")
    if age_group not in AGE_GROUPS:
        raise BriefValidationError(f"profile.age_group must be one of: {', '.join(sorted(AGE_GROUPS))}")
    clean_profile["age_group"] = age_group
    clean["profile"] = clean_profile

    weather = payload["weather"]
    if not isinstance(weather, dict):
        raise BriefValidationError("weather must be an object")
    clean_weather = dict(weather)
    for key in ("condition", "outfit", "campus_tip"):
        clean_weather[key] = require_text(weather.get(key), f"weather.{key}")
    clean_weather["low_c"] = require_number(weather.get("low_c"), "weather.low_c")
    clean_weather["high_c"] = require_number(weather.get("high_c"), "weather.high_c")
    if clean_weather["low_c"] > clean_weather["high_c"]:
        raise BriefValidationError("weather.low_c cannot exceed weather.high_c")
    rain = weather.get("rain_probability")
    if rain is not None:
        rain = require_number(rain, "weather.rain_probability")
        if not 0 <= rain <= 100:
            raise BriefValidationError("weather.rain_probability must be between 0 and 100")
    clean_weather["rain_probability"] = rain
    if weather.get("source_url"):
        clean_weather["source_url"] = require_url(weather["source_url"], "weather.source_url")
    clean["weather"] = clean_weather

    quote = payload["quote"]
    if not isinstance(quote, dict):
        raise BriefValidationError("quote must be an object")
    clean["quote"] = {
        key: require_text(quote.get(key), f"quote.{key}")
        for key in ("primary", "english", "author")
    }
    clean["general_news"] = validate_news(payload["general_news"], "general_news")
    clean["interest_news"] = validate_news(payload["interest_news"], "interest_news")
    clean["study_tip"] = require_text(payload["study_tip"], "study_tip")
    clean["action_anchor"] = require_text(payload["action_anchor"], "action_anchor")

    reminders = payload.get("reminders", [])
    if not isinstance(reminders, list):
        raise BriefValidationError("reminders must be an array")
    clean["reminders"] = [require_text(item, f"reminders[{index}]") for index, item in enumerate(reminders)]
    return clean


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def weather_line(payload: dict[str, Any]) -> str:
    weather = payload["weather"]
    rain = weather.get("rain_probability")
    rain_text = f" · 降水概率 {rain:g}%" if isinstance(rain, (int, float)) else ""
    return f"{weather['condition']} · {weather['low_c']:g}–{weather['high_c']:g}°C{rain_text}"


def news_markdown(items: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for item in items:
        label = f" · {item['category']}" if item.get("category") else ""
        lines.append(
            f"- **[{item['title']}]({item['url']})**{label} — {item['summary']} "
            f"（{item['publisher']}，{item['published_date']}）"
        )
    return "\n".join(lines)


def render_markdown(payload: dict[str, Any]) -> str:
    profile = payload["profile"]
    weather = payload["weather"]
    reminder_block = ""
    if payload["reminders"]:
        reminder_block = "\n## 今日提醒\n\n" + "\n".join(f"- {item}" for item in payload["reminders"]) + "\n"
    return f"""# {profile['display_name']}的校园晨报

{payload['date']} · {profile['city']}

## 今日天气

**{weather_line(payload)}**

- 穿衣：{weather['outfit']}
- 校园提示：{weather['campus_tip']}

## 今日一句

> {payload['quote']['primary']}<br>
> {payload['quote']['english']}<br>
> — {payload['quote']['author']}

## 综合要闻

{news_markdown(payload['general_news'])}

## 兴趣拓展

{news_markdown(payload['interest_news'])}

## 学习方法

{payload['study_tip']}
{reminder_block}
## 现在就做

**{payload['action_anchor']}**
"""


def news_html(items: list[dict[str, Any]]) -> str:
    cards = []
    for item in items:
        category = f'<span class="tag">{esc(item["category"])}</span>' if item.get("category") else ""
        cards.append(
            '<article class="news">'
            f'<h3><a href="{esc(item["url"])}">{esc(item["title"])}</a>{category}</h3>'
            f'<p>{esc(item["summary"])}</p>'
            f'<small>{esc(item["publisher"])} · {esc(item["published_date"])}</small>'
            "</article>"
        )
    return "".join(cards)


def render_html(payload: dict[str, Any]) -> str:
    profile = payload["profile"]
    weather = payload["weather"]
    reminders = ""
    if payload["reminders"]:
        items = "".join(f"<li>{esc(item)}</li>" for item in payload["reminders"])
        reminders = f'<section><h2>今日提醒</h2><ul>{items}</ul></section>'
    return f"""<!doctype html>
<html lang="{esc(profile['language'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(profile['display_name'])}的校园晨报 · {esc(payload['date'])}</title>
<style>
@page {{ size: A4; margin: 11mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: #172034; background: #eef3f8; font: 14px/1.45 system-ui,-apple-system,"Segoe UI","PingFang SC",sans-serif; }}
.page {{ width: 210mm; min-height: 297mm; margin: 12px auto; padding: 11mm; background: #fff; box-shadow: 0 4px 24px #22334d22; }}
header {{ display: flex; justify-content: space-between; gap: 24px; align-items: end; padding-bottom: 12px; border-bottom: 3px solid #215f88; }}
h1 {{ margin: 0; color: #164d70; font-size: 28px; }}
.date {{ text-align: right; color: #5c6a77; }}
.weather {{ margin: 13px 0; padding: 12px 14px; border-radius: 10px; background: #e8f4fa; }}
.weather strong {{ font-size: 17px; }}
.weather p {{ margin: 4px 0 0; }}
.quote {{ margin: 12px 0; padding: 8px 14px; border-left: 4px solid #e3a72f; background: #fff9e9; }}
.quote p {{ margin: 3px 0; }}
.grid {{ display: grid; grid-template-columns: 1.15fr .85fr; gap: 14px; }}
section {{ break-inside: avoid; }}
h2 {{ margin: 12px 0 6px; color: #1b587e; font-size: 17px; }}
.news {{ padding: 7px 0; border-bottom: 1px solid #dfe6eb; break-inside: avoid; }}
.news:last-child {{ border-bottom: 0; }}
.news h3 {{ margin: 0 0 3px; font-size: 14px; line-height: 1.35; }}
.news p {{ margin: 0 0 3px; }}
.news a {{ color: #172034; text-decoration: none; }}
.news small {{ color: #687783; }}
.tag {{ margin-left: 6px; padding: 1px 5px; border-radius: 4px; color: #1b587e; background: #deedf5; font-size: 11px; font-weight: 500; }}
.tip {{ padding: 9px 11px; border-radius: 8px; background: #f3f6f8; }}
.action {{ margin-top: 12px; padding: 11px 14px; border-radius: 8px; color: #fff; background: #215f88; font-size: 16px; font-weight: 700; }}
ul {{ margin: 4px 0; padding-left: 20px; }}
@media print {{ body {{ background: #fff; }} .page {{ margin: 0; box-shadow: none; }} }}
@media (max-width: 760px) {{ .page {{ width: 100%; min-height: 0; margin: 0; padding: 20px; }} .grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body><main class="page">
<header><h1>{esc(profile['display_name'])}的校园晨报</h1><div class="date">{esc(payload['date'])}<br>{esc(profile['city'])}</div></header>
<div class="weather"><strong>{esc(weather_line(payload))}</strong><p>穿衣：{esc(weather['outfit'])}</p><p>校园提示：{esc(weather['campus_tip'])}</p></div>
<div class="quote"><p>{esc(payload['quote']['primary'])}</p><p>{esc(payload['quote']['english'])}</p><p>— {esc(payload['quote']['author'])}</p></div>
<div class="grid">
<div><section><h2>综合要闻</h2>{news_html(payload['general_news'])}</section></div>
<div><section><h2>兴趣拓展</h2>{news_html(payload['interest_news'])}</section><section><h2>学习方法</h2><div class="tip">{esc(payload['study_tip'])}</div></section>{reminders}</div>
</div>
<div class="action">现在就做：{esc(payload['action_anchor'])}</div>
</main></body></html>
"""


def write_text(path: pathlib.Path, value: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=pathlib.Path, help="Path to brief JSON")
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("output"))
    args = parser.parse_args()

    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        payload = validate(raw)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        markdown_path = args.output_dir / "morning-brief.md"
        html_path = args.output_dir / "morning-brief.html"
        metadata_path = args.output_dir / "metadata.json"
        write_text(markdown_path, render_markdown(payload))
        write_text(html_path, render_html(payload))
        metadata = {
            "schema_version": 1,
            "date": payload["date"],
            "profile": payload["profile"],
            "sources": [
                {key: item[key] for key in ("title", "publisher", "published_date", "url")}
                for item in payload["general_news"] + payload["interest_news"]
            ],
            "outputs": {"markdown": str(markdown_path.resolve()), "html": str(html_path.resolve())},
        }
        write_text(metadata_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    except (OSError, json.JSONDecodeError, BriefValidationError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps({"ok": True, "outputs": metadata["outputs"], "metadata": str(metadata_path.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
