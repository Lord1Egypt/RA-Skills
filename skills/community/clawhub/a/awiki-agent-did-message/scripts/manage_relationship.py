"""Follow/unfollow/view relationship status/lists.

Usage:
    # Follow
    uv run python scripts/manage_relationship.py --follow "did:wba:localhost:user:abc123"

    # Unfollow
    uv run python scripts/manage_relationship.py --unfollow "did:wba:localhost:user:abc123"

    # View relationship status with a specific DID
    uv run python scripts/manage_relationship.py --status "did:wba:localhost:user:abc123"

    # View following list
    uv run python scripts/manage_relationship.py --following

    # View followers list
    uv run python scripts/manage_relationship.py --followers

[INPUT]: SDK (RPC calls), credential_store (load identity credentials),
         local_store, logging_config
[OUTPUT]: Relationship operation results with local contact sedimentation updates
[POS]: Social relationship management script

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys

from utils import SDKConfig, create_user_service_client, authenticated_rpc_call, resolve_to_did
from utils.logging_config import configure_logging
from credential_store import create_authenticator
import local_store


RPC_ENDPOINT = "/user-service/did/relationships/rpc"
logger = logging.getLogger(__name__)


async def follow(target_did: str, credential_name: str = "default") -> None:
    """Follow a specific DID."""
    logger.info("Following target=%s credential=%s", target_did, credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, data = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, RPC_ENDPOINT, "follow", {"target_did": target_did},
            auth=auth, credential_name=credential_name,
        )
        try:
            conn = local_store.get_connection()
            local_store.ensure_schema(conn)
            local_store.upsert_contact(
                conn,
                owner_did=data["did"],
                did=target_did,
                relationship="following",
                followed=True,
            )
            local_store.append_relationship_event(
                conn,
                owner_did=data["did"],
                target_did=target_did,
                event_type="followed",
                status="applied",
                credential_name=credential_name,
            )
            conn.close()
        except Exception:
            logger.debug("Failed to persist follow relationship locally", exc_info=True)
        print("Follow succeeded:", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False))


async def unfollow(target_did: str, credential_name: str = "default") -> None:
    """Unfollow a specific DID."""
    logger.info("Unfollowing target=%s credential=%s", target_did, credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, data = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, RPC_ENDPOINT, "unfollow", {"target_did": target_did},
            auth=auth, credential_name=credential_name,
        )
        try:
            conn = local_store.get_connection()
            local_store.ensure_schema(conn)
            local_store.upsert_contact(
                conn,
                owner_did=data["did"],
                did=target_did,
                relationship="none",
                followed=False,
            )
            local_store.append_relationship_event(
                conn,
                owner_did=data["did"],
                target_did=target_did,
                event_type="unfollowed",
                status="applied",
                credential_name=credential_name,
            )
            conn.close()
        except Exception:
            logger.debug("Failed to persist unfollow relationship locally", exc_info=True)
        print("Unfollow succeeded:", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_status(target_did: str, credential_name: str = "default") -> None:
    """View relationship status with a specific DID."""
    logger.info("Fetching relationship status target=%s credential=%s", target_did, credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, RPC_ENDPOINT, "get_status", {"target_did": target_did},
            auth=auth, credential_name=credential_name,
        )
        print("Relationship status:", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_following(
    credential_name: str = "default",
    limit: int = 50,
    offset: int = 0,
) -> None:
    """View following list."""
    logger.info("Fetching following list credential=%s limit=%d offset=%d", credential_name, limit, offset)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, RPC_ENDPOINT, "get_following",
            {"limit": limit, "offset": offset},
            auth=auth, credential_name=credential_name,
        )
        print("Following list:", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_followers(
    credential_name: str = "default",
    limit: int = 50,
    offset: int = 0,
) -> None:
    """View followers list."""
    logger.info("Fetching followers list credential=%s limit=%d offset=%d", credential_name, limit, offset)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, RPC_ENDPOINT, "get_followers",
            {"limit": limit, "offset": offset},
            auth=auth, credential_name=credential_name,
        )
        print("Followers list:", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Social relationship management")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--follow", type=str, help="Follow a specific DID or handle")
    group.add_argument("--unfollow", type=str, help="Unfollow a specific DID or handle")
    group.add_argument("--status", type=str, help="View relationship status with a specific DID or handle")
    group.add_argument("--following", action="store_true", help="View following list")
    group.add_argument("--followers", action="store_true", help="View followers list")

    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")
    parser.add_argument("--limit", type=int, default=50,
                        help="List result count (default: 50)")
    parser.add_argument("--offset", type=int, default=0,
                        help="List offset (default: 0)")

    args = parser.parse_args()
    logger.info("manage_relationship CLI started credential=%s", args.credential)

    if args.follow:
        target_did = asyncio.run(resolve_to_did(args.follow))
        asyncio.run(follow(target_did, args.credential))
    elif args.unfollow:
        target_did = asyncio.run(resolve_to_did(args.unfollow))
        asyncio.run(unfollow(target_did, args.credential))
    elif args.status:
        target_did = asyncio.run(resolve_to_did(args.status))
        asyncio.run(get_status(target_did, args.credential))
    elif args.following:
        asyncio.run(get_following(args.credential, args.limit, args.offset))
    elif args.followers:
        asyncio.run(get_followers(args.credential, args.limit, args.offset))


if __name__ == "__main__":
    main()
