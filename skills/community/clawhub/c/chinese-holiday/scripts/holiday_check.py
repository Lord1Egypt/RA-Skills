#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国节假日查询脚本
- 从网络请求节假日数据，不缓存本地数据
- 只返回两种类型：工作日 / 节假日
- 用法: python3 holiday_check.py <日期> [日期2 ...] [--json]
  日期格式: YYYY-MM-DD 或 YYYYMMDD
"""

import json
import sys
import urllib.request
from datetime import datetime


API_SOURCES = [
    {
        "name": "timor",
        "year_url": lambda year: f"https://timor.tech/api/holiday/year/{year}",
        "parse": "parse_timor",
    },
]

WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def fetch_json(url, timeout=8):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_timor(year_data, date_str):
    if year_data.get("code") != 0:
        return None
    holiday = year_data.get("holiday", {})
    mmdd = date_str[5:]
    day = holiday.get(mmdd)
    if not day:
        return None
    # holiday=true 或 after=false → 节假日（休息日）
    # holiday=false 且 after=true → 工作日（补班）
    if day.get("holiday", False):
        return "节假日"
    elif day.get("after", False):
        return "工作日"
    # 在字典中但 holiday=false 且无 after → 工作日
    return "工作日"


def classify_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = dt.weekday()
    weekday_str = WEEKDAY_NAMES[weekday]
    year = dt.year

    day_type = None
    api_source = "fallback"

    for api in API_SOURCES:
        if day_type:
            break
        try:
            url = api["year_url"](year)
            data = fetch_json(url)
            parser = globals()[api["parse"]]
            day_type = parser(data, date_str)
            if day_type:
                api_source = api["name"]
        except Exception:
            pass

    # 所有 API 失败，按星期判断
    if not day_type:
        day_type = "节假日" if weekday >= 5 else "工作日"

    return {
        "date": date_str,
        "type": day_type,
        "weekday": weekday,
        "weekday_str": weekday_str,
        "api": api_source,
    }


def format_output(info):
    return f"{info['date']} {info['weekday_str']} {info['type']}"


def main():
    args = []
    json_output = False

    for arg in sys.argv[1:]:
        if arg == "--json":
            json_output = True
        else:
            args.append(arg)

    if not args:
        print("用法: python3 holiday_check.py <日期> [日期2 ...] [--json]")
        print("日期格式: YYYY-MM-DD 或 YYYYMMDD")
        print("--json: 以 JSON 格式输出")
        sys.exit(0)

    results = []
    for arg in args:
        if arg.isdigit() and len(arg) == 8:
            date_str = f"{arg[0:4]}-{arg[4:6]}-{arg[6:8]}"
        elif len(arg) == 10 and arg[4] == "-" and arg[7] == "-":
            date_str = arg
        else:
            print(f"错误: 日期格式不正确 '{arg}'", file=sys.stderr)
            continue

        results.append(classify_date(date_str))

    if json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for info in results:
            print(format_output(info))


if __name__ == "__main__":
    main()
