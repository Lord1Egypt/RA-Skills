#!/usr/bin/env python3
"""
中国节假日查询 - 调用 timor.tech 免费节假日 API
用法: python3 china_holiday.py <command> [args]
"""

import sys
import urllib.request
import json
from datetime import date, datetime

BASE_URL = "https://timor.tech/api/holiday"

TODAY = date.today()
TODAY_STR = TODAY.isoformat()


def api_get(path: str) -> dict:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; ChinaHolidaySkill/1.0)"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def format_date(d: str) -> str:
    """把 2026-01-01 转成 2026年1月1日"""
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except Exception:
        return d


def format_type_info(t: dict) -> str:
    type_map = {0: "工作日", 1: "周末", 2: "节日", 3: "调休"}
    return f"【类型】{type_map.get(t.get('type'), '未知')} · {t.get('name', '')} · 周{'一二三四五六日'[t.get('week', 1)-1]}"


def cmd_info(date_str: str = None):
    """查询指定日期节假日信息"""
    target = f"/{date_str}" if date_str else ""
    data = api_get(f"/info{target}")
    if data.get("code") != 0:
        print(f"❌ 服务异常: {data}")
        return

    t = data.get("type", {})
    h = data.get("holiday")

    print(f"📅 {format_date(date_str) if date_str else format_date(TODAY_STR)}")
    print(f"   {format_type_info(t)}")

    if h:
        holiday_type = "🎉 节假日" if h.get("holiday") else "🔧 调休"
        wage = h.get("wage", 1)
        name = h.get("name", "")
        extra = ""
        if not h.get("holiday") and h.get("target"):
            extra = f"（目标: {h.get('target')}）"
        elif not h.get("holiday") and h.get("after") is not None:
            after_str = "假后调休" if h.get("after") else "假前调休"
            extra = f"（{after_str}）"
        print(f"   {holiday_type} {name} {extra} 薪资×{wage}")
    else:
        print("   普通工作日/周末，无特殊节假日安排")


def cmd_batch(dates: list):
    """批量查询多个日期"""
    if not dates:
        print("❌ 请提供至少一个日期，格式: 2026-01-01")
        return
    params = "&".join(f"d={d}" for d in dates)
    data = api_get(f"/batch?{params}")
    if data.get("code") != 0:
        print(f"❌ 服务异常: {data}")
        return

    holiday_data = data.get("holiday", {})
    type_data = data.get("type", {})

    print(f"📋 批量查询 {len(dates)} 个日期:\n")
    for d in dates:
        h = holiday_data.get(d)
        t = type_data.get(d, {})
        print(f"📅 {format_date(d)}")
        if t:
            print(f"   {format_type_info(t)}")
        if h:
            wage = h.get("wage", 1)
            name = h.get("name", "")
            holiday_type = "🎉" if h.get("holiday") else "🔧"
            print(f"   {holiday_type} {name} 薪资×{wage}")
        else:
            print("   普通日期")
        print()


def cmd_next(date_str: str = None, include_type: bool = False, include_week: bool = False):
    """查询下一个节假日"""
    target = f"/{date_str}" if date_str else ""
    params = []
    if include_type:
        params.append("type=Y")
    if include_week:
        params.append("week=Y")
    query = ("?" + "&".join(params)) if params else ""
    data = api_get(f"/next{target}{query}")
    if data.get("code") != 0:
        print(f"❌ 服务异常: {data}")
        return

    h = data.get("holiday")
    w = data.get("workday")

    print(f"🔍 从 {format_date(date_str) if date_str else format_date(TODAY_STR)} 起:\n")

    if h:
        rest = h.get("rest", 0)
        print(f"🎉 下一个节假日: {h.get('name')} ({h.get('date')})")
        print(f"   距离还有 {rest} 天，薪资×{h.get('wage', 1)}")
    else:
        print("🎉 未查到下一个节假日")

    if w:
        print(f"\n🔧 调休: {w.get('name')} ({w.get('date')}) 薪资×{w.get('wage', 1)}")


def cmd_workday(date_str: str = None):
    """查询下一个工作日"""
    target = f"/{date_str}" if date_str else ""
    data = api_get(f"/workday/next{target}")
    if data.get("code") != 0:
        print(f"❌ 服务异常: {data}")
        return

    w = data.get("workday")
    if w:
        rest = w.get("rest", 0)
        print(f"💼 下一个工作日: {w.get('date')} ({w.get('name')})")
        print(f"   距离还有 {rest} 天")
        print(f"   {format_type_info(w)}")
    else:
        print("❌ 30天内未找到工作日")


def cmd_year(date_str: str = None, include_type: bool = False, include_week: bool = False):
    """查询全年/全月节假日"""
    target = f"/{date_str}" if date_str else ""
    params = []
    if include_type:
        params.append("type=Y")
    if include_week:
        params.append("week=Y")
    query = ("?" + "&".join(params)) if params else ""
    # 整年需要加 /
    if date_str and len(date_str) == 4:
        target = f"/{date_str}/"
    data = api_get(f"/year{target}{query}")
    if data.get("code") != 0:
        print(f"❌ 服务异常: {data}")
        return

    h = data.get("holiday", {})
    if not h:
        print("❌ 该年份/月份暂无节假日数据")
        return

    print(f"📆 查询结果 ({len(h)} 个节假日):\n")
    for key, info in sorted(h.items()):
        wage = info.get("wage", 1)
        date_full = info.get("date", "")
        name = info.get("name", "")
        holiday_type = "🎉" if info.get("holiday") else "🔧"
        print(f"  {date_full} {holiday_type} {name} 薪资×{wage}")


def cmd_tts(mode: str = "today"):
    """TTS 语音播报"""
    path = {
        "today": "/tts",
        "next": "/tts/next",
        "tomorrow": "/tts/tomorrow",
    }.get(mode, "/tts")

    data = api_get(path)
    if data.get("code") != 0:
        print(f"❌ 服务异常: {data}")
        return

    print(f"🔊 播报内容:\n{data.get('tts', '')}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n可用命令:")
        print("  info [日期]         - 查询指定日期节假日信息（默认今天）")
        print("  batch <日期...>     - 批量查询多个日期")
        print("  next [日期]         - 查询下一个节假日")
        print("  workday [日期]      - 查询下一个工作日")
        print("  year [年份/月份]   - 查询全年/全月节假日")
        print("  tts                - 今日节假日播报")
        print("  tts-next           - 下一个节假日播报")
        print("  tts-tomorrow       - 明日节假日播报")
        print("\n示例:")
        print("  python3 china_holiday.py info 2026-10-01")
        print("  python3 china_holiday.py batch 2026-05-01 2026-06-01")
        print("  python3 china_holiday.py next")
        print("  python3 china_holiday.py year 2026")
        return

    cmd = sys.argv[1].lower()

    if cmd == "info":
        date_arg = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_info(date_arg)
    elif cmd == "batch":
        dates = sys.argv[2:]
        cmd_batch(dates)
    elif cmd == "next":
        date_arg = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_next(date_arg)
    elif cmd == "workday":
        date_arg = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_workday(date_arg)
    elif cmd == "year":
        date_arg = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_year(date_arg)
    elif cmd == "tts":
        cmd_tts("today")
    elif cmd == "tts-next":
        cmd_tts("next")
    elif cmd == "tts-tomorrow":
        cmd_tts("tomorrow")
    else:
        print(f"❌ 未知命令: {cmd}")


if __name__ == "__main__":
    main()
