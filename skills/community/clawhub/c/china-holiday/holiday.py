#!/usr/bin/env python3
"""
中国日历服务 - 判断法定节假日、周末、调休、寒暑假
"""

import json
import datetime
import sys
from pathlib import Path

try:
    import chinese_calendar
except ImportError:
    print("请安装 chinese-calendar: pip install chinese-calendar")
    sys.exit(1)


# 配置文件路径
CONFIG_DIR = Path(__file__).parent / "config"
REGIONS_FILE = CONFIG_DIR / "regions.json"


def load_regions():
    """加载地区配置"""
    if REGIONS_FILE.exists():
        with open(REGIONS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def is_weekend(date):
    """判断是否周末"""
    return date.weekday() >= 5  # 5=Saturday, 6=Sunday


def get_holiday_info(date):
    """获取假日信息"""
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    # 1. 检查是否为调休补班日（优先判断）
    if chinese_calendar.is_in_lieu(date):
        return {
            "date": str(date),
            "type": "workday",
            "name": "调休补班"
        }

    # 2. 检查是否为法定节假日 (假期)
    if chinese_calendar.is_holiday(date):
        is_hol, holiday_name = chinese_calendar.get_holiday_detail(date)
        return {
            "date": str(date),
            "type": "holiday",
            "name": holiday_name or "法定节假日",
            "is_off_day": True
        }

    # 3. 检查周末
    if is_weekend(date):
        return {
            "date": str(date),
            "type": "weekend",
            "name": "周末"
        }

    # 4. 普通工作日
    return {
        "date": str(date),
        "type": "workday",
        "name": "工作日"
    }


def is_holiday(date):
    """判断是否为假日（法定节假日或周末）"""
    info = get_holiday_info(date)
    return info["type"] in ("holiday", "weekend")


def is_workday(date):
    """判断是否需要上班（工作日或调休日）"""
    info = get_holiday_info(date)
    return info["type"] in ("workday",)


def get_holiday_name(date):
    """获取假日名称"""
    info = get_holiday_info(date)
    return info["name"]


def get_vacation(region, year=None):
    """获取指定地区的寒暑假时间"""
    regions = load_regions()
    if year is None:
        year = datetime.datetime.now().year

    region_data = regions.get(region)
    if not region_data:
        return None

    return {
        "region": region,
        "year": year,
        "summer": region_data.get("summer"),
        "winter": region_data.get("winter"),
        "spring": region_data.get("spring"),
        "autumn": region_data.get("autumn"),
    }


def format_today():
    """格式化输出今天的日期信息"""
    today = datetime.date.today()
    info = get_holiday_info(today)

    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_names[today.weekday()]

    result = f"今天是 {today} {weekday}\n"

    if info["type"] == "holiday":
        result += f"🎉 {info['name']} 假期"
    elif info["type"] == "weekend":
        result += "🎉 周末"
    elif info["type"] == "workday" and info["name"] == "调休补班":
        result += "💼 调休补班日"
    else:
        result += "💼 工作日"

    return result


def format_date(date_str):
    """格式化输出指定日期的信息"""
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "日期格式错误，请使用 YYYY-MM-DD"

    info = get_holiday_info(date)

    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_names[date.weekday()]

    result = f"{date} {weekday}\n"

    if info["type"] == "holiday":
        result += f"🎉 {info['name']}"
    elif info["type"] == "weekend":
        result += "🎉 周末"
    elif info["type"] == "workday" and info["name"] == "调休补班":
        result += "💼 调休补班日"
    else:
        result += "💼 工作日"

    return result


def list_holidays(year):
    """列出全年所有节假日"""
    holidays = []

    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    year_holidays = chinese_calendar.get_holidays(start, end)

    for date in year_holidays:
        # is_holiday 返回 True 表示是假日，False 表示是补班日
        is_off = chinese_calendar.is_holiday(date)
        is_hol, name = chinese_calendar.get_holiday_detail(date)
        holidays.append({
            "date": str(date),
            "name": name or ("法定节假日" if is_off else "补班日"),
            "type": "假期" if is_off else "补班"
        })

    holidays.sort(key=lambda x: x["date"])

    return holidays


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python holiday.py today              # 查看今天")
        print("  python holiday.py 2026-01-01         # 查看指定日期")
        print("  python holiday.py vacation 北京      # 查看北京寒暑假")
        print("  python holiday.py list 2026          # 查看全年节假日")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "today":
        print(format_today())
    elif cmd == "list":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.date.today().year
        holidays = list_holidays(year)
        print(f"{year} 年节假日:")
        for h in holidays:
            icon = "🎉" if h["type"] == "假期" else "💼"
            print(f"  {h['date']} {icon} {h['name']}")
    elif cmd == "vacation":
        region = sys.argv[2] if len(sys.argv) > 2 else "北京"
        vac = get_vacation(region)
        if vac:
            print(f"{region} {vac['year']} 年:")
            if vac["summer"]:
                print(f"  暑假: {vac['summer']}")
            if vac["winter"]:
                print(f"  寒假: {vac['winter']}")
            if vac["spring"]:
                print(f"  春假: {vac['spring']}")
            if vac["autumn"]:
                print(f"  秋假: {vac['autumn']}")
        else:
            print(f"未找到 {region} 的配置")
    else:
        print(format_date(cmd))


if __name__ == "__main__":
    main()
