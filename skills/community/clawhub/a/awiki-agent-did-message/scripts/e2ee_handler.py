"""Transparent E2EE handler for the WebSocket listener.

[INPUT]: credential_store (E2EE keys), SQLite-backed session store,
         E2eeClient (encrypt/decrypt), build_e2ee_error (error response builder)
[OUTPUT]: E2eeHandler class (protocol message handling + encrypted message decryption),
          DecryptResult NamedTuple (decrypted params + structured error responses)
[POS]: E2EE processing module for ws_listener.py, intercepts E2EE messages before
       classify_message, keeps SQLite as the single session truth source, and
       emits sender-facing e2ee_error notifications with failed message identifiers

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, NamedTuple

from credential_store import load_identity
from e2ee_session_store import E2eeStateTransaction, load_e2ee_client
from e2ee_outbox import record_remote_failure
from utils.e2ee import (
    SUPPORTED_E2EE_VERSION,
    build_e2ee_error_content,
    build_e2ee_error_message,
)

logger = logging.getLogger(__name__)
_E2EE_USER_NOTICE = "This is an encrypted message."

# E2EE message type sets
_E2EE_ALL_TYPES = frozenset({"e2ee_init", "e2ee_ack", "e2ee_msg", "e2ee_rekey", "e2ee_error"})
_E2EE_PROTOCOL_TYPES = frozenset({"e2ee_init", "e2ee_ack", "e2ee_rekey", "e2ee_error"})


class DecryptResult(NamedTuple):
    """Result of decrypt_message: decrypted params + error responses to send."""
    params: dict[str, Any] | None
    error_responses: list[tuple[str, dict[str, Any]]]


class E2eeHandler:
    """E2EE handler for the WebSocket listener.

    Responsibilities:
    - Protocol messages (init/rekey/error): handled internally, not forwarded to webhook
    - Encrypted messages (e2ee_msg): decrypted and returned as plaintext params for routing
    """

    def __init__(
        self,
        credential_name: str,
        save_interval: float = 30.0,
        decrypt_fail_action: str = "drop",
    ) -> None:
        self._credential_name = credential_name
        self._save_interval = save_interval
        self._decrypt_fail_action = decrypt_fail_action

        self._local_did: str | None = None
        self._lock = asyncio.Lock()

    async def initialize(self, local_did: str) -> bool:
        """Initialize: validate E2EE keys and ensure SQLite-backed state is loadable.

        Args:
            local_did: Local DID identifier.

        Returns:
            Whether initialization was successful.
        """
        try:
            cred = load_identity(self._credential_name)
            signing_pem: str | None = None
            x25519_pem: str | None = None
            if cred is not None:
                signing_pem = cred.get("e2ee_signing_private_pem")
                x25519_pem = cred.get("e2ee_agreement_private_pem")

            if signing_pem is None or x25519_pem is None:
                logger.warning("Credential '%s' is missing E2EE keys", self._credential_name)
                return False

            load_e2ee_client(local_did, self._credential_name)
            self._local_did = local_did
            logger.info("E2EE handler initialized successfully, DID=%s", local_did)
            return True

        except Exception:
            logger.exception("E2EE handler initialization failed")
            return False

    @property
    def is_ready(self) -> bool:
        """Whether the E2EE client is ready."""
        return self._local_did is not None

    def is_e2ee_type(self, msg_type: str) -> bool:
        """Check whether the message type belongs to the E2EE category."""
        return msg_type in _E2EE_ALL_TYPES

    def is_protocol_type(self, msg_type: str) -> bool:
        """Check whether the message type is an E2EE protocol message (handled internally, not forwarded)."""
        return msg_type in _E2EE_PROTOCOL_TYPES

    async def handle_protocol_message(
        self, params: dict[str, Any],
    ) -> list[tuple[str, dict[str, Any]]]:
        """Handle E2EE protocol messages (init/rekey/error).

        Args:
            params: The params field from the WebSocket push notification.

        Returns:
            List of responses to send (usually empty for the HPKE scheme).
        """
        if self._local_did is None:
            return []

        msg_type = params.get("type", "")
        sender_did = params.get("sender_did", "")
        raw_content = params.get("content", "")

        try:
            content = json.loads(raw_content) if isinstance(raw_content, str) else raw_content
        except (json.JSONDecodeError, TypeError):
            logger.warning("Failed to parse E2EE protocol message content: type=%s", msg_type)
            return []
        if msg_type == "e2ee_error" and isinstance(content, dict) and sender_did:
            content = dict(content)
            content.setdefault("sender_did", sender_did)

        async with self._lock:
            try:
                with E2eeStateTransaction(self._local_did, self._credential_name) as state_tx:
                    client = state_tx.client
                    if msg_type == "e2ee_error":
                        matched_outbox = record_remote_failure(
                            credential_name=self._credential_name,
                            peer_did=sender_did,
                            content=content,
                        )
                        if matched_outbox:
                            logger.info("Updated failed E2EE outbox record: %s", matched_outbox)
                    responses = await client.process_e2ee_message(msg_type, content)
                    state_tx.commit()
                logger.info(
                    "E2EE protocol message processed: type=%s sender=%s responses=%d",
                    msg_type, sender_did[:20], len(responses),
                )
                return responses
            except Exception:
                logger.exception(
                    "E2EE protocol message processing error: type=%s sender=%s",
                    msg_type, sender_did[:20],
                )
                return []

    async def decrypt_message(
        self, params: dict[str, Any],
    ) -> DecryptResult:
        """Decrypt an e2ee_msg message.

        On success, returns DecryptResult with plaintext params and no error responses.
        On failure, returns DecryptResult with fallback params and an e2ee_error response
        to notify the sender.

        Args:
            params: The params field from the WebSocket push notification.

        Returns:
            DecryptResult with decrypted params and error responses.
        """
        if self._local_did is None:
            return DecryptResult(self._on_decrypt_fail(params), [])

        raw_content = params.get("content", "")
        try:
            content = json.loads(raw_content) if isinstance(raw_content, str) else raw_content
        except (json.JSONDecodeError, TypeError):
            logger.warning("Failed to parse E2EE message content")
            return DecryptResult(self._on_decrypt_fail(params), [])

        async with self._lock:
            try:
                with E2eeStateTransaction(self._local_did, self._credential_name) as state_tx:
                    client = state_tx.client
                    original_type, plaintext = client.decrypt_message(content)
                    state_tx.commit()
            except Exception as exc:
                logger.exception(
                    "E2EE message decryption failed: sender=%s",
                    params.get("sender_did", "")[:20],
                )
                error_code, retry_hint = self._classify_error(exc)
                error_content = build_e2ee_error_content(
                    error_code=error_code,
                    session_id=content.get("session_id") if isinstance(content, dict) else None,
                    failed_msg_id=params.get("id"),
                    failed_server_seq=params.get("server_seq"),
                    retry_hint=retry_hint,
                    required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                    message=build_e2ee_error_message(
                        error_code,
                        required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                        detail=str(exc),
                    ),
                )
                return DecryptResult(
                    self._on_decrypt_fail(params),
                    [("e2ee_error", error_content)],
                )

        # Build plaintext params: replace type and content, add _e2ee marker
        decrypted_params = dict(params)
        decrypted_params["type"] = original_type
        decrypted_params["content"] = plaintext
        decrypted_params["_e2ee"] = True
        decrypted_params["_e2ee_notice"] = _E2EE_USER_NOTICE
        logger.info(
            "E2EE message decrypted successfully: sender=%s original_type=%s",
            params.get("sender_did", "")[:20], original_type,
        )
        return DecryptResult(decrypted_params, [])

    async def maybe_save_state(self) -> None:
        """Compatibility no-op: state is persisted immediately after each mutation."""
        return None

    async def force_save_state(self) -> None:
        """Compatibility no-op: state is persisted immediately after each mutation."""
        return None

    async def _do_save(self) -> None:
        """Compatibility no-op: state is persisted immediately after each mutation."""
        return None

    @staticmethod
    def _classify_error(exc: BaseException) -> tuple[str, str]:
        """Map a decryption exception to an E2EE error code and retry hint."""
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

    def _on_decrypt_fail(self, params: dict[str, Any]) -> dict[str, Any] | None:
        """Fallback strategy on decryption failure."""
        if self._decrypt_fail_action == "forward_raw":
            return params
        return None


__all__ = ["E2eeHandler", "DecryptResult"]
