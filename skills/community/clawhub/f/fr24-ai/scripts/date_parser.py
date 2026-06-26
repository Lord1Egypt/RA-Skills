"""日期归一化为 YYYY-MM-DD（Asia/Shanghai）。"""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")

RELATIVE = {
    "今天": 0,
    "今日": 0,
    "明天": 1,
    "明日": 1,
    "后天": 2,
}

WEEKDAY_CN = {
    "一": 0,
    "二": 1,
    "三": 2,
    "四": 3,
    "五": 4,
    "六": 5,
    "日": 6,
    "天": 6,
}


def today() -> date:
    return datetime.now(TZ).date()


def parse_date(text: str, base: date | None = None) -> tuple[str | None, str | None]:
    if not text or not str(text).strip():
        return None, "日期不能为空"
    raw = str(text).strip()
    base = base or today()

    if raw in RELATIVE:
        d = base + timedelta(days=RELATIVE[raw])
        return d.isoformat(), None

    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", raw)
    if m:
        return _safe_iso(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.fullmatch(r"(\d{4})[/.](\d{1,2})[/.](\d{1,2})", raw)
    if m:
        return _safe_iso(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    if raw in ("下周", "下星期"):
        this_monday = base - timedelta(days=base.weekday())
        return (this_monday + timedelta(days=7)).isoformat(), None
    if raw in ("本周", "本星期"):
        this_monday = base - timedelta(days=base.weekday())
        d = this_monday if this_monday >= base else this_monday + timedelta(days=7)
        return d.isoformat(), None

    week_m = re.fullmatch(r"(?:(本|下)周|下星期|本星期)([一二三四五六日天])", raw)
    if week_m:
        return _parse_weekday(week_m.group(1), week_m.group(2), base)

    m = re.fullmatch(r"(\d{1,2})月(\d{1,2})[日号]?", raw)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        year = base.year
        try:
            d = date(year, month, day)
        except ValueError:
            return None, f"日期无效：{raw}"
        if d < base:
            try:
                d = date(year + 1, month, day)
            except ValueError:
                return None, f"日期无效：{raw}"
        return d.isoformat(), None

    return None, f"无法解析日期：{raw}，请使用 YYYY-MM-DD 或「7月1日」"


def _parse_weekday(which: str, day_cn: str, base: date) -> tuple[str | None, str | None]:
    wd = WEEKDAY_CN.get(day_cn)
    if wd is None:
        return None, f"无法解析星期：{day_cn}"
    this_monday = base - timedelta(days=base.weekday())
    week_monday = this_monday if which == "本" else this_monday + timedelta(days=7)
    target = week_monday + timedelta(days=wd)
    if which == "本" and target < base:
        target = target + timedelta(days=7)
    return target.isoformat(), None


def _safe_iso(year: int, month: int, day: int) -> tuple[str | None, str | None]:
    try:
        return date(year, month, day).isoformat(), None
    except ValueError:
        return None, f"日期无效：{year}-{month}-{day}"
