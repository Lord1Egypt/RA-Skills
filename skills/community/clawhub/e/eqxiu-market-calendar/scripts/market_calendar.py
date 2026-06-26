#!/usr/bin/env python3
"""易企秀营销日历 CLI：获取准确日期、查询节日、生成模板商城搜索链接。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DATE_API = "https://msearch-api.eqxiu.com/yyyymm"
HOLIDAY_API = "https://msearch-api.eqxiu.com/m/holiday/queryByMonth"
MALL_SEARCH_BASE = "https://www.eqxiu.com/mall/search?keywords="
TIMEOUT = 10
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class MarketCalendarError(Exception):
    pass


def http_get(url: str) -> str:
    req = Request(url, headers={"User-Agent": "eqxiu-market-calendar/1.0"})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            if resp.status != 200:
                raise MarketCalendarError(f"HTTP {resp.status} from {url}")
            return body
    except HTTPError as e:
        raise MarketCalendarError(f"HTTP {e.code} from {url}") from e
    except URLError as e:
        raise MarketCalendarError(
            f"Network error reaching msearch-api.eqxiu.com: {e.reason}"
        ) from e


def fetch_today() -> str:
    text = http_get(DATE_API).strip()
    if not DATE_RE.match(text):
        raise MarketCalendarError(f"Unexpected date format from API: {text!r}")
    return text


def fetch_month(year: int, month: int) -> list[dict[str, Any]]:
    url = f"{HOLIDAY_API}?year={year}&month={month:02d}"
    raw = http_get(url)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise MarketCalendarError(f"Invalid JSON from holiday API: {e}") from e
    if not data.get("success"):
        raise MarketCalendarError(
            f"Holiday API failed: code={data.get('code')} msg={data.get('msg')}"
        )
    return data.get("list") or []


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def search_term(holiday: dict[str, Any]) -> str:
    word = (holiday.get("searchWord") or "").strip()
    if word:
        return word
    keywords = (holiday.get("keywords") or "").strip()
    if keywords:
        return keywords.split("|")[0].strip()
    return (holiday.get("name") or "").strip()


def mall_url(term: str) -> str:
    return f"{MALL_SEARCH_BASE}{quote(term, safe='')}"


def months_from_today(today: str) -> list[tuple[int, int]]:
    d = parse_date(today)
    current = (d.year, d.month)
    if d.month == 12:
        nxt = (d.year + 1, 1)
    else:
        nxt = (d.year, d.month + 1)
    return [current, nxt]


def months_covering_range(start: date, end: date) -> list[tuple[int, int]]:
    """Return each (year, month) that overlaps [start, end]."""
    months: list[tuple[int, int]] = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        if m == 12:
            y, m = y + 1, 1
        else:
            m += 1
    return months


def months_for_upcoming(
    today: str,
    days: int | None,
    *,
    all_future: bool = False,
    horizon_months: int = 12,
) -> list[tuple[int, int]]:
    """Months to query so upcoming --days / --all-future has complete API coverage."""
    start = parse_date(today)
    if all_future:
        end = start
        for _ in range(horizon_months):
            if end.month == 12:
                end = date(end.year + 1, 1, 1)
            else:
                end = date(end.year, end.month + 1, 1)
        end = end - timedelta(days=1)
    else:
        end = start + timedelta(days=days or 0)
    return months_covering_range(start, end)


def enrich_holiday(holiday: dict[str, Any]) -> dict[str, Any]:
    term = search_term(holiday)
    return {
        "id": holiday.get("id"),
        "name": holiday.get("name"),
        "startDate": holiday.get("startDate"),
        "endDate": holiday.get("endDate"),
        "promotStartDate": holiday.get("promotStartDate"),
        "level": holiday.get("level"),
        "searchWord": holiday.get("searchWord"),
        "keywords": holiday.get("keywords"),
        "search_term": term,
        "mall_url": mall_url(term) if term else "",
    }


def merge_holidays(month_pairs: list[tuple[int, int]]) -> list[dict[str, Any]]:
    seen: dict[int, dict[str, Any]] = {}
    for year, month in month_pairs:
        for item in fetch_month(year, month):
            hid = item.get("id")
            if hid is not None:
                seen[hid] = item
            else:
                seen[id(item)] = item
    merged = sorted(seen.values(), key=lambda h: h.get("startDate") or "")
    return [enrich_holiday(h) for h in merged]


def validate_month_not_past(year: int, month: int, today: str) -> None:
    t = parse_date(today)
    if (year, month) < (t.year, t.month):
        raise MarketCalendarError(
            f"不能查询过去的月份: {year}-{month:02d}（今天为 {today}）"
        )


def filter_future_holidays(
    holidays: list[dict[str, Any]], today: str
) -> list[dict[str, Any]]:
    """Only holidays with startDate on or after today (exclude past events)."""
    t = parse_date(today)
    return [h for h in holidays if parse_date(h["startDate"]) >= t]


def filter_upcoming(
    holidays: list[dict[str, Any]],
    today: str,
    days: int | None,
) -> list[dict[str, Any]]:
    """Future holidays (startDate >= today) with startDate <= today+days when days set."""
    t = parse_date(today)
    window_end = t + timedelta(days=days) if days is not None else None
    result = []
    for h in holidays:
        start = parse_date(h["startDate"])
        if start < t:
            continue
        if window_end is not None and start > window_end:
            continue
        result.append(h)
    return result


def print_table(holidays: list[dict[str, Any]]) -> None:
    cols = ("name", "startDate", "endDate", "level", "search_term", "mall_url")
    print("\t".join(cols))
    for h in holidays:
        print("\t".join(str(h.get(c, "")) for c in cols))


def print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_today(args: argparse.Namespace) -> int:
    today = fetch_today()
    if args.json:
        print_json({"today": today})
    else:
        print(today)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    today = fetch_today()
    if args.year is not None and args.month is not None:
        validate_month_not_past(args.year, args.month, today)
        months = [(args.year, args.month)]
    elif args.year is not None or args.month is not None:
        print("error: --year and --month must be used together", file=sys.stderr)
        return 1
    else:
        months = months_from_today(today)

    holidays = filter_future_holidays(merge_holidays(months), today)
    if args.json:
        print_json({"today": today, "months": months, "holidays": holidays})
    else:
        print_table(holidays)
    return 0


def cmd_upcoming(args: argparse.Namespace) -> int:
    today = fetch_today()
    days = None if args.all_future else args.days
    months = months_for_upcoming(today, days, all_future=args.all_future)
    holidays = merge_holidays(months)
    filtered = filter_upcoming(holidays, today, days)
    window_end = None
    if days is not None:
        window_end = (parse_date(today) + timedelta(days=days)).isoformat()
    if args.json:
        print_json(
            {
                "today": today,
                "days": days,
                "window_end": window_end,
                "all_future": args.all_future,
                "months": months,
                "holidays": filtered,
            }
        )
    else:
        print_table(filtered)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="易企秀营销日历：查询节日并生成模板商城搜索链接",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_today = sub.add_parser("today", help="获取 API 当前日期")
    p_today.add_argument("--json", action="store_true", help="JSON 输出")
    p_today.set_defaults(func=cmd_today)

    p_list = sub.add_parser("list", help="列出未来节日及商城链接（startDate>=today）")
    p_list.add_argument("--year", type=int, help="指定年份（须与 --month 同用）")
    p_list.add_argument("--month", type=int, help="指定月份 1-12")
    p_list.add_argument("--json", action="store_true", help="JSON 输出")
    p_list.set_defaults(func=cmd_list)

    p_up = sub.add_parser("upcoming", help="列出未来 N 天内开始的节日（startDate>=today）")
    p_up.add_argument(
        "--days",
        type=int,
        default=60,
        help="startDate 在 [today, today+N] 内，并拉取覆盖月份（默认 60）",
    )
    p_up.add_argument(
        "--all-future",
        action="store_true",
        help="startDate>=today 且无上限；拉取从今天起 12 个月 API 数据",
    )
    p_up.add_argument("--json", action="store_true", help="JSON 输出")
    p_up.set_defaults(func=cmd_upcoming)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except MarketCalendarError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
