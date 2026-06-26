#!/usr/bin/env python3
"""Single-reference BaZi (Four Pillars) calculator + DaYun (10-year luck cycles)."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from lunar_python import Solar

STEMS = "甲乙丙丁戊己庚辛壬癸"
YANG_STEMS = set("甲丙戊庚壬")
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
CYCLE = [STEMS[i % 10] + BRANCHES[i % 12] for i in range(60)]
CYCLE_INDEX = {gz: i for i, gz in enumerate(CYCLE)}


@dataclass
class Reference:
    dt: datetime
    year: str
    month: str
    day: str
    hour: str


def parse_dt(s: str, tz: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo(tz))


def load_reference(path: str, tz: str) -> Reference:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    dt = parse_dt(raw["reference_datetime"], tz)
    year = raw["reference_pillars"]["year"]
    month = raw["reference_pillars"]["month"]
    day = raw["reference_pillars"]["day"]
    hour = raw["reference_pillars"]["hour"]

    for p in (year, month, day, hour):
        if p not in CYCLE_INDEX:
            raise ValueError(f"Invalid pillar in reference: {p}")

    return Reference(dt=dt, year=year, month=month, day=day, hour=hour)


def lichun_adjusted_year(dt: datetime) -> int:
    boundary = dt.replace(month=2, day=4, hour=0, minute=0)
    return dt.year if dt >= boundary else dt.year - 1


def months_diff(a: datetime, b: datetime) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def hour_bin_start(dt: datetime) -> datetime:
    h = dt.hour
    if h == 23:
        return dt.replace(minute=0)
    if h % 2 == 1:
        h -= 1
    return dt.replace(hour=h, minute=0)


def hour_bins_diff(a: datetime, b: datetime) -> int:
    delta = b - a
    return int(delta.total_seconds() // 7200)


def shift_pillar(base: str, offset: int) -> str:
    return CYCLE[(CYCLE_INDEX[base] + offset) % 60]


def year_pillar_at(dt: datetime, ref: Reference) -> str:
    y_offset = lichun_adjusted_year(dt) - lichun_adjusted_year(ref.dt)
    return shift_pillar(ref.year, y_offset)


def calculate_pillars(birth: datetime, ref: Reference) -> dict:
    y_offset = lichun_adjusted_year(birth) - lichun_adjusted_year(ref.dt)
    m_offset = months_diff(ref.dt, birth)
    d_offset = (birth.date() - ref.dt.date()).days
    h_offset = hour_bins_diff(hour_bin_start(ref.dt), hour_bin_start(birth))

    year_pillar = shift_pillar(ref.year, y_offset)
    month_pillar = shift_pillar(ref.month, m_offset)
    day_pillar = shift_pillar(ref.day, d_offset)
    hour_pillar = shift_pillar(ref.hour, h_offset)

    return {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar,
        "eight_characters": f"{hour_pillar} {day_pillar} {month_pillar} {year_pillar}",
    }


def get_dayun_direction(year_stem: str, gender: str) -> tuple[bool, str]:
    is_yang_year = year_stem in YANG_STEMS
    # Rule: 阳男阴女顺，阴男阳女逆
    forward = (gender == "male" and is_yang_year) or (gender == "female" and not is_yang_year)
    return forward, ("顺排" if forward else "逆排")


def calc_start_age(birth: datetime, forward: bool) -> float:
    s = Solar.fromYmdHms(birth.year, birth.month, birth.day, birth.hour, birth.minute, 0)
    l = s.getLunar()
    jq = l.getNextJie(True) if forward else l.getPrevJie(True)
    jq_dt = parse_dt(jq.getSolar().toYmdHms()[:16], str(birth.tzinfo))
    delta_sec = (jq_dt - birth).total_seconds() if forward else (birth - jq_dt).total_seconds()
    days = max(delta_sec / 86400.0, 0.0)
    # Traditional conversion: 3 days = 1 year
    return round(days / 3.0, 2)


def build_dayun(month_pillar: str, start_age: float, forward: bool, count: int = 8) -> list[tuple[str, str]]:
    step = 1 if forward else -1
    out = []
    for i in range(1, count + 1):
        gz = shift_pillar(month_pillar, step * i)
        a0 = int(start_age) + (i - 1) * 10
        a1 = a0 + 9
        out.append((gz, f"{a0}-{a1}"))
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--birth", required=True, help='Birth datetime, e.g. "1992-08-14 21:35"')
    p.add_argument("--tz", default="Asia/Shanghai", help="IANA timezone")
    p.add_argument("--reference", required=True, help="Path to single reference JSON")
    p.add_argument("--gender", choices=["male", "female"], help="Required for DaYun calculation")
    args = p.parse_args()

    birth = parse_dt(args.birth, args.tz)
    ref = load_reference(args.reference, args.tz)
    result = calculate_pillars(birth, ref)

    print(f"Birth (local): {birth.strftime('%Y-%m-%d %H:%M')} ({args.tz})")
    print("时柱 日柱 月柱 年柱 当前大运 流年")
    current_dayun = "-"

    now = datetime.now(ZoneInfo(args.tz))
    current_liunian = year_pillar_at(now, ref)

    if args.gender:
        forward, direction_txt = get_dayun_direction(result["year"][0], args.gender)
        start_age = calc_start_age(birth, forward)
        dayun = build_dayun(result["month"], start_age, forward)

        age_now = (now - birth).days / 365.2425
        idx = int((age_now - start_age) // 10)
        if 0 <= idx < len(dayun):
            current_dayun = dayun[idx][0]
        elif idx < 0:
            current_dayun = "未起运"
        else:
            current_dayun = dayun[-1][0]
    else:
        direction_txt = "(need --gender)"
        start_age = None
        dayun = []

    d1 = current_dayun[:1] if len(current_dayun) == 2 else current_dayun
    d2 = current_dayun[1:] if len(current_dayun) == 2 else ""
    print(f" {result['hour'][0]}   {result['day'][0]}   {result['month'][0]}   {result['year'][0]}   {d1}   {current_liunian[0]}")
    print(f" {result['hour'][1]}   {result['day'][1]}   {result['month'][1]}   {result['year'][1]}   {d2}   {current_liunian[1]}")
    print(f"Eight Characters (L→R Hour/Day/Month/Year): {result['eight_characters']}")
    print(f"Current LiuNian ({now.year}): {current_liunian}")

    if args.gender:
        print(f"DaYun Direction: {direction_txt} ({'male' if args.gender=='male' else 'female'})")
        print(f"DaYun Start Age: {start_age}")
        print("DaYun List:")
        for gz, age_range in dayun:
            print(f"- {gz} ({age_range})")


if __name__ == "__main__":
    main()
