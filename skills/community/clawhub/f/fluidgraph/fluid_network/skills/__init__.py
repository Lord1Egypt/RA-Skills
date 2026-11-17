# -*- coding: utf-8 -*-
"""FluidGraph Skill 层 —— 给 Agent 用的稳定工具接口。

设计原则
--------
严格区分两件事：

**Agent 负责**
    理解自然语言、选择工具、组织调用顺序、解释结果。

**FluidGraph Core 负责**
    TOML 解析、网络校验、图拓扑、流路分析、流体求解、可靠性判断、结果生成。

**本层只做**：输入适配 → 调用 Core → 输出标准化。

这里没有、也永远不该有第二份物理实现。页面上、Agent 里看到的每一个
pressure / flow / velocity / status，都必须来自 Core 的
:class:`~fluid_network.solver.Solver` 与
:class:`~fluid_network.reliability.ReliabilityAnalyzer`。

工具清单
--------
============================  ============================================
``parse_network``             解析并校验网络定义，返回摘要或全部结构化错误
``analyze_scenario``          执行指定工况，返回完整 AnalysisResult
``analyze_all_scenarios``     一次跑完全部工况（compare 的常见前置）
``explain_load``              解释单个负载为什么是这个状态
``compare_scenarios``         按负载逐项对比多个工况
``render_report``             渲染 Markdown 报告
============================  ============================================
"""

from .analyze_scenario import analyze_all_scenarios, analyze_scenario
from .compare_scenarios import compare_scenarios
from .explain_load import explain_load
from .inputs import resolve_network_source
from .parse_network import parse_network, summarize_network
from .render_report import render_report
from .result import SkillResult

__all__ = [
    # 契约
    "SkillResult",
    # 工具
    "parse_network",
    "analyze_scenario",
    "analyze_all_scenarios",
    "explain_load",
    "compare_scenarios",
    "render_report",
    # 辅助
    "summarize_network",
    "resolve_network_source",
    "TOOLS",
    "get_tool",
    "to_openai_tools",
    "to_anthropic_tools",
]

# Skill 名称 -> 可调用对象。Runner 与 Schema 都以此为准，避免两处清单走样。
TOOLS = {
    "parse_network": parse_network,
    "analyze_scenario": analyze_scenario,
    "analyze_all_scenarios": analyze_all_scenarios,
    "explain_load": explain_load,
    "compare_scenarios": compare_scenarios,
    "render_report": render_report,
}


def get_tool(name: str):
    """按名字取工具；未知名会给出可用清单。"""
    try:
        return TOOLS[name]
    except KeyError:
        available = ", ".join(sorted(TOOLS))
        raise KeyError(f"未知工具 '{name}'；可用：{available}") from None


# --------------------------------------------------------------------------- #
# 与各家 tool-calling 格式的映射
#
# 这几个函数只做**形状转换**，不含任何业务逻辑 —— Schema 本身定义在
# fluid_network/skills/schema.py 里，是唯一真相。
# --------------------------------------------------------------------------- #
def to_openai_tools() -> list[dict]:
    """转成 OpenAI ``tools=[...]`` 的格式。"""
    from .schema import TOOL_SCHEMAS

    return [
        {
            "type": "function",
            "function": {
                "name": schema["name"],
                "description": schema["description"],
                "parameters": schema["input_schema"],
            },
        }
        for schema in TOOL_SCHEMAS
    ]


def to_anthropic_tools() -> list[dict]:
    """转成 Anthropic Messages API ``tools=[...]`` 的格式。"""
    from .schema import TOOL_SCHEMAS

    return [
        {
            "name": schema["name"],
            "description": schema["description"],
            "input_schema": schema["input_schema"],
        }
        for schema in TOOL_SCHEMAS
    ]


def to_mcp_tools() -> list[dict]:
    """转成 MCP ``tools/list`` 的格式。"""
    from .schema import TOOL_SCHEMAS

    return [
        {
            "name": schema["name"],
            "description": schema["description"],
            "inputSchema": schema["input_schema"],
        }
        for schema in TOOL_SCHEMAS
    ]
