"""Telegram routing rules for negotiate_safe.

Rendering lives in format_event.py. Transport lives in telegram_push.py.
This module owns the policy boundary between events and destinations:

* group vs DM
* signing URL privacy
* two-party role attribution
"""
from __future__ import annotations

import sys
from typing import Callable

from telegram_push import SigningUrlTargetError


SIGNING_GROUP_PLACEHOLDER = (
    "✍️ <b>Signing started</b>\n\n"
    "Each party will receive a private signing link in DM."
)


def stream_target(chat_id: str, group_chat_id: str | None) -> str:
    """Return where ordinary stream cards should appear."""
    return group_chat_id or chat_id


def should_publish_stream_event(
    event: dict,
    constraints: dict | None,
    group_chat_id: str | None,
) -> bool:
    """Return whether this local bot should publish this event.

    In two-party group mode, each bot observes the full sshsign history
    but should only post offer/counter/accept cards for its own role.
    Otherwise the investor bot can publish a founder message, which makes
    Telegram attribution look reversed.
    """
    etype = event.get("type")
    if (
        group_chat_id
        and etype in ("offer", "counter", "accept")
        and (constraints or {}).get("mode") == "two_party"
    ):
        local_role = ((constraints or {}).get("role") or "").lower()
        event_party = (event.get("party") or "").lower()
        if local_role and event_party and event_party != local_role:
            return False
    return True


def route_stream_message(
    *,
    event: dict,
    message: str,
    chat_id: str,
    group_chat_id: str | None,
    constraints: dict | None,
    sender: Callable,
    dm_sender: Callable,
    stderr=None,
) -> None:
    """Send one already-rendered stream message to the right Telegram target."""
    if not message:
        return
    if not should_publish_stream_event(event, constraints, group_chat_id):
        return

    etype = event.get("type")
    target = stream_target(chat_id, group_chat_id)
    if etype == "signing":
        try:
            dm_sender(chat_id, message=message)
        except SigningUrlTargetError:
            err = stderr or sys.stderr
            err.write(
                f"stream: refusing to send signing URL to "
                f"non-DM target chat_id={chat_id!r}\n"
            )
        if group_chat_id and not event.get("_suppress_group_placeholder"):
            sender(target, message=SIGNING_GROUP_PLACEHOLDER)
        return

    sender(target, message=message)
