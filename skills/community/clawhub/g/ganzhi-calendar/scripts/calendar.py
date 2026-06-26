#!/usr/bin/env python3
"""
Chinese Calendar Stem-Branch Calculator

Reference: 1984-02-02 = 甲子年甲子月甲子日 (start of 60-year cycle)
"""

from datetime import datetime, timedelta
import sys

# Heavenly Stems (天干)
STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# Earthly Branches (地支)
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# Reference: 1983-02-05 = 甲子日 (calibrated for accuracy)
REFERENCE_DATE = datetime(1983, 2, 5)

def get_day_stem_branch(date):
    """Calculate day stem-branch."""
    delta = (date.date() - REFERENCE_DATE.date()).days
    stem_idx = delta % 10
    branch_idx = delta % 12
    return STEMS[stem_idx] + BRANCHES[branch_idx]

def get_month_stem_branch(year, month):
    """
    Calculate month stem-branch.
    The month branches start from 寅 (month 1 = 寅月, month 2 = 卯月, etc.)
    The month stems are calculated from the year's stem.
    """
    # First find year stem index (0=甲, 1=乙, etc.)
    year_delta = year - 4  # 1984 is甲子 (stem 0), and 4 BCE was甲子
    year_stem_idx = year_delta % 10
    
    # Month branches: 正月=寅, 二月=卯, 三月=辰...
    month_branch_idx = (month + 1) % 12  # month 1 -> branch 2 (寅)
    if month_branch_idx == 0:
        month_branch_idx = 12
    
    # Month stems: formula is (year_stem * 2 + month) % 10
    month_stem_idx = (year_stem_idx * 2 + month) % 10
    
    return STEMS[month_stem_idx] + BRANCHES[month_branch_idx - 1]

def get_year_stem_branch(year):
    """Calculate year stem-branch."""
    # 1984 = 甲子, so offset
    year_delta = year - 4  # Adjust because 4 BCE was甲子 year
    cycle_year = year_delta % 60
    if cycle_year < 0:
        cycle_year += 60
    
    stem_idx = cycle_year % 10
    branch_idx = cycle_year % 12
    
    return STEMS[stem_idx] + BRANCHES[branch_idx]

def get_zodiac(branch):
    """Get Chinese zodiac animal from branch."""
    zodiac_map = {
        '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
        '辰': '龙', '巳': '蛇', '午': '马', '未': '羊',
        '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪'
    }
    return zodiac_map.get(branch, '?')

def get_nongli(date):
    """Get simplified lunar date. 
    This is approximate - uses 1984 as reference and assumes non-leap years.
    For accurate results, need a proper lunar calendar library.
    """
    # Find days since reference date
    delta = (date.date() - REFERENCE_DATE.date()).days
    
    # Chinese New Year 1984 was Feb 2
    # Each year has ~354 days (lunar year)
    # This is a rough approximation
    year_diff = date.year - 1984
    cnY_this_year = datetime(date.year, 2, 14)  # Approximate, real CNY varies
    
    days_from_cny = (date.date() - cnY_this_year.date()).days
    
    if days_from_cny < 0:
        # Before Chinese New Year, belong to previous lunar year
        cnY_prev = datetime(date.year - 1, 2, 14)
        days_from_cny = (date.date() - cnY_prev.date()).days
        lunar_year = date.year - 1
    else:
        lunar_year = date.year
    
    # Calculate which month (rough)
    month = days_from_cny // 30 + 1
    day = days_from_cny % 30 + 1
    
    # Format
    if day <= 10:
        day_str = f"初{STEMS[day-1]}"
    elif day <= 20:
        day_str = f"十{STEMS[day-10]}"
    elif day <= 29:
        day_str = f"廿{STEMS[day-20]}"
    else:
        day_str = f"卅{STEMS[day-30]}"
    
    month_zh = ['', '正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
    month_str = month_zh[min(month, 12)]
    
    return f"农历{month_str}月{day_str}"

def format_date(date):
    """Format a single date with all stem-branch info."""
    year = date.year
    month = date.month
    day = date.day
    
    year_sb = get_year_stem_branch(year)
    month_sb = get_month_stem_branch(year, month)
    day_sb = get_day_stem_branch(date)
    zodiac = get_zodiac(year_sb[1])
    nongli = get_nongli(date)
    
    return {
        'date': f"{month}月{day}日",
        'weekday': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][date.weekday()],
        'nongli': nongli,
        'month_sb': month_sb + '月',
        'day_sb': day_sb + '日',
        'year_sb': year_sb,
        'zodiac': zodiac
    }

def generate_weekly(start_date):
    """Generate a week of calendar data."""
    results = []
    for i in range(7):
        d = start_date + timedelta(days=i)
        info = format_date(d)
        results.append(info)
    return results

def main():
    if len(sys.argv) > 1:
        # Parse date from argument (YYYY-MM-DD or YYYY-M-D)
        try:
            parts = sys.argv[1].split('-')
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            date = datetime(year, month, day)
        except:
            print("Usage: python chinese_calendar.py [YYYY-MM-DD]")
            print("Or run without args for this week's calendar")
            sys.exit(1)
        
        info = format_date(date)
        print(f"{info['date']} {info['weekday']}")
        print(f"农历: {info['nongli']}")
        print(f"月柱: {info['month_sb']}")
        print(f"日柱: {info['day_sb']}")
        print(f"年柱: {info['year_sb']} ({info['zodiac']}年)")
    else:
        # Generate this week's calendar
        today = datetime.now()
        week = generate_weekly(today)
        
        # Get year stem-branch
        year_info = format_date(today)
        
        print(f"{year_info['year_sb']}({year_info['zodiac']}年) 🐎")
        print("| Date | Weekday | Nongli | 月天干地支 | 日天干地支 |")
        print("| ---- | ------- | ------ | ---------- | ---------- |")
        for info in week:
            print(f"| {info['date']} | {info['weekday']} | {info['nongli']} | {info['month_sb']} | {info['day_sb']} |")

if __name__ == "__main__":
    main()
