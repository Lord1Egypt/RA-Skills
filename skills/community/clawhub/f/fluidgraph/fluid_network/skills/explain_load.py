# -*- coding: utf-8 -*-
"""``explain_load`` —— 回答"这个负载为什么这样"。

职责边界
--------
**只做查询与解释，不做任何计算。** 所有数值都从传进来的 AnalysisResult 里取。

这个 Skill 存在的意义是：Agent 拿到一个负载的结论时，最需要回答的是
"为什么"，而不只是"是什么"。所以输出里同时给：

* 状态（HEALTHY / ISOLATED / LOW_PRESSURE / LOW_FLOW / UNSUPPORTED / FAILED）
* 数值（可空 —— 不可达时是 ``None`` 而不是 0）
* **诊断三件套**：``reason``、``isolation_point``、``path``

以及一句面向人的 ``explanation``，把"状态 + 数值 + 阈值"串成能直接转述的话。
"""

from __future__ import annotations

from typing import Any, Mapping

from ..diagnostics import Diagnostic
from ..models import LoadStatus
from .result import SkillResult

__all__ = ["explain_load"]

TOOL_NAME = "explain_load"


def explain_load(analysis_result: Any, load_id: str) -> SkillResult:
    """解释某个负载的状态。

    参数
    ----
    analysis_result
        :class:`~fluid_network.models.AnalysisResult` 对象，或它的 ``to_dict()``。
    load_id
        负载节点 id，例如 ``"L1"``。
    """
    data = _as_dict(analysis_result)
    if data is None:
        return SkillResult.failure(TOOL_NAME, [_bad_analysis_input(analysis_result)])

    loads = data.get("loads") or []
    if not loads:
        return SkillResult.failure(TOOL_NAME, [
            Diagnostic(
                code="no_loads_in_result",
                message="该分析结果里没有任何负载",
                suggestion="确认网络里定义了 type = \"load\" 的节点",
            )
        ])

    entry = next((l for l in loads if l.get("load_id") == load_id), None)
    if entry is None:
        available = [l.get("load_id") for l in loads]
        return SkillResult.failure(TOOL_NAME, [
            Diagnostic(
                code="unknown_load",
                message=f"分析结果中不存在负载 '{load_id}'",
                location="loads",
                field="load_id",
                suggestion=f"改用以下之一：{', '.join(str(a) for a in available)}",
                context={"requested": load_id, "available_loads": available},
            )
        ])

    path = (data.get("paths") or {}).get(load_id) or {}
    status = entry.get("status") or LoadStatus.FAILED.value

    payload = {
        "load_id": entry.get("load_id"),
        # 三个数值可能是 null —— 保持 null，绝不用 0 冒充"没有有效值"
        "pressure": entry.get("pressure"),
        "flow": entry.get("flow"),
        # 求解时索取的目标流量，与"实际送达"是两回事，分开呈现
        "required_flow": entry.get("required_flow"),
        "min_pressure": entry.get("min_pressure"),
        "min_flow": entry.get("min_flow"),
        "status": status,
        "status_label": _status_label(status),
        "functional": bool(entry.get("functional")),
        "reachable": bool(entry.get("reachable", path.get("reachable", False))),
        "path": list(path.get("path") or entry.get("path") or []),
        "node_path": list(path.get("node_path") or entry.get("node_path") or []),
        "isolation_point": path.get("isolation_point"),
        "reason": entry.get("reason") or path.get("reason") or "",
        "scenario_id": (data.get("scenario") or {}).get("id"),
        "explanation": _explain(entry, path, status),
    }
    return SkillResult.success(TOOL_NAME, data=payload)


# --------------------------------------------------------------------------- #
# 内部
# --------------------------------------------------------------------------- #
def _as_dict(value: Any) -> dict | None:
    """接受 AnalysisResult 对象或它的 dict 形态。"""
    if isinstance(value, Mapping):
        return dict(value)
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    return None


def _bad_analysis_input(value: Any) -> Diagnostic:
    return Diagnostic(
        code="invalid_analysis_result",
        message=f"需要一个 AnalysisResult（或其 dict），收到 {type(value).__name__}",
        suggestion="先调用 analyze_scenario 拿到结果，再把它的 data 字段传给本工具",
    )


def _status_label(status: str) -> str:
    try:
        return LoadStatus(status).zh
    except ValueError:
        return status


def _explain(entry: Mapping, path: Mapping, status: str) -> str:
    """把状态 + 数值 + 阈值串成一句可直接转述的话。

    刻意不复述 ``reason``（调用方已有该字段），而是补上"差多少 / 断在哪"
    这类需要跨字段看才能得出的信息。
    """
    load_id = entry.get("load_id")
    pressure = entry.get("pressure")
    flow = entry.get("flow")
    min_pressure = entry.get("min_pressure")
    min_flow = entry.get("min_flow")

    if status == LoadStatus.ISOLATED.value:
        cut = path.get("isolation_point")
        where = f"阀门 '{cut}' 关闭" if cut else "网络不连通"
        return (
            f"负载 '{load_id}' 不可达：{where}，该流路已从计算中移除。"
            "压力与流量没有有效值（null），不是 0。"
        )

    if status == LoadStatus.UNSUPPORTED.value:
        return (
            f"负载 '{load_id}' 无法判定：网络拓扑超出当前模型能力"
            "（存在回路或平行冗余通路），数值不可信。"
        )

    if status == LoadStatus.FAILED.value:
        return f"负载 '{load_id}' 求解失败，请检查网络定义。"

    if status == LoadStatus.LOW_PRESSURE.value:
        gap = (min_pressure or 0) - (pressure or 0)
        return (
            f"负载 '{load_id}' 压力不足：实际 {_fmt(pressure)} Pa "
            f"< 最低要求 {_fmt(min_pressure)} Pa，缺口 {_fmt(gap)} Pa。"
            f"流量 {_fmt(flow)} m3/s 是够的。"
        )

    if status == LoadStatus.LOW_FLOW.value:
        gap = (min_flow or 0) - (flow or 0)
        return (
            f"负载 '{load_id}' 流量不足：实际 {_fmt(flow)} m3/s "
            f"< 最低要求 {_fmt(min_flow)} m3/s，缺口 {_fmt(gap)} m3/s。"
            f"压力 {_fmt(pressure)} Pa 是够的。"
        )

    return (
        f"负载 '{load_id}' 功能正常：压力 {_fmt(pressure)} Pa "
        f">= {_fmt(min_pressure)} Pa，流量 {_fmt(flow)} m3/s >= {_fmt(min_flow)} m3/s。"
    )


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:,.6g}"
    return str(value)
