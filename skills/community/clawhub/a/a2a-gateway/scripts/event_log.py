"""
A2A Gateway v2.2 — Append-Only Event Log (simplified)

Event Sourcing backbone. Every event is immutable once written.
Task state is derived from event replay, not stored as mutable fields.

No index — direct JSONL scan. Sufficient for <10K events.
Re-add index layer when event count crosses threshold.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from schema import EventType, new_event

WORKSPACE = Path(__file__).parent.parent
EVENT_LOG_FILE = WORKSPACE / "audit" / "audit_log.jsonl"


def _ensure_dir(file_path: Path):
    file_path.parent.mkdir(parents=True, exist_ok=True)


def _generate_event_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"evt_{ts}_{uuid.uuid4().hex[:8]}"


def _scan_log(predicate: Callable[[Dict[str, Any]], bool],
              limit: Optional[int] = None,
              reverse: bool = False) -> List[Dict[str, Any]]:
    """Scan JSONL file with a filter predicate. Single pass, O(n)."""
    if not EVENT_LOG_FILE.exists():
        return []
    results = []
    with open(EVENT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            evt = json.loads(line)
            if predicate(evt):
                results.append(evt)
    if reverse:
        results.reverse()
    if limit is not None:
        results = results[-limit:] if not reverse else results[:limit]
    return results


# ── Core API ───────────────────────────────────────────────────────────────

def append(event: Dict[str, Any]) -> Dict[str, Any]:
    """Append an event to the immutable event log. Returns event with event_id."""
    _ensure_dir(EVENT_LOG_FILE)
    event = dict(event)
    event["event_id"] = _generate_event_id()
    with open(EVENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def get_events_for_task(task_id: str) -> List[Dict[str, Any]]:
    """All events for a task, in append order."""
    return _scan_log(lambda e: e.get("task_id") == task_id)


def get_events_by_type(event_type: EventType, limit: int = 100) -> List[Dict[str, Any]]:
    """Recent events of a specific type."""
    return _scan_log(
        lambda e: e.get("event_type") == event_type.value,
        limit=limit, reverse=True,
    )


def get_events_by_agent(agent_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Recent events involving a specific agent."""
    return _scan_log(
        lambda e: e.get("agent_id") == agent_id,
        limit=limit, reverse=True,
    )


def replay_state(task_id: str) -> Optional[Dict[str, Any]]:
    """
    Reconstruct task state from event replay.
    Source of truth — no mutable state stored elsewhere.
    """
    events = get_events_for_task(task_id)
    if not events:
        return None

    state = {
        "task_id": task_id,
        "current_state": None,
        "created_at": None,
        "dispatched_at": None,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "agent_id": None,
        "error": None,
        "result": None,
        "event_count": len(events),
    }

    for evt in events:
        etype = evt.get("event_type", "")
        payload = evt.get("payload", {})

        if etype == EventType.TASK_CREATED.value:
            state["current_state"] = "CREATED"
            state["created_at"] = evt["timestamp"]

        elif etype == EventType.TASK_DISPATCHED.value:
            state["current_state"] = "DISPATCHED"
            state["dispatched_at"] = evt["timestamp"]
            state["agent_id"] = payload.get("target_agent") or evt.get("agent_id")

        elif etype == EventType.TASK_RUNNING.value:
            state["current_state"] = "RUNNING"
            state["started_at"] = evt["timestamp"]

        elif etype == EventType.TASK_WAITING_CALLBACK.value:
            state["current_state"] = "WAITING_CALLBACK"

        elif etype == EventType.TASK_COMPLETED.value:
            state["current_state"] = "COMPLETED"
            state["completed_at"] = evt["timestamp"]
            state["result"] = payload.get("result")

        elif etype == EventType.TASK_FAILED.value:
            state["current_state"] = "FAILED"
            state["failed_at"] = evt["timestamp"]
            state["error"] = payload.get("error")

        elif etype == EventType.TASK_COMPENSATED.value:
            state["current_state"] = "COMPENSATED"

        elif etype == EventType.TASK_CANCELLED.value:
            state["current_state"] = "CANCELLED"

    return state


def get_all_tasks() -> List[str]:
    """All unique task_ids from the event log (via scan, no index)."""
    seen = set()
    tasks = []
    if not EVENT_LOG_FILE.exists():
        return tasks
    with open(EVENT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            evt = json.loads(line)
            tid = evt.get("task_id")
            if tid and tid not in seen:
                seen.add(tid)
                tasks.append(tid)
    return tasks


def count() -> int:
    """Total events in the log."""
    if not EVENT_LOG_FILE.exists():
        return 0
    n = 0
    with open(EVENT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                n += 1
    return n
