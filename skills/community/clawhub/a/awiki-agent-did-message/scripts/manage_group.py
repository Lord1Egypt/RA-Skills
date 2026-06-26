"""Manage AWiki groups.

Usage:
    # Create a group
    uv run python scripts/manage_group.py --create --name "OpenClaw Meetup" --slug "openclaw-meetup"

    # Join with the global 6-digit join-code
    uv run python scripts/manage_group.py --join --join-code 314159

    # View members
    uv run python scripts/manage_group.py --members --group-id GROUP_ID

[INPUT]: SDK group RPC calls, credential_store authenticator, local_store SQLite cache,
         public markdown URLs, logging_config
[OUTPUT]: Group operation results, local group/message persistence,
          and public markdown fetches with local X-Handle fallback
[POS]: Group management CLI

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from typing import Any
from urllib.parse import urlparse

import httpx
import local_store
from utils import (
    SDKConfig,
    JsonRpcError,
    authenticated_rpc_call,
    create_user_service_client,
)
from utils.logging_config import configure_logging
from credential_store import create_authenticator


GROUP_RPC_ENDPOINT = "/group/rpc"
logger = logging.getLogger(__name__)
_JOIN_GUIDANCE = "Groups can only be joined with the global 6-digit join-code. Use --join --join-code <code>."


def _get_identity_data_or_exit(credential_name: str, config: SDKConfig) -> dict[str, Any]:
    """Return persisted local identity data for the active credential."""
    _auth, data = _get_authenticator_or_exit(credential_name, config)
    return data


def _persist_group_snapshot(
    *,
    credential_name: str,
    identity_data: dict[str, Any],
    group_payload: dict[str, Any],
    my_role: str | None = None,
    membership_status: str | None = None,
    last_synced_seq: int | None = None,
    last_message_at: str | None = None,
) -> None:
    """Persist a local snapshot of one group."""
    group_id = str(group_payload.get("group_id") or "")
    if not group_id:
        return

    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.upsert_group(
            conn,
            owner_did=str(identity_data.get("did") or ""),
            group_id=group_id,
            group_did=group_payload.get("group_did"),
            name=group_payload.get("name"),
            group_mode=group_payload.get("group_mode") or "general",
            slug=group_payload.get("slug"),
            description=group_payload.get("description"),
            goal=group_payload.get("goal"),
            rules=group_payload.get("rules"),
            message_prompt=group_payload.get("message_prompt"),
            doc_url=group_payload.get("doc_url"),
            group_owner_did=group_payload.get("owner_did"),
            group_owner_handle=group_payload.get("owner_handle"),
            my_role=my_role,
            membership_status=membership_status,
            join_enabled=group_payload.get("join_enabled"),
            join_code=group_payload.get("join_code"),
            join_code_expires_at=group_payload.get("join_code_expires_at"),
            member_count=group_payload.get("member_count"),
            last_synced_seq=last_synced_seq,
            last_message_at=last_message_at,
            remote_created_at=group_payload.get("created_at"),
            remote_updated_at=group_payload.get("updated_at"),
            metadata=group_payload.get("metadata"),
            credential_name=credential_name,
        )
    finally:
        conn.close()


def _persist_group_member_snapshot(
    *,
    credential_name: str,
    identity_data: dict[str, Any],
    group_id: str,
    members: list[dict[str, Any]],
) -> None:
    """Replace the cached active-member snapshot for one group."""
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.replace_group_members(
            conn,
            owner_did=str(identity_data.get("did") or ""),
            group_id=group_id,
            members=members,
            credential_name=credential_name,
        )
        local_store.upsert_group(
            conn,
            owner_did=str(identity_data.get("did") or ""),
            group_id=group_id,
            member_count=len(members),
            credential_name=credential_name,
        )
    finally:
        conn.close()


def _persist_group_messages(
    *,
    credential_name: str,
    identity_data: dict[str, Any],
    group_id: str,
    payload: dict[str, Any],
) -> None:
    """Persist a fetched group history batch into the local message cache."""
    messages = payload.get("messages", [])
    if not messages:
        return

    my_did = str(identity_data.get("did") or "")
    batch: list[dict[str, Any]] = []
    max_server_seq: int | None = None
    last_message_at: str | None = None
    for message in messages:
        sender_did = str(message.get("sender_did") or "")
        direction = 1 if sender_did and sender_did == my_did else 0
        sent_at = message.get("sent_at") or message.get("created_at")
        server_seq = message.get("server_seq")
        if isinstance(server_seq, int):
            max_server_seq = server_seq if max_server_seq is None else max(max_server_seq, server_seq)
        if sent_at:
            last_message_at = str(sent_at)
        batch.append(
            {
                "msg_id": message.get("id", ""),
                "thread_id": local_store.make_thread_id(my_did, group_id=group_id),
                "direction": direction,
                "sender_did": sender_did,
                "receiver_did": None,
                "group_id": group_id,
                "group_did": message.get("group_did"),
                "content_type": message.get("type", "group_user"),
                "content": str(message.get("content", "")),
                "title": message.get("title"),
                "server_seq": server_seq,
                "sent_at": sent_at,
                "sender_name": message.get("sender_name"),
                "metadata": (
                    json.dumps(
                        {"system_event": message.get("system_event")},
                        ensure_ascii=False,
                    )
                    if message.get("system_event") is not None
                    else None
                ),
                "credential_name": credential_name,
                "owner_did": my_did,
            }
        )

    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.store_messages_batch(
            conn,
            batch,
            owner_did=my_did,
            credential_name=credential_name,
        )
        for message in messages:
            system_event = message.get("system_event")
            if not isinstance(system_event, dict):
                continue
            local_store.sync_group_member_from_system_event(
                conn,
                owner_did=my_did,
                group_id=group_id,
                system_event=system_event,
                credential_name=credential_name,
            )
        local_store.upsert_group(
            conn,
            owner_did=my_did,
            group_id=group_id,
            membership_status="active",
            last_synced_seq=payload.get("next_since_seq") or max_server_seq,
            last_message_at=last_message_at,
            credential_name=credential_name,
        )
    finally:
        conn.close()


def _persist_outgoing_group_message(
    *,
    credential_name: str,
    identity_data: dict[str, Any],
    group_id: str,
    content: str,
    client_msg_id: str | None,
    payload: dict[str, Any],
) -> None:
    """Persist one successful outgoing group message locally."""
    my_did = str(identity_data.get("did") or "")
    sender_name = identity_data.get("handle") or identity_data.get("name")
    msg_id = str(payload.get("message_id") or payload.get("id") or "")
    if not msg_id:
        return

    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.store_message(
            conn,
            msg_id=msg_id,
            owner_did=my_did,
            thread_id=local_store.make_thread_id(my_did, group_id=group_id),
            direction=1,
            sender_did=my_did,
            receiver_did=None,
            group_id=group_id,
            group_did=None,
            content_type="group_user",
            content=content,
            server_seq=payload.get("server_seq"),
            sent_at=payload.get("created_at"),
            sender_name=str(sender_name) if sender_name else None,
            credential_name=credential_name,
        )
        local_store.upsert_group(
            conn,
            owner_did=my_did,
            group_id=group_id,
            membership_status="active",
            last_synced_seq=payload.get("server_seq"),
            last_message_at=payload.get("created_at"),
            credential_name=credential_name,
            metadata={"last_post_client_msg_id": client_msg_id} if client_msg_id else None,
        )
    finally:
        conn.close()


def _parse_bool(value: str) -> bool:
    """Parse a CLI boolean value."""
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y", "on"}:
        return True
    if normalized in {"false", "0", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("Boolean values must be true or false")


def _get_authenticator_or_exit(credential_name: str, config: SDKConfig):
    """Return an authenticator or terminate with a user-facing error."""
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(
            f"Credential '{credential_name}' unavailable; please create an identity first"
        )
        raise SystemExit(1)
    return auth_result


async def _authenticated_group_call(
    credential_name: str,
    method: str,
    params: dict | None = None,
) -> dict:
    """Run an authenticated group RPC call."""
    config = SDKConfig()
    auth, _ = _get_authenticator_or_exit(credential_name, config)
    async with create_user_service_client(config) as client:
        return await authenticated_rpc_call(
            client,
            GROUP_RPC_ENDPOINT,
            method,
            params or {},
            auth=auth,
            credential_name=credential_name,
        )


async def create_group(
    *,
    name: str,
    slug: str,
    description: str,
    goal: str,
    rules: str,
    message_prompt: str | None,
    member_max_messages: int | None,
    member_max_total_chars: int | None,
    join_enabled: bool,
    credential_name: str,
) -> None:
    """Create a group."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info("Creating group credential=%s slug=%s", credential_name, slug)
    try:
        result = await _authenticated_group_call(
            credential_name,
            "create",
            {
                "name": name,
                "slug": slug,
                "description": description,
                "goal": goal,
                "rules": rules,
                "join_enabled": join_enabled,
                **({"message_prompt": message_prompt} if message_prompt is not None else {}),
                **(
                    {"member_max_messages": member_max_messages}
                    if member_max_messages is not None
                    else {}
                ),
                **(
                    {"member_max_total_chars": member_max_total_chars}
                    if member_max_total_chars is not None
                    else {}
                ),
            },
        )
    except JsonRpcError as exc:
        if exc.code == -32004:
            print(
                f"Slug '{slug}' is already taken. "
                "Please choose a different slug.",
                file=sys.stderr,
            )
        raise
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=result,
        my_role="owner",
        membership_status="active",
    )
    print("Group created successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_group(
    *,
    group_id: str,
    credential_name: str,
) -> None:
    """Get group detail."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Fetching group detail credential=%s group_id=%s",
        credential_name,
        group_id,
    )
    result = await _authenticated_group_call(
        credential_name,
        "get",
        {"group_id": group_id},
    )
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=result,
        membership_status="active",
    )
    print("Group detail:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def update_group(
    *,
    group_id: str,
    name: str | None,
    description: str | None,
    goal: str | None,
    rules: str | None,
    message_prompt: str | None,
    member_max_messages: int | None = None,
    member_max_total_chars: int | None = None,
    credential_name: str,
) -> None:
    """Update mutable group metadata."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Updating group credential=%s group_id=%s", credential_name, group_id
    )
    params = {"group_id": group_id}
    if name is not None:
        params["name"] = name
    if description is not None:
        params["description"] = description
    if goal is not None:
        params["goal"] = goal
    if rules is not None:
        params["rules"] = rules
    if message_prompt is not None:
        params["message_prompt"] = message_prompt
    if member_max_messages is not None:
        params["member_max_messages"] = member_max_messages
    if member_max_total_chars is not None:
        params["member_max_total_chars"] = member_max_total_chars
    result = await _authenticated_group_call(credential_name, "update", params)
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=result,
        my_role="owner",
        membership_status="active",
    )
    print("Group updated successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def refresh_join_code(
    *,
    group_id: str,
    credential_name: str,
) -> None:
    """Refresh the active join-code."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Refreshing group join-code credential=%s group_id=%s",
        credential_name,
        group_id,
    )
    result = await _authenticated_group_call(
        credential_name,
        "refresh_join_code",
        {"group_id": group_id},
    )
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=result,
        my_role="owner",
        membership_status="active",
    )
    print("Join-code refreshed successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_join_code(
    *,
    group_id: str,
    credential_name: str,
) -> None:
    """Get the active join-code."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Fetching group join-code credential=%s group_id=%s",
        credential_name,
        group_id,
    )
    result = await _authenticated_group_call(
        credential_name,
        "get_join_code",
        {"group_id": group_id},
    )
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=result,
        my_role="owner",
        membership_status="active",
    )
    print("Current join-code:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def set_join_enabled(
    *,
    group_id: str,
    join_enabled: bool,
    credential_name: str,
) -> None:
    """Enable or disable group joining."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Updating group join switch credential=%s group_id=%s join_enabled=%s",
        credential_name,
        group_id,
        join_enabled,
    )
    result = await _authenticated_group_call(
        credential_name,
        "set_join_enabled",
        {"group_id": group_id, "join_enabled": join_enabled},
    )
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=result,
        my_role="owner",
        membership_status="active",
    )
    print("Join switch updated successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def join_group(
    *,
    join_code: str,
    credential_name: str,
) -> None:
    """Join a group with the only supported global 6-digit join-code."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info("Joining group credential=%s", credential_name)
    result = await _authenticated_group_call(
        credential_name,
        "join",
        {"passcode": join_code},
    )
    detail = await _authenticated_group_call(
        credential_name,
        "get",
        {"group_id": result["group_id"]},
    )
    detail.setdefault("group_id", result.get("group_id"))
    detail.setdefault("message_prompt", result.get("message_prompt"))
    _persist_group_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_payload=detail,
        my_role="member",
        membership_status=str(result.get("status") or "active"),
    )
    print("Joined group successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def leave_group(
    *,
    group_id: str,
    credential_name: str,
) -> None:
    """Leave a group."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Leaving group credential=%s group_id=%s", credential_name, group_id
    )
    result = await _authenticated_group_call(
        credential_name,
        "leave",
        {"group_id": group_id},
    )
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.upsert_group(
            conn,
            owner_did=str(identity_data.get("did") or ""),
            group_id=group_id,
            membership_status="left",
            credential_name=credential_name,
        )
        local_store.delete_group_members(
            conn,
            owner_did=str(identity_data.get("did") or ""),
            group_id=group_id,
        )
    finally:
        conn.close()
    print("Left group successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def kick_member(
    *,
    group_id: str,
    target_did: str | None,
    target_user_id: str | None,
    credential_name: str,
) -> None:
    """Kick a member from a group."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Kicking group member credential=%s group_id=%s",
        credential_name,
        group_id,
    )
    params = {"group_id": group_id}
    if target_did is not None:
        params["target_did"] = target_did
    if target_user_id is not None:
        params["target_user_id"] = target_user_id
    result = await _authenticated_group_call(credential_name, "kick_member", params)
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.delete_group_members(
            conn,
            owner_did=str(identity_data.get("did") or ""),
            group_id=group_id,
            target_did=target_did,
            target_user_id=target_user_id,
        )
    finally:
        conn.close()
    print("Member removed successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_group_members(
    *,
    group_id: str,
    credential_name: str,
) -> None:
    """View group members."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Fetching group members credential=%s group_id=%s",
        credential_name,
        group_id,
    )
    result = await _authenticated_group_call(
        credential_name,
        "list_members",
        {"group_id": group_id},
    )
    _persist_group_member_snapshot(
        credential_name=credential_name,
        identity_data=identity_data,
        group_id=group_id,
        members=result.get("members", []),
    )
    print("Group members:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def post_message(
    *,
    group_id: str,
    content: str,
    client_msg_id: str | None,
    credential_name: str,
) -> None:
    """Post a group message."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Posting group message credential=%s group_id=%s",
        credential_name,
        group_id,
    )
    params = {"group_id": group_id, "content": content}
    if client_msg_id is not None:
        params["client_msg_id"] = client_msg_id
    result = await _authenticated_group_call(credential_name, "post_message", params)
    _persist_outgoing_group_message(
        credential_name=credential_name,
        identity_data=identity_data,
        group_id=group_id,
        content=content,
        client_msg_id=client_msg_id,
        payload=result,
    )
    print("Group message posted successfully:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def list_messages(
    *,
    group_id: str,
    since_seq: int | None,
    limit: int,
    credential_name: str,
) -> None:
    """List group messages."""
    config = SDKConfig()
    identity_data = _get_identity_data_or_exit(credential_name, config)
    logger.info(
        "Listing group messages credential=%s group_id=%s since_seq=%s limit=%d",
        credential_name,
        group_id,
        since_seq,
        limit,
    )
    params = {"group_id": group_id, "limit": limit}
    if since_seq is not None:
        params["since_seq"] = since_seq
    result = await _authenticated_group_call(credential_name, "list_messages", params)
    _persist_group_messages(
        credential_name=credential_name,
        identity_data=identity_data,
        group_id=group_id,
        payload=result,
    )
    print("Group messages:", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def fetch_doc(*, doc_url: str) -> None:
    """Fetch a public group markdown document."""
    logger.info("Fetching group markdown doc_url=%s", doc_url)
    config = SDKConfig()
    async with create_user_service_client(config) as client:
        public_fetch_error: httpx.RequestError | None = None
        response = None
        try:
            response = await client.get(doc_url)
        except httpx.RequestError as exc:
            public_fetch_error = exc
            logger.warning(
                "Public group markdown fetch failed, trying X-Handle fallback: %s", exc
            )
        else:
            if response.status_code == 200:
                print(response.text)
                return

        parsed = urlparse(doc_url)
        hostname = (parsed.hostname or "").strip()
        path = parsed.path or ""
        handle = hostname.split(".", 1)[0].strip() if "." in hostname else ""
        if handle and path:
            fallback_response = await client.get(path, headers={"X-Handle": handle})
            if fallback_response.status_code == 200:
                print(fallback_response.text)
                return
            fallback_response.raise_for_status()

        if response is not None:
            response.raise_for_status()
        if public_fetch_error is not None:
            raise public_fetch_error


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="AWiki group management")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--create", action="store_true", help="Create a group"
    )
    action.add_argument("--get", action="store_true", help="View group detail")
    action.add_argument("--update", action="store_true", help="Update group metadata")
    action.add_argument(
        "--refresh-join-code", action="store_true", help="Refresh the current join-code"
    )
    action.add_argument(
        "--get-join-code", action="store_true", help="View the current join-code"
    )
    action.add_argument(
        "--set-join-enabled", action="store_true", help="Enable or disable joining"
    )
    action.add_argument(
        "--join",
        action="store_true",
        help="Join with the only supported 6-digit join-code",
    )
    action.add_argument("--leave", action="store_true", help="Leave a group")
    action.add_argument(
        "--kick-member", action="store_true", help="Remove a member from a group"
    )
    action.add_argument("--members", action="store_true", help="View active members")
    action.add_argument(
        "--post-message", action="store_true", help="Post a group message"
    )
    action.add_argument(
        "--list-messages", action="store_true", help="List group messages"
    )
    action.add_argument(
        "--fetch-doc", action="store_true", help="Fetch the public group markdown"
    )

    parser.add_argument(
        "--name", "--group-name", dest="name", type=str, help="Group name"
    )
    parser.add_argument("--slug", type=str, help="Group slug")
    parser.add_argument("--description", type=str, help="Group description")
    parser.add_argument("--goal", type=str, help="Group goal")
    parser.add_argument("--rules", type=str, help="Group rules")
    parser.add_argument(
        "--message-prompt",
        type=str,
        help="Optional member posting prompt",
    )
    parser.add_argument(
        "--group-mode",
        choices=("discovery", "chat"),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--member-max-messages",
        type=int,
        help="Optional per-member message-count limit",
    )
    parser.add_argument(
        "--member-max-total-chars",
        type=int,
        help="Optional per-member total-char limit",
    )
    parser.add_argument(
        "--join-enabled", type=_parse_bool, default=None, help="true or false"
    )
    parser.add_argument("--group-id", type=str, help="Group ID")
    parser.add_argument(
        "--join-code",
        type=str,
        help="6-digit group join-code; this is the only supported way to join",
    )
    parser.add_argument(
        "--passcode",
        dest="join_code",
        type=str,
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--target-did", type=str, help="Target DID")
    parser.add_argument("--target-user-id", type=str, help="Target user ID")
    parser.add_argument("--content", type=str, help="Message content")
    parser.add_argument(
        "--client-msg-id", type=str, help="Client idempotency message ID"
    )
    parser.add_argument("--since-seq", type=int, help="Incremental message cursor")
    parser.add_argument("--limit", type=int, default=50, help="Message list limit")
    parser.add_argument("--doc-url", type=str, help="Public group markdown URL")
    parser.add_argument(
        "--credential", type=str, default="default", help="Credential name"
    )

    parser.add_argument("--public", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--max-members", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--handle", type=str, help=argparse.SUPPRESS)
    return parser


def _reject_legacy_args(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> None:
    """Reject deprecated invitation-era CLI arguments."""
    if args.public:
        parser.error(
            "Groups do not support --public; use --join-enabled true|false"
        )
    if args.max_members is not None:
        parser.error("Groups do not support --max-members")
    if args.handle:
        parser.error(_JOIN_GUIDANCE)


def main() -> None:
    """CLI entrypoint."""
    configure_logging(console_level=None, mirror_stdio=True)
    parser = _build_parser()
    args = parser.parse_args()
    _reject_legacy_args(args, parser)
    logger.info("manage_group CLI started credential=%s", args.credential)

    try:
        if args.create:
            if args.join_code:
                parser.error(
                    "Creating a group does not accept --join-code; the server generates the initial join-code"
                )
            required_create_args = [
                args.name,
                args.slug,
                args.description,
                args.goal,
                args.rules,
            ]
            if not all(required_create_args):
                parser.error(
                    "Creating a group requires --name --slug --description --goal --rules"
                )
            asyncio.run(
                create_group(
                    name=args.name,
                    slug=args.slug,
                    description=args.description,
                    goal=args.goal,
                    rules=args.rules,
                    message_prompt=args.message_prompt,
                    member_max_messages=args.member_max_messages,
                    member_max_total_chars=args.member_max_total_chars,
                    join_enabled=True
                    if args.join_enabled is None
                    else args.join_enabled,
                    credential_name=args.credential,
                )
            )
        elif args.get:
            if not args.group_id:
                parser.error("Viewing group detail requires --group-id")
            asyncio.run(
                get_group(group_id=args.group_id, credential_name=args.credential)
            )
        elif args.update:
            if not args.group_id:
                parser.error("Updating a group requires --group-id")
            if not any(
                [
                    args.name,
                    args.description,
                    args.goal,
                    args.rules,
                    args.message_prompt,
                    args.member_max_messages,
                    args.member_max_total_chars,
                ]
            ):
                parser.error("Updating a group requires at least one mutable field")
            asyncio.run(
                update_group(
                    group_id=args.group_id,
                    name=args.name,
                    description=args.description,
                    goal=args.goal,
                    rules=args.rules,
                    message_prompt=args.message_prompt,
                    member_max_messages=args.member_max_messages,
                    member_max_total_chars=args.member_max_total_chars,
                    credential_name=args.credential,
                )
            )
        elif args.refresh_join_code:
            if not args.group_id:
                parser.error("Refreshing the join-code requires --group-id")
            asyncio.run(
                refresh_join_code(
                    group_id=args.group_id, credential_name=args.credential
                )
            )
        elif args.get_join_code:
            if not args.group_id:
                parser.error("Viewing the join-code requires --group-id")
            asyncio.run(
                get_join_code(group_id=args.group_id, credential_name=args.credential)
            )
        elif args.set_join_enabled:
            if not args.group_id:
                parser.error("Updating the join switch requires --group-id")
            if args.join_enabled is None:
                parser.error(
                    "Updating the join switch requires --join-enabled true|false"
                )
            asyncio.run(
                set_join_enabled(
                    group_id=args.group_id,
                    join_enabled=args.join_enabled,
                    credential_name=args.credential,
                )
            )
        elif args.join:
            if args.group_id or args.doc_url:
                parser.error(_JOIN_GUIDANCE)
            if not args.join_code:
                parser.error("Joining a group requires --join-code")
            asyncio.run(
                join_group(join_code=args.join_code, credential_name=args.credential)
            )
        elif args.leave:
            if not args.group_id:
                parser.error("Leaving a group requires --group-id")
            asyncio.run(
                leave_group(group_id=args.group_id, credential_name=args.credential)
            )
        elif args.kick_member:
            if not args.group_id:
                parser.error("Removing a member requires --group-id")
            if bool(args.target_did) == bool(args.target_user_id):
                parser.error("Provide exactly one of --target-did or --target-user-id")
            asyncio.run(
                kick_member(
                    group_id=args.group_id,
                    target_did=args.target_did,
                    target_user_id=args.target_user_id,
                    credential_name=args.credential,
                )
            )
        elif args.members:
            if not args.group_id:
                parser.error("Viewing members requires --group-id")
            asyncio.run(
                get_group_members(
                    group_id=args.group_id, credential_name=args.credential
                )
            )
        elif args.post_message:
            if not args.group_id or not args.content:
                parser.error("Posting a message requires --group-id and --content")
            asyncio.run(
                post_message(
                    group_id=args.group_id,
                    content=args.content,
                    client_msg_id=args.client_msg_id,
                    credential_name=args.credential,
                )
            )
        elif args.list_messages:
            if not args.group_id:
                parser.error("Listing messages requires --group-id")
            asyncio.run(
                list_messages(
                    group_id=args.group_id,
                    since_seq=args.since_seq,
                    limit=args.limit,
                    credential_name=args.credential,
                )
            )
        elif args.fetch_doc:
            if not args.doc_url:
                parser.error("Fetching a group markdown document requires --doc-url")
            asyncio.run(fetch_doc(doc_url=args.doc_url))
        else:
            parser.error("No action selected")
    except JsonRpcError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error_type": "jsonrpc",
                    "code": exc.code,
                    "message": exc.message,
                    "data": exc.data,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        raise SystemExit(1) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("manage_group CLI failed")
        print(
            json.dumps(
                {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
