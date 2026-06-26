"""
A2A Gateway v2 — Task Center with State Machine

Every task mutation produces an event via event_log.append().
Current state is always reconstructed from event replay.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from schema import (
    TaskState, EventType, validate_transition, valid_transitions,
    new_event, new_routing_score,
    TRANSITION_TABLE, TERMINAL_STATES,
)
from event_log import append, get_events_for_task, replay_state, get_all_tasks


def generate_task_id(prefix: str = "task") -> str:
    """Generate a unique task ID."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:6]}"


def create_task(
    description: str,
    *,
    from_agent: str = "a2a-gateway",
    skill: Optional[str] = None,
    priority: str = "normal",
    context: Optional[Dict[str, Any]] = None,
    task_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new task. Produces task.created event."""
    task_id = task_id or generate_task_id()

    event = new_event(
        event_type=EventType.TASK_CREATED,
        agent_id=from_agent,
        task_id=task_id,
        payload={
            "description": description,
            "skill": skill,
            "priority": priority,
            "context": context or {},
        },
    )
    append(event)

    return {
        "task_id": task_id,
        "state": TaskState.CREATED.value,
        "description": description,
    }


def dispatch_task(
    task_id: str,
    target_agent: str,
    *,
    by: str = "a2a-gateway",
    route_score: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Dispatch a task to a target agent.
    State: CREATED → DISPATCHED
    Produces: route.match + task.dispatched events
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if not validate_transition(current, TaskState.DISPATCHED):
        raise ValueError(
            f"Cannot dispatch task '{task_id}': "
            f"invalid transition {current.value} → DISPATCHED. "
            f"Valid: {[s.value for s in valid_transitions(current)]}"
        )

    # Route match event
    if route_score:
        route_event = new_event(
            event_type=EventType.ROUTE_MATCH,
            task_id=task_id,
            agent_id=by,
            payload={"target_agent": target_agent, "score": route_score},
            correlation_id=correlation_id,
        )
        append(route_event)

    # Dispatch event
    dispatch_event = new_event(
        event_type=EventType.TASK_DISPATCHED,
        task_id=task_id,
        agent_id=by,
        payload={"target_agent": target_agent},
        correlation_id=correlation_id,
    )
    append(dispatch_event)

    return replay_state(task_id)


def start_task(
    task_id: str,
    *,
    by_agent: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Mark a task as running.
    State: DISPATCHED → RUNNING
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if not validate_transition(current, TaskState.RUNNING):
        raise ValueError(
            f"Cannot start task '{task_id}': "
            f"invalid transition {current.value} → RUNNING"
        )

    event = new_event(
        event_type=EventType.TASK_RUNNING,
        task_id=task_id,
        agent_id=by_agent,
        correlation_id=correlation_id,
    )
    append(event)

    return replay_state(task_id)


def wait_callback(
    task_id: str,
    *,
    by_agent: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Mark task as waiting for async callback.
    State: RUNNING → WAITING_CALLBACK
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if not validate_transition(current, TaskState.WAITING_CALLBACK):
        raise ValueError(
            f"Cannot mark callback for task '{task_id}': "
            f"invalid transition {current.value} → WAITING_CALLBACK"
        )

    event = new_event(
        event_type=EventType.TASK_WAITING_CALLBACK,
        task_id=task_id,
        agent_id=by_agent,
        correlation_id=correlation_id,
    )
    append(event)

    return replay_state(task_id)


def complete_task(
    task_id: str,
    result: Any,
    *,
    by_agent: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Mark a task as completed.
    State: RUNNING | WAITING_CALLBACK → COMPLETED
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if not validate_transition(current, TaskState.COMPLETED):
        raise ValueError(
            f"Cannot complete task '{task_id}': "
            f"invalid transition {current.value} → COMPLETED"
        )

    event = new_event(
        event_type=EventType.TASK_COMPLETED,
        task_id=task_id,
        agent_id=by_agent,
        payload={"result": result},
        correlation_id=correlation_id,
    )
    append(event)

    # ── P1 feedback loop: record outcome → adapt router ──
    _record_outcome(task_id)

    return replay_state(task_id)


def fail_task(
    task_id: str,
    error: str,
    *,
    by_agent: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Mark a task as failed.
    State: DISPATCHED | RUNNING | WAITING_CALLBACK → FAILED
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if not validate_transition(current, TaskState.FAILED):
        raise ValueError(
            f"Cannot fail task '{task_id}': "
            f"invalid transition {current.value} → FAILED"
        )

    event = new_event(
        event_type=EventType.TASK_FAILED,
        task_id=task_id,
        agent_id=by_agent,
        payload={"error": error},
        correlation_id=correlation_id,
    )
    append(event)

    # ── P1 feedback loop: record failure → adapt router ──
    _record_outcome(task_id)

    return replay_state(task_id)


def retry_task(
    task_id: str,
    *,
    by_agent: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retry a failed task. FAILED → DISPATCHED.
    This is the only way to re-enter the flow from FAILED.
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if current != TaskState.FAILED:
        raise ValueError(
            f"Cannot retry task '{task_id}': current state is {current.value}, not FAILED"
        )

    # Re-dispatch to the same agent
    target = state.get("agent_id", "unknown")
    return dispatch_task(
        task_id=task_id,
        target_agent=target,
        by=by_agent or "a2a-gateway",
        correlation_id=correlation_id,
    )


def cancel_task(
    task_id: str,
    reason: str = "",
    *,
    by_agent: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Cancel a task. Any non-terminal state → CANCELLED.
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if current in TERMINAL_STATES:
        raise ValueError(
            f"Cannot cancel task '{task_id}': already in terminal state {current.value}"
        )

    if not validate_transition(current, TaskState.CANCELLED):
        raise ValueError(
            f"Cannot cancel task '{task_id}' from {current.value}"
        )

    event = new_event(
        event_type=EventType.TASK_CANCELLED,
        task_id=task_id,
        agent_id=by_agent,
        payload={"reason": reason},
    )
    append(event)

    _record_outcome(task_id)

    return replay_state(task_id)


def compensate_task(
    task_id: str,
    reason: str = "",
    *,
    by_agent: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Mark a task as compensated (rollback applied).
    State: COMPLETED | FAILED → COMPENSATED
    """
    state = replay_state(task_id)
    if not state:
        raise ValueError(f"Task '{task_id}' not found")

    current = TaskState(state["current_state"])
    if not validate_transition(current, TaskState.COMPENSATED):
        raise ValueError(
            f"Cannot compensate task '{task_id}': "
            f"invalid transition {current.value} → COMPENSATED"
        )

    event = new_event(
        event_type=EventType.TASK_COMPENSATED,
        task_id=task_id,
        agent_id=by_agent,
        payload={"reason": reason},
    )
    append(event)

    return replay_state(task_id)


def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Get current task state via event replay."""
    return replay_state(task_id)


def get_task_history(task_id: str) -> List[Dict[str, Any]]:
    """Get full event history for a task."""
    return get_events_for_task(task_id)


def list_tasks(
    filter_state: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List all tasks, optionally filtered by state."""
    task_ids = get_all_tasks()
    result = []

    for tid in task_ids:
        state = replay_state(tid)
        if state:
            if filter_state and state["current_state"] != filter_state:
                continue
            result.append(state)

    return result


def summary() -> Dict[str, Any]:
    """Get a summary of all tasks by state."""
    tasks = list_tasks()
    counts = {}
    for t in tasks:
        s = t["current_state"]
        counts[s] = counts.get(s, 0) + 1

    return {
        "total_tasks": len(tasks),
        "by_state": counts,
        "terminal": sum(
            1 for t in tasks if t["current_state"] in {s.value for s in TERMINAL_STATES}
        ),
        "active": sum(
            1 for t in tasks if t["current_state"] not in {s.value for s in TERMINAL_STATES}
        ),
    }


# ── Internal: feedback hook (delegates to performance.py) ──────────────────

def _record_outcome(task_id: str):
    """Record task outcome for adaptive routing. Import deferred to avoid circular deps."""
    try:
        from performance import record_outcome
        record_outcome(task_id)
    except ImportError:
        pass  # performance module not available — no-op
