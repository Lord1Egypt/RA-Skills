"""Small reconciliation helpers for negotiate_safe.

The shared workflow truth lives in sshsign. This module only handles local
idempotency crumbs: what signing event did this process observe, and have we
already delivered the executed artifact from this output directory?
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable


EXECUTED_DELIVERED_MARKER = ".executed_delivered"
TERMINAL_SESSION_STATUSES = frozenset({
    "canceled",
    "rescinded",
    "rescinded_after_sign",
    "completed",
    "expired",
})

FOUNDER_WAIT_COUNTERPARTY = "waiting_for_counterparty"
FOUNDER_STALE_NO_MEMBER = "stale_no_founder_member"
FOUNDER_ALREADY_STREAMING = "already_streaming"
FOUNDER_WAIT_GROUP_ALREADY_PROMPTED = "waiting_for_group_bind_prompted"
FOUNDER_PROMPT_GROUP = "prompt_group_bind"
FOUNDER_START_STREAM = "start_stream"

INVESTOR_ALREADY_STREAMING = "already_streaming"
INVESTOR_STALE_NO_FOUNDER = "stale_no_founder_member"
INVESTOR_WAIT_FOUNDER_STREAM = "waiting_for_founder_stream"
INVESTOR_WAIT_GROUP_BIND = "waiting_for_group_bind"
INVESTOR_START_STREAM = "start_stream"


def normalize_status(status: object) -> str:
    """Normalize sshsign status values for comparisons."""
    return str(status or "").strip().lower()


def is_terminal_status(status: object) -> bool:
    """Return True for statuses where local pointers should be cleaned up."""
    return normalize_status(status) in TERMINAL_SESSION_STATUSES


def member_for_role(session: dict, role: str) -> dict | None:
    """Return the first session member row for a role."""
    for member in session.get("members") or []:
        if (member.get("role") or "").lower() == role:
            return member
    return None


def classify_founder_resume(
    session: dict,
    *,
    group_chat_id: object,
) -> tuple[str, dict | None]:
    """Classify the founder resume lifecycle phase after terminal checks."""
    status = normalize_status(session.get("status"))
    if status != "joined":
        return FOUNDER_WAIT_COUNTERPARTY, None

    founder_row = member_for_role(session, "founder")
    if founder_row is None:
        return FOUNDER_STALE_NO_MEMBER, None

    if founder_row.get("founder_streaming_at"):
        return FOUNDER_ALREADY_STREAMING, founder_row
    if not group_chat_id:
        if founder_row.get("founder_resumed_at"):
            return FOUNDER_WAIT_GROUP_ALREADY_PROMPTED, founder_row
        return FOUNDER_PROMPT_GROUP, founder_row
    return FOUNDER_START_STREAM, founder_row


def classify_investor_resume(
    state: dict,
    session: dict,
    *,
    group_chat_id: object,
) -> tuple[str, dict | None]:
    """Classify the investor resume lifecycle phase after terminal checks."""
    if state.get("investor_streaming_started"):
        return INVESTOR_ALREADY_STREAMING, None

    founder_row = member_for_role(session, "founder")
    if founder_row is None:
        return INVESTOR_STALE_NO_FOUNDER, None
    if not founder_row.get("founder_streaming_at"):
        return INVESTOR_WAIT_FOUNDER_STREAM, founder_row
    if not group_chat_id:
        return INVESTOR_WAIT_GROUP_BIND, founder_row
    return INVESTOR_START_STREAM, founder_row


def latest_signing_pending_id(output_dir: str | Path) -> str:
    """Return the latest signing pending_id recorded in events.ndjson."""
    events_path = Path(output_dir) / "events.ndjson"
    try:
        lines = events_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""

    pending_id = ""
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("type") == "signing":
            pending_id = str(event.get("pending_id") or "").strip()
    return pending_id


def _executed_delivered_marker(output_dir: str | Path, negotiation_id: str = "") -> Path:
    if negotiation_id:
        safe = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in negotiation_id)
        return Path(output_dir) / f".executed_delivered_{safe}"
    return Path(output_dir) / EXECUTED_DELIVERED_MARKER


def has_executed_delivered(output_dir: str | Path, negotiation_id: str = "") -> bool:
    """Return True once this output dir has delivered its executed PDF."""
    return _executed_delivered_marker(output_dir, negotiation_id).exists()


def mark_executed_delivered(output_dir: str | Path, negotiation_id: str = "") -> None:
    """Best-effort marker to keep reconciliation from double-posting PDFs."""
    try:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        _executed_delivered_marker(out, negotiation_id).write_text("1\n", encoding="utf-8")
    except OSError:
        pass


def reconcile_session(
    state: dict,
    *,
    founder_runner: Callable,
    investor_runner: Callable,
    session_client=None,
    sender=None,
    now_fn=None,
) -> int:
    """Dispatch one local state pointer to the right role reconciler.

    This is intentionally a facade over the existing resume functions for
    now. It gives the CLI/scan layer one reconciliation entry point without
    forcing a risky state-machine rewrite in the same step.
    """
    role = (state.get("role") or "founder").lower()
    runner = investor_runner if role == "investor" else founder_runner
    return runner(
        state,
        session_client=session_client,
        sender=sender,
        now_fn=now_fn,
    )


def reconcile_state_by_negotiation_id(
    negotiation_id: str,
    *,
    read_state: Callable,
    founder_runner: Callable,
    investor_runner: Callable,
    session_client=None,
    sender=None,
    now_fn=None,
) -> int:
    """Reconcile one known local pointer if it exists.

    Entry points such as `/bind` and investor join already know the
    negotiation that may be ready. This helper lets them try the same
    idempotent transition immediately, leaving cron as a retry path.
    """
    state = read_state(negotiation_id)
    if state is None:
        return 1
    return reconcile_session(
        state,
        founder_runner=founder_runner,
        investor_runner=investor_runner,
        session_client=session_client,
        sender=sender,
        now_fn=now_fn,
    )


def reconcile_active_sessions(
    *,
    list_active: Callable,
    founder_runner: Callable,
    investor_runner: Callable,
    session_client=None,
    sender=None,
    now_fn=None,
    stderr=None,
) -> int:
    """Reconcile every local active pointer, containing per-session failures.

    Returns 0 always. A failed pointer should never stop the cron tick from
    checking the rest, and the next tick can retry transient failures.
    """
    err = stderr or sys.stderr
    try:
        pointers = list_active()
    except Exception as e:  # noqa: BLE001
        err.write(f"scan: list_active failed: {e}\n")
        return 0

    for state in pointers:
        try:
            reconcile_session(
                state,
                founder_runner=founder_runner,
                investor_runner=investor_runner,
                session_client=session_client,
                sender=sender,
                now_fn=now_fn,
            )
        except Exception as e:  # noqa: BLE001
            err.write(
                f"scan: resume failed for {state.get('negotiation_id')}: {e}\n"
            )
    return 0
