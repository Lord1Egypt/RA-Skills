#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Research Forge 输出校验 lint 脚本。

检测研究输出 JSON 是否符合 deep-research-forge 的 schema 约束和协议承诺，
覆盖证据账本完整性、状态机合法性、质量门禁合规性和并行执行结构。

支持两种输入模式：
  1. evidence ledger JSON — 校验证据条目完整性
  2. research cycle report JSON — 校验状态机、质量门禁、并行执行

用法:
    python lint_research_output.py <output.json>
    python lint_research_output.py work/*.json
    python lint_research_output.py --strict <output.json>

退出码:
    0 = 无 error（可能有 warning）
    1 = 存在 error
"""

import argparse
import glob
import json
import re
import sys
from pathlib import Path


# ── 常量 ───────────────────────────────────────────────────────────────────

VALID_ENTRY_STATUS = {
    "confirmed_fact",
    "reported_claim",
    "user_signal",
    "inference",
    "gap",
}

VALID_SOURCE_TYPE = {
    "official",
    "public_record",
    "paper",
    "media",
    "community",
    "review",
    "social",
    "aggregator",
    "user_provided",
    "analysis",
}

VALID_RELIABILITY = {"high", "medium", "low", "unknown"}

VALID_CITATION_STRENGTH = {
    "direct-primary",
    "indirect-primary",
    "independent-corroborated",
    "single-secondary",
    "user-signal-only",
    "unsupported-gap",
}

VALID_FORMAL_STATUS = {
    "final-in-force",
    "applicable-obligation",
    "adopted-not-yet-applicable",
    "delegated-or-implementing-act",
    "official-guidance-final",
    "official-guidance-draft",
    "political-agreement",
    "pilot-or-trial",
    "institution-policy",
    "voluntary-code",
    "third-party-interpretation",
    "status-unclear",
}

VALID_AGENT_ROLES = {
    "lead-integrator",
    "source-scout",
    "timeline-analyst",
    "competitive-analyst",
    "user-signal-analyst",
    "dissent-reviewer",
    "decision-analyst",
    "single-agent",
    "unknown",
}

# ── 状态机 ─────────────────────────────────────────────────────────────────

VALID_STATES = {
    "planned",
    "spawned",
    "researching",
    "produced",
    "verifying",
    "conflict_arbitrating",
    "retrying",
    "passed",
    "failed",
    "hold",
    "escalated",
    "accepted",
}

VALID_STATE_TRANSITIONS = {
    "planned": {"spawned"},
    "spawned": {"researching"},
    "researching": {"produced"},
    "produced": {"verifying"},
    "verifying": {"passed", "conflict_arbitrating", "retrying", "hold", "failed"},
    "conflict_arbitrating": {"passed", "retrying", "escalated"},
    "retrying": {"researching"},
    "passed": {"accepted"},
    "hold": {"escalated"},
    "failed": {"escalated"},
    "escalated": set(),
    "accepted": set(),
}

# ── 验证报告 verdict ──────────────────────────────────────────────────────

VALID_VERDICTS = {"pass", "fail", "hold"}

VALID_VERIFIER_DIMENSIONS = {
    "source_reliability",
    "recency",
    "completeness",
    "independence",
    "corroboration",
}

VALID_GATE_NAMES = {
    "source_reliability",
    "recency",
    "completeness",
    "independence",
    "corroboration",
}

VALID_CONFLICT_TYPES = {
    "time_difference",
    "observation_angle",
    "methodology",
    "interest_bias",
    "source_genealogy",
}

VALID_RESOLUTION_STRATEGIES = {
    "prefer_latest",
    "prefer_most_reliable",
    "preserve_both_with_context",
    "prefer_independent_source",
    "methodology_difference",
    "unresolvable",
}


# ── LintReport ─────────────────────────────────────────────────────────────


class LintReport:
    """收集 lint 发现的问题。"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.errors = []
        self.warnings = []

    def error(self, code: str, message: str, location: str = ""):
        self.errors.append({"code": code, "message": message, "location": location})

    def warning(self, code: str, message: str, location: str = ""):
        self.warnings.append({"code": code, "message": message, "location": location})

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def summary(self) -> str:
        lines = []
        status = "FAIL" if self.has_errors else "PASS"
        lines.append(
            f"[{status}] {self.file_path} — "
            f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)"
        )
        for item in self.errors:
            loc = f" @ {item['location']}" if item["location"] else ""
            lines.append(f"  ERROR {item['code']}: {item['message']}{loc}")
        for item in self.warnings:
            loc = f" @ {item['location']}" if item["location"] else ""
            lines.append(f"  WARN  {item['code']}: {item['message']}{loc}")
        return "\n".join(lines)


# ── 证据账本校验 ────────────────────────────────────────────────────────────


def lint_evidence_ledger(data: dict, report: LintReport):
    """校验证据账本的完整性和字段合规性。

    检查每条 entry 的必填字段、status 合法性、confirmed_fact 的来源
    可追溯性，以及 reported_claim 的 corroboration 标记。
    """
    if "entries" not in data:
        # 不是 evidence ledger 格式，跳过
        return

    entries = data.get("entries", [])
    if not isinstance(entries, list):
        report.error(
            "LEDGER_ENTRIES_NOT_LIST",
            f"entries 应为数组，实际为 {type(entries).__name__}",
            "entries",
        )
        return

    if not entries:
        report.warning("LEDGER_EMPTY", "证据账本为空")
        return

    seen_ids = set()
    confirmed_without_source = 0

    for idx, entry in enumerate(entries):
        loc = f"entries[{idx}]"

        if not isinstance(entry, dict):
            report.error("ENTRY_NOT_OBJECT", f"证据条目不是对象", loc)
            continue

        # 必填字段
        entry_id = entry.get("id", "")
        if not entry_id:
            report.error("ENTRY_NO_ID", "证据条目缺少 id", loc)
        elif entry_id in seen_ids:
            report.error("ENTRY_ID_DUPLICATE", f"证据 id 重复: {entry_id}", loc)
        else:
            seen_ids.add(entry_id)

        if not entry.get("claim"):
            report.error("ENTRY_NO_CLAIM", f"证据 {entry_id} 缺少 claim", loc)

        # status 校验
        status = entry.get("status", "")
        if not status:
            report.error(
                "ENTRY_NO_STATUS",
                f"证据 {entry_id} 缺少 status",
                loc,
            )
        elif status not in VALID_ENTRY_STATUS:
            report.error(
                "ENTRY_BAD_STATUS",
                f"证据 {entry_id} status '{status}' 不在合法集合中",
                loc,
            )

        # source_type 校验
        source_type = entry.get("source_type", "")
        if not source_type:
            report.error(
                "ENTRY_NO_SOURCE_TYPE",
                f"证据 {entry_id} 缺少 source_type",
                loc,
            )
        elif source_type not in VALID_SOURCE_TYPE:
            report.error(
                "ENTRY_BAD_SOURCE_TYPE",
                f"证据 {entry_id} source_type '{source_type}' 不在合法集合中",
                loc,
            )

        # reliability 校验
        reliability = entry.get("reliability", "")
        if not reliability:
            report.error(
                "ENTRY_NO_RELIABILITY",
                f"证据 {entry_id} 缺少 reliability",
                loc,
            )
        elif reliability not in VALID_RELIABILITY:
            report.error(
                "ENTRY_BAD_RELIABILITY",
                f"证据 {entry_id} reliability '{reliability}' 不在合法集合中",
                loc,
            )

        # implication 校验
        if not entry.get("implication"):
            report.warning(
                "ENTRY_NO_IMPLICATION",
                f"证据 {entry_id} 缺少 implication",
                loc,
            )

        # confirmed_fact 必须有来源追溯
        if status == "confirmed_fact":
            if not entry.get("source_url") and not entry.get("source_title"):
                report.error(
                    "CONFIRMED_FACT_NO_SOURCE",
                    f"证据 {entry_id} status=confirmed_fact 但无 source_url 或 source_title",
                    loc,
                )
                confirmed_without_source += 1
            if not entry.get("accessed_at") and not entry.get("published_at"):
                report.warning(
                    "CONFIRMED_FACT_NO_DATE",
                    f"证据 {entry_id} status=confirmed_fact 但无 accessed_at 或 published_at",
                    loc,
                )

        # reported_claim 应有 corroboration 标记
        if status == "reported_claim":
            if not entry.get("corroboration_group") and not entry.get(
                "upstream_source_id"
            ):
                report.warning(
                    "REPORTED_CLAIM_NO_CORROB",
                    f"证据 {entry_id} status=reported_claim 但无 corroboration_group "
                    "或 upstream_source_id，无法判断是否为单源",
                    loc,
                )

        # citation_strength 校验
        cs = entry.get("citation_strength", "")
        if cs and cs not in VALID_CITATION_STRENGTH:
            report.error(
                "ENTRY_BAD_CITATION_STRENGTH",
                f"证据 {entry_id} citation_strength '{cs}' 不在合法集合中",
                loc,
            )

        # formal_status_label 校验
        fsl = entry.get("formal_status_label", "")
        if fsl and fsl not in VALID_FORMAL_STATUS:
            report.error(
                "ENTRY_BAD_FORMAL_STATUS",
                f"证据 {entry_id} formal_status_label '{fsl}' 不在合法集合中",
                loc,
            )

        # agent_role 校验
        ar = entry.get("agent_role", "")
        if ar and ar not in VALID_AGENT_ROLES:
            report.warning(
                "ENTRY_BAD_AGENT_ROLE",
                f"证据 {entry_id} agent_role '{ar}' 不在合法集合中",
                loc,
            )

        # formal_status_label 存在时检查 effective_date / application_date
        if fsl and fsl in {
            "final-in-force",
            "applicable-obligation",
            "adopted-not-yet-applicable",
        }:
            if not entry.get("effective_date") and not entry.get("application_date"):
                report.warning(
                    "FORMAL_STATUS_NO_DATE",
                    f"证据 {entry_id} formal_status_label='{fsl}' 但无 effective_date 或 application_date",
                    loc,
                )

    # 全局检查：confirmed_fact 占比过低
    if entries:
        confirmed_count = sum(
            1
            for e in entries
            if isinstance(e, dict) and e.get("status") == "confirmed_fact"
        )
        if confirmed_without_source > 0:
            report.error(
                "CONFIRMED_FACT_SOURCE_GAP",
                f"{confirmed_without_source} 条 confirmed_fact 缺少来源追溯",
                "entries",
            )


# ── 状态机校验 ──────────────────────────────────────────────────────────────


def lint_state_machine(data: dict, report: LintReport):
    """校验研究任务状态机的合法转移。

    检查 task 状态是否在合法集合中、转移序列是否合法、accepted 是否
    仅来自 passed、retrying 是否携带 retry_patch、cycle_count 超限
    是否进入 escalated。
    """
    tasks = data.get("tasks", [])
    if not tasks:
        # 尝试单任务格式
        task = _extract_single_task(data)
        if task:
            tasks = [task]
        else:
            return

    for idx, task in enumerate(tasks):
        if not isinstance(task, dict):
            continue

        task_id = task.get("task_id", f"task[{idx}]")
        loc_base = f"task {task_id}"

        state = task.get("state", "")
        if not state:
            report.warning(
                "STATE_MISSING",
                f"{loc_base} 缺少 state 字段",
                loc_base,
            )
            continue

        if state not in VALID_STATES:
            report.error(
                "STATE_INVALID",
                f"{loc_base} state '{state}' 不在合法集合中",
                loc_base,
            )
            continue

        # 状态转移序列校验
        state_log = task.get("state_log", [])
        if isinstance(state_log, list) and state_log:
            _lint_state_log(state_log, report, loc_base, task)

        # accepted 只能来自 passed
        if state == "accepted":
            if not _has_transition_from(state_log, "passed", "accepted"):
                report.error(
                    "ACCEPTED_NOT_FROM_PASSED",
                    f"{loc_base} state=accepted 但未经过 passed 状态",
                    loc_base,
                )

        # retrying 必须携带 retry_patch
        if state == "retrying":
            retry_patch = task.get("retry_patch")
            if not retry_patch:
                # 也检查 state_log 中最后一条是否有
                found_patch = False
                if isinstance(state_log, list):
                    for entry in reversed(state_log):
                        if isinstance(entry, dict) and entry.get("retry_patch"):
                            found_patch = True
                            break
                if not found_patch:
                    report.error(
                        "RETRYING_NO_PATCH",
                        f"{loc_base} state=retrying 但无 retry_patch",
                        loc_base,
                    )

        # cycle_count > max_cycles 必须进入 escalated
        max_cycles = task.get("max_cycles", 0)
        cycle_count = task.get("cycle_count", 0)
        if isinstance(max_cycles, int) and isinstance(cycle_count, int):
            if cycle_count > max_cycles and state != "escalated":
                report.error(
                    "MAX_CYCLES_NOT_ESCALATED",
                    f"{loc_base} cycle_count ({cycle_count}) > max_cycles ({max_cycles}) "
                    f"但 state='{state}' 而非 'escalated'",
                    loc_base,
                )

        # 依赖门禁：检查 dependency 是否已 passed
        dependency_ids = task.get("dependency_ids", [])
        if dependency_ids and isinstance(dependency_ids, list) and tasks:
            for dep_id in dependency_ids:
                dep_task = _find_task(tasks, dep_id)
                if dep_task and dep_task.get("state") not in {"passed", "accepted"}:
                    if state not in {"planned"}:
                        report.error(
                            "DEPENDENCY_GATE_VIOLATION",
                            f"{loc_base} 依赖 {dep_id} 未 passed/accepted 但本任务 state='{state}'",
                            loc_base,
                        )


def _extract_single_task(data: dict) -> dict | None:
    """从单任务格式中提取 task 信息。"""
    if "task_id" in data and "state" in data:
        return data
    return None


def _find_task(tasks: list, task_id: str) -> dict | None:
    """在任务列表中查找指定 task_id 的任务。"""
    for task in tasks:
        if isinstance(task, dict) and task.get("task_id") == task_id:
            return task
    return None


def _lint_state_log(
    state_log: list, report: LintReport, loc_base: str, task: dict
):
    """校验状态转移日志的合法性。"""
    for idx, entry in enumerate(state_log):
        if not isinstance(entry, dict):
            continue

        loc = f"{loc_base}.state_log[{idx}]"
        from_state = entry.get("from", "")
        to_state = entry.get("to", "")

        if not to_state:
            report.error("STATE_LOG_NO_TO", f"{loc} 缺少 to 字段", loc)
            continue

        if to_state not in VALID_STATES:
            report.error(
                "STATE_LOG_BAD_TO",
                f"{loc} to '{to_state}' 不在合法集合中",
                loc,
            )
            continue

        if from_state and from_state not in VALID_STATES:
            report.error(
                "STATE_LOG_BAD_FROM",
                f"{loc} from '{from_state}' 不在合法集合中",
                loc,
            )
            continue

        if from_state and from_state in VALID_STATE_TRANSITIONS:
            allowed = VALID_STATE_TRANSITIONS[from_state]
            if to_state not in allowed:
                report.error(
                    "STATE_LOG_BAD_TRANSITION",
                    f"{loc} 转移 {from_state} -> {to_state} 不合法",
                    loc,
                )


def _has_transition_from(state_log: list, from_state: str, to_state: str) -> bool:
    """检查状态日志中是否存在指定的转移。"""
    for entry in state_log:
        if isinstance(entry, dict):
            if entry.get("from") == from_state and entry.get("to") == to_state:
                return True
    return False


# ── 质量门禁校验 ──────────────────────────────────────────────────────────────


def lint_quality_gates(data: dict, report: LintReport):
    """校验质量门禁的合规性。

    检查 evidence_quality_gates 是否存在且 gate 名称合法，
    以及 verification report 的 verdict 是否与维度状态一致。
    """
    # 检查 ResearchEnvelope 中的 evidence_quality_gates
    gates = data.get("evidence_quality_gates", [])
    if isinstance(gates, list) and gates:
        for idx, gate in enumerate(gates):
            if not isinstance(gate, dict):
                continue
            loc = f"evidence_quality_gates[{idx}]"
            gate_name = gate.get("gate", "")
            if not gate_name:
                report.error("GATE_NO_NAME", f"{loc} 缺少 gate 字段", loc)
            elif gate_name not in VALID_GATE_NAMES:
                report.error(
                    "GATE_BAD_NAME",
                    f"{loc} gate '{gate_name}' 不在合法集合中",
                    loc,
                )
            if not gate.get("threshold"):
                report.warning(
                    "GATE_NO_THRESHOLD",
                    f"{loc} 缺少 threshold",
                    loc,
                )

    # 检查 verification report
    verdict = data.get("verdict", "")
    if verdict:
        if verdict not in VALID_VERDICTS:
            report.error(
                "VERDICT_INVALID",
                f"verdict '{verdict}' 不在 pass/fail/hold 中",
                "verdict",
            )

        # verdict=fail 必须有 retry_patch
        if verdict == "fail":
            if not data.get("retry_patch"):
                report.error(
                    "FAIL_NO_RETRY_PATCH",
                    "verdict=fail 但无 retry_patch",
                    "retry_patch",
                )

        # verified_dimensions 校验
        dims = data.get("verified_dimensions", {})
        if isinstance(dims, dict) and dims:
            for dim_name, dim_data in dims.items():
                if dim_name not in VALID_VERIFIER_DIMENSIONS:
                    report.warning(
                        "DIM_BAD_NAME",
                        f"verified_dimensions.{dim_name} 不在标准维度集合中",
                        f"verified_dimensions.{dim_name}",
                    )
                if isinstance(dim_data, dict):
                    dim_status = dim_data.get("status", "")
                    if dim_status and dim_status not in {"pass", "fail", "hold"}:
                        report.error(
                            "DIM_BAD_STATUS",
                            f"verified_dimensions.{dim_name}.status '{dim_status}' 不合法",
                            f"verified_dimensions.{dim_name}",
                        )

        # verdict=pass 但有 fail 维度
        if verdict == "pass" and isinstance(dims, dict):
            for dim_name, dim_data in dims.items():
                if isinstance(dim_data, dict) and dim_data.get("status") == "fail":
                    report.warning(
                        "PASS_WITH_FAIL_DIM",
                        f"verdict=pass 但 {dim_name}.status=fail",
                        f"verified_dimensions.{dim_name}",
                    )

    # 检查 confirmed/rejected evidence IDs
    confirmed_ids = data.get("confirmed_evidence_ids", [])
    rejected_ids = data.get("rejected_evidence_ids", [])
    if isinstance(confirmed_ids, list) and isinstance(rejected_ids, list):
        overlap = set(confirmed_ids) & set(rejected_ids)
        if overlap:
            report.error(
                "EVIDENCE_ID_IN_BOTH",
                f"证据 ID 同时出现在 confirmed 和 rejected 中: {overlap}",
                "confirmed_evidence_ids",
            )


# ── 并行执行校验 ────────────────────────────────────────────────────────────


def lint_parallel_execution(data: dict, report: LintReport):
    """校验并行研究执行的合规性。

    检查 ResearchCycleReport 的任务汇总、合并判断、冲突处理
    和覆盖缺口是否完整。
    """
    # 判断是否为 ResearchCycleReport
    if "research_sprint_id" not in data and "tasks_summary" not in data:
        return

    loc_base = "research_cycle_report"

    # tasks_summary 校验
    tasks_summary = data.get("tasks_summary", {})
    if isinstance(tasks_summary, dict):
        total = tasks_summary.get("total", 0)
        completed = tasks_summary.get("completed", 0)
        in_progress = tasks_summary.get("in_progress", 0)
        blocked = tasks_summary.get("blocked", 0)

        if isinstance(total, int) and isinstance(completed, int):
            if completed > total:
                report.error(
                    "SUMMARY_COMPLETED_EXCEEDS_TOTAL",
                    f"completed ({completed}) > total ({total})",
                    f"{loc_base}.tasks_summary",
                )

        if isinstance(total, int) and total > 0:
            expected_sum = (
                (completed if isinstance(completed, int) else 0)
                + (in_progress if isinstance(in_progress, int) else 0)
                + (blocked if isinstance(blocked, int) else 0)
            )
            # 允许差异（有些任务可能既不在 completed 也不在 in_progress/blocked）
            if expected_sum > total:
                report.warning(
                    "SUMMARY_COUNTS_EXCEED_TOTAL",
                    f"completed + in_progress + blocked ({expected_sum}) > total ({total})",
                    f"{loc_base}.tasks_summary",
                )

    # merge_judgment 校验
    merge_judgment = data.get("merge_judgment", {})
    if isinstance(merge_judgment, dict):
        accepted_lanes = merge_judgment.get("accepted_lanes", [])
        rejected_lanes = merge_judgment.get("rejected_lanes", [])
        downgraded_lanes = merge_judgment.get("downgraded_lanes", [])

        for lane_list, lane_type in [
            (accepted_lanes, "accepted"),
            (rejected_lanes, "rejected"),
            (downgraded_lanes, "downgraded"),
        ]:
            if lane_list and not isinstance(lane_list, list):
                report.error(
                    "MERGE_LANES_NOT_LIST",
                    f"merge_judgment.{lane_type} 应为数组",
                    f"{loc_base}.merge_judgment.{lane_type}",
                )

    # evidence_ledger_stats 校验
    stats = data.get("evidence_ledger_stats", {})
    if isinstance(stats, dict):
        total_entries = stats.get("total_entries", 0)
        confirmed = stats.get("confirmed", 0)
        rejected = stats.get("rejected", 0)
        flagged = stats.get("flagged", 0)

        if (
            isinstance(total_entries, int)
            and isinstance(confirmed, int)
            and isinstance(rejected, int)
            and isinstance(flagged, int)
        ):
            if confirmed + rejected + flagged > total_entries:
                report.warning(
                    "STATS_COUNTS_EXCEED_TOTAL",
                    f"confirmed + rejected + flagged ({confirmed + rejected + flagged}) "
                    f"> total_entries ({total_entries})",
                    f"{loc_base}.evidence_ledger_stats",
                )

    # coverage_gaps 校验
    gaps = data.get("coverage_gaps", {})
    if isinstance(gaps, dict):
        for level in ("critical", "medium", "low"):
            items = gaps.get(level)
            if items is not None and not isinstance(items, list):
                report.error(
                    "GAPS_NOT_LIST",
                    f"coverage_gaps.{level} 应为数组",
                    f"{loc_base}.coverage_gaps.{level}",
                )

    # next_action 校验
    if not data.get("next_action"):
        report.warning(
            "NO_NEXT_ACTION",
            "ResearchCycleReport 缺少 next_action",
            loc_base,
        )


# ── 冲突解决校验 ────────────────────────────────────────────────────────────


def lint_conflict_resolution(data: dict, report: LintReport):
    """校验冲突解决报告的合规性。

    检查 conflicts_analyzed 的结构、resolution_decision 的合法性
    和 unresolved_conflicts 的处理。
    """
    # 判断是否为 ConflictResolutionReport
    conflicts = data.get("conflicts_analyzed", [])
    if not conflicts:
        return

    if not isinstance(conflicts, list):
        report.error(
            "CONFLICTS_NOT_LIST",
            "conflicts_analyzed 应为数组",
            "conflicts_analyzed",
        )
        return

    loc_base = "conflict_resolution_report"

    for idx, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            continue

        loc = f"{loc_base}.conflicts_analyzed[{idx}]"
        conflict_id = conflict.get("conflict_id", "")

        # conflict_type 校验
        ct = conflict.get("conflict_type", "")
        if ct and ct not in VALID_CONFLICT_TYPES:
            report.error(
                "CONFLICT_BAD_TYPE",
                f"{loc} conflict_type '{ct}' 不在合法集合中",
                loc,
            )

        # resolution_decision 校验
        decision = conflict.get("resolution_decision", {})
        if isinstance(decision, dict):
            strategy = decision.get("strategy", "")
            if strategy and strategy not in VALID_RESOLUTION_STRATEGIES:
                report.error(
                    "CONFLICT_BAD_STRATEGY",
                    f"{loc} resolution_decision.strategy '{strategy}' 不在合法集合中",
                    loc,
                )
            if not decision.get("reasoning"):
                report.warning(
                    "CONFLICT_NO_REASONING",
                    f"{loc} resolution_decision 缺少 reasoning",
                    loc,
                )
        elif not decision:
            report.error(
                "CONFLICT_NO_DECISION",
                f"{loc} 缺少 resolution_decision",
                loc,
            )

        # claim_a / claim_b 校验
        for claim_key in ("claim_a", "claim_b"):
            claim = conflict.get(claim_key)
            if claim and isinstance(claim, dict):
                if not claim.get("statement"):
                    report.warning(
                        "CONFLICT_CLAIM_NO_STATEMENT",
                        f"{loc}.{claim_key} 缺少 statement",
                        f"{loc}.{claim_key}",
                    )
                if not claim.get("source"):
                    report.warning(
                        "CONFLICT_CLAIM_NO_SOURCE",
                        f"{loc}.{claim_key} 缺少 source",
                        f"{loc}.{claim_key}",
                    )

    # unresolved_conflicts 校验
    unresolved = data.get("unresolved_conflicts", [])
    if isinstance(unresolved, list) and unresolved:
        escalation_needed = data.get("escalation_needed")
        if escalation_needed is False:
            report.warning(
                "UNRESOLVED_NO_ESCALATION",
                f"有 {len(unresolved)} 条未解决冲突但 escalation_needed=false",
                loc_base,
            )


# ── JSON Schema 校验 ──────────────────────────────────────────────────────────


# Schema 文件路径映射
SCHEMA_FILES = {
    "evidence_ledger": "evidence-ledger.schema.json",
    "research_envelope": "research-envelope.schema.json",
    "verification_report": "verification-report.schema.json",
    "conflict_resolution": "conflict-resolution-report.schema.json",
}

# Schema 目录（相对于 skill 根目录）
SCHEMA_DIR = Path(__file__).parent.parent / "references"


def _try_load_schema(schema_name: str) -> dict | None:
    """尝试加载 JSON Schema 文件，失败时返回 None。"""
    filename = SCHEMA_FILES.get(schema_name)
    if not filename:
        return None
    schema_path = SCHEMA_DIR / filename
    if not schema_path.exists():
        return None
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _detect_schema_type(data: dict) -> str | None:
    """根据数据特征推断应使用哪个 schema。"""
    if "entries" in data and "research_object" in data:
        return "evidence_ledger"
    if "task_id" in data and "researcher_role" in data:
        return "research_envelope"
    if "verdict" in data and "verified_dimensions" in data:
        return "verification_report"
    if "conflicts_analyzed" in data:
        return "conflict_resolution"
    return None


def lint_json_schema(data: dict, report: LintReport):
    """使用 JSON Schema 校验数据结构。

    优先使用 jsonschema 库进行完整校验；
    如果库不可用，执行轻量一致性检查（比对 schema 中的 enum 值
    与 lint 脚本中的常量集合是否一致）。
    """
    schema_type = _detect_schema_type(data)
    if not schema_type:
        return

    schema = _try_load_schema(schema_type)
    if not schema:
        report.warning(
            "SCHEMA_FILE_NOT_FOUND",
            f"未找到 {schema_type} 对应的 schema 文件",
            SCHEMA_FILES.get(schema_type, ""),
        )
        return

    # 尝试使用 jsonschema 库
    try:
        import jsonschema

        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as exc:
            report.error(
                "SCHEMA_VALIDATION_ERROR",
                f"JSON Schema 校验失败: {exc.message}",
                str(exc.absolute_path) if exc.absolute_path else "",
            )
        except jsonschema.SchemaError as exc:
            report.warning(
                "SCHEMA_DEFINITION_ERROR",
                f"Schema 定义本身有问题: {exc.message}",
                SCHEMA_FILES.get(schema_type, ""),
            )
        return
    except ImportError:
        pass

    # Fallback: 轻量一致性检查
    _lint_schema_consistency(data, schema, schema_type, report)


def _lint_schema_consistency(
    data: dict, schema: dict, schema_type: str, report: LintReport
):
    """轻量一致性检查：比对 schema enum 与 lint 常量集合。

    这不替代 jsonschema 的完整校验，但能发现 schema 和 lint
    常量之间的漂移。
    """
    # 检查 schema 中的 enum 值是否与 lint 常量一致
    schema_enums = _extract_schema_enums(schema)
    lint_constants = {
        "status": VALID_ENTRY_STATUS,
        "source_type": VALID_SOURCE_TYPE,
        "reliability": VALID_RELIABILITY,
        "citation_strength": VALID_CITATION_STRENGTH,
        "formal_status_label": VALID_FORMAL_STATUS,
        "agent_role": VALID_AGENT_ROLES,
        "verdict": VALID_VERDICTS,
        "conflict_type": VALID_CONFLICT_TYPES,
        "resolution_strategy": VALID_RESOLUTION_STRATEGIES,
    }

    for field_name, schema_values in schema_enums.items():
        lint_values = lint_constants.get(field_name)
        if lint_values is None:
            continue
        # 检查 schema 中有但 lint 中没有的值
        missing_in_lint = schema_values - lint_values
        if missing_in_lint:
            report.warning(
                "SCHEMA_LINT_DRIFT",
                f"Schema 中 {field_name} 有值 {missing_in_lint} "
                f"但 lint 常量中不存在",
                f"schema.{field_name}",
            )
        # 检查 lint 中有但 schema 中没有的值
        missing_in_schema = lint_values - schema_values
        if missing_in_schema:
            report.warning(
                "LINT_SCHEMA_DRIFT",
                f"Lint 常量 {field_name} 有值 {missing_in_schema} "
                f"但 Schema 中不存在",
                f"lint.{field_name}",
            )


def _extract_schema_enums(schema: dict) -> dict[str, set[str]]:
    """递归提取 schema 中所有 enum 值，以 property 名为 key。"""
    result: dict[str, set[str]] = {}

    def _walk(node: dict):
        if not isinstance(node, dict):
            return
        if "enum" in node and isinstance(node["enum"], list):
            # 尝试找到 property 名
            prop_name = node.get("title", "")
            if not prop_name and "properties" in node:
                prop_name = list(node.get("properties", {}).keys())
            if isinstance(prop_name, str) and prop_name:
                result.setdefault(prop_name, set()).update(node["enum"])
        for value in node.values():
            if isinstance(value, dict):
                _walk(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        _walk(item)

    _walk(schema)
    return result


# ── Markdown 校验 ─────────────────────────────────────────────────────────────


# 空话标记词（Style Gate 可执行部分）
EMPTY_PHRASE_PATTERNS = [
    r"\bleverage[sd]?\b",
    r"\bsynerg(?:y|ies|istic)\b",
    r"\brevolutionary\b",
    r"\bgame[- ]changer\b",
    r"\bparadigm shift\b",
    r"\bcutting[- ]edge\b",
    r"\bworld[- ]class\b",
    r"\bbest[- ]in[- ]class\b",
    r"\bnext[- ]generation\b",
    r"\bdisruptive innovation\b",
]

# Evidence ID 引用模式: [E-001], [E-002], etc.
EVIDENCE_ID_PATTERN = re.compile(r"\[E-\d+\]")

# Evidence window 声明模式
EVIDENCE_WINDOW_PATTERNS = [
    r"[Ee]vidence (?:window|checked)[:\s]+",
    r"[Ss]ource window[:\s]+",
    r"[Ee]vidence checked through\b",
    r"\u8bc1\u636e\u7a97\u53e3[:\uff1a]",
    r"\u6765\u6e90\u7a97\u53e3[:\uff1a]",
]

# Confidence level 声明模式
CONFIDENCE_PATTERNS = [
    r"[Cc]onfidence[:\s]+",
    r"\u7f6e\u4fe1\u5ea6[:\uff1a]",
]


def lint_markdown(path: str) -> LintReport:
    """\u6821\u9a8c\u7814\u7a76\u8f93\u51fa Markdown \u6587\u4ef6\u7684\u5408\u89c4\u6027\u3002

    \u68c0\u67e5\uff1a\u8bc1\u636e\u7a97\u53e3\u58f0\u660e\u3001Evidence ID \u5f15\u7528\u3001\u7f6e\u4fe1\u5ea6\u58f0\u660e\u3001
    \u53cd\u8f6c\u6761\u4ef6\u5b58\u5728\u3001\u7a7a\u8bdd\u6807\u8bb0\u8bcd\u3001\u6765\u6e90\u5f15\u7528\u5b58\u5728\u3002
    """
    report = LintReport(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeDecodeError) as exc:
        report.error("FILE_READ_ERROR", f"\u6587\u4ef6\u8bfb\u53d6\u5931\u8d25: {type(exc).__name__}: {exc}")
        return report

    if not content.strip():
        report.error("MD_EMPTY", "Markdown \u6587\u4ef6\u4e3a\u7a7a")
        return report

    lines = content.split("\n")
    total_lines = len(lines)

    # 1. \u8bc1\u636e\u7a97\u53e3\u58f0\u660e\u68c0\u67e5
    has_evidence_window = any(
        re.search(pattern, content, re.IGNORECASE)
        for pattern in EVIDENCE_WINDOW_PATTERNS
    )
    if not has_evidence_window:
        report.warning(
            "MD_NO_EVIDENCE_WINDOW",
            "\u672a\u627e\u5230\u8bc1\u636e\u7a97\u53e3\u58f0\u660e\uff08\u5982 'Evidence checked through' \u6216 '\u8bc1\u636e\u7a97\u53e3'\uff09",
            "content",
        )

    # 2. Evidence ID \u5f15\u7528\u68c0\u67e5
    evidence_refs = EVIDENCE_ID_PATTERN.findall(content)
    if not evidence_refs:
        report.warning(
            "MD_NO_EVIDENCE_REFS",
            "\u672a\u627e\u5230 [E-xxx] \u683c\u5f0f\u7684\u8bc1\u636e ID \u5f15\u7528\uff1b\u5bf9\u4e8e\u6df1\u5ea6\u7814\u7a76\u62a5\u544a\u6216\u51b3\u7b56\u7b80\u62a5\uff0c\u5e94\u5728\u5173\u952e\u7ed3\u8bba\u65c1\u6807\u6ce8\u8bc1\u636e ID",
            "content",
        )
    else:
        unique_refs = set(evidence_refs)
        report._evidence_ref_count = len(unique_refs)  # type: ignore[attr-defined]

    # 3. \u7f6e\u4fe1\u5ea6\u58f0\u660e\u68c0\u67e5
    has_confidence = any(
        re.search(pattern, content, re.IGNORECASE)
        for pattern in CONFIDENCE_PATTERNS
    )
    if not has_confidence:
        report.warning(
            "MD_NO_CONFIDENCE",
            "\u672a\u627e\u5230\u7f6e\u4fe1\u5ea6\u58f0\u660e\uff08Confidence / \u7f6e\u4fe1\u5ea6\uff09",
            "content",
        )

    # 4. \u53cd\u8f6c\u6761\u4ef6\u68c0\u67e5\uff08\u5bf9\u4e8e\u51b3\u7b56\u7b80\u62a5\u548c\u6df1\u5ea6\u62a5\u544a\uff09
    reversal_keywords = [
        "reversal condition",
        "\u53cd\u8f6c\u6761\u4ef6",
        "what would change",
        "what would make this wrong",
        "monitoring signal",
        "\u76d1\u63a7\u4fe1\u53f7",
    ]
    content_lower = content.lower()
    has_reversal = any(kw in content_lower for kw in reversal_keywords)
    is_decision_or_deep = any(
        kw in content_lower
        for kw in ["decision", "verdict", "go / hold", "\u51b3\u7b56", "go/no-go", "go / no-go"]
    )
    if is_decision_or_deep and not has_reversal:
        report.error(
            "MD_NO_REVERSAL_CONDITIONS",
            "\u51b3\u7b56\u7c7b\u8f93\u51fa\u7f3a\u5c11\u53cd\u8f6c\u6761\u4ef6\u58f0\u660e",
            "content",
        )

    # 5. Style Gate: \u7a7a\u8bdd\u6807\u8bb0\u8bcd\u68c0\u67e5
    for idx, line in enumerate(lines):
        for pattern in EMPTY_PHRASE_PATTERNS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                report.warning(
                    "MD_EMPTY_PHRASE",
                    f"\u7a7a\u8bdd\u6807\u8bb0\u8bcd: '{match.group()}'",
                    f"line {idx + 1}",
                )

    # 6. \u6765\u6e90\u5f15\u7528\u5b58\u5728\u6027\u68c0\u67e5\uff08\u81f3\u5c11\u6709 URL \u6216\u6765\u6e90\u6807\u9898\uff09
    url_count = len(re.findall(r"https?://", content))
    if url_count == 0:
        report.warning(
            "MD_NO_SOURCES",
            "\u672a\u627e\u5230\u4efb\u4f55 URL \u6765\u6e90\u5f15\u7528\uff1b\u7814\u7a76\u8f93\u51fa\u5e94\u5305\u542b\u53ef\u8ffd\u6eaf\u7684\u6765\u6e90",
            "content",
        )

    # 7. \u6587\u4ef6\u592a\u77ed\u68c0\u67e5\uff08\u53ef\u80fd\u662f\u5360\u4f4d\u7b26\uff09
    if total_lines < 10:
        report.warning(
            "MD_TOO_SHORT",
            f"\u6587\u4ef6\u4ec5 {total_lines} \u884c\uff0c\u53ef\u80fd\u662f\u5360\u4f4d\u7b26\u6216\u672a\u5b8c\u6210\u7684\u8f93\u51fa",
            "content",
        )

    return report


# ── 主入口 ─────────────────────────────────────────────────────────────────────


def lint_file(path: str) -> LintReport:
    """\u5bf9\u5355\u4e2a\u6587\u4ef6\u6267\u884c lint \u68c0\u67e5\u3002\u81ea\u52a8\u8bc6\u522b JSON \u548c Markdown \u683c\u5f0f\u3002"""
    report = LintReport(path)

    # \u6839\u636e\u6587\u4ef6\u6269\u5c55\u540d\u8def\u7531\u5230\u4e0d\u540c\u7684 linter
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix == ".md":
        return lint_markdown(path)

    # JSON path
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        report.error("JSON_PARSE_ERROR", f"JSON 解析失败: {exc}")
        return report
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeDecodeError) as exc:
        report.error("FILE_READ_ERROR", f"文件读取失败: {type(exc).__name__}: {exc}")
        return report

    if not isinstance(data, dict):
        report.error(
            "OUTPUT_NOT_OBJECT",
            f"输出顶层应为 JSON 对象，实际为 {type(data).__name__}",
        )
        return report

    # 按输出类型执行对应检查
    lint_evidence_ledger(data, report)
    lint_state_machine(data, report)
    lint_quality_gates(data, report)
    lint_parallel_execution(data, report)
    lint_conflict_resolution(data, report)
    lint_json_schema(data, report)

    return report


def main() -> int:
    """脚本入口，支持单文件或通配符。"""
    parser = argparse.ArgumentParser(
        description="Lint Deep Research Forge output files (JSON + Markdown)."
    )
    parser.add_argument("paths", nargs="+", help="输出文件路径或通配符 (.json 或 .md)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="warning 也视为失败（退出码 1）",
    )
    args = parser.parse_args()

    files = []
    for pattern in args.paths:
        matched = sorted(glob.glob(pattern))
        if matched:
            files.extend(matched)
        elif Path(pattern).exists():
            files.append(pattern)

    if not files:
        print("No files matched.", file=sys.stderr)
        return 1

    has_failures = False
    for path in files:
        report = lint_file(path)
        print(report.summary())
        if report.has_errors:
            has_failures = True
        if args.strict and report.warnings:
            has_failures = True

    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
