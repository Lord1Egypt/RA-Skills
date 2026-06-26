#!/usr/bin/env python3
"""
百分比计算器
纯 Python 标准库实现
"""

import argparse
import sys


def calculate_percent(part: float, whole: float, precision: int = 2) -> float:
    """计算 part 占 whole 的百分比"""
    if whole == 0:
        raise ValueError("整体值不能为零")
    return round(part / whole * 100, precision)


def calculate_from_part(part: float, percent: float, precision: int = 2) -> float:
    """已知部分和百分比，求整体 = part / (percent / 100)"""
    if percent == 0:
        raise ValueError("百分比不能为零")
    return round(part / (percent / 100), precision)


def calculate_of_part(whole: float, percent: float, precision: int = 2) -> float:
    """已知整体和百分比，求部分 = whole * (percent / 100)"""
    return round(whole * percent / 100, precision)


def calculate_change(old_val: float, new_val: float, precision: int = 2) -> float:
    """计算增减百分比 = (new - old) / old * 100"""
    if old_val == 0:
        raise ValueError("原始值不能为零")
    return round((new_val - old_val) / old_val * 100, precision)


def format_number(num: float, use_thousands_sep: bool = False) -> str:
    """格式化数字（可选千分位分隔符）"""
    if use_thousands_sep:
        return f"{num:,.2f}"
    return f"{num}"


def main():
    parser = argparse.ArgumentParser(
        description='百分比计算器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s percent 25 200              25 占 200 的百分比
  %(prog)s from-part 50 25            50 是 25%% 时，整体是多少
  %(prog)s of-part 200 25             200 的 25%% 是多少
  %(prog)s change 100 150             从 100 增长到 150 的百分比
  %(prog)s percent 1 3 --precision 4  高精度计算
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # percent: part / whole * 100
    p_percent = subparsers.add_parser('percent', help='计算百分比（A 是 B 的百分之几）')
    p_percent.add_argument('part', type=float, help='部分值')
    p_percent.add_argument('whole', type=float, help='整体值')
    p_percent.add_argument('-p', '--precision', type=int, default=2, help='小数精度')
    p_percent.add_argument('-f', '--formatted', action='store_true', help='格式化数字')

    # from-part: part / (percent/100) = whole
    p_from_part = subparsers.add_parser('from-part', help='已知部分和百分比，求整体')
    p_from_part.add_argument('part', type=float, help='部分值')
    p_from_part.add_argument('percent', type=float, help='百分比')
    p_from_part.add_argument('-p', '--precision', type=int, default=2, help='小数精度')
    p_from_part.add_argument('-f', '--formatted', action='store_true', help='格式化数字')

    # of-part: whole * (percent/100) = part
    p_of_part = subparsers.add_parser('of-part', help='已知整体和百分比，求部分')
    p_of_part.add_argument('whole', type=float, help='整体值')
    p_of_part.add_argument('percent', type=float, help='百分比')
    p_of_part.add_argument('-p', '--precision', type=int, default=2, help='小数精度')
    p_of_part.add_argument('-f', '--formatted', action='store_true', help='格式化数字')

    # change: (new-old)/old * 100
    p_change = subparsers.add_parser('change', help='计算增减百分比')
    p_change.add_argument('old', type=float, help='原始值')
    p_change.add_argument('new', type=float, help='新值')
    p_change.add_argument('-p', '--precision', type=int, default=2, help='小数精度')
    p_change.add_argument('-f', '--formatted', action='store_true', help='格式化数字')

    args = parser.parse_args()

    try:
        if args.command == 'percent':
            result = calculate_percent(args.part, args.whole, args.precision)
            formatted = format_number(result, args.formatted)
            print(f"{formatted}%")

        elif args.command == 'from-part':
            result = calculate_from_part(args.part, args.percent, args.precision)
            formatted = format_number(result, args.formatted)
            print(formatted)

        elif args.command == 'of-part':
            result = calculate_of_part(args.whole, args.percent, args.precision)
            formatted = format_number(result, args.formatted)
            print(formatted)

        elif args.command == 'change':
            result = calculate_change(args.old, args.new, args.precision)
            formatted = format_number(result, args.formatted)
            if result > 0:
                print(f"+{formatted}%")
            else:
                print(f"{formatted}%")

        else:
            parser.print_help()
            sys.exit(1)

    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
