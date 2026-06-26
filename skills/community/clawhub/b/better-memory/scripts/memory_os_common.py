from __future__ import annotations

import json
import re
from pathlib import Path

MANAGED_AGENT_BLOCK_START = "<!-- OPENCLAW_MEMORY_OS_START -->"
MANAGED_AGENT_BLOCK_END = "<!-- OPENCLAW_MEMORY_OS_END -->"
MANAGED_MEMORY_BLOCK_START = "<!-- OPENCLAW_MEMORY_OS_L3_START -->"
MANAGED_MEMORY_BLOCK_END = "<!-- OPENCLAW_MEMORY_OS_L3_END -->"
MANAGED_HEARTBEAT_BLOCK_START = "<!-- OPENCLAW_MEMORY_OS_HEARTBEAT_START -->"
MANAGED_HEARTBEAT_BLOCK_END = "<!-- OPENCLAW_MEMORY_OS_HEARTBEAT_END -->"

DEFAULT_SETTINGS = {
    "stale_days": 45,
    "max_l3_per_kind": 12,
    "min_evidence_for_l3": 1,
    "migration_days": 14,
    "daily_entries_soft_limit": 40,
    "daily_review_time": "22:00",
    "weekly_rollup_day": "SUN",
    "weekly_rollup_time": "20:00",
    "monthly_review_day": 1,
    "monthly_review_time": "10:00",
    "l1_entry_threshold": 8,
}

DEFAULT_STATE = {
    "last_daily_review_at": None,
    "last_weekly_rollup_at": None,
    "last_monthly_review_at": None,
    "last_processed_l1_entry_id": None,
}


def sidecar_dir(workspace: Path) -> Path:
    return workspace / ".openclaw-memory-os"


def config_path(workspace: Path) -> Path:
    return sidecar_dir(workspace) / "config.json"


def state_path(workspace: Path) -> Path:
    return sidecar_dir(workspace) / "state.json"


def load_settings(workspace: Path) -> dict:
    settings = dict(DEFAULT_SETTINGS)
    path = config_path(workspace)
    if not path.exists():
        return settings
    loaded = json.loads(path.read_text(encoding="utf-8"))
    settings.update({key: value for key, value in loaded.items() if key in DEFAULT_SETTINGS})
    return settings


def save_settings(workspace: Path, overrides: dict) -> Path:
    path = config_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    settings = dict(DEFAULT_SETTINGS)
    settings.update({key: value for key, value in overrides.items() if key in DEFAULT_SETTINGS})
    path.write_text(json.dumps(settings, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return path


def load_state(workspace: Path) -> dict:
    state = dict(DEFAULT_STATE)
    path = state_path(workspace)
    if not path.exists():
        return state
    loaded = json.loads(path.read_text(encoding="utf-8"))
    state.update({key: value for key, value in loaded.items() if key in DEFAULT_STATE})
    return state


def save_state(workspace: Path, overrides: dict) -> Path:
    path = state_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = dict(DEFAULT_STATE)
    current = load_state(workspace)
    state.update(current)
    state.update({key: value for key, value in overrides.items() if key in DEFAULT_STATE})
    path.write_text(json.dumps(state, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return path


def upsert_marked_block(original: str, start: str, end: str, block: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = block.strip()
    if pattern.search(original):
        return pattern.sub(replacement, original) + ("\n" if not original.endswith("\n") else "")
    if original.strip():
        return original.rstrip() + "\n\n" + replacement + "\n"
    return replacement + "\n"


def remove_marked_block(original: str, start: str, end: str) -> str:
    pattern = re.compile(r"\n?" + re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.DOTALL)
    updated = pattern.sub("\n", original)
    collapsed = re.sub(r"\n{3,}", "\n\n", updated).strip()
    return (collapsed + "\n") if collapsed else ""
