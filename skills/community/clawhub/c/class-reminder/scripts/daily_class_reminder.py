#!/usr/bin/env python3
"""
daily_class_reminder.py - 每日课程提醒
由 OpenClaw 定时任务调用，查询明天课程并发送提醒
"""

import json
import sys
import os

# 添加 skill 脚本路径
sys.path.insert(0, '/home/admin/.openclaw/workspace/skills/class-reminder/scripts')
from class_reminder import parse_teacher_schedule, get_tomorrows_classes, format_reminder_text

# 配置
SCHEDULE_FILE = '/home/admin/.openclaw/workspace/data/schedule.xlsx'
SEMESTER_START = '2026-03-09'

def main():
    try:
        # 解析课程表
        schedule_data = parse_teacher_schedule(SCHEDULE_FILE, SEMESTER_START)
        
        if schedule_data.get('error'):
            print(f"❌ 解析课程表失败: {schedule_data['error']}")
            return 1
        
        # 获取明天课程
        result = get_tomorrows_classes(schedule_data)
        
        # 生成提醒文本
        reminder_text = format_reminder_text(result)
        
        # 输出提醒（OpenClaw 会捕获并发送）
        print(reminder_text)
        
        return 0
        
    except Exception as e:
        print(f"❌ 查询课程失败: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
