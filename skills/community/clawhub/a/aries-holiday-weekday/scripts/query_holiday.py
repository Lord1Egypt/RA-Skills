#!/usr/bin/env python3
"""gov.cn holiday notice helpers and cache-aware weekday queries."""

from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable

import requests


BASE_URL = "https://sousuoht.www.gov.cn"
SEARCH_PATH = "/athena/forward/2B22E8E39E850E17F95A016A74FCB6B673336FA8B6FEC0E2955907EF9AEE06BE"
ATHENA_APP_KEY = (
    "HHLciEtNtf9vkOtsJSmb4ZQfpB%2BMXw%2BeyOdHmF7ux1azvif74nniAN1XVWjYGM8gbOutLgJZT66T4D%2FPmaEpr4IcWfkmlJYdxMKkM%2BWB6yndPRS8%2FalFiBkQ2YIBn3WDNvGIUdKBBUjrTYN9DFRXGwkAbiRUbBk5I0fxFsIkI9E%3D"
)
ATHENA_APP_NAME = "%E5%9B%BD%E7%BD%91%E6%90%9C%E7%B4%A2"
ATHENA_KEY = "irs-c-box"
ATHENA_SECRET = "99b2eeecb4f10339"
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"


@dataclass
class SearchHit:
    title: str
    url: str
    score: float
    summary: str | None = None
    time: str | None = None
    raw: dict[str, Any] | None = None


def md5_hex(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def build_sign(timestamp_ms: int) -> str:
    return md5_hex(f"{ATHENA_KEY}{ATHENA_SECRET}{timestamp_ms}TRS")


def build_search_payload(search_word: str, page_no: int = 1, page_size: int = 10) -> dict[str, Any]:
    return {
        "code": "17da70961a7",
        "historySearchWords": [search_word],
        "dataTypeId": "107",
        "orderBy": "time",
        "searchBy": "title",
        "appendixType": "",
        "granularity": "ALL",
        "trackTotalHits": True,
        "beginDateTime": "",
        "endDateTime": "",
        "isSearchForced": 0,
        "filters": [],
        "pageNo": page_no,
        "pageSize": page_size,
        "customFilter": {"operator": "and", "properties": []},
        "searchWord": search_word,
    }


def build_search_headers(search_word: str, timestamp_ms: int) -> dict[str, str]:
    referer = (
        "https://sousuo.www.gov.cn/sousuo/search.shtml?"
        f"code=17da70961a7&dataTypeId=107&searchWord={requests.utils.quote(search_word)}"
    )
    return {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": BASE_URL,
        "Referer": referer,
        "athenaAppKey": ATHENA_APP_KEY,
        "athenaAppName": ATHENA_APP_NAME,
        "T-KEY": ATHENA_KEY,
        "T-SEC": ATHENA_SECRET,
        "T-T": str(timestamp_ms),
        "T-SIGN": build_sign(timestamp_ms),
    }


def extract_hits(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("result", {}).get("data", {}).get("middle", {}).get("list", []) or []


def strip_tags(value: Any) -> str:
    return re.sub(r"<[^>]+>", "", str(value or "")).strip()


def get_hit_title(item: dict[str, Any]) -> str:
    for key in ("title_no_tag", "title", "name"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return strip_tags(value)
    return ""


def get_hit_url(item: dict[str, Any]) -> str:
    for key in ("url", "linkUrl", "sourceUrl", "href"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def score_title(query: str, title: str) -> float:
    query_n = query.lower().strip()
    title_n = title.lower().strip()
    if not query_n or not title_n:
        return 0.0
    if query_n in title_n:
        return 1.0
    return SequenceMatcher(None, query_n, title_n).ratio()


def pick_best_hit(search_word: str, items: list[dict[str, Any]]) -> SearchHit | None:
    best: SearchHit | None = None
    for item in items:
        title = get_hit_title(item)
        url = get_hit_url(item)
        if not title or not url:
            continue
        candidate = SearchHit(
            title=title,
            url=url,
            score=score_title(search_word, title),
            summary=item.get("summary"),
            time=item.get("time"),
            raw=item,
        )
        if best is None or candidate.score > best.score:
            best = candidate
    return best


def gov_search(search_word: str, page_no: int = 1, page_size: int = 10) -> dict[str, Any]:
    """Search gov.cn and return the raw response plus normalized hits."""
    timestamp_ms = int(time.time() * 1000)
    response = requests.post(
        f"{BASE_URL}{SEARCH_PATH}",
        headers=build_search_headers(search_word, timestamp_ms),
        data=json.dumps(build_search_payload(search_word, page_no, page_size), ensure_ascii=False).encode("utf-8"),
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    items = extract_hits(payload)
    hits: list[dict[str, Any]] = []
    for item in items:
        title = get_hit_title(item)
        url = get_hit_url(item)
        if not title or not url:
            continue
        hits.append(
            asdict(
                SearchHit(
                    title=title,
                    url=url,
                    score=score_title(search_word, title),
                    summary=item.get("summary"),
                    time=item.get("time"),
                    raw=item,
                )
            )
        )
    best_hit = pick_best_hit(search_word, items)
    return {
        "search_word": search_word,
        "page_no": page_no,
        "page_size": page_size,
        "hits": hits,
        "best_hit": asdict(best_hit) if best_hit else None,
        "raw": payload,
    }


def _normalize_text(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


class _TargetDivTextParser(HTMLParser):
    def __init__(self, match_div: Callable[[dict[str, str]], bool]) -> None:
        super().__init__(convert_charrefs=True)
        self.match_div = match_div
        self.stack: list[str] = []
        self.capture_depth: int | None = None
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        depth_before = len(self.stack)
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        if self.capture_depth is None and self.match_div(attr_map):
            self.capture_depth = depth_before + 1
        elif self.capture_depth is not None and self.skip_depth == 0 and tag in {
            "p",
            "div",
            "li",
            "tr",
            "section",
            "article",
            "header",
            "footer",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        }:
            self.parts.append("\n")
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self.stack:
            self.stack.pop()
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.capture_depth is not None and self.skip_depth == 0 and tag in {"p", "div", "li", "tr"}:
            self.parts.append("\n")
        if tag == "div" and self.capture_depth is not None and len(self.stack) < self.capture_depth:
            self.capture_depth = None

    def handle_data(self, data: str) -> None:
        if self.capture_depth is None or self.skip_depth:
            return
        text = re.sub(r"\s+", " ", data).strip()
        if text:
            self.parts.append(text)
            self.parts.append(" ")

    def get_text(self) -> str:
        return _normalize_text("".join(self.parts))


def _extract_div_text(html: str, match_div: Callable[[dict[str, str]], bool]) -> str:
    parser = _TargetDivTextParser(match_div)
    parser.feed(html)
    parser.close()
    return parser.get_text()


def fetch_notice_body(url: str) -> str:
    """Fetch and extract the main body text from a gov.cn notice page."""
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        timeout=20,
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding or "utf-8"
    html = response.text
    text = _extract_div_text(
        html,
        lambda attrs: "trs_editor_view" in (attrs.get("class") or "").split(),
    )
    if not text:
        text = _extract_div_text(html, lambda attrs: attrs.get("id") == "UCAP-CONTENT")
    if not text:
        raise SystemExit(f"Could not extract notice body from {url}")
    return text


def cache_path(year: int) -> Path:
    return CACHE_DIR / f"{year}.json"


def load_year_cache(year: int) -> dict[str, Any] | None:
    path = cache_path(year)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_year_cache(year: int, payload: dict[str, Any]) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = cache_path(year)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return path


def _iter_notice_sections(notice_body: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        r"(?:^|\n)(?:[一二三四五六七八九十]+、)?(?P<holiday>[^\n：:]+)[：:](?P<detail>.*?)(?=(?:\n[一二三四五六七八九十]+、|$))",
        re.S,
    )
    sections: list[tuple[str, str]] = []
    for match in pattern.finditer(notice_body):
        holiday = match.group("holiday").strip()
        detail = match.group("detail").strip()
        if holiday and detail:
            sections.append((holiday, detail))
    return sections


def _parse_date_piece(year: int, month: int, day: int) -> str:
    return f"{year:04d}-{month:02d}-{day:02d}"


def _iter_dates_inclusive(start_dt: datetime, end_dt: datetime) -> list[str]:
    from datetime import timedelta

    days: list[str] = []
    current = start_dt
    while current <= end_dt:
        days.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return days


def parse_notice_payload(year: int, notice_title: str, notice_url: str, notice_body: str) -> dict[str, Any]:
    special_days: list[dict[str, Any]] = []
    for holiday_name, detail in _iter_notice_sections(notice_body):
        for range_match in re.finditer(
            r"(?P<sm>\d{1,2})月(?P<sd>\d{1,2})日(?:（[^）]*）)?(?:至(?:(?P<em>\d{1,2})月)?(?P<ed>\d{1,2})日(?:（[^）]*）)?)?放假(?:调休)?",
            detail,
        ):
            start_month = int(range_match.group("sm"))
            start_day = int(range_match.group("sd"))
            end_month = int(range_match.group("em")) if range_match.group("em") else None
            end_day = int(range_match.group("ed") or range_match.group("sd"))
            start_dt = datetime(year, start_month, start_day)
            end_dt = datetime(year, end_month or start_month, end_day)
            for date_str in _iter_dates_inclusive(start_dt, end_dt):
                special_days.append(
                    {
                        "date": date_str,
                        "workday": False,
                        "holiday": holiday_name,
                        "kind": "holiday",
                    }
                )

        for makeup_match in re.finditer(r"(?P<m>\d{1,2})月(?P<d>\d{1,2})日(?:（[^）]*）)?上班", detail):
            date_str = _parse_date_piece(year, int(makeup_match.group("m")), int(makeup_match.group("d")))
            special_days.append(
                {
                    "date": date_str,
                    "workday": True,
                    "holiday": holiday_name,
                    "kind": "makeup_workday",
                }
            )

    deduped: dict[str, dict[str, Any]] = {}
    for item in special_days:
        deduped[item["date"]] = item
    return {
        "year": year,
        "notice_title": notice_title,
        "notice_url": notice_url,
        "special_days": sorted(deduped.values(), key=lambda item: item["date"]),
    }


def validate_year_payload(year: int, payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SystemExit("Parsed cache payload must be a JSON object")
    required = ("year", "notice_title", "notice_url", "special_days")
    missing = [key for key in required if key not in payload]
    if missing:
        raise SystemExit(f"Cache payload missing fields: {', '.join(missing)}")
    if int(payload["year"]) != year:
        raise SystemExit(f"Cache payload year mismatch: expected {year}, got {payload['year']}")
    if not isinstance(payload["special_days"], list):
        raise SystemExit("Cache payload special_days must be a list")
    for item in payload["special_days"]:
        if not isinstance(item, dict):
            raise SystemExit("Each special_days entry must be an object")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(item.get("date", ""))):
            raise SystemExit("Each special_days entry must include date=YYYY-MM-DD")
        if not isinstance(item.get("workday"), bool):
            raise SystemExit("Each special_days entry must include a boolean workday")
        if not isinstance(item.get("holiday"), str):
            raise SystemExit("Each special_days entry must include a holiday string")
        if item.get("kind") not in {"holiday", "makeup_workday"}:
            raise SystemExit("Each special_days entry must use kind=holiday or kind=makeup_workday")
    return payload


def select_notice_hit(search_result: dict[str, Any], year: int) -> dict[str, Any]:
    desired_query = f"{year}节假日安排"
    hits = search_result.get("hits") or []
    titled_hits: list[dict[str, Any]] = []
    for hit in hits:
        if not isinstance(hit, dict):
            continue
        title = str(hit.get("title") or "")
        if title and str(year) in title:
            titled_hits.append(hit)
    candidates = titled_hits or [hit for hit in hits if isinstance(hit, dict)]
    if not candidates:
        best_hit = search_result.get("best_hit")
        if isinstance(best_hit, dict):
            return best_hit
        raise SystemExit("No usable gov.cn notice search result found")
    best = max(candidates, key=lambda hit: score_title(desired_query, str(hit.get("title") or "")))
    return best


def refresh_year(year: int, search_word: str = "节假日安排") -> dict[str, Any]:
    cached = load_year_cache(year)
    if cached is not None:
        return cached

    search_result = gov_search(search_word)
    best_hit = select_notice_hit(search_result, year)
    if not best_hit or not best_hit.get("url"):
        raise SystemExit(f"No gov.cn search result found for {search_word}")

    notice_url = str(best_hit["url"])
    notice_title = str(best_hit["title"])
    notice_body = fetch_notice_body(notice_url)
    parsed = parse_notice_payload(year, notice_title, notice_url, notice_body)
    validated = validate_year_payload(year, parsed)
    save_year_cache(year, validated)
    return validated


def load_or_refresh_year_cache(year: int) -> dict[str, Any]:
    cached = load_year_cache(year)
    if cached is not None:
        return cached
    return refresh_year(year)


def parse_year(value: str) -> int:
    if not re.fullmatch(r"\d{4}", value):
        raise SystemExit("Year input must use YYYY")
    return int(value)


def parse_month(value: str) -> tuple[int, int]:
    try:
        dt = datetime.strptime(value, "%Y-%m")
    except ValueError as exc:
        raise SystemExit("Month input must use YYYY-MM") from exc
    return dt.year, dt.month


def parse_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit("Date input must use YYYY-MM-DD") from exc


def weekday_label(dt: datetime) -> str:
    return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]


def fallback_workday_from_weekday(dt: datetime) -> bool:
    return dt.weekday() < 5


def special_day_index(cache: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for item in cache.get("special_days", []) or []:
        if isinstance(item, dict):
            date_str = item.get("date")
            if isinstance(date_str, str) and date_str:
                index[date_str] = item
    return index


def evaluate_date(date_str: str, cache: dict[str, Any] | None) -> dict[str, Any]:
    dt = parse_date(date_str)
    special = special_day_index(cache or {})
    item = special.get(date_str)
    if item:
        workday = bool(item.get("workday"))
        holiday = item.get("holiday")
        kind = item.get("kind") or ("makeup_workday" if workday else "holiday")
    else:
        workday = fallback_workday_from_weekday(dt)
        holiday = None
        kind = "workday" if workday else "weekend"
    return {
        "date": date_str,
        "weekday": weekday_label(dt),
        "workday": workday,
        "kind": kind,
        "holiday": holiday,
    }


def month_rows(year: int, month: int, cache: dict[str, Any] | None) -> list[dict[str, Any]]:
    last_day = calendar.monthrange(year, month)[1]
    rows = []
    for day in range(1, last_day + 1):
        rows.append(evaluate_date(f"{year:04d}-{month:02d}-{day:02d}", cache))
    return rows


def print_date(date_str: str, cache: dict[str, Any] | None) -> None:
    print(json.dumps(evaluate_date(date_str, cache), ensure_ascii=False, indent=2))


def print_month(year: int, month: int, cache: dict[str, Any] | None) -> None:
    rows = month_rows(year, month, cache)
    print("| date | weekday | workday | kind | holiday |")
    print("| --- | --- | --- | --- | --- |")
    for row in rows:
        print(
            f"| {row['date']} | {row['weekday']} | {'yes' if row['workday'] else 'no'} | "
            f"{row['kind']} | {row['holiday'] or ''} |"
        )


def print_search(search_word: str, page_no: int = 1, page_size: int = 10) -> None:
    print(json.dumps(gov_search(search_word, page_no=page_no, page_size=page_size), ensure_ascii=False, indent=2))


def print_body(url: str) -> None:
    print(fetch_notice_body(url))


def main() -> None:
    argv = sys.argv[1:]
    if len(argv) == 1 and re.fullmatch(r"\d{4}-\d{2}", argv[0]):
        year, month = parse_month(argv[0])
        print_month(year, month, load_or_refresh_year_cache(year))
        return
    if len(argv) == 1 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", argv[0]):
        dt = parse_date(argv[0])
        print_date(argv[0], load_or_refresh_year_cache(dt.year))
        return

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    search_parser = sub.add_parser("search", help="Search gov.cn notices")
    search_parser.add_argument("search_word")
    search_parser.add_argument("--page-no", type=int, default=1)
    search_parser.add_argument("--page-size", type=int, default=10)

    body_parser = sub.add_parser("body", help="Fetch a notice body")
    body_parser.add_argument("url")

    month_parser = sub.add_parser("month", help="Print a month view from cache")
    month_parser.add_argument("value", help="YYYY-MM")

    date_parser = sub.add_parser("date", help="Print a single date from cache")
    date_parser.add_argument("value", help="YYYY-MM-DD")

    cache_parser = sub.add_parser("cache", help="Inspect a year cache")
    cache_parser.add_argument("year", help="YYYY")

    refresh_parser = sub.add_parser("refresh", help="Refresh and save a year cache from gov.cn")
    refresh_parser.add_argument("year", help="YYYY")

    args = parser.parse_args(argv)

    if args.command == "search":
        print_search(args.search_word, page_no=args.page_no, page_size=args.page_size)
        return
    if args.command == "body":
        print_body(args.url)
        return
    if args.command == "month":
        year, month = parse_month(args.value)
        print_month(year, month, load_or_refresh_year_cache(year))
        return
    if args.command == "date":
        dt = parse_date(args.value)
        print_date(args.value, load_or_refresh_year_cache(dt.year))
        return
    if args.command == "cache":
        year = parse_year(args.year)
        cache = load_year_cache(year)
        if cache is None:
            raise SystemExit(f"Missing cache file: {cache_path(year)}")
        print(json.dumps(cache, ensure_ascii=False, indent=2))
        return
    if args.command == "refresh":
        year = parse_year(args.year)
        print(json.dumps(refresh_year(year), ensure_ascii=False, indent=2))
        return

    raise SystemExit("Unsupported command")


if __name__ == "__main__":
    main()
