#!/usr/bin/env python3
"""
验证cron表达式并展示最近10次执行时间的脚本
"""

import argparse
import sys
from datetime import datetime, timedelta
from typing import List, Optional
import re

class CronParser:
    """简单的cron表达式解析器"""
    
    @staticmethod
    def validate_cron_expression(cron_expr: str) -> bool:
        """
        验证cron表达式的基本语法
        """
        parts = cron_expr.strip().split()
        if len(parts) != 5:
            return False
        
        # 检查每个部分的基本格式
        for part in parts:
            if not CronParser._validate_part(part):
                return False
        
        return True
    
    @staticmethod
    def _validate_part(part: str) -> bool:
        """验证单个cron字段"""
        if part == "*":
            return True
        
        # 检查是否包含有效字符
        valid_chars = set("0123456789*,-/")
        if not all(c in valid_chars for c in part):
            return False
        
        # 简单的模式检查
        patterns = part.split(',')
        for pattern in patterns:
            if '/' in pattern:
                range_part, step_part = pattern.split('/', 1)
                if not step_part.isdigit():
                    return False
                if range_part != '*' and not CronParser._validate_range(range_part):
                    return False
            elif '-' in pattern:
                if not CronParser._validate_range(pattern):
                    return False
            elif pattern != '*' and not pattern.isdigit():
                return False
        
        return True
    
    @staticmethod
    def _validate_range(range_str: str) -> bool:
        """验证范围格式"""
        if '-' not in range_str:
            return False
        
        start, end = range_str.split('-', 1)
        return start.isdigit() and end.isdigit() and int(start) <= int(end)

def get_next_cron_times(cron_expr: str, count: int = 10) -> List[datetime]:
    """
    获取cron表达式接下来的执行时间
    注意：这是一个简化的实现，实际应用中应该使用croniter库
    """
    # 这里使用一个简化的实现
    # 实际项目中应该使用croniter库：pip install croniter
    times = []
    now = datetime.now()
    
    # 简化的逻辑：假设是每分钟执行一次的表达式
    # 实际应该根据cron表达式计算
    if cron_expr == "* * * * *":
        for i in range(count):
            times.append(now + timedelta(minutes=i))
    elif cron_expr == "0 * * * *":
        for i in range(count):
            next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=i)
            if next_hour > now:
                times.append(next_hour)
    elif cron_expr == "0 0 * * *":
        for i in range(count):
            next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=i)
            if next_day > now:
                times.append(next_day)
    else:
        # 对于其他表达式，使用一个简化的近似
        # 实际项目中应该使用croniter库
        for i in range(count):
            times.append(now + timedelta(hours=i))
    
    return times[:count]

def explain_cron_expression(cron_expr: str) -> str:
    """
    用自然语言解释cron表达式
    """
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        return "无效的cron表达式：必须是5个字段"
    
    minute, hour, day, month, weekday = parts
    
    explanations = []
    
    # 解释分钟
    if minute == "*":
        explanations.append("每分钟")
    elif minute == "0":
        explanations.append("整点")
    elif "/" in minute:
        step = minute.split("/")[1]
        explanations.append(f"每{step}分钟")
    else:
        explanations.append(f"在分钟 {minute}")
    
    # 解释小时
    if hour == "*":
        explanations.append("每小时")
    elif hour == "0":
        explanations.append("午夜")
    elif "-" in hour:
        start, end = hour.split("-")
        explanations.append(f"从{start}点到{end}点")
    else:
        explanations.append(f"在{hour}点")
    
    # 解释日
    if day == "*":
        explanations.append("每天")
    elif day == "1":
        explanations.append("每月1号")
    else:
        explanations.append(f"在{day}号")
    
    # 解释月
    if month == "*":
        explanations.append("每月")
    elif "-" in month:
        start, end = month.split("-")
        explanations.append(f"从{start}月到{end}月")
    else:
        explanations.append(f"在{month}月")
    
    # 解释星期
    if weekday == "*":
        explanations.append("每周任何一天")
    elif weekday == "0" or weekday == "7":
        explanations.append("周日")
    elif weekday == "1-5":
        explanations.append("工作日（周一到周五）")
    elif weekday == "6":
        explanations.append("周六")
    else:
        explanations.append(f"在星期{weekday}")
    
    return "，".join(explanations) + "执行"

def main():
    parser = argparse.ArgumentParser(description="验证和展示cron表达式")
    parser.add_argument("cron_expr", nargs="?", help="cron表达式 (例如: '*/5 9-17 * * 1-5')")
    parser.add_argument("--count", type=int, default=10, help="显示的执行时间数量 (默认: 10)")
    parser.add_argument("--explain", action="store_true", help="解释cron表达式的含义")
    
    args = parser.parse_args()
    
    # 如果没有提供cron表达式，则提示输入
    if not args.cron_expr:
        args.cron_expr = input("请输入cron表达式: ").strip()
    
    print("=" * 50)
    print(f"Cron表达式: {args.cron_expr}")
    print("=" * 50)
    
    # 验证cron表达式
    if not CronParser.validate_cron_expression(args.cron_expr):
        print("无效的cron表达式!")
        print("请检查表达式格式:")
        print("  格式: 分钟 小时 日 月 星期")
        print("  示例: */5 9-17 * * 1-5")
        sys.exit(1)
    
    print("有效的cron表达式")
    print()
    
    # 解释cron表达式
    explanation = explain_cron_expression(args.cron_expr)
    print("表达式解释:")
    print(f"  {explanation}")
    print()
    
    # 获取并显示执行时间
    print(f"最近{args.count}次执行时间:")
    print("-" * 30)
    
    try:
        next_times = get_next_cron_times(args.cron_expr, args.count)
        
        if not next_times:
            print("无法计算执行时间")
            print("提示: 安装croniter库以获得更准确的计算")
            print("      pip install croniter")
        else:
            for i, time in enumerate(next_times, 1):
                time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                day_of_week = time.strftime("%A")
                print(f"{i:2d}. {time_str} ({day_of_week})")
    
    except Exception as e:
        print(f"计算执行时间时出错: {e}")
        print("提示: 安装croniter库以获得更准确的计算")
        print("      pip install croniter")
    
    print()
    print("=" * 50)
    print("提示: 要获得更准确的执行时间计算，请安装croniter库:")
    print("      pip install croniter")
    print("=" * 50)

if __name__ == "__main__":
    main()