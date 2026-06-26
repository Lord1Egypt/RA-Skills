#!/usr/bin/env python3
import json
import sqlite3
from datetime import UTC, date, datetime
from pathlib import Path

from _fitbit_common import get_config

HEALTH_DB_PATH = Path(__file__).resolve().parent.parent / "assets" / "health_unified.sqlite3"


def _sqlite_ok(path: Path):
    try:
        conn = sqlite3.connect(str(path))
        row = conn.execute("PRAGMA integrity_check").fetchone()
        conn.close()
        return row and row[0] == "ok", row[0] if row else "no_result"
    except Exception as e:
        return False, str(e)


def _date_gap_stats(conn: sqlite3.Connection, table: str, source_clause: str = ""):
    q = f"SELECT date FROM {table} {source_clause} ORDER BY date"
    rows = [r[0] for r in conn.execute(q).fetchall()]
    if not rows:
        return {"count": 0, "min": None, "max": None, "missing_days": 0}
    d0 = date.fromisoformat(rows[0])
    d1 = date.fromisoformat(rows[-1])
    expected = (d1 - d0).days + 1
    missing = expected - len(set(rows))
    return {"count": len(rows), "min": rows[0], "max": rows[-1], "missing_days": max(missing, 0)}


def main():
    cfg = get_config()
    out = {
        "generated_at": datetime.now(UTC).isoformat(),
        "paths": {
            "fitbit_db": str(cfg.db_path),
            "health_db": str(HEALTH_DB_PATH),
            "token": str(cfg.token_path),
        },
    }

    out["integrity"] = {
        "fitbit_db": _sqlite_ok(cfg.db_path),
        "health_db": _sqlite_ok(HEALTH_DB_PATH),
        "token_exists": cfg.token_path.exists(),
    }

    fit = sqlite3.connect(str(cfg.db_path))
    uni = sqlite3.connect(str(HEALTH_DB_PATH))

    out["fitbit_daily"] = _date_gap_stats(fit, "daily_metrics")
    out["fitbit_quality"] = [
        {"data_quality": r[0], "count": r[1]}
        for r in fit.execute("SELECT data_quality, COUNT(*) FROM daily_metrics GROUP BY data_quality ORDER BY data_quality").fetchall()
    ]
    out["fitbit_sync_runs"] = fit.execute("SELECT COUNT(*) FROM sync_runs").fetchone()[0]
    out["fitbit_quality_flags"] = fit.execute("SELECT COUNT(*) FROM quality_flags").fetchone()[0]

    out["unified_fitbit_daily"] = _date_gap_stats(uni, "daily_health_summary", "WHERE source='fitbit'")
    out["unified_apple_daily"] = _date_gap_stats(uni, "daily_health_summary", "WHERE source='apple_health'")
    out["apple_raw_records"] = uni.execute("SELECT COUNT(*) FROM apple_health_records").fetchone()[0]
    has_import_manifest = bool(
        uni.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='apple_import_files'").fetchone()
    )
    out["apple_import_files"] = (
        uni.execute("SELECT COUNT(*) FROM apple_import_files").fetchone()[0] if has_import_manifest else None
    )
    out["ingest_runs"] = uni.execute("SELECT COUNT(*) FROM ingest_runs").fetchone()[0]

    # Check fitbit parity over overlap range.
    minmax = uni.execute("SELECT MIN(date), MAX(date) FROM daily_health_summary WHERE source='fitbit'").fetchone()
    if minmax and minmax[0] and minmax[1]:
        a, b = minmax[0], minmax[1]
        fit_rows = fit.execute("SELECT COUNT(*) FROM daily_metrics WHERE date BETWEEN ? AND ?", (a, b)).fetchone()[0]
        uni_rows = uni.execute("SELECT COUNT(*) FROM daily_health_summary WHERE source='fitbit' AND date BETWEEN ? AND ?", (a, b)).fetchone()[0]
        out["fitbit_parity"] = {"start": a, "end": b, "fitbit_rows": fit_rows, "unified_rows": uni_rows, "ok": fit_rows == uni_rows}
    else:
        out["fitbit_parity"] = {"ok": False, "reason": "no_fitbit_rows_in_unified"}

    fit.close()
    uni.close()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
