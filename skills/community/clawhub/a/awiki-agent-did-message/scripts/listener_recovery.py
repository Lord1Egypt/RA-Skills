"""Listener runtime health and auto-recovery helpers.

[INPUT]: SDKConfig, service_manager status/start operations, local daemon
         reachability probe, persisted runtime JSON state, credential name
[OUTPUT]: Shared listener health reports plus persisted restart backoff helpers
          for heartbeat/read/send fallback flows
[POS]: Operational helper layer shared by check_status.py, check_inbox.py, and
       message_transport.py to keep WebSocket receive mode available without
       blocking HTTP fallback

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from message_daemon import is_local_daemon_available
from utils.config import SDKConfig

logger = logging.getLogger(__name__)

_MAX_AUTO_RESTART_FAILURES = 3
_STATE_FILE_NAME = "listener_recovery.json"


def _state_path(config: SDKConfig | None = None) -> Path:
    """Return the persisted listener recovery state file path."""
    resolved = config or SDKConfig.load()
    return resolved.data_dir / "runtime" / _STATE_FILE_NAME


def _default_state() -> dict[str, Any]:
    """Return the default on-disk state structure."""
    return {"credentials": {}}


def _normalize_entry(entry: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize one credential entry loaded from disk."""
    data = entry or {}
    consecutive_failures = data.get("consecutive_restart_failures", 0)
    if not isinstance(consecutive_failures, int) or consecutive_failures < 0:
        consecutive_failures = 0
    last_result = data.get("last_restart_result", "not_needed")
    if not isinstance(last_result, str) or not last_result:
        last_result = "not_needed"
    last_attempt_at = data.get("last_restart_attempt_at")
    if not isinstance(last_attempt_at, str) or not last_attempt_at:
        last_attempt_at = None
    last_error = data.get("last_error")
    if not isinstance(last_error, str) or not last_error:
        last_error = None
    auto_restart_paused = bool(
        data.get("auto_restart_paused", False)
        or consecutive_failures >= _MAX_AUTO_RESTART_FAILURES
    )
    return {
        "consecutive_restart_failures": consecutive_failures,
        "last_restart_attempt_at": last_attempt_at,
        "last_restart_result": last_result,
        "last_error": last_error,
        "auto_restart_paused": auto_restart_paused,
    }


def _load_state(config: SDKConfig | None = None) -> dict[str, Any]:
    """Load the full persisted runtime state from disk."""
    path = _state_path(config)
    if not path.exists():
        return _default_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.debug("Failed to load listener recovery state", exc_info=True)
        return _default_state()
    if not isinstance(data, dict):
        return _default_state()
    credentials = data.get("credentials")
    if not isinstance(credentials, dict):
        return _default_state()
    return {"credentials": credentials}


def _save_state(data: dict[str, Any], config: SDKConfig | None = None) -> None:
    """Persist the runtime state to disk."""
    path = _state_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _update_entry(
    credential_name: str,
    entry: dict[str, Any],
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Persist one credential entry and return its normalized representation."""
    data = _load_state(config)
    data.setdefault("credentials", {})[credential_name] = entry
    _save_state(data, config)
    return _normalize_entry(entry)


def get_listener_recovery_state(
    credential_name: str,
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Return the persisted recovery state for one credential."""
    data = _load_state(config)
    entry = data.get("credentials", {}).get(credential_name)
    return _normalize_entry(entry if isinstance(entry, dict) else None)


def note_listener_healthy(
    credential_name: str,
    *,
    config: SDKConfig | None = None,
    result: str = "not_needed",
) -> dict[str, Any]:
    """Clear backoff counters after a healthy listener check."""
    current = get_listener_recovery_state(credential_name, config=config)
    if (
        current["consecutive_restart_failures"] == 0
        and not current["auto_restart_paused"]
        and current["last_restart_result"] == result
        and current["last_error"] is None
    ):
        return current
    entry = {
        "consecutive_restart_failures": 0,
        "last_restart_attempt_at": current["last_restart_attempt_at"],
        "last_restart_result": result,
        "last_error": None,
        "auto_restart_paused": False,
    }
    return _update_entry(credential_name, entry, config=config)


def record_listener_restart_failure(
    credential_name: str,
    error: str,
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Increment the persisted restart failure counter for one credential."""
    current = get_listener_recovery_state(credential_name, config=config)
    consecutive_failures = current["consecutive_restart_failures"] + 1
    entry = {
        "consecutive_restart_failures": consecutive_failures,
        "last_restart_attempt_at": datetime.now(timezone.utc).isoformat(),
        "last_restart_result": "failed",
        "last_error": error,
        "auto_restart_paused": consecutive_failures >= _MAX_AUTO_RESTART_FAILURES,
    }
    return _update_entry(credential_name, entry, config=config)


def probe_listener_runtime(
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Probe the current listener runtime state without mutating it."""
    resolved = config or SDKConfig.load()
    service_status: dict[str, Any] = {}
    try:
        from service_manager import get_service_manager

        service_status = get_service_manager().status()
    except Exception as exc:  # noqa: BLE001
        service_status = {
            "installed": False,
            "running": False,
            "error": str(exc),
        }
        logger.debug("Failed to query listener service status", exc_info=True)

    service_running = bool(service_status.get("running", False))
    installed = bool(service_status.get("installed", False))
    daemon_available = is_local_daemon_available(config=resolved)
    return {
        "installed": installed,
        "running": service_running or daemon_available,
        "service_running": service_running,
        "daemon_available": daemon_available,
        "service_status": service_status,
    }


def _build_runtime_report(
    *,
    state: dict[str, Any],
    probe: dict[str, Any],
    was_running: bool,
    degraded: bool,
    restart_attempted: bool = False,
    restart_succeeded: bool = False,
) -> dict[str, Any]:
    """Merge probe and persisted state into one caller-facing report."""
    report = {
        "installed": probe["installed"],
        "running": probe["running"],
        "service_running": probe["service_running"],
        "daemon_available": probe["daemon_available"],
        "service_status": probe["service_status"],
        "was_running": was_running,
        "degraded": degraded,
        "restart_attempted": restart_attempted,
        "restart_succeeded": restart_succeeded,
        **state,
    }
    return report


def get_listener_runtime_report(
    credential_name: str,
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Return the current listener runtime report without auto-restart."""
    probe = probe_listener_runtime(config=config)
    state = get_listener_recovery_state(credential_name, config=config)
    if probe["running"]:
        state = note_listener_healthy(credential_name, config=config)
    return _build_runtime_report(
        state=state,
        probe=probe,
        was_running=probe["running"],
        degraded=False,
    )


def ensure_listener_runtime(
    credential_name: str,
    *,
    config: SDKConfig | None = None,
) -> dict[str, Any]:
    """Ensure the listener runtime is healthy, with persisted restart backoff."""
    resolved = config or SDKConfig.load()
    initial_probe = probe_listener_runtime(config=resolved)
    if initial_probe["running"]:
        state = note_listener_healthy(credential_name, config=resolved)
        return _build_runtime_report(
            state=state,
            probe=initial_probe,
            was_running=True,
            degraded=False,
        )

    current_state = get_listener_recovery_state(credential_name, config=resolved)
    if current_state["auto_restart_paused"]:
        return _build_runtime_report(
            state=current_state,
            probe=initial_probe,
            was_running=False,
            degraded=True,
        )

    if not initial_probe["installed"]:
        state = record_listener_restart_failure(
            credential_name,
            "Listener service is not installed",
            config=resolved,
        )
        final_probe = probe_listener_runtime(config=resolved)
        return _build_runtime_report(
            state=state,
            probe=final_probe,
            was_running=False,
            degraded=True,
            restart_attempted=True,
            restart_succeeded=False,
        )

    try:
        from service_manager import get_service_manager

        get_service_manager().start()
    except Exception as exc:  # noqa: BLE001
        state = record_listener_restart_failure(
            credential_name,
            str(exc),
            config=resolved,
        )
        final_probe = probe_listener_runtime(config=resolved)
        return _build_runtime_report(
            state=state,
            probe=final_probe,
            was_running=False,
            degraded=True,
            restart_attempted=True,
            restart_succeeded=False,
        )

    for _ in range(5):
        time.sleep(0.2)
        final_probe = probe_listener_runtime(config=resolved)
        if final_probe["running"]:
            state = note_listener_healthy(
                credential_name,
                config=resolved,
                result="restarted",
            )
            return _build_runtime_report(
                state=state,
                probe=final_probe,
                was_running=False,
                degraded=True,
                restart_attempted=True,
                restart_succeeded=True,
            )

    state = record_listener_restart_failure(
        credential_name,
        "Listener restart attempt did not become healthy",
        config=resolved,
    )
    final_probe = probe_listener_runtime(config=resolved)
    return _build_runtime_report(
        state=state,
        probe=final_probe,
        was_running=False,
        degraded=True,
        restart_attempted=True,
        restart_succeeded=False,
    )


__all__ = [
    "ensure_listener_runtime",
    "get_listener_recovery_state",
    "get_listener_runtime_report",
    "note_listener_healthy",
    "probe_listener_runtime",
    "record_listener_restart_failure",
]
