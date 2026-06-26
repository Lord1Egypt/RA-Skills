"""SQLite-backed E2EE session state store.

[INPUT]: local_store SQLite connection/schema, credential_store identity keys,
         legacy JSON E2EE state (migration), and utils.e2ee E2eeClient export/
         restore helpers
[OUTPUT]: Disk-first E2EE client load/save helpers plus SQLite transaction
          wrapper for state mutations
[POS]: Persistence bridge between E2EE runtime code and awiki.db, replacing
       JSON-file session truth with SQLite rows and transactional updates

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import sqlite3
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from credential_store import load_identity
from e2ee_store import delete_e2ee_state, load_e2ee_state
from utils import E2eeClient

import local_store

_STATE_VERSION = "hpke_v1"


def _utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _load_key_material(credential_name: str) -> tuple[str | None, str | None]:
    """Load the credential's E2EE private keys."""
    cred = load_identity(credential_name)
    if cred is None:
        return None, None
    return (
        cred.get("e2ee_signing_private_pem"),
        cred.get("e2ee_agreement_private_pem"),
    )


def _rows_to_state(
    *,
    rows: list[sqlite3.Row],
    local_did: str,
    signing_pem: str | None,
    x25519_pem: str | None,
) -> dict[str, Any]:
    """Build an ``E2eeClient.from_state`` payload from SQLite rows."""
    sessions: list[dict[str, Any]] = []
    confirmed_session_ids: list[str] = []
    for row in rows:
        session = dict(row)
        sessions.append(
            {
                "session_id": session["session_id"],
                "local_did": local_did,
                "peer_did": session["peer_did"],
                "is_initiator": bool(session["is_initiator"]),
                "send_chain_key": session["send_chain_key"],
                "recv_chain_key": session["recv_chain_key"],
                "send_seq": session["send_seq"],
                "recv_seq": session["recv_seq"],
                "expires_at": session["expires_at"],
                "created_at": session["created_at"],
                "active_at": session["active_at"],
            }
        )
        if session["peer_confirmed"]:
            confirmed_session_ids.append(session["session_id"])
    return {
        "version": _STATE_VERSION,
        "local_did": local_did,
        "signing_pem": signing_pem,
        "x25519_pem": x25519_pem,
        "confirmed_session_ids": sorted(confirmed_session_ids),
        "sessions": sessions,
    }


def _load_rows_locked(
    conn: sqlite3.Connection,
    *,
    local_did: str,
) -> list[sqlite3.Row]:
    """Load all persisted E2EE sessions for one owner."""
    return conn.execute(
        """
        SELECT owner_did, peer_did, session_id, is_initiator, send_chain_key,
               recv_chain_key, send_seq, recv_seq, expires_at, created_at,
               active_at, peer_confirmed, credential_name, updated_at
        FROM e2ee_sessions
        WHERE owner_did = ?
        ORDER BY peer_did
        """,
        (local_did,),
    ).fetchall()


def _save_rows_locked(
    conn: sqlite3.Connection,
    *,
    local_did: str,
    credential_name: str,
    client: E2eeClient,
    loaded_peer_dids: set[str],
) -> None:
    """Persist the current E2EE client state into SQLite rows."""
    state = client.export_state()
    sessions = state.get("sessions", [])
    confirmed_ids = set(state.get("confirmed_session_ids", []))
    current_peer_dids = {
        str(session["peer_did"])
        for session in sessions
        if session.get("peer_did")
    }

    for removed_peer_did in sorted(loaded_peer_dids - current_peer_dids):
        conn.execute(
            "DELETE FROM e2ee_sessions WHERE owner_did = ? AND peer_did = ?",
            (local_did, removed_peer_did),
        )

    for session in sessions:
        peer_did = str(session["peer_did"])
        session_id = str(session["session_id"])
        conn.execute(
            """
            INSERT INTO e2ee_sessions
            (owner_did, peer_did, session_id, is_initiator, send_chain_key,
             recv_chain_key, send_seq, recv_seq, expires_at, created_at,
             active_at, peer_confirmed, credential_name, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(owner_did, peer_did) DO UPDATE SET
                session_id = excluded.session_id,
                is_initiator = excluded.is_initiator,
                send_chain_key = excluded.send_chain_key,
                recv_chain_key = excluded.recv_chain_key,
                send_seq = excluded.send_seq,
                recv_seq = excluded.recv_seq,
                expires_at = excluded.expires_at,
                created_at = excluded.created_at,
                active_at = excluded.active_at,
                peer_confirmed = excluded.peer_confirmed,
                credential_name = excluded.credential_name,
                updated_at = excluded.updated_at
            """,
            (
                local_did,
                peer_did,
                session_id,
                int(bool(session.get("is_initiator", False))),
                session["send_chain_key"],
                session["recv_chain_key"],
                int(session.get("send_seq", 0)),
                int(session.get("recv_seq", 0)),
                session.get("expires_at"),
                session.get("created_at") or _utc_now_iso(),
                session.get("active_at"),
                int(session_id in confirmed_ids),
                credential_name,
                _utc_now_iso(),
            ),
        )


def _migrate_legacy_json_locked(
    conn: sqlite3.Connection,
    *,
    local_did: str,
    credential_name: str,
    signing_pem: str | None,
    x25519_pem: str | None,
) -> list[sqlite3.Row]:
    """Import legacy JSON E2EE state into SQLite on first access."""
    existing_rows = _load_rows_locked(conn, local_did=local_did)
    if existing_rows:
        return existing_rows

    legacy_state = load_e2ee_state(credential_name)
    if legacy_state is None or legacy_state.get("local_did") != local_did:
        return existing_rows

    if signing_pem is not None:
        legacy_state["signing_pem"] = signing_pem
    if x25519_pem is not None:
        legacy_state["x25519_pem"] = x25519_pem
    client = E2eeClient.from_state(legacy_state)
    _save_rows_locked(
        conn,
        local_did=local_did,
        credential_name=credential_name,
        client=client,
        loaded_peer_dids=set(),
    )
    delete_e2ee_state(credential_name)
    return _load_rows_locked(conn, local_did=local_did)


def _load_client_locked(
    conn: sqlite3.Connection,
    *,
    local_did: str,
    credential_name: str,
) -> tuple[E2eeClient, set[str]]:
    """Load a disk-first E2EE client inside an open SQLite transaction."""
    signing_pem, x25519_pem = _load_key_material(credential_name)
    rows = _migrate_legacy_json_locked(
        conn,
        local_did=local_did,
        credential_name=credential_name,
        signing_pem=signing_pem,
        x25519_pem=x25519_pem,
    )
    if rows:
        state = _rows_to_state(
            rows=rows,
            local_did=local_did,
            signing_pem=signing_pem,
            x25519_pem=x25519_pem,
        )
        client = E2eeClient.from_state(state)
    else:
        client = E2eeClient(local_did, signing_pem=signing_pem, x25519_pem=x25519_pem)
    loaded_peer_dids = {str(row["peer_did"]) for row in rows}
    return client, loaded_peer_dids


@dataclass
class E2eeStateTransaction(AbstractContextManager["E2eeStateTransaction"]):
    """SQLite-backed transaction wrapper for one E2EE client mutation."""

    local_did: str
    credential_name: str = "default"

    def __post_init__(self) -> None:
        self._conn = local_store.get_connection()
        local_store.ensure_schema(self._conn)
        self._conn.execute("BEGIN IMMEDIATE")
        self.client, self._loaded_peer_dids = _load_client_locked(
            self._conn,
            local_did=self.local_did,
            credential_name=self.credential_name,
        )
        self._closed = False

    def commit(self) -> None:
        """Persist the in-memory client back into SQLite and commit."""
        _save_rows_locked(
            self._conn,
            local_did=self.local_did,
            credential_name=self.credential_name,
            client=self.client,
            loaded_peer_dids=self._loaded_peer_dids,
        )
        self._conn.commit()
        self._closed = True

    def commit_without_saving(self) -> None:
        """Commit a read-only transaction (for migration side effects only)."""
        self._conn.commit()
        self._closed = True

    def rollback(self) -> None:
        """Rollback any pending SQLite changes."""
        self._conn.rollback()
        self._closed = True

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        if not self._closed:
            self.rollback()
        self._conn.close()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
        return None


def load_e2ee_client(local_did: str, credential_name: str = "default") -> E2eeClient:
    """Load the latest E2EE state from SQLite (migrating legacy JSON if needed)."""
    tx = E2eeStateTransaction(local_did=local_did, credential_name=credential_name)
    try:
        tx.commit_without_saving()
        return tx.client
    finally:
        tx.close()


def save_e2ee_client(client: E2eeClient, credential_name: str = "default") -> None:
    """Persist one E2EE client into SQLite using a fresh transaction."""
    tx = E2eeStateTransaction(local_did=client.local_did, credential_name=credential_name)
    try:
        tx.client = client
        tx.commit()
    finally:
        tx.close()


__all__ = [
    "E2eeStateTransaction",
    "load_e2ee_client",
    "save_e2ee_client",
]
