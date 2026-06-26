#!/usr/bin/env python3
"""
1688-freedom-query-merchant-data CLI 统一入口

Usage:
    python3 cli.py <command> [options]

Commands:
    rag_query          RAG 语义检索接口文档
    query_shop_data    查询商家经营数据
    configure          配置 AK

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)


def _discover_capabilities() -> dict:
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


def _configure(args: list):
    """配置 AK"""
    from _const import OPENCLAW_CONFIG_PATH

    if not args:
        if OPENCLAW_CONFIG_PATH.exists():
            print(json.dumps({"success": True, "markdown": f"✅ 配置文件存在：{OPENCLAW_CONFIG_PATH}", "data": {}}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, "markdown": f"❌ 配置文件不存在：{OPENCLAW_CONFIG_PATH}\n\n请运行: `cli.py configure YOUR_AK`", "data": {}}, ensure_ascii=False, indent=2))
        return

    ak_value = args[0]
    OPENCLAW_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    config = {}
    if OPENCLAW_CONFIG_PATH.exists():
        try:
            with open(OPENCLAW_CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    config.setdefault("skills", {}).setdefault("entries", {})
    config["skills"]["entries"]["1688-freedom-query-merchant-data"] = {"apiKey": ak_value}

    with open(OPENCLAW_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(json.dumps({"success": True, "markdown": "✅ AK 配置成功", "data": {}}, ensure_ascii=False, indent=2))


def _usage(commands: dict):
    lines = ["用法: python3 cli.py <command> [options]\n", "可用命令:"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append(f"  {name:<20} {desc}")
        except Exception:
            lines.append(f"  {name}")
    lines.append(f"  {'configure':<20} 配置 AK")

    print(json.dumps({
        "success": False,
        "markdown": "\n".join(lines),
        "data": {},
    }, ensure_ascii=False, indent=2))


def main():
    commands = _discover_capabilities()

    if len(sys.argv) < 2:
        _usage(commands)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "configure":
        _configure(sys.argv[2:])
        return

    if cmd not in commands:
        _usage(commands)
        sys.exit(1)

    module_path = commands[cmd]
    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()


if __name__ == "__main__":
    main()
