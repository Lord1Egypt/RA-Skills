#!/usr/bin/env python3
"""Fail-safe Fitbit pipeline with backup, validation, and optional rollback.

Flow:
1) Acquire lock (single writer)
2) Snapshot Fitbit DB + unified DB + token file
3) Sync Fitbit range into local cache
4) Import synced range into unified DB
5) Validate freshness + row parity + integrity
6) Persist run report
7) Roll back from snapshots on failure (optional, default enabled)
"""

import argparse
import json
import os
import shutil
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from _fitbit_common import get_config
from fitbit_backup_prune import prune_pipeline_snapshots
from fitbit_sync import backfill
from health_db import connect, import_fitbit_cache

HEALTH_DB_PATH = Path(__file__).resolve().parent.parent / "assets" / "health_unified.sqlite3"
BACKUP_ROOT = Path(__file__).resolve().parent.parent / "backups" / "pipeline"
RUNS_ROOT = Path(__file__).resolve().parent.parent / "runs"
LOCK_PATH = Path(__file__).resolve().parent.parent / "assets" / ".fitbit_pipeline.lock"


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@contextmanager
def pipeline_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    f = open(path, "w")
    try:
        import fcntl

        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise RuntimeError(f"pipeline lock already held: {path}")
    try:
        f.write(f"pid={os.getpid()} started={now_iso()}\n")
        f.flush()
        yield
    finally:
        try:
            import fcntl

            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        f.close()


def _sqlite_snapshot(src: Path, dest: Path) -> None:
    src_conn = sqlite3.connect(str(src))
    dest_conn = sqlite3.connect(str(dest))
    try:
        src_conn.backup(dest_conn)
    finally:
        dest_conn.close()
        src_conn.close()


def _verify_sqlite(path: Path) -> tuple[bool, str]:
    try:
        conn = sqlite3.connect(str(path))
        try:
            row = conn.execute("PRAGMA integrity_check").fetchone()
            ok = bool(row) and row[0] == "ok"
            return ok, row[0] if row else "no_result"
        finally:
            conn.close()
    except Exception as e:
        return False, str(e)


def create_snapshots(cfg, backup_dir: Path) -> dict:
    backup_dir.mkdir(parents=True, exist_ok=True)
    snap = {
        "fitbit_db": str(backup_dir / "fitbit_metrics.sqlite3"),
        "health_db": str(backup_dir / "health_unified.sqlite3"),
        "token": str(backup_dir / "fitbit_tokens.json"),
    }

    _sqlite_snapshot(cfg.db_path, Path(snap["fitbit_db"]))
    _sqlite_snapshot(HEALTH_DB_PATH, Path(snap["health_db"]))

    if cfg.token_path.exists():
        shutil.copy2(cfg.token_path, snap["token"])
    else:
        Path(snap["token"]).write_text("{}")

    ver = {
        "fitbit_db": _verify_sqlite(Path(snap["fitbit_db"])),
        "health_db": _verify_sqlite(Path(snap["health_db"])),
        "token_exists": Path(snap["token"]).exists(),
    }
    if not (ver["fitbit_db"][0] and ver["health_db"][0] and ver["token_exists"]):
        raise RuntimeError(f"snapshot verification failed: {ver}")
    snap["verification"] = ver

    return snap


def restore_snapshots(cfg, snapshots: dict) -> None:
    shutil.copy2(snapshots["fitbit_db"], cfg.db_path)
    shutil.copy2(snapshots["health_db"], HEALTH_DB_PATH)
    shutil.copy2(snapshots["token"], cfg.token_path)


def db_scalar(path: Path, query: str, params=()):
    conn = sqlite3.connect(str(path))
    try:
        row = conn.execute(query, params).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def run_checks(start: str, end: str, max_lag_days: int) -> list[CheckResult]:
    checks: list[CheckResult] = []

    cfg = get_config()
    latest_fitbit = db_scalar(cfg.db_path, "SELECT MAX(date) FROM daily_metrics")
    lag = None
    if latest_fitbit:
        lag = (date.today() - date.fromisoformat(latest_fitbit)).days
    ok_fresh = latest_fitbit is not None and lag is not None and lag <= max_lag_days
    checks.append(
        CheckResult(
            name="freshness.fitbit_daily_metrics",
            ok=ok_fresh,
            detail=f"latest={latest_fitbit} lag_days={lag} threshold={max_lag_days}",
        )
    )

    fitbit_rows = db_scalar(
        cfg.db_path,
        "SELECT COUNT(*) FROM daily_metrics WHERE date BETWEEN ? AND ?",
        (start, end),
    )
    unified_rows = db_scalar(
        HEALTH_DB_PATH,
        "SELECT COUNT(*) FROM daily_health_summary WHERE source='fitbit' AND date BETWEEN ? AND ?",
        (start, end),
    )
    ok_parity = (fitbit_rows or 0) == (unified_rows or 0) and (fitbit_rows or 0) > 0
    checks.append(
        CheckResult(
            name="parity.fitbit_cache_to_unified",
            ok=ok_parity,
            detail=f"start={start} end={end} fitbit_rows={fitbit_rows} unified_rows={unified_rows}",
        )
    )

    degraded_recent = db_scalar(
        cfg.db_path,
        "SELECT COUNT(*) FROM daily_metrics WHERE date BETWEEN ? AND ? AND data_quality='degraded'",
        (start, end),
    )
    ok_quality = (degraded_recent or 0) == 0
    checks.append(
        CheckResult(
            name="quality.no_degraded_rows_in_window",
            ok=ok_quality,
            detail=f"degraded_rows={degraded_recent} window={start}..{end}",
        )
    )

    fitbit_integrity = _verify_sqlite(cfg.db_path)
    health_integrity = _verify_sqlite(HEALTH_DB_PATH)
    checks.append(
        CheckResult(
            name="integrity.fitbit_db",
            ok=fitbit_integrity[0],
            detail=f"result={fitbit_integrity[1]}",
        )
    )
    checks.append(
        CheckResult(
            name="integrity.health_db",
            ok=health_integrity[0],
            detail=f"result={health_integrity[1]}",
        )
    )

    return checks


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--start", help="Start date YYYY-MM-DD")
    p.add_argument("--end", help="End date YYYY-MM-DD")
    p.add_argument("--days-backfill", type=int, default=3, help="Used when --start/--end omitted")
    p.add_argument("--max-lag-days", type=int, default=1)
    p.add_argument("--rollback-on-fail", action="store_true", default=True)
    p.add_argument("--no-rollback-on-fail", dest="rollback_on_fail", action="store_false")
    p.add_argument("--prune-backups", action="store_true", default=True, help="Prune old pipeline snapshots after a successful run")
    p.add_argument("--no-prune-backups", dest="prune_backups", action="store_false")
    p.add_argument("--keep-recent-backup-days", type=int, default=1, help="Keep all pipeline snapshots from the most recent N distinct days; older days keep only the latest snapshot")
    p.add_argument("--dry-run", action="store_true", help="No API sync or DB writes; run preflight and checks only")
    return p.parse_args()


def _preflight(cfg) -> list[CheckResult]:
    out: list[CheckResult] = []
    out.append(CheckResult("preflight.fitbit_db_exists", cfg.db_path.exists(), f"path={cfg.db_path}"))
    out.append(CheckResult("preflight.health_db_exists", HEALTH_DB_PATH.exists(), f"path={HEALTH_DB_PATH}"))
    out.append(CheckResult("preflight.token_exists", cfg.token_path.exists(), f"path={cfg.token_path}"))
    return out


def main() -> int:
    args = parse_args()
    cfg = get_config()

    if args.start and args.end:
        start, end = args.start, args.end
    else:
        end_d = date.today()
        start_d = end_d - timedelta(days=max(args.days_backfill - 1, 0))
        start, end = start_d.isoformat(), end_d.isoformat()

    run_id = stamp()
    backup_dir = BACKUP_ROOT / run_id
    run_report_path = RUNS_ROOT / f"fitbit_pipeline_{run_id}.json"
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)

    report = {
        "ok": False,
        "run_id": run_id,
        "started_at": now_iso(),
        "window": {"start": start, "end": end},
        "backup_dir": str(backup_dir),
        "steps": [],
        "checks": [],
        "rollback_performed": False,
        "dry_run": args.dry_run,
    }

    try:
        with pipeline_lock(LOCK_PATH):
            preflight = _preflight(cfg)
            report["checks"].extend(asdict(c) for c in preflight)
            if not all(c.ok for c in preflight):
                raise RuntimeError("preflight failed")

            if args.dry_run:
                checks = run_checks(start, end, args.max_lag_days)
                report["checks"].extend(asdict(c) for c in checks)
                report["steps"].append({"name": "dry_run", "ok": True, "detail": "no writes performed"})
                report["ok"] = all(c.ok for c in checks)
                report["finished_at"] = now_iso()
                run_report_path.write_text(json.dumps(report, indent=2))
                print(json.dumps(report, indent=2))
                return 0 if report.get("ok") else 2

            snapshots = create_snapshots(cfg, backup_dir)
            report["steps"].append({"name": "backup", "ok": True, "snapshots": snapshots})

            sync_results = backfill(start, end, emit_text=False)
            report["steps"].append({"name": "fitbit_sync", "ok": True, "days": len(sync_results), "results": sync_results})

            conn = connect(HEALTH_DB_PATH)
            try:
                import_result = import_fitbit_cache(conn, cfg.db_path, start, end)
            finally:
                conn.close()
            report["steps"].append({"name": "unified_import", "ok": True, "result": import_result})

            checks = run_checks(start, end, args.max_lag_days)
            report["checks"].extend(asdict(c) for c in checks)

            if not all(c["ok"] for c in report["checks"]):
                raise RuntimeError("validation failed")

            if args.prune_backups:
                try:
                    prune = prune_pipeline_snapshots(keep_recent_days=args.keep_recent_backup_days, apply=True)
                    report["steps"].append({"name": "backup_prune", "ok": True, "result": prune})
                except Exception as prune_err:
                    report["steps"].append({"name": "backup_prune", "ok": False, "error": str(prune_err)})

            report["ok"] = True
            report["finished_at"] = now_iso()

    except Exception as e:
        report["error"] = str(e)
        report["finished_at"] = now_iso()

        if args.rollback_on_fail and backup_dir.exists():
            try:
                restore_snapshots(cfg, {
                    "fitbit_db": str(backup_dir / "fitbit_metrics.sqlite3"),
                    "health_db": str(backup_dir / "health_unified.sqlite3"),
                    "token": str(backup_dir / "fitbit_tokens.json"),
                })
                report["rollback_performed"] = True
            except Exception as rollback_err:
                report["rollback_error"] = str(rollback_err)

    run_report_path.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
