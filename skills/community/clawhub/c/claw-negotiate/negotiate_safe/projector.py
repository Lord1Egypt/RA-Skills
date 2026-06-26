"""Idempotent Telegram projector for shared-orchestrator events."""
from __future__ import annotations

import os
from typing import Callable

import delivery_store
from format_event import format_event
from telegram import route_stream_message, should_publish_stream_event
from telegram_push import edit_telegram_message, send_signing_url_to_dm, send_telegram
from upstream import augment_signing_url, synthesize_offer_event


def heartbeat_delivery_key(role: str, round_num: int) -> str:
    return f"turn_heartbeat:{(role or '').lower()}:{int(round_num)}"


def delivery_key(event: dict) -> str:
    etype = event.get("type") or "event"
    if etype in ("offer", "counter", "accept"):
        return "offer:{party}:{round}:{etype}".format(
            party=event.get("party") or "",
            round=event.get("round"),
            etype=etype,
        )
    if etype == "signing":
        return f"signing:{event.get('pending_id') or ''}"
    if etype == "signing_group_started":
        return "signing_group_started"
    return f"{etype}:{event.get('id') or event.get('round') or ''}"


def _delivery_target(*, event: dict, dm_chat_id: str, group_chat_id: str | None) -> str:
    if event.get("type") == "signing" and group_chat_id:
        return f"dm:{dm_chat_id};group:{group_chat_id}"
    if event.get("type") == "signing_group_started" and group_chat_id:
        return str(group_chat_id)
    return str(group_chat_id or dm_chat_id)


def _claim_delivery(
    *,
    delivery_client,
    session_id: str,
    key: str,
    target: str,
) -> bool:
    if delivery_client is None:
        if delivery_store.has_delivery(session_id, key):
            return False
        return True

    payload = delivery_client.claim_delivery(session_id, key, target=target)
    return bool(payload.get("created"))


def _delivery_message_id(*, delivery_client, session_id: str, key: str) -> str:
    if delivery_client is None:
        payload = delivery_store.read_deliveries(session_id).get("delivered", {}).get(key)
    else:
        try:
            payload = delivery_client.get_delivery(session_id, key)
        except Exception:
            payload = None
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("message_id") or payload.get("messageId") or "").strip()


def _maybe_edit_heartbeat(
    *,
    session_id: str,
    event: dict,
    message: str,
    target: str,
    delivery_client,
    editor: Callable,
) -> bool:
    if event.get("type") not in ("offer", "counter", "accept"):
        return False
    party = (event.get("party") or "").lower()
    if not party:
        return False
    try:
        round_num = int(event.get("round", 0))
    except (TypeError, ValueError):
        return False
    key = heartbeat_delivery_key(party, round_num)
    message_id = _delivery_message_id(
        delivery_client=delivery_client,
        session_id=session_id,
        key=key,
    )
    if not message_id:
        return False
    result = editor(target, message_id=message_id, message=message)
    return bool(getattr(result, "ok", False))


def project_event(
    *,
    session_id: str,
    event: dict,
    constraints: dict | None,
    dm_chat_id: str,
    group_chat_id: str | None,
    sender: Callable = send_telegram,
    dm_sender: Callable = send_signing_url_to_dm,
    editor: Callable = edit_telegram_message,
    delivery_client=None,
) -> bool:
    if event.get("type") == "signing":
        event = augment_signing_url(
            event,
            os.environ.get("TELEGRAM_BOT_USERNAME", ""),
        )

    role = (constraints or {}).get("role") or ""
    if event.get("type") in ("offer", "counter", "accept"):
        party = event.get("party") or ""
        if role in ("founder", "investor") and party and party != role:
            return False

    key = delivery_key(event)
    if not should_publish_stream_event(event, constraints, group_chat_id):
        return False

    message = format_event(event, constraints=constraints)
    if not message:
        return False
    target = _delivery_target(
        event=event,
        dm_chat_id=str(dm_chat_id),
        group_chat_id=str(group_chat_id) if group_chat_id else None,
    )
    if not _claim_delivery(
        delivery_client=delivery_client,
        session_id=session_id,
        key=key,
        target=target,
    ):
        return False
    edited = False
    if group_chat_id:
        edited = _maybe_edit_heartbeat(
            session_id=session_id,
            event=event,
            message=message,
            target=target,
            delivery_client=delivery_client,
            editor=editor,
        )
    if not edited:
        route_stream_message(
            event=event,
            message=message,
            chat_id=str(dm_chat_id),
            group_chat_id=str(group_chat_id) if group_chat_id else None,
            constraints=constraints,
            sender=sender,
            dm_sender=dm_sender,
        )
    if delivery_client is None:
        delivery_store.mark_delivery(session_id, key, target)
    return True


def project_history(
    *,
    session_id: str,
    history_rows: list[dict],
    constraints: dict | None,
    dm_chat_id: str,
    group_chat_id: str | None,
    sender: Callable = send_telegram,
    dm_sender: Callable = send_signing_url_to_dm,
    editor: Callable = edit_telegram_message,
    delivery_client=None,
) -> int:
    count = 0
    for row in history_rows:
        event = synthesize_offer_event(row)
        if not event:
            continue
        if project_event(
            session_id=session_id,
            event=event,
            constraints=constraints,
            dm_chat_id=dm_chat_id,
            group_chat_id=group_chat_id,
            sender=sender,
            dm_sender=dm_sender,
            editor=editor,
            delivery_client=delivery_client,
        ):
            count += 1
    return count
