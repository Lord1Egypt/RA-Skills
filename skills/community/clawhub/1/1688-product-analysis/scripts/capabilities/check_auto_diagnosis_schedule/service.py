#!/usr/bin/env python3
"""Deterministically check the local Newton schedule database."""

from __future__ import annotations

import sqlite3
from pathlib import Path


NAME_MARKERS = ("1688商品自动体检", "1688商品体检")
DESCRIPTION_MARKERS = ("自动找出需要优化的商品", "找出待优化商品", "商品诊断报告")


def _find_workspace_db(start: Path | None = None) -> Path | None:
    current = (start or Path(__file__)).resolve()
    for parent in (current, *current.parents):
        candidate = parent / "newton.db"
        if candidate.is_file():
            return candidate
    return None


def _matches(name: str, description: str) -> bool:
    if any(marker in name for marker in NAME_MARKERS):
        return True
    return "1688商品体检" in description and any(
        marker in description for marker in DESCRIPTION_MARKERS
    )


def check_auto_diagnosis_schedule(db_path: Path | str | None = None) -> dict:
    resolved_db = Path(db_path).resolve() if db_path else _find_workspace_db()
    if not resolved_db or not resolved_db.is_file():
        return {
            "showScheduleOption": False,
            "status": "query_failed",
            "reason": "workspace_db_not_found",
        }

    try:
        uri = f"{resolved_db.as_uri()}?mode=ro"
        with sqlite3.connect(uri, uri=True, timeout=3) as connection:
            rows = connection.execute(
                "SELECT name, enabled, description FROM schedule"
            ).fetchall()
    except (OSError, sqlite3.Error):
        return {
            "showScheduleOption": False,
            "status": "query_failed",
            "reason": "schedule_query_failed",
        }

    for raw_name, raw_enabled, raw_description in rows:
        name = str(raw_name or "")
        description = str(raw_description or "")
        enabled = bool(raw_enabled)
        if enabled and _matches(name, description):
            return {
                "showScheduleOption": False,
                "status": "configured",
                "matchedName": name,
                "enabled": True,
            }

    return {
        "showScheduleOption": True,
        "status": "not_configured",
    }
