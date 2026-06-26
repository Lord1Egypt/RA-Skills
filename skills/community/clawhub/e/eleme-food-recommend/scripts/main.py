#!/usr/bin/env python
"""
饿了么外卖推荐 Skill - 主入口
根据用户饭点和口味偏好推荐外卖
"""
import json
import sys
import argparse
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import load_config, update_config, get_config
from recommend import generate_recommendation, get_meal_time_status


def cmd_set_config(args):
    """设置用户配置"""
    config = {}

    if args.cookie:
        config['cookie'] = args.cookie
    if args.breakfast:
        config['breakfast'] = args.breakfast
    if args.lunch:
        config['lunch'] = args.lunch
    if args.dinner:
        config['dinner'] = args.dinner
    if args.flavor:
        config['flavor'] = args.flavor
    if args.count:
        config['recommend_count'] = args.count
    if args.latitude:
        config['location'] = config.get('location', {})
        config['location']['latitude'] = args.latitude
    if args.longitude:
        config['location'] = config.get('location', {})
        config['location']['longitude'] = args.longitude
    if args.address:
        config['location'] = config.get('location', {})
        config['location']['address'] = args.address

    update_config(**config)

    print(json.dumps({
        "message": "配置已更新",
        "config": get_config()
    }, ensure_ascii=False, indent=2))


def cmd_show_config(args):
    """显示当前配置"""
    config = get_config()

    # 不显示完整cookie，只显示前几位
    if config.get('cookie'):
        config['cookie'] = config['cookie'][:20] + '...' if len(config['cookie']) > 20 else config['cookie']

    print(json.dumps(config, ensure_ascii=False, indent=2))


def cmd_recommend(args):
    """获取推荐"""
    result = generate_recommendation()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_status(args):
    """查看饭点状态"""
    status = get_meal_time_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description='饿了么外卖推荐 Skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  设置配置:
    python scripts/main.py set-config --cookie "your_cookie" --flavor "清淡" --count 3

  查看配置:
    python scripts/main.py show-config

  获取推荐:
    python scripts/main.py recommend

  查看饭点状态:
    python scripts/main.py status
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # set-config 子命令
    set_parser = subparsers.add_parser('set-config', help='设置用户配置')
    set_parser.add_argument('--cookie', help='饿了么Cookie')
    set_parser.add_argument('--breakfast', help='早餐时间，如 07:30')
    set_parser.add_argument('--lunch', help='午餐时间，如 11:30')
    set_parser.add_argument('--dinner', help='晚餐时间，如 18:30')
    set_parser.add_argument('--flavor', help='口味偏好：清淡/微辣/中辣/辣/重口/甜/酸/不限')
    set_parser.add_argument('--count', type=int, help='推荐菜品数量')
    set_parser.add_argument('--latitude', help='纬度')
    set_parser.add_argument('--longitude', help='经度')
    set_parser.add_argument('--address', help='地址描述')
    set_parser.set_defaults(func=cmd_set_config)

    # show-config 子命令
    show_parser = subparsers.add_parser('show-config', help='显示当前配置')
    show_parser.set_defaults(func=cmd_show_config)

    # recommend 子命令
    rec_parser = subparsers.add_parser('recommend', help='获取今日推荐')
    rec_parser.set_defaults(func=cmd_recommend)

    # status 子命令
    status_parser = subparsers.add_parser('status', help='查看饭点状态')
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        # 默认显示配置
        cmd_show_config(args)
        return

    args.func(args)


if __name__ == "__main__":
    main()
