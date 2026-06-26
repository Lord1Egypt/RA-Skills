"""Local database migration helpers for owner_did-aware multi-identity storage.

[INPUT]: local_store (SQLite schema management), SDKConfig (data_dir),
         service_manager (listener stop/start coordination for explicit upgrade flows)
[OUTPUT]: detect_local_database_layout(), migrate_local_database(),
          ensure_local_database_ready(), ensure_local_database_ready_for_upgrade()
[POS]: Shared migration module used by check_status.py and the standalone
       migrate_local_database.py CLI, with idempotent self-healing for
       already-ready databases

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import local_store
from service_manager import get_service_manager
from utils.config import SDKConfig

logger = logging.getLogger(__name__)


def _database_path(config: SDKConfig | None = None) -> Path:
    """Return the local SQLite database path."""
    resolved_config = config or SDKConfig()
    return resolved_config.data_dir / "database" / "awiki.db"


def _backup_root(config: SDKConfig | None = None) -> Path:
    """Return the database migration backup directory."""
    resolved_config = config or SDKConfig()
    backup_dir = resolved_config.data_dir / "database" / ".migration-backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir


def detect_local_database_layout(config: SDKConfig | None = None) -> dict[str, Any]:
    """Detect whether the local database requires migration."""
    db_path = _database_path(config)
    if not db_path.exists():
        return {
            "status": "not_found",
            "db_path": str(db_path),
            "before_version": None,
        }

    conn = local_store.get_connection()
    try:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
    finally:
        conn.close()

    return {
        "status": "legacy" if version < local_store._SCHEMA_VERSION else "ready",
        "db_path": str(db_path),
        "before_version": version,
    }


def _backup_database(config: SDKConfig | None = None) -> Path:
    """Create a SQLite backup before migration."""
    db_path = _database_path(config)
    backup_path = _backup_root(config) / (
        f"awiki-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.db"
    )
    source = sqlite3.connect(str(db_path))
    try:
        destination = sqlite3.connect(str(backup_path))
        try:
            source.backup(destination)
        finally:
            destination.close()
    finally:
        source.close()
    logger.info("Created local database backup path=%s", backup_path)
    return backup_path


def _ensure_database_schema(
    *,
    db_path: str,
    status: str,
    backup_path: str | None,
) -> dict[str, Any]:
    """Run idempotent schema repair and return the migration summary."""
    conn = local_store.get_connection()
    try:
        before_version = conn.execute("PRAGMA user_version").fetchone()[0]
        local_store.ensure_schema(conn)
        after_version = conn.execute("PRAGMA user_version").fetchone()[0]
    finally:
        conn.close()

    return {
        "status": status,
        "db_path": db_path,
        "before_version": before_version,
        "after_version": after_version,
        "backup_path": backup_path,
    }


def migrate_local_database(config: SDKConfig | None = None) -> dict[str, Any]:
    """Migrate the local SQLite database to the latest schema."""
    detection = detect_local_database_layout(config)
    if detection["status"] == "not_found":
        return {
            "status": "not_needed",
            "db_path": detection["db_path"],
            "before_version": None,
            "after_version": None,
            "backup_path": None,
        }
    if detection["status"] == "ready":
        return _ensure_database_schema(
            db_path=detection["db_path"],
            status="ready",
            backup_path=None,
        )

    backup_path = _backup_database(config)
    return _ensure_database_schema(
        db_path=detection["db_path"],
        status="migrated",
        backup_path=str(backup_path),
    )


def ensure_local_database_ready(config: SDKConfig | None = None) -> dict[str, Any]:
    """Ensure the local database is ready for multi-identity use."""
    detection = detect_local_database_layout(config)
    if detection["status"] == "not_found":
        return detection
    return migrate_local_database(config)


def _build_listener_upgrade_report() -> dict[str, Any]:
    """Return the default listener-coordination report payload."""
    return {
        "checked": True,
        "was_running": False,
        "stop_attempted": False,
        "stopped": False,
        "restart_attempted": False,
        "restarted": False,
    }


def _with_listener_restart(
    operation,
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Run one explicit database-upgrade operation with listener stop/restart."""
    listener_report = _build_listener_upgrade_report()
    service_manager = get_service_manager()
    try:
        before_status = service_manager.status()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to inspect listener status before database upgrade")
        return {
            "status": "error",
            "db_path": str(_database_path(config)),
            "before_version": None,
            "after_version": None,
            "backup_path": None,
            "error": f"listener_status_check_failed: {exc}",
            "listener_service": {
                **listener_report,
                "status_error": str(exc),
            },
        }

    listener_report["status_before"] = before_status
    listener_report["was_running"] = bool(before_status.get("running", False))

    if listener_report["was_running"]:
        listener_report["stop_attempted"] = True
        try:
            service_manager.stop()
            after_stop_status = service_manager.status()
        except Exception as exc:  # noqa: BLE001
            logger.exception("Failed to stop listener before database upgrade")
            return {
                "status": "error",
                "db_path": str(_database_path(config)),
                "before_version": None,
                "after_version": None,
                "backup_path": None,
                "error": f"listener_stop_failed: {exc}",
                "listener_service": {
                    **listener_report,
                    "error": "listener_stop_failed",
                    "stop_error": str(exc),
                },
            }

        listener_report["status_after_stop"] = after_stop_status
        listener_report["stopped"] = not bool(after_stop_status.get("running", False))
        if not listener_report["stopped"]:
            return {
                "status": "error",
                "db_path": str(_database_path(config)),
                "before_version": None,
                "after_version": None,
                "backup_path": None,
                "error": "listener_stop_failed: listener still running after stop",
                "listener_service": {
                    **listener_report,
                    "error": "listener_stop_failed",
                },
            }

    try:
        result = operation(config)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Local database upgrade operation failed")
        result = {
            "status": "error",
            "db_path": str(_database_path(config)),
            "before_version": None,
            "after_version": None,
            "backup_path": None,
            "error": f"database_upgrade_failed: {exc}",
        }

    if listener_report["was_running"]:
        listener_report["restart_attempted"] = True
        try:
            service_manager.start()
            after_restart_status = service_manager.status()
            listener_report["status_after_restart"] = after_restart_status
            listener_report["restarted"] = bool(after_restart_status.get("running", False))
        except Exception as exc:  # noqa: BLE001
            logger.exception("Failed to restart listener after database upgrade")
            listener_report["restart_error"] = str(exc)
            listener_report["restarted"] = False

        if not listener_report["restarted"]:
            listener_report["error"] = "listener_restart_failed"
            result = {
                **result,
                "status": "error",
                "error": "listener_restart_failed",
            }

    result["listener_service"] = listener_report
    return result


def ensure_local_database_ready_for_upgrade(
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Ensure database readiness for explicit upgrade flows with listener restart.

    This wrapper is intended for install / manual-upgrade commands. It stops the
    WebSocket listener first when the service is currently running, performs the
    database readiness check/migration, then restores the original running state.
    """
    detection = detect_local_database_layout(config)
    if detection["status"] == "not_found":
        result = ensure_local_database_ready(config)
        result["listener_service"] = _build_listener_upgrade_report()
        return result
    return _with_listener_restart(ensure_local_database_ready, config=config)


__all__ = [
    "detect_local_database_layout",
    "ensure_local_database_ready",
    "ensure_local_database_ready_for_upgrade",
    "migrate_local_database",
]
