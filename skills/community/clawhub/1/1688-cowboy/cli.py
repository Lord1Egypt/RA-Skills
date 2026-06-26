#!/usr/bin/env python3
"""
niuzai-receptionist -- 接待助手 Skill CLI 统一入口

用法：
    python3 cli.py <command> [options]

Commands（白名单，只暴露 SKILL.md 当前主张的对外能力）：
    daily_report        查看工作日报      cli.py daily_report --date today
    knowledge_query     查询待完善知识    cli.py knowledge_query
    knowledge_answer    补充知识库答案    cli.py knowledge_answer --question "..." --answer "..."
    test_chat           模拟对话试答        cli.py test_chat --query "..."
    transfer_inquiries  查询转人工询盘（分页） cli.py transfer_inquiries --date 2026-05-14 --page-num 1 --page-size 10
    configure           配置 AK           cli.py configure YOUR_AK

注：hire-reception 是主 Agent 内部 5 步流程编排，不走 CLI；
    quote_* / score / skill_* 等历史能力已下线并清空代码。
    详见 references/common/internals.md。

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import ast
import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

# 命令白名单：只暴露 SKILL.md 当前主张的对外 CLI 能力
# 历史能力目录（quote_* / score / skill_*）已清空，白名单作为双保险兑底
EXPOSED_COMMANDS = {
    "daily_report",
    "knowledge_query",
    "knowledge_answer",
    "test_chat",
    "transfer_inquiries",
    "configure",
    "cowboy_config",
}


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
        # 白名单过滤：仅暴露当前主张的对外 CLI 能力
        if cmd_name not in EXPOSED_COMMANDS:
            continue
        commands[cmd_name] = {'module': module_path, 'desc': cmd_desc}

    return commands


def _usage(commands: dict):
    lines = ["**niuzai-receptionist 用法**\n", "```"]
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
