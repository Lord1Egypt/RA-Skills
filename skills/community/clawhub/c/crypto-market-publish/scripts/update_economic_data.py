#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济数据实际值更新工具
用于手动更新已发布经济数据的实际值，触发利多利空分析
"""

import sys
import argparse
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace')

from economic_analyzer import EconomicDataAnalyzer


def list_known_events():
    """列出已知的经济数据事件"""
    analyzer = EconomicDataAnalyzer()
    actual_data = analyzer.load_actual_data()

    print("📋 已有实际值的经济数据:")
    print("=" * 80)
    print()

    if not actual_data:
        print("暂无已更新的数据")
        return

    for name, data in actual_data.items():
        print(f"📊 {name}")
        print(f"   实际值: {data.get('actual', 'N/A')}")
        print(f"   更新时间: {data.get('datetime', 'N/A')}")
        print()


def update_actual_value(name: str, actual: str, datetime_str: str = None):
    """更新经济数据的实际值"""
    analyzer = EconomicDataAnalyzer()

    print(f"📝 更新经济数据实际值")
    print("=" * 80)
    print(f"数据名称: {name}")
    print(f"实际值: {actual}")
    print(f"发布时间: {datetime_str or datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # 更新实际值
    analyzer.update_actual_value(name, actual, datetime_str)

    # 生成分析报告
    from economic_calendar import EconomicCalendar
    calendar = EconomicCalendar()

    # 查找对应的事件
    events = calendar.fetch_economic_calendar(days=30)
    matched_event = None

    for event in events:
        if name in event.get('name', ''):
            matched_event = event.copy()
            break

    if matched_event:
        matched_event['actual'] = actual
        print()
        print("📊 影响分析:")
        print("=" * 80)
        print()
        print(analyzer.generate_impact_report(matched_event))
    else:
        print(f"⚠️ 未找到匹配的事件: {name}")
        print("影响分析报告: 无法生成（事件不在预告列表中）")


def analyze_event(name: str, actual: str, expected: str, previous: str):
    """分析经济数据"""
    from economic_analyzer import EconomicDataAnalyzer

    analyzer = EconomicDataAnalyzer()

    event = {
        'name': name,
        'actual': actual,
        'expected': expected,
        'previous': previous
    }

    print("📊 经济数据分析")
    print("=" * 80)
    print()
    print(analyzer.generate_impact_report(event))


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='经济数据实际值更新工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

1. 更新已发布数据的实际值:
   python3 update_economic_data.py update "CPI 消费者价格指数" "2.1%"

2. 指定发布时间:
   python3 update_economic_data.py update "非农就业数据" "+280K" "2026-03-13 21:30"

3. 查看已有数据:
   python3 update_economic_data.py list

4. 直接分析数据（不保存）:
   python3 update_economic_data.py analyze "CPI" "2.1%" "2.3%" "2.4%"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # update 命令
    update_parser = subparsers.add_parser('update', help='更新实际值')
    update_parser.add_argument('name', help='数据名称（如"CPI 消费者价格指数"）')
    update_parser.add_argument('actual', help='实际值（如"2.1%"）')
    update_parser.add_argument('--datetime', help='发布时间（默认为当前时间）')

    # list 命令
    subparsers.add_parser('list', help='列出已有数据')

    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析数据')
    analyze_parser.add_argument('name', help='数据名称')
    analyze_parser.add_argument('actual', help='实际值')
    analyze_parser.add_argument('expected', help='预期值')
    analyze_parser.add_argument('previous', help='前值')

    args = parser.parse_args()

    if args.command == 'update':
        update_actual_value(args.name, args.actual, args.datetime)
    elif args.command == 'list':
        list_known_events()
    elif args.command == 'analyze':
        analyze_event(args.name, args.actual, args.expected, args.previous)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
