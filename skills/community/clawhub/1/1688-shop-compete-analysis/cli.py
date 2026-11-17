#!/usr/bin/env python3
"""
1688-shop-compete-analysis CLI 统一入口

Usage:
    python3 cli.py <command> [options]

Commands:
    compete_category        竞争分析类目树（cateId 唯一合法来源）
    compete_shop_analysis   初步竞店分析（本店定位+行业排行+流失去向+监控清单）
    compete_shop_drill      竞店结构下钻（核心指标/商品/价格带/词/买家六维）
    compete_offer_drill     竞品（商品级）三维下钻（引流词/流量来源/买家结构）
    customer_loss           买家流失商品分析与竞对对比
    query_shop_data         竞争域裸接口取数（快捷命令未覆盖的维度）
    （其余能力见 capabilities/ 目录，运行时自动发现）

所有能力经 accio-mcp-cli 调用 MCP 工具取数，鉴权由本地网关登录态注入，无需配置 AK。

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

# Windows 中文环境 stdout 默认 cp936，无法编码 ¥ / 📄 / ❌ 等输出字符，
# 不处理会抛 UnicodeEncodeError；入口处统一强制 UTF-8。
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

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


def _usage(commands: dict):
    lines = ["用法: python3 cli.py <command> [options]\n", "可用命令:"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append(f"  {name:<20} {desc}")
        except Exception:
            lines.append(f"  {name}")

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

    if cmd not in commands:
        _usage(commands)
        sys.exit(1)

    module_path = commands[cmd]
    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()


if __name__ == "__main__":
    main()
