"""E2EE outbox helpers for resendable private encrypted messages.

[INPUT]: local_store (SQLite persistence), outgoing encrypted message context,
         incoming e2ee_error payloads
[OUTPUT]: begin_send_attempt(), mark_send_success(), record_remote_failure(),
          list_failed_records(), get_record(), mark_dropped()
[POS]: Persistence helper layer between E2EE messaging scripts/listener and SQLite
       outbox state, enabling user-driven resend decisions after peer-side failures

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
from typing import Any

from credential_store import load_identity
import local_store


def _open_db():
    conn = local_store.get_connection()
    local_store.ensure_schema(conn)
    return conn


def _load_owner_did(credential_name: str) -> str:
    """Resolve owner_did from credential storage."""
    credential = load_identity(credential_name)
    if credential is None or not credential.get("did"):
        raise ValueError(f"Credential '{credential_name}' is unavailable")
    return str(credential["did"])


def begin_send_attempt(
    *,
    peer_did: str,
    plaintext: str,
    original_type: str,
    credential_name: str,
    session_id: str | None,
    outbox_id: str | None = None,
) -> str:
    """Create or reset an E2EE outbox entry before attempting network send."""
    owner_did = _load_owner_did(credential_name)
    conn = _open_db()
    try:
        if outbox_id is None:
            return local_store.queue_e2ee_outbox(
                conn,
                owner_did=owner_did,
                peer_did=peer_did,
                plaintext=plaintext,
                session_id=session_id,
                original_type=original_type,
                credential_name=credential_name,
            )
        local_store.update_e2ee_outbox_status(
            conn,
            outbox_id=outbox_id,
            local_status="queued",
            owner_did=owner_did,
            credential_name=credential_name,
        )
        return outbox_id
    finally:
        conn.close()


def mark_send_success(
    *,
    outbox_id: str,
    credential_name: str,
    local_did: str,
    peer_did: str,
    plaintext: str,
    original_type: str,
    session_id: str | None,
    sent_msg_id: str | None,
    sent_server_seq: int | None,
    sent_at: str | None,
    client_msg_id: str,
    title: str | None = None,
) -> None:
    """Persist a successful encrypted send into outbox and local messages."""
    conn = _open_db()
    try:
        metadata = json.dumps(
            {
                "outbox_id": outbox_id,
                "session_id": session_id,
                "client_msg_id": client_msg_id,
            },
            ensure_ascii=False,
        )
        local_store.mark_e2ee_outbox_sent(
            conn,
            outbox_id=outbox_id,
            owner_did=local_did,
            credential_name=credential_name,
            session_id=session_id,
            sent_msg_id=sent_msg_id,
            sent_server_seq=sent_server_seq,
            metadata=metadata,
        )
        local_store.store_message(
            conn,
            msg_id=sent_msg_id or outbox_id,
            owner_did=local_did,
            thread_id=local_store.make_thread_id(local_did, peer_did=peer_did),
            direction=1,
            sender_did=local_did,
            receiver_did=peer_did,
            content_type=original_type,
            content=plaintext,
            title=title,
            server_seq=sent_server_seq,
            sent_at=sent_at,
            is_e2ee=True,
            credential_name=credential_name,
            metadata=metadata,
        )
        local_store.upsert_contact(conn, owner_did=local_did, did=peer_did)
    finally:
        conn.close()


def record_remote_failure(
    *,
    credential_name: str,
    peer_did: str,
    content: dict[str, Any],
) -> str | None:
    """Update the best matching outbox entry from a received e2ee_error payload."""
    owner_did = _load_owner_did(credential_name)
    conn = _open_db()
    try:
        return local_store.mark_e2ee_outbox_failed(
            conn,
            owner_did=owner_did,
            credential_name=credential_name,
            peer_did=peer_did,
            session_id=content.get("session_id"),
            failed_msg_id=content.get("failed_msg_id"),
            failed_server_seq=content.get("failed_server_seq"),
            error_code=str(content.get("error_code", "unknown")),
            retry_hint=content.get("retry_hint"),
            metadata=json.dumps(content, ensure_ascii=False),
        )
    finally:
        conn.close()


def list_failed_records(credential_name: str) -> list[dict[str, Any]]:
    """List failed E2EE outbox entries for the credential."""
    owner_did = _load_owner_did(credential_name)
    conn = _open_db()
    try:
        return local_store.list_e2ee_outbox(
            conn,
            owner_did=owner_did,
            credential_name=credential_name,
            local_status="failed",
        )
    finally:
        conn.close()


def get_record(outbox_id: str, credential_name: str) -> dict[str, Any] | None:
    """Fetch one E2EE outbox record."""
    owner_did = _load_owner_did(credential_name)
    conn = _open_db()
    try:
        return local_store.get_e2ee_outbox(
            conn,
            outbox_id=outbox_id,
            owner_did=owner_did,
            credential_name=credential_name,
        )
    finally:
        conn.close()


def mark_dropped(outbox_id: str, credential_name: str) -> None:
    """Mark an E2EE outbox record as dropped by the local user."""
    owner_did = _load_owner_did(credential_name)
    conn = _open_db()
    try:
        local_store.update_e2ee_outbox_status(
            conn,
            outbox_id=outbox_id,
            local_status="dropped",
            owner_did=owner_did,
            credential_name=credential_name,
        )
    finally:
        conn.close()


def record_local_failure(
    *,
    outbox_id: str,
    credential_name: str,
    error_code: str,
    retry_hint: str | None = None,
    metadata: str | None = None,
) -> None:
    """Mark a local send attempt as failed before any peer response exists."""
    owner_did = _load_owner_did(credential_name)
    conn = _open_db()
    try:
        local_store.set_e2ee_outbox_failure_by_id(
            conn,
            outbox_id=outbox_id,
            owner_did=owner_did,
            credential_name=credential_name,
            error_code=error_code,
            retry_hint=retry_hint,
            metadata=metadata,
        )
    finally:
        conn.close()


__all__ = [
    "begin_send_attempt",
    "mark_send_success",
    "record_remote_failure",
    "record_local_failure",
    "list_failed_records",
    "get_record",
    "mark_dropped",
]
