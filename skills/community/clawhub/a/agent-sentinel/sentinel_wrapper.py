"""
sentinel_wrapper.py
Local-first bridge between OpenClaw and AgentSentinel.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from urllib import error, request
import uuid


DEFAULT_CONFIG = """
budgets:
  session: 5.00
  run: 1.00
denied_actions:
  - "rm -rf /"
  - "format"
""".lstrip()

DEFAULT_POLICY = {
    "budgets": {
        "session": 5.0,
        "run": 1.0,
    },
    "denied_actions": [
        "rm -rf /",
        "format",
    ],
}

DEFAULT_STATE = {
    "session_total": 0.0,
    "run_total": 0.0,
    "run_id": "",
    "synced_events": 0,
}

PLATFORM_URL = "https://api.agentsentinel.dev"


def _agent_sentinel_home() -> Path:
    return Path(os.getenv("AGENT_SENTINEL_HOME", ".agent-sentinel"))


def _state_path() -> Path:
    return _agent_sentinel_home() / "openclaw_state.json"


def _events_path() -> Path:
    return _agent_sentinel_home() / "openclaw_events.jsonl"


def _ensure_home() -> None:
    _agent_sentinel_home().mkdir(parents=True, exist_ok=True)


def bootstrap() -> None:
    """Create a starter policy file if missing."""
    _ensure_home()
    config_path = Path("callguard.yaml")
    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG)

    if not _state_path().exists():
        _write_state(DEFAULT_STATE)

    print(
        json.dumps(
            {
                "status": "READY",
                "message": "AgentSentinel initialized in local-first mode.",
                "config_path": str(config_path),
                "state_path": str(_state_path()),
                "events_path": str(_events_path()),
                "remote_sync": False,
                "remote_sync_note": (
                    "Set AGENT_SENTINEL_API_KEY and run `sync` to upload "
                    "local events to AgentSentinel."
                ),
            }
        )
    )


def _cloud_api_key() -> str:
    return os.getenv("AGENT_SENTINEL_API_KEY", "").strip()


def _cloud_enabled() -> bool:
    return bool(_cloud_api_key())


def _read_state() -> dict[str, object]:
    path = _state_path()
    if not path.exists():
        state = dict(DEFAULT_STATE)
        state["run_id"] = str(uuid.uuid4())
        return state

    try:
        state = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        state = dict(DEFAULT_STATE)

    if not state.get("run_id"):
        state["run_id"] = str(uuid.uuid4())
    return state


def _write_state(state: dict[str, object]) -> None:
    _ensure_home()
    _state_path().write_text(json.dumps(state, indent=2))


def _load_policy() -> dict[str, object]:
    config_path = Path("callguard.yaml")
    if not config_path.exists():
        return dict(DEFAULT_POLICY)

    policy = {
        "budgets": dict(DEFAULT_POLICY["budgets"]),
        "denied_actions": list(DEFAULT_POLICY["denied_actions"]),
    }
    section: str | None = None

    for raw_line in config_path.read_text().splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if not line.startswith(" "):
            if stripped == "budgets:":
                section = "budgets"
            elif stripped == "denied_actions:":
                section = "denied_actions"
            else:
                section = None
            continue

        if section == "budgets":
            if ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            try:
                policy["budgets"][key.strip()] = float(value.strip())
            except ValueError:
                continue
        elif section == "denied_actions" and stripped.startswith("- "):
            action = stripped[2:].strip().strip("\"'")
            if action and action not in policy["denied_actions"]:
                policy["denied_actions"].append(action)

    return policy


def _status_payload(remote_enabled: bool) -> dict[str, object]:
    policy = _load_policy()
    state = _read_state()
    pending_events = max(_event_count() - int(state.get("synced_events", 0)), 0)

    run_budget = policy["budgets"].get("run")
    session_budget = policy["budgets"].get("session")

    return {
        "status": "OK",
        "remote_sync": remote_enabled,
        "cloud_configured": _cloud_enabled(),
        "run_total": state["run_total"],
        "session_total": state["session_total"],
        "run_id": state["run_id"],
        "pending_sync_events": pending_events,
        "run_budget": run_budget,
        "session_budget": session_budget,
        "remaining_run_budget": run_budget - state["run_total"],
        "remaining_session_budget": session_budget - state["session_total"],
        "denied_actions": policy["denied_actions"],
    }


def cmd_status() -> None:
    remote_enabled = False
    print(json.dumps(_status_payload(remote_enabled)))


def cmd_reset(args: argparse.Namespace) -> None:
    state = _read_state()

    if args.scope == "all":
        state = dict(DEFAULT_STATE)
        state["run_id"] = str(uuid.uuid4())
    else:
        state["run_total"] = 0.0
        state["run_id"] = str(uuid.uuid4())

    _write_state(state)
    print(
        json.dumps(
            {
                "status": "RESET",
                "scope": args.scope,
                "run_total": state["run_total"],
                "session_total": state["session_total"],
            }
        )
    )


def _append_event(
    *,
    state: dict[str, object],
    action_name: str,
    estimated_cost: float,
    outcome: str,
    details: dict[str, object],
) -> None:
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "action": action_name,
        "cost_usd": max(estimated_cost, 0.0),
        "duration_ms": 0.0,
        "outcome": outcome,
        "tags": ["openclaw", "skill", "local-first"],
        "payload": {
            "inputs": details,
            "outputs": {
                "run_total": state["run_total"],
                "session_total": state["session_total"],
            },
        },
    }
    _ensure_home()
    with _events_path().open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _event_count() -> int:
    path = _events_path()
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def cmd_sync() -> None:
    state = _read_state()
    api_key = _cloud_api_key()
    if not api_key:
        print(
            json.dumps(
                {
                    "status": "ERROR",
                    "message": "Set AGENT_SENTINEL_API_KEY to enable cloud sync.",
                }
            )
        )
        return

    path = _events_path()
    if not path.exists():
        print(json.dumps({"status": "OK", "synced": 0, "pending": 0}))
        return

    with path.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()

    synced_events = int(state.get("synced_events", 0))
    pending_lines = lines[synced_events:]
    entries = [json.loads(line) for line in pending_lines if line.strip()]
    if not entries:
        print(json.dumps({"status": "OK", "synced": 0, "pending": 0}))
        return

    body = json.dumps(
        {
            "run_id": state["run_id"],
            "agent_id": os.getenv("AGENT_SENTINEL_AGENT_ID"),
            "entries": entries,
        }
    ).encode("utf-8")

    req = request.Request(
        url=f"{PLATFORM_URL}/api/v1/ingest",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=3) as response:
            if 200 <= response.status < 300:
                state["synced_events"] = synced_events + len(entries)
                _write_state(state)
                print(
                    json.dumps(
                        {
                            "status": "SYNCED",
                            "synced": len(entries),
                            "pending": 0,
                            "remote_sync": True,
                        }
                    )
                )
                return
            print(
                json.dumps(
                    {
                        "status": "ERROR",
                        "message": f"Cloud sync failed with status {response.status}.",
                        "pending": len(entries),
                    }
                )
            )
    except (error.URLError, error.HTTPError, TimeoutError):
        print(
            json.dumps(
                {
                    "status": "ERROR",
                    "message": "Cloud sync failed.",
                    "pending": len(entries),
                }
            )
        )


def cmd_check(args: argparse.Namespace) -> None:
    remote_enabled = False
    policy = _load_policy()
    state = _read_state()
    cmd = args.cmd.strip()
    estimated_cost = float(args.cost)

    denied_action = next(
        (pattern for pattern in policy["denied_actions"] if pattern and pattern in cmd),
        None,
    )
    if denied_action:
        _append_event(
            state=state,
            action_name="openclaw_check",
            estimated_cost=estimated_cost,
            outcome="error",
            details={
                "cmd": cmd,
                "decision": "blocked",
                "reason": f"Action matches denied pattern: {denied_action}",
            },
        )
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "cmd": cmd,
                    "estimated_cost": estimated_cost,
                    "error": f"Action matches denied pattern: {denied_action}",
                    "instruction": "Action blocked by local safety policy.",
                    "remote_sync": remote_enabled,
                }
            )
        )
        return

    run_total = state["run_total"] + estimated_cost
    session_total = state["session_total"] + estimated_cost
    run_budget = float(policy["budgets"]["run"])
    session_budget = float(policy["budgets"]["session"])

    if run_total > run_budget:
        _append_event(
            state=state,
            action_name="openclaw_check",
            estimated_cost=estimated_cost,
            outcome="error",
            details={
                "cmd": cmd,
                "decision": "blocked",
                "reason": (
                    f"Run budget exceeded: {run_total:.2f} > {run_budget:.2f} USD"
                ),
            },
        )
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "cmd": cmd,
                    "estimated_cost": estimated_cost,
                    "error": (
                        f"Run budget exceeded: {run_total:.2f} > {run_budget:.2f} USD"
                    ),
                    "instruction": "Action blocked by local safety policy.",
                    "remote_sync": remote_enabled,
                }
            )
        )
        return

    if session_total > session_budget:
        _append_event(
            state=state,
            action_name="openclaw_check",
            estimated_cost=estimated_cost,
            outcome="error",
            details={
                "cmd": cmd,
                "decision": "blocked",
                "reason": (
                    "Session budget exceeded: "
                    f"{session_total:.2f} > {session_budget:.2f} USD"
                ),
            },
        )
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "cmd": cmd,
                    "estimated_cost": estimated_cost,
                    "error": (
                        "Session budget exceeded: "
                        f"{session_total:.2f} > {session_budget:.2f} USD"
                    ),
                    "instruction": "Action blocked by local safety policy.",
                    "remote_sync": remote_enabled,
                }
            )
        )
        return

    state["run_total"] = run_total
    state["session_total"] = session_total
    _write_state(state)
    _append_event(
        state=state,
        action_name="openclaw_check",
        estimated_cost=estimated_cost,
        outcome="success",
        details={
            "cmd": cmd,
            "decision": "allowed",
        },
    )

    payload = _status_payload(remote_enabled)
    payload.update(
        {
            "status": "ALLOWED",
            "message": "Action permitted.",
            "cmd": cmd,
            "estimated_cost": estimated_cost,
        }
    )
    print(json.dumps(payload))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", action="store_true")
    subparsers = parser.add_subparsers(dest="command")

    check = subparsers.add_parser("check")
    check.add_argument("--cmd", required=True)
    check.add_argument("--cost", type=float, default=0.01)

    subparsers.add_parser("status")
    subparsers.add_parser("sync")
    reset = subparsers.add_parser("reset")
    reset.add_argument("--scope", choices=["run", "all"], default="run")

    args = parser.parse_args()

    if args.bootstrap:
        bootstrap()
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "status":
        cmd_status()
    elif args.command == "sync":
        cmd_sync()
    elif args.command == "reset":
        cmd_reset(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
