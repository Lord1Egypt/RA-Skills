#!/usr/bin/env python3
"""本地生日提醒计算器。

特性：
- 支持阳历与农历生日
- 每条记录可覆盖全局默认值
- 支持当天提醒、提前 N 天、多次提醒
- 默认时区 Asia/Shanghai

用法示例：
  python3 scripts/birthday_reminder.py check --config assets/birthdays.example.json
  python3 scripts/birthday_reminder.py check --config assets/birthdays.example.json --now 2026-03-25T09:00:00+08:00
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from dataclasses import dataclass
from zoneinfo import ZoneInfo

DEFAULT_TZ = "Asia/Shanghai"
DEFAULT_REMIND_AT = "09:00"
DEFAULT_OFFSETS = [0]
DEFAULT_WINDOW_MINUTES = 70

# 1900-2099 农历数据（常见公开算法）
LUNAR_INFO = [
    0x04BD8, 0x04AE0, 0x0A570, 0x054D5, 0x0D260, 0x0D950, 0x16554, 0x056A0, 0x09AD0, 0x055D2,
    0x04AE0, 0x0A5B6, 0x0A4D0, 0x0D250, 0x1D255, 0x0B540, 0x0D6A0, 0x0ADA2, 0x095B0, 0x14977,
    0x04970, 0x0A4B0, 0x0B4B5, 0x06A50, 0x06D40, 0x1AB54, 0x02B60, 0x09570, 0x052F2, 0x04970,
    0x06566, 0x0D4A0, 0x0EA50, 0x06E95, 0x05AD0, 0x02B60, 0x186E3, 0x092E0, 0x1C8D7, 0x0C950,
    0x0D4A0, 0x1D8A6, 0x0B550, 0x056A0, 0x1A5B4, 0x025D0, 0x092D0, 0x0D2B2, 0x0A950, 0x0B557,
    0x06CA0, 0x0B550, 0x15355, 0x04DA0, 0x0A5B0, 0x14573, 0x052B0, 0x0A9A8, 0x0E950, 0x06AA0,
    0x0AEA6, 0x0AB50, 0x04B60, 0x0AAE4, 0x0A570, 0x05260, 0x0F263, 0x0D950, 0x05B57, 0x056A0,
    0x096D0, 0x04DD5, 0x04AD0, 0x0A4D0, 0x0D4D4, 0x0D250, 0x0D558, 0x0B540, 0x0B5A0, 0x195A6,
    0x095B0, 0x049B0, 0x0A974, 0x0A4B0, 0x0B27A, 0x06A50, 0x06D40, 0x0AF46, 0x0AB60, 0x09570,
    0x04AF5, 0x04970, 0x064B0, 0x074A3, 0x0EA50, 0x06B58, 0x05AC0, 0x0AB60, 0x096D5, 0x092E0,
    0x0C960, 0x0D954, 0x0D4A0, 0x0DA50, 0x07552, 0x056A0, 0x0ABB7, 0x025D0, 0x092D0, 0x0CAB5,
    0x0A950, 0x0B4A0, 0x0BAA4, 0x0AD50, 0x055D9, 0x04BA0, 0x0A5B0, 0x15176, 0x052B0, 0x0A930,
    0x07954, 0x06AA0, 0x0AD50, 0x05B52, 0x04B60, 0x0A6E6, 0x0A4E0, 0x0D260, 0x0EA65, 0x0D530,
    0x05AA0, 0x076A3, 0x096D0, 0x04AFB, 0x04AD0, 0x0A4D0, 0x1D0B6, 0x0D250, 0x0D520, 0x0DD45,
    0x0B5A0, 0x056D0, 0x055B2, 0x049B0, 0x0A577, 0x0A4B0, 0x0AA50, 0x1B255, 0x06D20, 0x0ADA0,
    0x14B63,
]


@dataclass
class PersonConfig:
    name: str
    calendar: str
    month: int
    day: int
    leap_month: bool
    remind_at: str
    offset_days: list[int]
    timezone: str
    leap_strategy: str


def leap_month_of_year(year: int) -> int:
    return LUNAR_INFO[year - 1900] & 0xF


def leap_days(year: int) -> int:
    if leap_month_of_year(year):
        return 30 if (LUNAR_INFO[year - 1900] & 0x10000) else 29
    return 0


def month_days(year: int, month: int) -> int:
    return 30 if (LUNAR_INFO[year - 1900] & (0x10000 >> month)) else 29


def lunar_year_days(year: int) -> int:
    total = 348
    mask = 0x8000
    while mask > 0x8:
        total += 1 if (LUNAR_INFO[year - 1900] & mask) else 0
        mask >>= 1
    return total + leap_days(year)


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool) -> dt.date:
    if year < 1900 or year > 2099:
        raise ValueError("农历转换仅支持 1900-2099 年")
    if month < 1 or month > 12:
        raise ValueError("农历月份必须为 1-12")
    if day < 1 or day > 30:
        raise ValueError("农历日期必须为 1-30")

    leap_month = leap_month_of_year(year)
    if is_leap_month and leap_month != month:
        raise ValueError(f"{year} 年没有闰 {month} 月")

    offset = 0
    for y in range(1900, year):
        offset += lunar_year_days(y)

    for m in range(1, month):
        offset += month_days(year, m)
        if leap_month == m:
            offset += leap_days(year)

    if is_leap_month:
        offset += month_days(year, month)

    max_day = leap_days(year) if is_leap_month else month_days(year, month)
    if day > max_day:
        raise ValueError(f"{year} 年农历 {'闰' if is_leap_month else ''}{month} 月没有 {day} 日")

    offset += day - 1
    base = dt.date(1900, 1, 31)
    return base + dt.timedelta(days=offset)


def parse_hhmm(hhmm: str) -> tuple[int, int]:
    try:
        h_str, m_str = hhmm.split(":", 1)
        hour, minute = int(h_str), int(m_str)
    except Exception as exc:
        raise ValueError(f"非法提醒时间：{hhmm}") from exc
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"非法提醒时间：{hhmm}")
    return hour, minute


def normalize_offsets(raw: list[int]) -> list[int]:
    vals = sorted({int(x) for x in raw})
    if any(x < 0 for x in vals):
        raise ValueError("offset_days 不能为负数")
    return vals


def resolve_person(defaults: dict, item: dict) -> PersonConfig:
    calendar = str(item.get("calendar", defaults.get("calendar", "solar"))).lower()
    if calendar not in ("solar", "lunar"):
        raise ValueError(f"{item.get('name', 'unknown')} 的 calendar 必须是 solar/lunar")

    offsets = normalize_offsets(item.get("offset_days", defaults.get("offset_days", DEFAULT_OFFSETS)))
    remind_at = str(item.get("remind_at", defaults.get("remind_at", DEFAULT_REMIND_AT)))
    timezone = str(item.get("timezone", defaults.get("timezone", DEFAULT_TZ)))
    leap_strategy = str(item.get("leap_strategy", defaults.get("leap_strategy", "skip")))
    if leap_strategy not in ("skip", "use-non-leap"):
        raise ValueError("leap_strategy 仅支持 skip/use-non-leap")

    name = str(item["name"])
    month = int(item["month"])
    day = int(item["day"])
    leap_month = bool(item.get("leap_month", False))

    return PersonConfig(
        name=name,
        calendar=calendar,
        month=month,
        day=day,
        leap_month=leap_month,
        remind_at=remind_at,
        offset_days=offsets,
        timezone=timezone,
        leap_strategy=leap_strategy,
    )


def birthday_date_for_year(person: PersonConfig, year: int) -> dt.date:
    if person.calendar == "solar":
        try:
            return dt.date(year, person.month, person.day)
        except ValueError:
            # 例如 2/29 在平年：默认顺延到 3/1
            if person.month == 2 and person.day == 29:
                return dt.date(year, 3, 1)
            raise

    try:
        return lunar_to_solar(year, person.month, person.day, person.leap_month)
    except ValueError:
        if person.leap_month and person.leap_strategy == "use-non-leap":
            return lunar_to_solar(year, person.month, person.day, False)
        raise


def scheduled_times(person: PersonConfig, now: dt.datetime) -> list[tuple[dt.datetime, dt.date, int]]:
    tz = ZoneInfo(person.timezone or DEFAULT_TZ)
    now_local = now.astimezone(tz)
    hour, minute = parse_hhmm(person.remind_at)

    candidates = []
    for year in (now_local.year - 1, now_local.year, now_local.year + 1, now_local.year + 2):
        birthday = birthday_date_for_year(person, year)
        for offset in person.offset_days:
            remind_day = birthday - dt.timedelta(days=offset)
            remind_dt = dt.datetime(
                remind_day.year,
                remind_day.month,
                remind_day.day,
                hour,
                minute,
                tzinfo=tz,
            )
            candidates.append((remind_dt, birthday, offset))
    return candidates


def check_due(config: dict, now: dt.datetime, window_minutes: int) -> list[dict]:
    defaults = config.get("defaults", {})
    people = config.get("people", [])

    if not isinstance(people, list):
        raise ValueError("people 必须是数组")

    due_from = now - dt.timedelta(minutes=window_minutes)
    rows: list[dict] = []

    for raw in people:
        person = resolve_person(defaults, raw)
        for remind_dt, birthday, offset in scheduled_times(person, now):
            remind_utc = remind_dt.astimezone(dt.timezone.utc)
            if due_from <= remind_utc <= now:
                rows.append(
                    {
                        "name": person.name,
                        "calendar": person.calendar,
                        "birthday_date": birthday.isoformat(),
                        "offset_days": offset,
                        "remind_at": remind_dt.isoformat(),
                        "message": f"{person.name} 生日提醒：{'当天' if offset == 0 else f'提前 {offset} 天'}（生日 {birthday.isoformat()}）",
                    }
                )

    rows.sort(key=lambda x: x["remind_at"])
    return rows


def list_all_reminders(config: dict, now: dt.datetime) -> list[dict]:
    defaults = config.get("defaults", {})
    people = config.get("people", [])
    if not isinstance(people, list):
        raise ValueError("people 必须是数组")

    rows: list[dict] = []
    for raw in people:
        person = resolve_person(defaults, raw)
        tz = ZoneInfo(person.timezone or DEFAULT_TZ)
        now_local = now.astimezone(tz)
        hour, minute = parse_hhmm(person.remind_at)

        this_year = birthday_date_for_year(person, now_local.year)
        next_year = birthday_date_for_year(person, now_local.year + 1)
        birthday = this_year if this_year >= now_local.date() else next_year

        for offset in person.offset_days:
            remind_day = birthday - dt.timedelta(days=offset)
            remind_dt = dt.datetime(
                remind_day.year,
                remind_day.month,
                remind_day.day,
                hour,
                minute,
                tzinfo=tz,
            )
            rows.append(
                {
                    "name": person.name,
                    "calendar": person.calendar,
                    "birthday_date": birthday.isoformat(),
                    "offset_days": offset,
                    "remind_at": remind_dt.isoformat(),
                    "timezone": person.timezone,
                }
            )
    rows.sort(key=lambda x: (x["remind_at"], x["name"]))
    return rows


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_now(raw_now: str | None, timezone: str) -> dt.datetime:
    tz = ZoneInfo(timezone)
    if raw_now:
        raw = raw_now.strip()
        parsed = None
        # 优先支持更易读的格式：yyyy-MM-DD HH:mm:ss
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                parsed = dt.datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue
        if parsed is None:
            parsed = dt.datetime.fromisoformat(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        return parsed.astimezone(dt.timezone.utc)
    return dt.datetime.now(tz).astimezone(dt.timezone.utc)


def cmd_check(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    tz_name = config.get("defaults", {}).get("timezone", DEFAULT_TZ)
    now = parse_now(args.now, tz_name)
    rows = check_due(config, now, args.window_minutes)

    if args.output == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        if not rows:
            print("无到期提醒")
            return 0
        for row in rows:
            print(f"[{row['remind_at']}] {row['message']}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    tz_name = config.get("defaults", {}).get("timezone", DEFAULT_TZ)
    now = parse_now(args.now, tz_name)
    rows = list_all_reminders(config, now)

    if args.output == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        if not rows:
            print("无已配置提醒")
            return 0
        for row in rows:
            offset_text = "当天" if row["offset_days"] == 0 else f"提前 {row['offset_days']} 天"
            print(
                f"[{row['remind_at']}] {row['name']} ({row['calendar']}) {offset_text} "
                f"-> 生日 {row['birthday_date']} ({row['timezone']})"
            )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="本地生日提醒计算器")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="检查当前窗口内到期提醒")
    check.add_argument("--config", required=True, help="生日配置 JSON 路径")
    check.add_argument("--window-minutes", type=int, default=DEFAULT_WINDOW_MINUTES, help="检查窗口（分钟），默认 70")
    check.add_argument("--now", default=None, help="测试时间，例如 2026-03-25 09:00:00")
    check.add_argument("--output", choices=["text", "json"], default="text")
    check.set_defaults(func=cmd_check)

    list_cmd = sub.add_parser("list", help="列出所有已配置提醒（按下一次生日计算）")
    list_cmd.add_argument("--config", required=True, help="生日配置 JSON 路径")
    list_cmd.add_argument("--now", default=None, help="基准时间，例如 2026-03-25 09:00:00")
    list_cmd.add_argument("--output", choices=["text", "json"], default="text")
    list_cmd.set_defaults(func=cmd_list)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
