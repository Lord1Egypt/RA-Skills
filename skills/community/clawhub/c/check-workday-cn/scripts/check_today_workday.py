#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import date, datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

API_TEMPLATE = "https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
DEFAULT_TZ = ZoneInfo("Asia/Shanghai")


@dataclass(frozen=True)
class WorkdayResult:
    query_date: date
    is_workday: bool
    reason: str
    source_url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether today (or a given date) is a workday in China."
    )
    parser.add_argument(
        "--date",
        dest="query_date",
        help="Date in YYYY-MM-DD. Defaults to today in Asia/Shanghai.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="HTTP timeout in seconds. Default: 15.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Retry attempts for transient network failures. Default: 3.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output.",
    )
    return parser.parse_args()


def parse_query_date(query_date: str | None) -> date:
    if query_date is None:
        return datetime.now(DEFAULT_TZ).date()
    try:
        return date.fromisoformat(query_date)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date value: {query_date}. Use YYYY-MM-DD.") from exc


def load_holiday_data(year: int, timeout: float, retries: int) -> tuple[dict, str]:
    source_url = API_TEMPLATE.format(year=year)
    request = Request(source_url, headers={"User-Agent": "check-workday-cn/1.0"})
    attempts = max(1, retries)
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload, source_url
        except HTTPError as exc:
            # 4xx errors are not transient in this context.
            raise SystemExit(f"Failed to fetch holiday data ({exc.code}) from {source_url}") from exc
        except URLError as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(0.5 * attempt)

    if isinstance(last_error, URLError):
        raise SystemExit(f"Failed to fetch holiday data from {source_url}: {last_error.reason}") from last_error
    raise SystemExit(f"Failed to fetch holiday data from {source_url}")


def decide_workday(query_date: date, payload: dict, source_url: str) -> WorkdayResult:
    days = payload.get("days", [])
    entry_map = {
        item.get("date"): item
        for item in days
        if isinstance(item, dict) and isinstance(item.get("date"), str)
    }
    date_key = query_date.isoformat()
    entry = entry_map.get(date_key)

    if entry is not None:
        is_off_day = bool(entry.get("isOffDay"))
        holiday_name = entry.get("name") or "holiday schedule"
        if is_off_day:
            reason = f"holiday override: {holiday_name} marked as off day"
            is_workday = False
        else:
            reason = f"holiday override: {holiday_name} marked as working day"
            is_workday = True
        return WorkdayResult(
            query_date=query_date,
            is_workday=is_workday,
            reason=reason,
            source_url=source_url,
        )

    if query_date.weekday() < 5:
        return WorkdayResult(
            query_date=query_date,
            is_workday=True,
            reason="weekday fallback: Monday-Friday and no holiday override",
            source_url=source_url,
        )

    return WorkdayResult(
        query_date=query_date,
        is_workday=False,
        reason="weekday fallback: Saturday-Sunday and no holiday override",
        source_url=source_url,
    )


def print_result(result: WorkdayResult, as_json: bool) -> None:
    if as_json:
        print(
            json.dumps(
                {
                    "date": result.query_date.isoformat(),
                    "is_workday": result.is_workday,
                    "reason": result.reason,
                    "source_url": result.source_url,
                },
                ensure_ascii=False,
            )
        )
        return

    status = "WORKDAY" if result.is_workday else "OFFDAY"
    print(f"date: {result.query_date.isoformat()}")
    print(f"is_workday: {result.is_workday}")
    print(f"status: {status}")
    print(f"reason: {result.reason}")
    print(f"source_url: {result.source_url}")


def main() -> None:
    args = parse_args()
    query_date = parse_query_date(args.query_date)
    payload, source_url = load_holiday_data(
        query_date.year,
        timeout=args.timeout,
        retries=args.retries,
    )
    result = decide_workday(query_date, payload, source_url)
    print_result(result, as_json=args.json)


if __name__ == "__main__":
    main()
