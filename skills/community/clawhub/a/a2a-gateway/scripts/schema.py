"""
A2A Gateway v2 — Unified Schema Definitions

Agent Card v2, Task State Machine, Event Payload contracts.
All type annotations are JSON-serializable dicts for maximum interoperability.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


# ── Agent Card v2 ──────────────────────────────────────────────────────────

class LatencyClass(str, Enum):
    """Agent response latency classification."""
    FAST = "fast"          # < 5s, synchronous
    NORMAL = "normal"      # 5-30s
    SLOW = "slow"          # 30s-5min
    ASYNC = "async"        # callback required


class ReliabilityTier(str, Enum):
    """Retry / idempotency contract."""
    AT_MOST_ONCE = "at_most_once"
    AT_LEAST_ONCE = "at_least_once"
    EXACTLY_ONCE = "exactly_once"


class AgentStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


def new_agent_card(
    agent_id: str,
    name: str,
    description: str = "",
    *,
    skills: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    input_schema: Optional[Dict[str, Any]] = None,
    output_schema: Optional[Dict[str, Any]] = None,
    side_effects: bool = False,
    latency_class: LatencyClass = LatencyClass.NORMAL,
    reliability_tier: ReliabilityTier = ReliabilityTier.AT_MOST_ONCE,
    tool_permissions: Optional[List[str]] = None,
    status: AgentStatus = AgentStatus.ONLINE,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a v2 Agent Card with full contract fields."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": "2.0",
        "agent_id": agent_id,
        "name": name,
        "description": description,
        # ── Contract Layer ──
        "contract": {
            "input_schema": input_schema or {
                "type": "object",
                "properties": {},
            },
            "output_schema": output_schema or {
                "type": "object",
                "properties": {},
            },
            "side_effects": side_effects,
            "latency_class": latency_class.value,
            "reliability_tier": reliability_tier.value,
            "tool_permissions": tool_permissions or [],
        },
        # ── Capability Layer ──
        "skills": skills or [],
        "capabilities": capabilities or skills or [],
        # ── Lifecycle ──
        "status": status.value,
        "created_at": now,
        "updated_at": now,
        "metadata": metadata or {},
    }


# ── Task State Machine ─────────────────────────────────────────────────────

class TaskState(str, Enum):
    CREATED = "CREATED"
    DISPATCHED = "DISPATCHED"
    RUNNING = "RUNNING"
    WAITING_CALLBACK = "WAITING_CALLBACK"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATED = "COMPENSATED"
    CANCELLED = "CANCELLED"


# Allowed transitions: from state → set of valid next states
TRANSITION_TABLE: Dict[TaskState, set[TaskState]] = {
    TaskState.CREATED:      {TaskState.DISPATCHED, TaskState.CANCELLED},
    TaskState.DISPATCHED:   {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.RUNNING:      {TaskState.WAITING_CALLBACK, TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.WAITING_CALLBACK: {TaskState.RUNNING, TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.COMPLETED:    {TaskState.COMPENSATED},
    TaskState.FAILED:       {TaskState.COMPENSATED, TaskState.DISPATCHED},  # retry
    TaskState.COMPENSATED:  set(),        # terminal
    TaskState.CANCELLED:    set(),        # terminal
}

# Terminal states (no further transitions)
TERMINAL_STATES: set[TaskState] = {TaskState.COMPENSATED, TaskState.CANCELLED}


def validate_transition(from_state: TaskState, to_state: TaskState) -> bool:
    """Check if a state transition is legal."""
    return to_state in TRANSITION_TABLE.get(from_state, set())


def valid_transitions(from_state: TaskState) -> set[TaskState]:
    """Return the set of valid next states."""
    return TRANSITION_TABLE.get(from_state, set())


# ── Event Payload Contracts ────────────────────────────────────────────────

class EventType(str, Enum):
    """Event types for the append-only event log."""
    # Lifecycle
    TASK_CREATED = "task.created"
    TASK_DISPATCHED = "task.dispatched"
    TASK_RUNNING = "task.running"
    TASK_WAITING_CALLBACK = "task.waiting_callback"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    TASK_COMPENSATED = "task.compensated"
    TASK_CANCELLED = "task.cancelled"
    # Routing
    ROUTE_ATTEMPT = "route.attempt"
    ROUTE_MATCH = "route.match"
    ROUTE_MISS = "route.miss"
    ROUTE_FEEDBACK = "route.feedback"
    # Agent
    AGENT_REGISTERED = "agent.registered"
    AGENT_UPDATED = "agent.updated"
    AGENT_STATUS_CHANGED = "agent.status_changed"
    AGENT_PERFORMANCE_UPDATED = "agent.performance_updated"
    # Health
    HEALTH_CHECK = "health.check"
    HEALTH_DRIFT_ALERT = "health.drift_alert"
    # Tool
    TOOL_CALL = "tool.call"


def new_event(
    event_type: EventType,
    agent_id: Optional[str] = None,
    task_id: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None,
    causation_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create an immutable event for the append-only event log."""
    return {
        "event_id": "",          # filled by event log on append
        "event_type": event_type.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "task_id": task_id,
        "payload": payload or {},
        "correlation_id": correlation_id,
        "causation_id": causation_id,
        "metadata": metadata or {},
    }


# ── Routing Score ──────────────────────────────────────────────────────────

def new_routing_score(
    agent_id: str,
    capability_fit: float = 0.0,
    context_fit: float = 0.0,
    risk_fit: float = 0.0,
    *,
    weights: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Create a routing score record for a candidate agent."""
    w = weights or {"capability": 0.5, "context": 0.3, "risk": 0.2}
    total = (
        capability_fit * w.get("capability", 0.5) +
        context_fit * w.get("context", 0.3) +
        risk_fit * w.get("risk", 0.2)
    )
    return {
        "agent_id": agent_id,
        "scores": {
            "capability_fit": capability_fit,
            "context_fit": context_fit,
            "risk_fit": risk_fit,
        },
        "weights": w,
        "total": round(total, 4),
    }
