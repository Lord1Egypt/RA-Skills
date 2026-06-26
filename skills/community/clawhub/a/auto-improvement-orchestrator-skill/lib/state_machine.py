#!/usr/bin/env python3
"""State-machine helpers for the auto-improvement pipeline.

Extracted from the original lane_common.py — contains directory-tree
management, state transitions, and run/receipt bookkeeping.

Depends on lib.common for read_json / write_json / utc_now_iso / etc.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import os

from lib.common import (
    compact_timestamp,
    read_json,
    slugify,
    utc_now_iso,
    write_json,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_STATE_ROOT = Path(os.environ.get("OPENCLAW_ROOT", os.path.expanduser("~/.openclaw"))) / "shared-context/intel/auto-improvement/generic-skill"

# ---------------------------------------------------------------------------
# Tree / init
# ---------------------------------------------------------------------------


def ensure_tree(state_root: Path) -> dict[str, Path]:
    state_root = state_root.expanduser().resolve()
    mapping = {
        "root": state_root,
        "candidate_versions": state_root / "candidate_versions",
        "rankings": state_root / "rankings",
        "executions": state_root / "executions",
        "state": state_root / "state",
        "receipts": state_root / "receipts",
    }
    for path in mapping.values():
        path.mkdir(parents=True, exist_ok=True)
    init_state_files(mapping)
    return mapping


def init_state_files(paths: dict[str, Path]) -> None:
    defaults = {
        paths["state"] / "current_state.json": {
            "lane": "generic-skill",
            "status": "idle",
            "stage": "idle",
            "current_run_id": None,
            "target_path": None,
            "next_step": "propose_candidates",
            "next_owner": "proposer",
            "truth_anchor": str(paths["state"] / "current_state.json"),
            "updated_at": None,
        },
        paths["state"] / "pending_promote.json": {
            "pending": [],
            "last_updated": None,
        },
        paths["state"] / "veto.json": {
            "vetoes": [],
            "last_updated": None,
        },
        paths["state"] / "last_run.json": {
            "lane": "generic-skill",
            "last_run_id": None,
            "last_stage": "idle",
            "last_status": "idle",
            "last_updated": None,
            "truth_anchor": str(paths["state"] / "last_run.json"),
        },
    }
    for path, payload in defaults.items():
        if not path.exists():
            write_json(path, payload)


# ---------------------------------------------------------------------------
# State transitions
# ---------------------------------------------------------------------------


def next_step_for_stage(stage: str) -> tuple[str, str]:
    mapping = {
        "proposed": ("rank_candidates", "critic"),
        "ranked": ("evaluate_candidate", "evaluator"),
        "evaluated": ("execute_candidate", "executor"),
        "executed": ("apply_gate", "gate"),
        "gated_keep": ("propose_candidates", "proposer"),
        "gated_pending": ("human_promote_review", "human"),
        "gated_revert": ("inspect_failure_and_re-propose", "proposer"),
        "gated_reject": ("re-propose_or_manual_override", "proposer"),
    }
    return mapping.get(stage, ("inspect_state", "human"))


def update_state(
    state_root: Path,
    *,
    run_id: str,
    stage: str,
    status: str,
    target_path: str,
    truth_anchor: str,
    extra: dict[str, Any] | None = None,
) -> None:
    paths = ensure_tree(state_root)
    current_state_path = paths["state"] / "current_state.json"
    last_run_path = paths["state"] / "last_run.json"
    next_step, next_owner = next_step_for_stage(stage)
    payload = {
        "lane": "generic-skill",
        "current_run_id": run_id,
        "stage": stage,
        "status": status,
        "target_path": target_path,
        "next_step": next_step,
        "next_owner": next_owner,
        "truth_anchor": truth_anchor,
        "updated_at": utc_now_iso(),
    }
    if extra:
        payload.update(extra)
    write_json(current_state_path, payload)
    last_run = {
        "lane": "generic-skill",
        "last_run_id": run_id,
        "last_stage": stage,
        "last_status": status,
        "last_updated": payload["updated_at"],
        "truth_anchor": truth_anchor,
        "target_path": target_path,
    }
    if extra:
        for key in ("decision", "candidate_id", "target_path", "receipt_path"):
            if key in extra:
                last_run[key] = extra[key]
    write_json(last_run_path, last_run)


# ---------------------------------------------------------------------------
# Pending / veto
# ---------------------------------------------------------------------------


def append_pending_promote(state_root: Path, entry: dict[str, Any]) -> Path:
    paths = ensure_tree(state_root)
    pending_path = paths["state"] / "pending_promote.json"
    payload = read_json(pending_path)
    payload.setdefault("pending", []).append(entry)
    payload["last_updated"] = utc_now_iso()
    write_json(pending_path, payload)
    return pending_path


def append_veto(state_root: Path, entry: dict[str, Any]) -> Path:
    paths = ensure_tree(state_root)
    veto_path = paths["state"] / "veto.json"
    payload = read_json(veto_path)
    payload.setdefault("vetoes", []).append(entry)
    payload["last_updated"] = utc_now_iso()
    write_json(veto_path, payload)
    return veto_path


# ---------------------------------------------------------------------------
# Run / receipt helpers
# ---------------------------------------------------------------------------


def make_receipt_path(state_root: Path, prefix: str, run_id: str, candidate_id: str | None = None) -> Path:
    paths = ensure_tree(state_root)
    suffix = f"-{candidate_id}" if candidate_id else ""
    return paths["receipts"] / f"{prefix}-{run_id}{suffix}.json"


def make_run_id(target: Path) -> str:
    return f"generic-skill-{slugify(target.name)}-{compact_timestamp()}"


# ---------------------------------------------------------------------------
# Backup / restore
# ---------------------------------------------------------------------------


def backup_file(target: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, destination)
    return destination


def restore_backup(backup_path: Path, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_path, target_path)
