#!/usr/bin/env python3
"""
Chinese Statutory Holidays Query Tool

Query Chinese statutory holidays, check if a date is a working day/holiday.
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# Chinese Statutory Holidays Data
# Format: { year: { "holidays": [...], "adjusted_workdays": [...] } }
HOLIDAYS_DATA = {
    2024: {
        "holidays": [
            {"name": "元旦", "name_en": "New Year's Day", "dates": ["2024-01-01"]},
            {"name": "春节", "name_en": "Spring Festival", "dates": ["2024-02-10", "2024-02-11", "2024-02-12", "2024-02-13", "2024-02-14", "2024-02-15", "2024-02-17"]},
            {"name": "清明节", "name_en": "Qingming Festival", "dates": ["2024-04-04", "2024-04-05", "2024-04-06"]},
            {"name": "劳动节", "name_en": "Labor Day", "dates": ["2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-05-05"]},
            {"name": "端午节", "name_en": "Dragon Boat Festival", "dates": ["2024-06-10"]},
            {"name": "中秋节", "name_en": "Mid-Autumn Festival", "dates": ["2024-09-17"]},
            {"name": "国庆节", "name_en": "National Day", "dates": ["2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04", "2024-10-05", "2024-10-06", "2024-10-07"]},
        ],
        "adjusted_workdays": ["2024-02-04", "2024-02-18", "2024-04-07", "2024-04-28", "2024-05-11", "2024-09-14", "2024-09-29", "2024-10-12"]
    },
    2025: {
        "holidays": [
            {"name": "元旦", "name_en": "New Year's Day", "dates": ["2025-01-01"]},
            {"name": "春节", "name_en": "Spring Festival", "dates": ["2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31", "2025-02-01", "2025-02-02", "2025-02-03", "2025-02-04"]},
            {"name": "清明节", "name_en": "Qingming Festival", "dates": ["2025-04-04", "2025-04-05", "2025-04-06"]},
            {"name": "劳动节", "name_en": "Labor Day", "dates": ["2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05"]},
            {"name": "端午节", "name_en": "Dragon Boat Festival", "dates": ["2025-05-31", "2025-06-01", "2025-06-02"]},
            {"name": "中秋节", "name_en": "Mid-Autumn Festival", "dates": ["2025-10-06"]},
            {"name": "国庆节", "name_en": "National Day", "dates": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05", "2025-10-06", "2025-10-07", "2025-10-08"]},
        ],
        "adjusted_workdays": ["2025-01-26", "2025-02-08", "2025-04-27", "2025-09-28", "2025-10-11"]
    },
    2026: {
        "holidays": [
            {"name": "元旦", "name_en": "New Year's Day", "dates": ["2026-01-01", "2026-01-02", "2026-01-03"]},
            {"name": "春节", "name_en": "Spring Festival", "dates": ["2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21", "2026-02-22", "2026-02-23"]},
            {"name": "清明节", "name_en": "Qingming Festival", "dates": ["2026-04-05", "2026-04-06", "2026-04-07"]},
            {"name": "劳动节", "name_en": "Labor Day", "dates": ["2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05"]},
            {"name": "端午节", "name_en": "Dragon Boat Festival", "dates": ["2026-06-19", "2026-06-20", "2026-06-21"]},
            {"name": "中秋节", "name_en": "Mid-Autumn Festival", "dates": ["2026-09-25"]},
            {"name": "国庆节", "name_en": "National Day", "dates": ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08"]},
        ],
        "adjusted_workdays": ["2026-02-15", "2026-02-28", "2026-09-27", "2026-10-10", "2026-10-11"]
    }
}

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(dt: datetime) -> str:
    """Format datetime with weekday."""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return f"{dt.strftime('%Y-%m-%d')} ({weekdays[dt.weekday()]})"

def get_holiday_set(year: int) -> Tuple[set, set]:
    """Get holiday dates and adjusted workdays for a year."""
    if year not in HOLIDAYS_DATA:
        return set(), set()
    
    holiday_dates = set()
    for holiday in HOLIDAYS_DATA[year]["holidays"]:
        holiday_dates.update(holiday["dates"])
    
    adjusted_workdays = set(HOLIDAYS_DATA[year]["adjusted_workdays"])
    
    return holiday_dates, adjusted_workdays

def get_holiday_info(date_str: str) -> Optional[Dict]:
    """Get holiday info for a specific date."""
    dt = parse_date(date_str)
    year = dt.year
    
    if year not in HOLIDAYS_DATA:
        return None
    
    for holiday in HOLIDAYS_DATA[year]["holidays"]:
        if date_str in holiday["dates"]:
            return holiday
    
    return None

def check_date(date_str: str) -> Tuple[int, str, Optional[Dict]]:
    """
    Check if a date is a working day, weekend, holiday, or adjusted workday.
    
    Returns:
        (status_code, status_name, holiday_info)
        status_code: 0=working, 1=weekend, 2=holiday, 3=adjusted workday
    """
    dt = parse_date(date_str)
    year = dt.year
    
    holiday_dates, adjusted_workdays = get_holiday_set(year)
    
    # Check if it's an adjusted workday first
    if date_str in adjusted_workdays:
        return 3, "ADJUSTED_WORKDAY", None
    
    # Check if it's a holiday
    if date_str in holiday_dates:
        holiday_info = get_holiday_info(date_str)
        return 2, "HOLIDAY", holiday_info
    
    # Check if it's a weekend
    if dt.weekday() >= 5:  # Saturday or Sunday
        return 1, "WEEKEND", None
    
    # Otherwise it's a working day
    return 0, "WORKING", None

def cmd_today():
    """Check today's status."""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    code, status, holiday_info = check_date(date_str)
    
    print(f"{format_date(today)}")
    
    if status == "HOLIDAY" and holiday_info:
        print(f"Status: {status} - {holiday_info['name']} ({holiday_info['name_en']})")
    elif status == "ADJUSTED_WORKDAY":
        print(f"Status: {status} - Working day (调休上班)")
    elif status == "WEEKEND":
        print(f"Status: {status} - Rest day")
    else:
        print(f"Status: {status} - Normal working day")
    
    return code

def cmd_check(date_str: str):
    """Check a specific date."""
    try:
        dt = parse_date(date_str)
    except ValueError:
        print(f"Error: Invalid date format. Use YYYY-MM-DD.")
        return -1
    
    code, status, holiday_info = check_date(date_str)
    
    print(f"{format_date(dt)}")
    
    if status == "HOLIDAY" and holiday_info:
        print(f"Status: {status} - {holiday_info['name']} ({holiday_info['name_en']})")
    elif status == "ADJUSTED_WORKDAY":
        print(f"Status: {status} - Working day (调休上班)")
    elif status == "WEEKEND":
        print(f"Status: {status} - Rest day")
    else:
        print(f"Status: {status} - Normal working day")
    
    return code

def cmd_list(year: int):
    """List all holidays in a year."""
    if year not in HOLIDAYS_DATA:
        print(f"Error: No holiday data available for year {year}")
        print(f"Available years: {', '.join(map(str, sorted(HOLIDAYS_DATA.keys())))}")
        return
    
    print(f"=== {year} Chinese Statutory Holidays ===\n")
    
    for i, holiday in enumerate(HOLIDAYS_DATA[year]["holidays"], 1):
        dates = holiday["dates"]
        name = holiday["name"]
        name_en = holiday["name_en"]
        
        if len(dates) == 1:
            print(f"{i}. {name} ({name_en})")
            print(f"   {dates[0]}\n")
        else:
            print(f"{i}. {name} ({name_en})")
            print(f"   {dates[0]} to {dates[-1]} ({len(dates)} days)\n")
    
    # Show adjusted workdays
    adjusted = HOLIDAYS_DATA[year]["adjusted_workdays"]
    if adjusted:
        print(f"Adjusted Workdays (调休上班):")
        for d in sorted(adjusted):
            dt = parse_date(d)
            weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            print(f"   {d} ({weekdays[dt.weekday()]})")

def cmd_next():
    """Find the next upcoming holiday."""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    
    # Search in current year and next year
    found = None
    for year in [today.year, today.year + 1]:
        if year not in HOLIDAYS_DATA:
            continue
        
        for holiday in HOLIDAYS_DATA[year]["holidays"]:
            for date_str in holiday["dates"]:
                if date_str > today_str:
                    dt = parse_date(date_str)
                    days_until = (dt - today).days
                    if found is None or days_until < found["days"]:
                        found = {
                            "name": holiday["name"],
                            "name_en": holiday["name_en"],
                            "start": holiday["dates"][0],
                            "end": holiday["dates"][-1],
                            "days": days_until
                        }
                    break
    
    if found:
        print(f"Next holiday: {found['name']} ({found['name_en']})")
        if found["start"] == found["end"]:
            print(f"Date: {found['start']}")
        else:
            print(f"Date: {found['start']} to {found['end']}")
        print(f"Days until: {found['days']} days")
    else:
        print("No upcoming holidays found in available data.")

def print_usage():
    """Print usage information."""
    print("Chinese Statutory Holidays Query Tool\n")
    print("Usage:")
    print("  python holidays.py today              Check today's status")
    print("  python holidays.py check <YYYY-MM-DD> Check a specific date")
    print("  python holidays.py list <year>        List all holidays in a year")
    print("  python holidays.py next               Find next upcoming holiday")
    print("\nExamples:")
    print("  python holidays.py today")
    print("  python holidays.py check 2025-01-01")
    print("  python holidays.py list 2025")
    print("  python holidays.py next")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "today":
        sys.exit(cmd_today())
    elif command == "check":
        if len(sys.argv) < 3:
            print("Error: Please provide a date (YYYY-MM-DD)")
            sys.exit(1)
        sys.exit(cmd_check(sys.argv[2]))
    elif command == "list":
        if len(sys.argv) < 3:
            print("Error: Please provide a year")
            sys.exit(1)
        try:
            year = int(sys.argv[2])
            cmd_list(year)
        except ValueError:
            print("Error: Year must be a number")
            sys.exit(1)
    elif command == "next":
        cmd_next()
    elif command in ["help", "-h", "--help"]:
        print_usage()
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
