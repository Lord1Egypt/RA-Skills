#!/usr/bin/env python3
"""
1688-product-analysis —— 1688 商品诊断 CLI 统一入口

Usage:
    python3 cli.py <command> [options]   # Windows 上用 python 或 py -3

Commands（更多参数见项目根目录 SKILL.md）:
    alibaba.1688.get.offer.data    获取商品综合数据（基础/表现/货盘/搜推/广告/热搜词/热品 等）

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)


def _force_utf8_stdio():
    """Windows 默认按 GBK 等本地编码输出，非 ASCII 文案会乱码甚至抛 UnicodeEncodeError"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass


def _discover_capabilities() -> dict:
    """扫描 capabilities/*/cmd.py，自动注册命令"""
    commands = {}
    caps_dir = os.path.join(SCRIPTS_DIR, "capabilities")

    if not os.path.isdir(caps_dir):
        return commands

    for name in sorted(os.listdir(caps_dir)):
        cmd_path = os.path.join(caps_dir, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = f"capabilities.{name}.cmd"
        try:
            mod = importlib.import_module(module_path)
            cmd_name = getattr(mod, 'COMMAND_NAME', name)
            commands[cmd_name] = module_path
        except Exception:
            pass

    return commands


def _usage(commands: dict):
    lines = ["**1688-product-analysis 用法**\n", "```"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append(f"python3 cli.py {name:<20} {desc}")
        except Exception:
            lines.append(f"python3 cli.py {name}")
    lines.append("```")

    print(json.dumps({
        "success": False,
        "data": {},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))


def main():
    _force_utf8_stdio()
    commands = _discover_capabilities()

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        _usage(commands)
        sys.exit(1)

    cmd = sys.argv[1]
    module_path = commands[cmd]

    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    try:
        module.main()
    finally:
        # 命令一经分派即尝试上报；埋点失败不覆盖业务命令的返回或异常。
        try:
            from _tracker import report_skill_usage
            report_skill_usage(api_name=cmd)
        except Exception:
            pass


if __name__ == "__main__":
    main()
