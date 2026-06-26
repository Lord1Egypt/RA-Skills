#!/usr/bin/env python3
"""
中文倒数日/纪念日计算器 — cn-countdown
用法:
  python3 countdown.py --list
  python3 countdown.py --add "名称" --date "2026-06-07" --tag "考试"
  python3 countdown.py --delete "名称"
  python3 countdown.py --edit "名称" --new-date "2026-06-08"
  python3 countdown.py --to "2026-06-07"
  python3 countdown.py --since "2020-01-01"
"""

import json
import os
import sys
import argparse
from datetime import datetime, date

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
DATA_FILE = os.path.join(WORKSPACE, "countdown.json")

# 颜色定义
C_RESET  = "\033[0m"
C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE   = "\033[94m"
C_PURPLE = "\033[95m"
C_CYAN   = "\033[96m"
C_WHITE  = "\033[97m"
C_BOLD   = "\033[1m"
C_DIM    = "\033[2m"

# 标签颜色
TAG_COLORS = {
    "生日":   C_PURPLE,
    "纪念日": C_RED,
    "考试":   C_YELLOW,
    "节日":   C_CYAN,
    "目标":   C_GREEN,
    "其他":   C_WHITE,
}

MONTH_NAMES = {
    1:"一月",2:"二月",3:"三月",4:"四月",5:"五月",6:"六月",
    7:"七月",8:"八月",9:"九月",10:"十月",11:"十一月",12:"十二月"
}

DAY_NAMES = {
    0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"
}


def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"events": []}


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def today():
    return date.today()


def parse_date(s):
    """解析 YYYY-MM-DD 格式"""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError(f"日期格式不正确: {s}，请使用 YYYY-MM-DD")


def parse_ymd(s):
    """解析纯 YYYY-MM 格式（月/日不足补1）"""
    for fmt in ("%Y-%m", "%Y/%m"):
        try:
            dt = datetime.strptime(s.strip(), fmt)
            return dt.replace(day=1).date()
        except ValueError:
            pass
    raise ValueError(f"日期格式不正确: {s}")


def lunar_check(date_str):
    """检测是否像农历生日（只给月日，如 05-20）"""
    if len(date_str) <= 5 and date_str.count("-") == 1:
        return True
    if len(date_str) <= 5 and date_str.count("/") == 1:
        return True
    return False


def format_weekday(d):
    wd = d.weekday()
    return DAY_NAMES[wd]


def format_full_date(d):
    return f"{d.year}年{d.month}月{d.day}日"


def format_chinese_date(d):
    return f"{d.year}年{MONTH_NAMES[d.month]}{d.day}日"


def days_diff(d1, d2):
    return (d2 - d1).days


def add_event(name, date_str, tag="其他", note=""):
    """添加一个日子"""
    data = load()

    # 检查重复
    for ev in data["events"]:
        if ev["name"] == name:
            print(f"\n⚠️  「{name}」已存在，使用 --edit 或 --delete 管理")
            return

    target_date = parse_date(date_str)

    event = {
        "name": name,
        "date": date_str.strip(),
        "tag": tag,
        "note": note,
        "added": today().isoformat()
    }
    data["events"].append(event)
    save(data)

    t = target_date
    weekday = format_weekday(t)
    chinese_date = format_chinese_date(t)
    print(f"\n✅ 已添加「{C_BOLD}{C_CYAN}{name}{C_RESET}」")
    print(f"   📅 {t.year}年{MONTH_NAMES[t.month]}{t.day}日 {weekday}")
    print(f"   🏷️  {tag} | 添加于 {today().isoformat()}")

    # 立即显示倒计时
    display_single(event, brief=True)


def display_single(event, brief=False):
    """展示单个事件的倒计时/已过"""
    try:
        target = parse_date(event["date"])
    except ValueError:
        print(f"  ⚠️  日期格式有误: {event['date']}")
        return

    diff = days_diff(today(), target)
    tag = event.get("tag", "其他")
    tag_color = TAG_COLORS.get(tag, C_WHITE)

    if diff == 0:
        status = f"{C_BOLD}{C_GREEN}🎉 今天就是这一天！{C_RESET}"
    elif diff == 1:
        status = f"{C_YELLOW}⏳ 明天就是这一天！{C_RESET}"
    elif diff == -1:
        status = f"{C_BLUE}🕐 昨天是这一天{C_RESET}"
    elif diff > 0:
        years = diff // 365
        months = (diff % 365) // 30
        days_left = diff % 30
        if years > 0:
            time_str = f"{years}年{months}月" if months > 0 else f"{years}年"
        elif months > 0:
            time_str = f"{months}个月{days_left}天" if days_left > 0 else f"{months}个月"
        else:
            time_str = f"{diff}天"
        status = f"{C_BOLD}{C_RED}倒计时 {diff} 天{C_RESET}（约 {time_str}）"
    else:
        past_days = abs(diff)
        years = past_days // 365
        months = (past_days % 365) // 30
        days_left = past_days % 30
        if years > 0:
            time_str = f"{years}年{months}月" if months > 0 else f"{years}年"
        elif months > 0:
            time_str = f"{months}个月{days_left}天" if days_left > 0 else f"{months}个月"
        else:
            time_str = f"{past_days}天"
        status = f"{C_GREEN}已过去 {past_days} 天{C_RESET}（约 {time_str}）"

    if brief:
        print(f"   {status}")
    else:
        target = parse_date(event["date"])
        print(f"\n  {C_BOLD}{tag_color}【{event['name']}】{C_RESET}")
        print(f"  📅 {format_full_date(target)} {format_weekday(target)}")
        print(f"  🏷️  {tag_color}{tag}{C_RESET}  {status}")
        if event.get("note"):
            print(f"  📝 {event['note']}")


def list_events(sort_by="countdown"):
    """列出所有日子"""
    data = load()
    if not data["events"]:
        print(f"\n{C_DIM}还没有记录任何日子~{C_RESET}")
        print(f"   使用 {C_CYAN}--add \"名称\" --date \"YYYY-MM-DD\"{C_RESET} 添加第一个！")
        print()
        return

    events = data["events"]

    # 计算倒计时并排序
    def get_diff(ev):
        try:
            return days_diff(today(), parse_date(ev["date"]))
        except ValueError:
            return 999999

    if sort_by == "countdown":
        events = sorted(events, key=get_diff)
    elif sort_by == "name":
        events = sorted(events, key=lambda x: x["name"])

    # 标题
    today_d = today()
    print(f"\n{C_BOLD}{'='*50}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  📅 倒数日历  |  今天是 {today_d.year}年{today_d.month}月{today_d.day}日 "
          f"{format_weekday(today_d)}{C_RESET}")
    print(f"{C_BOLD}{'='*50}{C_RESET}\n")

    # 分区：已过 / 即将到来 / 未来
    upcoming = []
    past = []
    today_events = []

    for ev in events:
        try:
            diff = days_diff(today(), parse_date(ev["date"]))
        except ValueError:
            continue
        if diff == 0:
            today_events.append(ev)
        elif diff > 0:
            upcoming.append((ev, diff))
        else:
            past.append((ev, abs(diff)))

    # 今日
    if today_events:
        print(f"{C_BOLD}{C_GREEN}🎉 今天！{C_RESET}")
        for ev in today_events:
            display_single(ev)

    # 即将到来（30天内）
    upcoming_30 = [(ev, d) for ev, d in upcoming if d <= 30]
    if upcoming_30:
        print(f"\n{C_BOLD}{C_YELLOW}⏳ 即将到来（30天内）{'='*20}{C_RESET}")
        for ev, diff in upcoming_30:
            tag_color = TAG_COLORS.get(ev.get("tag", "其他"), C_WHITE)
            bar = "█" * min(diff, 30)
            print(f"  {tag_color}●{C_RESET} {C_BOLD}{ev['name']}{C_RESET}"
                  f"  {C_RED}倒计时 {diff} 天{C_RESET}  [{bar}{' '*(30-len(bar))}]")
        print()

    # 全部倒计时（未来）
    if upcoming:
        print(f"\n{C_BOLD}{C_BLUE}📆 未来倒计时{'='*27}{C_RESET}")
        print(f"  {'名称':<12} {'目标日期':<14} {'倒计时':>6}  {'标签'}")
        print(f"  {'-'*12} {'-'*14} {'-'*6}  {'-'*6}")
        for ev, diff in upcoming:
            try:
                t = parse_date(ev["date"])
            except ValueError:
                continue
            tag_color = TAG_COLORS.get(ev.get("tag", "其他"), C_WHITE)
            tag = ev.get("tag", "其他")
            print(f"  {C_BOLD}{ev['name']:<12}{C_RESET} {t.isoformat()}  {C_RED}{diff:>5}天{C_RESET}  {tag_color}{tag}{C_RESET}")
        print()

    # 已过去
    if past:
        print(f"\n{C_BOLD}{C_GREEN}📆 已过去{'='*30}{C_RESET}")
        print(f"  {'名称':<12} {'日期':<14} {'已过':>6}  {'标签'}")
        print(f"  {'-'*12} {'-'*14} {'-'*6}  {'-'*6}")
        for ev, diff in past:
            try:
                t = parse_date(ev["date"])
            except ValueError:
                continue
            tag_color = TAG_COLORS.get(ev.get("tag", "其他"), C_WHITE)
            tag = ev.get("tag", "其他")
            print(f"  {C_BOLD}{ev['name']:<12}{C_RESET} {t.isoformat()}  {C_GREEN}{diff:>5}天{C_RESET}  {tag_color}{tag}{C_RESET}")
        print()

    # 统计
    print(f"{C_BOLD}{'─'*50}{C_RESET}")
    print(f"  共 {len(events)} 个记录  |  "
          f"{C_GREEN}已过 {len(past)} 个{C_RESET}  |  "
          f"{C_RED}即将 {len(upcoming)} 个{C_RESET}")


def delete_event(name):
    """删除一个日子"""
    data = load()
    for i, ev in enumerate(data["events"]):
        if ev["name"] == name:
            data["events"].pop(i)
            save(data)
            print(f"\n🗑️  已删除「{C_BOLD}{C_YELLOW}{name}{C_RESET}」")
            return
    print(f"\n⚠️  未找到「{name}」，使用 --list 查看所有记录")


def edit_event(name, new_date=None, new_name=None, new_tag=None, new_note=None):
    """编辑一个日子"""
    data = load()
    for ev in data["events"]:
        if ev["name"] == name:
            if new_name:
                ev["name"] = new_name
            if new_date:
                ev["date"] = new_date.strip()
            if new_tag:
                ev["tag"] = new_tag
            if new_note:
                ev["note"] = new_note
            save(data)
            print(f"\n✏️  已更新「{C_BOLD}{C_CYAN}{ev['name']}{C_RESET}」")
            display_single(ev)
            return
    print(f"\n⚠️  未找到「{name}」")


def quick_to(target_date_str):
    """快速计算从今天到某天"""
    target = parse_date(target_date_str)
    diff = days_diff(today(), target)
    print(f"\n{C_BOLD}📅 距离 {target.year}年{target.month}月{target.day}日 "
          f"{format_weekday(target)} {C_RESET}")
    if diff == 0:
        print(f"   {C_BOLD}{C_GREEN}🎉 今天！{C_RESET}")
    elif diff > 0:
        years = diff // 365
        months = (diff % 365) // 30
        days = diff % 30
        parts = []
        if years: parts.append(f"{years}年")
        if months: parts.append(f"{months}个月")
        if days or not parts: parts.append(f"{days}天")
        time_str = "".join(parts)
        print(f"   {C_RED}{C_BOLD}倒计时 {diff} 天{C_RESET}")
        print(f"   约 {time_str}（{diff}天）")
    else:
        past = abs(diff)
        print(f"   {C_GREEN}已过去 {past} 天{C_RESET}")


def quick_since(start_date_str):
    """快速计算从某天到今天"""
    start = parse_date(start_date_str)
    diff = days_diff(start, today())
    print(f"\n{C_BOLD}📅 从 {start.year}年{start.month}月{start.day}日 "
          f"{format_weekday(start)} 到今天{C_RESET}")
    years = diff // 365
    months = (diff % 365) // 30
    days = diff % 30
    parts = []
    if years: parts.append(f"{years}年")
    if months: parts.append(f"{months}个月")
    if days or not parts: parts.append(f"{days}天")
    time_str = "".join(parts)
    print(f"   {C_GREEN}{C_BOLD}已过去 {diff} 天{C_RESET}")
    print(f"   约 {time_str}")


def print_help():
    print("""
╔══════════════════════════════════════════════════════╗
║          📅  CN Countdown — 倒数日/纪念日计算器       ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  查看列表:     --list                                ║
║  添加日子:     --add "名称" --date "YYYY-MM-DD"      ║
║                --tag "生日/纪念日/考试/节日/目标/其他" ║
║                --note "备注"                         ║
║                                                      ║
║  删除日子:     --delete "名称"                        ║
║  编辑日子:     --edit "名称" --new-date "YYYY-MM-DD"  ║
║                                                      ║
║  快速倒计时:   --to "YYYY-MM-DD"                     ║
║  快速已过:     --since "YYYY-MM-DD"                   ║
║                                                      ║
║  示例:                                                 ║
║  python3 countdown.py --add "高考" --date "2026-06-07" --tag "考试"║
║  python3 countdown.py --add "在一起" --date "2020-09-01" --tag "纪念日"║
║  python3 countdown.py --list                         ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--add", dest="add_name", help="添加日子名称")
    parser.add_argument("--date", dest="date", help="目标日期 YYYY-MM-DD")
    parser.add_argument("--tag", dest="tag", default="其他",
                        help="标签: 生日/纪念日/考试/节日/目标/其他")
    parser.add_argument("--note", dest="note", default="", help="备注")
    parser.add_argument("--list", dest="list", action="store_true", help="列出所有日子")
    parser.add_argument("--delete", dest="delete", help="删除日子")
    parser.add_argument("--edit", dest="edit", help="编辑日子名称")
    parser.add_argument("--new-date", dest="new_date", help="新日期")
    parser.add_argument("--new-name", dest="new_name", help="新名称")
    parser.add_argument("--new-tag", dest="new_tag", help="新标签")
    parser.add_argument("--to", dest="to_date", help="快速倒计时到某天")
    parser.add_argument("--since", dest="since_date", help="快速计算从某天到今天")
    parser.add_argument("--help", dest="help", action="store_true")

    args = parser.parse_args()

    if args.help:
        print_help()
        return

    # 快速倒计时
    if args.to_date:
        try:
            quick_to(args.to_date)
        except ValueError as e:
            print(f"⚠️  {e}")
        return

    # 快速已过
    if args.since_date:
        try:
            quick_since(args.since_date)
        except ValueError as e:
            print(f"⚠️  {e}")
        return

    # 添加
    if args.add_name:
        if not args.date:
            print("⚠️  添加日子需要 --date 参数，格式：YYYY-MM-DD")
            return
        try:
            add_event(args.add_name, args.date, args.tag, args.note)
        except ValueError as e:
            print(f"⚠️  {e}")
        return

    # 删除
    if args.delete:
        delete_event(args.delete)
        return

    # 编辑
    if args.edit:
        edit_event(args.edit, args.new_date, args.new_name, args.new_tag, args.note)
        return

    # 列出
    if args.list:
        list_events()
        return

    # 默认：列出
    list_events()


if __name__ == "__main__":
    main()
