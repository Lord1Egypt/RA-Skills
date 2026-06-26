#!/usr/bin/env python3
# create_reminders.py - 从邮件创建提醒事项
# 用法: echo '[邮件JSON]' | ./create_reminders.py

import json
import sys
import re
from datetime import datetime, timedelta
import subprocess

def extract_datetime(text):
    """从文本中提取日期时间信息"""
    if not text:
        return None
    
    text = str(text)
    now = datetime.now()
    
    # 匹配模式
    patterns = [
        # 完整日期时间：2026年3月31日 14:30 或 2026-03-31 14:30
        (r'(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})[日]?\s*(\d{1,2}):(\d{2})', 'full'),
        # X月X日 + 时间：3月31日 下午2点 或 3月31日 14:00
        (r'(\d{1,2})[月](\d{1,2})[日]?\s*(上午|下午|早上|晚上)?\s*(\d{1,2})[:点时](\d{2})?', 'month_day'),
        # 相对日期
        (r'(明天|今天|后天|大后天)\s*(上午|下午|早上|晚上)?\s*(\d{1,2})[:点时](\d{2})?', 'relative'),
        # 周几 + 时间
        (r'(周一|周二|周三|周四|周五|周六|周日|星期[一二三四五六日])\s*(上午|下午|早上|晚上)?\s*(\d{1,2})[:点时](\d{2})?', 'weekday'),
    ]
    
    for pattern, ptype in patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            try:
                if ptype == 'full':
                    year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                    hour, minute = int(groups[3]), int(groups[4])
                    return datetime(year, month, day, hour, minute)
                    
                elif ptype == 'month_day':
                    month, day = int(groups[0]), int(groups[1])
                    year = now.year
                    if month < now.month or (month == now.month and day < now.day):
                        year += 1
                    
                    hour = int(groups[3]) if groups[3] else 9
                    minute = int(groups[4]) if len(groups) > 4 and groups[4] else 0
                    
                    if groups[2] in ['下午', '晚上'] and hour <= 12:
                        hour += 12
                    
                    return datetime(year, month, day, hour, minute)
                    
                elif ptype == 'relative':
                    day_offset = 0
                    if '明天' in text:
                        day_offset = 1
                    elif '后天' in text:
                        day_offset = 2
                    elif '大后天' in text:
                        day_offset = 3
                    
                    target_date = now + timedelta(days=day_offset)
                    hour = int(groups[2]) if groups[2] else 9
                    minute = int(groups[3]) if len(groups) > 3 and groups[3] else 0
                    
                    if groups[1] in ['下午', '晚上'] and hour <= 12:
                        hour += 12
                    
                    return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                elif ptype == 'weekday':
                    weekday_map = {
                        '周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4, '周六': 5, '周日': 6,
                        '星期一': 0, '星期二': 1, '星期三': 2, '星期四': 3, '星期五': 4, '星期六': 5, '星期日': 6
                    }
                    target_weekday = weekday_map.get(groups[0], 0)
                    
                    days_ahead = target_weekday - now.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    
                    target_date = now + timedelta(days=days_ahead)
                    hour = int(groups[2]) if groups[2] else 9
                    minute = int(groups[3]) if len(groups) > 3 and groups[3] else 0
                    
                    if groups[1] in ['下午', '晚上'] and hour <= 12:
                        hour += 12
                    
                    return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
            except (ValueError, IndexError):
                continue
    
    return None

def create_reminder_with_remindctl(title, notes, due_date):
    """使用 remindctl CLI 创建提醒事项"""
    # 提前2小时提醒
    alarm_date = due_date - timedelta(hours=2)
    
    # 格式化日期
    due_str = due_date.strftime('%Y-%m-%d %H:%M')
    
    # 构建命令
    cmd = [
        'remindctl', 'add',
        '--title', title,
        '--due', due_str,
        '--notes', notes
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    try:
        emails = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("查看邮件数量: 0")
        print("创建提醒数量: 0")
        sys.exit(0)
    
    if not isinstance(emails, list):
        emails = [emails]
    
    created_count = 0
    reminders_created = []
    
    for email in emails:
        subject = email.get('subject', '')
        summary = email.get('summary', '')
        sender = email.get('sender', '')
        
        # 合并主题和摘要来提取时间
        full_text = f"{subject} {summary}"
        event_time = extract_datetime(full_text)
        
        if event_time and event_time > datetime.now():
            # 提取事件标题
            event_title = re.sub(r'(会议|会议通知|邀请|活动|日程|提醒|安排)[：:]?\s*', '', subject)
            if not event_title:
                event_title = subject[:50] if subject else "邮件提醒"
            
            notes = f"来自邮件: {sender}\n\n{summary[:200] if summary else ''}"
            
            if create_reminder_with_remindctl(event_title, notes, event_time):
                created_count += 1
                reminders_created.append({
                    'title': event_title,
                    'time': event_time.strftime('%Y-%m-%d %H:%M')
                })
    
    # 输出结果
    print(f"查看邮件数量: {len(emails)}")
    print(f"创建提醒数量: {created_count}")
    if reminders_created:
        print("\n提醒详情:")
        for r in reminders_created:
            print(f"• {r['title']} - {r['time']}")

if __name__ == '__main__':
    main()
