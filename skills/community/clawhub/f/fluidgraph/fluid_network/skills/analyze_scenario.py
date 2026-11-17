# -*- coding: utf-8 -*-
"""``analyze_scenario`` —— 对指定工况执行完整分析。

职责边界
--------
直接复用 :class:`~fluid_network.analysis.AnalysisBuilder` 整条链
（Flow Path Analyzer → Solver → Reliability → AnalysisResult）。
**本 Skill 不含任何计算逻辑**，只负责：

* 把各种形态的网络来源解析出来（:mod:`.inputs`）；
* 找不到工况时给出**结构化**错误（而不是一个 KeyError）；
* 返回完整的 AnalysisResult。
"""

from __future__ import annotations

from typing import Any

from ..analysis import AnalysisBuilder
from ..diagnostics import Diagnostic
from ..exceptions import FluidNetworkError
from ..models import Scenario
from ..parser import FluidConfigParser
from .inputs import resolve_network_source
from .result import SkillResult

__all__ = ["analyze_scenario", "analyze_all_scenarios"]

TOOL_NAME = "analyze_scenario"


def analyze_scenario(
    network_source: Any,
    scenario_id: str,
    *,
    builder: AnalysisBuilder | None = None,
) -> SkillResult:
    """分析一个工况，返回完整 AnalysisResult。

    参数
    ----
    network_source
        TOML 文件路径 / TOML 文本 / 已解析的 TOML 字典 / ``Network`` 对象。
    scenario_id
        工况 id，例如 ``"normal"``、``"v1_failure"``。
    """
    try:
        resolved = resolve_network_source(network_source, parser=FluidConfigParser())
    except FluidNetworkError as exc:
        return SkillResult.from_exception(TOOL_NAME, exc)
    except Exception as exc:  # noqa: BLE001
        return SkillResult.from_exception(TOOL_NAME, exc)

    scenario = resolved.scenario(scenario_id)
    created_ad_hoc = False
    if scenario is None and not resolved.scenarios:
        # 传进来的是一个**裸 Network**（不带工况定义）。这种情况下没有工况清单
        # 可查，就按"阀门全开"构造一个同名工况 —— 这是最符合直觉的默认，
        # 但必须在 warnings 里说清楚，不能让调用方以为它读到了某个已定义的工况。
        scenario = Scenario(id=scenario_id, name=scenario_id)
        created_ad_hoc = True

    if scenario is None:
        return SkillResult.failure(TOOL_NAME, [_unknown_scenario(scenario_id, resolved.scenario_ids)])

    try:
        analysis = (builder or AnalysisBuilder()).build(resolved.network, scenario)
    except FluidNetworkError as exc:
        return SkillResult.from_exception(TOOL_NAME, exc)
    except Exception as exc:  # noqa: BLE001
        return SkillResult.from_exception(TOOL_NAME, exc)

    payload = analysis.to_dict()
    payload["source"] = {"kind": resolved.source_kind, "ref": resolved.source_ref}

    warnings = [
        Diagnostic(
            code="solver_warning",
            message=text,
            severity="warning",
        )
        for text in analysis.warnings
    ]
    if created_ad_hoc:
        warnings.append(
            Diagnostic(
                code="scenario_created_ad_hoc",
                message=f"传入的是 Network 对象，不含工况定义；已按默认（阀门全开）"
                        f"构造工况 '{scenario_id}'",
                suggestion="如需按特定阀门状态分析，请传入 TOML（含 [[scenarios]]）"
                            "或 (network, scenarios) 二元组",
                severity="warning",
                context={"scenario_id": scenario_id},
            )
        )
    return SkillResult.success(TOOL_NAME, data=payload, warnings=warnings)


def analyze_all_scenarios(network_source: Any) -> SkillResult:
    """把网络里定义的全部工况都跑一遍，返回 ``{scenario_id: AnalysisResult}``。

    这是 compare_scenarios 的常见前置 —— 与其让 Agent 逐个调用再去拼装，
    不如提供一个能一次拿全的入口。
    """
    try:
        resolved = resolve_network_source(network_source, parser=FluidConfigParser())
    except FluidNetworkError as exc:
        return SkillResult.from_exception(TOOL_NAME, exc)
    except Exception as exc:  # noqa: BLE001
        return SkillResult.from_exception(TOOL_NAME, exc)

    builder = AnalysisBuilder()
    results: dict[str, dict] = {}
    failures: list[Diagnostic] = []

    for scenario in resolved.scenarios:
        try:
            results[scenario.id] = builder.build(resolved.network, scenario).to_dict()
        except Exception as exc:  # noqa: BLE001 - 单个工况失败不该拖垮其余
            failures.append(
                Diagnostic(
                    code="scenario_analysis_failed",
                    message=f"工况 '{scenario.id}' 分析失败：{exc}",
                    location=f"[[scenarios]] {scenario.id}",
                    suggestion="检查该工况的 valve_states 是否引用了已定义的阀门",
                    context={"scenario_id": scenario.id},
                )
            )

    data = {
        "source": {"kind": resolved.source_kind, "ref": resolved.source_ref},
        "scenarios": results,
    }
    if failures and not results:
        return SkillResult.failure(TOOL_NAME, failures, data=data)
    return SkillResult.success(TOOL_NAME, data=data, warnings=tuple(failures))


# --------------------------------------------------------------------------- #
def _unknown_scenario(scenario_id: str, available: list[str]) -> Diagnostic:
    """工况不存在时的结构化错误 —— 关键是把「有哪些可选」直接告诉 Agent。"""
    return Diagnostic(
        code="unknown_scenario",
        message=f"工况 '{scenario_id}' 不存在",
        location="[[scenarios]]",
        field="id",
        suggestion=f"改用以下之一：{', '.join(available)}" if available
                   else "该网络没有定义任何工况，请先在 TOML 里添加 [[scenarios]]",
        context={"requested": scenario_id, "available_scenarios": available},
    )
