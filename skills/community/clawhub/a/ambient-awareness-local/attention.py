from __future__ import annotations

from typing import Dict, Any


DEFAULT_EVENT_WEIGHTS = {
    "clock_tick": 0.05,
    "file_created": 0.65,
    "file_modified": 0.55,
    "file_deleted": 0.6,
    "sensor_error": 0.8,
    "motion_detected": 0.75,
    "audio_detected": 0.65,
    "text_observed": 0.5,
}


def score_event(event: Dict[str, Any]) -> float:
    event_type = event.get("event_type", "")
    base = DEFAULT_EVENT_WEIGHTS.get(event_type, 0.2)
    confidence = float(event.get("confidence", 1.0))
    hint = float(event.get("importance_hint", 0.0))
    score = max(base, hint) * confidence
    return max(0.0, min(1.0, score))


def decision_for_score(score: float, wake_threshold: float, queue_threshold: float) -> str:
    if score >= wake_threshold:
        return "wake_now"
    if score >= queue_threshold:
        return "queue"
    return "log_only"
