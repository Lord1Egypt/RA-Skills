#!/usr/bin/env python3
"""
1688-item-batch-opt-apply —— 1688商品批量优化应用 CLI 统一入口

批量任务编排层：任务解析（上下文/Excel/文件夹）、任务台账、结果落账、
Excel 产物导出、任务确认/结果展示/批量应用三类组件卡片参数构造。
单任务执行与应用写入由主 Agent 委托对应执行技能完成，本 CLI 不直接
调用生图接口、不直接写商品。

Usage:
    python3 cli.py <command> [options]

Commands（更多参数见项目根目录 SKILL.md）:
    parse_tasks         解析批量任务（上下文/Excel/文件夹），写入台账并输出任务确认卡参数
    save_result         落账任务执行/应用结果（主 Agent 每处理一个任务都需要存储）
    export_results      导出台账为 Excel 产物（非交互式，供产物展示/下载）
    build_result_card   生成执行结果展示卡参数（含进度与应用到商品入口）
    build_apply_card    合并逐条目的应用参数为批量应用卡参数（item_id 粒度）
    query_offer_prop    按匹配词查询实际商品属性（最多 20 个商品，只读）

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

_DISCOVERY_ERRORS = {}


def _discover_capabilities() -> dict:
    """扫描 scripts/capabilities/*/cmd.py，自动注册命令并保留加载错误。"""
    commands = {}
    _DISCOVERY_ERRORS.clear()
    caps_dir = os.path.join(SCRIPTS_DIR, "capabilities")

    if not os.path.isdir(caps_dir):
        return commands

    for name in sorted(os.listdir(caps_dir)):
        cmd_path = os.path.join(caps_dir, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = "capabilities.{}.cmd".format(name)
        try:
            mod = importlib.import_module(module_path)
            cmd_name = getattr(mod, 'COMMAND_NAME', name)
            commands[cmd_name] = module_path
        except Exception as exc:  # 加载失败不阻断其它命令，但在 usage 中可见
            _DISCOVERY_ERRORS[name] = "%s: %s" % (type(exc).__name__, exc)

    return commands


def _usage(commands: dict):
    lines = ["**1688-item-batch-opt-apply 用法**\n", "```"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append("python3 cli.py {:<20} {}".format(name, desc))
        except Exception:
            lines.append("python3 cli.py {}".format(name))
    if _DISCOVERY_ERRORS:
        lines.append("")
        lines.append("# 加载失败的命令：")
        for name, err in sorted(_DISCOVERY_ERRORS.items()):
            lines.append("#   {} -> {}".format(name, err))
    lines.append("```")

    print(json.dumps({
        "success": False,
        "data": {},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))


def main():
    commands = _discover_capabilities()

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        _usage(commands)
        sys.exit(1)

    cmd = sys.argv[1]
    module_path = commands[cmd]

    sys.argv = ["cli.py {}".format(cmd)] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()


if __name__ == "__main__":
    main()
