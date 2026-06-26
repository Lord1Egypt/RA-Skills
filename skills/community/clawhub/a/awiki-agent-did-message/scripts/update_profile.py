"""Update DID Profile (nickname, bio, tags, etc.).

Usage:
    # Update nickname
    uv run python scripts/update_profile.py --nick-name "DID Pro"

    # Update multiple fields
    uv run python scripts/update_profile.py \\
        --nick-name "DID Pro" \\
        --bio "Decentralized identity enthusiast" \\
        --tags "developer,did,agent"

    # Update Profile Markdown
    uv run python scripts/update_profile.py --profile-md "# About Me\n\nI am an agent."

[INPUT]: SDK (RPC calls), credential_store (load identity credentials),
         logging_config
[OUTPUT]: Updated Profile information
[POS]: Profile update script

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

from utils import SDKConfig, create_user_service_client, authenticated_rpc_call
from utils.logging_config import configure_logging
from credential_store import create_authenticator


PROFILE_RPC = "/user-service/did/profile/rpc"
logger = logging.getLogger(__name__)


async def update_profile(
    credential_name: str,
    nick_name: str | None = None,
    bio: str | None = None,
    tags: list[str] | None = None,
    profile_md: str | None = None,
) -> None:
    """Update own Profile."""
    logger.info(
        "Updating profile credential=%s fields=%s",
        credential_name,
        [
            field_name
            for field_name, field_value in (
                ("nick_name", nick_name),
                ("bio", bio),
                ("tags", tags),
                ("profile_md", profile_md),
            )
            if field_value is not None
        ],
    )
    params: dict = {}
    if nick_name is not None:
        params["nick_name"] = nick_name
    if bio is not None:
        params["bio"] = bio
    if tags is not None:
        params["tags"] = tags
    if profile_md is not None:
        params["profile_md"] = profile_md

    if not params:
        print("Please specify at least one field to update")
        print("Available fields: --nick-name, --bio, --tags, --profile-md")
        sys.exit(1)

    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        updated = await authenticated_rpc_call(
            client, PROFILE_RPC, "update_me", params,
            auth=auth, credential_name=credential_name,
        )
        print("Profile updated successfully:", file=sys.stderr)
        print(json.dumps(updated, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Update DID Profile")
    parser.add_argument("--nick-name", type=str, help="Nickname")
    parser.add_argument("--bio", type=str, help="Bio")
    parser.add_argument("--tags", type=str, help="Tags (comma-separated)")
    parser.add_argument("--profile-md", type=str, help="Profile Markdown content")
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")

    args = parser.parse_args()
    logger.info("update_profile CLI started credential=%s", args.credential)

    tags = args.tags.split(",") if args.tags else None

    asyncio.run(update_profile(
        credential_name=args.credential,
        nick_name=args.nick_name,
        bio=args.bio,
        tags=tags,
        profile_md=args.profile_md,
    ))


if __name__ == "__main__":
    main()
