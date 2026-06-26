"""Unified status check: local upgrade + identity verification + inbox/group summary.

Usage:
    python scripts/check_status.py                     # Status check with E2EE auto-processing + auto-decrypt
    python scripts/check_status.py --credential alice   # Specify credential
    python scripts/check_status.py --upgrade-only       # Run local upgrade and exit

[INPUT]: SDK (RPC calls, E2eeClient), credential_store (authenticator factory),
         SQLite-backed E2EE session store, credential_migration,
         database_migration, local_store, listener recovery helpers,
         logging_config
[OUTPUT]: Structured JSON status report (local upgrade + identity + inbox +
          group_watch + e2ee_sessions + realtime listener runtime), with
          automatic E2EE protocol handling, plaintext delivery for unread
          encrypted messages, listener auto-restart backoff, and incremental
          group message fetching with classification (text / member events),
          plus listener-coordinated database upgrade support for explicit
          ``--upgrade-only`` runs
[POS]: Unified status check entry point for Agent session startup and heartbeat calls
       with mandatory, server_seq-aware E2EE auto-processing, plaintext
       delivery for unread encrypted messages, local discovery-group watch
       summaries, and incremental group message fetching with per-group
       new_messages classification

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

from utils import (
    SDKConfig,
    E2eeClient,
    rpc_call,
    create_user_service_client,
    create_molt_message_client,
    authenticated_rpc_call,
)
from utils.e2ee import (
    SUPPORTED_E2EE_VERSION,
    build_e2ee_error_content,
    build_e2ee_error_message,
)
from utils.logging_config import configure_logging
import local_store
from credential_migration import ensure_credential_storage_ready
from database_migration import (
    ensure_local_database_ready,
    ensure_local_database_ready_for_upgrade,
)
from credential_store import load_identity, create_authenticator
from e2ee_session_store import load_e2ee_client, save_e2ee_client
from e2ee_outbox import record_remote_failure
from listener_recovery import ensure_listener_runtime, get_listener_runtime_report
from message_transport import is_websocket_mode


MESSAGE_RPC = "/message/rpc"
AUTH_RPC = "/user-service/did-auth/rpc"
GROUP_RPC_ENDPOINT = "/group/rpc"
PROFILE_RPC = "/user-service/did/profile/rpc"
_GROUP_MSG_FETCH_LIMIT = 50
logger = logging.getLogger(__name__)

# E2EE protocol message types
_E2EE_SESSION_SETUP_TYPES = {"e2ee_init", "e2ee_rekey"}
_E2EE_MSG_TYPES = {"e2ee_init", "e2ee_ack", "e2ee_msg", "e2ee_rekey", "e2ee_error"}
_E2EE_TYPE_ORDER = {
    "e2ee_init": 0,
    "e2ee_ack": 1,
    "e2ee_rekey": 2,
    "e2ee_msg": 3,
    "e2ee_error": 4,
}
_E2EE_USER_NOTICE = "This is an encrypted message."
_INBOX_FETCH_LIMIT = 50
_INBOX_MESSAGE_LIMIT = 10


def _message_time_value(message: dict[str, Any]) -> str:
    """Return a sortable timestamp string for one message."""
    timestamp = message.get("sent_at") or message.get("created_at")
    return timestamp if isinstance(timestamp, str) else ""


def ensure_local_upgrade_ready(
    credential_name: str = "default",
    *,
    coordinate_listener_during_database_upgrade: bool = False,
) -> dict[str, Any]:
    """Run local credential/database upgrades needed by the current skill version."""
    credential_layout = ensure_credential_storage_ready(credential_name)
    if coordinate_listener_during_database_upgrade:
        local_database = ensure_local_database_ready_for_upgrade()
    else:
        local_database = ensure_local_database_ready()
    ready = (
        credential_layout.get("credential_ready", False)
        and local_database.get("status") != "error"
    )

    performed: list[str] = []
    migration = credential_layout.get("migration")
    if isinstance(migration, dict) and migration.get("status") not in {
        None,
        "not_needed",
    }:
        performed.append("credential_layout")
    if local_database.get("status") == "migrated":
        performed.append("local_database")

    return {
        "status": "ready" if ready else "error",
        "credential_ready": credential_layout.get("credential_ready", False),
        "database_ready": local_database.get("status") != "error",
        "performed": performed,
        "credential_layout": credential_layout,
        "local_database": local_database,
    }


def _message_sort_key(message: dict[str, Any]) -> tuple[Any, ...]:
    """Build a stable E2EE inbox ordering key with server_seq priority inside a sender stream."""
    sender_did_raw = message.get("sender_did")
    sender_did = sender_did_raw if isinstance(sender_did_raw, str) else ""
    server_seq = message.get("server_seq")
    has_server_seq = 0 if isinstance(server_seq, int) else 1
    server_seq_value = server_seq if isinstance(server_seq, int) else 0
    return (
        sender_did,
        has_server_seq,
        server_seq_value,
        _message_time_value(message),
        _E2EE_TYPE_ORDER.get(message.get("type"), 99),
    )


def _is_user_visible_message_type(msg_type: str) -> bool:
    """Return whether a message type should be exposed to end users."""
    return msg_type not in _E2EE_MSG_TYPES


def _decorate_user_visible_e2ee_message(
    message: dict[str, Any],
    *,
    original_type: str,
    plaintext: str,
) -> dict[str, Any]:
    """Decorate a decrypted E2EE message for status output."""
    rendered = dict(message)
    rendered["type"] = original_type
    rendered["content"] = plaintext
    rendered["is_e2ee"] = True
    rendered["e2ee_notice"] = _E2EE_USER_NOTICE
    rendered.pop("title", None)
    return rendered


def _strip_hidden_user_fields(message: dict[str, Any]) -> dict[str, Any]:
    """Remove fields intentionally hidden from user-facing output."""
    rendered = dict(message)
    rendered.pop("title", None)
    return rendered


def _classify_decrypt_error(exc: BaseException) -> tuple[str, str]:
    """Map decrypt failures to stable sender-visible error metadata."""
    msg = str(exc).lower()
    if "unsupported_version" in msg:
        return "unsupported_version", "drop"
    if "session" in msg and ("not found" in msg or "find session" in msg):
        return "session_not_found", "rekey_then_resend"
    if "expired" in msg:
        return "session_expired", "rekey_then_resend"
    if "seq" in msg or "sequence" in msg:
        return "invalid_seq", "rekey_then_resend"
    return "decryption_failed", "resend"


def _build_visible_inbox_report(
    visible_messages: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the status-friendly inbox report from user-visible messages."""
    ordered_messages = sorted(
        visible_messages,
        key=lambda message: (
            _message_time_value(message),
            message.get("server_seq")
            if isinstance(message.get("server_seq"), int)
            else -1,
        ),
        reverse=True,
    )

    by_type: dict[str, int] = {}
    text_by_sender: dict[str, dict[str, Any]] = {}
    text_count = 0

    for message in ordered_messages:
        msg_type = str(message.get("type") or "unknown")
        by_type[msg_type] = by_type.get(msg_type, 0) + 1

        if msg_type != "text":
            continue
        text_count += 1
        sender_did = str(message.get("sender_did") or "unknown")
        message_time = _message_time_value(message)
        if sender_did not in text_by_sender:
            text_by_sender[sender_did] = {"count": 0, "latest": ""}
        text_by_sender[sender_did]["count"] += 1
        if message_time > text_by_sender[sender_did]["latest"]:
            text_by_sender[sender_did]["latest"] = message_time

    return {
        "status": "ok",
        "total": len(ordered_messages),
        "by_type": by_type,
        "text_messages": text_count,
        "text_by_sender": text_by_sender,
        "messages": ordered_messages[:_INBOX_MESSAGE_LIMIT],
    }


def _message_id_value(message: dict[str, Any]) -> str | None:
    """Return one stable message identifier when available."""
    for key in ("id", "msg_id"):
        value = message.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _message_dedup_key(message: dict[str, Any]) -> tuple[Any, ...]:
    """Build a stable deduplication key for merged local/remote inbox results."""
    message_id = _message_id_value(message)
    if message_id:
        return ("id", message_id)
    return (
        "fallback",
        message.get("sender_did"),
        message.get("receiver_did"),
        message.get("group_id"),
        message.get("type"),
        message.get("content"),
        _message_time_value(message),
    )


def _message_display_sort_key(message: dict[str, Any]) -> tuple[Any, ...]:
    """Build a descending-friendly display key for merged visible inbox messages."""
    server_seq = message.get("server_seq")
    has_server_seq = 1 if isinstance(server_seq, int) else 0
    server_seq_value = server_seq if isinstance(server_seq, int) else -1
    return (
        has_server_seq,
        server_seq_value,
        _message_time_value(message),
        str(message.get("id") or message.get("msg_id") or ""),
    )


def _merge_visible_inbox_messages(
    local_messages: list[dict[str, Any]],
    remote_messages: list[dict[str, Any]],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    """Merge visible local-cache and HTTP inbox messages with deduplication."""
    merged_by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
    for message in remote_messages:
        merged_by_key[_message_dedup_key(message)] = dict(message)
    for message in local_messages:
        merged_by_key[_message_dedup_key(message)] = dict(message)
    merged = list(merged_by_key.values())
    merged.sort(key=_message_display_sort_key, reverse=True)
    return merged[:limit]


def _load_local_visible_inbox_messages(owner_did: str | None) -> list[dict[str, Any]]:
    """Load visible unread inbox messages from local SQLite cache."""
    if not owner_did:
        return []
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        rows = conn.execute(
            """
            SELECT
                m.msg_id AS id,
                m.sender_did,
                m.sender_name,
                m.receiver_did,
                m.group_id,
                m.group_did,
                g.name AS group_name,
                m.content_type AS type,
                m.content,
                m.server_seq,
                m.sent_at,
                m.stored_at AS created_at,
                m.is_e2ee
            FROM messages m
            LEFT JOIN groups g
              ON g.owner_did = m.owner_did
             AND g.group_id = m.group_id
            WHERE m.owner_did = ?
              AND m.direction = 0
              AND m.is_read = 0
            ORDER BY COALESCE(m.server_seq, -1) DESC,
                     COALESCE(m.sent_at, m.stored_at) DESC,
                     m.stored_at DESC
            LIMIT ?
            """,
            (owner_did, _INBOX_FETCH_LIMIT),
        ).fetchall()
    finally:
        conn.close()

    visible_messages: list[dict[str, Any]] = []
    for row in rows:
        message = dict(row)
        msg_type = str(message.get("type") or "")
        if not _is_user_visible_message_type(msg_type):
            continue
        if int(message.get("is_e2ee") or 0):
            message["is_e2ee"] = True
            message["e2ee_notice"] = _E2EE_USER_NOTICE
        visible_messages.append(message)
    return visible_messages


def _build_local_inbox_report(owner_did: str | None) -> dict[str, Any]:
    """Build one inbox report from local SQLite cache only."""
    if not owner_did:
        return {
            "status": "no_identity",
            "total": 0,
            "by_type": {},
            "text_messages": 0,
            "text_by_sender": {},
            "messages": [],
        }
    try:
        visible_messages = _load_local_visible_inbox_messages(owner_did)
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "error": str(exc),
            "total": 0,
            "by_type": {},
            "text_messages": 0,
            "text_by_sender": {},
            "messages": [],
        }
    report = _build_visible_inbox_report(visible_messages)
    report["source"] = "local_ws_cache"
    return report


async def _sync_remote_visible_inbox_messages(
    *,
    credential_name: str,
    auth: Any,
    owner_did: str,
    config: SDKConfig,
) -> dict[str, Any]:
    """Best-effort HTTP inbox sync used while websocket local cache is active."""
    result: dict[str, Any] = {
        "attempted": True,
        "status": "ok",
        "messages": [],
        "total": 0,
    }
    try:
        async with create_molt_message_client(config) as client:
            inbox = await authenticated_rpc_call(
                client,
                MESSAGE_RPC,
                "get_inbox",
                params={"user_did": owner_did, "limit": _INBOX_FETCH_LIMIT},
                auth=auth,
                credential_name=credential_name,
            )
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "HTTP inbox sync failed during status check credential=%s error=%s",
            credential_name,
            exc,
        )
        result["status"] = "error"
        result["error"] = str(exc)
        return result

    visible_messages = [
        _strip_hidden_user_fields(message)
        for message in inbox.get("messages", [])
        if _is_user_visible_message_type(str(message.get("type") or ""))
    ]
    result["messages"] = visible_messages
    result["total"] = len(visible_messages)
    return result


def summarize_group_watch(owner_did: str | None) -> dict[str, Any]:
    """Summarize locally tracked groups for heartbeat decisions."""
    if not owner_did:
        return {"status": "no_identity", "active_groups": 0, "groups": []}

    try:
        conn = local_store.get_connection()
        try:
            local_store.ensure_schema(conn)
            group_rows = conn.execute(
                """
                SELECT
                    group_id,
                    name,
                    group_mode,
                    slug,
                    my_role,
                    member_count,
                    group_owner_did,
                    group_owner_handle,
                    last_synced_seq,
                    last_read_seq,
                    last_message_at,
                    stored_at
                FROM groups
                WHERE owner_did = ? AND membership_status = 'active'
                ORDER BY COALESCE(last_message_at, stored_at) DESC, stored_at DESC
                LIMIT 20
                """,
                (owner_did,),
            ).fetchall()

            groups: list[dict[str, Any]] = []
            groups_with_pending_recommendations = 0
            for row in group_rows:
                group_id = row["group_id"]
                tracked_members_row = conn.execute(
                    """
                    SELECT
                        COUNT(*) AS cnt,
                        MAX(joined_at) AS latest_joined_at
                    FROM group_members
                    WHERE owner_did = ? AND group_id = ? AND status = 'active'
                    """,
                    (owner_did, group_id),
                ).fetchone()
                owner_message_row = conn.execute(
                    """
                    SELECT
                        COUNT(*) AS cnt,
                        MAX(sent_at) AS latest_sent_at
                    FROM messages
                    WHERE owner_did = ?
                      AND group_id = ?
                      AND content_type = 'group_user'
                      AND sender_did = COALESCE(?, '')
                    """,
                    (owner_did, group_id, row["group_owner_did"]),
                ).fetchone()
                local_user_message_row = conn.execute(
                    """
                    SELECT COUNT(*) AS cnt
                    FROM messages
                    WHERE owner_did = ? AND group_id = ? AND content_type = 'group_user'
                    """,
                    (owner_did, group_id),
                ).fetchone()
                recommendation_row = conn.execute(
                    """
                    SELECT
                        SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_count,
                        MAX(created_at) AS last_recommended_at
                    FROM relationship_events
                    WHERE owner_did = ?
                      AND source_group_id = ?
                      AND event_type = 'ai_recommended'
                    """,
                    (owner_did, group_id),
                ).fetchone()
                saved_contact_row = conn.execute(
                    """
                    SELECT COUNT(*) AS cnt
                    FROM contacts
                    WHERE owner_did = ? AND source_group_id = ?
                    """,
                    (owner_did, group_id),
                ).fetchone()

                pending_recommendations = int(
                    recommendation_row["pending_count"] or 0
                )
                if pending_recommendations > 0:
                    groups_with_pending_recommendations += 1

                local_group_user_messages = int(local_user_message_row["cnt"] or 0)
                tracked_active_members = int(tracked_members_row["cnt"] or 0)
                groups.append(
                    {
                        "group_id": group_id,
                        "name": row["name"],
                        "group_mode": row["group_mode"],
                        "slug": row["slug"],
                        "my_role": row["my_role"],
                        "member_count": row["member_count"],
                        "tracked_active_members": tracked_active_members,
                        "group_owner_did": row["group_owner_did"],
                        "group_owner_handle": row["group_owner_handle"],
                        "local_group_user_messages": local_group_user_messages,
                        "local_owner_messages": int(owner_message_row["cnt"] or 0),
                        "latest_owner_message_at": owner_message_row["latest_sent_at"],
                        "latest_member_joined_at": tracked_members_row["latest_joined_at"],
                        "pending_recommendations": pending_recommendations,
                        "last_recommended_at": recommendation_row["last_recommended_at"],
                        "saved_contacts": int(saved_contact_row["cnt"] or 0),
                        "recommendation_signal_ready": (
                            tracked_active_members >= 1
                            or local_group_user_messages >= 1
                        ),
                        "last_synced_seq": row["last_synced_seq"],
                        "last_read_seq": row["last_read_seq"],
                        "last_message_at": row["last_message_at"],
                        "stored_at": row["stored_at"],
                    }
                )

            return {
                "status": "ok",
                "active_groups": len(groups),
                "groups_with_pending_recommendations": (
                    groups_with_pending_recommendations
                ),
                "groups": groups,
            }
        finally:
            conn.close()
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "active_groups": 0,
            "groups": [],
            "error": str(exc),
        }


# ---------- Group message helpers ----------


def _classify_group_messages(
    messages: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Classify group messages into text / member_joined / member_left / member_kicked buckets."""
    buckets: dict[str, list[dict[str, Any]]] = {
        "text": [],
        "member_joined": [],
        "member_left": [],
        "member_kicked": [],
    }
    for msg in messages:
        content_type = msg.get("type") or msg.get("content_type") or ""
        system_event = msg.get("system_event")
        if isinstance(system_event, dict):
            kind = system_event.get("kind", "")
            if kind in buckets:
                buckets[kind].append(msg)
                continue
        if content_type in ("group_user", "text"):
            buckets["text"].append(msg)
    return buckets


def _persist_and_classify_group_messages(
    *,
    owner_did: str,
    group_id: str,
    payload: dict[str, Any],
    credential_name: str,
) -> dict[str, Any]:
    """Persist fetched group messages and return classified buckets.

    Reuses the persistence logic from manage_group._persist_group_messages():
    store_messages_batch + sync_group_member_from_system_event + upsert_group.
    """
    messages = payload.get("messages", [])
    if not messages:
        return {
            "total": 0,
            "text": [],
            "member_joined": [],
            "member_left": [],
            "member_kicked": [],
        }

    batch: list[dict[str, Any]] = []
    max_server_seq: int | None = None
    last_message_at: str | None = None
    for msg in messages:
        sender_did = str(msg.get("sender_did") or "")
        direction = 1 if sender_did and sender_did == owner_did else 0
        sent_at = msg.get("sent_at") or msg.get("created_at")
        server_seq = msg.get("server_seq")
        if isinstance(server_seq, int):
            max_server_seq = (
                server_seq if max_server_seq is None else max(max_server_seq, server_seq)
            )
        if sent_at:
            last_message_at = str(sent_at)
        batch.append(
            {
                "msg_id": msg.get("id", ""),
                "thread_id": local_store.make_thread_id(owner_did, group_id=group_id),
                "direction": direction,
                "sender_did": sender_did,
                "receiver_did": None,
                "group_id": group_id,
                "group_did": msg.get("group_did"),
                "content_type": msg.get("type", "group_user"),
                "content": str(msg.get("content", "")),
                "title": msg.get("title"),
                "server_seq": server_seq,
                "sent_at": sent_at,
                "sender_name": msg.get("sender_name"),
                "metadata": (
                    json.dumps(
                        {"system_event": msg.get("system_event")},
                        ensure_ascii=False,
                    )
                    if msg.get("system_event") is not None
                    else None
                ),
                "credential_name": credential_name,
                "owner_did": owner_did,
            }
        )

    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.store_messages_batch(
            conn, batch, owner_did=owner_did, credential_name=credential_name
        )
        for msg in messages:
            system_event = msg.get("system_event")
            if not isinstance(system_event, dict):
                continue
            local_store.sync_group_member_from_system_event(
                conn,
                owner_did=owner_did,
                group_id=group_id,
                system_event=system_event,
                credential_name=credential_name,
            )
        local_store.upsert_group(
            conn,
            owner_did=owner_did,
            group_id=group_id,
            membership_status="active",
            last_synced_seq=payload.get("next_since_seq") or max_server_seq,
            last_message_at=last_message_at,
            credential_name=credential_name,
        )
    finally:
        conn.close()

    classified = _classify_group_messages(messages)
    classified["total"] = len(messages)
    return classified


async def _fetch_one_group_messages(
    client,
    *,
    group_id: str,
    since_seq: int | None,
    owner_did: str,
    credential_name: str,
    auth,
) -> dict[str, Any]:
    """Fetch incremental messages for one group and return classified results.

    Returns empty result on error rather than raising.
    """
    empty: dict[str, Any] = {
        "total": 0,
        "text": [],
        "member_joined": [],
        "member_left": [],
        "member_kicked": [],
    }
    try:
        params: dict[str, Any] = {
            "group_id": group_id,
            "limit": _GROUP_MSG_FETCH_LIMIT,
        }
        if since_seq is not None:
            params["since_seq"] = since_seq
        payload = await authenticated_rpc_call(
            client,
            GROUP_RPC_ENDPOINT,
            "list_messages",
            params,
            auth=auth,
            credential_name=credential_name,
        )
        return _persist_and_classify_group_messages(
            owner_did=owner_did,
            group_id=group_id,
            payload=payload,
            credential_name=credential_name,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Failed to fetch group messages group_id=%s error=%s", group_id, exc
        )
        return {**empty, "error": str(exc)}


async def fetch_group_messages(
    group_watch: dict[str, Any],
    *,
    owner_did: str,
    credential_name: str,
) -> dict[str, Any]:
    """Fetch incremental messages for all active groups in the watch set.

    Coordinates parallel fetches via asyncio.gather, then best-effort resolves
    missing profile_url for member_joined events.
    """
    groups = group_watch.get("groups", [])
    if not groups:
        return {"fetched_groups": 0, "total_new_messages": 0, "errors": []}

    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        return {
            "fetched_groups": 0,
            "total_new_messages": 0,
            "errors": ["no_authenticator"],
        }

    auth, _ = auth_result

    async with create_user_service_client(config) as client:
        # Parallel fetch for all groups
        tasks = []
        for group in groups:
            tasks.append(
                _fetch_one_group_messages(
                    client,
                    group_id=group["group_id"],
                    since_seq=group.get("last_synced_seq"),
                    owner_did=owner_did,
                    credential_name=credential_name,
                    auth=auth,
                )
            )
        results = await asyncio.gather(*tasks)

        # Attach results to group entries and collect profile backfill targets
        errors: list[str] = []
        total_new = 0
        profile_backfill: list[tuple[str, dict[str, Any]]] = []

        for group, result in zip(groups, results):
            if "error" in result:
                errors.append(f"{group['group_id']}: {result['error']}")
            total_new += result.get("total", 0)
            group["new_messages"] = result

            # Collect member_joined events missing profile_url
            for event in result.get("member_joined", []):
                se = event.get("system_event", {})
                subject = se.get("subject", {})
                if subject.get("handle") and not subject.get("profile_url"):
                    profile_backfill.append((group["group_id"], event))

        # Best-effort profile_url backfill for new members
        for group_id, event in profile_backfill:
            se = event.get("system_event", {})
            subject = se.get("subject", {})
            handle = subject.get("handle", "")
            local_part = handle.split(".")[0] if "." in handle else handle
            if not local_part:
                continue
            try:
                profile = await rpc_call(
                    client,
                    PROFILE_RPC,
                    "get_public_profile",
                    {"handle": local_part},
                )
                profile_url = profile.get("profile_url")
                if profile_url:
                    subject["profile_url"] = profile_url
                    # Update local member cache
                    user_id = se.get("subject", {}).get("user_id", "")
                    if user_id:
                        conn = local_store.get_connection()
                        try:
                            local_store.ensure_schema(conn)
                            local_store.upsert_group_member(
                                conn,
                                owner_did=owner_did,
                                group_id=group_id,
                                user_id=user_id,
                                profile_url=profile_url,
                                credential_name=credential_name,
                            )
                        finally:
                            conn.close()
            except Exception:  # noqa: BLE001
                pass  # best-effort, silently ignore

    return {
        "fetched_groups": len(groups),
        "total_new_messages": total_new,
        "errors": errors,
    }


# ---------- E2EE helpers ----------


def _load_or_create_e2ee_client(local_did: str, credential_name: str) -> E2eeClient:
    """Load the latest disk-first E2EE state from SQLite."""
    return load_e2ee_client(local_did, credential_name)


def _save_e2ee_client(client: E2eeClient, credential_name: str) -> None:
    """Persist the latest E2EE state into SQLite."""
    save_e2ee_client(client, credential_name)


async def _send_msg(
    http_client,
    sender_did,
    receiver_did,
    msg_type,
    content,
    *,
    auth,
    credential_name="default",
):
    """Send a message (E2EE or plain)."""
    if isinstance(content, dict):
        content = json.dumps(content)
    return await authenticated_rpc_call(
        http_client,
        MESSAGE_RPC,
        "send",
        params={
            "sender_did": sender_did,
            "receiver_did": receiver_did,
            "content": content,
            "type": msg_type,
        },
        auth=auth,
        credential_name=credential_name,
    )


# ---------- Core functions ----------


async def check_identity(credential_name: str = "default") -> dict[str, Any]:
    """Check identity status; bootstrap missing JWT and refresh expired JWT."""
    data = load_identity(credential_name)
    if data is None:
        return {"status": "no_identity", "did": None, "name": None, "jwt_valid": False}

    result: dict[str, Any] = {
        "status": "ok",
        "did": data["did"],
        "name": data.get("name"),
        "jwt_valid": False,
    }

    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        result["status"] = "no_did_document"
        result["error"] = "Credential missing DID document; please recreate identity"
        return result

    auth, _ = auth_result
    old_token = data["jwt_token"]

    try:
        async with create_user_service_client(config) as client:
            await authenticated_rpc_call(
                client,
                AUTH_RPC,
                "get_me",
                auth=auth,
                credential_name=credential_name,
            )
            result["jwt_valid"] = True
            # Check if token was refreshed (authenticated_rpc_call auto-persists new JWT)
            refreshed_data = load_identity(credential_name)
            if refreshed_data and refreshed_data.get("jwt_token") != old_token:
                result["jwt_refreshed"] = True
    except Exception as e:
        result["status"] = "jwt_refresh_failed"
        result["error"] = str(e)

    return result


async def summarize_inbox(
    credential_name: str = "default",
) -> dict[str, Any]:
    """Fetch inbox and summarize user-visible unread messages."""
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        return {
            "status": "no_identity",
            "total": 0,
            "by_type": {},
            "text_messages": 0,
            "text_by_sender": {},
            "messages": [],
        }

    auth, data = auth_result
    try:
        async with create_molt_message_client(config) as client:
            inbox = await authenticated_rpc_call(
                client,
                MESSAGE_RPC,
                "get_inbox",
                params={"user_did": data["did"], "limit": _INBOX_FETCH_LIMIT},
                auth=auth,
                credential_name=credential_name,
            )
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "error": str(exc),
            "total": 0,
            "by_type": {},
            "text_messages": 0,
            "text_by_sender": {},
            "messages": [],
        }

    messages = inbox.get("messages", [])
    visible_messages = [
        _strip_hidden_user_fields(message)
        for message in messages
        if _is_user_visible_message_type(str(message.get("type") or ""))
    ]
    return _build_visible_inbox_report(visible_messages)


async def _build_inbox_report_with_auto_e2ee(
    credential_name: str = "default",
    *,
    listener_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fetch inbox, auto-handle E2EE, and return the surfaced messages.

    When the real-time WebSocket listener is running, E2EE processing is
    skipped here to avoid state conflicts (the listener already handles
    E2EE in real time and owns the session state file).
    """
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        return {
            "status": "no_identity",
            "total": 0,
            "by_type": {},
            "text_messages": 0,
            "text_by_sender": {},
            "messages": [],
        }

    websocket_mode = is_websocket_mode(config)
    listener_owned_inbox = False
    if websocket_mode:
        resolved_listener_status = listener_status or ensure_listener_runtime(
            credential_name,
            config=config,
        )
        listener_owned_inbox = bool(resolved_listener_status.get("was_running", False))

    auth, data = auth_result
    if websocket_mode and listener_owned_inbox:
        report = _build_local_inbox_report(data["did"])
        local_messages = list(report.get("messages", []))
        remote_sync = await _sync_remote_visible_inbox_messages(
            credential_name=credential_name,
            auth=auth,
            owner_did=str(data["did"]),
            config=config,
        )
        merged_messages = _merge_visible_inbox_messages(
            local_messages,
            remote_sync.get("messages", []),
            limit=_INBOX_FETCH_LIMIT,
        )
        report = _build_visible_inbox_report(merged_messages)
        report["source"] = "local_ws_cache"
        report["http_sync"] = {
            "attempted": True,
            "status": remote_sync.get("status", "error"),
            "total": remote_sync.get("total", 0),
        }
        if isinstance(remote_sync.get("error"), str):
            report["http_sync"]["error"] = remote_sync["error"]
        return report
    try:
        async with create_molt_message_client(config) as client:
            inbox = await authenticated_rpc_call(
                client,
                MESSAGE_RPC,
                "get_inbox",
                params={"user_did": data["did"], "limit": _INBOX_FETCH_LIMIT},
                auth=auth,
                credential_name=credential_name,
            )
            messages = list(inbox.get("messages", []))
            messages.sort(key=_message_sort_key)

            e2ee_client = _load_or_create_e2ee_client(data["did"], credential_name)
            processed_ids: list[str] = []
            processed_id_set: set[str] = set()
            rendered_decrypted_messages: list[dict[str, Any]] = []

            if listener_owned_inbox:
                # ws_listener owns E2EE state — skip processing to avoid
                # state conflicts (race condition on session seq numbers).
                logger.info(
                    "ws_listener is running, skipping E2EE inbox processing"
                )
            else:
                for message in messages:
                    msg_type = str(message.get("type") or "")
                    if msg_type not in _E2EE_MSG_TYPES:
                        continue

                    sender_did = str(message.get("sender_did") or "")
                    try:
                        content = (
                            json.loads(message.get("content"))
                            if isinstance(message.get("content"), str)
                            else message.get("content", {})
                        )
                    except (TypeError, json.JSONDecodeError):
                        logger.warning(
                            "Skipping malformed E2EE inbox payload type=%s sender=%s",
                            msg_type,
                            sender_did,
                        )
                        continue

                    if msg_type == "e2ee_msg":
                        try:
                            original_type, plaintext = e2ee_client.decrypt_message(content)
                            rendered_decrypted_messages.append(
                                _decorate_user_visible_e2ee_message(
                                    message,
                                    original_type=original_type,
                                    plaintext=plaintext,
                                )
                            )
                            if isinstance(message.get("id"), str) and message["id"]:
                                processed_ids.append(message["id"])
                                processed_id_set.add(message["id"])
                        except Exception as exc:  # noqa: BLE001
                            error_code, retry_hint = _classify_decrypt_error(exc)
                            error_content = build_e2ee_error_content(
                                error_code=error_code,
                                session_id=content.get("session_id"),
                                failed_msg_id=message.get("id"),
                                failed_server_seq=message.get("server_seq"),
                                retry_hint=retry_hint,
                                required_e2ee_version=(
                                    SUPPORTED_E2EE_VERSION
                                    if error_code == "unsupported_version"
                                    else None
                                ),
                                message=build_e2ee_error_message(
                                    error_code,
                                    required_e2ee_version=(
                                        SUPPORTED_E2EE_VERSION
                                        if error_code == "unsupported_version"
                                        else None
                                    ),
                                    detail=str(exc),
                                ),
                            )
                            await _send_msg(
                                client,
                                data["did"],
                                sender_did,
                                "e2ee_error",
                                error_content,
                                auth=auth,
                                credential_name=credential_name,
                            )
                            logger.warning(
                                "Failed to auto-decrypt E2EE inbox message sender=%s error=%s",
                                sender_did,
                                exc,
                            )
                        continue

                    try:
                        if msg_type == "e2ee_error":
                            record_remote_failure(
                                credential_name=credential_name,
                                peer_did=sender_did,
                                content=content,
                            )
                        responses = await e2ee_client.process_e2ee_message(msg_type, content)
                        session_ready = True
                        terminal_error_notified = any(
                            response_type == "e2ee_error"
                            for response_type, _ in responses
                        )
                        if msg_type in _E2EE_SESSION_SETUP_TYPES:
                            session_ready = e2ee_client.has_session_id(
                                content.get("session_id")
                            )
                        for response_type, response_content in responses:
                            await _send_msg(
                                client,
                                data["did"],
                                sender_did,
                                response_type,
                                response_content,
                                auth=auth,
                                credential_name=credential_name,
                            )

                        if session_ready or terminal_error_notified:
                            if isinstance(message.get("id"), str) and message["id"]:
                                processed_ids.append(message["id"])
                                processed_id_set.add(message["id"])
                    except Exception as exc:  # noqa: BLE001
                        logger.warning(
                            "E2EE auto-processing failed type=%s sender=%s error=%s",
                            msg_type,
                            sender_did,
                            exc,
                        )

            if processed_ids:
                await authenticated_rpc_call(
                    client,
                    MESSAGE_RPC,
                    "mark_read",
                    params={"user_did": data["did"], "message_ids": processed_ids},
                    auth=auth,
                    credential_name=credential_name,
                )

            if not listener_owned_inbox:
                _save_e2ee_client(e2ee_client, credential_name)

        remaining_messages = [
            message
            for message in messages
            if str(message.get("id") or "") not in processed_id_set
        ]
        visible_messages = rendered_decrypted_messages + [
            _strip_hidden_user_fields(message)
            for message in remaining_messages
            if _is_user_visible_message_type(str(message.get("type") or ""))
        ]
        report = _build_visible_inbox_report(visible_messages)
        report["source"] = (
            "remote_http_fallback" if websocket_mode else "remote_http"
        )
        return report
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "error": str(exc),
            "total": 0,
            "by_type": {},
            "text_messages": 0,
            "text_by_sender": {},
            "messages": [],
        }


async def check_status(
    credential_name: str = "default",
) -> dict[str, Any]:
    """Unified status check orchestrator."""
    report: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    report["local_upgrade"] = ensure_local_upgrade_ready(credential_name)
    report["credential_layout"] = report["local_upgrade"]["credential_layout"]
    report["local_database"] = report["local_upgrade"]["local_database"]
    if not report["credential_layout"]["credential_ready"]:
        report["identity"] = {
            "status": "storage_migration_required",
            "did": None,
            "name": None,
            "jwt_valid": False,
            "error": "Credential storage migration failed or is incomplete",
        }
        report["inbox"] = {"status": "skipped", "total": 0}
        report["group_watch"] = {"status": "skipped", "active_groups": 0, "groups": []}
        report["e2ee_sessions"] = {"active": 0}
        return report

    if report["local_database"]["status"] == "error":
        report["identity"] = {
            "status": "local_database_migration_failed",
            "did": None,
            "name": None,
            "jwt_valid": False,
            "error": "Local database migration failed",
        }
        report["inbox"] = {"status": "skipped", "total": 0}
        report["group_watch"] = {"status": "skipped", "active_groups": 0, "groups": []}
        report["e2ee_sessions"] = {"active": 0}
        return report

    # 1. Identity check
    report["identity"] = await check_identity(credential_name)

    # Return early if identity does not exist
    if report["identity"]["status"] == "no_identity":
        report["inbox"] = {"status": "skipped", "total": 0}
        report["group_watch"] = {"status": "no_identity", "active_groups": 0, "groups": []}
        report["e2ee_sessions"] = {"active": 0}
        return report

    # 2. Local discovery-group watch summary
    owner_did = report["identity"].get("did")
    report["group_watch"] = summarize_group_watch(owner_did)

    # 2b. Fetch incremental group messages for active groups
    if (
        report["group_watch"].get("status") == "ok"
        and report["group_watch"].get("active_groups", 0) > 0
        and owner_did
    ):
        report["group_watch"]["fetch_summary"] = await fetch_group_messages(
            report["group_watch"],
            owner_did=owner_did,
            credential_name=credential_name,
        )

    config = SDKConfig()
    websocket_mode = is_websocket_mode(config)
    if websocket_mode:
        listener_runtime = ensure_listener_runtime(
            credential_name,
            config=config,
        )
    else:
        listener_runtime = get_listener_runtime_report(
            credential_name,
            config=config,
        )

    # 3. Inbox summary / delivery
    report["inbox"] = await _build_inbox_report_with_auto_e2ee(
        credential_name,
        listener_status=listener_runtime,
    )

    # 4. E2EE session status
    try:
        e2ee_client = load_e2ee_client(owner_did, credential_name)
        report["e2ee_sessions"] = {
            "active": len(e2ee_client.export_state().get("sessions", []))
        }
    except Exception:  # noqa: BLE001
        report["e2ee_sessions"] = {"active": 0}

    # 5. Real-time listener status
    report["realtime_listener"] = {
        "mode": "websocket" if websocket_mode else "http",
        "installed": listener_runtime.get("installed", False),
        "running": listener_runtime.get("running", False),
        "service_running": listener_runtime.get("service_running", False),
        "daemon_available": listener_runtime.get("daemon_available", False),
        "degraded": listener_runtime.get("degraded", False),
        "auto_restart_paused": listener_runtime.get("auto_restart_paused", False),
        "consecutive_restart_failures": listener_runtime.get(
            "consecutive_restart_failures",
            0,
        ),
        "last_restart_attempt_at": listener_runtime.get("last_restart_attempt_at"),
        "last_restart_result": listener_runtime.get("last_restart_result"),
    }
    last_error = listener_runtime.get("last_error")
    if isinstance(last_error, str) and last_error:
        report["realtime_listener"]["last_error"] = last_error
    if not listener_runtime.get("installed", False):
        report["realtime_listener"]["hint"] = (
            "Run: python scripts/setup_realtime.py --credential " + credential_name
        )

    return report


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Unified status check")
    parser.add_argument(
        "--upgrade-only",
        action="store_true",
        help="Run local skill upgrade checks/migrations and exit",
    )
    parser.add_argument(
        "--credential",
        type=str,
        default="default",
        help="Credential name (default: default)",
    )
    args = parser.parse_args()
    logging.getLogger(__name__).info(
        "check_status CLI started credential=%s upgrade_only=%s",
        args.credential,
        args.upgrade_only,
    )

    if args.upgrade_only:
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "local_upgrade": ensure_local_upgrade_ready(
                args.credential,
                coordinate_listener_during_database_upgrade=True,
            ),
        }
        report["credential_layout"] = report["local_upgrade"]["credential_layout"]
        report["local_database"] = report["local_upgrade"]["local_database"]
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    report = asyncio.run(check_status(args.credential))
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
