"""Pure Python Chinese lunar calendar helpers for cross-platform rendering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import lru_cache

LUNAR_INFO = (
    0x04BD8,
    0x04AE0,
    0x0A570,
    0x054D5,
    0x0D260,
    0x0D950,
    0x16554,
    0x056A0,
    0x09AD0,
    0x055D2,
    0x04AE0,
    0x0A5B6,
    0x0A4D0,
    0x0D250,
    0x1D255,
    0x0B540,
    0x0D6A0,
    0x0ADA2,
    0x095B0,
    0x14977,
    0x04970,
    0x0A4B0,
    0x0B4B5,
    0x06A50,
    0x06D40,
    0x1AB54,
    0x02B60,
    0x09570,
    0x052F2,
    0x04970,
    0x06566,
    0x0D4A0,
    0x0EA50,
    0x06E95,
    0x05AD0,
    0x02B60,
    0x186E3,
    0x092E0,
    0x1C8D7,
    0x0C950,
    0x0D4A0,
    0x1D8A6,
    0x0B550,
    0x056A0,
    0x1A5B4,
    0x025D0,
    0x092D0,
    0x0D2B2,
    0x0A950,
    0x0B557,
    0x06CA0,
    0x0B550,
    0x15355,
    0x04DA0,
    0x0A5D0,
    0x14573,
    0x052D0,
    0x0A9A8,
    0x0E950,
    0x06AA0,
    0x0AEA6,
    0x0AB50,
    0x04B60,
    0x0AAE4,
    0x0A570,
    0x05260,
    0x0F263,
    0x0D950,
    0x05B57,
    0x056A0,
    0x096D0,
    0x04DD5,
    0x04AD0,
    0x0A4D0,
    0x0D4D4,
    0x0D250,
    0x0D558,
    0x0B540,
    0x0B5A0,
    0x195A6,
    0x095B0,
    0x049B0,
    0x0A974,
    0x0A4B0,
    0x0B27A,
    0x06A50,
    0x06D40,
    0x0AF46,
    0x0AB60,
    0x09570,
    0x04AF5,
    0x04970,
    0x064B0,
    0x074A3,
    0x0EA50,
    0x06B58,
    0x05AC0,
    0x0AB60,
    0x096D5,
    0x092E0,
    0x0C960,
    0x0D954,
    0x0D4A0,
    0x0DA50,
    0x07552,
    0x056A0,
    0x0ABB7,
    0x025D0,
    0x092D0,
    0x0CAB5,
    0x0A950,
    0x0B4A0,
    0x0BAA4,
    0x0AD50,
    0x055D9,
    0x04BA0,
    0x0A5B0,
    0x15176,
    0x052B0,
    0x0A930,
    0x07954,
    0x06AA0,
    0x0AD50,
    0x05B52,
    0x04B60,
    0x0A6E6,
    0x0A4E0,
    0x0D260,
    0x0EA65,
    0x0D530,
    0x05AA0,
    0x076A3,
    0x096D0,
    0x04BD7,
    0x04AD0,
    0x0A4D0,
    0x1D0B6,
    0x0D250,
    0x0D520,
    0x0DD45,
    0x0B5A0,
    0x056D0,
    0x055B2,
    0x049B0,
    0x0A577,
    0x0A4B0,
    0x0AA50,
    0x1B255,
    0x06D20,
    0x0ADA0,
)
BASE_SOLAR_DATE = date(1900, 1, 31)
MAX_SUPPORTED_YEAR = 1900 + len(LUNAR_INFO) - 1
LUNAR_MONTH_NAMES = ("", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊")
LUNAR_DAY_PREFIX = ("初", "十", "廿", "三")
LUNAR_DAY_DIGITS = ("", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十")


@dataclass(frozen=True)
class LunarDate:
    year: int
    month: int
    day: int
    is_leap_month: bool = False


def leap_month(year: int) -> int:
    return LUNAR_INFO[year - 1900] & 0xF


def leap_days(year: int) -> int:
    leap = leap_month(year)
    if not leap:
        return 0
    return 30 if (LUNAR_INFO[year - 1900] & 0x10000) else 29


def month_days(year: int, month: int) -> int:
    if month < 1 or month > 12:
        raise ValueError(f"Invalid lunar month: {month}")
    return 30 if (LUNAR_INFO[year - 1900] & (0x10000 >> month)) else 29


def lunar_year_days(year: int) -> int:
    days = 348
    month_bits = LUNAR_INFO[year - 1900] >> 4
    for _ in range(12):
        days += month_bits & 1
        month_bits >>= 1
    return days + leap_days(year)


def format_lunar_day(day: int) -> str:
    if day <= 0 or day > 30:
        return ""
    if day == 10:
        return "初十"
    if day == 20:
        return "二十"
    if day == 30:
        return "三十"
    prefix = LUNAR_DAY_PREFIX[(day - 1) // 10]
    suffix = LUNAR_DAY_DIGITS[day % 10]
    return f"{prefix}{suffix}"


@lru_cache(maxsize=512)
def solar_to_lunar(solar_date: date) -> LunarDate:
    if solar_date < BASE_SOLAR_DATE:
        raise ValueError(f"Unsupported date before {BASE_SOLAR_DATE.isoformat()}: {solar_date.isoformat()}")

    offset = (solar_date - BASE_SOLAR_DATE).days
    lunar_year = 1900
    while lunar_year <= MAX_SUPPORTED_YEAR:
        year_days = lunar_year_days(lunar_year)
        if offset < year_days:
            break
        offset -= year_days
        lunar_year += 1
    if lunar_year > MAX_SUPPORTED_YEAR:
        raise ValueError(
            f"Unsupported date after the encoded lunar calendar range ending in {MAX_SUPPORTED_YEAR}: {solar_date.isoformat()}"
        )

    leap = leap_month(lunar_year)
    lunar_month = 1
    is_leap_month = False
    while lunar_month <= 12:
        if leap and lunar_month == leap + 1 and not is_leap_month:
            lunar_month -= 1
            is_leap_month = True
            month_length = leap_days(lunar_year)
        else:
            month_length = month_days(lunar_year, lunar_month)

        if offset < month_length:
            break

        offset -= month_length
        if is_leap_month and lunar_month == leap:
            is_leap_month = False
        lunar_month += 1

    return LunarDate(year=lunar_year, month=lunar_month, day=offset + 1, is_leap_month=is_leap_month)


def format_lunar_text(solar_date: date) -> str:
    lunar = solar_to_lunar(solar_date)
    month_name = LUNAR_MONTH_NAMES[lunar.month] if 0 < lunar.month < len(LUNAR_MONTH_NAMES) else ""
    day_name = format_lunar_day(lunar.day)
    if not month_name or not day_name:
        return ""
    prefix = "农历 闰" if lunar.is_leap_month else "农历 "
    return f"{prefix}{month_name}月{day_name}"
