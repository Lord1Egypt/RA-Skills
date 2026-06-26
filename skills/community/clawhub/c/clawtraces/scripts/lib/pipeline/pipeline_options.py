# FILE_META
# INPUT:  config dict (from config_loader) + runtime overrides
# OUTPUT: PipelineOptions / SessionCandidate / ProcessResult dataclasses
# POS:    skill lib — shared value types between pipeline.py and CLI entry points
# MISSION: Define the collection pipeline's I/O contract as value types.

"""Shared dataclasses for the unified collection pipeline.

``PipelineOptions`` carries everything the pipeline needs to decide what
to discover, what to filter, and what to process. ``SessionCandidate`` is
the unit of work produced by ``filter_sessions``. ``ProcessResult`` is
the outcome of ``process_session``, consumed in-memory by the CLI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EligibilityRules:
    model_whitelist: list[str]
    min_turns: int
    min_tool_use_count: int
    min_reasoning_turns: int
    allow_non_cache_trace: bool
    include_cron_tasks: bool

    @classmethod
    def from_config(cls, cfg: dict) -> "EligibilityRules":
        e = cfg["eligibility"]
        return cls(
            model_whitelist=list(e["model_whitelist"]),
            min_turns=e["min_turns"],
            min_tool_use_count=e["min_tool_use_count"],
            min_reasoning_turns=e["min_reasoning_turns"],
            allow_non_cache_trace=e["allow_non_cache_trace"],
            include_cron_tasks=e["include_cron_tasks"],
        )


@dataclass
class PipelineOptions:
    sessions_dirs: list[str]
    output_dir: str
    eligibility: EligibilityRules
    list_size: int
    include_ineligible: bool = False
    explicit_session_ids: list[str] | None = None
    force_active: bool = False
    force_rejected: bool = False
    since_ts: float | None = None

    @classmethod
    def from_config(
        cls,
        config: dict,
        sessions_dirs: list[str],
        output_dir: str,
        *,
        list_size: int | None = None,
        include_ineligible: bool = False,
        explicit_session_ids: list[str] | None = None,
        force_active: bool = False,
        force_rejected: bool = False,
        since_ts: float | None = None,
    ) -> "PipelineOptions":
        max_size = config["max_list_size"]
        default_size = config["default_list_size"]
        effective_size = list_size if list_size is not None else default_size
        if effective_size < 1:
            raise ValueError(f"list_size must be >= 1, got {effective_size}")
        if effective_size > max_size:
            effective_size = max_size
        return cls(
            sessions_dirs=list(sessions_dirs),
            output_dir=output_dir,
            eligibility=EligibilityRules.from_config(config),
            list_size=effective_size,
            include_ineligible=include_ineligible,
            explicit_session_ids=(
                list(explicit_session_ids) if explicit_session_ids else None
            ),
            force_active=force_active,
            force_rejected=force_rejected,
            since_ts=since_ts,
        )


@dataclass
class SessionCandidate:
    """One row produced by filter_sessions — basis for list display and selection."""
    session_id: str
    agent_id: str
    file_path: str
    model: str = ""
    turns: int = 0
    has_compaction: bool = False
    started_at: str = ""
    ended_at: str = ""
    summary: str = ""
    eligible: bool = False
    reject_reason: str | None = None
    reject_detail: dict[str, Any] | None = None
    runtime_status: str | None = None  # "active" | "rejected" | "submitted" | None


@dataclass
class ProcessResult:
    """Outcome of converting one session to a trajectory file."""
    session_id: str
    ok: bool
    trajectory_path: str | None = None
    stats_path: str | None = None
    reject_reason: str | None = None
    reject_detail: dict[str, Any] | None = None
    candidate_meta: dict[str, Any] | None = None
