"""E2EE end-to-end encryption client (wraps ANP e2e_encryption_hpke).

[INPUT]: ANP E2eeHpkeSession / HpkeKeyManager / detect_message_type, local_did,
         signing_pem (secp256r1 key-2), x25519_pem (key-3)
[OUTPUT]: E2eeClient class providing high-level API for one-step initialization,
          encryption, decryption, proof-field-compatible protocol processing,
          state export/restore, and canonical e2ee_error message text generation
[POS]: Wraps ANP's underlying HPKE E2EE protocol (RFC 9180 + Chain Ratchet) to provide
       a simple encrypt/decrypt interface for upper-layer applications;
       supports cross-process state persistence and emits sender-facing e2ee_error
       responses for terminal protocol failures

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Any

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_pem_private_key,
)

from anp.e2e_encryption_hpke import (
    E2eeHpkeSession,
    SessionState,
    HpkeKeyManager,
    MessageType,
    generate_proof,
    validate_proof,
    detect_message_type,
    extract_x25519_public_key_from_did_document,
    extract_signing_public_key_from_did_document,
)
from anp.authentication import resolve_did_wba_document

logger = logging.getLogger(__name__)

# State version marker, used to distinguish from old formats
_STATE_VERSION = "hpke_v1"
SUPPORTED_E2EE_VERSION = "1.1"


def _extract_proof_verification_method(proof: Any) -> str:
    """Extract the proof verification method with field-name compatibility.

    The ANP HPKE protocol uses snake_case ``verification_method`` in message
    proofs, while some older callers may still send camelCase
    ``verificationMethod``. The receiver accepts both to avoid session setup
    failures during mixed-version deployments.

    Args:
        proof: Proof object from the E2EE message content.

    Returns:
        Verification method ID, or an empty string when unavailable.
    """
    if not isinstance(proof, dict):
        return ""
    return str(
        proof.get("verification_method")
        or proof.get("verificationMethod")
        or ""
    )


def ensure_supported_e2ee_version(content: dict[str, Any]) -> str:
    """Validate the required E2EE content version for the awiki runtime."""
    version = str(content.get("e2ee_version", "")).strip()
    if not version:
        raise ValueError(
            f"unsupported_version: missing e2ee_version (required {SUPPORTED_E2EE_VERSION})"
        )
    if version != SUPPORTED_E2EE_VERSION:
        raise ValueError(
            f"unsupported_version: expected {SUPPORTED_E2EE_VERSION}, got {version}"
        )
    return version


def build_e2ee_error_content(
    error_code: str,
    *,
    session_id: str | None = None,
    failed_msg_id: str | None = None,
    failed_server_seq: int | None = None,
    retry_hint: str | None = None,
    required_e2ee_version: str | None = None,
    message: str | None = None,
) -> dict[str, Any]:
    """Build an E2EE error payload without relying on a newer ANP package release."""
    content: dict[str, Any] = {
        "e2ee_version": SUPPORTED_E2EE_VERSION,
        "error_code": error_code,
    }
    if session_id is not None:
        content["session_id"] = session_id
    if failed_msg_id is not None:
        content["failed_msg_id"] = failed_msg_id
    if failed_server_seq is not None:
        content["failed_server_seq"] = failed_server_seq
    if retry_hint is not None:
        content["retry_hint"] = retry_hint
    if required_e2ee_version is not None:
        content["required_e2ee_version"] = required_e2ee_version
    if message is not None:
        content["message"] = message
    return content


def build_e2ee_error_message(
    error_code: str,
    *,
    required_e2ee_version: str | None = None,
    detail: str | None = None,
) -> str:
    """Build a consistent human-readable e2ee_error message."""
    version = required_e2ee_version or SUPPORTED_E2EE_VERSION
    base_messages = {
        "unsupported_version": (
            f"Peer E2EE content version is unsupported. "
            f"Please upgrade to e2ee_version={version}."
        ),
        "session_not_found": (
            "E2EE session was not found on the receiver. "
            "Please rekey or re-initialize before resending."
        ),
        "session_expired": (
            "E2EE session has expired. Please rekey and resend the message."
        ),
        "decryption_failed": (
            "E2EE decryption failed on the receiver. You may resend the message "
            "or rekey and resend."
        ),
        "invalid_seq": (
            "E2EE message sequence is invalid. Please rekey before resending."
        ),
        "proof_expired": (
            "The E2EE control message expired before it was processed. "
            "Please resend it with a fresh timestamp."
        ),
        "proof_from_future": (
            "The E2EE control message timestamp is too far in the future. "
            "Please sync the sender clock and resend."
        ),
    }
    message = base_messages.get(error_code, "E2EE processing failed.")
    if detail:
        return f"{message} Detail: {detail}"
    return message


def _classify_protocol_error(exc: BaseException) -> tuple[str, str] | None:
    """Map protocol-processing failures to sender-visible error codes when safe."""
    msg = str(exc).lower()
    if "unsupported_version" in msg:
        return ("unsupported_version", "drop")
    if "proof_expired" in msg:
        return ("proof_expired", "resend")
    if "proof_from_future" in msg:
        return ("proof_from_future", "drop")
    return None


class E2eeClient:
    """E2EE end-to-end encryption client (HPKE scheme).

    Wraps ANP ``E2eeHpkeSession`` and ``HpkeKeyManager``, providing:
    - One-step session initialization (no multi-step handshake)
    - Message encryption and decryption (Chain Ratchet forward secrecy)
    - Expired session cleanup

    Key design: E2EE uses two independent key pairs --
    - key-2 secp256r1: proof signing (identity verification)
    - key-3 X25519: HPKE key agreement
    Both are separate from the DID identity key (secp256k1 key-1).
    """

    def __init__(
        self,
        local_did: str,
        *,
        signing_pem: str | None = None,
        x25519_pem: str | None = None,
    ) -> None:
        """Initialize E2EE client.

        Args:
            local_did: Local DID identifier.
            signing_pem: secp256r1 signing key PEM string (key-2).
            x25519_pem: X25519 agreement key PEM string (key-3).
        """
        self.local_did = local_did
        self._signing_pem = signing_pem
        self._x25519_pem = x25519_pem

        # Load key objects
        self._signing_key: ec.EllipticCurvePrivateKey | None = None
        if signing_pem is not None:
            key = load_pem_private_key(signing_pem.encode("utf-8"), password=None)
            if isinstance(key, ec.EllipticCurvePrivateKey):
                self._signing_key = key

        self._x25519_key: X25519PrivateKey | None = None
        if x25519_pem is not None:
            key = load_pem_private_key(x25519_pem.encode("utf-8"), password=None)
            if isinstance(key, X25519PrivateKey):
                self._x25519_key = key

        self._key_manager = HpkeKeyManager()
        self._confirmed_session_ids: set[str] = set()

    async def initiate_handshake(
        self, peer_did: str
    ) -> tuple[str, dict[str, Any]]:
        """Initiate an E2EE session (one-step initialization).

        Retrieves the peer's X25519 public key from their DID document, then creates
        a session and sends e2ee_init. The session becomes ACTIVE immediately after
        sending, no response from the peer is needed.

        Args:
            peer_did: Peer DID identifier.

        Returns:
            ``(msg_type, content_dict)`` tuple, where msg_type is ``"e2ee_init"``.

        Raises:
            RuntimeError: Missing required keys or unable to retrieve peer DID document.
        """
        if self._signing_key is None or self._x25519_key is None:
            raise RuntimeError("Missing E2EE keys (signing_pem or x25519_pem), please recreate identity")

        # Retrieve peer DID document
        peer_doc = await resolve_did_wba_document(peer_did)
        if peer_doc is None:
            raise RuntimeError(f"Unable to retrieve peer DID document: {peer_did}")

        # Extract peer X25519 public key
        peer_pk, peer_key_id = extract_x25519_public_key_from_did_document(peer_doc)

        # Determine local signing verification method ID
        signing_vm = f"{self.local_did}#key-2"

        # Determine local X25519 key ID
        local_x25519_key_id = f"{self.local_did}#key-3"

        session = E2eeHpkeSession(
            local_did=self.local_did,
            peer_did=peer_did,
            local_x25519_private_key=self._x25519_key,
            local_x25519_key_id=local_x25519_key_id,
            signing_private_key=self._signing_key,
            signing_verification_method=signing_vm,
        )

        msg_type, content = session.initiate_session(peer_pk, peer_key_id)

        # One-step initialization: ACTIVE immediately after sending
        self._key_manager.register_session(session)

        return msg_type, content

    async def process_e2ee_message(
        self, msg_type: str, content: dict[str, Any]
    ) -> list[tuple[str, dict[str, Any]]]:
        """Process a received E2EE protocol message.

        Args:
            msg_type: Message type (``e2ee_init`` / ``e2ee_rekey`` / ``e2ee_error``).
            content: Message content dict.

        Returns:
            List of messages to send (in HPKE scheme, usually an empty list
            since init/rekey do not require a reply).
        """
        if msg_type == "e2ee_ack":
            return await self._handle_ack(content)

        detected = detect_message_type(msg_type)
        if detected is None:
            logger.warning("Unrecognized E2EE message type: %s", msg_type)
            return []

        if detected != MessageType.E2EE_ERROR:
            try:
                ensure_supported_e2ee_version(content)
            except ValueError as exc:
                logger.warning("Unsupported E2EE version for %s: %s", msg_type, exc)
                sender_did = content.get("sender_did")
                if sender_did:
                    return [(
                        "e2ee_error",
                        build_e2ee_error_content(
                            error_code="unsupported_version",
                            session_id=content.get("session_id"),
                            retry_hint="drop",
                            required_e2ee_version=SUPPORTED_E2EE_VERSION,
                            message=build_e2ee_error_message(
                                "unsupported_version",
                                required_e2ee_version=SUPPORTED_E2EE_VERSION,
                            ),
                        ),
                    )]
                return []

        if detected == MessageType.E2EE_INIT:
            return await self._handle_init(content)
        elif detected == MessageType.E2EE_REKEY:
            return await self._handle_rekey(content)
        elif detected == MessageType.E2EE_ERROR:
            return await self._handle_error(content)
        elif detected == MessageType.E2EE_MSG:
            logger.warning("process_e2ee_message does not handle encrypted messages, use decrypt_message instead")
            return []
        else:
            logger.warning("Unhandled E2EE message subtype: %s", detected)
            return []

    def has_active_session(self, peer_did: str) -> bool:
        """Check whether an active encryption session exists with the specified peer."""
        session = self._key_manager.get_active_session(self.local_did, peer_did)
        return session is not None

    def has_session_id(self, session_id: str | None) -> bool:
        """Check whether the specified session_id currently exists and is active."""
        if not session_id:
            return False
        return self._key_manager.get_session_by_id(session_id) is not None

    def is_session_confirmed(self, session_id: str | None) -> bool:
        """Check whether a session has been remotely confirmed via e2ee_ack."""
        if not session_id:
            return False
        return session_id in self._confirmed_session_ids

    async def ensure_active_session(
        self, peer_did: str
    ) -> list[tuple[str, dict[str, Any]]]:
        """Ensure an active session exists with the peer, auto-handshake if needed.

        If a valid session already exists, returns an empty list.
        If the session is missing or expired, initiates a new handshake and returns
        the handshake message(s) that must be sent to the peer.

        Args:
            peer_did: Peer DID identifier.

        Returns:
            List of ``(msg_type, content_dict)`` messages to send (empty if session
            is already active, ``[("e2ee_init", ...)]`` if a handshake was initiated).

        Raises:
            RuntimeError: Missing required keys or unable to retrieve peer DID document.
        """
        if self.has_active_session(peer_did):
            return []
        msg_type, content = await self.initiate_handshake(peer_did)
        logger.info("Auto-handshake initiated for expired/missing session: peer=%s", peer_did[:20])
        return [(msg_type, content)]

    def encrypt_message(
        self, peer_did: str, plaintext: str, original_type: str = "text"
    ) -> tuple[str, dict[str, Any]]:
        """Encrypt a message.

        Args:
            peer_did: Peer DID identifier.
            plaintext: Plaintext content.
            original_type: Original message type (default ``"text"``).

        Returns:
            ``(msg_type, content_dict)`` tuple, where msg_type is ``"e2ee_msg"``.

        Raises:
            RuntimeError: No active session with the peer.
        """
        session = self._key_manager.get_active_session(self.local_did, peer_did)
        if session is None:
            raise RuntimeError(f"No active E2EE session with {peer_did}")
        return session.encrypt_message(original_type, plaintext)

    def decrypt_message(self, content: dict[str, Any]) -> tuple[str, str]:
        """Decrypt a message.

        Finds the corresponding session by ``session_id`` and decrypts.

        Args:
            content: Encrypted message content dict (contains ``session_id``, ``ciphertext``, etc.).

        Returns:
            ``(original_type, plaintext)`` tuple.

        Raises:
            RuntimeError: Cannot find the corresponding session.
        """
        session_id = content.get("session_id")
        if not session_id:
            raise RuntimeError("Message missing session_id")

        ensure_supported_e2ee_version(content)

        session = self._key_manager.get_session_by_id(session_id)
        if session is None:
            raise RuntimeError(f"Cannot find session for session_id={session_id}")
        return session.decrypt_message(content)

    def cleanup_expired(self) -> None:
        """Clean up expired sessions."""
        self._key_manager.cleanup_expired()

    # ------------------------------------------------------------------
    # State export / restore
    # ------------------------------------------------------------------

    def export_state(self) -> dict[str, Any]:
        """Export client state (keys + ACTIVE sessions).

        Returns:
            JSON-serializable dict for persistence.
        """
        sessions: list[dict[str, Any]] = []
        for session in self._key_manager._sessions_by_did_pair.values():
            if session.state == SessionState.ACTIVE and not session.is_expired():
                exported = self._export_session(session)
                if exported is not None:
                    sessions.append(exported)
        return {
            "version": _STATE_VERSION,
            "local_did": self.local_did,
            "signing_pem": self._signing_pem,
            "x25519_pem": self._x25519_pem,
            "confirmed_session_ids": sorted(self._confirmed_session_ids),
            "sessions": sessions,
        }

    @classmethod
    def from_state(cls, state: dict[str, Any]) -> E2eeClient:
        """Restore a complete client from an exported dict.

        Args:
            state: Dict generated by ``export_state()``.

        Returns:
            Restored ``E2eeClient`` instance.
        """
        # Detect old format: no version marker or version mismatch
        if state.get("version") != _STATE_VERSION:
            logger.info("Detected old E2EE state format, creating new client")
            return cls(
                state["local_did"],
                signing_pem=state.get("signing_pem"),
                x25519_pem=state.get("x25519_pem"),
            )

        client = cls(
            state["local_did"],
            signing_pem=state.get("signing_pem"),
            x25519_pem=state.get("x25519_pem"),
        )
        for session_data in state.get("sessions", []):
            session = cls._restore_session(session_data)
            if session is not None:
                client._key_manager.register_session(session)
        client._confirmed_session_ids = set(state.get("confirmed_session_ids", []))
        return client

    def _build_ack_content(
        self,
        *,
        session_id: str,
        recipient_did: str,
        expires: int = 86400,
    ) -> dict[str, Any]:
        """Build a signed e2ee_ack payload for an accepted session."""
        if self._signing_key is None:
            raise RuntimeError("Missing E2EE signing key for ack")
        content = {
            "e2ee_version": SUPPORTED_E2EE_VERSION,
            "session_id": session_id,
            "sender_did": self.local_did,
            "recipient_did": recipient_did,
            "expires": expires,
        }
        return generate_proof(content, self._signing_key, f"{self.local_did}#key-2")

    @staticmethod
    def _export_session(session: E2eeHpkeSession) -> dict[str, Any] | None:
        """Serialize a single ACTIVE session."""
        if session.state != SessionState.ACTIVE:
            return None
        send_chain_key = session._send_chain_key
        recv_chain_key = session._recv_chain_key
        if send_chain_key is None or recv_chain_key is None:
            return None
        return {
            "session_id": session.session_id,
            "local_did": session.local_did,
            "peer_did": session.peer_did,
            "is_initiator": session._is_initiator,
            "send_chain_key": base64.b64encode(send_chain_key).decode("ascii"),
            "recv_chain_key": base64.b64encode(recv_chain_key).decode("ascii"),
            "send_seq": session._seq_manager._send_seq,
            "recv_seq": session._seq_manager._recv_seq,
            "expires_at": session._expires_at,
            "created_at": session._created_at,
            "active_at": session._active_at,
        }

    @staticmethod
    def _restore_session(data: dict[str, Any]) -> E2eeHpkeSession | None:
        """Restore a single ACTIVE session from a dict.

        Uses ``object.__new__()`` to bypass ``__init__`` and directly set internal attributes.
        """
        expires_at = data.get("expires_at")
        if expires_at is not None and time.time() > expires_at:
            return None

        session = object.__new__(E2eeHpkeSession)
        session.local_did = data["local_did"]
        session.peer_did = data["peer_did"]
        session._session_id = data["session_id"]
        session._state = SessionState.ACTIVE
        session._is_initiator = data.get("is_initiator", True)
        session._send_chain_key = base64.b64decode(data["send_chain_key"])
        session._recv_chain_key = base64.b64decode(data["recv_chain_key"])
        session._expires_at = expires_at
        session._created_at = data.get("created_at", time.time())
        session._active_at = data.get("active_at")

        # Restore SeqManager
        from anp.e2e_encryption_hpke.session import SeqManager, SeqMode
        seq_mgr = object.__new__(SeqManager)
        seq_mgr._mode = SeqMode.STRICT
        seq_mgr._send_seq = data.get("send_seq", 0)
        seq_mgr._recv_seq = data.get("recv_seq", 0)
        seq_mgr._max_skip = 256
        seq_mgr._used_seqs = {}
        seq_mgr._skip_key_ttl = 300
        session._seq_manager = seq_mgr

        # Attributes not needed in ACTIVE state, set to None to prevent AttributeError
        session._local_x25519_private_key = None
        session._local_x25519_key_id = ""
        session._signing_private_key = None
        session._signing_verification_method = ""
        session._default_expires = data.get("expires_at", 86400)

        return session

    # ------------------------------------------------------------------
    # Internal handler methods
    # ------------------------------------------------------------------

    async def _handle_init(
        self, content: dict[str, Any]
    ) -> list[tuple[str, dict[str, Any]]]:
        """Handle e2ee_init: retrieve sender DID document to verify proof, create and activate session."""
        if self._signing_key is None or self._x25519_key is None:
            logger.error("Missing E2EE keys, cannot process e2ee_init")
            return []

        sender_did = content.get("sender_did", "")
        if not sender_did:
            logger.warning("e2ee_init message missing sender_did")
            return []

        # Retrieve sender DID document
        sender_doc = await resolve_did_wba_document(sender_did)
        if sender_doc is None:
            logger.warning("Unable to retrieve sender DID document: %s", sender_did)
            return []

        # Extract sender signing public key (for proof verification)
        proof = content.get("proof", {})
        vm_id = _extract_proof_verification_method(proof)
        try:
            sender_signing_pk = extract_signing_public_key_from_did_document(
                sender_doc, vm_id
            )
        except ValueError as e:
            logger.warning("Unable to extract sender signing public key: %s", e)
            return []

        # Determine local key IDs
        signing_vm = f"{self.local_did}#key-2"
        local_x25519_key_id = f"{self.local_did}#key-3"

        session = E2eeHpkeSession(
            local_did=self.local_did,
            peer_did=sender_did,
            local_x25519_private_key=self._x25519_key,
            local_x25519_key_id=local_x25519_key_id,
            signing_private_key=self._signing_key,
            signing_verification_method=signing_vm,
        )

        try:
            session.process_init(content, sender_signing_pk)
        except (ValueError, RuntimeError) as e:
            logger.warning("Failed to process e2ee_init: %s", e)
            classified = _classify_protocol_error(e)
            if classified is None:
                return []
            error_code, retry_hint = classified
            return [(
                "e2ee_error",
                build_e2ee_error_content(
                    error_code=error_code,
                    session_id=content.get("session_id"),
                    retry_hint=retry_hint,
                    required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                    message=build_e2ee_error_message(
                        error_code,
                        required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                        detail=str(e),
                    ),
                ),
            )]

        # Register session (immediately ACTIVE)
        self._key_manager.register_session(session)
        logger.info(
            "E2EE session activated (receiver): %s <-> %s (session_id=%s)",
            session.local_did, session.peer_did, session.session_id,
        )

        ack_content = self._build_ack_content(
            session_id=session.session_id or content.get("session_id", ""),
            recipient_did=sender_did,
            expires=int(content.get("expires", 86400)),
        )
        self._confirmed_session_ids.add(session.session_id or content.get("session_id", ""))
        return [("e2ee_ack", ack_content)]

    async def _handle_rekey(
        self, content: dict[str, Any]
    ) -> list[tuple[str, dict[str, Any]]]:
        """Handle e2ee_rekey: rebuild session."""
        if self._signing_key is None or self._x25519_key is None:
            logger.error("Missing E2EE keys, cannot process e2ee_rekey")
            return []

        sender_did = content.get("sender_did", "")
        if not sender_did:
            logger.warning("e2ee_rekey message missing sender_did")
            return []

        # Retrieve sender DID document
        sender_doc = await resolve_did_wba_document(sender_did)
        if sender_doc is None:
            logger.warning("Unable to retrieve sender DID document: %s", sender_did)
            return []

        # Extract sender signing public key
        proof = content.get("proof", {})
        vm_id = _extract_proof_verification_method(proof)
        try:
            sender_signing_pk = extract_signing_public_key_from_did_document(
                sender_doc, vm_id
            )
        except ValueError as e:
            logger.warning("Unable to extract sender signing public key: %s", e)
            return []

        signing_vm = f"{self.local_did}#key-2"
        local_x25519_key_id = f"{self.local_did}#key-3"

        # Try to get existing session for rekey
        session = self._key_manager.get_active_session(self.local_did, sender_did)
        if session is not None:
            try:
                session.process_rekey(content, sender_signing_pk)
                self._key_manager.register_session(session)
                logger.info(
                    "E2EE session rekey successful: %s <-> %s", self.local_did, sender_did
                )
                ack_content = self._build_ack_content(
                    session_id=session.session_id or content.get("session_id", ""),
                    recipient_did=sender_did,
                    expires=int(content.get("expires", 86400)),
                )
                self._confirmed_session_ids.add(session.session_id or content.get("session_id", ""))
                return [("e2ee_ack", ack_content)]
            except (ValueError, RuntimeError) as e:
                logger.warning("Rekey of existing session failed, attempting to create new session: %s", e)

        # No existing session or rekey failed, create new session
        session = E2eeHpkeSession(
            local_did=self.local_did,
            peer_did=sender_did,
            local_x25519_private_key=self._x25519_key,
            local_x25519_key_id=local_x25519_key_id,
            signing_private_key=self._signing_key,
            signing_verification_method=signing_vm,
        )
        try:
            session.process_rekey(content, sender_signing_pk)
        except (ValueError, RuntimeError) as e:
            logger.warning("Failed to process e2ee_rekey: %s", e)
            classified = _classify_protocol_error(e)
            if classified is None:
                return []
            error_code, retry_hint = classified
            return [(
                "e2ee_error",
                build_e2ee_error_content(
                    error_code=error_code,
                    session_id=content.get("session_id"),
                    retry_hint=retry_hint,
                    required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                    message=build_e2ee_error_message(
                        error_code,
                        required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                        detail=str(e),
                    ),
                ),
            )]

        self._key_manager.register_session(session)
        logger.info(
            "E2EE session rekey (new): %s <-> %s", self.local_did, sender_did
        )
        ack_content = self._build_ack_content(
            session_id=session.session_id or content.get("session_id", ""),
            recipient_did=sender_did,
            expires=int(content.get("expires", 86400)),
        )
        self._confirmed_session_ids.add(session.session_id or content.get("session_id", ""))
        return [("e2ee_ack", ack_content)]

    async def _handle_ack(
        self, content: dict[str, Any]
    ) -> list[tuple[str, dict[str, Any]]]:
        """Handle e2ee_ack: verify proof and mark the session as confirmed."""
        ensure_supported_e2ee_version(content)

        session_id = content.get("session_id", "")
        sender_did = content.get("sender_did", "")
        recipient_did = content.get("recipient_did", "")
        if not session_id or not sender_did:
            logger.warning("e2ee_ack missing session_id or sender_did")
            return []
        if recipient_did and recipient_did != self.local_did:
            logger.warning("e2ee_ack recipient mismatch: expected=%s got=%s", self.local_did, recipient_did)
            return []

        sender_doc = await resolve_did_wba_document(sender_did)
        if sender_doc is None:
            logger.warning("Unable to retrieve ack sender DID document: %s", sender_did)
            return []

        proof = content.get("proof", {})
        vm_id = _extract_proof_verification_method(proof)
        try:
            sender_signing_pk = extract_signing_public_key_from_did_document(
                sender_doc, vm_id
            )
            validate_proof(
                content,
                sender_signing_pk,
                max_past_age_seconds=int(content.get("expires", 86400)),
            )
        except Exception as exc:
            logger.warning("Failed to verify e2ee_ack: %s", exc)
            return []

        session = self._key_manager.get_session_by_id(session_id)
        if session is None:
            logger.warning("Received e2ee_ack for unknown session_id=%s", session_id)
            return []
        if session.peer_did != sender_did:
            logger.warning("Received e2ee_ack from unexpected peer: %s", sender_did)
            return []

        self._confirmed_session_ids.add(session_id)
        logger.info("E2EE session confirmed by peer: %s", session_id)
        return []

    async def _handle_error(
        self, content: dict[str, Any]
    ) -> list[tuple[str, dict[str, Any]]]:
        """Handle E2EE Error: log, remove the corresponding session, and auto re-handshake for recoverable errors."""
        try:
            ensure_supported_e2ee_version(content)
        except ValueError as exc:
            logger.warning("Ignoring legacy e2ee_error without supported version: %s", exc)
            return []

        error_code = content.get("error_code", "unknown")
        session_id = content.get("session_id", "")
        logger.warning(
            "Received E2EE error: code=%s, session_id=%s", error_code, session_id
        )
        peer_did: str | None = None
        if session_id:
            session = self._key_manager.get_session_by_id(session_id)
            if session is not None:
                peer_did = session.peer_did
                self._key_manager.remove_session(session.local_did, session.peer_did)

        # Auto re-handshake for recoverable errors
        _recoverable = {"session_not_found", "session_expired", "decryption_failed"}
        if peer_did is None:
            sender_did = content.get("sender_did", "")
            if isinstance(sender_did, str) and sender_did:
                peer_did = sender_did
                logger.info(
                    "E2EE error fallback using sender_did for re-handshake: %s",
                    sender_did[:20],
                )
        if error_code in _recoverable and peer_did is not None:
            try:
                msg_type, init_content = await self.initiate_handshake(peer_did)
                logger.info(
                    "Auto re-handshake initiated after E2EE error: peer=%s", peer_did[:20]
                )
                return [(msg_type, init_content)]
            except Exception:
                logger.exception("Auto re-handshake failed: peer=%s", peer_did)
        return []


__all__ = [
    "E2eeClient",
    "SUPPORTED_E2EE_VERSION",
    "ensure_supported_e2ee_version",
    "build_e2ee_error_content",
    "build_e2ee_error_message",
]
