#!/usr/bin/env python3
"""
时间戳转换工具
纯 Python 标准库实现
"""

import time
import argparse
import sys
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


def get_current_timestamp() -> int:
    """获取当前时间戳（秒）"""
    return int(time.time())


def get_current_timestamp_ms() -> int:
    """获取当前时间戳（毫秒）"""
    return int(time.time() * 1000)


def timestamp_to_datetime(ts: int, tz_name: str = 'Asia/Shanghai') -> datetime:
    """时间戳转日期时间"""
    # 自动判断秒/毫秒
    if ts > 10**10:
        ts = ts / 1000
    dt = datetime.fromtimestamp(ts)
    if tz_name:
        try:
            dt = datetime.fromtimestamp(ts, tz=ZoneInfo(tz_name))
        except Exception:
            pass
    return dt


def datetime_to_timestamp(dt_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> int:
    """日期时间字符串转时间戳"""
    dt = datetime.strptime(dt_str, fmt)
    return int(dt.timestamp())


def format_timestamp(ts: int, fmt: str, tz_name: str = 'Asia/Shanghai') -> str:
    """格式化时间戳"""
    dt = timestamp_to_datetime(ts, tz_name)
    return dt.strftime(fmt)


def main():
    parser = argparse.ArgumentParser(
        description='时间戳转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s now                        当前时间戳（秒）
  %(prog)s now-ms                     当前时间戳（毫秒）
  %(prog)s to-datetime 1714214400     时间戳转日期时间
  %(prog)s to-timestamp "2024-04-27 14:30:00"  日期时间转时间戳
  %(prog)s format 1714214400 "%%Y-%%m-%%d %%H:%%M:%%S"  格式化输出
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # now
    subparsers.add_parser('now', help='获取当前时间戳（秒）')
    subparsers.add_parser('now-ms', help='获取当前时间戳（毫秒）')

    # to-datetime
    p_to_dt = subparsers.add_parser('to-datetime', help='时间戳转日期时间')
    p_to_dt.add_argument('timestamp', type=int, help='Unix 时间戳')
    p_to_dt.add_argument('-z', '--timezone', default='Asia/Shanghai', help='时区')

    # to-timestamp
    p_to_ts = subparsers.add_parser('to-timestamp', help='日期时间转时间戳')
    p_to_ts.add_argument('datetime', help='日期时间字符串')
    p_to_ts.add_argument('-f', '--format', default='%Y-%m-%d %H:%M:%S', help='日期格式')

    # format
    p_fmt = subparsers.add_parser('format', help='格式化时间戳')
    p_fmt.add_argument('timestamp', type=int, help='Unix 时间戳')
    p_fmt.add_argument('format', help='输出格式，如 %Y-%m-%d %H:%M:%S')
    p_fmt.add_argument('-z', '--timezone', default='Asia/Shanghai', help='时区')

    args = parser.parse_args()

    if args.command == 'now':
        print(get_current_timestamp())

    elif args.command == 'now-ms':
        print(get_current_timestamp_ms())

    elif args.command == 'to-datetime':
        dt = timestamp_to_datetime(args.timestamp, args.timezone)
        print(dt.strftime('%Y-%m-%d %H:%M:%S'))

    elif args.command == 'to-timestamp':
        ts = datetime_to_timestamp(args.datetime, args.format)
        print(ts)

    elif args.command == 'format':
        result = format_timestamp(args.timestamp, args.format, args.timezone)
        print(result)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
