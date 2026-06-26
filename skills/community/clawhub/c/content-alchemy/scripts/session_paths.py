#!/usr/bin/env python3
"""Shared helpers for persistent content-alchemy session paths."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any


SESSION_ENV_VAR = "CONTENT_ALCHEMY_SESSION_ROOT"
LEGACY_SESSION_ROOT = Path("/tmp/content-alchemy/sessions").resolve()


def session_root() -> Path:
    configured = os.environ.get(SESSION_ENV_VAR)
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".content-alchemy" / "sessions").expanduser().resolve()


def ensure_session_root() -> Path:
    root = session_root()
    root.mkdir(parents=True, exist_ok=True)
    return root


def safe_stem(path: Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", path.stem)
    stem = stem.strip("-").lower()
    return stem or "pdf-session"


def artifact_paths(pdf_path: Path, root: Path | None = None) -> dict[str, Path]:
    session_dir = (root or session_root()).expanduser().resolve()
    slug = safe_stem(pdf_path)
    return {
        "root": session_dir,
        "state": (session_dir / f"{slug}.json").resolve(),
        "plan": (session_dir / f"{slug}-plan.json").resolve(),
        "segment_results": (session_dir / f"{slug}-segments").resolve(),
        "checkpoint_results": (session_dir / f"{slug}-checkpoints").resolve(),
    }


def _copy_artifact(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
        return
    shutil.copy2(source, destination)


def migrate_legacy_session(pdf_path: Path) -> dict[str, Any]:
    destination_root = ensure_session_root()
    if destination_root == LEGACY_SESSION_ROOT:
        return {
            "legacy_root": str(LEGACY_SESSION_ROOT),
            "session_root": str(destination_root),
            "migrated": False,
            "artifacts": [],
        }

    legacy = artifact_paths(pdf_path, LEGACY_SESSION_ROOT)
    current = artifact_paths(pdf_path, destination_root)
    migrated: list[str] = []

    for artifact_name in ("state", "plan", "segment_results", "checkpoint_results"):
        source = legacy[artifact_name]
        destination = current[artifact_name]
        if not source.exists() or destination.exists():
            continue
        _copy_artifact(source, destination)
        migrated.append(str(destination))

    return {
        "legacy_root": str(LEGACY_SESSION_ROOT),
        "session_root": str(destination_root),
        "migrated": bool(migrated),
        "artifacts": migrated,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_existing_state(pdf_path: Path) -> dict[str, Any] | None:
    migrate_legacy_session(pdf_path)
    state_path = artifact_paths(pdf_path)["state"]
    if not state_path.exists():
        return None

    try:
        state = load_json(state_path)
    except Exception:
        return None

    raw_pdf_path = state.get("pdf_path")
    if raw_pdf_path:
        try:
            if Path(str(raw_pdf_path)).expanduser().resolve() != pdf_path.resolve():
                return None
        except Exception:
            return None
    return state


def existing_session_summary(pdf_path: Path) -> dict[str, Any] | None:
    state = load_existing_state(pdf_path)
    if state is None:
        return None

    paths = artifact_paths(pdf_path)
    completed_segments = sorted(int(value) for value in state.get("completed_segments", []))
    completed_checkpoints = sorted(
        int(value) for value in state.get("completed_checkpoints", [])
    )
    return {
        "state_file": str(paths["state"]),
        "current_segment": state.get("current_segment"),
        "current_page_start": state.get("current_page_start"),
        "current_page_end": state.get("current_page_end"),
        "total_segments": state.get("total_segments"),
        "completed_segments": completed_segments,
        "completed_segment_count": len(completed_segments),
        "completed_checkpoints": completed_checkpoints,
        "completed_checkpoint_count": len(completed_checkpoints),
        "last_checkpoint_segment": state.get("last_checkpoint_segment", 0),
        "updated_at": state.get("updated_at"),
        "strategy_mode": state.get("strategy_mode"),
        "segment_size": state.get("segment_size"),
    }


def list_session_states() -> list[dict[str, Any]]:
    root = ensure_session_root()
    sessions: list[dict[str, Any]] = []
    for path in sorted(root.glob("*.json")):
        if path.name.endswith("-plan.json"):
            continue
        try:
            state = load_json(path)
        except Exception:
            continue
        if state.get("status") != "active":
            continue
        updated_at = state.get("updated_at")
        sessions.append(
            {
                "state_file": str(path.resolve()),
                "pdf_path": state.get("pdf_path"),
                "file_name": state.get("file_name"),
                "title": state.get("title"),
                "strategy_mode": state.get("strategy_mode"),
                "current_segment": state.get("current_segment"),
                "current_page_start": state.get("current_page_start"),
                "current_page_end": state.get("current_page_end"),
                "total_segments": state.get("total_segments"),
                "completed_segments": sorted(
                    int(value) for value in state.get("completed_segments", [])
                ),
                "completed_segment_count": len(state.get("completed_segments", [])),
                "completed_checkpoints": sorted(
                    int(value) for value in state.get("completed_checkpoints", [])
                ),
                "completed_checkpoint_count": len(state.get("completed_checkpoints", [])),
                "updated_at": updated_at,
            }
        )
    sessions.sort(
        key=lambda item: (
            item.get("updated_at") or "",
            item.get("current_segment") or 0,
        ),
        reverse=True,
    )
    return sessions
