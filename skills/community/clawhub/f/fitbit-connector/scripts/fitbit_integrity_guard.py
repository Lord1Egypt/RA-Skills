#!/usr/bin/env python3
"""Fitbit integrity guardrail.

Checks that:
- Fitbit cache DB is structurally healthy and duplicate-free
- Unified DB keeps Fitbit and Apple Health rows source-separated
- Fitbit cache dates are fully propagated into unified DB for the audited span
- Backup retention pressure is visible

Outputs compact JSON suitable for cron announcements.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FITBIT_DB = PROJECT_ROOT / "assets" / "fitbit_metrics.sqlite3"
UNIFIED_DB = PROJECT_ROOT / "assets" / "health_unified.sqlite3"
BACKUP_DIR = PROJECT_ROOT / "backups"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _sqlite_ok(path: Path) -> Dict[str, Any]:
    try:
        conn = sqlite3.connect(str(path))
        row = conn.execute("PRAGMA integrity_check").fetchone()
        conn.close()
        ok = bool(row and row[0] == "ok")
        return {"ok": ok, "detail": row[0] if row else "no_result"}
    except Exception as e:
        return {"ok": False, "detail": str(e)}


def _bytes_to_mb(n: int) -> float:
    return round(n / (1024 * 1024), 2)


def _dir_size(path: Path) -> int:
    total = 0
    if not path.exists():
        return total
    for p in path.rglob("*"):
        if p.is_file():
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def _date_rows(conn: sqlite3.Connection, query: str, params: tuple = ()) -> List[str]:
    return [r[0] for r in conn.execute(query, params).fetchall()]


def main(compact: bool = False) -> None:
    fit = sqlite3.connect(str(FITBIT_DB))
    uni = sqlite3.connect(str(UNIFIED_DB))

    fit_dates = _date_rows(fit, "SELECT date FROM daily_metrics ORDER BY date")
    unified_fitbit_dates = _date_rows(
        uni,
        "SELECT date FROM daily_health_summary WHERE source='fitbit' ORDER BY date",
    )
    unified_apple_dates = _date_rows(
        uni,
        "SELECT date FROM daily_health_summary WHERE source='apple_health' ORDER BY date",
    )

    missing_in_unified = sorted(set(fit_dates) - set(unified_fitbit_dates))
    extra_in_unified = sorted(set(unified_fitbit_dates) - set(fit_dates))

    duplicate_cache_groups = fit.execute(
        "SELECT COUNT(*) FROM (SELECT date FROM daily_metrics GROUP BY date HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    duplicate_unified_fitbit_groups = uni.execute(
        "SELECT COUNT(*) FROM (SELECT date FROM daily_health_summary WHERE source='fitbit' GROUP BY date HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    duplicate_unified_apple_groups = uni.execute(
        "SELECT COUNT(*) FROM (SELECT date FROM daily_health_summary WHERE source='apple_health' GROUP BY date HAVING COUNT(*) > 1)"
    ).fetchone()[0]

    source_counts = [
        {"source": r[0], "count": r[1]}
        for r in uni.execute(
            "SELECT source, COUNT(*) FROM daily_health_summary GROUP BY source ORDER BY source"
        ).fetchall()
    ]

    overlap_days = len(set(unified_fitbit_dates) & set(unified_apple_dates))
    degraded_fitbit_days = fit.execute(
        "SELECT COUNT(*) FROM daily_metrics WHERE data_quality='degraded'"
    ).fetchone()[0]
    partial_fitbit_days = fit.execute(
        "SELECT COUNT(*) FROM daily_metrics WHERE data_quality='partial'"
    ).fetchone()[0]

    backup_files = sorted([p for p in BACKUP_DIR.rglob("*") if p.is_file()])
    backup_bytes = _dir_size(BACKUP_DIR)

    issues: List[str] = []
    if not _sqlite_ok(FITBIT_DB)["ok"]:
        issues.append("fitbit_db_integrity_failed")
    if not _sqlite_ok(UNIFIED_DB)["ok"]:
        issues.append("unified_db_integrity_failed")
    if duplicate_cache_groups:
        issues.append("duplicate_fitbit_cache_dates")
    if duplicate_unified_fitbit_groups:
        issues.append("duplicate_unified_fitbit_dates")
    if duplicate_unified_apple_groups:
        issues.append("duplicate_unified_apple_dates")
    if missing_in_unified:
        issues.append("fitbit_cache_unified_parity_gap")
    if backup_bytes >= 5 * 1024 * 1024 * 1024:
        issues.append("fitbit_backup_pressure")
    if degraded_fitbit_days:
        issues.append("fitbit_degraded_days_present")

    status = "ok"
    if any(x in issues for x in [
        "fitbit_db_integrity_failed",
        "unified_db_integrity_failed",
        "duplicate_fitbit_cache_dates",
        "duplicate_unified_fitbit_dates",
        "duplicate_unified_apple_dates",
        "fitbit_cache_unified_parity_gap",
    ]):
        status = "fail"
    elif issues:
        status = "warn"

    out: Dict[str, Any] = {
        "generated_at": utc_now_iso(),
        "status": status,
        "issues": issues,
        "paths": {
            "fitbit_db": str(FITBIT_DB),
            "unified_db": str(UNIFIED_DB),
            "backup_dir": str(BACKUP_DIR),
        },
        "integrity": {
            "fitbit_db": _sqlite_ok(FITBIT_DB),
            "unified_db": _sqlite_ok(UNIFIED_DB),
        },
        "fitbit_cache": {
            "row_count": len(fit_dates),
            "range": {
                "start": fit_dates[0] if fit_dates else None,
                "end": fit_dates[-1] if fit_dates else None,
            },
            "duplicate_date_groups": duplicate_cache_groups,
            "quality": {
                "partial_days": partial_fitbit_days,
                "degraded_days": degraded_fitbit_days,
            },
        },
        "unified": {
            "source_counts": source_counts,
            "fitbit_duplicate_date_groups": duplicate_unified_fitbit_groups,
            "apple_duplicate_date_groups": duplicate_unified_apple_groups,
            "same_date_overlap_between_sources": overlap_days,
        },
        "parity": {
            "fitbit_dates": len(fit_dates),
            "unified_fitbit_dates": len(unified_fitbit_dates),
            "missing_in_unified": missing_in_unified,
            "missing_in_unified_count": len(missing_in_unified),
            "extra_in_unified": extra_in_unified,
            "extra_in_unified_count": len(extra_in_unified),
            "ok": not missing_in_unified and not extra_in_unified,
        },
        "backup_pressure": {
            "file_count": len(backup_files),
            "size_mb": _bytes_to_mb(backup_bytes),
            "warn_threshold_mb": 5120,
            "warn": backup_bytes >= 5 * 1024 * 1024 * 1024,
        },
        "separation_policy": {
            "fitbit_and_apple_remain_distinct_sources": True,
            "fitbit_should_be_used_explicitly_for_training_queries": True,
            "apple_health_should_be_requested_explicitly": True,
            "best_source_blending_exists_only_as_explicit_opt_in": True,
        },
    }

    fit.close()
    uni.close()

    if compact:
        compact_out = {
            "status": out["status"],
            "parity_ok": out["parity"]["ok"],
            "fitbit_cache_row_count": out["fitbit_cache"]["row_count"],
            "unified_fitbit_row_count": next((x["count"] for x in out["unified"]["source_counts"] if x["source"] == "fitbit"), 0),
            "missing_in_unified_count": out["parity"]["missing_in_unified_count"],
            "degraded_day_count": out["fitbit_cache"]["quality"]["degraded_days"],
            "backup_size_mb": out["backup_pressure"]["size_mb"],
            "backup_file_count": out["backup_pressure"]["file_count"],
            "apple_health_separate": out["separation_policy"]["fitbit_and_apple_remain_distinct_sources"],
            "issues": out["issues"],
            "generated_at": out["generated_at"],
        }
        print(json.dumps(compact_out, ensure_ascii=False))
    else:
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Fitbit integrity guard checks")
    parser.add_argument("--compact", action="store_true", help="Emit compact one-line JSON summary")
    args = parser.parse_args()
    main(compact=args.compact)
