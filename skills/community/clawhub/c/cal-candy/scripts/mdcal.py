#!/usr/bin/env python
"""
MDCal - Markdown Calendar CLI
基于 Markdown 文件的日历系统，供 OpenClaw 调用
"""

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from rich import print

# 配置
CALENDAR_DIR = Path(os.environ.get('MDCAL_DIR', '~/.openclaw/workspace/calendar'))
CALENDAR_DIR = CALENDAR_DIR.expanduser()

# 提醒文件
REMIND_FILE = CALENDAR_DIR / 'reminders.json'

# 确保目录存在
CALENDAR_DIR.mkdir(parents=True, exist_ok=True)


def get_month_file(year: int, month: int) -> Path:
    """获取指定月份的 Markdown 文件路径"""
    return CALENDAR_DIR / f"{year}-{month:02d}.md"


def parse_markdown_events(content: str, year: int, month: int) -> list:
    """解析 Markdown 文件中的事件"""
    events = []
    lines = content.strip().split('\n')
    
    # 匹配格式: - [ ] 2026-03-18 14:00 会议标题 :: 描述 #ab12c
    # 或者: - [x] 2026-03-18 14:00 会议标题 :: 描述 #ab12c
    #pattern = r'^- \[([ x])\] (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})(?: (\w+))?(?: :: (.+?))?(?: #(\w{5}))?$'
    pattern = r'^- \[([ x])\] (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) (.*?)(?: :: (.*?))? #(\w{5})\s*$'
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            done, date, time, title, desc, eid = match.groups()
            events.append({
                'done': done == 'x',
                'date': date,
                'time': time,
                'title': title or '无标题',
                'desc': desc or '',
                'id': eid or '',
                'raw': line.strip()
            })
    
    return events


def write_markdown_events(filepath: Path, events: list):
    """将事件写回 Markdown 文件"""
    lines = ['# 日历\n', '## 事件\n']
    
    # 按日期和时间排序
    sorted_events = sorted(events, key=lambda e: (e['date'], e['time']))
    
    for e in sorted_events:
        done = 'x' if e.get('done') else ' '
        title = e.get('title', '无标题')
        desc = f" :: {e['desc']}" if e.get('desc') else ''
        eid = f" #{e['id']}" if e.get('id') else ''
        line = f"- [{done}] {e['date']} {e['time']} {title}{desc}{eid}\n"
        lines.append(line)
    
    filepath.write_text(''.join(lines), encoding='utf-8')


def add_event(date: str, time: str, title: str, desc: str = ''):
    """添加事件"""
    # 解析日期
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        # 支持相对日期
        if date == 'today':
            dt = datetime.now()
        elif date == 'tomorrow':
            dt = datetime.now() + timedelta(days=1)
        else:
            print(f"错误: 日期格式无效，请使用 YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        date = dt.strftime('%Y-%m-%d')
    
    year, month = dt.year, dt.month
    filepath = get_month_file(year, month)
    
    # 读取现有事件
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
        events = parse_markdown_events(content, year, month)
    else:
        events = []
    
    # 添加新事件
    id = str(uuid.uuid4())[:5]
    events.append({
        'date': date,
        'time': time,
        'title': title,
        'desc': desc,
        'done': False,
        'id': id,
    })
    
    # 写回文件
    write_markdown_events(filepath, events)
    print(f"✓ 已添加: {date} {time} {title}")

    return id


def add_reminder(event_key: str, minutes: int):
    """添加事件提醒"""
    reminders = {}
    if REMIND_FILE.exists():
        with open(REMIND_FILE, 'r', encoding='utf-8') as f:
            reminders = json.load(f)

    reminders[event_key] = minutes

    with open(REMIND_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

    print(f"✓ 已设置提醒: 提前 {minutes} 分钟")


def get_reminder_minutes(event_key: str) -> int:
    """获取事件提醒分钟数"""
    if not REMIND_FILE.exists():
        return 0
    with open(REMIND_FILE, 'r', encoding='utf-8') as f:
        reminders = json.load(f)
    return reminders.get(event_key, 0)


def check_reminders():
    """检查需要提醒的事件，返回需要提醒的事件列表"""
    now = datetime.now()
    to_remind = []

    # 读取提醒设置
    reminders = {}
    if REMIND_FILE.exists():
        with open(REMIND_FILE, 'r', encoding='utf-8') as f:
            reminders = json.load(f)
    
    if not reminders:
        return []
    
    # 遍历所有事件
    for filepath in sorted(CALENDAR_DIR.glob('*.md')):
        year = int(filepath.stem.split('-')[0])
        month = int(filepath.stem.split('-')[1])
        
        if not filepath.name.replace('.md', '').replace(str(year), '').replace('-', '').isdigit():
            continue
            
        content = filepath.read_text(encoding='utf-8')
        events = parse_markdown_events(content, year, month)
        
        for e in events:
            event_key = e['id']

            if not event_key or event_key not in reminders:
                continue

            # 计算事件时间
            event_dt = datetime.strptime(f"{e['date']} {e['time']}", "%Y-%m-%d %H:%M")
            remind_minutes = reminders[event_key]
            remind_time = event_dt - timedelta(minutes=remind_minutes)

            # 检查是否需要提醒 (5分钟窗口)
            if now >= remind_time and now < event_dt:
                to_remind.append({
                    'title': e['title'],
                    'date': e['date'],
                    'time': e['time'],
                    'minutes_before': remind_minutes,
                    'event_key': event_key
                })
    
    return to_remind


def delete_reminder(event_key: str):
    """删除事件提醒"""
    if not REMIND_FILE.exists():
        print(f"错误: 未找到 ID 为 {event_key} 的提醒", file=sys.stderr)
        sys.exit(1)

    with open(REMIND_FILE, 'r', encoding='utf-8') as f:
        reminders = json.load(f)

    if event_key not in reminders:
        print(f"错误: 未找到 ID 为 {event_key} 的提醒", file=sys.stderr)
        sys.exit(1)

    del reminders[event_key]

    with open(REMIND_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

    print(f"✓ 已删除提醒: {event_key}")


def list_reminders():
    """列出所有提醒设置"""
    reminders = {}
    if REMIND_FILE.exists():
        with open(REMIND_FILE, 'r', encoding='utf-8') as f:
            reminders = json.load(f)

    if not reminders:
        print("暂无提醒设置")
        return

    print("📢 提醒设置:")
    for key, minutes in reminders.items():
        print(f"  • {key}: 提前 {minutes} 分钟")


def list_events(month: str = None, show_all: bool = False):
    """列出事件"""
    now = datetime.now()
    events = []
    
    if month:
        # 指定月份
        try:
            if '-' in month:
                year, m = month.split('-')
                files = [get_month_file(int(year), int(m))]
            else:
                files = [get_month_file(now.year, int(month))]
        except:
            print(f"错误: 月份格式无效", file=sys.stderr)
            sys.exit(1)
    else:
        # 所有文件
        files = list(CALENDAR_DIR.glob('*.md'))
    
    for filepath in sorted(files):
        year = int(filepath.stem.split('-')[0])
        month = int(filepath.stem.split('-')[1])
        content = filepath.read_text(encoding='utf-8')
        events.extend(parse_markdown_events(content, year, month))
    
    if not events:
        print("暂无事件")
        return
    
    # 过滤：默认只显示未来事件
    if not show_all:
        today = now.strftime('%Y-%m-%d')
        events = [e for e in events if e['date'] >= today]
    
    # 排序并显示
    events = sorted(events, key=lambda e: (e['date'], e['time']))
    
    current_date = ''
    for e in events:
        if e['date'] != current_date:
            current_date = e['date']
            
            print(f"\n📅 {current_date} ")
            print("-" * 40)
        
        eid = e.get('id') or '00000'
        status = '✅' if e['done'] else '⭕'
        time = e['time']
        title = e['title']
        desc = f" :: {e['desc']}" if e['desc'] else ''
        print(f"  {status} {time} {title}{desc} #{eid}")


def delete_event(event_id: str):
    """删除事件"""
    files = list(CALENDAR_DIR.glob('*.md'))

    for filepath in sorted(files):
        year = int(filepath.stem.split('-')[0])
        month = int(filepath.stem.split('-')[1])
        content = filepath.read_text(encoding='utf-8')
        events = parse_markdown_events(content, year, month)

        for i, e in enumerate(events):
            if e['id'] == event_id:
                del events[i]
                write_markdown_events(filepath, events)
                print(f"✓ 已删除: {e['date']} {e['time']} {e['title']}")
                if REMIND_FILE.exists():
                    with open(REMIND_FILE, 'r', encoding='utf-8') as f:
                        reminders = json.load(f)
                    if event_id in reminders:
                        del reminders[event_id]
                        with open(REMIND_FILE, 'w', encoding='utf-8') as f:
                            json.dump(reminders, f, ensure_ascii=False, indent=2)
                        print(f"✓ 已删除关联提醒: {event_id}")
                return

    print(f"错误: 未找到 ID 为 {event_id} 的事件", file=sys.stderr)
    sys.exit(1)


def view_calendar(year: int = None, month: int = None):
    """以日历视图显示"""
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    
    first_day = datetime(year, month, 1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # 读取当月事件
    filepath = get_month_file(year, month)
    events = {}
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
        for e in parse_markdown_events(content, year, month):
            day = int(e['date'].split('-')[2])
            if day not in events:
                events[day] = []
            events[day].append(e)
    
    # 打印日历
    print(f"\n{'='*38}")
    print(f"  {year}年{month}月")
    print(f"{'='*38}")
    cal_title =" 一  二  三  四  五  六  日"
    print(f"[bold yellow]{cal_title}[/bold yellow]")
    
    # 第一天是周几 (0=周一)
    start_week = first_day.weekday()
    
    # 填充空白
    for _ in range(start_week):
        print("    ", end='')
    
    for day in range(1, last_day.day + 1):
        date = datetime(year, month, day)
        day_str = f"{day:2d}"
        
        if date.date() == now.date():
            marker = f" [bold underline red]{day_str}[/] " if day in events else f"({day_str})"
        elif day in events:
            marker = f" [r]{day_str}[/r] "
        else:
            marker = f" {day_str} "
        
        if date.weekday() in (5, 6):
            marker = f"[pink1]{marker}[/pink1]"
        print(marker, end='')
        
        # 换行
        if (start_week + day) % 7 == 0:
            print()
    
    print("\n")
    
    # 显示当天事件
    if now.year == year and now.month == month:
        print(f"📌 今日事件 ({now.strftime('%Y-%m-%d')}):")
        if now.day in events:
            for e in events[now.day]:
                status = '✅' if e['done'] else '⭕'
                print(f"  {status} {e['time']} {e['title']}")
        else:
            print("  (无)")


def today_events():
    """显示今日事件"""
    now = datetime.now()
    filepath = get_month_file(now.year, now.month)
    
    if not filepath.exists():
        print("今日无事件")
        return
    
    content = filepath.read_text(encoding='utf-8')
    today = now.strftime('%Y-%m-%d')
    events = [e for e in parse_markdown_events(content, now.year, now.month) if e['date'] == today]
    
    if not events:
        print("今日无事件")
        return
    
    print(f"📅 {today} 今日事件:")
    for e in sorted(events, key=lambda x: x['time']):
        status = '✅' if e['done'] else '⭕'
        print(f"  {status} {e['time']} {e['title']}")


def upcoming_events(days: int = 7):
    """显示即将到来的事件"""
    now = datetime.now()
    end_date = now + timedelta(days=days)
    
    all_events = []
    for filepath in sorted(CALENDAR_DIR.glob('*.md')):
        year = int(filepath.stem.split('-')[0])
        month = int(filepath.stem.split('-')[1])
        content = filepath.read_text(encoding='utf-8')
        all_events.extend(parse_markdown_events(content, year, month))
    
    # 过滤未来事件
    events = [e for e in all_events 
              if now.strftime('%Y-%m-%d') <= e['date'] <= end_date.strftime('%Y-%m-%d')]
    
    if not events:
        print(f"未来 {days} 天无事件")
        return
    
    print(f"📆 未来 {days} 天事件:")
    for e in sorted(events, key=lambda x: (x['date'], x['time'])):
        print(f"  ⭕ {e['date']} {e['time']} {e['title']}")


def main():
    parser = argparse.ArgumentParser(description='MDCal - Markdown Calendar CLI')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加事件')
    add_parser.add_argument('date', help='日期 (YYYY-MM-DD 或 today/tomorrow)')
    add_parser.add_argument('time', help='时间 (HH:MM)')
    add_parser.add_argument('title', help='事件标题')
    add_parser.add_argument('desc', nargs='?', default='', help='事件描述')
    add_parser.add_argument('-r', '--remind', type=int, default=0, help='提前提醒分钟数 (如 15, 30, 60)')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出事件')
    list_parser.add_argument('month', nargs='?', help='月份 (YYYY-MM 或 MM)')
    list_parser.add_argument('-a', '--all', action='store_true', help='显示所有事件包括过去')
    
    # delete 命令
    del_parser = subparsers.add_parser('delete', help='删除事件')
    del_parser.add_argument('event_id', type=str, help='事件 ID (5位UUID)')
    
    # view 命令
    view_parser = subparsers.add_parser('view', help='查看日历')
    view_parser.add_argument('year', nargs='?', type=int, help='年份')
    view_parser.add_argument('month', nargs='?', type=int, help='月份')
    
    # today 命令
    subparsers.add_parser('today', help='今日事件')
    
    # upcoming 命令
    up_parser = subparsers.add_parser('upcoming', help='即将到来的事件')
    up_parser.add_argument('-d', '--days', type=int, default=7, help='天数 (默认7)')
    
    # remind 命令
    rem_parser = subparsers.add_parser('remind', help='设置/查看提醒')
    rem_parser.add_argument('event_key', nargs='?', help='事件id (5 chars uuid)')
    rem_parser.add_argument('minutes', type=int, nargs='?', help='提前分钟数')
    
    # remind-del 命令
    remdel_parser = subparsers.add_parser('remind-del', help='删除提醒')
    remdel_parser.add_argument('event_key', help='事件 ID (5位UUID)')

    # check-reminders 命令
    subparsers.add_parser('check', help='检查需要提醒的事件 (供 cron 调用)')
    
    args = parser.parse_args()
    
    if not args.command:
        # 默认显示今日
        today_events()
        return
    
    if args.command == 'add':
        event_key = add_event(args.date, args.time, args.title, args.desc)
        if args.remind > 0 and event_key:
            add_reminder(event_key, args.remind)
    elif args.command == 'list':
        list_events(args.month, args.all)
    elif args.command == 'delete':
        delete_event(args.event_id)
    elif args.command == 'view':
        view_calendar(args.year, args.month)
    elif args.command == 'today':
        today_events()
    elif args.command == 'upcoming':
        upcoming_events(args.days)
    elif args.command == 'remind':
        if args.event_key and args.minutes:
            add_reminder(args.event_key, args.minutes)
        else:
            list_reminders()
    elif args.command == 'remind-del':
        delete_reminder(args.event_key)
    elif args.command == 'check':
        to_remind = check_reminders()
        if to_remind:
            for r in to_remind:
                print(f"🔔 提醒: {r['title']} 于 {r['date']} {r['time']} 开始 (提前 {r['minutes_before']} 分钟)")
        else:
            print("暂无需要提醒的事件")


if __name__ == '__main__':
    main()
