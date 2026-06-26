"""E2EE end-to-end encrypted messaging (HPKE scheme, with cross-process state persistence).

Usage:
    # Send an encrypted message (normal path; auto-initializes the session if needed)
    uv run python scripts/e2ee_messaging.py --send "did:wba:awiki.ai:user:abc123" --content "secret message"

    # Optional advanced mode: pre-initialize an E2EE session explicitly
    uv run python scripts/e2ee_messaging.py --handshake "did:wba:awiki.ai:user:abc123"

    # Process E2EE messages in inbox (auto-handle init + decrypt)
    uv run python scripts/e2ee_messaging.py --process --peer "did:wba:awiki.ai:user:abc123"

Supported workflows:
1. Alice: --send <Bob's DID> --content "secret" -> Auto-init session if needed, then send encrypted message
2. Bob:   --process --peer <Alice's DID>        -> Process inbox, accept e2ee_init, then decrypt message
3. Optional advanced: --handshake <Bob's DID>   -> Pre-warm a session for debugging or recovery

[INPUT]: SDK (E2eeClient, RPC calls), credential_store (authenticated identity
         loading), SQLite-backed E2EE session store, logging_config
[OUTPUT]: E2EE operation results with failure-aware inbox processing, sender-facing
          e2ee_error notifications, and disk-first session persistence
[POS]: End-to-end encrypted messaging script, integrates SQLite-backed session
       persistence for cross-process E2EE communication (HPKE scheme)

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys
import uuid
from typing import Any

from utils import SDKConfig, E2eeClient, create_molt_message_client, authenticated_rpc_call, resolve_to_did
from utils.e2ee import (
    SUPPORTED_E2EE_VERSION,
    build_e2ee_error_content,
    build_e2ee_error_message,
)
from utils.logging_config import configure_logging
from credential_store import create_authenticator
from e2ee_session_store import (
    E2eeStateTransaction,
    load_e2ee_client,
    save_e2ee_client,
)
from message_transport import is_websocket_mode, message_rpc_call
from e2ee_outbox import (
    begin_send_attempt,
    get_record,
    list_failed_records,
    mark_dropped,
    record_local_failure,
    mark_send_success,
    record_remote_failure,
)


MESSAGE_RPC = "/message/rpc"
logger = logging.getLogger(__name__)

# E2EE related message types
_E2EE_MSG_TYPES = {"e2ee_init", "e2ee_ack", "e2ee_msg", "e2ee_rekey", "e2ee_error"}
_E2EE_SESSION_SETUP_TYPES = {"e2ee_init", "e2ee_rekey"}
_E2EE_USER_NOTICE = "This is an encrypted message."

# E2EE message type protocol order
_E2EE_TYPE_ORDER = {"e2ee_init": 0, "e2ee_ack": 1, "e2ee_rekey": 2, "e2ee_msg": 3, "e2ee_error": 4}


def _message_time_value(message: dict[str, Any]) -> str:
    """Return a sortable timestamp string for one message."""
    timestamp = message.get("sent_at") or message.get("created_at")
    return timestamp if isinstance(timestamp, str) else ""


def _sender_did_value(message: dict[str, Any], fallback: str = "?") -> str:
    """Return a safe sender DID string for logging and user-facing output."""
    sender_did = message.get("sender_did")
    return sender_did if isinstance(sender_did, str) and sender_did else fallback


def _message_sort_key(message: dict[str, Any]) -> tuple[Any, ...]:
    """Build a stable inbox ordering key with server_seq priority inside a sender stream."""
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


def _render_user_visible_e2ee_text(plaintext: str) -> str:
    """Render the minimal user-facing text for a decrypted E2EE message."""
    return f"{_E2EE_USER_NOTICE}\n{plaintext}"


def _render_auto_session_notice(peer_did: str) -> str:
    """Render the user-facing notice for the send-first auto-init flow."""
    return (
        "No active E2EE session found; sent automatic init before the encrypted payload. "
        f"Peer: {peer_did}"
    )


def _classify_decrypt_error(exc: BaseException) -> tuple[str, str]:
    """Map decryption failures to e2ee_error code and retry hint."""
    msg = str(exc).lower()
    if "unsupported_version" in msg:
        return "unsupported_version", "drop"
    if "session" in msg and "not found" in msg:
        return "session_not_found", "rekey_then_resend"
    if "expired" in msg:
        return "session_expired", "rekey_then_resend"
    if "seq" in msg or "sequence" in msg:
        return "invalid_seq", "rekey_then_resend"
    return "decryption_failed", "resend"


def _load_or_create_e2ee_client(
    local_did: str, credential_name: str
) -> E2eeClient:
    """Load the latest disk-first E2EE client state from SQLite."""
    client = load_e2ee_client(local_did, credential_name)
    if client._signing_key is None or client._x25519_key is None:  # noqa: SLF001
        print("Warning: Credential missing E2EE keys (key-2/key-3); please recreate identity to enable HPKE E2EE")
    return client


def _save_e2ee_client(client: E2eeClient, credential_name: str) -> None:
    """Persist the latest E2EE client state into SQLite."""
    save_e2ee_client(client, credential_name)


async def _send_msg(
    client,
    sender_did,
    receiver_did,
    msg_type,
    content,
    *,
    auth,
    credential_name="default",
    client_msg_id: str | None = None,
    title: str | None = None,
):
    """Send a message (E2EE or plain)."""
    if isinstance(content, dict):
        content = json.dumps(content)
    if client_msg_id is None:
        client_msg_id = str(uuid.uuid4())
    params = {
        "sender_did": sender_did,
        "receiver_did": receiver_did,
        "content": content,
        "type": msg_type,
        "client_msg_id": client_msg_id,
    }
    if title is not None:
        params["title"] = title
    if client is None:
        return await message_rpc_call(
            "send",
            params=params,
            credential_name=credential_name,
        )
    return await authenticated_rpc_call(
        client, MESSAGE_RPC, "send",
        params=params,
        auth=auth,
        credential_name=credential_name,
    )


async def initiate_handshake(
    peer_did: str,
    credential_name: str = "default",
) -> None:
    """Manually initiate an E2EE session (advanced/manual path)."""
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, data = auth_result
    with E2eeStateTransaction(data["did"], credential_name) as state_tx:
        e2ee_client = state_tx.client
        msg_type, content = await e2ee_client.initiate_handshake(peer_did)

        if is_websocket_mode(config):
            await _send_msg(
                None,
                data["did"],
                peer_did,
                msg_type,
                content,
                auth=auth,
                credential_name=credential_name,
            )
        else:
            async with create_molt_message_client(config) as client:
                await _send_msg(
                    client,
                    data["did"],
                    peer_did,
                    msg_type,
                    content,
                    auth=auth,
                    credential_name=credential_name,
                )

        state_tx.commit()

    print("E2EE session established (one-step initialization)")
    print(f"  session_id: {content.get('session_id')}")
    print(f"  peer_did  : {peer_did}")
    print("Session is ACTIVE; you can send encrypted messages now")
    print("Tip: --send auto-initializes a session when needed; manual handshake is mainly for debugging or pre-warming.")


async def send_encrypted(
    peer_did: str,
    plaintext: str,
    credential_name: str = "default",
    original_type: str = "text",
    outbox_id: str | None = None,
    title: str | None = None,
) -> None:
    """Send an encrypted message through the normal send-first flow."""
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, data = auth_result
    client = None
    if not is_websocket_mode(config):
        client = await create_molt_message_client(config).__aenter__()
    try:
        with E2eeStateTransaction(data["did"], credential_name) as state_tx:
            e2ee_client = state_tx.client

            # Auto-handshake if session is missing or expired
            init_msgs = await e2ee_client.ensure_active_session(peer_did)
            enc_type, enc_content = e2ee_client.encrypt_message(
                peer_did,
                plaintext,
                original_type,
            )
            session_id = enc_content.get("session_id")
            state_tx.commit()

        if init_msgs:
            print(_render_auto_session_notice(peer_did))
        for init_type, init_content in init_msgs:
            await _send_msg(
                client,
                data["did"],
                peer_did,
                init_type,
                init_content,
                auth=auth,
                credential_name=credential_name,
            )

        outbox_id = begin_send_attempt(
            peer_did=peer_did,
            plaintext=plaintext,
            original_type=original_type,
            credential_name=credential_name,
            session_id=session_id,
            outbox_id=outbox_id,
        )
        send_client_msg_id = str(uuid.uuid4())
        try:
            send_result = await _send_msg(
                client,
                data["did"],
                peer_did,
                enc_type,
                enc_content,
                auth=auth,
                credential_name=credential_name,
                client_msg_id=send_client_msg_id,
                title=title,
            )
        except Exception as exc:
            record_local_failure(
                outbox_id=outbox_id,
                credential_name=credential_name,
                error_code="send_request_failed",
                retry_hint="resend",
                metadata=json.dumps({"error": str(exc)}, ensure_ascii=False),
            )
            print(f"Encrypted message send failed; outbox_id={outbox_id}")
            raise

        mark_send_success(
            outbox_id=outbox_id,
            credential_name=credential_name,
            local_did=data["did"],
            peer_did=peer_did,
            plaintext=plaintext,
            original_type=original_type,
            session_id=session_id,
            sent_msg_id=send_result.get("id"),
            sent_server_seq=send_result.get("server_seq"),
            sent_at=send_result.get("sent_at"),
            client_msg_id=send_client_msg_id,
            title=title,
        )
    finally:
        if client is not None:
            await client.__aexit__(None, None, None)
    print("Encrypted message sent")
    print(f"  Plaintext: {plaintext}")
    print(f"  Receiver : {peer_did}")
    print(f"  Outbox ID: {outbox_id}")


async def process_inbox(
    peer_did: str,
    credential_name: str = "default",
) -> None:
    """Process E2EE messages in inbox."""
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)
    if is_websocket_mode(config):
        print(
            "WebSocket receive mode is enabled; the background listener owns E2EE inbox processing. "
            "Use check_status/check_inbox or switch to HTTP mode for manual --process."
        )
        sys.exit(1)

    auth, data = auth_result
    async with create_molt_message_client(config) as client:
        # Get inbox
        inbox = await authenticated_rpc_call(
            client, MESSAGE_RPC, "get_inbox",
            params={"user_did": data["did"], "limit": 50},
            auth=auth, credential_name=credential_name,
        )
        messages = inbox.get("messages", [])
        if not messages:
            print("Inbox is empty")
            return

        # Sort by sender stream + server_seq, fallback to created_at.
        messages.sort(key=_message_sort_key)

        e2ee_client: E2eeClient | None = None

        # Try to restore existing E2EE client from disk
        e2ee_client = _load_or_create_e2ee_client(data["did"], credential_name)
        processed_ids = []

        for msg in messages:
            msg_type = msg["type"]
            sender_did = _sender_did_value(msg)
            processed_ok = False

            if msg_type in _E2EE_MSG_TYPES:
                content = json.loads(msg["content"])

                if msg_type == "e2ee_msg":
                    try:
                        original_type, plaintext = e2ee_client.decrypt_message(content)
                        logger.info(
                            "Decrypted E2EE inbox message sender=%s original_type=%s",
                            sender_did,
                            original_type,
                        )
                        print(_render_user_visible_e2ee_text(plaintext))
                        processed_ok = True
                    except Exception as e:
                        logger.warning(
                            "Failed to decrypt E2EE inbox message sender=%s error=%s",
                            sender_did,
                            e,
                        )
                        error_code, retry_hint = _classify_decrypt_error(e)
                        error_content = build_e2ee_error_content(
                            error_code=error_code,
                            session_id=content.get("session_id"),
                            failed_msg_id=msg.get("id"),
                            failed_server_seq=msg.get("server_seq"),
                            retry_hint=retry_hint,
                            required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                            message=build_e2ee_error_message(
                                error_code,
                                required_e2ee_version=SUPPORTED_E2EE_VERSION if error_code == "unsupported_version" else None,
                                detail=str(e),
                            ),
                        )
                        await _send_msg(
                            client, data["did"], sender_did, "e2ee_error", error_content,
                            auth=auth, credential_name=credential_name,
                        )
                else:
                    if msg_type == "e2ee_error":
                        matched_outbox_id = record_remote_failure(
                            credential_name=credential_name,
                            peer_did=sender_did,
                            content=content,
                        )
                        if matched_outbox_id:
                            logger.info(
                                "Matched failed E2EE outbox sender=%s outbox_id=%s",
                                sender_did,
                                matched_outbox_id,
                            )
                    responses = await e2ee_client.process_e2ee_message(msg_type, content)
                    session_ready = True
                    terminal_error_notified = any(
                        resp_type == "e2ee_error" for resp_type, _ in responses
                    )
                    if msg_type in _E2EE_SESSION_SETUP_TYPES:
                        session_ready = e2ee_client.has_session_id(content.get("session_id"))
                    logger.info(
                        "Processed E2EE protocol message type=%s sender=%s responses=%d session_ready=%s terminal_error_notified=%s",
                        msg_type,
                        sender_did,
                        len(responses),
                        session_ready,
                        terminal_error_notified,
                    )
                    if session_ready:
                        processed_ok = True
                    elif terminal_error_notified:
                        processed_ok = True
                    for resp_type, resp_content in responses:
                        await _send_msg(
                            client, data["did"], peer_did, resp_type, resp_content,
                            auth=auth, credential_name=credential_name,
                        )
            else:
                print(f"  [{msg_type}] From {sender_did[:40]}...: {msg['content']}")
                processed_ok = True

            if processed_ok:
                processed_ids.append(msg["id"])

        # Mark as read
        if processed_ids:
            await authenticated_rpc_call(
                client, MESSAGE_RPC, "mark_read",
                params={"user_did": data["did"], "message_ids": processed_ids},
                auth=auth, credential_name=credential_name,
            )
            logger.info("Marked %d E2EE inbox message(s) as read", len(processed_ids))

        # Save E2EE client state to disk
        if e2ee_client is not None:
            _save_e2ee_client(e2ee_client, credential_name)


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(
        description=(
            "E2EE end-to-end encrypted messaging (normal path: --send "
            "auto-initializes the session if needed)"
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--handshake",
        type=str,
        help="Optional advanced mode: pre-initialize an E2EE session with a specific DID or handle",
    )
    group.add_argument(
        "--send",
        type=str,
        help="Send encrypted message and auto-initialize or rekey the E2EE session if needed",
    )
    group.add_argument("--process", action="store_true",
                       help="Process E2EE messages in inbox manually (recovery/debug path)")
    group.add_argument("--list-failed", action="store_true",
                       help="List failed local E2EE outbox records")
    group.add_argument("--retry", type=str,
                       help="Retry a failed local E2EE outbox record by outbox_id")
    group.add_argument("--drop", type=str,
                       help="Mark a failed local E2EE outbox record as dropped")

    parser.add_argument("--content", type=str, help="Message content (required with --send)")
    parser.add_argument("--title", type=str, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--peer", type=str,
                        help="Peer DID or handle (required with --process)")
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")

    args = parser.parse_args()
    logger.info(
        "e2ee_messaging CLI started credential=%s action=%s",
        args.credential,
        (
            "handshake" if args.handshake else
            "send" if args.send else
            "process" if args.process else
            "list_failed" if args.list_failed else
            "retry" if args.retry else
            "drop"
        ),
    )

    if args.handshake:
        peer_did = asyncio.run(resolve_to_did(args.handshake))
        asyncio.run(initiate_handshake(peer_did, args.credential))
    elif args.send:
        if not args.content:
            parser.error("Sending encrypted message requires --content")
        peer_did = asyncio.run(resolve_to_did(args.send))
        asyncio.run(send_encrypted(peer_did, args.content, args.credential, title=args.title))
    elif args.process:
        if not args.peer:
            parser.error("Processing inbox requires --peer")
        peer_did = asyncio.run(resolve_to_did(args.peer))
        asyncio.run(process_inbox(peer_did, args.credential))
    elif args.list_failed:
        records = list_failed_records(args.credential)
        print(json.dumps(records, indent=2, ensure_ascii=False))
    elif args.retry:
        record = get_record(args.retry, args.credential)
        if record is None:
            parser.error(f"Outbox record '{args.retry}' not found")
        asyncio.run(
            send_encrypted(
                record["peer_did"],
                record["plaintext"],
                args.credential,
                original_type=record.get("original_type") or "text",
                outbox_id=record["outbox_id"],
            )
        )
    elif args.drop:
        mark_dropped(args.drop, args.credential)
        print(f"Dropped outbox record: {args.drop}")


if __name__ == "__main__":
    main()
