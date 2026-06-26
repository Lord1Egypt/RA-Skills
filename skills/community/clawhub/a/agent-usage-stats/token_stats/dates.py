"""Date and time-range parsing helpers."""

from __future__ import annotations

from datetime import datetime, timedelta


def parse_date(s: str) -> tuple:
    """Parse 'YYYY-MM-DD' → (start_ts, end_ts)"""
    dt = datetime.strptime(s.strip(), "%Y-%m-%d")
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end = dt.replace(hour=23, minute=59, second=59, microsecond=0)
    return start.timestamp(), end.timestamp()


def parse_time_label(label: str) -> tuple:
    """Parse a time label → (start_ts, end_ts).

    Supports:
      today, yesterday, this-week / week, last-week, last-7d
      YYYY-MM-DD (single day)
      YYYY-MM-DD~YYYY-MM-DD (date range)
    """
    s = label.strip().lower()
    now = datetime.now()

    if s == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "yesterday":
        d = now - timedelta(days=1)
        start = d.replace(hour=0, minute=0, second=0, microsecond=0)
        end = d.replace(hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    if s in ("this-week", "week"):
        monday = now - timedelta(days=now.weekday())
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-week":
        monday = now - timedelta(days=now.weekday() + 7)
        sunday = monday + timedelta(days=6)
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        end = sunday.replace(hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    if s == "last-7d":
        start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s in ("this-month", "month"):
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-month":
        first_of_this = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_last = first_of_this - timedelta(seconds=1)
        start_of_last = end_of_last.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start_of_last.timestamp(), end_of_last.timestamp()

    if s in ("this-year", "year"):
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-year":
        start = now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(year=now.year - 1, month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    # Date range: YYYY-MM-DD~YYYY-MM-DD
    if "~" in s:
        parts = s.split("~", 1)
        start_ts, _ = parse_date(parts[0])
        _, end_ts = parse_date(parts[1])
        return start_ts, end_ts

    # Single date
    return parse_date(s)


def split_months(from_ts, to_ts):
    """Split a time range into calendar month buckets.
    Returns [(label, start_ts, end_ts), ...]"""
    from_dt = datetime.fromtimestamp(from_ts)
    to_dt = datetime.fromtimestamp(to_ts)
    months = []
    current = from_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    while current <= to_dt:
        month_start = current
        if current.month == 12:
            next_month = current.replace(year=current.year + 1, month=1)
        else:
            next_month = current.replace(month=current.month + 1)
        month_end = min(next_month - timedelta(seconds=1), to_dt)
        label = month_start.strftime('%Y-%m')
        months.append((label, month_start.timestamp(), month_end.timestamp()))
        current = next_month
    return months


def label_to_display(label: str) -> str:
    """将时间标签转为人类可读的日期字符串，用于对比模式列头。"""
    s = label.strip().lower()
    now = datetime.now()
    if s == "today":
        return now.strftime("%Y-%m-%d")
    if s == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    if s in ("this-week", "week"):
        monday = now - timedelta(days=now.weekday())
        return f"{monday.strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s == "last-week":
        monday = now - timedelta(days=now.weekday() + 7)
        sunday = monday + timedelta(days=6)
        return f"{monday.strftime('%Y-%m-%d')}~{sunday.strftime('%Y-%m-%d')}"
    if s == "last-7d":
        start = now - timedelta(days=7)
        return f"{start.strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s in ("this-month", "month"):
        start = now.replace(day=1)
        return f"{start.strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s == "last-month":
        first_of_this = now.replace(day=1)
        end_of_last = first_of_this - timedelta(days=1)
        return f"{end_of_last.replace(day=1).strftime('%Y-%m-%d')}~{end_of_last.strftime('%Y-%m-%d')}"
    if s in ("this-year", "year"):
        return f"{now.replace(month=1, day=1).strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s == "last-year":
        return f"{now.year - 1}-01-01~{now.year - 1}-12-31"
    return label
