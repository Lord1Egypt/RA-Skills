"""
A2A Gateway v2.2 — Unified Agent Performance & Health

Three-layer internal structure:
  Layer 1: runtime_state   — volatile liveness (online/offline/degraded)
  Layer 2: historical_stats — stable success/latency from event replay
  Layer 3: scoring_policy   — derived reliability score for router

Single source of truth: event log → replay → all stats derived.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from event_log import get_events_for_task, get_all_tasks, append
from schema import EventType, new_event

WORKSPACE = Path(__file__).parent.parent
PERF_FILE = WORKSPACE / "registry" / "performance.json"

STALE_HOURS = 24  # agent considered stale after 24h inactivity


# ═══════════════════════════════════════════════════════════════════════════
# Layer 1: Runtime State (volatile)
# ═══════════════════════════════════════════════════════════════════════════

def check_liveness(agent_id: str, card: Dict[str, Any]) -> str:
    """Check if an agent is alive based on last activity timestamp."""
    status = card.get("status", "unknown")
    if status == "offline":
        return "offline"

    updated_at = card.get("updated_at")
    if not updated_at:
        return "unknown"

    try:
        dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        hours = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
        if hours <= STALE_HOURS:
            return "online" if status == "online" else "degraded"
        return "stale"
    except (ValueError, TypeError):
        return "unknown"


# ═══════════════════════════════════════════════════════════════════════════
# Layer 2: Historical Stats (stable, derived from event log)
# ═══════════════════════════════════════════════════════════════════════════

def empty_stats() -> Dict[str, Any]:
    return {
        "total_tasks": 0,
        "successes": 0,
        "failures": 0,
        "latencies_ms": [],     # ring buffer, last 100
        "failure_reasons": {},
        "last_active": None,
    }


def _compute_latency(events: List[Dict[str, Any]]) -> Optional[float]:
    """Latency from dispatched→terminal in milliseconds."""
    t1 = t2 = None
    for evt in events:
        if evt["event_type"] == EventType.TASK_DISPATCHED.value:
            t1 = evt["timestamp"]
        elif evt["event_type"] in (EventType.TASK_COMPLETED.value, EventType.TASK_FAILED.value):
            t2 = evt["timestamp"]
    if t1 and t2:
        try:
            d1 = datetime.fromisoformat(t1.replace("Z", "+00:00"))
            d2 = datetime.fromisoformat(t2.replace("Z", "+00:00"))
            return (d2 - d1).total_seconds() * 1000
        except (ValueError, TypeError):
            pass
    return None


def rebuild_stats() -> Dict[str, Dict[str, Any]]:
    """Full rebuild of historical stats from event log."""
    stats: Dict[str, Dict[str, Any]] = {}
    for task_id in get_all_tasks():
        events = get_events_for_task(task_id)
        if not events:
            continue

        agent_id = None
        outcome = None
        error = None

        for evt in events:
            etype = evt["event_type"]
            payload = evt.get("payload", {})
            if etype == EventType.TASK_DISPATCHED.value:
                agent_id = payload.get("target_agent") or evt.get("agent_id")
            elif etype == EventType.TASK_COMPLETED.value:
                outcome = "success"
            elif etype == EventType.TASK_FAILED.value:
                outcome = "failure"
                error = payload.get("error", "unknown")

        if not agent_id:
            continue

        if agent_id not in stats:
            stats[agent_id] = empty_stats()

        s = stats[agent_id]
        s["total_tasks"] += 1

        latency = _compute_latency(events)
        if latency is not None:
            s["latencies_ms"].append(latency)
            if len(s["latencies_ms"]) > 100:
                s["latencies_ms"] = s["latencies_ms"][-100:]

        if outcome == "success":
            s["successes"] += 1
        elif outcome == "failure":
            s["failures"] += 1
            if error:
                s["failure_reasons"][error] = s["failure_reasons"].get(error, 0) + 1

        s["last_active"] = events[-1]["timestamp"]

    return stats


# ═══════════════════════════════════════════════════════════════════════════
# Layer 3: Scoring Policy (derived reliability score for router)
# ═══════════════════════════════════════════════════════════════════════════

def reliability_score(stats: Dict[str, Any]) -> float:
    """
    Single scalar reliability score 0.0-1.0.

    Simple formula: success_rate.
    Minimum 3 tasks required for meaningful score.
    """
    total = stats["total_tasks"]
    if total == 0:
        return 0.5  # neutral default
    return stats["successes"] / total


def _p50(latencies: List[float]) -> Optional[float]:
    if not latencies:
        return None
    s = sorted(latencies)
    return s[len(s) // 2]


def _recommend_status(stats: Dict[str, Any], liveness: str) -> str:
    """Recommend agent status based on data + liveness."""
    if liveness in ("offline", "stale"):
        return "offline"
    score = reliability_score(stats)
    if stats["total_tasks"] < 3:
        return liveness  # not enough data, trust liveness
    if score >= 0.8:
        return "online"
    if score >= 0.5:
        return "degraded"
    return "offline"


# ═══════════════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════════════

def get_agent_performance(agent_id: str, card: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get unified performance snapshot for one agent.
    Combines all three layers.
    """
    all_stats = rebuild_stats()
    stats = all_stats.get(agent_id, empty_stats())
    liveness = check_liveness(agent_id, card or {})

    return {
        "agent_id": agent_id,
        "layer_1_runtime": {
            "liveness": liveness,
        },
        "layer_2_historical": {
            "total_tasks": stats["total_tasks"],
            "successes": stats["successes"],
            "failures": stats["failures"],
            "latency_p50_ms": _p50(stats["latencies_ms"]),
            "top_failures": dict(
                sorted(stats["failure_reasons"].items(), key=lambda x: -x[1])[:3]
            ),
            "last_active": stats["last_active"],
        },
        "layer_3_scoring": {
            "reliability": round(reliability_score(stats), 4),
            "status_recommendation": _recommend_status(stats, liveness),
        },
    }


def rank_agents(cards: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Rank all agents by reliability score (for router consumption)."""
    all_stats = rebuild_stats()
    ranked = []
    for agent_id, stats in all_stats.items():
        liveness = check_liveness(agent_id, (cards or {}).get(agent_id, {}))
        score = reliability_score(stats)
        ranked.append({
            "agent_id": agent_id,
            "total_tasks": stats["total_tasks"],
            "reliability": round(score, 4),
            "liveness": liveness,
            "status": _recommend_status(stats, liveness),
        })
    ranked.sort(key=lambda x: -x["reliability"])
    return ranked


def record_outcome(task_id: str) -> Optional[Dict[str, Any]]:
    """
    Record task outcome into performance system.
    Called after task reaches terminal state.

    1. Emit route.feedback event with reason
    2. Rebuild stats (derived from events)
    3. Persist
    """
    from event_log import replay_state as _replay

    state = _replay(task_id)
    if not state or state["current_state"] not in ("COMPLETED", "FAILED", "CANCELLED"):
        return None

    agent_id = state.get("agent_id", "unknown")
    current = state["current_state"]

    if current == "COMPLETED":
        reason = f"Agent {agent_id} completed task successfully"
    elif current == "FAILED":
        reason = f"Agent {agent_id} failed: {state.get('error', 'unknown')}"
    else:
        reason = f"Task {task_id} {current.lower()}"

    event = new_event(
        event_type=EventType.ROUTE_FEEDBACK,
        task_id=task_id,
        agent_id=agent_id,
        payload={"outcome": current, "error": state.get("error")},
    )
    event["semantics"] = {"reason": reason}
    event["schema_version"] = "2.2"
    append(event)

    # Rebuild and persist
    stats = rebuild_stats()
    _persist(stats)

    return event


def _persist(stats: Dict[str, Any]):
    PERF_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PERF_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "agents": stats,
        }, f, indent=2, ensure_ascii=False)


# ── CLI (minimal) ──────────────────────────────────────────────────────────

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 performance.py <agent_id>  — show agent performance")
        print("       python3 performance.py rank          — rank all agents")
        sys.exit(1)

    if sys.argv[1] == "rank":
        ranked = rank_agents()
        for r in ranked:
            print(f"{r['agent_id']:<35} reliability={r['reliability']:.3f}  "
                  f"tasks={r['total_tasks']}  status={r['status']}")
    else:
        perf = get_agent_performance(sys.argv[1])
        print(json.dumps(perf, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
