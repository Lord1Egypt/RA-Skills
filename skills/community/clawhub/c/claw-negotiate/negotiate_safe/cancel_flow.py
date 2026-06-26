"""Pure decision helpers for cancel/rescind session lifecycle."""
from __future__ import annotations

from dataclasses import dataclass

from reconcile import normalize_status


CANCEL_COMPLETED_REFUSED_EVENT = "cancel_completed_refused"
CANCELED_BEFORE_DEAL_EVENT = "canceled_before_deal_initiator"
RESCINDED_AFTER_SIGN_EVENT = "rescinded_after_sign_initiator"

CANCEL_NOOP_STATUSES = frozenset({
    "canceled",
    "expired",
    "rescinded",
    "rescinded_after_sign",
})


@dataclass(frozen=True)
class CancelPreflight:
    """Decision to make before calling sshsign cancel-session."""

    action: str
    return_code: int | None = None
    event_type: str = ""
    status: str = ""

    @property
    def should_continue(self) -> bool:
        return self.action == "continue"


def cancel_preflight(status: object) -> CancelPreflight:
    """Classify a session status before attempting cancellation."""
    normalized = normalize_status(status)
    if normalized == "completed":
        return CancelPreflight(
            action="refuse",
            return_code=1,
            event_type=CANCEL_COMPLETED_REFUSED_EVENT,
            status=normalized,
        )
    if normalized in CANCEL_NOOP_STATUSES:
        return CancelPreflight(
            action="noop",
            return_code=0,
            status=normalized,
        )
    return CancelPreflight(action="continue", status=normalized)


def cancel_success_event_type(*, rescind: bool) -> str:
    """Return the chat event to emit after a successful cancel-session call."""
    if rescind:
        return RESCINDED_AFTER_SIGN_EVENT
    return CANCELED_BEFORE_DEAL_EVENT
