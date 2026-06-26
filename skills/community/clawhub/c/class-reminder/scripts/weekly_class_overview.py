#!/usr/bin/env python3
"""
weekly_class_overview.py - 每周课程概览
生成下周（周一至周日）的课程概览
"""

import json
import sys
from datetime import datetime, timedelta

sys.path.insert(0, '/home/admin/.openclaw/workspace/skills/class-reminder/scripts')
from class_reminder import parse_teacher_schedule, get_classes_for_date

SCHEDULE_FILE = '/home/admin/.openclaw/workspace/data/schedule.xlsx'
SEMESTER_START = '2026-03-09'

WEEKDAY_NAMES = {1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'}

def get_next_week_dates():
    """获取下周的日期列表（周一到周日）"""
    today = datetime.now()
    # 找到下周一
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:  # 今天已经是周一，取下周
        days_until_monday = 7
    next_monday = today + timedelta(days=days_until_monday)
    
    # 生成下周每一天的日期
    week_dates = []
    for i in range(7):
        date = next_monday + timedelta(days=i)
        week_dates.append({
            'date': date.strftime('%Y-%m-%d'),
            'weekday': date.isoweekday(),
            'weekday_name': WEEKDAY_NAMES[date.isoweekday()]
        })
    
    return week_dates

def main():
    try:
        # 解析课程表
        schedule_data = parse_teacher_schedule(SCHEDULE_FILE, SEMESTER_START)
        
        if schedule_data.get('error'):
            print(f"❌ 解析课程表失败: {schedule_data['error']}")
            return 1
        
        # 获取下周日期
        week_dates = get_next_week_dates()
        
        # 收集每天的课程
        week_classes = {}
        for day_info in week_dates:
            classes = get_classes_for_date(schedule_data, day_info['date'])
            if classes:
                week_classes[day_info['weekday_name']] = classes
        
        # 生成概览文本
        lines = ["📅 下周课程概览", ""]
        
        if not week_classes:
            lines.append("🎉 下周没有课程安排，好好休息！")
        else:
            for day_name in ['周一', '周二', '周三', '周四', '周五', '周六', '周日']:
                if day_name not in week_classes:
                    continue
                    
                lines.append(f"\n【{day_name}】")
                for i, cls in enumerate(week_classes[day_name], 1):
                    course_title = cls['name']
                    if cls.get('type'):
                        course_title = f"【{cls['type']}】{course_title}"
                    
                    time_range = cls['start_time']
                    if cls.get('end_time'):
                        time_range = f"{cls['start_time']}-{cls['end_time']}"
                    
                    lines.append(f"  {i}. {course_title}")
                    lines.append(f"     ⏰ {time_range}  📍 {cls['location']}")
        
        lines.append("")
        lines.append("🍋 提前规划，高效学习！")
        
        print("\n".join(lines))
        return 0
        
    except Exception as e:
        print(f"❌ 生成概览失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
