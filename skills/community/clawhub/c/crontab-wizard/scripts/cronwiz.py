#!/usr/bin/env python3
"""
cronwiz.py — Explain, generate, and validate crontab expressions.

Usage:
    python3 cronwiz.py explain "*/5 * * * *"
    python3 cronwiz.py generate --every 5m
    python3 cronwiz.py next "0 9 * * 1-5" --count 5
    python3 cronwiz.py validate "0 25 * * *"
"""

import argparse
import re
import sys
from datetime import datetime, timedelta


# Cron field definitions
FIELD_NAMES = ["minute", "hour", "day-of-month", "month", "day-of-week"]
FIELD_RANGES = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day-of-month": (1, 31),
    "month": (1, 12),
    "day-of-week": (0, 7),  # 0 and 7 both = Sunday
}

MONTH_NAMES = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

DOW_NAMES = {
    "sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6,
}

SPECIAL_SHORTCUTS = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *",
}


def normalize_expr(expr: str) -> str:
    """Expand special shortcuts."""
    lower = expr.strip().lower()
    return SPECIAL_SHORTCUTS.get(lower, expr.strip())


def validate_field(value: str, field_name: str) -> list:
    """Validate a single cron field, return list of errors."""
    errors = []
    lo, hi = FIELD_RANGES[field_name]

    # Replace names with numbers for month/dow
    v = value.lower()
    if field_name == "month":
        for name, num in MONTH_NAMES.items():
            v = v.replace(name, str(num))
    elif field_name == "day-of-week":
        for name, num in DOW_NAMES.items():
            v = v.replace(name, str(num))

    # Split by comma for lists
    parts = v.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            errors.append(f"{field_name}: empty value in list")
            continue

        # Handle step values: */N or range/N
        step = None
        if "/" in part:
            base, step_str = part.split("/", 1)
            try:
                step = int(step_str)
                if step <= 0:
                    errors.append(f"{field_name}: step must be positive, got {step}")
            except ValueError:
                errors.append(f"{field_name}: invalid step value '{step_str}'")
                continue
            part = base

        # Handle ranges: N-M
        if "-" in part and part != "*":
            range_parts = part.split("-", 1)
            try:
                r_lo = int(range_parts[0])
                r_hi = int(range_parts[1])
                if r_lo < lo or r_lo > hi:
                    errors.append(f"{field_name}: {r_lo} out of range ({lo}-{hi})")
                if r_hi < lo or r_hi > hi:
                    errors.append(f"{field_name}: {r_hi} out of range ({lo}-{hi})")
                if r_lo > r_hi:
                    errors.append(f"{field_name}: invalid range {r_lo}-{r_hi}")
            except ValueError:
                errors.append(f"{field_name}: invalid range '{part}'")
            continue

        # Handle wildcard
        if part == "*":
            continue

        # Handle single number
        try:
            num = int(part)
            if num < lo or num > hi:
                errors.append(f"{field_name}: {num} out of range ({lo}-{hi})")
        except ValueError:
            errors.append(f"{field_name}: invalid value '{part}'")

    return errors


def validate_expression(expr: str) -> list:
    """Validate a full cron expression. Returns list of error strings."""
    normalized = normalize_expr(expr)
    fields = normalized.split()

    if len(fields) != 5:
        return [f"Expected 5 fields, got {len(fields)}: '{normalized}'"]

    errors = []
    for i, (value, name) in enumerate(zip(fields, FIELD_NAMES)):
        errors.extend(validate_field(value, name))

    return errors


def explain_field(value: str, field_name: str) -> str:
    """Explain a single cron field in English."""
    if value == "*":
        return f"every {field_name}"

    # Step
    if "/" in value:
        base, step = value.split("/", 1)
        if base == "*":
            return f"every {step} {field_name}s"
        else:
            return f"every {step} {field_name}s starting from {base}"

    # Range
    if "-" in value:
        lo, hi = value.split("-", 1)
        # Named days
        if field_name == "day-of-week":
            days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            try:
                lo_name = days[int(lo)]
                hi_name = days[int(hi)]
                return f"{lo_name} through {hi_name}"
            except (ValueError, IndexError):
                pass
        return f"{field_name} {lo} through {hi}"

    # List
    if "," in value:
        return f"{field_name} {value}"

    # Single value
    if field_name == "day-of-week":
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        try:
            idx = int(value)
            if idx == 7:
                idx = 0
            return days[idx]
        except (ValueError, IndexError):
            pass

    if field_name == "month":
        months = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
        try:
            return months[int(value)]
        except (ValueError, IndexError):
            pass

    return f"at {field_name} {value}"


def explain_expression(expr: str) -> str:
    """Explain a full cron expression in plain English."""
    normalized = normalize_expr(expr)
    fields = normalized.split()

    if len(fields) != 5:
        return f"Invalid expression: expected 5 fields, got {len(fields)}"

    minute, hour, dom, month, dow = fields

    parts = []

    # Time description
    if minute == "*" and hour == "*":
        parts.append("Every minute")
    elif minute.startswith("*/"):
        parts.append(f"Every {minute.split('/')[1]} minutes")
    elif hour == "*":
        parts.append(f"At minute {minute} of every hour")
    elif hour.startswith("*/"):
        parts.append(f"At minute {minute}, every {hour.split('/')[1]} hours")
    else:
        h = hour.zfill(2) if hour.isdigit() else hour
        m = minute.zfill(2) if minute.isdigit() else minute
        parts.append(f"At {h}:{m}")

    # Day-of-month
    if dom != "*":
        parts.append(f"on day {dom} of the month")

    # Month
    if month != "*":
        parts.append(f"in {explain_field(month, 'month')}")

    # Day-of-week
    if dow != "*":
        parts.append(f"on {explain_field(dow, 'day-of-week')}")

    return ", ".join(parts)


def expand_field(value: str, lo: int, hi: int) -> set:
    """Expand a cron field into a set of integer values."""
    result = set()
    for part in value.split(","):
        step = 1
        if "/" in part:
            base, step_str = part.split("/", 1)
            step = int(step_str)
            part = base

        if part == "*":
            result.update(range(lo, hi + 1, step))
        elif "-" in part:
            r_lo, r_hi = part.split("-", 1)
            result.update(range(int(r_lo), int(r_hi) + 1, step))
        else:
            val = int(part)
            if step > 1:
                result.update(range(val, hi + 1, step))
            else:
                result.add(val)
    return result


def next_runs(expr: str, count: int, start: datetime = None) -> list:
    """Calculate the next N run times for a cron expression."""
    normalized = normalize_expr(expr)
    fields = normalized.split()
    if len(fields) != 5:
        return []

    minutes = expand_field(fields[0], 0, 59)
    hours = expand_field(fields[1], 0, 23)
    doms = expand_field(fields[2], 1, 31)
    months = expand_field(fields[3], 1, 12)
    dows = expand_field(fields[4], 0, 7)
    # Normalize dow 7 → 0
    if 7 in dows:
        dows.add(0)
        dows.discard(7)

    if start is None:
        start = datetime.now()

    # Advance by 1 minute to avoid matching current time
    current = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
    results = []
    max_iterations = 525960  # ~1 year of minutes

    for _ in range(max_iterations):
        if (current.month in months and
            current.day in doms and
            current.weekday() in _convert_dow(dows) and
            current.hour in hours and
            current.minute in minutes):
            results.append(current)
            if len(results) >= count:
                break
        current += timedelta(minutes=1)

    return results


def _convert_dow(cron_dows: set) -> set:
    """Convert cron day-of-week (0=Sun) to Python weekday() (0=Mon)."""
    mapping = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
    return {mapping.get(d, d) for d in cron_dows if d in mapping}


def generate_expression(every: str = None, at: str = None, on: str = None) -> str:
    """Generate a cron expression from human-friendly options."""
    minute = "*"
    hour = "*"
    dom = "*"
    month = "*"
    dow = "*"

    if every:
        every = every.lower().strip()
        if every.endswith("m") or every.endswith("min"):
            n = re.search(r"(\d+)", every)
            if n:
                minute = f"*/{n.group(1)}"
        elif every.endswith("h") or every.endswith("hr"):
            n = re.search(r"(\d+)", every)
            if n:
                minute = "0"
                hour = f"*/{n.group(1)}"
        elif every == "day" or every == "daily":
            minute = "0"
            hour = "0"
        elif every == "week" or every == "weekly":
            minute = "0"
            hour = "0"
            dow = "1"  # Monday
        elif every == "month" or every == "monthly":
            minute = "0"
            hour = "0"
            dom = "1"

    if at:
        parts = at.split(":")
        hour = parts[0]
        minute = parts[1] if len(parts) > 1 else "0"

    if on:
        on = on.lower()
        day_map = {"mon": "1", "tue": "2", "wed": "3", "thu": "4",
                   "fri": "5", "sat": "6", "sun": "0",
                   "monday": "1", "tuesday": "2", "wednesday": "3",
                   "thursday": "4", "friday": "5", "saturday": "6",
                   "sunday": "0", "weekdays": "1-5", "weekends": "0,6"}
        if on in day_map:
            dow = day_map[on]

    return f"{minute} {hour} {dom} {month} {dow}"


def main():
    parser = argparse.ArgumentParser(
        description="Crontab expression wizard — explain, generate, validate, and preview cron schedules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s explain "*/5 * * * *"
  %(prog)s explain "@daily"
  %(prog)s validate "0 25 * * *"
  %(prog)s next "0 9 * * 1-5" --count 10
  %(prog)s generate --every 5m
  %(prog)s generate --every daily --at 09:00
  %(prog)s generate --every week --at 14:30 --on friday
""",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # explain
    p_explain = subparsers.add_parser("explain", help="Explain a cron expression in plain English")
    p_explain.add_argument("expression", help="Cron expression (5 fields or shortcut like @daily)")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate a cron expression")
    p_validate.add_argument("expression", help="Cron expression to validate")

    # next
    p_next = subparsers.add_parser("next", help="Show next N run times")
    p_next.add_argument("expression", help="Cron expression")
    p_next.add_argument("--count", "-n", type=int, default=5, help="Number of runs to show (default: 5)")

    # generate
    p_gen = subparsers.add_parser("generate", help="Generate a cron expression from options")
    p_gen.add_argument("--every", help="Interval: 5m, 2h, daily, weekly, monthly")
    p_gen.add_argument("--at", help="Time: HH:MM (e.g., 09:00)")
    p_gen.add_argument("--on", help="Day: mon, tue, ..., weekdays, weekends")

    args = parser.parse_args()

    if args.command == "explain":
        expr = args.expression
        errors = validate_expression(expr)
        if errors:
            print(f"Warning: expression may have issues:")
            for e in errors:
                print(f"  - {e}")
            print()
        explanation = explain_expression(expr)
        normalized = normalize_expr(expr)
        print(f"Expression: {normalized}")
        print(f"Meaning:    {explanation}")

    elif args.command == "validate":
        expr = args.expression
        errors = validate_expression(expr)
        normalized = normalize_expr(expr)
        if errors:
            print(f"INVALID: {normalized}")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print(f"VALID: {normalized}")
            print(f"  → {explain_expression(expr)}")

    elif args.command == "next":
        expr = args.expression
        errors = validate_expression(expr)
        if errors:
            print("Expression has errors:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        runs = next_runs(expr, args.count)
        normalized = normalize_expr(expr)
        print(f"Expression: {normalized}")
        print(f"Meaning:    {explain_expression(expr)}")
        print(f"\nNext {args.count} runs:")
        for i, run in enumerate(runs, 1):
            print(f"  {i}. {run.strftime('%Y-%m-%d %H:%M (%A)')}")

    elif args.command == "generate":
        expr = generate_expression(args.every, args.at, args.on)
        print(f"Expression: {expr}")
        print(f"Meaning:    {explain_expression(expr)}")


if __name__ == "__main__":
    main()
