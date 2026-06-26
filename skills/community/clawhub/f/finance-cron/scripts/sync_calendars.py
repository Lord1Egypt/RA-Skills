#!/usr/bin/env python3
"""
Trading Calendar Sync Script
Syncs trading calendars from pandas_market_calendars and other sources
"""

import argparse
import json
import sys
from datetime import datetime, date
from pathlib import Path

try:
    import pandas_market_calendars as mcal
    HAS_PANDAS_MCAL = True
except ImportError:
    HAS_PANDAS_MCAL = False

try:
    import exchange_calendars as xcals
    HAS_XCALS = True
except ImportError:
    HAS_XCALS = False


def sync_us_calendar(years: list[int]) -> dict:
    """Sync US market calendar (NYSE)"""
    holidays = {}
    
    if HAS_PANDAS_MCAL:
        nyse = mcal.get_calendar('NYSE')
        for year in years:
            schedule = nyse.schedule(f'{year}-01-01', f'{year}-12-31')
            # Get all dates that are NOT in schedule (holidays + weekends)
            # Actually, we need holidays specifically
            holidays_list = []
            
            # Use valid_days to find all trading days
            valid_days = nyse.valid_days(f'{year}-01-01', f'{year}-12-31')
            
            # Iterate through all weekdays in the year
            from datetime import timedelta
            current = date(year, 1, 1)
            end = date(year, 12, 31)
            
            while current <= end:
                # Skip weekends
                if current.weekday() < 5:  # Mon-Fri
                    if current not in valid_days.to_list():
                        holidays_list.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
            
            holidays[str(year)] = holidays_list
    else:
        # Fallback: return empty dict, will use local data
        print("Warning: pandas_market_calendars not installed", file=sys.stderr)
        return None
    
    return {
        "market": "US",
        "holidays": holidays,
        "weekends": [0, 6],
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "source": "pandas_market_calendars (NYSE)"
    }


def sync_cn_calendar(years: list[int]) -> dict:
    """
    Sync China A-share market calendar
    Note: Requires chinese_calendar or manual data
    """
    holidays = {}
    workdays = {}
    
    # Chinese calendar is complex due to lunar new year adjustments
    # Best to use chinese_calendar library or manual maintenance
    
    try:
        import chinese_calendar
        from datetime import timedelta
        
        for year in years:
            holidays_list = []
            workdays_list = []
            
            current = date(year, 1, 1)
            end = date(year, 12, 31)
            
            while current <= end:
                is_holiday = chinese_calendar.is_holiday(current)
                is_workday = chinese_calendar.is_workday(current)
                
                # Weekend but marked as workday (调休)
                if current.weekday() >= 5 and is_workday:
                    workdays_list.append(current.strftime('%Y-%m-%d'))
                # Weekday but holiday
                elif current.weekday() < 5 and is_holiday:
                    holidays_list.append(current.strftime('%Y-%m-%d'))
                    
                current += timedelta(days=1)
            
            holidays[str(year)] = holidays_list
            workdays[str(year)] = workdays_list
    except ImportError:
        print("Warning: chinese_calendar not installed, using local data", file=sys.stderr)
        return None
    
    return {
        "market": "CN",
        "holidays": holidays,
        "workdays": workdays,
        "weekends": [0, 6],
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "source": "chinese_calendar"
    }


def sync_hk_calendar(years: list[int]) -> dict:
    """Sync Hong Kong market calendar"""
    holidays = {}
    
    if HAS_PANDAS_MCAL:
        hkex = mcal.get_calendar('HKEX')
        
        for year in years:
            holidays_list = []
            schedule = hkex.schedule(f'{year}-01-01', f'{year}-12-31')
            valid_days = hkex.valid_days(f'{year}-01-01', f'{year}-12-31')
            
            from datetime import timedelta
            current = date(year, 1, 1)
            end = date(year, 12, 31)
            
            while current <= end:
                if current.weekday() < 5:
                    if current not in valid_days.to_list():
                        holidays_list.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
            
            holidays[str(year)] = holidays_list
    else:
        print("Warning: pandas_market_calendars not installed", file=sys.stderr)
        return None
    
    return {
        "market": "HK",
        "holidays": holidays,
        "weekends": [0, 6],
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "source": "pandas_market_calendars (HKEX)"
    }


def main():
    parser = argparse.ArgumentParser(description='Sync trading calendars')
    parser.add_argument('--market', '-m', choices=['US', 'CN', 'HK', 'ALL'], 
                        default='ALL', help='Market to sync')
    parser.add_argument('--years', '-y', type=int, nargs='+',
                        default=[2024, 2025], help='Years to sync')
    parser.add_argument('--output', '-o', type=str,
                        default=None, help='Output directory')
    
    args = parser.parse_args()
    
    # Determine output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / 'data'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    markets = ['US', 'CN', 'HK'] if args.market == 'ALL' else [args.market]
    
    sync_functions = {
        'US': sync_us_calendar,
        'CN': sync_cn_calendar,
        'HK': sync_hk_calendar,
    }
    
    file_names = {
        'US': 'us-holidays.json',
        'CN': 'cn-holidays.json',
        'HK': 'hk-holidays.json',
    }
    
    results = {}
    
    for market in markets:
        print(f"Syncing {market} calendar...")
        
        sync_func = sync_functions[market]
        calendar_data = sync_func(args.years)
        
        if calendar_data:
            output_file = output_dir / file_names[market]
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(calendar_data, f, indent=2)
            results[market] = {
                'status': 'success',
                'file': str(output_file),
                'holidays_count': sum(len(v) for v in calendar_data.get('holidays', {}).values())
            }
            print(f"  Saved to {output_file}")
        else:
            results[market] = {
                'status': 'skipped',
                'reason': 'Library not available or using local data'
            }
            print(f"  Skipped (using local data)")
    
    print("\nSync results:")
    print(json.dumps(results, indent=2))
    
    return 0 if all(r.get('status') != 'error' for r in results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
