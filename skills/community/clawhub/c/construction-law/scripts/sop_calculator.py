#!/usr/bin/env python3
"""
Singapore SOP Act Payment Timeline Calculator (v2.8.1)
"""

import argparse
import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

try:
    from version import VERSION
except ImportError:
    VERSION = "2.6.0"

_HOLIDAY_JSON = Path(__file__).resolve().parent.parent / "data" / "sg_holidays.json"


def _load_gazetted_holidays_from_json():
    try:
        with open(_HOLIDAY_JSON, "r", encoding="utf-8") as f:
            raw = json.load(f)
        holidays = set()
        for year, value in raw.items():
            if year == "_meta":
                continue
            # Support both flat list format and structured {dates: [...]} format
            if isinstance(value, list):
                dates_list = value
            elif isinstance(value, dict) and 'dates' in value:
                dates_list = value['dates']
            else:
                continue
            for d_str in dates_list:
                holidays.add(datetime.strptime(d_str, "%Y-%m-%d").date())
        return holidays
    except FileNotFoundError:
        return None


_GAZETTED_HOLIDAYS = _load_gazetted_holidays_from_json() or {
    date(2025, 1, 1),  date(2025, 1, 29), date(2025, 1, 30),
    date(2025, 3, 31), date(2025, 4, 18), date(2025, 5, 1),
    date(2025, 5, 12), date(2025, 6, 7),  date(2025, 8, 9),
    date(2025, 10, 20), date(2025, 12, 25),
    date(2026, 1, 1),  date(2026, 2, 17), date(2026, 2, 18),
    date(2026, 3, 21), date(2026, 4, 3),  date(2026, 5, 1),
    date(2026, 5, 31), date(2026, 5, 27),
    date(2026, 8, 9),  date(2026, 11, 8),  date(2026, 12, 25),
    date(2027, 1, 1),  date(2027, 2, 6),  date(2027, 2, 7),
    date(2027, 3, 26), date(2027, 5, 1),  date(2027, 5, 11),
    date(2027, 5, 21), date(2027, 8, 9),  date(2027, 10, 28),
    date(2027, 12, 25),
}


def _add_sunday_in_lieu(holidays):
    result = set(holidays)
    for d in list(holidays):
        if d.weekday() == 6:
            candidate = d + timedelta(days=1)
            while candidate in result:
                candidate = candidate + timedelta(days=1)
            result.add(candidate)
    return result


SG_PUBLIC_HOLIDAYS = _add_sunday_in_lieu(_GAZETTED_HOLIDAYS)

# Coverage tracking: years with holiday data
_COVERED_YEARS = {d.year for d in _GAZETTED_HOLIDAYS}


def _check_year_coverage(target_date: date):
    """Raise ValueError if the target year has no holiday data.

    Called by all public date functions (is_sop_day, add_sop_days,
    sop_days_between) to prevent silent fallthrough on uncovered years.
    Without this guard, dates in years with no holiday data would be
    treated as having zero public holidays — the dangerous direction
    (understating protection, i.e. deadlines appear later than they are).
    """
    if target_date.year not in _COVERED_YEARS:
        raise ValueError(
            f"No holiday data for year {target_date.year}. "
            f"Covered years: {sorted(_COVERED_YEARS)}. "
            f"Update {_HOLIDAY_JSON.name} with gazetted holidays for {target_date.year} "
            f"before relying on SOP deadline calculations."
        )


def is_sop_day(d: date) -> bool:
    """Return True if *d* is not a gazetted public holiday.

    Saturdays and Sundays return True (they count as SOP days)
    unless the date is also a gazetted public holiday or an
    in-lieu day derived from a Sunday public holiday.

    Raises ValueError if the year has no holiday data — does not
    silently return False for uncovered years.

    Note: ad-hoc declared holidays (e.g. Polling Day) are only
    reflected if manually added to the holiday data.
    """
    _check_year_coverage(d)
    return d not in SG_PUBLIC_HOLIDAYS


def add_sop_days(start: date, n: int) -> date:
    """Add *n* SOP days to *start*, skipping public holidays.

    When *n* is 0, returns *start* unchanged — the caller is
    responsible for whether *start* itself is a working day.
    This matches the SOP Act convention where day-zero is the
    event date (e.g. date of service) and counting begins the
    next day.

    Raises ValueError if the start or result year has no holiday
    data, preventing silent fallthrough on uncovered years.
    """
    _check_year_coverage(start)
    if n == 0:
        return start
    cur = start
    remaining = n
    while remaining > 0:
        cur = cur + timedelta(days=1)
        # Check year coverage when we cross into a new year
        if cur.year != start.year:
            _check_year_coverage(cur)
        if cur not in SG_PUBLIC_HOLIDAYS:
            remaining -= 1
    return cur


def sop_days_between(a: date, b: date) -> int:
    """Count the number of SOP days between *a* and *b* (exclusive of *a*).

    Inverse of add_sop_days: sop_days_between(a, add_sop_days(a, n)) == n.

    Raises ValueError if any year in the range has no holiday data.
    """
    if b <= a:
        return 0
    _check_year_coverage(a)
    _check_year_coverage(b)
    cnt, cur = 0, a
    while cur < b:
        cur += timedelta(days=1)
        if cur not in SG_PUBLIC_HOLIDAYS:
            cnt += 1
    return cnt


def calc_timeline(claim_date_str, response_period=21, fmt="md", output=None):
    claim_date = datetime.strptime(claim_date_str, "%Y-%m-%d").date()

    # Verify holiday data covers the claim year
    _check_year_coverage(claim_date)

    response_deadline = add_sop_days(claim_date, response_period)
    dispute_period_end = add_sop_days(response_deadline, 7)
    # s.13(3)(a): 7 SOP days from entitlement (dispute_period_end), NOT including
    # the day entitlement arose. See H P Construction & Engineering Pte Ltd v
    # Mega Team Engineering Pte Ltd [2024] SGHC(A) 5. Locked by:
    # tests/test_sop_golden.py::test_determination_extended_is_7_sop_days_after_determination
    adjudication_app_deadline = add_sop_days(dispute_period_end, 7)
    adjudication_response_deadline = add_sop_days(adjudication_app_deadline, 7)
    determination_deadline = add_sop_days(adjudication_response_deadline, 7)
    determination_extended = add_sop_days(adjudication_response_deadline, 14)
    payment_due = add_sop_days(determination_deadline, 7)
    direct_payment_available = add_sop_days(payment_due, 1)
    timeline = [
        {"date": claim_date, "event": "Payment Claim served", "section": "s.10", "action": "Claimant", "critical": True, "note": "Must state claimed amount and be served on respondent. Triggers the SOP clock."},
        {"date": response_deadline, "event": "Payment Response deadline", "section": "s.11", "action": "Respondent", "critical": True, "note": f"Within {response_period} SOP days. FAILURE = smash-and-grab exposure."},
        {"date": dispute_period_end, "event": "Dispute settlement period ends / entitlement to adjudicate arises", "section": "s.12", "action": "Both parties", "critical": False, "note": "If unpaid or disputed, claimant may apply for adjudication from this point."},
        {"date": adjudication_app_deadline, "event": "Adjudication application deadline", "section": "s.13", "action": "Claimant", "critical": True, "note": "Within 7 SOP days of entitlement. MISS THIS = lose the right to adjudicate this claim cycle."},
        {"date": adjudication_response_deadline, "event": "Adjudication response deadline", "section": "s.15", "action": "Respondent", "critical": True, "note": "7 SOP days from receipt of application."},
        {"date": determination_deadline, "event": "Adjudicator's determination deadline", "section": "s.17(1)(b)", "action": "Adjudicator", "critical": True, "note": f"7 SOP days from adjudication response deadline. Extendable to {determination_extended.strftime('%d %b %Y')} (+7 days) with claimant's written consent under s.17(2)."},
        {"date": payment_due, "event": "Payment of adjudicated amount due", "section": "s.22(1)", "action": "Respondent", "critical": True, "note": "7 SOP days from receipt of determination. Temporarily binding — pay now, argue later."},
        {"date": direct_payment_available, "event": "Direct payment from principal available", "section": "s.23", "action": "Claimant", "critical": False, "note": "If respondent fails to pay the adjudicated amount, claimant may seek direct payment from principal."},
    ]
    for t in timeline:
        t["day"] = sop_days_between(claim_date, t["date"])
    return {
        "claim_date": claim_date,
        "response_period": response_period,
        "timeline": timeline,
        "determination_extended": determination_extended,
    }


def main():
    parser = argparse.ArgumentParser(description="Singapore SOP Act Payment Timeline Calculator (holiday-aware)")
    parser.add_argument("--claim-date", required=True, help="Payment claim date (YYYY-MM-DD)")
    parser.add_argument("--response-period", type=int, default=21, help="Payment response period in SOP days (default: 21)")
    parser.add_argument("--format", default="md", choices=["md", "csv"], help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    try:
        result = calc_timeline(args.claim_date, args.response_period, args.format, args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    timeline = result["timeline"]
    claim_date = result["claim_date"]
    determination_extended = result["determination_extended"]

    if args.format == "md":
        lines = [
            "# SOP Act Payment Timeline",
            "",
            f"**Payment Claim Date:** {claim_date.strftime('%d %B %Y')} ({claim_date.strftime('%A')})",
            f"**Payment Response Period:** {args.response_period} SOP days",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "> All deadlines are computed in **SOP days** — Singapore public holidays "
            "are excluded (SOP Act s.2 read with the Holidays Act 1998). "
            "Saturdays and Sundays are NOT excluded.",
            "",
            "> ⚠️ **Ad-hoc holidays** (e.g. Polling Day) are only reflected if manually "
            "added to the holiday data. If a Polling Day or other ad-hoc declared holiday "
            "falls within your timeline, verify the deadline manually.",
            "",
            "---",
            "",
            "## Timeline",
            "",
            "| Day | Date | Event | Section | Action By | Critical |",
            "|-----|------|-------|---------|-----------|----------|",
        ]
        for t in timeline:
            critical = "⚠️ YES" if t["critical"] else ""
            day_str = f"D+{t['day']}" if t['day'] > 0 else "D0"
            lines.append(
                f"| {day_str} | {t['date'].strftime('%d %b %Y')} ({t['date'].strftime('%a')}) "
                f"| {t['event']} | {t['section']} | {t['action']} | {critical} |"
            )
        lines.extend(["", "## Notes", ""])
        for t in timeline:
            lines.append(f"- **{t['event']}** ({t['section']}): {t['note']}")
        lines.extend([
            "",
            "## Key Warnings",
            "",
            "### ⚠️ Smash and Grab",
            "If NO payment response is served by the respondent (s.11), the "
            "respondent CANNOT raise withholding reasons in adjudication "
            "(s.15(3)). This is the 'smash and grab' exposure.",
            "",
            "### ⚠️ Time-Bar",
            "Adjudication application must be made within **7 SOP days** of entitlement arising. "
            "Missing this deadline = lose the right to adjudicate for this payment claim cycle.",
            "",
            "### ⚠️ Temporarily Binding",
            "An adjudication determination is **temporarily binding** — pay now, argue later. "
            "The adjudicated amount must be paid even if the respondent intends to challenge "
            "it in arbitration or court.",
            "",
            "---",
            f"*Generated by Construction Law Skill v{VERSION}*",
        ])
        output_text = "\n".join(lines)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_text)
            print(f"Timeline written to {args.output}")
        else:
            print(output_text)

    elif args.format == "csv":
        import csv
        out = open(args.output, 'w', newline='') if args.output else sys.stdout
        writer = csv.writer(out)
        writer.writerow(["# DISCLAIMER", "This is a workflow aid not legal advice. Verify edition amendments and governing law before use."])
        writer.writerow(["Payment Claim Date", claim_date.strftime('%Y-%m-%d')])
        writer.writerow(["Response Period (SOP days)", args.response_period])
        writer.writerow(["Note", "All periods exclude SG public holidays per SOP Act s.2"])
        writer.writerow([])
        writer.writerow(["Day", "Date", "Day of Week", "Event", "Section", "Action By", "Critical", "Notes"])
        for t in timeline:
            day_str = f"D+{t['day']}" if t['day'] > 0 else "D0"
            writer.writerow([day_str, t['date'].strftime('%Y-%m-%d'), t['date'].strftime('%A'), t['event'], t['section'], t['action'], "YES" if t['critical'] else "", t['note']])
        if args.output:
            out.close()
            print(f"CSV written to {args.output}")


if __name__ == "__main__":
    main()
