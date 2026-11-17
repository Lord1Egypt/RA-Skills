# -*- coding: utf-8 -*-
"""``render_report`` —— 把 AnalysisResult 渲染成 Markdown 报告。

职责边界
--------
**报告里的每一个数字都取自 AnalysisResult，本模块不计算任何新的物理量。**

唯一做的"运算"是把 Pa 换成 kPa、把 m³/s 换成 L/s 这类**单位换算** ——
与前端同一条规矩。缺失值一律写 ``n/a``，绝不写成 0。
"""

from __future__ import annotations

from typing import Any, Mapping

from ..diagnostics import Diagnostic
from ..models import LoadStatus
from .result import SkillResult

__all__ = ["render_report"]

TOOL_NAME = "render_report"

_STATUS_MARK = {
    LoadStatus.HEALTHY.value: "OK",
    LoadStatus.ISOLATED.value: "FAIL",
    LoadStatus.LOW_PRESSURE.value: "FAIL",
    LoadStatus.LOW_FLOW.value: "FAIL",
    LoadStatus.UNSUPPORTED.value: "SKIP",
    LoadStatus.FAILED.value: "FAIL",
}

_STATUS_ZH = {
    LoadStatus.HEALTHY.value: "正常",
    LoadStatus.ISOLATED.value: "不可达",
    LoadStatus.LOW_PRESSURE.value: "压力不足",
    LoadStatus.LOW_FLOW.value: "流量不足",
    LoadStatus.UNSUPPORTED.value: "拓扑不支持",
    LoadStatus.FAILED.value: "求解失败",
}


def render_report(analysis_result: Any) -> SkillResult:
    """生成 Markdown 报告。

    参数
    ----
    analysis_result
        AnalysisResult 对象或它的 dict。
    """
    data = _as_dict(analysis_result)
    if data is None:
        return SkillResult.failure(TOOL_NAME, [
            Diagnostic(
                code="invalid_analysis_result",
                message=f"需要一个 AnalysisResult（或其 dict），收到 {type(analysis_result).__name__}",
                suggestion="先调用 analyze_scenario 拿到结果，再把它的 data 字段传给本工具",
            )
        ])

    markdown = _render(data)
    return SkillResult.success(
        TOOL_NAME,
        data={"markdown": markdown, "format": "markdown"},
    )


# --------------------------------------------------------------------------- #
# 渲染
# --------------------------------------------------------------------------- #
def _render(data: Mapping) -> str:
    out: list[str] = []
    add = out.append
    scenario = data.get("scenario") or {}
    topology = data.get("topology") or {}
    summary = data.get("summary") or {}

    add("# 流体网络分析报告")
    add("")

    # -- 工况 ---------------------------------------------------------- #
    add("## 工况")
    add("")
    add(f"- 工况 ID：`{scenario.get('id') or 'n/a'}`")
    add(f"- 工况名称：{scenario.get('name') or 'n/a'}")
    add(f"- 网络 ID：`{data.get('network_id') or 'n/a'}`")
    add(f"- 报告 schema：`{data.get('schema_version') or 'n/a'}`")
    add("")

    # -- 网络状态 ------------------------------------------------------ #
    add("## 网络状态")
    add("")
    add(f"- 是否连通：{'是' if topology.get('connected') else '否'}")
    add(f"- 拓扑是否被当前模型支持：{'是' if topology.get('supported') else '否'}")
    isolated_nodes = topology.get("isolated_nodes") or []
    add(f"- 不可达节点（{len(isolated_nodes)}）：{_join(isolated_nodes)}")
    main_pipe = data.get("main_pipe_id")
    if main_pipe:
        add(f"- 主干管：`{main_pipe}`")
    if not topology.get("supported") and topology.get("unsupported_reason"):
        add(f"- 不支持原因：{topology['unsupported_reason']}")
    add("")

    # -- 流路分析 ------------------------------------------------------ #
    add("## 流路分析")
    add("")
    paths = data.get("paths") or {}
    if not paths:
        add("_本次分析没有流路信息。_")
    else:
        for load_id, path in paths.items():
            if path.get("reachable"):
                chain = path.get("path") or []
                node_chain = path.get("node_path") or []
                add(f"- **{load_id}**：{' -> '.join(chain) if chain else 'n/a'}")
                if node_chain:
                    add(f"  - 节点路径：{' -> '.join(node_chain)}")
            else:
                cut = path.get("isolation_point")
                add(f"- **{load_id}**：不可达" + (f"（切断点：`{cut}`）" if cut else ""))
                add(f"  - {path.get('reason') or 'n/a'}")
    add("")

    # -- 负载状态 ------------------------------------------------------ #
    add("## 负载状态")
    add("")
    loads = data.get("loads") or []
    if not loads:
        add("_本次分析没有负载。_")
    else:
        add("| 负载 | 状态 | 功能 | 压力 | 最低要求压力 | 流量 | 最低要求流量 | 需求流量 |")
        add("|---|---|---|---|---|---|---|---|")
        for load in loads:
            status = load.get("status") or ""
            add(
                f"| {load.get('load_id')} "
                f"| {_mark(status)} {status} "
                f"| {'是' if load.get('functional') else '否'} "
                f"| {_pressure(load.get('pressure'))} "
                f"| {_pressure(load.get('min_pressure'))} "
                f"| {_flow(load.get('flow'))} "
                f"| {_flow(load.get('min_flow'))} "
                f"| {_flow(load.get('required_flow'))} |"
            )
        add("")
        add("> 压力单位为 kPa，流量单位为 L/s（原始 JSON 为 SI：Pa / m3/s）。")
        add("> `n/a` 表示**没有有效计算值**（例如负载被切断），不是 0。")
    add("")

    # -- 管路状态 ------------------------------------------------------ #
    add("## 管路状态")
    add("")
    pipes = data.get("pipes") or []
    if pipes:
        add("| 管路 | 流向 | 流量 | 流速 | 压降 | 参与计算 |")
        add("|---|---|---|---|---|---|")
        for pipe in pipes:
            add(
                f"| {pipe.get('pipe_id')} "
                f"| {pipe.get('from')} -> {pipe.get('to')} "
                f"| {_flow(pipe.get('flow'))} "
                f"| {_velocity(pipe.get('velocity'))} "
                f"| {_pressure(pipe.get('pressure_drop'))} "
                f"| {'是' if pipe.get('active') else '否'} |"
            )
        add("")
    else:
        add("_本次分析没有管路信息。_")
        add("")

    valves = data.get("valves") or []
    if valves:
        add("### 阀门")
        add("")
        add("| 阀门 | 位置 | 状态 | 流量 |")
        add("|---|---|---|---|")
        for valve in valves:
            add(
                f"| {valve.get('valve_id')} "
                f"| {valve.get('from')} -> {valve.get('to')} "
                f"| {'开启' if valve.get('is_open') else '关闭'} "
                f"| {_flow(valve.get('flow'))} |"
            )
        add("")

    # -- 可靠性结论 ---------------------------------------------------- #
    add("## 可靠性结论")
    add("")
    add(
        f"共 **{_num(summary.get('total_loads'))}** 个负载："
        f"正常 **{_num(summary.get('functional_loads'))}**、"
        f"故障 **{_num(summary.get('failed_loads'))}**、"
        f"隔离 **{_num(summary.get('isolated_loads'))}**。"
    )
    add("")

    counts = summary.get("status_counts") or {}
    if counts:
        add("| 状态 | 数量 |")
        add("|---|---|")
        for status, count in counts.items():
            add(f"| {status}（{_STATUS_ZH.get(status, status)}） | {count} |")
        add("")

    failing = [l for l in loads if not l.get("functional")]
    if failing:
        add("**未满足要求的负载：**")
        add("")
        for load in failing:
            add(f"- `{load.get('load_id')}` — {load.get('reason') or 'n/a'}")
        add("")
    elif loads:
        add("全部负载均满足最低压力与最低流量要求。")
        add("")

    # -- 异常与警告 ---------------------------------------------------- #
    add("## 异常与警告")
    add("")
    warnings = data.get("warnings") or []
    if not warnings:
        add("_无。_")
    else:
        for warning in warnings:
            add(f"- {warning}")
    add("")

    return "\n".join(out)


# --------------------------------------------------------------------------- #
# 格式化（只做单位换算与缺失值处理）
# --------------------------------------------------------------------------- #
def _mark(status: str) -> str:
    return f"[{_STATUS_MARK.get(status, 'FAIL')}]"


def _pressure(pa: Any) -> str:
    """Pa -> kPa。``None`` 渲染成 ``n/a`` —— 绝不写 0。"""
    if not _is_number(pa):
        return "n/a"
    return f"{pa / 1000:,.2f} kPa"


def _flow(m3s: Any) -> str:
    """m3/s -> L/s。"""
    if not _is_number(m3s):
        return "n/a"
    return f"{m3s * 1000:,.4f} L/s"


def _velocity(value: Any) -> str:
    if not _is_number(value):
        return "n/a"
    return f"{value:,.4f} m/s"


def _num(value: Any) -> str:
    return str(value) if _is_number(value) else "0"


def _join(items: list) -> str:
    return ", ".join(str(i) for i in items) if items else "无"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _as_dict(value: Any) -> dict | None:
    if isinstance(value, Mapping):
        return dict(value)
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    return None
