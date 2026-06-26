"""Resolve a Handle to DID or look up Handle by DID.

Usage:
    # Resolve handle to DID
    uv run python scripts/resolve_handle.py --handle alice

    # Look up handle by DID
    uv run python scripts/resolve_handle.py --did "did:wba:awiki.ai:alice:k1_abc123"

[INPUT]: SDK (handle resolution), user-service RPC, logging_config
[OUTPUT]: Handle/DID mapping information
[POS]: CLI for Handle resolution and reverse lookup

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys

from utils import SDKConfig, create_user_service_client, resolve_handle, lookup_handle
from utils.cli_errors import exit_with_cli_error
from utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


async def do_resolve(handle: str | None, did: str | None) -> None:
    """Resolve Handle or look up by DID."""
    logger.info("Resolving identifier handle=%s did=%s", handle, did)
    config = SDKConfig()

    async with create_user_service_client(config) as client:
        if handle:
            logger.info("Resolving handle handle=%s", handle)
            result = await resolve_handle(client, handle)
        elif did:
            logger.info("Looking up handle for DID did=%s", did)
            result = await lookup_handle(client, did)
        else:
            print("Either --handle or --did is required.")
            sys.exit(1)

        print(json.dumps(result, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Resolve Handle / look up Handle by DID")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--handle", type=str, help="Handle to resolve (e.g., alice)")
    group.add_argument("--did", type=str, help="DID to look up handle for")

    args = parser.parse_args()
    logger.info(
        "resolve_handle CLI started mode=%s",
        "handle" if args.handle else "did",
    )
    try:
        asyncio.run(do_resolve(handle=args.handle, did=args.did))
    except Exception as exc:  # noqa: BLE001
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="resolve_handle CLI failed",
        )


if __name__ == "__main__":
    main()
