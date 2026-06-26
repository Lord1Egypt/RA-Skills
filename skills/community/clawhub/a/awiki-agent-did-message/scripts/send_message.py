"""Send a message to a specified DID.

Usage:
    # Send a text message
    uv run python scripts/send_message.py --to "did:wba:localhost:user:abc123" --content "Hello!"

    # Specify message type
    uv run python scripts/send_message.py --to "did:wba:localhost:user:abc123" --content "hello" --type text

[INPUT]: SDK (RPC calls), credential_store (load identity credentials),
         local_store (local persistence), logging_config
[OUTPUT]: Send result (with server_seq and client_msg_id) plus local contact/event updates
[POS]: Message sending script, auto-generates client_msg_id for idempotent delivery.

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

from utils import SDKConfig, resolve_to_did
from utils.logging_config import configure_logging
from credential_store import create_authenticator
from message_transport import message_rpc_call
import local_store


MESSAGE_RPC = "/message/rpc"
logger = logging.getLogger(__name__)


def _strip_hidden_result_fields(result: dict[str, object]) -> dict[str, object]:
    """Remove fields intentionally hidden from user-facing CLI output."""
    rendered = dict(result)
    rendered.pop("title", None)
    return rendered


async def send_message(
    receiver: str,
    content: str,
    msg_type: str = "text",
    credential_name: str = "default",
    title: str | None = None,
) -> None:
    """Send a message to a specified DID or handle."""
    config = SDKConfig()
    receiver_did = await resolve_to_did(receiver, config)
    logger.info(
        "Sending message credential=%s receiver=%s resolved_receiver=%s type=%s content_length=%d",
        credential_name,
        receiver,
        receiver_did,
        msg_type,
        len(content),
    )
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    _auth, data = auth_result
    result = await message_rpc_call(
        "send",
        params={
            k: v for k, v in {
                "sender_did": data["did"],
                "receiver_did": receiver_did,
                "content": content,
                "title": title,
                "type": msg_type,
                "client_msg_id": str(uuid.uuid4()),
            }.items() if v is not None
        },
        credential_name=credential_name,
        config=config,
    )

    # Store sent message locally
    try:
        conn = local_store.get_connection()
        local_store.ensure_schema(conn)
        local_store.store_message(
            conn,
            msg_id=result.get("id", str(uuid.uuid4())),
            owner_did=data["did"],
            thread_id=local_store.make_thread_id(
                data["did"], peer_did=receiver_did,
            ),
            direction=1,
            sender_did=data["did"],
            receiver_did=receiver_did,
            content_type=msg_type,
            content=content,
            title=title,
            server_seq=result.get("server_seq"),
            sent_at=result.get("sent_at"),
            credential_name=credential_name,
        )
        # Record receiver in contacts
        contact_fields = {}
        if receiver != receiver_did:
            contact_fields["handle"] = receiver
        local_store.upsert_contact(
            conn,
            owner_did=data["did"],
            did=receiver_did,
            messaged=True,
            **contact_fields,
        )
        local_store.append_relationship_event(
            conn,
            owner_did=data["did"],
            target_did=receiver_did,
            target_handle=receiver if receiver != receiver_did else None,
            event_type="messaged",
            status="applied",
            credential_name=credential_name,
        )
        conn.close()
    except Exception:
        logger.debug("Failed to persist sent message locally", exc_info=True)

    print("Message sent successfully:", file=sys.stderr)
    print(json.dumps(_strip_hidden_result_fields(result), indent=2, ensure_ascii=False))
    logger.info(
        "Message sent credential=%s msg_id=%s server_seq=%s",
        credential_name,
        result.get("id"),
        result.get("server_seq"),
    )


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Send DID message")
    parser.add_argument("--to", required=True, type=str, help="Receiver DID or handle")
    parser.add_argument("--content", required=True, type=str, help="Message content")
    parser.add_argument("--type", type=str, default="text",
                        help="Message type (default: text)")
    parser.add_argument("--title", type=str, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")

    args = parser.parse_args()
    logger.info(
        "send_message CLI started credential=%s receiver=%s type=%s",
        args.credential,
        args.to,
        args.type,
    )
    asyncio.run(send_message(args.to, args.content, args.type, args.credential, title=args.title))


if __name__ == "__main__":
    main()
