#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FluidGraph Skill Runner —— 在命令行调用 Skill，验证 tool contract。

用法::

    python skill_runner.py parse_network examples/example.toml
    python skill_runner.py analyze_scenario examples/example.toml normal
    python skill_runner.py analyze_scenario examples/example.toml v1_failure
    python skill_runner.py analyze_all_scenarios examples/example.toml
    python skill_runner.py explain_load outputs/v1_failure.json L1
    python skill_runner.py compare_scenarios outputs/normal.json outputs/v1_failure.json
    python skill_runner.py render_report outputs/v1_failure.json

    python skill_runner.py --list                        # 列出全部工具
    python skill_runner.py --schema                      # 输出 JSON Schema
    python skill_runner.py --schema --format anthropic   # 转成 Anthropic tools 格式

默认输出紧凑 JSON；``--pretty`` 缩进。``render_report`` 默认输出 Markdown 原文，
加 ``--json`` 可以强制回 JSON。

**这个 CLI 也是 Agent 的参考实现**：Agent 看到的返回值，与这里打印的
``SkillResult`` 完全一致 —— 包括失败时的结构化 errors。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fluid_network.console import configure_stdout, safe_print  # noqa: E402
from fluid_network.skills import TOOLS, get_tool  # noqa: E402
from fluid_network.skills.schema import describe_tools, validate_arguments  # noqa: E402

# 每个工具的位置参数 -> 关键字参数名。
# CLI 用位置参数是为了好敲；内部一律走关键字，避免位置错位。
POSITIONAL_ARGS: dict[str, list[str]] = {
    "parse_network": ["network_source"],
    "analyze_scenario": ["network_source", "scenario_id"],
    "analyze_all_scenarios": ["network_source"],
    "explain_load": ["analysis_result", "load_id"],
    "compare_scenarios": ["analysis_results"],
    "render_report": ["analysis_result"],
}

# 这些工具的第一个参数如果是 .json 文件，读进来后当作 AnalysisResult 用
_JSON_INPUT_TOOLS = {"explain_load", "compare_scenarios", "render_report"}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="FluidGraph Skill Runner —— 调用 Skill 并输出结构化结果",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="工具清单：\n  " + "\n  ".join(sorted(TOOLS)),
    )
    parser.add_argument("tool", nargs="?", help="工具名")
    parser.add_argument("args", nargs="*", help="工具参数")

    parser.add_argument("--pretty", action="store_true", help="缩进输出 JSON")
    parser.add_argument("--json", dest="force_json", action="store_true",
                        help="即使 render_report 也输出 JSON")
    parser.add_argument("--strict", dest="strict", action="store_true", default=None,
                        help="parse_network：未知字段视为错误（默认行为）")
    parser.add_argument("--lenient", dest="strict", action="store_false",
                        help="parse_network：容忍未知字段")
    parser.add_argument("--list", action="store_true", help="列出全部工具后退出")
    parser.add_argument("--schema", action="store_true", help="输出工具 Schema 后退出")
    parser.add_argument("--format", default="raw",
                        choices=["raw", "openai", "anthropic", "mcp"],
                        help="配合 --schema：转换到某家的 tool-calling 格式")
    return parser.parse_args(argv)


# --------------------------------------------------------------------------- #
def load_argument(tool: str, name: str, value: str):
    """把 CLI 字符串参数转成工具真正需要的形态。

    只有 ``.json`` 才当文件读 —— 其余原样传字符串，由 Skill 层自己判定
    是路径还是 TOML 文本。
    """
    if tool in _JSON_INPUT_TOOLS and (name == "analysis_result" or name == "analysis_results"):
        # 先试 JSON 字面量再试文件：内联 JSON 可能长达数万字符，
        # 直接丢给 Path.is_file() 在 Linux 上会抛 OSError(ENAMETOOLONG)。
        # 顺序反过来就没有这个问题 —— 能解析成 JSON 的一定不是文件路径。
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        try:
            path = Path(value)
            if path.is_file() and path.suffix.lower() == ".json":
                return json.loads(path.read_text(encoding="utf-8"))
        except OSError:
            # 路径过长 / 非法字符 —— 都不是文件，原样交回让 Skill 报结构化错误
            pass
        return value
    return value


def build_kwargs(tool: str, raw_args: list[str], ns: argparse.Namespace) -> dict:
    # compare_scenarios 接受**可变数量**的文件，先单独处理，
    # 否则会被下面的元数检查当成"多余参数"拦下来。
    if tool == "compare_scenarios":
        if len(raw_args) < 2:
            raise ValueError(
                "compare_scenarios 至少需要 2 个分析结果文件；"
                "用法：python skill_runner.py compare_scenarios <a.json> <b.json> [...]"
            )
        return {
            "analysis_results": [
                load_argument(tool, "analysis_result", value) for value in raw_args
            ]
        }

    names = POSITIONAL_ARGS.get(tool, [])
    if len(raw_args) < len(names):
        missing = names[len(raw_args):]
        raise ValueError(
            f"工具 '{tool}' 缺少参数：{', '.join(missing)}；"
            f"用法：python skill_runner.py {tool} " + " ".join(f"<{n}>" for n in names)
        )
    extra = raw_args[len(names):]
    if extra:
        raise ValueError(
            f"工具 '{tool}' 收到多余的参数：{', '.join(extra)}；"
            f"它只接受 {len(names)} 个：{', '.join(names)}"
        )

    kwargs: dict = {}
    for name, value in zip(names, raw_args):
        kwargs[name] = load_argument(tool, name, value)

    if tool == "parse_network" and ns.strict is not None:
        kwargs["strict"] = ns.strict

    return kwargs


# --------------------------------------------------------------------------- #
def emit(result, ns: argparse.Namespace, tool: str) -> int:
    """输出结果。render_report 成功时默认打 Markdown 原文。"""
    if not result.ok:
        safe_print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return 1

    if tool == "render_report" and not ns.force_json:
        safe_print(result.data["markdown"])
        return 0

    indent = 2 if ns.pretty else None
    safe_print(json.dumps(result.to_dict(), indent=indent, ensure_ascii=False))
    return 0


def _usage_error(tool: str, message: str, *, suggestion: str = "") -> int:
    """用法/参数错误也走统一的 SkillResult 形状。

    对 Agent 来说，"工具参数错了"和"工具执行失败了"应该长得一样 ——
    都是 ``ok=false`` + 结构化 errors。分开两种格式只会让调用方多写一个分支。
    """
    payload = {
        "ok": False,
        "tool": tool,
        "data": None,
        "errors": [{
            "code": "usage_error",
            "severity": "error",
            "message": message,
            **({"suggestion": suggestion} if suggestion else {}),
        }],
        "warnings": [],
    }
    safe_print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 2


def main(argv: list[str]) -> int:
    configure_stdout()
    ns = parse_args(argv)

    if ns.list:
        for item in describe_tools():
            safe_print(f"{item['name']}")
            safe_print(f"    参数: {', '.join(item['properties'])}")
            safe_print(f"    必需: {', '.join(item['required'])}")
            safe_print(f"    {item['description'].split('。')[0]}。")
        return 0

    if ns.schema:
        from fluid_network.skills import to_anthropic_tools, to_mcp_tools, to_openai_tools
        from fluid_network.skills.schema import TOOL_SCHEMAS

        converters = {
            "raw": lambda: TOOL_SCHEMAS,
            "openai": to_openai_tools,
            "anthropic": to_anthropic_tools,
            "mcp": to_mcp_tools,
        }
        safe_print(json.dumps(converters[ns.format](), indent=2, ensure_ascii=False))
        return 0

    if not ns.tool:
        safe_print("用法：python skill_runner.py <tool> [args...]")
        safe_print("可用工具：" + ", ".join(sorted(TOOLS)))
        safe_print("加 --list 查看参数说明。")
        return 2

    if ns.tool not in TOOLS:
        return _usage_error(
            ns.tool,
            f"未知工具 '{ns.tool}'",
            suggestion="可用工具：" + ", ".join(sorted(TOOLS)),
        )

    try:
        kwargs = build_kwargs(ns.tool, ns.args, ns)
    except ValueError as exc:
        return _usage_error(ns.tool, str(exc),
                            suggestion=f"python skill_runner.py --list 可查看每个工具的参数")

    # 参数校验 —— 让 Agent 在真正调用前就能拿到可读的参数错误
    problems = validate_arguments(ns.tool, kwargs)
    if problems:
        payload = {
            "ok": False,
            "tool": ns.tool,
            "data": None,
            "errors": [
                {"code": "invalid_arguments", "severity": "error", "message": p}
                for p in problems
            ],
            "warnings": [],
        }
        safe_print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 2

    tool = get_tool(ns.tool)
    result = tool(**kwargs)
    return emit(result, ns, ns.tool)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
