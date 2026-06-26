#!/usr/bin/env python3
"""
cn-calendar-manager: 日历事件创建工具
从自然语言描述生成 .ics 日历文件（兼容 Google/Apple/Outlook）
用法: python calendar_manager.py "明天上午10点开会讨论项目进度"
"""

import sys
import re
from datetime import datetime, timedelta
from pathlib import Path


def parse_natural_date(text: str) -> tuple:
    """解析自然语言时间描述，返回(year, month, day, hour, minute, duration_min)"""
    text = text.strip()
    today = datetime.now()

    if '今天' in text:
        base = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif '明天' in text:
        base = today + timedelta(days=1)
        base = base.replace(hour=0, minute=0, second=0, microsecond=0)
    elif '后天' in text:
        base = today + timedelta(days=2)
        base = base.replace(hour=0, minute=0, second=0, microsecond=0)
    elif '下周' in text:
        days = 7 - today.weekday() + (1 if today.weekday() >= 5 else 0)
        base = today + timedelta(days=days)
        base = base.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        base = today.replace(hour=0, minute=0, second=0, microsecond=0)

    # 时间匹配
    hour, minute = 10, 0
    time_pattern = re.findall(r'(\d{1,2})[点时](?:(\d{1,2})分?)?', text)
    if time_pattern:
        hour = int(time_pattern[0][0])
        minute = int(time_pattern[0][1]) if time_pattern[0][1] else 0
        hour = max(0, min(23, hour))
        minute = max(0, min(59, minute))

    # 时长（默认1小时）
    duration = 60
    dur_match = re.search(r'(\d+)\s*(?:小时|小时半|个?小时)', text)
    if dur_match:
        dur_h = int(dur_match.group(1))
        if '半' in text:
            duration = int(dur_h * 60 + 30)
        else:
            duration = dur_h * 60

    # 日期具体指定
    date_pattern = re.findall(r'(\d{1,2})[月/\-](\d{1,2})', text)
    if date_pattern:
        month, day = int(date_pattern[0][0]), int(date_pattern[0][1])
        year = today.year
        if month < today.month:
            year += 1
        base = base.replace(year=year, month=month, day=day)

    return base.year, base.month, base.day, hour, minute, duration


def extract_title(text: str) -> str:
    """从描述中提取事件标题"""
    text = text.strip()
    # 去掉时间前缀
    text = re.sub(r'^(今天|明天|后天|下周)[上午下午晚上早中]?', '', text)
    text = re.sub(r'\d+[点时:分]', '', text)
    text = text.strip()

    # 关键词触发
    keywords = ['会议', '约会', '面试', '演讲', '培训', '讨论', '汇报', '见面', '举行', '开始']
    for kw in keywords:
        if kw in text:
            idx = text.index(kw)
            result = text[idx:].strip()
            return result[:50] if result else "日程事件"

    # 兜底：去掉数字和标点
    result = re.sub(r'[\d\.\,\、\。]+', '', text).strip()
    return result[:30] if result else "日程事件"


def generate_ics(year, month, day, hour, minute, duration_min, title, description="", location=""):
    """生成标准 .ics 文件内容"""
    start = datetime(year, month, day, hour, minute)
    end = start + timedelta(minutes=duration_min)

    dt_start = start.strftime('%Y%m%dT%H%M%S')
    dt_end = end.strftime('%Y%m%dT%H%M%S')
    dt_stamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    uid = f"{hash(title)}{hash(str(start))}@qclaw-calendar"

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//QClaw//CN Calendar Manager//ZH
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dt_stamp}
DTSTART:{dt_start}
DTEND:{dt_end}
SUMMARY:{title}
"""
    if description:
        ics_content += f"DESCRIPTION:{description}\n"
    if location:
        ics_content += f"LOCATION:{location}\n"

    ics_content += """END:VEVENT
END:VCALENDAR"""
    return ics_content


def main():
    if len(sys.argv) < 2:
        print("用法: python calendar_manager.py <自然语言描述>")
        print("示例:")
        print("  python calendar_manager.py \"明天上午10点开会讨论项目\"")
        print("  python calendar_manager.py \"下周一14点进行团队培训\"")
        print("  python calendar_manager.py \"后天上午9点面试候选人张明\"")
        sys.exit(1)

    text = ' '.join(sys.argv[1:])

    try:
        year, month, day, hour, minute, duration = parse_natural_date(text)
        title = extract_title(text)

        ics_content = generate_ics(year, month, day, hour, minute, duration, title)

        date_str = f"{year}{month:02d}{day:02d}"
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)[:20]
        filename = f"calendar_{date_str}_{safe_title}.ics"
        output_path = Path.home() / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ics_content)

        print(f"✅ 日历事件已创建: {output_path}")
        print(f"📅 标题: {title}")
        print(f"🕐 时间: {year}年{month}月{day}日 {hour:02d}:{minute:02d}")
        print(f"⏱️  时长: {duration}分钟")
        print(f"📁 文件: {filename}")
        print(f"\n💡 使用方式:")
        print(f"  - Google Calendar: 导入 .ics 文件")
        print(f"  - Apple Calendar: 双击打开 .ics")
        print(f"  - Outlook: 文件→打开→导入→.ics")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ 解析失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
