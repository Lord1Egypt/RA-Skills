#!/usr/bin/env python3
"""
1688-supplychain-order-inquiry -- 订单询盘 CLI 统一入口

用法：
    python3 cli.py <command> [options]

Commands:
    inquiry_send    订单询盘    python3 cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货"
    batch_inquiry   批量询盘    python3 cli.py batch_inquiry -t '[{"order_ids":["..."],"question":"..."}]'
    configure       配置AK      python3 cli.py configure YOUR_AK

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import ast
import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)


def _extract_constants(file_path: str) -> dict:
    """从 cmd.py 文件中提取 COMMAND_NAME 和 COMMAND_DESC，不执行导入"""
    result = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ('COMMAND_NAME', 'COMMAND_DESC'):
                        if isinstance(node.value, ast.Constant):
                            result[target.id] = node.value.value
    except Exception:
        pass
    return result


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
        module_path = "capabilities.{}.cmd".format(name)
        constants = _extract_constants(cmd_path)
        cmd_name = constants.get('COMMAND_NAME', name)
        cmd_desc = constants.get('COMMAND_DESC', '')
        commands[cmd_name] = {'module': module_path, 'desc': cmd_desc}

    return commands


def _usage(commands: dict):
    lines = ["**1688-supplychain-order-inquiry 用法**\n", "```"]
    for name in sorted(commands):
        desc = commands[name].get('desc', '')
        lines.append("python3 cli.py {:<22} {}".format(name, desc))
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
    module_path = commands[cmd]['module']

    sys.argv = ["cli.py {}".format(cmd)] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()

    # 埋点上报（静默，不影响主流程）
    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass


if __name__ == "__main__":
    main()
