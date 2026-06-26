"""User Search (用户搜索) — search users by semantic matching.

Usage:
    # Search users
    uv run python scripts/search_users.py "alice"

    # Search with a specific credential
    uv run python scripts/search_users.py "AI agent" --credential bob

[INPUT]: SDK (RPC calls), credential_store (load identity credentials),
         logging_config
[OUTPUT]: Search results as JSON output
[POS]: User search script — calls search-service /search/rpc

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys

from utils import SDKConfig, create_user_service_client, authenticated_rpc_call
from utils.logging_config import configure_logging
from credential_store import create_authenticator


SEARCH_RPC = "/search/rpc"
logger = logging.getLogger(__name__)


async def search_users(query: str, credential_name: str = "default") -> None:
    """Search users by semantic matching."""
    logger.info("Searching users query=%r credential=%s", query, credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(f"Credential '{credential_name}' unavailable; please create an identity first")
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, SEARCH_RPC, "search.users",
            params={"type": "keyword", "q": query},
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="User Search (用户搜索)")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")

    args = parser.parse_args()
    logger.info("search_users CLI started credential=%s query=%r", args.credential, args.query)

    asyncio.run(search_users(args.query, args.credential))


if __name__ == "__main__":
    main()
