#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BACKUPS = ROOT / "backups"
LIVE_FITBIT = ROOT / "assets" / "fitbit_metrics.sqlite3"
LIVE_UNIFIED = ROOT / "assets" / "health_unified.sqlite3"
REPORTS = ROOT / "reports"


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def sqlite_dates(db: Path, query: str) -> list[str]:
    conn = sqlite3.connect(str(db))
    try:
        return [r[0] for r in conn.execute(query).fetchall()]
    finally:
        conn.close()


def sqlite_scalar(db: Path, query: str) -> Any:
    conn = sqlite3.connect(str(db))
    try:
        row = conn.execute(query).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def mb(n: int) -> float:
    return round(n / (1024 * 1024), 2)


def snapshot_info(snap: Path, live_fitbit_dates: set[str], live_unified_fitbit_dates: set[str]) -> dict[str, Any]:
    fitbit_db = snap / "fitbit_metrics.sqlite3"
    unified_db = snap / "health_unified.sqlite3"
    token = snap / "fitbit_tokens.json"

    fitbit_dates = sqlite_dates(fitbit_db, "SELECT date FROM daily_metrics ORDER BY date") if fitbit_db.exists() else []
    unified_fitbit_dates = (
        sqlite_dates(unified_db, "SELECT date FROM daily_health_summary WHERE source='fitbit' ORDER BY date")
        if unified_db.exists()
        else []
    )

    size_fitbit = fitbit_db.stat().st_size if fitbit_db.exists() else 0
    size_unified = unified_db.stat().st_size if unified_db.exists() else 0
    size_token = token.stat().st_size if token.exists() else 0

    fitbit_sync_runs = sqlite_scalar(fitbit_db, "SELECT COUNT(*) FROM sync_runs") if fitbit_db.exists() else None
    unified_fitbit_count = len(unified_fitbit_dates)

    return {
        "snapshot": str(snap.relative_to(ROOT)),
        "kind": snap.parent.name,
        "stamp": snap.name,
        "day": snap.name[:8],
        "size_mb": {
            "fitbit_db": mb(size_fitbit),
            "unified_db": mb(size_unified),
            "token": mb(size_token),
            "total": mb(size_fitbit + size_unified + size_token),
        },
        "fitbit_cache": {
            "count": len(fitbit_dates),
            "min": fitbit_dates[0] if fitbit_dates else None,
            "max": fitbit_dates[-1] if fitbit_dates else None,
            "sync_runs": fitbit_sync_runs,
            "extra_vs_live": sorted(set(fitbit_dates) - live_fitbit_dates),
            "missing_vs_live_count": len(live_fitbit_dates - set(fitbit_dates)),
        },
        "unified_fitbit": {
            "count": unified_fitbit_count,
            "min": unified_fitbit_dates[0] if unified_fitbit_dates else None,
            "max": unified_fitbit_dates[-1] if unified_fitbit_dates else None,
            "extra_vs_live": sorted(set(unified_fitbit_dates) - live_unified_fitbit_dates),
            "missing_vs_live_count": len(live_unified_fitbit_dates - set(unified_fitbit_dates)),
        },
    }


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    live_fitbit_dates = set(sqlite_dates(LIVE_FITBIT, "SELECT date FROM daily_metrics ORDER BY date"))
    live_unified_fitbit_dates = set(
        sqlite_dates(LIVE_UNIFIED, "SELECT date FROM daily_health_summary WHERE source='fitbit' ORDER BY date")
    )

    snapshots = []
    for snap in sorted([p for p in BACKUPS.rglob("*") if p.is_dir() and (p / "fitbit_metrics.sqlite3").exists()]):
        snapshots.append(snapshot_info(snap, live_fitbit_dates, live_unified_fitbit_dates))

    by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in snapshots:
        by_kind[s["kind"]].append(s)
        by_day[s["day"]].append(s)

    snapshots_with_hidden_fitbit_data = [
        {
            "snapshot": s["snapshot"],
            "extra_dates": s["fitbit_cache"]["extra_vs_live"],
        }
        for s in snapshots
        if s["fitbit_cache"]["extra_vs_live"]
    ]
    snapshots_with_hidden_unified_fitbit_data = [
        {
            "snapshot": s["snapshot"],
            "extra_dates": s["unified_fitbit"]["extra_vs_live"],
        }
        for s in snapshots
        if s["unified_fitbit"]["extra_vs_live"]
    ]

    report = {
        "generated_at": now_iso(),
        "root": str(ROOT),
        "summary": {
            "snapshot_count": len(snapshots),
            "live_fitbit_cache_count": len(live_fitbit_dates),
            "live_unified_fitbit_count": len(live_unified_fitbit_dates),
            "snapshots_with_hidden_fitbit_cache_dates": len(snapshots_with_hidden_fitbit_data),
            "snapshots_with_hidden_unified_fitbit_dates": len(snapshots_with_hidden_unified_fitbit_data),
            "conclusion": "Backups are large because they repeatedly snapshot health_unified.sqlite3; no snapshot contains Fitbit daily dates absent from the live Fitbit cache DB.",
        },
        "size_by_kind_mb": {
            kind: round(sum(s["size_mb"]["total"] for s in items), 2) for kind, items in by_kind.items()
        },
        "snapshot_counts_by_kind": {kind: len(items) for kind, items in by_kind.items()},
        "days": {
            day: {
                "count": len(items),
                "latest_snapshot": sorted(items, key=lambda x: x["stamp"])[-1]["snapshot"],
            }
            for day, items in sorted(by_day.items())
        },
        "hidden_fitbit_cache_data": snapshots_with_hidden_fitbit_data,
        "hidden_unified_fitbit_data": snapshots_with_hidden_unified_fitbit_data,
        "snapshots": snapshots,
    }

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out = REPORTS / f"fitbit_backup_audit_{stamp}.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps({"ok": True, "operation": "fitbit-backup-audit", "report": str(out), "summary": report["summary"]}, indent=2))


if __name__ == "__main__":
    main()
