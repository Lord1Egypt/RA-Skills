#!/usr/bin/env python3
"""
1688-shop-daily-report —— 店铺经营日报 CLI 统一入口

Usage:
    python3 cli.py <command> [options]

Commands（更多参数见项目根目录 SKILL.md）:
    configure                      配置 AK（查看状态/设置/重置）
    get_trade_data                 获取指定日期的交易数据
    get_traffic_data               获取指定日期的流量数据
    get_user_data                  获取指定日期的买家数据

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import site
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

# 部分执行环境（如 workflow 沙箱）会禁用 user site-packages（PYTHONNOUSERSITE / ENABLE_USER_SITE=False），
# 而 requests 常装在用户目录（~/Library/Python/x.y/lib/python/site-packages）。不兜底的后果是：
# 除 configure 外的 9 个命令全部 import 失败 → 命令表只剩 configure → 误报“命令不存在”并打印用法。
# 此处显式把用户级 site-packages 补回 sys.path（仅追加，不影响已有优先级）。
try:
    _user_site = site.getusersitepackages()
    if _user_site and os.path.isdir(_user_site) and _user_site not in sys.path:
        sys.path.append(_user_site)
except Exception:
    pass

def _discover_capabilities() -> tuple:
    """自动注册命令：逐个尝试导入 capabilities/*/cmd.py

    返回 (commands, load_errors)。**不得静默吞掉 import 异常**：依赖缺失（如 requests 未安装、
    或沙箱未加载 user site-packages）会导致除 configure 外的命令全部注册失败，
    若吞掉异常就会表现为“命令不存在”+打印用法，排查时极具误导性。
    """
    commands = {}
    load_errors = {}
    caps_dir = os.path.join(SCRIPTS_DIR, "capabilities")

    if not os.path.isdir(caps_dir):
        return commands, load_errors

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
            load_errors[name] = f"{type(exc).__name__}: {exc}"

    return commands, load_errors

def _usage(commands: dict, load_errors: dict = None):
    lines = ["**1688-shop-daily-report 用法**\n", "```"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append(f"python3 cli.py {name:<20} {desc}")
        except Exception:
            lines.append(f"python3 cli.py {name}")
    lines.append("```")

    # 有命令注册失败时必须显式报出：否则依赖缺失会伪装成“命令不存在”
    if load_errors:
        missing = sorted(load_errors)
        lines.append(f"\n⚠️ 以下 {len(missing)} 个命令加载失败（大概率是 Python 依赖缺失）：{', '.join(missing)}")
        lines.append(f"首个错误：{load_errors[missing[0]]}")
        lines.append("修复：`python3 -m pip install -r requirements.txt`")

    print(json.dumps({
        "success": False,
        "data": {"loadErrors": load_errors or {}},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))

def main():
    commands, load_errors = _discover_capabilities()

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        _usage(commands, load_errors)
        sys.exit(1)

    cmd = sys.argv[1]
    module_path = commands[cmd]

    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()

    # 每次命令执行后上报埋点，失败不影响主流程
    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass

if __name__ == "__main__":
    main()
