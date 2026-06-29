#!/usr/bin/env python3
"""Decide whether find-community-help should run for a given host state."""

from __future__ import annotations

import json
import re
import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


DEFAULTS = {
    "active_conversation_window": "24h",
    "quiet_after_user_action": "20m",
    "quiet_after_agent_action": "5m",
    "repeat_fingerprint_cooldown": "12h",
    "max_runs_per_thread_per_day": 1,
    "max_runs_per_user_per_day": 3,
}
EVENTS = {
    "heartbeat",
    "scheduled",
    "task_end",
    "failure_recovery",
    "idle_fallback",
    "user_request",
    "manual_request",
}
MANUAL_EVENTS = {"user_request", "manual_request"}
SEMANTIC_SIGNAL_NAMES = {
    "no_clear_next_step",
    "progress_stalled",
    "repeated_local_attempts",
    "suspected_reinventing_wheel",
    "user_requested_community_help",
    "user_requested_deep_community_help",
    "related_failures",
    "user_corrections",
    "unresolved_blocker_count",
    "version_mismatch_seen",
}


@dataclass
class Decision:
    should_run: bool
    search_mode: str
    trigger_reason: str
    reason: str
    error_code: str | None = None
    observed_signals: list[str] | None = None


@dataclass
class ActivityClock:
    now: datetime
    last_thread_activity: datetime
    last_user_action: datetime
    last_agent_action: datetime


@dataclass
class TriggerContext:
    signals: list[str]
    cooldown_bypassed: bool
    scheduled_trigger_managed_by_host: bool
    user_configured_periodic_travel: bool


class InputError(Exception):
    """Raised when a readable state file has malformed fields."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def decision_status(decision: Decision) -> str:
    if decision.trigger_reason == "error":
        return "error"
    return "ready" if decision.should_run else "blocked"


def decision_payload(decision: Decision) -> dict[str, object]:
    payload: dict[str, object] = {
        "should_run": decision.should_run,
        "search_mode": decision.search_mode,
        "trigger_reason": decision.trigger_reason,
        "reason": decision.reason,
        "status": decision_status(decision),
    }
    if decision.error_code is not None:
        payload["error_code"] = decision.error_code
    if decision.observed_signals:
        payload["observed_signals"] = decision.observed_signals
    return payload


def emit(decision: Decision) -> None:
    print(json.dumps(decision_payload(decision), ensure_ascii=False))


def parse_duration(value: str) -> timedelta:
    stripped = value.strip().lower()
    match = re.fullmatch(r"([+-]?\d+)([mhd])", stripped)
    if not match:
        raise InputError("invalid_duration", "invalid duration format")
    amount = int(match.group(1))
    unit = match.group(2)
    if amount <= 0:
        raise InputError("invalid_duration", "duration must be a positive integer with unit")
    if unit == "m":
        return timedelta(minutes=amount)
    if unit == "h":
        return timedelta(hours=amount)
    if unit == "d":
        return timedelta(days=amount)
    raise InputError("invalid_duration", "invalid duration unit")


def parse_timestamp(name: str, value: str) -> datetime:
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise InputError("invalid_timestamp", f"invalid timestamp for {name}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InputError("invalid_timestamp", f"{name} must include a timezone offset")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to a JSON state file")
    return parser.parse_args()


def as_bool(value: object, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    raise InputError("invalid_boolean", "invalid boolean value")


def as_int(value: object, default: int, *, minimum: int | None = None) -> int:
    if value is None:
        parsed = default
    elif isinstance(value, bool):
        raise InputError("invalid_integer", "invalid integer value")
    else:
        try:
            parsed = int(value)
        except (TypeError, ValueError) as exc:
            raise InputError("invalid_integer", "invalid integer value") from exc
    if minimum is not None and parsed < minimum:
        raise InputError("invalid_integer", "invalid integer value")
    return parsed


def as_bool_or_count_signal(value: object, *, threshold: int) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return as_int(value, 0, minimum=0) >= threshold


def get_duration(state: dict[str, object], key: str) -> timedelta:
    raw = state.get(key, DEFAULTS[key])
    if isinstance(raw, str):
        return parse_duration(raw)
    raise InputError("invalid_duration", f"invalid duration value for {key}")


def get_event_kind(state: dict[str, object]) -> str:
    raw = str(state.get("event_kind", "")).strip().lower()
    if raw == "idle":
        raw = "idle_fallback"
    return raw


def safe_event_kind(state: dict[str, object]) -> str:
    event_kind = get_event_kind(state)
    return event_kind if event_kind in EVENTS else "unsupported"


def normalize_label(value: object, default: str) -> str:
    if value is None:
        return default
    text = str(value).strip().lower()
    return text or default


def get_optional_timestamp(state: dict[str, object], key: str) -> datetime | None:
    raw = state.get(key)
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    return parse_timestamp(key, text)


def get_required_raw(state: dict[str, object], key: str) -> str:
    if key not in state:
        raise KeyError(key)
    raw = state[key]
    if raw is None:
        raise KeyError(key)
    text = str(raw).strip()
    if not text or text.lower() == "none":
        raise KeyError(key)
    return text


def get_fallback_timestamp(state: dict[str, object], key: str, fallback: datetime) -> datetime:
    raw = state.get(key)
    if raw is None:
        return fallback
    text = str(raw).strip()
    if not text or text.lower() == "none":
        return fallback
    return parse_timestamp(key, text)


def blocked(
    event_kind: str,
    reason: str,
    error_code: str,
    observed_signals: list[str] | None = None,
) -> Decision:
    return Decision(False, "low", event_kind, reason, error_code, observed_signals or [])


def parse_activity_clock(state: dict[str, object]) -> ActivityClock:
    now = parse_timestamp("now", get_required_raw(state, "now"))
    last_thread_activity = parse_timestamp(
        "last_thread_activity",
        get_required_raw(state, "last_thread_activity"),
    )
    return ActivityClock(
        now=now,
        last_thread_activity=last_thread_activity,
        last_user_action=get_fallback_timestamp(state, "last_user_action", last_thread_activity),
        last_agent_action=get_fallback_timestamp(state, "last_agent_action", last_thread_activity),
    )


def append_signal(signals: list[str], signal: str) -> None:
    if signal not in signals:
        signals.append(signal)


def collect_semantic_signals(state: dict[str, object]) -> list[str]:
    signals: list[str] = []
    if as_bool(state.get("no_clear_next_step"), False):
        append_signal(signals, "no_clear_next_step")
    if as_bool(state.get("progress_stalled"), False):
        append_signal(signals, "progress_stalled")
    if as_bool_or_count_signal(state.get("repeated_local_attempts"), threshold=2):
        append_signal(signals, "repeated_local_attempts")
    if as_bool_or_count_signal(state.get("attempted_fixes_count"), threshold=2):
        append_signal(signals, "repeated_local_attempts")
    if as_bool(state.get("suspected_reinventing_wheel"), False):
        append_signal(signals, "suspected_reinventing_wheel")
    if as_bool(state.get("user_requested_community_help"), False):
        append_signal(signals, "user_requested_community_help")
    if as_bool(state.get("user_requested_deep_community_help"), False):
        append_signal(signals, "user_requested_deep_community_help")

    # Legacy inputs map to the new semantic gate instead of bypassing it.
    if as_int(state.get("related_failures"), 0, minimum=0) >= 2:
        append_signal(signals, "related_failures")
    if as_int(state.get("user_corrections"), 0, minimum=0) >= 2:
        append_signal(signals, "user_corrections")
    if as_int(state.get("unresolved_blocker_count"), 0, minimum=0) >= 1:
        append_signal(signals, "unresolved_blocker_count")
    if as_bool(state.get("version_mismatch_seen"), False):
        append_signal(signals, "version_mismatch_seen")
    if as_bool(state.get("user_explicit_search_request"), False):
        append_signal(signals, "user_requested_community_help")
    if as_bool(state.get("user_explicit_deep_research_request"), False):
        append_signal(signals, "user_requested_deep_community_help")
    return signals


def infer_search_mode(event_kind: str, signals: list[str]) -> tuple[str, list[str]]:
    if "user_requested_deep_community_help" in signals:
        return "high", signals
    if (
        event_kind in {"failure_recovery", *MANUAL_EVENTS}
        or "user_requested_community_help" in signals
        or "progress_stalled" in signals
        or "repeated_local_attempts" in signals
        or "related_failures" in signals
        or "user_corrections" in signals
        or "unresolved_blocker_count" in signals
    ):
        return "medium", signals
    return "low", signals


def check_quiet_gates(
    state: dict[str, object],
    event_kind: str,
    clock: ActivityClock,
) -> Decision | None:
    active_window = get_duration(state, "active_conversation_window")
    quiet_after_user = get_duration(state, "quiet_after_user_action")
    quiet_after_agent = get_duration(state, "quiet_after_agent_action")
    max_runs_per_thread = as_int(
        state.get("max_runs_per_thread_per_day"),
        DEFAULTS["max_runs_per_thread_per_day"],
        minimum=0,
    )
    max_runs_per_user = as_int(
        state.get("max_runs_per_user_per_day"),
        DEFAULTS["max_runs_per_user_per_day"],
        minimum=0,
    )

    if as_bool(state.get("user_operation_in_progress"), False):
        return blocked(event_kind, "user operation in progress", "user_operation_in_progress")
    if as_bool(state.get("agent_response_in_progress"), False):
        return blocked(event_kind, "agent response in progress", "agent_response_in_progress")
    if as_bool(state.get("tool_approval_pending"), False):
        return blocked(event_kind, "tool approval pending", "tool_approval_pending")
    if clock.now - clock.last_thread_activity > active_window:
        return blocked(event_kind, "active conversation window expired", "active_window_expired")
    if clock.now - clock.last_user_action < quiet_after_user:
        return blocked(event_kind, "quiet window after user action has not elapsed", "quiet_after_user_action")
    if clock.now - clock.last_agent_action < quiet_after_agent:
        return blocked(event_kind, "quiet window after agent action has not elapsed", "quiet_after_agent_action")
    if as_int(state.get("thread_runs_today"), 0, minimum=0) >= max_runs_per_thread:
        return blocked(event_kind, "thread run limit reached", "thread_run_limit_reached")
    if as_int(state.get("user_runs_today"), 0, minimum=0) >= max_runs_per_user:
        return blocked(event_kind, "user run limit reached", "user_run_limit_reached")
    return None


def check_idle_fallback_gate(state: dict[str, object], event_kind: str) -> Decision | None:
    if event_kind != "idle_fallback":
        return None
    host_supports_heartbeat = as_bool(state.get("host_supports_heartbeat"), True)
    user_prefers_idle_fallback = as_bool(state.get("user_prefers_idle_fallback"), False)
    idle_fallback_enabled = as_bool(state.get("idle_fallback_enabled"), False)
    if idle_fallback_enabled or not host_supports_heartbeat or user_prefers_idle_fallback:
        return None
    return blocked(
        event_kind,
        "idle fallback needs explicit opt-in or a host without heartbeat support",
        "idle_fallback_not_enabled",
        [
            "host_supports_heartbeat" if host_supports_heartbeat else "host_without_heartbeat",
            "idle_fallback_not_opted_in",
        ],
    )


def check_repeat_fingerprint_gate(
    state: dict[str, object],
    event_kind: str,
    clock: ActivityClock,
    signals: list[str],
) -> tuple[Decision | None, bool]:
    current_fingerprint_hash = str(state.get("current_fingerprint_hash", "")).strip()
    last_travel_fingerprint_hash = str(state.get("last_travel_fingerprint_hash", "")).strip()
    last_travel_generated_at = get_optional_timestamp(state, "last_travel_generated_at")
    repeat_fingerprint_cooldown = get_duration(state, "repeat_fingerprint_cooldown")
    cooldown_active = bool(
        current_fingerprint_hash
        and last_travel_fingerprint_hash
        and current_fingerprint_hash == last_travel_fingerprint_hash
        and last_travel_generated_at is not None
        and clock.now - last_travel_generated_at < repeat_fingerprint_cooldown
    )
    cooldown_bypassed = cooldown_active and cooldown_escalation_allowed(state, signals)
    if cooldown_active and not cooldown_bypassed:
        return (
            blocked(
                event_kind,
                "repeat fingerprint cooldown is still active",
                "duplicate_fingerprint_cooldown",
                ["fingerprint_repeat_window_active"],
            ),
            False,
        )
    return None, cooldown_bypassed


def signal_set_from_state(value: object) -> set[str]:
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    if isinstance(value, str):
        return {item.strip() for item in value.split(",") if item.strip()}
    return set()


def cooldown_escalation_allowed(state: dict[str, object], signals: list[str]) -> bool:
    current_signals = set(signals)
    if not current_signals:
        return False
    if as_bool(state.get("semantic_escalation_since_last_hint"), False):
        return True
    if current_signals & {"user_requested_community_help", "user_requested_deep_community_help"}:
        return True

    last_signals = signal_set_from_state(
        state.get("last_travel_semantic_signals", state.get("last_community_help_semantic_signals"))
    )
    return bool(last_signals and current_signals - last_signals)


def check_semantic_gate(event_kind: str, signals: list[str]) -> Decision | None:
    if SEMANTIC_SIGNAL_NAMES.intersection(signals):
        return None
    return blocked(
        event_kind,
        "community help needs a stuck, stalled, repeated, reinventing-wheel, or explicit help signal",
        "semantic_signal_missing",
        signals,
    )


def scheduled_ownership(state: dict[str, object]) -> tuple[bool, bool]:
    return (
        as_bool(state.get("scheduled_trigger_managed_by_host"), False),
        as_bool(state.get("user_configured_periodic_travel"), False),
    )


def check_scheduled_gate(
    state: dict[str, object],
    event_kind: str,
    signals: list[str],
    scheduled_trigger_managed_by_host: bool,
    user_configured_periodic_travel: bool,
) -> Decision | None:
    if event_kind != "scheduled":
        return None
    if not (scheduled_trigger_managed_by_host or user_configured_periodic_travel):
        return blocked(
            event_kind,
            "scheduled community help needs a host-managed schedule or explicit periodic help opt-in",
            "scheduled_opt_in_required",
            signals,
        )
    scheduled_prompt_origin = normalize_label(state.get("scheduled_prompt_origin"), "manual")
    scheduled_prompt_emotion = normalize_label(state.get("scheduled_prompt_emotion"), "neutral")
    if scheduled_prompt_origin != "manual" and scheduled_prompt_emotion not in {"neutral", "none"}:
        return blocked(
            event_kind,
            "host-generated scheduled prompts must stay neutral",
            "scheduled_prompt_must_be_neutral",
            ["host_generated_scheduled_prompt", f"scheduled_prompt_emotion:{scheduled_prompt_emotion}"],
        )
    return None


def add_scheduled_signals(
    event_kind: str,
    observed_signals: list[str],
    scheduled_trigger_managed_by_host: bool,
    user_configured_periodic_travel: bool,
) -> list[str]:
    if event_kind != "scheduled":
        return observed_signals
    if scheduled_trigger_managed_by_host:
        return ["scheduled_trigger_managed_by_host", *observed_signals]
    if user_configured_periodic_travel:
        return ["user_configured_periodic_travel", *observed_signals]
    return observed_signals


def build_trigger_context(
    state: dict[str, object],
    event_kind: str,
    clock: ActivityClock,
) -> tuple[Decision | None, TriggerContext | None]:
    quiet_block = check_quiet_gates(state, event_kind, clock)
    if quiet_block is not None:
        return quiet_block, None
    idle_block = check_idle_fallback_gate(state, event_kind)
    if idle_block is not None:
        return idle_block, None

    signals = collect_semantic_signals(state)
    repeat_block, cooldown_bypassed = check_repeat_fingerprint_gate(state, event_kind, clock, signals)
    if repeat_block is not None:
        return repeat_block, None
    scheduled_trigger_managed_by_host, user_configured_periodic_travel = scheduled_ownership(state)
    scheduled_block = check_scheduled_gate(
        state,
        event_kind,
        signals,
        scheduled_trigger_managed_by_host,
        user_configured_periodic_travel,
    )
    if scheduled_block is not None:
        return scheduled_block, None
    semantic_block = check_semantic_gate(event_kind, signals)
    if semantic_block is not None:
        return semantic_block, None

    return None, TriggerContext(
        signals,
        cooldown_bypassed,
        scheduled_trigger_managed_by_host,
        user_configured_periodic_travel,
    )


def decide(state: dict[str, object]) -> Decision:
    event_kind = get_event_kind(state)
    if event_kind not in EVENTS:
        return blocked("unsupported", "unsupported event_kind", "unsupported_event_kind")

    if not as_bool(state.get("enabled"), True):
        return blocked(event_kind, "community help is disabled", "disabled")

    if event_kind in MANUAL_EVENTS:
        signals = collect_semantic_signals(state)
        if not signals:
            signals = ["user_requested_community_help"]
        search_mode, observed_signals = infer_search_mode(event_kind, signals)
        return Decision(
            True,
            search_mode,
            event_kind,
            "explicit user request for community help",
            None,
            observed_signals,
        )

    try:
        clock = parse_activity_clock(state)
    except KeyError as exc:
        return blocked(event_kind, f"missing required field: {exc.args[0]}", "missing_required_field")

    gate_block, context = build_trigger_context(state, event_kind, clock)
    if gate_block is not None:
        return gate_block
    if context is None:
        return blocked(event_kind, "internal trigger context missing", "internal_error")

    search_mode, observed_signals = infer_search_mode(event_kind, context.signals)
    observed_signals = add_scheduled_signals(
        event_kind,
        observed_signals,
        context.scheduled_trigger_managed_by_host,
        context.user_configured_periodic_travel,
    )
    if context.cooldown_bypassed:
        observed_signals = ["repeat_fingerprint_escalation_bypass", *observed_signals]
    return Decision(
        True,
        search_mode,
        event_kind,
        "semantic help signal, active conversation, quiet window, within cooldown",
        None,
        observed_signals,
    )


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        emit(Decision(False, "low", "error", f"unable to read state file: {exc}"))
        return 1

    try:
        state = json.loads(raw)
    except json.JSONDecodeError as exc:
        emit(Decision(False, "low", "error", f"invalid JSON: {exc.msg}"))
        return 1

    if not isinstance(state, dict):
        emit(Decision(False, "low", "error", "state must be a JSON object"))
        return 0

    try:
        decision = decide(state)
    except InputError as exc:
        emit(Decision(False, "low", safe_event_kind(state), exc.message, exc.code))
        return 0
    except Exception as exc:  # pragma: no cover - defensive fallback
        emit(
            Decision(
                False,
                "low",
                get_event_kind(state),
                f"unexpected error: {exc}",
                "unexpected_internal_error",
            )
        )
        return 1

    emit(decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
