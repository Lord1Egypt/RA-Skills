#!/usr/bin/env python3
"""
飞书日历智能时间推荐算法
基于规则的时间推荐，避开常见繁忙时段
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
import pytz

def parse_time(time_str):
    """解析时间字符串"""
    try:
        # 尝试多种格式
        for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(time_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"无法解析时间格式: {time_str}")
    except Exception as e:
        print(f"时间解析错误: {e}", file=sys.stderr)
        sys.exit(1)

def recommend_times(start_time, end_time, duration_minutes, work_hours=(9, 18)):
    """
    推荐会议时间
    
    参数:
    - start_time: 开始时间范围
    - end_time: 结束时间范围
    - duration_minutes: 会议时长（分钟）
    - work_hours: 工作时间范围 (开始小时, 结束小时)
    """
    recommendations = []
    
    # 转换为本地时区（亚洲/上海）
    tz = pytz.timezone('Asia/Shanghai')
    start = start_time.astimezone(tz) if start_time.tzinfo else tz.localize(start_time)
    end = end_time.astimezone(tz) if end_time.tzinfo else tz.localize(end_time)
    
    # 避免的时间段（常见会议时间）
    avoid_times = [
        ("周一", 9, 10),   # 周一上午站会
        ("周一", 14, 15),  # 周一下午规划会
        ("周五", 16, 18),  # 周五下午复盘
    ]
    
    # 推荐的优先时间段
    preferred_times = [
        ("周二", 10, 12),  # 周二上午
        ("周三", 14, 16),  # 周三下午
        ("周四", 10, 12),  # 周四上午
    ]
    
    current = start
    while current < end:
        # 检查是否在工作时间内
        hour = current.hour
        weekday = current.strftime("%A")
        chinese_weekday = {
            "Monday": "周一", "Tuesday": "周二", "Wednesday": "周三",
            "Thursday": "周四", "Friday": "周五", "Saturday": "周六", "Sunday": "周日"
        }[weekday]
        
        # 跳过非工作时间
        if hour < work_hours[0] or hour >= work_hours[1]:
            current += timedelta(hours=1)
            continue
        
        # 跳过周末
        if weekday in ["Saturday", "Sunday"]:
            current += timedelta(days=1)
            continue
        
        # 检查是否在避免时间段
        avoid = False
        for avoid_day, avoid_start, avoid_end in avoid_times:
            if chinese_weekday == avoid_day and avoid_start <= hour < avoid_end:
                avoid = True
                break
        
        if avoid:
            current += timedelta(hours=1)
            continue
        
        # 计算优先级分数
        priority = 5  # 基础分数
        
        # 增加优先时间段的分数
        for pref_day, pref_start, pref_end in preferred_times:
            if chinese_weekday == pref_day and pref_start <= hour < pref_end:
                priority += 3
        
        # 上午时间段通常更好
        if 9 <= hour < 12:
            priority += 1
        
        # 检查时间是否可用（简单检查）
        end_meeting = current + timedelta(minutes=duration_minutes)
        if end_meeting.hour >= work_hours[1]:
            # 会议结束时间超出工作时间
            current += timedelta(hours=1)
            continue
        
        # 添加到推荐列表
        recommendation = {
            "start_time": current.isoformat(),
            "end_time": end_meeting.isoformat(),
            "priority": priority,
            "weekday": chinese_weekday,
            "time_of_day": "上午" if hour < 12 else "下午"
        }
        
        recommendations.append(recommendation)
        
        # 移动到下一个可能的时间段
        current += timedelta(hours=2)  # 至少间隔2小时
    
    # 按优先级排序
    recommendations.sort(key=lambda x: x["priority"], reverse=True)
    
    return recommendations[:5]  # 返回前5个推荐

def main():
    parser = argparse.ArgumentParser(description="飞书日历智能时间推荐")
    parser.add_argument("--start", required=True, help="开始时间 (格式: YYYY-MM-DDTHH:MM:SS)")
    parser.add_argument("--end", required=True, help="结束时间 (格式: YYYY-MM-DDTHH:MM:SS)")
    parser.add_argument("--duration", type=int, default=60, help="会议时长（分钟）")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="输出格式")
    
    args = parser.parse_args()
    
    # 解析时间
    start_time = parse_time(args.start)
    end_time = parse_time(args.end)
    
    # 获取推荐
    recommendations = recommend_times(start_time, end_time, args.duration)
    
    # 输出结果
    if args.format == "json":
        print(json.dumps({
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations)
        }, ensure_ascii=False, indent=2))
    else:
        print("智能时间推荐结果：")
        print("=" * 50)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['weekday']} {rec['time_of_day']}")
            print(f"   时间: {rec['start_time']} - {rec['end_time']}")
            print(f"   优先级: {'★' * rec['priority']}")
            print()

if __name__ == "__main__":
    main()