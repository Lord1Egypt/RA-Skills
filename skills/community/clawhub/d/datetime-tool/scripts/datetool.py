#!/usr/bin/env python3
"""DateTime Tool - Date and time utilities."""

import argparse
import datetime as dt
import time
import sys
from typing import Optional


def get_now(unix: bool = False, iso: bool = False) -> None:
    """Get current time."""
    now = dt.datetime.now()
    
    if unix:
        print(int(now.timestamp()))
    elif iso:
        print(now.isoformat())
    else:
        print(now.strftime("%Y-%m-%d %H:%M:%S"))


def convert_date(date_str: str, to_format: str = 'unix') -> None:
    """Convert date between formats."""
    # Try multiple input formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
    ]
    
    dt = None
    for fmt in formats:
        try:
            dt = dt.datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    
    # Try unix timestamp
    if dt is None:
        try:
            ts = int(date_str)
            dt = dt.datetime.fromtimestamp(ts)
        except:
            pass
    
    if dt is None:
        print(f"Error: Could not parse date: {date_str}", file=sys.stderr)
        return
    
    # Output in requested format
    if to_format == 'unix':
        print(int(dt.timestamp()))
    elif to_format == 'iso':
        print(dt.isoformat())
    elif to_format == 'date':
        print(dt.strftime("%Y-%m-%d"))
    elif to_format == 'time':
        print(dt.strftime("%H:%M:%S"))
    elif to_format == 'datetime':
        print(dt.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print(dt.strftime(to_format))


def format_date(date_str: str, fmt: str = "%Y-%m-%d") -> None:
    """Format a date string."""
    # Try parsing
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%dT%H:%M:%S",
    ]
    
    dt = None
    for f in formats:
        try:
            dt = dt.datetime.strptime(date_str, f)
            break
        except ValueError:
            continue
    
    if dt is None:
        # Try as unix
        try:
            ts = int(date_str)
            dt = dt.datetime.fromtimestamp(ts)
        except:
            print(f"Error: Could not parse: {date_str}", file=sys.stderr)
            return
    
    print(dt.strftime(fmt))


def add_time(date_str: str, value: int, unit: str) -> None:
    """Add time to a date."""
    # Parse date
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]
    dt = None
    for fmt in formats:
        try:
            dt = dt.datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    
    if dt is None:
        print(f"Error: Could not parse: {date_str}", file=sys.stderr)
        return
    
    # Add time
    if unit in ['day', 'days']:
        dt += dt.timedelta(days=value)
    elif unit in ['hour', 'hours']:
        dt += dt.timedelta(hours=value)
    elif unit in ['minute', 'minutes']:
        dt += dt.timedelta(minutes=value)
    elif unit in ['second', 'seconds']:
        dt += dt.timedelta(seconds=value)
    elif unit in ['week', 'weeks']:
        dt += dt.timedelta(weeks=value)
    elif unit in ['month', 'months']:
        # Approximate
        dt = dt + dt.timedelta(days=value * 30)
    elif unit in ['year', 'years']:
        dt = dt + dt.timedelta(days=value * 365)
    else:
        print(f"Error: Unknown unit: {unit}", file=sys.stderr)
        return
    
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))


def subtract_time(date_str: str, value: int, unit: str) -> None:
    """Subtract time from a date."""
    # Parse date
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]
    dt = None
    for fmt in formats:
        try:
            dt = dt.datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    
    if dt is None:
        print(f"Error: Could not parse: {date_str}", file=sys.stderr)
        return
    
    # Subtract time
    if unit in ['day', 'days']:
        dt -= dt.timedelta(days=value)
    elif unit in ['hour', 'hours']:
        dt -= dt.timedelta(hours=value)
    elif unit in ['minute', 'minutes']:
        dt -= dt.timedelta(minutes=value)
    elif unit in ['second', 'seconds']:
        dt -= dt.timedelta(seconds=value)
    elif unit in ['week', 'weeks']:
        dt -= dt.timedelta(weeks=value)
    else:
        print(f"Error: Unknown unit: {unit}", file=sys.stderr)
        return
    
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))


def countdown(target_str: str) -> None:
    """Countdown to a date."""
    # Parse target date
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]
    target = None
    for fmt in formats:
        try:
            target = dt.datetime.strptime(target_str, fmt)
            break
        except ValueError:
            continue
    
    if target is None:
        print(f"Error: Could not parse: {target_str}", file=sys.stderr)
        return
    
    now = dt.datetime.now()
    delta = target - now
    
    if delta.total_seconds() < 0:
        print(f"Date has passed: {target_str}")
        return
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"Countdown to {target_str}:")
    print(f"  {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
    
    # Also show in different units
    total_seconds = int(delta.total_seconds())
    print(f"  ({total_seconds} total seconds)")


def calculate_age(birthdate_str: str) -> None:
    """Calculate age from birthdate."""
    # Parse birthdate
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"]
    birthdate = None
    for fmt in formats:
        try:
            birthdate = dt.datetime.strptime(birthdate_str, fmt)
            break
        except ValueError:
            continue
    
    if birthdate is None:
        print(f"Error: Could not parse: {birthdate_str}", file=sys.stderr)
        return
    
    today = dt.datetime.now()
    age = today.year - birthdate.year
    
    # Adjust if birthday hasn't occurred this year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    
    print(f"Age: {age} years")
    
    # Also show in other units
    delta = today - birthdate
    print(f"Days since birth: {delta.days}")
    print(f"Weeks since birth: {delta.days // 7}")


def count_weekdays(start_str: str, end_str: str) -> None:
    """Count weekdays in a date range."""
    # Parse dates
    start = None
    end = None
    
    for fmt in ["%Y-%m-%d", "%Y/%m/%d"]:
        try:
            start = dt.datetime.strptime(start_str, fmt)
            break
        except ValueError:
            continue
    
    for fmt in ["%Y-%m-%d", "%Y/%m/%d"]:
        try:
            end = dt.datetime.strptime(end_str, fmt)
            break
        except ValueError:
            continue
    
    if start is None or end is None:
        print(f"Error: Could not parse dates", file=sys.stderr)
        return
    
    if start > end:
        start, end = end, start
    
    # Count weekdays
    weekdays = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # Monday=0, Friday=4
            weekdays += 1
        current += dt.timedelta(days=1)
    
    print(f"Weekdays from {start_str} to {end_str}: {weekdays}")


def parse_relative(relative_str: str) -> None:
    """Parse relative time like 'tomorrow', 'yesterday', 'next week'."""
    now = dt.datetime.now()
    
    parts = relative_str.lower().split()
    if len(parts) != 2:
        print(f"Error: Use format like 'tomorrow', 'yesterday', 'next week'", file=sys.stderr)
        return
    
    modifier, unit = parts
    
    if modifier == "tomorrow":
        result = now + dt.timedelta(days=1)
    elif modifier == "yesterday":
        result = now - dt.timedelta(days=1)
    elif modifier == "next":
        if unit == "week":
            result = now + dt.timedelta(weeks=1)
        elif unit == "month":
            result = now + dt.timedelta(days=30)
        elif unit == "year":
            result = now + dt.timedelta(days=365)
        else:
            print(f"Error: Unknown unit: {unit}", file=sys.stderr)
            return
    elif modifier == "last":
        if unit == "week":
            result = now - dt.timedelta(weeks=1)
        elif unit == "month":
            result = now - dt.timedelta(days=30)
        elif unit == "year":
            result = now - dt.timedelta(days=365)
        else:
            print(f"Error: Unknown unit: {unit}", file=sys.stderr)
            return
    else:
        print(f"Error: Unknown modifier: {modifier}", file=sys.stderr)
        return
    
    print(result.strftime("%Y-%m-%d %H:%M:%S"))


def main():
    parser = argparse.ArgumentParser(description='DateTime utility tool')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # now
    now_parser = subparsers.add_parser('now', help='Current time')
    now_parser.add_argument('--unix', action='store_true', help='Unix timestamp')
    now_parser.add_argument('--iso', action='store_true', help='ISO format')
    
    # convert
    convert_parser = subparsers.add_parser('convert', help='Convert date format')
    convert_parser.add_argument('date', help='Date string or timestamp')
    convert_parser.add_argument('--to', default='unix', help='Output format')
    
    # format
    format_parser = subparsers.add_parser('format', help='Format date')
    format_parser.add_argument('date', help='Date string')
    format_parser.add_argument('--format', '-f', default='%Y-%m-%d', help='Output format')
    
    # add
    add_parser = subparsers.add_parser('add', help='Add time')
    add_parser.add_argument('value', type=int, help='Value to add')
    add_parser.add_argument('unit', help='Unit (day, hour, minute, week, etc.)')
    add_parser.add_argument('date', nargs='?', help='Starting date (default: now)')
    
    # subtract
    sub_parser = subparsers.add_parser('subtract', help='Subtract time')
    sub_parser.add_argument('value', type=int, help='Value to subtract')
    sub_parser.add_argument('unit', help='Unit (day, hour, minute, week, etc.)')
    sub_parser.add_argument('date', nargs='?', help='Starting date')
    
    # countdown
    cd_parser = subparsers.add_parser('countdown', help='Countdown to date')
    cd_parser.add_argument('date', help='Target date')
    
    # age
    age_parser = subparsers.add_parser('age', help='Calculate age')
    age_parser.add_argument('birthdate', help='Birthdate')
    
    # weekdays
    wd_parser = subparsers.add_parser('weekdays', help='Count weekdays')
    wd_parser.add_argument('start', help='Start date')
    wd_parser.add_argument('end', help='End date')
    
    # relative
    rel_parser = subparsers.add_parser('relative', help='Parse relative time')
    rel_parser.add_argument('relative', help='Relative time (tomorrow, yesterday, next week)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\nExamples:")
        print("  datetime-tool now")
        print("  datetime-tool now --unix")
        print("  datetime-tool convert 2026-03-17 --to unix")
        print("  datetime-tool add 7 days")
        print("  datetime-tool countdown 2026-12-31")
        sys.exit(1)
    
    if args.command == 'now':
        get_now(args.unix, args.iso)
    elif args.command == 'convert':
        convert_date(args.date, args.to)
    elif args.command == 'format':
        format_date(args.date, args.format)
    elif args.command == 'add':
        date = args.date if args.date else dt.datetime.now().strftime("%Y-%m-%d")
        add_time(date, args.value, args.unit)
    elif args.command == 'subtract':
        date = args.date if args.date else dt.datetime.now().strftime("%Y-%m-%d")
        subtract_time(date, args.value, args.unit)
    elif args.command == 'countdown':
        countdown(args.date)
    elif args.command == 'age':
        calculate_age(args.birthdate)
    elif args.command == 'weekdays':
        count_weekdays(args.start, args.end)
    elif args.command == 'relative':
        parse_relative(args.relative)


if __name__ == '__main__':
    main()
