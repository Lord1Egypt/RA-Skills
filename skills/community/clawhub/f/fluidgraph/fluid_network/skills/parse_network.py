# -*- coding: utf-8 -*-
"""``parse_network`` —— 解析并校验流体网络定义。

职责边界
--------
**只调用 Core 的 parser**，不复制任何校验规则。这个 Skill 的价值在于把
"解析成功/失败"变成 Agent 能直接消费的形状：

* ``valid`` 一个布尔说清结果；
* 失败时返回**全部**问题的结构化诊断（位置 / 字段 / 修复建议）；
* 成功时返回网络摘要，让 Agent 不必去翻 ``Network`` 对象。
"""

from __future__ import annotations

from typing import Any

from ..diagnostics import Diagnostic
from ..exceptions import FluidNetworkError
from ..models import Network, NodeType, Scenario
from ..parser import FluidConfigParser
from .inputs import ResolvedNetwork, resolve_network_source
from .result import SkillResult

__all__ = ["parse_network", "summarize_network"]

TOOL_NAME = "parse_network"


def parse_network(network_source: Any, *, strict: bool = True) -> SkillResult:
    """解析 TOML 网络定义。

    参数
    ----
    network_source
        TOML 文件路径、TOML 文本、已解析的 TOML 字典，或 ``Network`` 对象。
    strict
        为 ``True``（默认）时未知字段视为错误；为 ``False`` 时忽略。
    """
    parser = FluidConfigParser(strict=strict)
    try:
        resolved = resolve_network_source(network_source, parser=parser)
    except FluidNetworkError as exc:
        return SkillResult.from_exception(TOOL_NAME, exc)
    except Exception as exc:  # noqa: BLE001 - traceback 不该流到 Agent
        return SkillResult.from_exception(TOOL_NAME, exc)

    warnings = _network_warnings(resolved.network)
    return SkillResult.success(
        TOOL_NAME,
        data={
            "valid": True,
            "source": {"kind": resolved.source_kind, "ref": resolved.source_ref},
            "summary": summarize_network(resolved.network, resolved.scenarios),
        },
        warnings=warnings,
    )


# --------------------------------------------------------------------------- #
def summarize_network(
    network: Network,
    scenarios: tuple[Scenario, ...] = (),
) -> dict:
    """网络摘要 —— 只做信息整理，不做任何物理计算。"""
    pumps = network.nodes_of_type(NodeType.PUMP)
    loads = network.loads
    junctions = network.nodes_of_type(NodeType.JUNCTION)

    summary = {
        "network_id": network.id,
        "network_name": network.name,
        "counts": {
            "nodes": len(network.nodes),
            "pumps": len(pumps),
            "junctions": len(junctions),
            "loads": len(loads),
            "pipes": len(network.pipes),
            "valves": len(network.valves),
            "scenarios": len(scenarios),
        },
        "nodes": [
            {
                "id": node.id,
                "type": node.type.value,
                "pressure": node.pressure,
                "min_pressure": node.min_pressure,
                "min_flow": node.min_flow,
                "required_flow": node.required_flow,
                "supply_limit": node.supply_limit,
            }
            for node in network.nodes
        ],
        "pipes": [
            {
                "id": pipe.id,
                "from": pipe.from_node,
                "to": pipe.to_node,
                "resistance": pipe.resistance,
                "diameter": pipe.diameter,
                "length": pipe.length,
            }
            for pipe in network.pipes
        ],
        "valves": [
            {"id": valve.id, "from": valve.from_node, "to": valve.to_node}
            for valve in network.valves
        ],
        "scenarios": [
            {
                "id": scenario.id,
                "name": scenario.display_name,
                "valve_states": dict(scenario.valve_states),
            }
            for scenario in scenarios
        ],
        # 求解器现阶段的能力边界，让 Agent 提前知道什么能问、什么不能问
        "capabilities": {
            "supported_topology": "tree (series/parallel)",
            "supported_node_types": [t.value for t in NodeType],
            "single_pump": True,
            "steady_state": True,
            "incompressible": True,
        },
    }

    # 求解前就能看出的结构性风险，提前告知（不阻断解析）
    notes: list[str] = []
    if len(pumps) == 0:
        notes.append("网络中没有 pump 节点，无法求解（需要至少一个压力源）")
    elif len(pumps) > 1:
        notes.append(f"网络中有 {len(pumps)} 个 pump 节点，当前模型只支持单泵")
    if not loads:
        notes.append("网络中没有 load 节点，求解结果不会有负载判定")
    if not scenarios:
        notes.append("网络没有定义任何工况（[[scenarios]]），无法执行 analyze_scenario")
    if notes:
        summary["notices"] = notes

    return summary


def _network_warnings(network: Network) -> tuple[Diagnostic, ...]:
    """把构建 Network 时产生的非致命提示透出来。"""
    return tuple(getattr(network, "diagnostics", ()) or ())
