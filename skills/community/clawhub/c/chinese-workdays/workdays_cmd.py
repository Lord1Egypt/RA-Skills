#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI tool for Chinese Workdays Calculator
Usage examples:
  python workdays_cmd.py 2026-01-01 2026-12-31
  python workdays_cmd.py 2026-03  # whole month
  python workdays_cmd.py 2026-Q1 # quarter
"""

import sys
from datetime import datetime
from chinese_workdays import ChineseWorkdays

def parse_date_range(arg: str):
    """Parse date range from user input"""
    # Whole year: 2026 or 2026-YEAR
    if arg.isdigit() or (arg.endswith('-YEAR') and arg[:-5].isdigit()):
        year = int(arg.replace('-YEAR', ''))
        return f"{year}-01-01", f"{year}-12-31"
    
    # Whole month: 2026-03 or 2026-3
    if '-' in arg and len(arg) <= 7:
        parts = arg.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            year, month = int(parts[0]), int(parts[1])
            import calendar
            _, last_day = calendar.monthrange(year, month)
            return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day:02d}"
    
    # Quarter: 2026-Q1, 2026-Q2, etc.
    if '-' in arg and len(arg) >= 5 and arg[-2] == 'Q' and arg[-1] in '1234':
        parts = arg.split('-')
        if len(parts) == 2 and parts[0].isdigit():
            year = int(parts[0])
            quarter = int(arg[-1])  # Extract digit from Q1, Q2, etc.
            start_month = (quarter - 1) * 3 + 1
            end_month = quarter * 3
            # Get last day of end month
            import calendar
            _, last_day = calendar.monthrange(year, end_month)
            return f"{year}-{start_month:02d}-01", f"{year}-{end_month:02d}-{last_day:02d}"
    
    # Assume it's a single date or will be passed through
    return arg, arg

def format_output(start, end, workdays, total_days=None):
    """Format the result output"""
    result = f"📅 工作日统计\n"
    result += f"📊 期间: {start} 至 {end}\n"
    if total_days is not None:
        result += f"📏 总天数: {total_days}\n"
    result += f"💼 法定工作日: {workdays} 天\n\n"
    
    # Calculate percentage if total days known
    if total_days and total_days > 0:
        pct = workdays / total_days * 100
        result += f"工作日占比: {pct:.1f}%\n"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("用法: python workdays_cmd.py <开始日期> [结束日期]")
        print("支持格式:")
        print("  python workdays_cmd.py 2026-01-01 2026-12-31")
        print("  python workdays_cmd.py 2026-03          # 整月")
        print("  python workdays_cmd.py 2026-Q1          # 季度")
        print("  python workdays_cmd.py 2026             # 全年")
        print("  python workdays_cmd.py today            # 今天")
        sys.exit(1)
    
    start_arg = sys.argv[1]
    end_arg = sys.argv[2] if len(sys.argv) > 2 else None
    
    if start_arg.lower() == 'today':
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        start_arg = today
        end_arg = end_arg or today
    
    if end_arg is None:
        start, end = parse_date_range(start_arg)
    else:
        start, end = start_arg, end_arg
    
    try:
        calc = ChineseWorkdays()
        total_days = (calc._parse_date(end) - calc._parse_date(start)).days + 1
        workdays = calc.count_workdays(start, end)
        
        print(format_output(start, end, workdays, total_days))
        
        # Show holidays in range
        holidays = []
        for h in calc.list_holidays():
            h_start = calc._parse_date(h['start'])
            h_end = calc._parse_date(h['end'])
            # Check if holiday overlaps with our range
            range_start = calc._parse_date(start)
            range_end = calc._parse_date(end)
            if not (h_end < range_start or h_start > range_end):
                holidays.append(f"  • {h['name']}: {h['start']} ~ {h['end']}")
        
        if holidays:
            print("📋 期间包含的节假日:")
            print("\n".join(holidays))
            print()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()