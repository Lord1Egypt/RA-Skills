#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date Utils - 日期时间计算工具

功能：
- Unix 时间戳转换
- 相对日期计算（昨天/前天/N 天前）
- 日期格式转换
- 工作日判断
- 周数计算
- 日期差值计算
- 本周/上周起止日期

时区：Asia/Shanghai (UTC+8)
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone

# 固定时区：Asia/Shanghai (UTC+8)
CST = timezone(timedelta(hours=8))


def get_now():
    """获取当前上海时间"""
    return datetime.now(CST)


def parse_date(date_str):
    """解析日期字符串，支持 today/yesterday 或 YYYY-MM-DD 格式"""
    if date_str == "today":
        return get_now().date()
    elif date_str == "yesterday":
        return (get_now() - timedelta(days=1)).date()
    else:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(json.dumps({
                "error": f"日期格式错误：{date_str}，请使用 YYYY-MM-DD 格式或 today/yesterday",
                "command": "parse"
            }, ensure_ascii=False))
            sys.exit(1)


def cmd_timestamp(args):
    """获取 Unix 时间戳"""
    date = parse_date(args.date)
    time_str = args.time if args.time else "00:00:00"

    # 构造完整时间，支持 HH:MM 和 HH:MM:SS 格式
    try:
        parts = time_str.split(":")
        if len(parts) == 2:
            h, m = map(int, parts)
            s = 0
        elif len(parts) == 3:
            h, m, s = map(int, parts)
        else:
            raise ValueError("时间格式错误")
        dt = datetime(date.year, date.month, date.day, h, m, s, tzinfo=CST)
        timestamp = int(dt.timestamp())
    except ValueError:
        print(json.dumps({
            "error": f"时间格式错误：{time_str}，请使用 HH:MM 或 HH:MM:SS 格式",
            "command": "timestamp"
        }, ensure_ascii=False))
        sys.exit(1)

    result = {
        "command": "timestamp",
        "date": date.isoformat(),
        "time": time_str,
        "timestamp": timestamp,
        "timezone": "Asia/Shanghai (UTC+8)"
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_relative(args):
    """获取相对日期"""
    if args.base:
        base_date = parse_date(args.base)
    else:
        base_date = get_now().date()

    offset = args.offset
    target_date = base_date + timedelta(days=offset)

    # 星期几
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_str = weekday_cn[target_date.weekday()]

    result = {
        "command": "relative",
        "base_date": base_date.isoformat(),
        "offset": offset,
        "target_date": target_date.isoformat(),
        "weekday": weekday_str
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_format(args):
    """日期格式转换"""
    date = parse_date(args.date)
    target_format = args.target

    # 中文格式特殊处理
    if "%Y年%m月%d日" in target_format:
        formatted = date.strftime("%Y年%m月%d日")
    else:
        formatted = date.strftime(target_format)

    # 星期几（中文）
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_str = weekday_cn[date.weekday()]

    # ISO 周数
    iso_year, iso_week, _ = date.isocalendar()

    result = {
        "command": "format",
        "input_date": date.isoformat(),
        "format": target_format,
        "formatted": formatted,
        "weekday": weekday_str,
        "iso_week": f"{iso_year}-W{iso_week:02d}",
        "iso_year": iso_year,
        "iso_week_number": iso_week
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_workday(args):
    """工作日判断"""
    date = parse_date(args.date)
    weekday = date.weekday()  # 0=周一，6=周日
    is_workday = weekday < 5

    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_str = weekday_cn[weekday]

    result = {
        "command": "workday",
        "date": date.isoformat(),
        "weekday": weekday_str,
        "is_workday": is_workday,
        "status": "工作日" if is_workday else "休息日"
    }

    # 获取最近工作日
    if args.nearest and not is_workday:
        # 向前查找最近工作日
        d = date
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        result["nearest_workday"] = d.isoformat()
        result["nearest_workday_weekday"] = weekday_cn[d.weekday()]

    print(json.dumps(result, ensure_ascii=False))


def cmd_week(args):
    """获取 ISO 周数"""
    date = parse_date(args.date)
    iso_year, iso_week, _ = date.isocalendar()

    # 本周起止日期（周一到周日）
    monday = date - timedelta(days=date.weekday())
    sunday = monday + timedelta(days=6)

    result = {
        "command": "week",
        "date": date.isoformat(),
        "iso_year": iso_year,
        "iso_week": iso_week,
        "week_label": f"{iso_year}-W{iso_week:02d}",
        "week_start": monday.isoformat(),
        "week_end": sunday.isoformat(),
        "week_range": f"{monday.strftime('%m月%d日')}~{sunday.strftime('%m月%d日')}"
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_diff(args):
    """计算日期差值"""
    start = parse_date(args.start)
    end = parse_date(args.end)
    delta = end - start
    days = delta.days

    result = {
        "command": "diff",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "days": days,
        "weeks": days // 7,
        "remaining_days": days % 7
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_week_range(args):
    """获取本周/上周起止日期"""
    if args.date:
        date = parse_date(args.date)
    else:
        date = get_now().date()

    offset = args.offset if args.offset else 0
    # 计算目标周的周一
    monday = date - timedelta(days=date.weekday()) + timedelta(weeks=offset)
    sunday = monday + timedelta(days=6)

    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    result = {
        "command": "week_range",
        "offset": offset,
        "label": "本周" if offset == 0 else f"{abs(offset)}周{'前' if offset < 0 else '后'}",
        "monday": monday.isoformat(),
        "sunday": sunday.isoformat(),
        "monday_weekday": weekday_cn[monday.weekday()],
        "sunday_weekday": weekday_cn[sunday.weekday()],
        "range": f"{monday.strftime('%m月%d日')}~{sunday.strftime('%m月%d日')}"
    }
    print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="日期时间计算工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # timestamp
    ts_parser = subparsers.add_parser("timestamp", help="获取 Unix 时间戳")
    ts_parser.add_argument("--date", default="today", help="日期 (YYYY-MM-DD / today / yesterday)")
    ts_parser.add_argument("--time", default="00:00:00", help="时间 (HH:MM:SS)")

    # relative
    rel_parser = subparsers.add_parser("relative", help="获取相对日期")
    rel_parser.add_argument("--offset", type=int, required=True, help="偏移天数（正数=未来，负数=过去）")
    rel_parser.add_argument("--base", help="基准日期 (YYYY-MM-DD / today)，默认今天")

    # format
    fmt_parser = subparsers.add_parser("format", help="日期格式转换")
    fmt_parser.add_argument("--date", default="today", help="日期 (YYYY-MM-DD / today / yesterday)")
    fmt_parser.add_argument("--target", default="%Y-%m-%d", help="目标格式 (strftime 格式)")

    # workday
    wd_parser = subparsers.add_parser("workday", help="工作日判断")
    wd_parser.add_argument("--date", default="today", help="日期 (YYYY-MM-DD / today / yesterday)")
    wd_parser.add_argument("--nearest", action="store_true", help="获取最近的工作日")

    # week
    wk_parser = subparsers.add_parser("week", help="获取 ISO 周数")
    wk_parser.add_argument("--date", default="today", help="日期 (YYYY-MM-DD / today / yesterday)")

    # diff
    diff_parser = subparsers.add_parser("diff", help="计算日期差值")
    diff_parser.add_argument("--start", required=True, help="开始日期 (YYYY-MM-DD)")
    diff_parser.add_argument("--end", required=True, help="结束日期 (YYYY-MM-DD)")

    # week-range
    wr_parser = subparsers.add_parser("week-range", help="获取本周/上周起止日期")
    wr_parser.add_argument("--date", help="基准日期 (YYYY-MM-DD / today)，默认今天")
    wr_parser.add_argument("--offset", type=int, default=0, help="周偏移（-1=上周，1=下周）")

    args = parser.parse_args()

    if args.command == "timestamp":
        cmd_timestamp(args)
    elif args.command == "relative":
        cmd_relative(args)
    elif args.command == "format":
        cmd_format(args)
    elif args.command == "workday":
        cmd_workday(args)
    elif args.command == "week":
        cmd_week(args)
    elif args.command == "diff":
        cmd_diff(args)
    elif args.command == "week-range":
        cmd_week_range(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
