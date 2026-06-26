#!/usr/bin/env python3
"""
法院开庭日历创建脚本
用法: python3 create_court_calendar.py <案号> <案由> <YYYY-MM-DD HH:MM> <地点> [日历名称] [PDF链接]

示例:
  python3 create_court_calendar.py '（2026）沪01民初1234号' '民间借贷纠纷' '2026-04-24 10:00' '上海市第一中级人民法院 第八法庭' 'http://example.com/notice.pdf'
"""

import sys
import os
import hashlib
import subprocess
import tempfile


def create_court_calendar(case_no, case_type, hearing_time, location, calendar_name="工作", pdf_url=None):
    """
    1. AppleScript创建日历事件（直接写指定日历，无弹窗）
       - summary: 开庭：{案由}
       - description: 案号 - 案由 - 开庭地点（不含链接，纯文本）
       - url: PDF链接（如有）
       - location: 开庭地点
    2. launchd plist设置提前1天提醒（系统通知中心）
    """

    from datetime import datetime, timedelta

    # 解析时间
    start_dt = datetime.strptime(hearing_time, "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(hours=2)
    alarm_dt = start_dt - timedelta(days=1)

    start_str = start_dt.strftime("%Y年%m月%d日 %H:%M:%S")
    end_str = end_dt.strftime("%Y年%m月%d日 %H:%M:%S")

    # description不含URL，保持纯净
    desc = f"案号：{case_no} - 案由：{case_type} - 开庭地点：{location}"

    # 构建AppleScript，URL单独处理
    if pdf_url:
        script = f'''tell application "Calendar"
    tell calendar "{calendar_name}"
        make new event at end with properties {{summary:"⚖️ 开庭：{case_type}", start date:date "{start_str}", end date:date "{end_str}", description:"{desc}", location:"{location}", url:"{pdf_url}"}}
    end tell
end tell'''
    else:
        script = f'''tell application "Calendar"
    tell calendar "{calendar_name}"
        make new event at end with properties {{summary:"⚖️ 开庭：{case_type}", start date:date "{start_str}", end date:date "{end_str}", description:"{desc}", location:"{location}"}}
    end tell
end tell'''

    # 写入临时scpt文件（避免多行-e转义问题）
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False, encoding='utf-8')
    f.write(script)
    f.close()

    result = subprocess.run(['osascript', f.name], capture_output=True, text=True)
    subprocess.run(['rm', '-f', f.name])

    if result.returncode != 0:
        print(f"AppleScript error: {result.stderr}")
        return False

    # 创建launchd plist（提前1天提醒）
    uid_hash = hashlib.md5(case_no.encode()).hexdigest()[:8]
    plist_path = os.path.expanduser(f"~/Library/LaunchAgents/com.mm.court-{uid_hash}.plist")

    notification_text = f"⚖️ 明日上午{start_dt.strftime('%H点%M分')}开庭：{case_type}\\n案号：{case_no}\\n地点：{location}"

    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mm.court-{uid_hash}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/osascript</string>
        <string>-e</string>
        <string>display notification "{notification_text}" with title "开庭提醒"</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>{start_dt.hour}</integer>
        <key>Minute</key>
        <integer>{start_dt.minute}</integer>
        <key>Month</key>
        <integer>{alarm_dt.month}</integer>
        <key>Day</key>
        <integer>{alarm_dt.day}</integer>
    </dict>
</dict>
</plist>'''

    os.makedirs(os.path.dirname(plist_path), exist_ok=True)
    with open(plist_path, 'w') as f:
        f.write(plist_content)

    subprocess.run(['launchctl', 'load', plist_path], capture_output=True)

    return True


def delete_court_events(case_no, calendar_name="工作"):
    """根据案号删除旧的开庭事件（用于重建前清理）"""
    script = f'''tell application "Calendar"
    set calEvents to every event of calendar "{calendar_name}" whose description contains "{case_no}"
    repeat with evt in calEvents
        delete evt
    end repeat
end tell'''

    f = tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False, encoding='utf-8')
    f.write(script)
    f.close()

    result = subprocess.run(['osascript', f.name], capture_output=True, text=True)
    subprocess.run(['rm', '-f', f.name])
    return result.returncode == 0


def main():
    if len(sys.argv) < 5:
        print("用法: python3 create_court_calendar.py <案号> <案由> <YYYY-MM-DD HH:MM> <地点> [日历名称] [PDF链接]")
        print("示例: python3 create_court_calendar.py '（2026）沪01民初1234号' '民间借贷纠纷' '2026-04-24 10:00' '上海市第一中级人民法院 第八法庭' '工作' 'http://example.com/notice.pdf'")
        sys.exit(1)

    case_no = sys.argv[1]
    case_type = sys.argv[2]
    hearing_time = sys.argv[3]
    location = sys.argv[4]
    calendar_name = sys.argv[5] if len(sys.argv) > 5 else "工作"
    pdf_url = sys.argv[6] if len(sys.argv) > 6 else None

    success = create_court_calendar(case_no, case_type, hearing_time, location, calendar_name, pdf_url)

    if success:
        print(f"✅ 日历已创建")
        print(f"📅 ⚖️ 开庭：{case_type}")
        print(f"📍 {location}")
        print(f"🕙 {hearing_time}")
        if pdf_url:
            print(f"🔗 {pdf_url}")
        print(f"⏰ 提前1天提醒")


if __name__ == "__main__":
    main()
