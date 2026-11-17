"""Core data models for agentSAFE MCP.

Every finding from any analyzer (Slither, Aderyn, Mythril, Heimdall, LLM agents)
MUST normalize to `Finding`. Status values never imply "contract is safe".
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from agentsafe import CHAIN_ID, REPORT_DISCLAIMER

_ADDRESS_RE = re.compile(r"^0[xX][0-9a-fA-F]{40}$")


def normalize_address(value: str) -> str:
    """Validate and normalize a 20-byte EVM address to lowercase 0x-hex."""
    v = (value or "").strip()
    if not _ADDRESS_RE.match(v):
        raise ValueError(f"invalid EVM address: {value!r} (expected '0x' + 40 hex characters)")
    return v.lower()


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(StrEnum):
    """Verification status of a finding.

    - tool_detected: a deterministic tool reported it (not yet proven exploitable)
    - llm_suggested: LLM hypothesis requiring evidence
    - cross_checked: independent, traceable supporting evidence attached
    - manual_review: needs human confirmation
    None of these states may be used to claim "the contract is safe".
    """

    TOOL_DETECTED = "tool_detected"
    LLM_SUGGESTED = "llm_suggested"
    CROSS_CHECKED = "cross_checked"
    MANUAL_REVIEW = "manual_review"


class TaskState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class StageState(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Finding(BaseModel):
    """A single normalized audit finding. See E_VERSION_PLAN section 5."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=300)
    severity: Severity
    status: FindingStatus
    source: list[str] = Field(min_length=1)
    detector_id: str | None = None
    description: str = Field(min_length=1)
    evidence: str = ""
    recommendation: str = ""
    file_path: str | None = None
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("source")
    @classmethod
    def _validate_source(cls, v: list[str]) -> list[str]:
        cleaned = [s.strip().lower() for s in v if s and s.strip()]
        if not cleaned:
            raise ValueError("source must contain at least one non-empty tool/agent name")
        return cleaned

    @field_validator("evidence")
    @classmethod
    def _validate_evidence(cls, v: str, info) -> str:
        status = info.data.get("status")
        if status != FindingStatus.MANUAL_REVIEW and not v.strip():
            raise ValueError(
                "evidence is required unless status is manual_review; "
                "findings without evidence must never be presented as confirmed"
            )
        return v

    @field_validator("line_end")
    @classmethod
    def _validate_line_range(cls, v: int | None, info) -> int | None:
        start = info.data.get("line_start")
        if v is not None and start is not None and v < start:
            raise ValueError("line_end must be >= line_start")
        return v

    def merge_key(self) -> tuple[str, str | None, str | None, int | None, str]:
        """Deterministic dedup key.

        Detector findings (e.g. Slither) with the same detector_id at the same
        location merge even when titles differ; semantic findings (LLM, no
        detector_id) additionally key on the normalized title. The orchestrator
        combines this with evidence similarity - this key is never the sole
        basis for claiming two findings are identical.
        """
        if self.detector_id:
            return (
                "detector",
                self.detector_id.strip().lower(),
                (self.file_path or "").lower(),
                self.line_start,
                "",  # title intentionally excluded for detector findings
            )
        return (
            "semantic",
            None,
            (self.file_path or "").lower(),
            self.line_start,
            self.title.strip().lower(),
        )


class AuditRequest(BaseModel):
    """Validated audit request. Mainnet only."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    address: str
    chain: Literal["ethereum-mainnet"] = CHAIN_ID

    @field_validator("address")
    @classmethod
    def _validate_address(cls, v: str) -> str:
        return normalize_address(v)


class StageStatus(BaseModel):
    """Execution state of one pipeline stage."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    state: StageState = StageState.PENDING
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_code: str | None = None
    detail: str | None = None


class TaskStatus(BaseModel):
    """Reconstructable task state (source of truth: GitHub Actions run + artifacts)."""

    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(min_length=8, max_length=64)
    address: str | None = None
    state: TaskState = TaskState.QUEUED
    run_id: int | None = None
    stages: list[StageStatus] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    error_code: str | None = None
    # x402 payment binding (Phase 12): paid=True only after a payment passed
    # official SDK verification for this task's dispatch; payment_ref is the
    # canonical fingerprint of the verified payment payload (replay ledger key).
    paid: bool = False
    payment_ref: str | None = None

    def stage(self, name: str) -> StageStatus:
        for s in self.stages:
            if s.name == name:
                return s
        raise KeyError(name)


class LLMUsage(BaseModel):
    """LLM call accounting for one audit. Hard budget enforcement lives in router."""

    total_calls: int = 0
    total_prompt_tokens: int | None = None
    total_completion_tokens: int | None = None
    providers_used: list[str] = Field(default_factory=list)
    models_used: list[str] = Field(default_factory=list)
    failed_calls: int = 0


class ReportSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_findings: int = 0
    by_severity: dict[str, int] = Field(default_factory=dict)
    by_status: dict[str, int] = Field(default_factory=dict)
    tools_executed: list[str] = Field(default_factory=list)
    tools_failed: list[str] = Field(default_factory=list)


class AuditReport(BaseModel):
    """Full audit report persisted as report.json artifact."""

    model_config = ConfigDict(extra="forbid")

    address: str
    chain: Literal["ethereum-mainnet"] = CHAIN_ID
    task_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_verified_source: bool = False
    summary: ReportSummary = Field(default_factory=ReportSummary)
    findings: list[Finding] = Field(default_factory=list)
    tools_used: list[str] = Field(default_factory=list)
    tool_versions: dict[str, str] = Field(default_factory=dict)
    llm_usage: LLMUsage = Field(default_factory=LLMUsage)
    limitations: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    execution_time_seconds: float | None = None
    disclaimer: str = REPORT_DISCLAIMER

    @field_validator("address")
    @classmethod
    def _validate_address(cls, v: str) -> str:
        return normalize_address(v)
