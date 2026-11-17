"""Shared deadline-budget policy for every official HaloArena client.

The server owns the turn deadline. Clients own only a local inference cap and
the transport reserve needed to submit before that deadline.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Callable, Mapping


DEFAULT_DECISION_CAP_SECONDS = 105.0
DIPLOMACY_DECISION_CAP_SECONDS = 165.0
DEFAULT_SUBMIT_RESERVE_SECONDS = 8.0
HERMES_SUBMIT_RESERVE_SECONDS = 12.0


def _deadline_value(envelope: Mapping[str, Any]) -> object:
    raw = envelope.get("turn_deadline")
    state = envelope.get("state")
    if not raw and isinstance(state, Mapping):
        raw = state.get("turn_deadline")
    return raw


def decision_cap_seconds(envelope: Mapping[str, Any]) -> float:
    """Return the official wall-clock cap for this game's model call."""

    game_type = envelope.get("game_type")
    state = envelope.get("state")
    if not game_type and isinstance(state, Mapping):
        game_type = state.get("game_type")
    if str(game_type or "").strip().lower() == "diplomacy":
        return DIPLOMACY_DECISION_CAP_SECONDS
    return DEFAULT_DECISION_CAP_SECONDS


def decision_budget(
    envelope: Mapping[str, Any],
    *,
    configured_seconds: float | None = None,
    submit_reserve_seconds: float = DEFAULT_SUBMIT_RESERVE_SECONDS,
    clock: Callable[[], float] = time.time,
) -> dict[str, float | str]:
    """Return one deadline-derived inference budget and public provenance."""

    configured = max(
        0.0,
        float(
            decision_cap_seconds(envelope)
            if configured_seconds is None
            else configured_seconds
        ),
    )
    reserve = max(0.0, float(submit_reserve_seconds))
    raw = _deadline_value(envelope)
    if not raw:
        return {
            "configured_seconds": configured,
            "effective_seconds": configured,
            "server_remaining_seconds": configured + reserve,
            "submit_reserve_seconds": reserve,
            "policy": "configured_cap_no_deadline",
        }
    try:
        deadline = datetime.fromisoformat(str(raw).replace("Z", "+00:00")).timestamp()
    except (TypeError, ValueError):
        return {
            "configured_seconds": configured,
            "effective_seconds": configured,
            "server_remaining_seconds": configured + reserve,
            "submit_reserve_seconds": reserve,
            "policy": "configured_cap_invalid_deadline",
        }

    remaining = max(0.0, deadline - clock())
    effective = max(0.0, min(configured, remaining - reserve))
    return {
        "configured_seconds": configured,
        "effective_seconds": effective,
        "server_remaining_seconds": remaining,
        "submit_reserve_seconds": reserve,
        "policy": "deadline_submit_reserve",
    }
