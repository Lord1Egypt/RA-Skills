"""Manage locally persisted contact sedimentation and recommendation events.

Usage:
    # Record an AI recommendation candidate from a group
    uv run python scripts/manage_contacts.py --record-recommendation \
      --target-did "did:wba:awiki.ai:user:bob" \
      --source-type meetup \
      --source-name "OpenClaw Meetup Hangzhou 2026" \
      --source-group-id grp_123 \
      --reason "Strong infra fit and clear collaboration intent"

    # Save a contact after user confirmation
    uv run python scripts/manage_contacts.py --save-from-group \
      --target-did "did:wba:awiki.ai:user:bob" \
      --target-handle "bob.awiki.ai" \
      --source-type meetup \
      --source-name "OpenClaw Meetup Hangzhou 2026" \
      --source-group-id grp_123 \
      --reason "Strong infra fit and clear collaboration intent"

    # Update local follow / message / note state
    uv run python scripts/manage_contacts.py --mark-followed --target-did "did:wba:awiki.ai:user:bob"
    uv run python scripts/manage_contacts.py --mark-messaged --target-did "did:wba:awiki.ai:user:bob"
    uv run python scripts/manage_contacts.py --note --target-did "did:wba:awiki.ai:user:bob" --text "Met at the meetup."

[INPUT]: credential_store identity data, local_store, logging_config
[OUTPUT]: Local contact snapshot updates and append-only relationship events
[POS]: Local relationship-sedimentation CLI for group discovery workflows

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from typing import Any

import local_store
from credential_store import create_authenticator
from utils import SDKConfig
from utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def _identity_or_exit(credential_name: str) -> dict[str, Any]:
    """Load local identity metadata or exit with a user-facing error."""
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(
            f"Credential '{credential_name}' unavailable; please create an identity first"
        )
        raise SystemExit(1)
    _auth, data = auth_result
    return data


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Manage local contact sedimentation for group discovery"
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--record-recommendation",
        action="store_true",
        help="Record an AI recommendation candidate without writing contacts",
    )
    action.add_argument(
        "--save-from-group",
        action="store_true",
        help="Save a confirmed contact from a discovery group",
    )
    action.add_argument(
        "--mark-followed",
        action="store_true",
        help="Mark a contact as followed locally",
    )
    action.add_argument(
        "--mark-messaged",
        action="store_true",
        help="Mark a contact as messaged locally",
    )
    action.add_argument(
        "--note",
        action="store_true",
        help="Update the local note for one contact",
    )

    parser.add_argument("--target-did", type=str, help="Target DID")
    parser.add_argument("--target-handle", type=str, help="Target handle")
    parser.add_argument(
        "--source-type",
        type=str,
        help="Source type: event / meetup / hiring / dinner / private_session / online_group",
    )
    parser.add_argument("--source-name", type=str, help="Source name")
    parser.add_argument("--source-group-id", type=str, help="Source group ID")
    parser.add_argument("--reason", type=str, help="Recommendation or save reason")
    parser.add_argument("--score", type=float, default=None, help="Recommendation score")
    parser.add_argument("--text", type=str, help="Free-form note text")
    parser.add_argument(
        "--connected-at",
        type=str,
        default=None,
        help="Connection timestamp in ISO 8601 format (defaults to now)",
    )
    parser.add_argument(
        "--credential",
        type=str,
        default="default",
        help="Credential name (default: default)",
    )
    return parser


def _require_target_did(args: argparse.Namespace, parser: argparse.ArgumentParser) -> str:
    """Require and return the target DID."""
    if not args.target_did:
        parser.error("This action requires --target-did")
    return args.target_did


def _require_group_context(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Require the minimum source context for group-based sedimentation."""
    missing = [
        name
        for name in ("source_type", "source_name", "source_group_id", "reason")
        if not getattr(args, name)
    ]
    if missing:
        flags = " ".join(f"--{item.replace('_', '-')}" for item in missing)
        parser.error(f"This action requires {flags}")


def record_recommendation(args: argparse.Namespace) -> None:
    """Record an AI recommendation candidate as a pending event."""
    identity = _identity_or_exit(args.credential)
    connected_at = args.connected_at or _now_iso()
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        event_id = local_store.append_relationship_event(
            conn,
            owner_did=str(identity["did"]),
            target_did=args.target_did,
            target_handle=args.target_handle,
            event_type="ai_recommended",
            source_type=args.source_type,
            source_name=args.source_name,
            source_group_id=args.source_group_id,
            reason=args.reason,
            score=args.score,
            status="pending",
            metadata={"connected_at": connected_at},
            credential_name=args.credential,
        )
    finally:
        conn.close()
    print(
        json.dumps(
            {
                "ok": True,
                "event_id": event_id,
                "status": "pending",
                "target_did": args.target_did,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def save_from_group(args: argparse.Namespace) -> None:
    """Persist a confirmed contact snapshot and acceptance event."""
    identity = _identity_or_exit(args.credential)
    connected_at = args.connected_at or _now_iso()
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.upsert_contact(
            conn,
            owner_did=str(identity["did"]),
            did=args.target_did,
            handle=args.target_handle,
            source_type=args.source_type,
            source_name=args.source_name,
            source_group_id=args.source_group_id,
            connected_at=connected_at,
            recommended_reason=args.reason,
            note=args.text,
        )
        event_id = local_store.append_relationship_event(
            conn,
            owner_did=str(identity["did"]),
            target_did=args.target_did,
            target_handle=args.target_handle,
            event_type="saved_to_contacts",
            source_type=args.source_type,
            source_name=args.source_name,
            source_group_id=args.source_group_id,
            reason=args.reason,
            score=args.score,
            status="accepted",
            metadata={"connected_at": connected_at, "note": args.text},
            credential_name=args.credential,
        )
    finally:
        conn.close()
    print(
        json.dumps(
            {
                "ok": True,
                "event_id": event_id,
                "target_did": args.target_did,
                "saved": True,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def mark_followed(args: argparse.Namespace) -> None:
    """Mark one contact as followed locally."""
    identity = _identity_or_exit(args.credential)
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.upsert_contact(
            conn,
            owner_did=str(identity["did"]),
            did=args.target_did,
            handle=args.target_handle,
            followed=True,
        )
        event_id = local_store.append_relationship_event(
            conn,
            owner_did=str(identity["did"]),
            target_did=args.target_did,
            target_handle=args.target_handle,
            event_type="followed",
            status="applied",
            credential_name=args.credential,
        )
    finally:
        conn.close()
    print(json.dumps({"ok": True, "event_id": event_id}, indent=2, ensure_ascii=False))


def mark_messaged(args: argparse.Namespace) -> None:
    """Mark one contact as messaged locally."""
    identity = _identity_or_exit(args.credential)
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.upsert_contact(
            conn,
            owner_did=str(identity["did"]),
            did=args.target_did,
            handle=args.target_handle,
            messaged=True,
        )
        event_id = local_store.append_relationship_event(
            conn,
            owner_did=str(identity["did"]),
            target_did=args.target_did,
            target_handle=args.target_handle,
            event_type="messaged",
            status="applied",
            credential_name=args.credential,
        )
    finally:
        conn.close()
    print(json.dumps({"ok": True, "event_id": event_id}, indent=2, ensure_ascii=False))


def update_note(args: argparse.Namespace) -> None:
    """Update the local note for one contact."""
    identity = _identity_or_exit(args.credential)
    conn = local_store.get_connection()
    try:
        local_store.ensure_schema(conn)
        local_store.upsert_contact(
            conn,
            owner_did=str(identity["did"]),
            did=args.target_did,
            handle=args.target_handle,
            note=args.text,
        )
        event_id = local_store.append_relationship_event(
            conn,
            owner_did=str(identity["did"]),
            target_did=args.target_did,
            target_handle=args.target_handle,
            event_type="note_updated",
            reason=args.text,
            status="applied",
            credential_name=args.credential,
        )
    finally:
        conn.close()
    print(json.dumps({"ok": True, "event_id": event_id}, indent=2, ensure_ascii=False))


def main() -> None:
    """CLI entrypoint."""
    configure_logging(console_level=None, mirror_stdio=True)
    parser = _build_parser()
    args = parser.parse_args()
    logger.info("manage_contacts CLI started credential=%s", args.credential)

    if args.record_recommendation:
        _require_target_did(args, parser)
        _require_group_context(args, parser)
        record_recommendation(args)
    elif args.save_from_group:
        _require_target_did(args, parser)
        _require_group_context(args, parser)
        save_from_group(args)
    elif args.mark_followed:
        _require_target_did(args, parser)
        mark_followed(args)
    elif args.mark_messaged:
        _require_target_did(args, parser)
        mark_messaged(args)
    elif args.note:
        _require_target_did(args, parser)
        if not args.text:
            parser.error("--note requires --text")
        update_note(args)
    else:
        parser.error("No action selected")


if __name__ == "__main__":
    main()
