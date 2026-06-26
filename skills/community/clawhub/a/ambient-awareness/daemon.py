from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from attention import score_event, decision_for_score
from sensor_loader import load_sensors, read_json
from sensor_api import AwarenessEvent

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "state"
EVENT_LOG = STATE_DIR / "event_log.jsonl"
WAKE_LOG = STATE_DIR / "wake_requests.jsonl"
WORLD_STATE = STATE_DIR / "world_state.json"
REGISTRY = ROOT / "registry.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, item: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def load_world_state() -> Dict[str, Any]:
    if WORLD_STATE.exists():
        with WORLD_STATE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "created_at": now_iso(),
        "last_poll_at": None,
        "sensors": {},
        "recent_events": [],
        "counters": {
            "total_events": 0,
            "wake_requests": 0,
            "queued_events": 0
        }
    }


def save_world_state(state: Dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = WORLD_STATE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    tmp.replace(WORLD_STATE)


def normalize_event(event: AwarenessEvent | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(event, AwarenessEvent):
        data = event.to_dict()
    else:
        data = dict(event)
    data["trusted_instruction"] = False
    data.setdefault("timestamp", now_iso())
    data.setdefault("confidence", 1.0)
    data.setdefault("importance_hint", 0.0)
    data.setdefault("payload", {})
    return data


def handle_events(events: List[Dict[str, Any]], registry: Dict[str, Any], state: Dict[str, Any]) -> None:
    wake_threshold = float(registry.get("wake_threshold", 0.8))
    queue_threshold = float(registry.get("queue_threshold", 0.5))

    for event in events:
        event_score = score_event(event)
        event["attention_score"] = event_score
        decision = decision_for_score(event_score, wake_threshold, queue_threshold)
        event["attention_decision"] = decision

        append_jsonl(EVENT_LOG, event)
        state["counters"]["total_events"] += 1
        state["recent_events"].append(event)
        state["recent_events"] = state["recent_events"][-25:]

        if decision in {"wake_now", "queue"}:
            wake_request = {
                "timestamp": now_iso(),
                "decision": decision,
                "reason": event.get("summary", "No summary"),
                "source_event_id": event.get("event_id"),
                "attention_score": event_score,
                "event": event,
            }
            append_jsonl(WAKE_LOG, wake_request)
            if decision == "wake_now":
                state["counters"]["wake_requests"] += 1
                print(f"WAKE_NOW score={event_score:.2f}: {event.get('summary')}")
            else:
                state["counters"]["queued_events"] += 1
                print(f"QUEUE score={event_score:.2f}: {event.get('summary')}")
        else:
            print(f"LOG_ONLY score={event_score:.2f}: {event.get('summary')}")


def poll_once() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    registry = read_json(REGISTRY)
    sensors = load_sensors(ROOT, REGISTRY)
    state = load_world_state()
    state["last_poll_at"] = now_iso()

    all_events: List[Dict[str, Any]] = []

    for sensor in sensors:
        try:
            health = sensor.healthcheck()
            state["sensors"][sensor.id] = health
            events = [normalize_event(e) for e in sensor.poll()]
            all_events.extend(events)
        except Exception as exc:
            error_event = normalize_event({
                "sensor_id": getattr(sensor, "id", "unknown"),
                "event_type": "sensor_error",
                "summary": f"Sensor failed: {exc}",
                "confidence": 1.0,
                "importance_hint": 0.9,
                "payload": {"error": repr(exc)},
            })
            all_events.append(error_event)

    handle_events(all_events, registry, state)
    save_world_state(state)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ambient Awareness daemon")
    parser.add_argument("--once", action="store_true", help="Poll sensors once and exit")
    parser.add_argument("--loop", action="store_true", help="Poll sensors forever")
    parser.add_argument("--interval", type=float, default=5.0, help="Loop interval in seconds")
    args = parser.parse_args()

    if not args.once and not args.loop:
        args.once = True

    if args.once:
        poll_once()
        return

    while True:
        poll_once()
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
