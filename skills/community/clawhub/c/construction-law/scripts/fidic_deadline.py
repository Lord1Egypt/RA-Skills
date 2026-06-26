#!/usr/bin/env python3
"""
FIDIC Deadline Calculator — Seat-Aware

Computes contractual deadlines based on the seat country's public holidays.
Supports multiple day-counting modes:
  - calendar: Pure calendar days (FIDIC 2017 default — Sub-Clause 1.1.19)
  - exclude_ph: Calendar days excluding public holidays of the seat country
  - working: Excludes weekends AND public holidays (for contracts that define "working day")

Singapore is supported out of the box with gazette-verified holiday data.
For any other jurisdiction, supply your own holiday file with --holidays-file.

Usage:
    python3 fidic_deadline.py --seat SG --trigger 2026-05-15 --period 28
    python3 fidic_deadline.py --seat SG --trigger 2026-05-15 --period 28 --mode exclude_ph
    python3 fidic_deadline.py --seat AE --trigger 2026-03-18 --period 28 --mode exclude_ph --holidays-file my_ae_holidays.json
    python3 fidic_deadline.py --list-seats
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    from version import VERSION
except ImportError:
    VERSION = "2.11.0"

HOLIDAYS_DIR = Path(__file__).resolve().parent.parent / "data" / "holidays"
SG_HOLIDAYS_JSON = Path(__file__).resolve().parent.parent / "data" / "sg_holidays.json"

VISIBLE_DISCLAIMER = "> \u26a0\ufe0f **Disclaimer:** This is a workflow aid, not legal advice. Verify the contract's definition of 'day', the seat country, and applicable holidays before reliance."

# Only Singapore is bundled and maintained
BUNDLED_SEATS = {'SG'}


def list_available_seats(holidays_file=None):
    """List available country holiday files (bundled + user-supplied)."""
    seats = []
    # Bundled SG
    if HOLIDAYS_DIR.exists():
        for f in sorted(HOLIDAYS_DIR.glob("*.json")):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
                meta = data.get('_meta', {})
                seats.append({
                    'iso': meta.get('iso', f.stem),
                    'country': meta.get('country', f.stem),
                    'years': [k for k in data.keys() if k != '_meta'],
                    'notes': meta.get('notes', ''),
                    'bundled': True
                })
            except (json.JSONDecodeError, OSError):
                continue
    # User-supplied file
    if holidays_file:
        try:
            with open(holidays_file, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            meta = data.get('_meta', {})
            seats.append({
                'iso': meta.get('iso', Path(holidays_file).stem),
                'country': meta.get('country', Path(holidays_file).stem),
                'years': [k for k in data.keys() if k != '_meta'],
                'notes': meta.get('notes', '') + ' [user-supplied]',
                'bundled': False
            })
        except (json.JSONDecodeError, OSError):
            pass
    return seats


def load_holidays_from_file(filepath, year):
    """Load public holidays from a specific JSON file for a given year.

    Returns a set of date objects.
    Raises ValueError if year not found.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    year_str = str(year)
    if year_str not in data:
        available_years = [k for k in data.keys() if k != '_meta']
        raise ValueError(
            f"No holiday data for year {year} in {filepath}. "
            f"Available years: {', '.join(available_years)}."
        )

    year_data = data[year_str]
    # Support both flat list and structured {dates: [...]} format
    if isinstance(year_data, list):
        dates_list = year_data
    elif isinstance(year_data, dict) and 'dates' in year_data:
        dates_list = year_data['dates']
    else:
        raise ValueError(f"Invalid format for year {year} in {filepath}")

    return {datetime.strptime(d, "%Y-%m-%d").date() for d in dates_list}


def load_holidays(seat_iso, year, holidays_file=None):
    """Load public holidays for a given country and year.

    For SG: uses bundled gazette-verified data.
    For other seats: requires holidays_file to be supplied.

    Returns a set of date objects.
    Raises ValueError if country or year not found.
    """
    seat_iso = seat_iso.upper()

    if seat_iso in BUNDLED_SEATS:
        # Use bundled data
        holiday_file = HOLIDAYS_DIR / f"{seat_iso}.json"
        if not holiday_file.exists():
            # Fallback: SG can also be loaded from sg_holidays.json
            if seat_iso == "SG" and SG_HOLIDAYS_JSON.exists():
                holiday_file = SG_HOLIDAYS_JSON
            else:
                raise ValueError(
                    f"Bundled holiday data for '{seat_iso}' not found. "
                    f"Expected at: {HOLIDAYS_DIR / f'{seat_iso}.json'}"
                )
        return load_holidays_from_file(str(holiday_file), year)

    # Non-bundled seat: require user-supplied file
    if not holidays_file:
        raise ValueError(
            f"No bundled holiday data for seat '{seat_iso.lower()}'. "
            f"This tool only ships verified data for Singapore. "
            f"For other jurisdictions, supply your own holiday list with --holidays-file. "
            f"Format: see docs/holiday-file-format.md. "
            f"Source recommendation: your jurisdiction's official gazette or ministry of manpower equivalent."
        )

    return load_holidays_from_file(holidays_file, year)


def get_weekend_days(seat_iso, holidays_file=None):
    """Get weekend days for a country. Returns set of weekday numbers (0=Mon, 6=Sun)."""
    seat_iso = seat_iso.upper()

    # Try to read from the holiday file metadata
    filepath = None
    if seat_iso in BUNDLED_SEATS:
        candidate = HOLIDAYS_DIR / f"{seat_iso}.json"
        if candidate.exists():
            filepath = str(candidate)
    elif holidays_file:
        filepath = holidays_file

    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            meta = data.get('_meta', {})
            weekend = meta.get('weekend', ['Sat', 'Sun'])
        except (json.JSONDecodeError, OSError):
            weekend = ['Sat', 'Sun']
    else:
        weekend = ['Sat', 'Sun']

    day_map = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
    return {day_map[d] for d in weekend}


def get_in_lieu_holidays(seat_iso, holidays, year, mode='exclude_ph', holidays_file=None):
    """Derive in-lieu holidays based on country rules.

    In 'working' mode, weekends are already excluded, so a PH falling on a
    weekend day does NOT generate an in-lieu weekday — it's already skipped.
    In-lieu rules only apply in 'exclude_ph' mode where weekends count but PHs don't.

    Currently supports:
    - SG: Sunday PH -> Monday in-lieu (Holidays Act 1998 s.4(2)) — always applies
    - User-supplied files: reads in_lieu_rule from _meta and applies accordingly
    """
    seat_iso = seat_iso.upper()

    # Determine which file to read
    filepath = None
    if seat_iso in BUNDLED_SEATS:
        candidate = HOLIDAYS_DIR / f"{seat_iso}.json"
        if candidate.exists():
            filepath = str(candidate)
    elif holidays_file:
        filepath = holidays_file

    if not filepath:
        return set()

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return set()

    rule = data.get('_meta', {}).get('in_lieu_rule', 'none')
    weekend_days = get_weekend_days(seat_iso, holidays_file)
    in_lieu = set()

    if rule == 'auto_sunday_to_monday':
        # Singapore: Sunday PH -> Monday in-lieu (statutory, always applies)
        for h in holidays:
            if h.weekday() == 6:  # Sunday
                monday = h + timedelta(days=1)
                in_lieu.add(monday)

    elif rule in ('rest_day_replacement', 'substitute_next_working_day'):
        # PH on weekend -> next working day
        # Only applies in exclude_ph mode. In working mode, weekends are
        # already excluded so no replacement is needed.
        if mode == 'working':
            return set()
        for h in holidays:
            if h.weekday() in weekend_days:
                candidate = h + timedelta(days=1)
                while candidate.weekday() in weekend_days or candidate in holidays:
                    candidate += timedelta(days=1)
                in_lieu.add(candidate)

    return in_lieu


def compute_deadline(trigger_date, period, seat_iso, mode='calendar', holidays_file=None):
    """Compute a contractual deadline.

    Args:
        trigger_date: The date the clock starts (e.g. awareness of event)
        period: Number of days in the notice period
        seat_iso: ISO country code for the seat
        mode: 'calendar' | 'exclude_ph' | 'working'
        holidays_file: Path to user-supplied holiday JSON (required for non-SG seats)

    Returns:
        dict with deadline date, holidays skipped, and computation trace
    """
    seat_iso = seat_iso.upper()

    # Determine verification level
    if seat_iso in BUNDLED_SEATS:
        verification_note = 'Singapore holidays verified against MOM gazette (skill-maintained).'
    else:
        verification_note = f'User-supplied holiday data for {seat_iso}. Verification is your responsibility.'

    if mode == 'calendar':
        # Pure calendar days — FIDIC 2017 default
        deadline = trigger_date + timedelta(days=period)
        return {
            'trigger': trigger_date,
            'period': period,
            'mode': mode,
            'seat': seat_iso,
            'deadline': deadline,
            'holidays_skipped': [],
            'weekends_skipped': [],
            'verification': verification_note,
            'note': 'FIDIC 2017 Sub-Clause 1.1.19: "day" means calendar day. No holidays excluded unless Particular Conditions amend this.'
        }

    # For exclude_ph and working modes, we need holiday data
    # This will raise ValueError for non-SG seats without holidays_file
    # Collect holidays for all years the period might span
    years_needed = set()
    # Estimate: period + buffer for holidays/weekends
    estimate_end = trigger_date + timedelta(days=period * 2)
    for y in range(trigger_date.year, estimate_end.year + 1):
        years_needed.add(y)

    all_holidays = set()
    first_error = None
    loaded_any_year = False
    for y in years_needed:
        try:
            year_holidays = load_holidays(seat_iso, y, holidays_file)
            loaded_any_year = True
            all_holidays.update(year_holidays)
            # Add in-lieu days
            in_lieu = get_in_lieu_holidays(seat_iso, year_holidays, y, mode, holidays_file)
            all_holidays.update(in_lieu)
        except ValueError as e:
            if first_error is None:
                first_error = e
            # keep checking later years in case the first estimated year is missing but a later one exists
            continue

    if not loaded_any_year and first_error is not None:
        raise first_error

    weekend_days = get_weekend_days(seat_iso, holidays_file) if mode == 'working' else set()

    # Count days
    current = trigger_date
    days_counted = 0
    holidays_skipped = []
    weekends_skipped = []

    while days_counted < period:
        current += timedelta(days=1)

        if mode == 'working' and current.weekday() in weekend_days:
            weekends_skipped.append(current)
            continue

        if current in all_holidays:
            holidays_skipped.append(current)
            continue

        days_counted += 1

    return {
        'trigger': trigger_date,
        'period': period,
        'mode': mode,
        'seat': seat_iso,
        'deadline': current,
        'holidays_skipped': holidays_skipped,
        'weekends_skipped': weekends_skipped,
        'verification': verification_note,
        'note': f"{'Excludes PHs only' if mode == 'exclude_ph' else 'Excludes weekends + PHs'} for {seat_iso}. Verify contract definition of 'day'."
    }


def format_result(result, fmt='text'):
    """Format the deadline computation result."""
    if fmt == 'md':
        lines = [VISIBLE_DISCLAIMER, ""]
        lines.append("# Contractual Deadline Computation")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Trigger date | {result['trigger'].strftime('%d %b %Y (%A)')} |")
        lines.append(f"| Period | {result['period']} days |")
        lines.append(f"| Mode | {result['mode']} |")
        lines.append(f"| Seat country | {result['seat']} |")
        lines.append(f"| **Deadline** | **{result['deadline'].strftime('%d %b %Y (%A)')}** |")
        lines.append(f"| Calendar days elapsed | {(result['deadline'] - result['trigger']).days} |")
        lines.append("")

        if result['holidays_skipped']:
            lines.append(f"### Public holidays skipped ({len(result['holidays_skipped'])})")
            for h in result['holidays_skipped']:
                lines.append(f"- {h.strftime('%d %b %Y (%A)')}")
            lines.append("")

        if result['weekends_skipped']:
            lines.append(f"### Weekends skipped ({len(result['weekends_skipped'])})")
            lines.append(f"- {len(result['weekends_skipped'])} weekend days excluded")
            lines.append("")

        lines.append(f"> **Note:** {result['note']}")
        lines.append("")
        if result.get('verification'):
            lines.append(f"> \U0001f6e1\ufe0f **Verification:** {result['verification']}")
            lines.append("")
        lines.append("> This is a workflow and analysis aid only. It does not constitute legal advice.")
        return "\n".join(lines)

    else:
        # Plain text
        lines = []
        lines.append("FIDIC Deadline Computation")
        lines.append("=" * 40)
        lines.append(f"Trigger:    {result['trigger'].strftime('%d %b %Y (%A)')}")
        lines.append(f"Period:     {result['period']} days ({result['mode']})")
        lines.append(f"Seat:       {result['seat']}")
        lines.append(f"Deadline:   {result['deadline'].strftime('%d %b %Y (%A)')}")
        lines.append(f"Calendar:   {(result['deadline'] - result['trigger']).days} calendar days elapsed")

        if result['holidays_skipped']:
            lines.append(f"\nHolidays skipped ({len(result['holidays_skipped'])}):")
            for h in result['holidays_skipped']:
                lines.append(f"  - {h.strftime('%d %b %Y (%A)')}")

        if result['weekends_skipped']:
            lines.append(f"\nWeekends skipped: {len(result['weekends_skipped'])} days")

        lines.append(f"\nNote: {result['note']}")
        if result.get('verification'):
            lines.append(f"Verification: {result['verification']}")
        lines.append("\nDisclaimer: This is a workflow aid, not legal advice.")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="FIDIC Deadline Calculator \u2014 compute contractual deadlines based on seat country holidays",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Day-counting modes:
  calendar    Pure calendar days (FIDIC 2017 default \u2014 Sub-Clause 1.1.19)
  exclude_ph  Calendar days excluding public holidays of the seat country
  working     Excludes weekends AND public holidays (for contracts defining "working day")

Singapore is supported out of the box. For other jurisdictions, supply --holidays-file.

Examples:
  %(prog)s --seat SG --trigger 2026-05-15 --period 28
  %(prog)s --seat SG --trigger 2026-05-15 --period 28 --mode exclude_ph
  %(prog)s --seat AE --trigger 2026-03-18 --period 28 --mode exclude_ph --holidays-file ae_holidays.json
  %(prog)s --list-seats
"""
    )
    parser.add_argument("--seat", help="ISO country code for the seat (e.g. SG, AE, MY, GB)")
    parser.add_argument("--trigger", help="Trigger date (YYYY-MM-DD) \u2014 when the clock starts")
    parser.add_argument("--period", type=int, help="Number of days in the notice/deadline period")
    parser.add_argument("--mode", choices=['calendar', 'exclude_ph', 'working'], default='calendar',
                        help="Day-counting mode (default: calendar)")
    parser.add_argument("--holidays-file", help="Path to user-supplied holiday JSON file (required for non-SG seats in exclude_ph/working modes)")
    parser.add_argument("--format", choices=['text', 'md'], default='text',
                        help="Output format (default: text)")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--list-seats", action='store_true', help="List available seat countries")
    parser.add_argument("--version", action='version', version=f"fidic_deadline v{VERSION}")

    args = parser.parse_args()

    if args.list_seats:
        seats = list_available_seats(args.holidays_file)
        if not seats:
            print("No country holiday files found.")
            print(f"Bundled: SG (Singapore) in {HOLIDAYS_DIR}")
            print("For other jurisdictions, supply --holidays-file <path>")
            sys.exit(1)
        print("Available seat countries:")
        print(f"{'ISO':<6} {'Country':<35} {'Years':<20} {'Source':<12} Notes")
        print("-" * 100)
        for s in seats:
            years_str = ", ".join(s['years'][:5])
            source = "bundled" if s.get('bundled') else "user-file"
            notes_short = s['notes'][:40] + "..." if len(s['notes']) > 40 else s['notes']
            print(f"{s['iso']:<6} {s['country']:<35} {years_str:<20} {source:<12} {notes_short}")
        sys.exit(0)

    if not args.seat or not args.trigger or not args.period:
        parser.error("--seat, --trigger, and --period are required (or use --list-seats)")

    try:
        trigger = datetime.strptime(args.trigger, "%Y-%m-%d").date()
    except ValueError:
        parser.error(f"Invalid date format: {args.trigger}. Use YYYY-MM-DD.")

    try:
        result = compute_deadline(trigger, args.period, args.seat, args.mode, args.holidays_file)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    output = format_result(result, args.format)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
