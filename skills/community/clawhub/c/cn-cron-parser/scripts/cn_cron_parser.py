#!/usr/bin/env python3
"""
cn-cron-parser - Cron表达式解析工具
"""
import argparse
from datetime import datetime, timedelta

def parse_cron_desc(cron):
    """解析Cron为人类可读描述"""
    parts = cron.strip().split()
    if len(parts) != 5:
        return "无效的Cron表达式（需要5个字段）"
    
    minute, hour, day, month, weekday = parts
    
    desc = []
    
    # 分钟
    if minute == '*':
        desc.append("每分钟")
    elif minute.startswith('*/'):
        interval = minute[2:]
        desc.append(f"每{interval}分钟")
    elif ',' in minute:
        desc.append(f"在第{minute}分钟")
    elif minute == '0':
        pass  # 整点
    else:
        desc.append(f"在{minute}分")
    
    # 小时
    if hour == '*':
        pass
    elif hour.startswith('*/'):
        interval = hour[2:]
        desc.append(f"每{interval}小时")
    elif hour != '*':
        desc.append(f"{hour}点")
    
    # 日期
    if day == '*':
        pass
    elif day != '*':
        desc.append(f"每月{day}号")
    
    # 月份
    month_names = {1:'一月',2:'二月',3:'三月',4:'四月',5:'五月',6:'六月',
                   7:'七月',8:'八月',9:'九月',10:'十月',11:'十一月',12:'十二月'}
    if month == '*':
        pass
    elif month in month_names:
        desc.append(month_names[int(month)])
    
    # 星期
    weekday_names = {0:'周日',1:'周一',2:'周二',3:'周三',4:'周四',5:'周五',6:'周六'}
    if weekday == '*':
        pass
    elif weekday in weekday_names:
        desc.append(weekday_names[int(weekday)])
    
    if not desc:
        return "每分钟"
    
    return ' '.join(desc)

def get_next_run(cron, count=5):
    """计算下次执行时间"""
    try:
        from croniter import croniter
        
        now = datetime.now()
        cron_obj = croniter(cron, now)
        
        results = []
        for i in range(count):
            next_time = cron_obj.get_next(datetime)
            results.append(next_time.strftime('%Y-%m-%d %H:%M:%S (%A)'))
        
        return results
    except ImportError:
        return ["需要安装croniter: pip install croniter"]
    except Exception as e:
        return [f"解析错误: {e}"]

def show_templates():
    """显示常用模板"""
    templates = [
        ("0 9 * * *", "每天早上9点"),
        ("0 9 * * 1-5", "工作日早上9点"),
        ("0 9 * * 0", "每周日早上9点"),
        ("*/15 * * * *", "每15分钟"),
        ("*/30 * * * *", "每30分钟"),
        ("0 * * * *", "每小时"),
        ("0 0 * * *", "每天午夜"),
        ("0 0 * * 0", "每周日午夜"),
        ("0 0 1 * *", "每月1号午夜"),
        ("0 9 1 * *", "每月1号早上9点"),
        ("*/5 * * * *", "每5分钟"),
    ]
    
    print("常用Cron模板：")
    print("-" * 50)
    for cron, desc in templates:
        print(f"{cron:20} {desc}")

def main():
    parser = argparse.ArgumentParser(description='Cron表达式解析工具')
    parser.add_argument('cron', nargs='?', help='Cron表达式')
    parser.add_argument('--next', action='store_true', help='显示下次执行时间')
    parser.add_argument('--templates', action='store_true', help='显示常用模板')
    parser.add_argument('--count', type=int, default=5, help='显示下次执行次数')
    
    args = parser.parse_args()
    
    if args.templates:
        show_templates()
        return
    
    if not args.cron:
        print("用法:")
        print("  python3 cn_cron_parser.py '0 9 * * *'")
        print("  python3 cn_cron_parser.py '0 9 * * *' --next")
        print("  python3 cn_cron_parser.py --templates")
        print("\n格式: 分 时 日 月 周")
        return
    
    print(f"Cron: {args.cron}")
    print(f"描述: {parse_cron_desc(args.cron)}")
    
    if args.next:
        print(f"\n下次执行时间（最近{args.count}次）:")
        for t in get_next_run(args.cron, args.count):
            print(f"  {t}")

if __name__ == '__main__':
    main()