#!/usr/bin/env python3
"""
1688-shop-crm-customer-filter —— 1688店铺CRM客户智能筛选 CLI 统一入口

Usage:
    python3 cli.py <command> [options]

Commands（更多参数见项目根目录 SKILL.md）:
    alibaba.1688.customer.attr.field.config  获取筛选列配置
    alibaba.1688.customer.list          筛选客户列表
    customer_attr_add      新增属性列

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)


def _discover_capabilities() -> tuple:
    """扫描 capabilities/*/cmd.py，自动注册命令"""
    commands = {}
    errors = []
    caps_dir = os.path.join(SCRIPTS_DIR, "capabilities")

    if not os.path.isdir(caps_dir):
        return commands, errors

    for name in sorted(os.listdir(caps_dir)):
        cmd_path = os.path.join(caps_dir, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = f"capabilities.{name}.cmd"
        try:
            mod = importlib.import_module(module_path)
            cmd_name = getattr(mod, 'COMMAND_NAME', name)
            commands[cmd_name] = module_path
        except Exception as exc:
            errors.append(f"{module_path}: {type(exc).__name__}: {exc}")

    return commands, errors


def _usage(commands: dict):
    lines = ["**1688-shop-crm-customer-filter 用法**\n", "```"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append(f"python3 cli.py {name:<16} {desc}")
        except Exception:
            lines.append(f"python3 cli.py {name}")
    lines.append("```")

    print(json.dumps({
        "success": False,
        "data": {},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))


def main():
    commands, discovery_errors = _discover_capabilities()
    for error in discovery_errors:
        print(f"capability 加载失败：{error}", file=sys.stderr)

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        _usage(commands)
        return 1

    cmd = sys.argv[1]
    module_path = commands[cmd]

    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    exit_code = module.main()

    # 每次命令执行后上报埋点，失败不影响主流程
    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass
    # capability 未显式返回退出码视为失败，避免“打印了错误但进程为 0”。
    return exit_code if isinstance(exit_code, int) else 1


if __name__ == "__main__":
    sys.exit(main())
