# -*- coding: utf-8 -*-
"""``compare_scenarios`` —— 按负载逐项对比多个工况。

关于 null 的 delta
------------------
这是本模块最需要注意的地方。负载从 HEALTHY 变成 ISOLATED 时::

    pressure: 350400 -> null

**不能**把差值算成 ``-350400``。那样会凭空造出一个"压力下降了 350 kPa"的
假结论 —— 而真相是这个值根本不存在（负载被切断了）。

所以这里的规则是：

* 两侧都有值 → 给出真实 delta；
* 只有一侧有值 → ``delta = None``，并在 ``note`` 里说明**为什么**；
* 两侧都没有 → ``delta = None``，不加说明。

同时提供 ``status_changed`` 与 ``transition``（``"HEALTHY -> ISOLATED"``），
让 Agent 不必自己去比字符串。
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from ..diagnostics import Diagnostic
from ..models import LoadStatus
from .result import SkillResult

__all__ = ["compare_scenarios"]

TOOL_NAME = "compare_scenarios"

# 数值字段 -> 展示名，用于生成 note
_METRICS = ("pressure", "flow")

_NULL_NOTES = {
    "pressure": "前一个工况有压力值，当前工况无有效值（负载不可达）",
    "flow": "前一个工况有流量值，当前工况无有效值（负载不可达）",
}


def compare_scenarios(analysis_results: Sequence[Any]) -> SkillResult:
    """对比两个或多个工况的分析结果。

    参数
    ----
    analysis_results
        至少两个 AnalysisResult（对象或 dict），顺序即对比顺序。
    """
    if not isinstance(analysis_results, (list, tuple)):
        return SkillResult.failure(TOOL_NAME, [
            Diagnostic(
                code="invalid_comparison_input",
                message=f"需要一个分析结果列表，收到 {type(analysis_results).__name__}",
                suggestion="把两个或更多 analyze_scenario 的 data 放进一个列表再传入",
            )
        ])

    if len(analysis_results) < 2:
        return SkillResult.failure(TOOL_NAME, [
            Diagnostic(
                code="not_enough_scenarios",
                message=f"对比至少需要 2 个工况，收到 {len(analysis_results)} 个",
                suggestion="再跑一个工况（例如 normal 与 v1_failure）后一起传入",
            )
        ])

    parsed: list[dict] = []
    for index, item in enumerate(analysis_results):
        data = _as_dict(item)
        if data is None:
            return SkillResult.failure(TOOL_NAME, [
                Diagnostic(
                    code="invalid_analysis_result",
                    message=f"第 {index} 项不是 AnalysisResult（{type(item).__name__}）",
                    suggestion="只传 analyze_scenario 返回的 data，不要传文件路径或 TOML",
                )
            ])
        parsed.append(data)

    scenario_ids = [_scenario_id(d, i) for i, d in enumerate(parsed)]

    # 以第一个工况的负载集合为基准，同时兜住后续工况里新增的负载
    load_ids: list[str] = []
    for data in parsed:
        for load in (data.get("loads") or []):
            lid = load.get("load_id")
            if lid and lid not in load_ids:
                load_ids.append(lid)

    if not load_ids:
        return SkillResult.failure(TOOL_NAME, [
            Diagnostic(
                code="no_loads_in_result",
                message="这些分析结果里都没有负载，无从对比",
                suggestion="确认网络里定义了 type = \"load\" 的节点",
            )
        ])

    comparisons: dict[str, dict] = {}
    warnings: list[Diagnostic] = []

    for load_id in load_ids:
        entries = [_find_load(data, load_id) for data in parsed]
        missing = [sid for sid, e in zip(scenario_ids, entries) if e is None]
        if missing:
            warnings.append(
                Diagnostic(
                    code="load_missing_in_scenario",
                    message=f"负载 '{load_id}' 在工况 {', '.join(missing)} 中不存在",
                    suggestion="对比时该工况的对应项为 null，不代表流量为零",
                    context={"load_id": load_id, "scenarios": missing},
                    severity="warning",
                )
            )

        series: dict[str, list] = {}
        deltas: dict[str, Any] = {}
        notes: dict[str, str] = {}

        for metric in _METRICS:
            values = [(_get(e, metric) if e else None) for e in entries]
            series[metric] = values
            deltas[metric] = _delta(values, metric, notes)

        statuses = [(_get(e, "status") if e else None) for e in entries]
        changed = len(set(statuses)) > 1 and all(s is not None for s in statuses)
        transition = " -> ".join(str(s) for s in statuses)

        # 功能状态的变化方向：变好 / 变坏 / 没变 —— Agent 最常用的判断
        direction = _direction([_functional(e) for e in entries])

        comparisons[load_id] = {
            "load_id": load_id,
            "scenarios": scenario_ids,
            "status": statuses,
            "status_changed": changed,
            "transition": transition,
            "direction": direction,
            "functional": [_functional(e) for e in entries],
            "pressure": series["pressure"],
            "flow": series["flow"],
            "delta": deltas,
            "notes": notes,
        }

    return SkillResult.success(
        TOOL_NAME,
        data={
            "scenarios": scenario_ids,
            "loads": comparisons,
            "summary": _summarize(comparisons, scenario_ids),
        },
        warnings=tuple(warnings),
    )


# --------------------------------------------------------------------------- #
# 内部
# --------------------------------------------------------------------------- #
def _as_dict(value: Any) -> dict | None:
    if isinstance(value, Mapping):
        return dict(value)
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    return None


def _scenario_id(data: Mapping, index: int) -> str:
    scenario = data.get("scenario") or {}
    return scenario.get("id") or f"scenario_{index}"


def _find_load(data: Mapping, load_id: str) -> Mapping | None:
    for load in (data.get("loads") or []):
        if load.get("load_id") == load_id:
            return load
    return None


def _get(entry: Mapping | None, key: str) -> Any:
    return None if entry is None else entry.get(key)


def _functional(entry: Mapping | None) -> bool | None:
    return None if entry is None else bool(entry.get("functional"))


def _delta(values: list, metric: str, notes: dict) -> float | None:
    """计算首尾差值，并正确处理 null。

    只在**两端都有有效值**时才给数字。任一端为 null 就返回 None 并写清楚原因 ——
    把 ``350400 -> null`` 算成 ``-350400`` 会凭空造出一个不存在的"下降了"结论。
    """
    first, last = values[0], values[-1]

    if first is None and last is None:
        return None

    if first is not None and last is not None:
        return last - first

    # 恰好一端有值 —— 明确说明，不要伪造
    if first is None:
        notes[metric] = "前一个工况无有效值，当前工况有值（无法计算增量）"
    else:
        notes[metric] = _NULL_NOTES.get(metric, "当前工况无有效值（无法计算增量）")
    return None


def _direction(functionals: list) -> str:
    """功能状态的总体走向：improved / degraded / unchanged / mixed / unknown。"""
    known = [f for f in functionals if f is not None]
    if len(known) < 2:
        return "unknown"

    before, after = known[0], known[-1]
    if before == after:
        # 中间有反复也算 mixed
        if len(set(known)) > 1:
            return "mixed"
        return "unchanged"
    return "improved" if (after and not before) else "degraded"


def _summarize(comparisons: Mapping[str, dict], scenario_ids: list[str]) -> dict:
    degraded = [lid for lid, c in comparisons.items() if c["direction"] == "degraded"]
    improved = [lid for lid, c in comparisons.items() if c["direction"] == "improved"]
    changed = [lid for lid, c in comparisons.items() if c["status_changed"]]

    return {
        "scenarios": scenario_ids,
        "loads_compared": len(comparisons),
        "status_changed": changed,
        "degraded": degraded,
        "improved": improved,
        "unchanged": [
            lid for lid, c in comparisons.items()
            if c["direction"] == "unchanged"
        ],
    }
