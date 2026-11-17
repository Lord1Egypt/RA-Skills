#!/usr/bin/env python3
"""
co_parenting_calendar.py — custody rotation engine for co-parents.

Subcommands:
  plan       Generate a dated custody rotation (alternating-week, 2-2-3,
             3-4-4-3) with overnight counts and ICS export.
  holidays   Holiday priority table for a year (alternating priority,
             Mother's/Father's Day pinned to the named parent).
  fairness   Overnight / weekend / weekday split audit with <35% flag.
  override   Patch a date range to one parent + make-up-time suggestion.

Stdlib only. Offline. Informational tool — not legal advice.
"""
import argparse
import json
import sys
from datetime import date, timedelta

# ─── Rotation patterns: cyclic (days, parent) blocks from the start date ───
SCHEDULES = {
    # Classic 7/7: one full week per parent, exchange Friday or Monday.
    "alternating-week": [(7, "A"), (7, "B")],
    # 2-2-3: Wk1 A(Mon,Tue) B(Wed,Thu) A(Fri-Sun); Wk2 mirrored. 14-day cycle.
    "2-2-3": [(2, "A"), (2, "B"), (3, "A"), (2, "B"), (2, "A"), (3, "B")],
    # 3-4-4-3: Wk1 A(Mon-Wed) B(Thu-Sun); Wk2 A(Mon-Thu) B(Fri-Sun).
    "3-4-4-3": [(3, "A"), (4, "B"), (4, "A"), (3, "B")],
}

DEFAULT_LABELS = {"A": "Parent A", "B": "Parent B"}


def parse_date(s):
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def build_rotation(schedule, start, days, first="A"):
    """Return {date: parent} for `days` days from `start`."""
    pat = list(SCHEDULES[schedule])
    if first == "B":
        pat = [(n, "p" if p == "A" else "A") for (n, p) in
               [(n, p) for (n, p) in pat]]
        pat = [(n, "B" if p == "p" else "A") for (n, p) in pat]
    assign = {}
    i, used = 0, 0
    cur = start
    while used < days:
        block_n, parent = pat[i % len(pat)]
        for k in range(block_n):
            if used >= days:
                break
            assign[cur] = parent
            cur += timedelta(days=1)
            used += 1
        i += 1
    return assign


def exchange_days(assign):
    """Dates where custody flips (exchange happens that morning)."""
    out = []
    days = sorted(assign)
    for prev, curd in zip(days, days[1:]):
        if assign[prev] != assign[curd]:
            out.append(curd)
    return out


def cmd_plan(a):
    start = parse_date(a.start)
    assign = build_rotation(a.schedule, start, a.days, a.first)
    labels = {"A": a.label_a, "B": a.label_b}
    lines = []
    cur = None
    for d in sorted(assign):
        p = assign[d]
        if p != cur:
            wd = d.strftime("%a")
            lines.append(f"{d.isoformat()} {wd:<3} -> {labels[p]}")
            cur = p
        if a.daily:
            print(f"{d.isoformat()} {d.strftime('%a'):<3} {labels[assign[d]]}")
    if not a.daily:
        print(f"Rotation: {a.schedule} starting {start} (first block: {labels[a.first]})")
        for ln in lines:
            print(ln)
    n_a = sum(1 for v in assign.values() if v == "A")
    n_b = len(assign) - n_a
    ex = exchange_days(assign)
    print(f"\nOvernights: {labels['A']}={n_a} ({100*n_a/len(assign):.0f}%)  "
          f"{labels['B']}={n_b} ({100*n_b/len(assign):.0f}%)  "
          f"period={len(assign)}d  exchanges={len(ex)} (~{len(ex)/(len(assign)/30):.1f}/month)")
    if a.ics:
        write_ics(a.ics, assign, labels, a.exchange_time)
        print(f"ICS written: {a.ics}")
    if a.json:
        print(json.dumps({
            "schedule": a.schedule, "start": a.start, "days": len(assign),
            "overnights": {"A": n_a, "B": n_b},
            "exchange_dates": [d.isoformat() for d in ex],
            "assignment": {d.isoformat(): p for d, p in sorted(assign.items())},
        }, indent=2))


def write_ics(path, assign, labels, exchange_time):
    hh, mm = exchange_time.split(":")
    with open(path, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//co-parenting-calendar//EN\r\n")
        stamp = date.today().strftime("%Y%m%dT000000Z")
        # All-day custody blocks per parent run
        run_start = None
        run_parent = None
        for d in sorted(assign):
            p = assign[d]
            if p != run_parent and run_start is not None:
                f.write(vevent_allday(run_start, d - timedelta(days=1), run_parent, labels))
            if p != run_parent:
                run_start, run_parent = d, p
        if run_start:
            f.write(vevent_allday(run_start, max(assign) , run_parent, labels))
        # Exchange events
        for d in exchange_days(assign):
            f.write(vevent_exchange(d, hh, mm, assign[d], labels))
        f.write("END:VCALENDAR\r\n")


def vevent_allday(d1, d2, parent, labels):
    return ("BEGIN:VEVENT\r\nUID:{0}-{1}@coparent\r\nDTSTAMP:{2}\r\n"
            "DTSTART;VALUE=DATE:{0}\r\nDTEND;VALUE=DATE:{3}\r\n"
            "SUMMARY:With {4}\r\nTRANSP:TRANSPARENT\r\nEND:VEVENT\r\n").format(
        d1.strftime("%Y%m%d"), parent, date.today().strftime("%Y%m%dT000000Z"),
        (d2 + timedelta(days=1)).strftime("%Y%m%d"), labels[parent])


def vevent_exchange(d, hh, mm, to_parent, labels):
    return ("BEGIN:VEVENT\r\nUID:ex-{0}@coparent\r\nDTSTAMP:{1}\r\n"
            "DTSTART:{0}T{2}{3}00\r\nDTEND:{0}T{2}{3}45\r\n"
            "SUMMARY:Exchange -> {4}\r\nBEGIN:VALARM\r\nTRIGGER:-PT12H\r\n"
            "ACTION:DISPLAY\r\nDESCRIPTION:Pack for exchange tomorrow\r\n"
            "END:VALARM\r\nEND:VEVENT\r\n").format(
        d.strftime("%Y%m%d"), date.today().strftime("%Y%m%dT000000Z"), hh, mm,
        labels[to_parent])


# ─── Holidays ───
def easter(year):
    a = year % 19
    b, c = year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def nth_weekday(year, month, weekday, n):
    d = date(year, month, 1)
    count = 0
    while True:
        if d.weekday() == weekday:
            count += 1
            if count == n:
                return d
        d += timedelta(days=1)


def last_weekday(year, month, weekday):
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    while d.weekday() != weekday:
        d -= timedelta(days=1)
    return d


def holiday_list(year, birthday=None):
    e = easter(year)
    hl = [
        ("New Year's Day", date(year, 1, 1)),
        ("Mid-winter break (week of)", nth_weekday(year, 2, 0, 3)),
        ("Spring break (week of)", nth_weekday(year, 3, 0, 3)),
        ("Easter Sunday", e),
        ("Memorial Day", last_weekday(year, 5, 0)),
        ("Independence Day", date(year, 7, 4)),
        ("Labor Day", nth_weekday(year, 9, 0, 1)),
        ("Thanksgiving", nth_weekday(year, 11, 3, 4)),
        ("Christmas Eve", date(year, 12, 24)),
        ("Christmas Day", date(year, 12, 25)),
        ("New Year's Eve", date(year, 12, 31)),
    ]
    if birthday:
        hl.append(("Child's birthday", birthday))
    hl.sort(key=lambda x: x[1])
    return hl


def cmd_holidays(a):
    year = a.year
    birthday = parse_date(a.birthday).replace(year=year) if a.birthday else None
    hl = holiday_list(year, birthday)
    labels = {"A": a.label_a, "B": a.label_b}
    odd_priority = a.odd  # who has first pick in odd years
    fixed = {"Mother's Day": a.mother, "Father's Day": a.father}
    print(f"Holiday priority {year} ({'odd' if year % 2 else 'even'} year) — "
          f"first pick: {labels[odd_priority]}")
    toggle = odd_priority
    rows = []
    for name, d in hl:
        rows.append((name, d, labels[toggle]))
        toggle = "B" if toggle == "A" else "A"
    # Mother's/Father's Day rows
    md = nth_weekday(year, 5, 6, 2)
    fd = nth_weekday(year, 6, 6, 3)
    rows.append(("Mother's Day", md, labels[a.mother]))
    rows.append(("Father's Day", fd, labels[a.father]))
    for name, d, who in sorted(rows, key=lambda r: r[1]):
        print(f"{d.isoformat()} {d.strftime('%a'):<3} {name:<28} -> {who}")
    print("\nNote: define 'holiday starts 6pm prior day / ends 8am next day' "
          "wording in the parenting plan to kill edge disputes.")
    if a.json:
        print(json.dumps([{"date": d.isoformat(), "holiday": n, "parent": w}
                          for n, d, w in sorted(rows, key=lambda r: r[1])], indent=2))


def cmd_fairness(a):
    start, end = parse_date(a.start), parse_date(a.end)
    days = (end - start).days + 1
    assign = build_rotation(a.schedule, start, days, a.first)
    labels = {"A": a.label_a, "B": a.label_b}
    stat = {}
    for p in "AB":
        overnights = sum(1 for v in assign.values() if v == p)
        weekends = sum(1 for d, v in assign.items() if d.weekday() >= 5 and v == p)
        # longest gap without an overnight
        gap, longest, last_day = 0, 0, None
        for d in sorted(assign):
            if v_of(assign, d) == p:
                gap = 0
            else:
                gap += 1
                longest = max(longest, gap)
        stat[p] = {"overnights": overnights, "pct": round(100 * overnights / days, 1),
                   "weekend_days": weekends, "longest_gap_days": longest}
        stat[p]["verdict"] = ("<35% — below common shared-custody threshold "
                              "(many US states treat <35% as minority time)")
        if stat[p]["pct"] >= 35:
            stat[p]["verdict"] = ("shared-time band (>=35%)" if stat[p]["pct"] < 65
                                  else "majority-time band (>=65%)")
    for p in "AB":
        s = stat[p]
        print(f"{labels[p]}: {s['overnights']}/{days} overnights ({s['pct']}%), "
              f"weekend days {s['weekend_days']}, longest gap {s['longest_gap_days']}d "
              f"— {s['verdict']}")
    if a.json:
        print(json.dumps({"period_days": days, **{labels[k]: v for k, v in stat.items()}},
                         indent=2))


def v_of(assign, d):
    return assign.get(d)


def cmd_override(a):
    start, end = parse_date(a.start), parse_date(a.end)
    n = (end - start).days + 1
    print(f"Override: {start} .. {end} ({n}d) -> {a.parent.upper()}  reason: {a.reason}")
    print(f"Make-up doctrine: offer the other parent a block of equal length "
          f"({n}d) within 30 days, in writing, BEFORE agreeing the override.")
    print("Log entry (append to the co-parenting log):")
    print(f"  {date.today().isoformat()}: agreed {a.start}..{a.end} to "
          f"{a.parent.upper()} ({a.reason}); make-up {n}d owed to other parent.")
    if a.json:
        print(json.dumps({"from": a.start, "to": a.end, "days": n,
                          "parent": a.parent.upper(), "reason": a.reason,
                          "makeup_owed_days": n}, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan", help="dated rotation + stats + ICS")
    p.add_argument("--schedule", choices=sorted(SCHEDULES), default="2-2-3")
    p.add_argument("--start", required=True, help="YYYY-MM-DD (block boundary)")
    p.add_argument("--days", type=int, default=28)
    p.add_argument("--first", choices=["A", "B"], default="A")
    p.add_argument("--label-a", default=DEFAULT_LABELS["A"])
    p.add_argument("--label-b", default=DEFAULT_LABELS["B"])
    p.add_argument("--daily", action="store_true", help="print every day")
    p.add_argument("--ics", help="write .ics (blocks + exchange events)")
    p.add_argument("--exchange-time", default="18:00")
    p.set_defaults(fn=cmd_plan)

    h = sub.add_parser("holidays", help="holiday priority table for a year")
    h.add_argument("--year", type=int, required=True)
    h.add_argument("--odd", choices=["A", "B"], default="A",
                   help="who gets first pick in ODD years")
    h.add_argument("--mother", choices=["A", "B"], dest="mother", default="A")
    h.add_argument("--father", choices=["A", "B"], dest="father", default="B")
    h.add_argument("--birthday", help="YYYY-MM-DD (year ignored)")
    h.add_argument("--label-a", default=DEFAULT_LABELS["A"])
    h.add_argument("--label-b", default=DEFAULT_LABELS["B"])
    h.set_defaults(fn=cmd_holidays)

    f = sub.add_parser("fairness", help="overnight/weekend audit")
    f.add_argument("--schedule", choices=sorted(SCHEDULES), required=True)
    f.add_argument("--start", required=True)
    f.add_argument("--end", required=True)
    f.add_argument("--first", choices=["A", "B"], default="A")
    f.add_argument("--label-a", default=DEFAULT_LABELS["A"])
    f.add_argument("--label-b", default=DEFAULT_LABELS["B"])
    f.set_defaults(fn=cmd_fairness)

    o = sub.add_parser("override", help="patch + make-up suggestion")
    o.add_argument("--from", dest="start", required=True)
    o.add_argument("--to", dest="end", required=True)
    o.add_argument("--parent", choices=["A", "B"], required=True)
    o.add_argument("--reason", default="travel")
    o.set_defaults(fn=cmd_override)

    a = ap.parse_args()
    if getattr(a, "json", None):
        a.json = True
    a.fn(a)


if __name__ == "__main__":
    main()
