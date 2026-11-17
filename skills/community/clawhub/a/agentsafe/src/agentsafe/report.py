"""Report building: merge, dedupe, summarize. Zero findings NEVER equals safe.

Dedup rules (Prompt 7):
- detector-keyed findings merge by (detector_id, file, line) even with
  different titles;
- LLM findings merge into tool findings when location overlaps or evidence is
  strongly similar (cross-support is preserved, not discarded);
- every merge keeps ALL original sources in `source` and records merged_from.
"""

from __future__ import annotations

import difflib
import logging
import re
from collections.abc import Sequence
from datetime import UTC, datetime

from agentsafe import CHAIN_ID, REPORT_DISCLAIMER
from agentsafe.schemas import (
    AuditReport,
    Finding,
    FindingStatus,
    LLMUsage,
    ReportSummary,
    Severity,
)

logger = logging.getLogger("agentSAFE.report")

_SEVERITY_ORDER = {
    Severity.CRITICAL: 0,
    Severity.HIGH: 1,
    Severity.MEDIUM: 2,
    Severity.LOW: 3,
    Severity.INFO: 4,
}
_EVIDENCE_SIMILARITY = 0.60
_LINE_TOLERANCE = 5


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, _norm(a)[:2000], _norm(b)[:2000]).ratio()


def _loc(f: Finding) -> tuple[str | None, int | None]:
    return ((f.file_path or "").lower() or None), f.line_start


def merge_findings(findings: Sequence[Finding]) -> list[Finding]:
    """Deterministic, testable merge. Tool findings dominate; LLM findings
    either merge into them (adding source + evidence) or survive standalone."""
    tool = [f for f in findings if f.status == FindingStatus.TOOL_DETECTED]
    llm = [f for f in findings if f.status == FindingStatus.LLM_SUGGESTED]
    other = [
        f
        for f in findings
        if f.status in (FindingStatus.CROSS_CHECKED, FindingStatus.MANUAL_REVIEW)
    ]

    # 1) detector merge among tool findings
    merged_tool: dict[tuple, Finding] = {}
    for f in tool:
        key = f.merge_key()
        if key in merged_tool:
            merged_tool[key] = _absorb(merged_tool[key], f)
        else:
            merged_tool[key] = f

    tool_list = list(merged_tool.values())

    # 2) LLM findings: attach to overlapping tool findings, or keep standalone
    standalone: list[Finding] = []
    for f in llm:
        host = _find_host(f, tool_list)
        if host is not None:
            _absorb_into(host, f, cross=True)
        else:
            standalone.append(f)

    # 3) LLM-vs-LLM duplicates by normalized title+location
    deduped: dict[tuple, Finding] = {}
    for f in standalone:
        llm_key = ("llm", *_loc(f), _norm(f.title)[:120])
        if llm_key in deduped:
            deduped[llm_key] = _absorb(deduped[llm_key], f)
        else:
            deduped[llm_key] = f

    out = tool_list + list(deduped.values()) + list(other)
    out.sort(key=lambda f: (_SEVERITY_ORDER[f.severity], f.status.value, f.title))
    return out


def _absorb(primary: Finding, duplicate: Finding) -> Finding:
    """Return primary carrying duplicate's sources/evidence (never loses info)."""
    merged = primary.model_copy(deep=True)
    _absorb_into(merged, duplicate)
    return merged


def _absorb_into(host: Finding, dup: Finding, *, cross: bool = False) -> None:
    for s in dup.source:
        if s not in host.source:
            host.source.append(s)
    host.metadata.setdefault("merged_from", [])
    host.metadata["merged_from"].append(
        {
            "source": dup.source,
            "title": dup.title,
            "status": dup.status.value,
            "detector_id": dup.detector_id,
        }
    )
    if _norm(dup.evidence) and _norm(dup.evidence) not in _norm(host.evidence):
        host.evidence = (host.evidence + "\n--- additional evidence ---\n" + dup.evidence)[:4000]
    if dup.confidence is not None:
        host.confidence = max(host.confidence or 0.0, dup.confidence)
    if (
        cross
        and dup.severity in _SEVERITY_ORDER
        and _SEVERITY_ORDER[dup.severity] < _SEVERITY_ORDER[host.severity]
    ):
        host.severity = dup.severity  # cross-support may raise severity


def _find_host(candidate: Finding, tools: Sequence[Finding]) -> Finding | None:
    best: Finding | None = None
    best_score = 0.0
    for t in tools:
        score = 0.0
        (cf, cl), (tf, tl) = _loc(candidate), _loc(t)
        if cf and tf and cf == tf:
            if cl is None or tl is None or abs(cl - tl) <= _LINE_TOLERANCE:
                score = 0.9
        if score == 0.0:
            ev = _similar(candidate.evidence, t.evidence)
            ti = _similar(candidate.title, t.title)
            if ev >= _EVIDENCE_SIMILARITY and ti >= 0.4:
                score = ev * 0.85
        if score > best_score:
            best, best_score = t, score
    return best if best_score >= _EVIDENCE_SIMILARITY else None


def summarize(
    findings: Sequence[Finding], tools_executed: Sequence[str], tools_failed: Sequence[str]
) -> ReportSummary:
    by_sev: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for f in findings:
        by_sev[f.severity.value] = by_sev.get(f.severity.value, 0) + 1
        by_status[f.status.value] = by_status.get(f.status.value, 0) + 1
    return ReportSummary(
        total_findings=len(findings),
        by_severity=by_sev,
        by_status=by_status,
        tools_executed=list(tools_executed),
        tools_failed=list(tools_failed),
    )


def build_report(
    *,
    address: str,
    task_id: str | None,
    is_verified_source: bool,
    raw_findings: Sequence[Finding],
    tools_executed: Sequence[str],
    tools_failed: Sequence[str],
    tool_versions: dict[str, str],
    llm_usage: LLMUsage,
    limitations: Sequence[str],
    errors: Sequence[str],
    execution_time_seconds: float,
) -> AuditReport:
    findings = merge_findings(raw_findings)
    return AuditReport(
        address=address,
        chain=CHAIN_ID,
        task_id=task_id,
        timestamp=datetime.now(UTC),
        is_verified_source=is_verified_source,
        summary=summarize(findings, tools_executed, tools_failed),
        findings=findings,
        tools_used=sorted(set(tools_executed) | set(tools_failed)),
        tool_versions=dict(tool_versions),
        llm_usage=llm_usage,
        limitations=list(limitations),
        errors=list(errors),
        execution_time_seconds=round(execution_time_seconds, 2),
        disclaimer=REPORT_DISCLAIMER,
    )
