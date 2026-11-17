#!/usr/bin/env python3
"""dtconv - convert between timestamps, datetime strings, timezones and formats.

Standard library only. Python 3.9+ gets everything; on 3.7/3.8 the only thing that
stops working is IANA zone names (Asia/Shanghai), because zoneinfo does not exist
there — timestamps, formats, natural language, arithmetic and UTC/local/+08:00
offsets all keep working. Run with --help for usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # Python < 3.9, or a build without zoneinfo
    try:
        from backports.zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    except ImportError:
        ZoneInfo = None

        class ZoneInfoNotFoundError(Exception):
            pass


# ------------------------------------------------------------------ timezones

OFFSET_RE = re.compile(r"^(?:utc|gmt)?([+-])(\d{1,2})(?::?(\d{2}))?$", re.I)

NO_ZONEINFO_HINT = ("this Python has no zoneinfo module (needs 3.9+, or "
                    "'pip install backports.zoneinfo tzdata'). Everything else still "
                    "works — use UTC, local, or a fixed offset such as +08:00")

NO_TZDATA_HINT = ("the IANA timezone database is not installed — 'pip install tzdata', "
                  "or use a fixed offset such as +08:00")


def local_tz():
    return datetime.now().astimezone().tzinfo


def get_tz(name):
    """Accept 'local', 'UTC', '+08:00', 'UTC+8' or any IANA name like 'Asia/Tokyo'."""
    if name is None or name.strip().lower() == "local":
        return local_tz()
    text = name.strip()
    if text.lower() in ("utc", "z", "zulu", "gmt"):
        return timezone.utc
    m = OFFSET_RE.match(text)
    if m:
        sign = 1 if m.group(1) == "+" else -1
        off = timedelta(hours=int(m.group(2)), minutes=int(m.group(3) or 0))
        return timezone(sign * off)
    if ZoneInfo is None:
        raise ValueError(f"cannot resolve timezone {text!r}: {NO_ZONEINFO_HINT}")
    try:
        return ZoneInfo(text)
    except ZoneInfoNotFoundError:
        raise ValueError(f"unknown timezone {text!r} — check the spelling, or "
                         f"{NO_TZDATA_HINT}")



def tz_label(dt):
    name = dt.tzname() or ""
    return f"{dt.strftime('%z')}{' ' + name if name and not name.startswith(('+', '-', 'UTC')) else ''}".strip()


# ------------------------------------------------------------- epoch numbers

UNIT_DIVISOR = {"s": 1, "ms": 1_000, "us": 1_000_000, "ns": 1_000_000_000}


def guess_epoch_unit(value):
    """Digit magnitude is a reliable discriminator for any date in 1973..5138."""
    a = abs(value)
    if a < 1e11:
        return "s"
    if a < 1e14:
        return "ms"
    if a < 1e17:
        return "us"
    return "ns"


def parse_epoch(text, unit=None):
    t = text.strip().replace("_", "").replace(",", "")
    if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", t):
        return None
    value = float(t)
    unit = unit or guess_epoch_unit(value)
    dt = datetime.fromtimestamp(value / UNIT_DIVISOR[unit], timezone.utc)
    return dt, f"unix timestamp ({unit})"


COMPACT_FORMATS = [("%Y%m%d%H%M%S", 14), ("%Y%m%d%H%M", 12), ("%Y%m%d", 8)]


def parse_compact(text):
    """20260826 / 202608261530 read as calendar dates, not epochs.

    A bare 8-digit number is far more often a compact date than a 1970s epoch,
    so this is tried first; --unit forces the epoch reading when that is wrong.
    """
    t = text.strip()
    for fmt, length in COMPACT_FORMATS:
        if len(t) == length and t.isdigit() and "1900" <= t[:4] <= "2199":
            try:
                return datetime.strptime(t, fmt), f"compact datetime ({fmt})"
            except ValueError:
                pass
    return None


# ---------------------------------------------------------- absolute strings

ABS_FORMATS = [
    "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M", "%Y/%m/%d",
    "%Y.%m.%d %H:%M:%S", "%Y.%m.%d",
    "%Y年%m月%d日%H时%M分%S秒", "%Y年%m月%d日 %H:%M:%S", "%Y年%m月%d日",
    "%b %d %Y %H:%M:%S", "%b %d, %Y", "%B %d, %Y", "%d %b %Y %H:%M:%S", "%d %b %Y",
    "%H:%M:%S", "%H:%M",
]


def _attach_time(dt, tail):
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            tod = datetime.strptime(tail.strip(), fmt).time()
            return dt.replace(hour=tod.hour, minute=tod.minute, second=tod.second)
        except ValueError:
            continue
    return dt


def parse_slash(text):
    """1/2/2026 is genuinely ambiguous; assume M/D/Y but say so when D/M/Y also fits."""
    if not re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}(\s+.*)?", text):
        return None
    head, _, tail = text.partition(" ")
    first, second, _ = head.split("/")
    parsed = {}
    for label, fmt in (("M/D/Y", "%m/%d/%Y"), ("D/M/Y", "%d/%m/%Y")):
        try:
            parsed[label] = datetime.strptime(head, fmt)
        except ValueError:
            pass
    if not parsed:
        return None
    label = "M/D/Y" if "M/D/Y" in parsed else "D/M/Y"
    dt = parsed[label]
    warning = None
    if len(parsed) == 2 and first != second:
        other = parsed["D/M/Y" if label == "M/D/Y" else "M/D/Y"]
        warning = (f"{head} is ambiguous - read as {label} ({dt.date()}); "
                   f"the other reading is {other.date()}.")
    return _attach_time(dt, tail) if tail else dt, f"slash date ({label})", warning


ISO_FRACTION_RE = re.compile(r"(\.\d{6})\d+")
ISO_OFFSET_RE = re.compile(r"([+-]\d{2})(\d{2})$")
ISO_BASIC_RE = re.compile(r"(\d{4})(\d{2})(\d{2})[T ](\d{2})(\d{2})(\d{2})(\.\d+)?(.*)")

ISO_FALLBACK_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M%z",
    "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M",
]


def normalize_iso(text):
    """Reshape ISO variants into what fromisoformat accepts.

    Python 3.9/3.10 only parse exactly what isoformat() emits, so the shapes that show
    up in real logs — Go/Java nanosecond stamps, offsets written '+0800', ISO basic
    format — are rejected there while working on 3.11+. Normalizing first makes the
    behaviour identical across versions. Sub-microsecond digits are dropped because
    datetime cannot hold them.
    """
    t = re.sub(r"[zZ]$", "+00:00", text.strip())
    t = ISO_FRACTION_RE.sub(r"\1", t)
    t = ISO_OFFSET_RE.sub(r"\1:\2", t)
    m = ISO_BASIC_RE.fullmatch(t)
    if m:
        year, month, day, hour, minute, second, frac, rest = m.groups()
        t = f"{year}-{month}-{day}T{hour}:{minute}:{second}{frac or ''}{rest}"
    return t


def parse_iso(text):
    """ISO 8601 / RFC 3339 in any of its shapes, or None."""
    t = normalize_iso(text)
    from_iso = getattr(datetime, "fromisoformat", None)  # 3.7+
    if from_iso:
        try:
            return from_iso(t)
        except ValueError:
            pass
    for fmt in ISO_FALLBACK_FORMATS:
        try:
            return datetime.strptime(t, fmt)
        except ValueError:
            continue
    return None


def parse_absolute(text):
    """Return (datetime, label, warning) - datetime may be naive. None if no match."""
    t = text.strip()
    iso = parse_iso(t)
    if iso:
        return iso, "ISO 8601", None
    if re.search(r"[A-Za-z]{3},?\s", t):
        try:
            return parsedate_to_datetime(t), "RFC 2822", None
        except (TypeError, ValueError, IndexError):
            pass
    slash = parse_slash(t)
    if slash:
        return slash
    for fmt in ABS_FORMATS:
        try:
            dt = datetime.strptime(t, fmt)
        except ValueError:
            continue
        if fmt.startswith("%H"):  # time-only input means "today at that time"
            now = datetime.now()
            dt = dt.replace(year=now.year, month=now.month, day=now.day)
        return dt, f"pattern {fmt}", None
    return None


# ------------------------------------------------------- relative expressions

UNIT_ALIASES = {
    "y": "years", "yr": "years", "yrs": "years", "year": "years", "years": "years", "年": "years",
    "mo": "months", "mon": "months", "month": "months", "months": "months",
    "月": "months", "个月": "months",
    "w": "weeks", "wk": "weeks", "wks": "weeks", "week": "weeks", "weeks": "weeks", "周": "weeks",
    "d": "days", "day": "days", "days": "days", "天": "days", "日": "days",
    "h": "hours", "hr": "hours", "hrs": "hours", "hour": "hours", "hours": "hours",
    "小时": "hours", "个小时": "hours", "时": "hours",
    "m": "minutes", "min": "minutes", "mins": "minutes", "minute": "minutes",
    "minutes": "minutes", "分": "minutes", "分钟": "minutes",
    "s": "seconds", "sec": "seconds", "secs": "seconds", "second": "seconds",
    "seconds": "seconds", "秒": "seconds",
}

TOKEN_RE = re.compile(r"([+-]?\d+(?:\.\d+)?)\s*([a-zA-Z\u4e00-\u9fff]+)")

WEEKDAYS = {"monday": 0, "mon": 0, "tuesday": 1, "tue": 1, "tues": 1, "wednesday": 2,
            "wed": 2, "thursday": 3, "thu": 3, "thur": 3, "thurs": 3, "friday": 4,
            "fri": 4, "saturday": 5, "sat": 5, "sunday": 6, "sun": 6}

DAY_WORDS = {"today": 0, "tomorrow": 1, "yesterday": -1, "今天": 0, "今日": 0,
             "明天": 1, "明日": 1, "昨天": -1, "昨日": -1, "后天": 2, "前天": -2,
             "大后天": 3, "大前天": -3}

SPAN_WORDS = {"明年": ("months", 12), "去年": ("months", -12), "今年": ("months", 0),
              "本月": ("months", 0), "这个月": ("months", 0), "本周": ("weeks", 0),
              "这周": ("weeks", 0)}

RELATIVE_HINT = re.compile(
    r"\b(now|today|tomorrow|yesterday|ago|next|last|this|coming|later|earlier)\b|from now|"
    r"^\s*in\s+\d|^\s*[+-]\s*\d|"
    r"现在|当前|此刻|今天|今日|明天|明日|昨天|昨日|后天|前天|下周|上周|本周|这周|"
    r"下个?月|上个?月|本月|这个月|明年|去年|今年|前|后|以后|之后", re.I)


def parse_delta(text):
    """'2h30m' / '3 days' / '1年2个月' -> (months, timedelta). ValueError if empty."""
    months, kwargs, found = 0, {}, False
    for num, unit in TOKEN_RE.findall(text):
        key = UNIT_ALIASES.get(unit.lower())
        if not key:
            continue
        found = True
        value = float(num)
        if key == "years":
            months += int(value * 12)
        elif key == "months":
            months += int(value)
        else:
            kwargs[key] = kwargs.get(key, 0) + value
    if not found:
        raise ValueError(f"no duration found in {text!r}")
    return months, timedelta(**kwargs)


DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def shift(dt, months=0, delta=timedelta(0)):
    """Calendar-aware shift: month/year steps clamp the day (Jan 31 + 1mo -> Feb 28)."""
    if months:
        total = dt.year * 12 + (dt.month - 1) + months
        year, month = divmod(total, 12)
        month += 1
        last = DAYS_IN_MONTH[month - 1]
        if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            last = 29
        dt = dt.replace(year=year, month=month, day=min(dt.day, last))
    return dt + delta


def extract_time_of_day(text):
    """Pull an explicit clock time out of a relative phrase ('tomorrow 9:30am')."""
    m = re.search(r"(上午|早上|凌晨|下午|晚上|中午)?\s*(\d{1,2})\s*点\s*(半|\d{1,2})?\s*分?", text)
    if m:
        hour = int(m.group(2))
        if m.group(1) in ("下午", "晚上") and hour < 12:
            hour += 12
        minute = 30 if m.group(3) == "半" else int(m.group(3) or 0)
        return text[:m.start()] + " " + text[m.end():], (hour, minute, 0)
    m = re.search(r"(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm)?", text, re.I)
    if m:
        hour, ap = int(m.group(1)), (m.group(4) or "").lower()
        if ap == "pm" and hour < 12:
            hour += 12
        if ap == "am" and hour == 12:
            hour = 0
        return text[:m.start()] + " " + text[m.end():], (hour, int(m.group(2)), int(m.group(3) or 0))
    m = re.search(r"(?<!\d)(\d{1,2})\s*(am|pm)\b", text, re.I)
    if m:
        hour = int(m.group(1)) % 12 + (12 if m.group(2).lower() == "pm" else 0)
        return text[:m.start()] + " " + text[m.end():], (hour, 0, 0)
    return text, None


def _apply_tod(dt, tod, to_midnight):
    if tod:
        return dt.replace(hour=tod[0], minute=tod[1], second=tod[2], microsecond=0)
    if to_midnight:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt


def parse_natural(text, base):
    """Resolve a relative phrase against `base`. Returns (datetime, label) or None."""
    t = text.strip().lower().replace("星期", "周").replace("礼拜", "周")
    if not RELATIVE_HINT.search(t):
        return None
    t, tod = extract_time_of_day(t)
    t = re.sub(r"\s+", " ", t).strip()

    if t in ("", "now", "现在", "当前", "此刻"):
        return _apply_tod(base, tod, False), "now"

    for word, offset in sorted(DAY_WORDS.items(), key=lambda kv: -len(kv[0])):
        if word in t:
            return _apply_tod(base + timedelta(days=offset), tod, True), f"relative day ({word})"

    # numeric offsets: '3 days ago', 'in 2 hours', '2天前', '3小时后', '+1d', '-30m'
    direction, body = None, t
    if re.search(r"(ago|earlier|前)\s*$", t):
        direction, body = -1, re.sub(r"(ago|earlier|前)\s*$", "", t)
    elif re.search(r"(later|from now|after|后|之后|以后)\s*$", t):
        direction, body = 1, re.sub(r"(later|from now|after|后|之后|以后)\s*$", "", t)
    elif t.startswith("in "):
        direction, body = 1, t[3:]
    elif re.match(r"^[+-]\s*\d", t):
        direction, body = 1, t.replace(" ", "")
    if direction is not None:
        try:
            months, delta = parse_delta(body)
        except ValueError:
            months = None
        if months is not None:
            return _apply_tod(shift(base, direction * months, direction * delta), tod, False), \
                "relative offset"

    # 下周一 / 上周五 / 本周 / 下个月 / 上个月
    m = re.fullmatch(r"(下|上|本|这)\s*个?\s*(周|月|年)\s*([一二三四五六日天])?", t)
    if m:
        step = {"下": 1, "上": -1, "本": 0, "这": 0}[m.group(1)]
        span, wd = m.group(2), m.group(3)
        if span == "周":
            dt = base + timedelta(weeks=step)
            if wd:
                idx = "一二三四五六日天".index(wd)
                idx = 6 if idx > 5 else idx
                dt = dt - timedelta(days=dt.weekday()) + timedelta(days=idx)
        elif span == "月":
            dt = shift(base, months=step)
        else:
            dt = shift(base, months=12 * step)
        return _apply_tod(dt, tod, True), "relative expression"

    for word, (kind, step) in SPAN_WORDS.items():
        if word in t:
            dt = shift(base, months=step) if kind == "months" else base + timedelta(weeks=step)
            return _apply_tod(dt, tod, True), f"relative span ({word})"

    # next monday / last friday / this week / next month
    m = re.fullmatch(r"(next|last|this|coming|past)\s+(\w+)", t)
    if m:
        word = m.group(2)
        step = 0 if m.group(1) == "this" else (1 if m.group(1) in ("next", "coming") else -1)
        if word in WEEKDAYS:
            target = WEEKDAYS[word]
            if step >= 0:
                days = (target - base.weekday()) % 7 or (7 if step else 0)
            else:
                days = -(((base.weekday() - target) % 7) or 7)
            return _apply_tod(base + timedelta(days=days), tod, True), f"weekday ({t})"
        key = UNIT_ALIASES.get(word)
        if key == "weeks":
            dt = base + timedelta(weeks=step)
        elif key == "days":
            dt = base + timedelta(days=step)
        elif key == "months":
            dt = shift(base, months=step)
        elif key == "years":
            dt = shift(base, months=12 * step)
        else:
            return None
        return _apply_tod(dt, tod, True), f"relative expression ({t})"
    return None


# --------------------------------------------------------------- entry parsing


EXCEL_DAY_OFFSET = 25569  # days from Excel's 1899-12-30 origin to the unix epoch


def parse_excel_serial(text):
    """Spreadsheet serial numbers (45900 -> a 2025 date), naive wall-clock dates.

    Excel counts 1900 as a leap year, so serials below 61 are off by one day.
    """
    t = text.strip()
    if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", t):
        return None
    serial = float(t)
    offset = EXCEL_DAY_OFFSET if serial >= 61 else EXCEL_DAY_OFFSET - 1
    naive = datetime(1970, 1, 1) + timedelta(seconds=round((serial - offset) * 86400))
    return naive, "Excel/spreadsheet serial number"


def parse_input(text, in_tz, unit=None, base=None):
    """Return (aware datetime, label, warning). Raises ValueError when unreadable."""
    text = text.strip()
    if unit == "excel":
        hit = parse_excel_serial(text)
        if not hit:
            raise ValueError(f"{text!r} is not a number, so --unit excel cannot apply")
        return hit[0].replace(tzinfo=in_tz), hit[1], None
    if unit:
        hit = parse_epoch(text, unit)
        if not hit:
            raise ValueError(f"{text!r} is not a number, so --unit cannot apply")
        return hit[0], hit[1], None

    natural = parse_natural(text, base or datetime.now(in_tz))
    if natural:
        return natural[0], natural[1], None

    compact = parse_compact(text)
    if compact:
        return compact[0].replace(tzinfo=in_tz), compact[1], None

    epoch = parse_epoch(text)
    if epoch:
        return epoch[0], epoch[1], None

    absolute = parse_absolute(text)
    if absolute:
        dt, label, warning = absolute
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=in_tz)
        return dt, label, warning

    raise ValueError(f"could not understand {text!r}")


# ------------------------------------------------------------------ formatting

NAMED_FORMATS = {
    "iso": lambda d: d.isoformat(),
    "iso8601": lambda d: d.isoformat(),
    "rfc3339": lambda d: re.sub(r"\+00:00$", "Z", d.astimezone(timezone.utc).isoformat()),
    "rfc2822": lambda d: format_datetime(d),
    "http": lambda d: format_datetime(d.astimezone(timezone.utc), usegmt=True),
    "unix": lambda d: str(int(d.timestamp())),
    "unix_ms": lambda d: str(int(d.timestamp() * 1_000)),
    "unix_us": lambda d: str(int(d.timestamp() * 1_000_000)),
    "unix_ns": lambda d: str(int(d.timestamp() * 1_000_000_000)),
    "date": lambda d: d.strftime("%Y-%m-%d"),
    "time": lambda d: d.strftime("%H:%M:%S"),
    "datetime": lambda d: d.strftime("%Y-%m-%d %H:%M:%S"),
    "sql": lambda d: d.strftime("%Y-%m-%d %H:%M:%S"),
    "compact": lambda d: d.strftime("%Y%m%d%H%M%S"),
    "cn": lambda d: d.strftime("%Y年%m月%d日 %H:%M:%S"),
}


def render(dt, fmt):
    named = NAMED_FORMATS.get(fmt.strip().lower())
    return named(dt) if named else dt.strftime(fmt)


def human_duration(seconds, max_parts=2):
    seconds = abs(float(seconds))
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    parts = []
    for name, size in (("year", 31_536_000), ("month", 2_592_000), ("day", 86_400),
                       ("hour", 3_600), ("minute", 60), ("second", 1)):
        if seconds >= size:
            count, seconds = divmod(seconds, size)
            parts.append(f"{int(count)} {name}{'s' if count != 1 else ''}")
            if len(parts) == max_parts:
                break
    return " ".join(parts) or "0 seconds"


def relative_to_now(dt):
    seconds = (dt - datetime.now(timezone.utc)).total_seconds()
    if abs(seconds) < 1:
        return "just now"
    return f"in {human_duration(seconds)}" if seconds > 0 else f"{human_duration(seconds)} ago"


def build_report(dt, tz, source=None, label=None, custom_fmt=None, warning=None):
    view = dt.astimezone(tz)
    utc = dt.astimezone(timezone.utc)
    stamp = dt.timestamp()
    data = {
        "input": source,
        "parsed_as": label,
        "unix": int(stamp),
        "unix_ms": int(stamp * 1_000),
        "utc": render(utc, "rfc3339"),
        "iso8601": view.isoformat(),
        "datetime": view.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": f"{getattr(tz, 'key', str(tz))} ({tz_label(view)})",
        "rfc2822": format_datetime(view),
        "weekday": view.strftime("%A"),
        "iso_week": view.strftime("%G-W%V-%u"),
        "day_of_year": int(view.strftime("%j")),
        "relative": relative_to_now(dt),
    }
    if custom_fmt:
        data["formatted"] = render(view, custom_fmt)
    if warning:
        data["warning"] = warning
    return data


REPORT_ROWS = [
    ("input", "input"), ("parsed as", "parsed_as"), ("unix (s)", "unix"),
    ("unix (ms)", "unix_ms"), ("UTC", "utc"), ("local time", "datetime"),
    ("timezone", "timezone"), ("ISO 8601", "iso8601"), ("RFC 2822", "rfc2822"),
    ("calendar", "_calendar"), ("relative", "relative"), ("formatted", "formatted"),
]


def print_report(data):
    data = dict(data)
    data["_calendar"] = (f"{data['weekday']}, ISO week {data['iso_week']}, "
                         f"day {data['day_of_year']} of year")
    for label, key in REPORT_ROWS:
        value = data.get(key)
        if value is not None:
            print(f"{label:<11} {value}")
    if data.get("warning"):
        print(f"\nnote: {data['warning']}")


def do_diff(a, b, tz):
    seconds = (b - a).total_seconds()
    data = {
        "from": a.astimezone(tz).isoformat(),
        "to": b.astimezone(tz).isoformat(),
        "seconds": seconds,
        "minutes": round(seconds / 60, 3),
        "hours": round(seconds / 3600, 3),
        "days": round(seconds / 86400, 3),
        "human": human_duration(seconds, max_parts=4),
        "direction": "later" if seconds >= 0 else "earlier",
    }
    return data


def print_diff(data):
    print(f"from        {data['from']}")
    print(f"to          {data['to']}")
    print(f"difference  {data['human']} ({data['direction']})")
    print(f"seconds     {data['seconds']:,.0f}")
    print(f"in days     {data['days']:,.3f}   hours {data['hours']:,.3f}   "
          f"minutes {data['minutes']:,.3f}")


EPILOG = """examples:
  dtconv.py                                   # everything about "now"
  dtconv.py 1735689600 -z Asia/Shanghai       # timestamp -> local wall clock
  dtconv.py "2026-08-26 15:30" -f unix_ms     # datetime string -> epoch millis
  dtconv.py "2026-08-26T07:30:00Z" -z America/New_York
  dtconv.py "3 days ago" "下周一 09:00"        # natural language, one line each
  dtconv.py now --add "-2h30m" -f iso         # arithmetic
  dtconv.py "2026-01-01" --diff "2026-12-25"  # duration between two moments
  dtconv.py 1735689600 --json                 # machine-readable output

named formats for -f: """ + ", ".join(sorted(NAMED_FORMATS)) + """
  (anything else is treated as a strftime pattern, e.g. -f "%Y/%m/%d %H:%M")
"""


def build_parser():
    p = argparse.ArgumentParser(
        prog="dtconv", description="Convert between timestamps, datetime strings, "
        "timezones and formats.", epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", nargs="*", help="timestamps / datetime strings / phrases "
                   "like '3 days ago' (default: now)")
    p.add_argument("-z", "--tz", default="local", help="output timezone: IANA name, "
                   "UTC, +08:00 or local (default: local)")
    p.add_argument("--in-tz", default="local", help="timezone assumed for inputs that "
                   "carry no offset (default: local)")
    p.add_argument("-f", "--format", help="output only this format (named or strftime)")
    p.add_argument("-u", "--unit", choices=sorted(UNIT_DIVISOR) + ["excel"],
                   help="force the unit of numeric input instead of guessing; "
                        "'excel' reads spreadsheet serial numbers")
    p.add_argument("--add", metavar="DELTA", help="shift the result, e.g. '+3d', "
                   "'-2h30m', '1 month', '1年2个月'")
    p.add_argument("--diff", metavar="OTHER", help="show the duration from input to OTHER")
    p.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    return p


VALUE_FLAGS = ("--add", "--diff")


def normalize_argv(argv):
    """Let '--add -2h30m' work: argparse would otherwise read the value as a flag."""
    out, i = [], 0
    while i < len(argv):
        arg = argv[i]
        if arg in VALUE_FLAGS and i + 1 < len(argv) and re.match(r"^-\s*\d", argv[i + 1]):
            out.append(f"{arg}={argv[i + 1]}")
            i += 2
            continue
        out.append(arg)
        i += 1
    return out


def main(argv=None):
    args = build_parser().parse_args(normalize_argv(list(argv if argv is not None else sys.argv[1:])))
    try:
        out_tz, in_tz = get_tz(args.tz), get_tz(args.in_tz)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    inputs = args.input or ["now"]
    base = datetime.now(in_tz)
    results = []
    for raw in inputs:
        try:
            dt, label, warning = parse_input(raw, in_tz, args.unit, base)
            if args.add:
                months, delta = parse_delta(args.add)
                dt = shift(dt, months, delta)
                label = f"{label} + {args.add.strip()}"
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        results.append((raw, dt, label, warning))

    if args.diff:
        try:
            other, _, _ = parse_input(args.diff, in_tz, args.unit, base)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        payload = [do_diff(dt, other, out_tz) for _, dt, _, _ in results]
        if args.json:
            print(json.dumps(payload[0] if len(payload) == 1 else payload,
                             indent=2, ensure_ascii=False))
        else:
            for i, item in enumerate(payload):
                if i:
                    print()
                print_diff(item)
        return 0

    reports = [build_report(dt, out_tz, raw, label, args.format, warning)
               for raw, dt, label, warning in results]
    if args.json:
        print(json.dumps(reports[0] if len(reports) == 1 else reports,
                         indent=2, ensure_ascii=False))
    elif args.format:
        for report in reports:
            prefix = f"{report['input']} -> " if len(reports) > 1 else ""
            print(f"{prefix}{report['formatted']}")
            if report.get("warning"):
                print(f"note: {report['warning']}", file=sys.stderr)
    else:
        for i, report in enumerate(reports):
            if i:
                print()
            print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
