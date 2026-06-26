"""View DID Profile (own or public).

Usage:
    # View own Profile
    uv run python scripts/get_profile.py

    # View public Profile of a specific DID
    uv run python scripts/get_profile.py --did "did:wba:localhost:user:abc123"

    # View public Profile of a specific handle
    uv run python scripts/get_profile.py --handle alice

    # Resolve a DID document
    uv run python scripts/get_profile.py --resolve "did:wba:localhost:user:abc123"

[INPUT]: SDK (RPC calls), credential_store (load identity credentials),
         logging_config
[OUTPUT]: Profile information as JSON output
[POS]: Profile query script

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from utils import SDKConfig, create_user_service_client, rpc_call, authenticated_rpc_call
from utils.logging_config import configure_logging
from credential_store import create_authenticator


PROFILE_RPC = "/user-service/did/profile/rpc"
logger = logging.getLogger(__name__)


async def get_my_profile(credential_name: str = "default") -> None:
    """View own Profile."""
    logger.info("Fetching own profile credential=%s", credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        me = await authenticated_rpc_call(
            client, PROFILE_RPC, "get_me",
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps(me, indent=2, ensure_ascii=False))


async def get_public_profile(*, did: str | None = None, handle: str | None = None) -> None:
    """View public Profile of a specific DID or handle."""
    logger.info("Fetching public profile did=%s handle=%s", did, handle)
    params: dict[str, str] = {}
    if did:
        params["did"] = did
    elif handle:
        params["handle"] = handle
    else:
        print("Error: must provide --did or --handle")
        sys.exit(1)

    config = SDKConfig()
    async with create_user_service_client(config) as client:
        profile = await rpc_call(
            client, PROFILE_RPC, "get_public_profile", params
        )
        print(json.dumps(profile, indent=2, ensure_ascii=False))


async def resolve_did(did: str) -> None:
    """Resolve a DID document."""
    logger.info("Resolving DID document did=%s", did)
    config = SDKConfig()
    async with create_user_service_client(config) as client:
        resolved = await rpc_call(
            client, PROFILE_RPC, "resolve", {"did": did}
        )
        print(json.dumps(resolved, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="View DID Profile")
    parser.add_argument("--did", type=str, help="View public Profile of a specific DID")
    parser.add_argument("--handle", type=str, help="View public Profile of a specific handle")
    parser.add_argument("--resolve", type=str, help="Resolve a specific DID document")
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")

    args = parser.parse_args()
    logger.info(
        "get_profile CLI started credential=%s mode=%s",
        args.credential,
        "resolve" if args.resolve else "public" if args.did or args.handle else "self",
    )

    if args.resolve:
        asyncio.run(resolve_did(args.resolve))
    elif args.did or args.handle:
        asyncio.run(get_public_profile(did=args.did, handle=args.handle))
    else:
        asyncio.run(get_my_profile(args.credential))


if __name__ == "__main__":
    main()
