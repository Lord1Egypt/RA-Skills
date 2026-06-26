#!/usr/bin/env python3
"""
统一命令行入口

自动发现 biz/ 下所有业务域，路由到对应的 cmd.py 执行。

用法：python3 scripts/cli.py <业务域> <动作> [--参数名=参数值]

示例：
  python3 scripts/cli.py example your_function --param1=test
"""

import os
import sys
import importlib

_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, _PROJECT_ROOT)

BIZ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biz')


def discover_commands():
    """自动发现 biz/ 下所有包含 cmd.py 的子目录"""
    commands = {}
    if not os.path.isdir(BIZ_DIR):
        return commands
    for name in sorted(os.listdir(BIZ_DIR)):
        cmd_path = os.path.join(BIZ_DIR, name, 'cmd.py')
        if os.path.isfile(cmd_path):
            commands[name] = f"scripts.biz.{name}.cmd"
    return commands


def parse_args(args):
    """解析 --key=value 格式的参数"""
    kwargs = {}
    positional = []
    for arg in args:
        if arg.startswith('--'):
            if '=' in arg:
                key, value = arg[2:].split('=', 1)
                kwargs[key] = value
            else:
                kwargs[arg[2:]] = True
        else:
            positional.append(arg)
    return positional, kwargs


def main():
    commands = discover_commands()

    if len(sys.argv) < 2:
        print("用法：python3 scripts/cli.py <业务域> <动作> [--参数]")
        print()
        print("可用业务域：")
        for name in commands:
            print(f"  - {name}")
        sys.exit(1)

    domain = sys.argv[1]

    if domain not in commands:
        print(f"❌ 未知业务域：{domain}")
        print(f"可用业务域：{', '.join(commands.keys())}")
        sys.exit(1)

    if len(sys.argv) < 3:
        print(f"❌ 请指定动作")
        print(f"用法：python3 scripts/cli.py {domain} <动作> [--参数]")
        sys.exit(1)

    action = sys.argv[2]
    positional, kwargs = parse_args(sys.argv[3:])

    # 动态导入对应的 cmd 模块
    try:
        cmd_module = importlib.import_module(commands[domain])
    except ImportError as e:
        print(f"❌ 加载模块失败：{e}")
        sys.exit(1)

    # 查找并调用对应的动作函数
    handler = getattr(cmd_module, action, None)
    if handler is None or not callable(handler):
        print(f"❌ 未知动作：{domain}.{action}")
        # 列出可用动作
        available = [name for name in dir(cmd_module)
                     if not name.startswith('_') and callable(getattr(cmd_module, name))]
        if available:
            print(f"可用动作：{', '.join(available)}")
        sys.exit(1)

    try:
        handler(*positional, **kwargs)
    except TypeError as e:
        print(f"❌ 参数错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
