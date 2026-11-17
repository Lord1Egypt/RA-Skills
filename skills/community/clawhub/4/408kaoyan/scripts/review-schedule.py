#!/usr/bin/env python3
"""
艾宾浩斯遗忘曲线 — 复习时间计算器

基于标准艾宾浩斯间隔重复节点：
  R1: 1天后  |  R2: 3天后  |  R3: 7天后
  R4: 16天后 |  R5: 35天后

用法：
  python review-schedule.py <学习日期> [--format json|table]
  
示例：
  python review-schedule.py 2026-07-14
  python review-schedule.py 2026-07-14 --format json
"""

import sys
import json
import io
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


EBBINGHAUS_INTERVALS = [
    ("R1", 1,  "快速费曼复述 + 浏览课件"),
    ("R2", 3,  "做对应章节真题/习题"),
    ("R3", 7,  "画出知识关系图 + 关联更多知识点"),
    ("R4", 16, "限时模拟考试 + 闭卷解题"),
    ("R5", 35, "费曼教学（写笔记/教别人）+ 终极查漏补缺"),
]


def parse_date(date_str: str) -> datetime:
    """解析日期字符串 YYYY-MM-DD."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def calculate_schedule(learn_date: str) -> list[dict]:
    """计算给定学习日期的复习时间表."""
    dt = parse_date(learn_date)
    schedule = []
    for label, days, method in EBBINGHAUS_INTERVALS:
        review_date = dt + timedelta(days=days)
        schedule.append({
            "node": label,
            "days_after": days,
            "review_date": review_date.strftime("%Y-%m-%d"),
            "weekday": _weekday_cn(review_date),
            "method": method,
        })
    return schedule


def _weekday_cn(dt: datetime) -> str:
    """返回中文星期."""
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return days[dt.weekday()]


def format_table(schedule: list[dict]) -> str:
    """格式化为表格."""
    header = f"{'节点':<6} {'距学习':<8} {'复习日期':<14} {'星期':<6} {'推荐方式'}"
    lines = [header, "-" * len(header)]
    for s in schedule:
        lines.append(
            f"{s['node']:<6} {s['days_after']}天后{'':<3} "
            f"{s['review_date']:<14} {s['weekday']:<6} {s['method']}"
        )
    return "\n".join(lines)


def format_json(schedule: list[dict]) -> str:
    """格式化为 JSON."""
    return json.dumps(schedule, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print("用法: python review-schedule.py <学习日期 YYYY-MM-DD> [--format json|table]")
        sys.exit(1)

    learn_date = sys.argv[1]
    output_format = "table"

    for arg in sys.argv[2:]:
        if arg.startswith("--format"):
            output_format = arg.split("=")[-1] if "=" in arg else "table"

    schedule = calculate_schedule(learn_date)

    if output_format == "json":
        print(format_json(schedule))
    else:
        print(f"\n📅 学习日期：{learn_date}")
        print(f"{'='*60}")
        print(format_table(schedule))
        print(f"{'='*60}")
        print("💡 提示：R1-R3 为关键节点，遗忘速度最快，务必按时复习。")
        print()


if __name__ == "__main__":
    main()
