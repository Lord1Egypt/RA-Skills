#!/usr/bin/env python3
"""
Feishu Agent Team - CLI 入口
"""

import os
import sys
import argparse

# 添加 src 目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.routing import TeamRouter, route_task


def cmd_route(args):
    """测试路由"""
    router = TeamRouter(args.config)
    specialist = router.route_task(args.task)
    print(f"任务 '{args.task}' → {specialist or 'Coordinator（默认）'}")
    return 0


def cmd_info(args):
    """显示团队信息"""
    router = TeamRouter(args.config)
    
    coord = router.get_coordinator_info()
    print("=" * 50)
    print("调度中心:", coord.get('name', 'N/A'))
    print("描述:", coord.get('description', 'N/A'))
    print("-" * 50)
    print("专家团队:")
    for spec in router.get_all_specialists():
        print(f"  [{spec['name']}] {spec['description']}")
        print(f"    关键词: {', '.join(spec['keywords'][:5])}...")
    print("=" * 50)
    return 0


def cmd_init(args):
    """初始化项目"""
    print("Feishu Agent Team 初始化完成")
    print("请编辑 config/team.yaml 自定义团队")
    return 0


def main():
    parser = argparse.ArgumentParser(description='Feishu Agent Team CLI')
    parser.add_argument('--config', help='配置文件路径')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    # route 子命令
    p_route = subparsers.add_parser('route', help='测试任务路由')
    p_route.add_argument('task', help='任务文本')
    p_route.set_defaults(func=cmd_route)
    
    # info 子命令
    p_info = subparsers.add_parser('info', help='显示团队信息')
    p_info.set_defaults(func=cmd_info)
    
    # init 子命令
    p_init = subparsers.add_parser('init', help='初始化')
    p_init.set_defaults(func=cmd_init)
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
