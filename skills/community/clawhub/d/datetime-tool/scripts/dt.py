#!/usr/bin/env python3
"""DateTime Tool - Date and time utilities."""

import argparse
import calendar
import datetime
import sys
from typing import Optional


def get_now(unix: bool = False, iso: bool = False, utc: bool = False) -> str:
    """Get current datetime."""
    if utc:
        dt = datetime.datetime.now(datetime.timezone.utc)
    else:
        dt = datetime.datetime.now()
    
    if unix:
        return str(int(dt.timestamp()))
    if iso:
        return dt.isoformat()
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def convert_time(value: str) -> str:
    """Convert timestamp or date string."""
    # Try Unix timestamp
    try:
        ts = int(value)
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass
    
    # Try ISO format
    try:
        dt = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass
    
    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    
    return f"Could not parse: {value}"


def format_time(value: str, fmt: str) -> str:
    """Format a date string."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%b %d %Y",
    ]
    
    dt = None
    for f in formats:
        try:
            dt = datetime.datetime.strptime(value, f)
            break
        except ValueError:
            continue
    
    if not dt:
        return f"Could not parse: {value}"
    
    return dt.strftime(fmt)


def add_time(value: str, amount: int, unit: str) -> str:
    """Add time to a date."""
    # Parse the input date
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    
    dt = None
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(value, fmt)
            break
        except ValueError:
            continue
    
    if not dt:
        # Use today
        dt = datetime.datetime.now()
    
    # Add time
    delta = None
    unit_lower = unit.lower().rstrip('s')  # Remove plural
    
    if unit_lower in ['day', 'days']:
        delta = datetime.timedelta(days=amount)
    elif unit_lower in ['hour', 'hours']:
        delta = datetime.timedelta(hours=amount)
    elif unit_lower in ['minute', 'minutes']:
        delta = datetime.timedelta(minutes=amount)
    elif unit_lower in ['week', 'weeks']:
        delta = datetime.timedelta(weeks=amount)
    elif unit_lower in ['month', 'months']:
        # Approximate month as 30 days
        delta = datetime.timedelta(days=amount * 30)
    elif unit_lower in ['year', 'years']:
        # Approximate year as 365 days
        delta = datetime.timedelta(days=amount * 365)
    
    if delta:
        new_dt = dt + delta
        return new_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    return f"Unknown unit: {unit}"


def timezone_time(tz: str, time_str: Optional[str] = None) -> str:
    """Show time in a timezone."""
    try:
        import pytz
    except ImportError:
        # Simple fallback without pytz
        return f"Timezone: {tz}\n(pytz not installed)"
    
    try:
        timezone = pytz.timezone(tz)
        
        if time_str:
            # Parse the given time
            dt = datetime.datetime.strptime(time_str, "%H:%M")
            dt = dt.replace(year=datetime.datetime.now().year, 
                          month=datetime.datetime.now().month,
                          day=datetime.datetime.now().day)
            dt = timezone.localize(dt)
        else:
            dt = datetime.datetime.now(timezone)
        
        return f"Time in {tz}: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Error: {e}"


def relative_time(value: str) -> str:
    """Show relative time."""
    # Parse input
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
    
    dt = None
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(value, fmt)
            break
        except ValueError:
            continue
    
    if not dt:
        # Try as timestamp
        try:
            dt = datetime.datetime.fromtimestamp(int(value))
        except:
            return f"Could not parse: {value}"
    
    now = datetime.datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 0:
        return f"In {format_duration(-seconds)}"
    elif seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours ago"
    else:
        return f"{int(seconds / 86400)} days ago"


def format_duration(seconds: float) -> str:
    """Format duration."""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    else:
        return f"{int(seconds / 86400)} days"


def show_calendar(year: int, month: int) -> str:
    """Show month calendar."""
    cal = calendar.month(year, month)
    return cal


def main():
    parser = argparse.ArgumentParser(description='DateTime tool')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Now
    now_parser = subparsers.add_parser('now', help='Current time')
    now_parser.add_argument('--unix', action='store_true', help='Unix timestamp')
    now_parser.add_argument('--iso', action='store_true', help='ISO format')
    now_parser.add_argument('--utc', action='store_true', help='UTC time')
    
    # Convert
    convert_parser = subparsers.add_parser('convert', help='Convert timestamp/date')
    convert_parser.add_argument('value', help='Timestamp or date string')
    
    # Format
    format_parser = subparsers.add_parser('format', help='Format date')
    format_parser.add_argument('value', help='Date string')
    format_parser.add_argument('--format', '-f', default='%Y-%m-%d %H:%M:%S', help='Output format')
    
    # Add
    add_parser = subparsers.add_parser('add', help='Add time')
    add_parser.add_argument('amount', type=int, help='Amount to add')
    add_parser.add_argument('unit', help='Unit (days, weeks, months, etc.)')
    add_parser.add_argument('--date', help='Starting date (default: now)')
    
    # Sub
    sub_parser = subparsers.add_parser('sub', help='Subtract time')
    sub_parser.add_argument('amount', type=int, help='Amount to subtract')
    sub_parser.add_argument('unit', help='Unit (days, weeks, months, etc.)')
    sub_parser.add_argument('--date', help='Starting date (default: now)')
    
    # Timezone
    tz_parser = subparsers.add_parser('tz', help='Time in timezone')
    tz_parser.add_argument('timezone', help='Timezone (e.g., America/New_York)')
    tz_parser.add_argument('--time', help='Time (HH:MM)')
    
    # Relative
    relative_parser = subparsers.add_parser('relative', help='Relative time')
    relative_parser.add_argument('value', help='Date/timestamp')
    
    # Calendar
    cal_parser = subparsers.add_parser('calendar', help='Show calendar')
    cal_parser.add_argument('year', type=int, help='Year')
    cal_parser.add_argument('month', type=int, help='Month')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\nExamples:")
        print("  datetime-tool now")
        print("  datetime-tool now --unix")
        print("  datetime-tool convert 1700000000")
        print("  datetime-tool format '2024-01-01' --format '%B %d, %Y'")
        print("  datetime-tool add 7 days")
        print("  datetime-tool tz 'America/New_York'")
        print("  datetime-tool relative '2024-01-01'")
        print("  datetime-tool calendar 2024 1")
        sys.exit(1)
    
    if args.command == 'now':
        print(get_now(args.unix, args.iso, args.utc))
    elif args.command == 'convert':
        print(convert_time(args.value))
    elif args.command == 'format':
        print(format_time(args.value, args.format))
    elif args.command == 'add':
        date_str = args.date or datetime.datetime.now().strftime("%Y-%m-%d")
        print(add_time(date_str, args.amount, args.unit))
    elif args.command == 'sub':
        date_str = args.date or datetime.datetime.now().strftime("%Y-%m-%d")
        print(add_time(date_str, -args.amount, args.unit))
    elif args.command == 'tz':
        print(timezone_time(args.timezone, args.time))
    elif args.command == 'relative':
        print(relative_time(args.value))
    elif args.command == 'calendar':
        print(show_calendar(args.year, args.month))


if __name__ == '__main__':
    main()
