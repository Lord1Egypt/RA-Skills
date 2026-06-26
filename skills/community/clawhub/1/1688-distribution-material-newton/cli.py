#!/usr/bin/env python3
"""
1688-distribution-material-newton — 1688 素材优化 CLI 统一入口

用法：
    python3 cli.py <command> [options]                        # capabilities 模式
    python3 cli.py <domain> <action> [--key=value]            # biz 域模式

Commands（capabilities 模式，更多参数见项目根目录 SKILL.md）:
    configure       配置 AK              cli.py configure YOUR_AK
    image_info      获取商品主图          cli.py image_info --offer_id 123456
    image_optimize  图片优化（AI 生图）    cli.py image_optimize --image_urls "url" --prompt "优化主图"
    cutout_image    抠图（生成白底图）     cli.py cutout_image --image_urls "url"
    title_optimize  标题优化              cli.py title_optimize --offer_id 123456 --prompt "优化标题"
    selling_point   卖点生成              cli.py selling_point --offer_id 123456 --prompt "生成卖点"

Biz 域模式：
    isv_token fetch  --app_key=YOUR_KEY    获取 ISV Token
    isv_token status --app_key=YOUR_KEY    查询 ISV Token 状态

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SCRIPTS_DIR)

BIZ_DIR = os.path.join(SCRIPTS_DIR, "biz")


def _discover_capabilities() -> dict:
    """扫描 biz/*/cmd.py，自动注册命令（含 COMMAND_NAME 的模块）"""
    commands = {}

    if not os.path.isdir(BIZ_DIR):
        return commands

    for name in sorted(os.listdir(BIZ_DIR)):
        cmd_path = os.path.join(BIZ_DIR, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = f"biz.{name}.cmd"
        try:
            mod = importlib.import_module(module_path)
            # 只注册有 COMMAND_NAME 的模块为顶层命令
            cmd_name = getattr(mod, 'COMMAND_NAME', None)
            if cmd_name:
                commands[cmd_name] = module_path
        except Exception:
            pass

    return commands


def _discover_biz_domains() -> dict:
    """扫描 biz/*/cmd.py，注册没有 COMMAND_NAME 的业务域（避免与 capabilities 命令重复）"""
    domains = {}
    if not os.path.isdir(BIZ_DIR):
        return domains
    for name in sorted(os.listdir(BIZ_DIR)):
        cmd_path = os.path.join(BIZ_DIR, name, 'cmd.py')
        if os.path.isfile(cmd_path):
            # 跳过有 COMMAND_NAME 的模块（已被 _discover_capabilities 注册）
            module_path = f"biz.{name}.cmd"
            try:
                mod = importlib.import_module(module_path)
                if getattr(mod, 'COMMAND_NAME', None):
                    continue
            except Exception:
                pass
            domains[name] = f"scripts.biz.{name}.cmd"
    return domains


def _parse_biz_args(args):
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


def _usage(commands: dict, domains: dict):
    lines = ["**1688-distribution-material-newton 素材优化工具**\n", "```"]

    if commands:
        lines.append("== Capabilities ==")
        for name in sorted(commands):
            try:
                mod = importlib.import_module(commands[name])
                desc = getattr(mod, 'COMMAND_DESC', '')
                lines.append(f"python3 cli.py {name:<20} {desc}")
            except Exception:
                lines.append(f"python3 cli.py {name}")

    if domains:
        lines.append("")
        lines.append("== Biz 域 ==")
        for name in sorted(domains):
            lines.append(f"python3 cli.py {name} <action> [--key=value]")

    lines.append("```")

    print(json.dumps({
        "success": False,
        "data": {},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))


def main():
    commands = _discover_capabilities()
    domains = _discover_biz_domains()

    if len(sys.argv) < 2:
        _usage(commands, domains)
        sys.exit(1)

    cmd = sys.argv[1]

    # 优先匹配 capabilities 命令
    if cmd in commands:
        module_path = commands[cmd]
        sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]
        module = importlib.import_module(module_path)
        module.main()
    # 其次匹配 biz 域
    elif cmd in domains:
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "data": {},
                "markdown": f"❌ 请指定动作\n\n用法：`python3 cli.py {cmd} <动作> [--参数]`",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        action = sys.argv[2]
        positional, kwargs = _parse_biz_args(sys.argv[3:])

        try:
            cmd_module = importlib.import_module(domains[cmd])
        except ImportError as e:
            print(json.dumps({
                "success": False,
                "data": {},
                "markdown": f"❌ 加载模块失败：{e}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        handler = getattr(cmd_module, action, None)
        if handler is None or not callable(handler):
            # 只展示在该模块中定义的函数，排除 import 进来的
            available = [name for name in dir(cmd_module)
                         if not name.startswith('_') and callable(getattr(cmd_module, name))
                         and getattr(getattr(cmd_module, name), '__module__', '') == cmd_module.__name__]
            print(json.dumps({
                "success": False,
                "data": {},
                "markdown": f"❌ 未知动作：{cmd}.{action}\n\n可用动作：{', '.join(available) if available else '无'}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        try:
            handler(*positional, **kwargs)
        except TypeError as e:
            print(json.dumps({
                "success": False,
                "data": {},
                "markdown": f"❌ 参数错误：{e}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        _usage(commands, domains)
        sys.exit(1)

    # 每次命令执行后上报埋点，失败不影响主流程
    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass


if __name__ == "__main__":
    main()
