#!/usr/bin/env python3
"""
年龄计算器
精确年龄、生日倒计时、星座生肖
"""

import argparse
import sys
import json
from datetime import datetime, date
from typing import Tuple, Optional

# 星座日期范围
ZODIAC_DATES = [
    ((3, 21), (4, 19), "白羊座"),
    ((4, 20), (5, 20), "金牛座"),
    ((5, 21), (6, 21), "双子座"),
    ((6, 22), (7, 22), "巨蟹座"),
    ((7, 23), (8, 22), "狮子座"),
    ((8, 23), (9, 22), "处女座"),
    ((9, 23), (10, 23), "天秤座"),
    ((10, 24), (11, 22), "天蝎座"),
    ((11, 23), (12, 21), "射手座"),
    ((12, 22), (1, 19), "摩羯座"),
    ((1, 20), (2, 18), "水瓶座"),
    ((2, 19), (3, 20), "双鱼座"),
]

# 生肖
CHINESE_ZODIAC = ["猴", "鸡", "狗", "猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊"]

def parse_date(date_str: str) -> Optional[date]:
    """
    解析多种日期格式
    """
    formats = [
        "%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日",
        "%m-%d", "%m/%d", "%m月%d日",
        "%Y%m%d",
    ]
    
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str.strip(), fmt)
            # 如果没有年份，用今年
            if parsed.year == 1900:
                return date(date.today().year, parsed.month, parsed.day)
            return parsed.date()
        except ValueError:
            continue
    
    return None

def calculate_age(birth_date: date, ref_date: date = None) -> Tuple[int, int, int]:
    """
    计算精确年龄
    返回 (年, 月, 日)
    """
    if ref_date is None:
        ref_date = date.today()
    
    years = ref_date.year - birth_date.year
    months = ref_date.month - birth_date.month
    days = ref_date.day - birth_date.day
    
    if days < 0:
        months -= 1
        # 获取上个月的天数
        if ref_date.month == 1:
            prev_month = 12
            prev_year = ref_date.year - 1
        else:
            prev_month = ref_date.month - 1
            prev_year = ref_date.year
        
        days_in_prev_month = (date(prev_year, prev_month + 1, 1) - date(prev_year, prev_month, 1)).days
        days += days_in_prev_month
    
    if months < 0:
        years -= 1
        months += 12
    
    return (years, months, days)

def days_to_birthday(birth_date: date, ref_date: date = None) -> int:
    """
    计算距离下次生日的天数
    """
    if ref_date is None:
        ref_date = date.today()
    
    next_birthday = date(ref_date.year, birth_date.month, birth_date.day)
    
    if next_birthday <= ref_date:
        next_birthday = date(ref_date.year + 1, birth_date.month, birth_date.day)
    
    return (next_birthday - ref_date).days

def get_zodiac(birth_date: date) -> str:
    """
    获取星座
    """
    month, day = birth_date.month, birth_date.day
    
    for (start_m, start_d), (end_m, end_d), zodiac in ZODIAC_DATES:
        # 处理摩羯座跨年情况
        if start_m > end_m:  # 摩羯座 12/22 - 1/19
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
                return zodiac
        else:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d) or \
               (start_m < month < end_m):
                return zodiac
    
    return "未知"

def get_chinese_zodiac(birth_date: date) -> str:
    """
    获取生肖
    """
    return CHINESE_ZODIAC[birth_date.year % 12]

def main():
    parser = argparse.ArgumentParser(description="年龄计算器")
    parser.add_argument("birthday", help="生日日期")
    parser.add_argument("-a", "--action", default="all",
                        choices=["age", "countdown", "zodiac", "all"],
                        help="计算类型")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    birth_date = parse_date(args.birthday)
    if birth_date is None:
        print("错误：无法解析日期，请使用 YYYY-MM-DD 格式", file=sys.stderr)
        sys.exit(1)
    
    today = date.today()
    
    result = {}
    
    if args.action in ["age", "all"]:
        years, months, days = calculate_age(birth_date, today)
        result["age"] = {
            "years": years,
            "months": months,
            "days": days,
            "formatted": f"{years}岁{months}个月{days}天"
        }
    
    if args.action in ["countdown", "all"]:
        days_left = days_to_birthday(birth_date, today)
        result["birthday_countdown"] = {
            "days": days_left,
            "formatted": f"{days_left}天后"
        }
    
    if args.action in ["zodiac", "all"]:
        result["zodiac"] = get_zodiac(birth_date)
        result["chinese_zodiac"] = get_chinese_zodiac(birth_date)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "age" in result:
            print(f"年龄: {result['age']['formatted']}")
        if "zodiac" in result:
            print(f"星座: {result['zodiac']}")
            print(f"生肖: {result['chinese_zodiac']}")
        if "birthday_countdown" in result:
            print(f"距离下次生日: {result['birthday_countdown']['formatted']}")

if __name__ == "__main__":
    main()
