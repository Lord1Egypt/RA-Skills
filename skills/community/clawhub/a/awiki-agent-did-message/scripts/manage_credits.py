"""Query credits balance, transactions, and rules.

Usage:
    # View credit balance
    python scripts/manage_credits.py --balance

    # View credit transaction history
    python scripts/manage_credits.py --transactions
    python scripts/manage_credits.py --transactions --limit 20 --offset 0

    # View all credit rules (no auth required)
    python scripts/manage_credits.py --rules

[INPUT]: SDK (RPC calls), credential_store (load identity credentials),
         logging_config
[OUTPUT]: Credits information as JSON output
[POS]: Credits query script for balance, transactions, and rules

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys

from utils import SDKConfig, create_user_service_client, rpc_call, authenticated_rpc_call
from utils.logging_config import configure_logging
from credential_store import create_authenticator


CREDITS_RPC = "/user-service/credits/rpc"
logger = logging.getLogger(__name__)


async def get_balance(credential_name: str = "default") -> None:
    """View current credit balance."""
    logger.info("Fetching credit balance credential=%s", credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Please create an identity first with setup_identity.py or register_handle.py",
        }, ensure_ascii=False))
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CREDITS_RPC, "get_balance", {},
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_transactions(
    credential_name: str = "default",
    limit: int = 20,
    offset: int = 0,
) -> None:
    """View credit transaction history."""
    logger.info(
        "Fetching credit transactions credential=%s limit=%d offset=%d",
        credential_name, limit, offset,
    )
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Please create an identity first with setup_identity.py or register_handle.py",
        }, ensure_ascii=False))
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CREDITS_RPC, "get_transactions",
            {"limit": limit, "offset": offset},
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))


async def get_rules() -> None:
    """View all credit rules (public, no auth required)."""
    logger.info("Fetching credit rules")
    config = SDKConfig()
    async with create_user_service_client(config) as client:
        result = await rpc_call(
            client, CREDITS_RPC, "get_rules", {},
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Credits management — view balance, transactions, and rules")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--balance", action="store_true", help="View current credit balance")
    group.add_argument("--transactions", action="store_true", help="View credit transaction history")
    group.add_argument("--rules", action="store_true", help="View all credit rules (no auth required)")

    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")
    parser.add_argument("--limit", type=int, default=20,
                        help="Transaction list limit (default: 20)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Transaction list offset (default: 0)")

    args = parser.parse_args()
    logger.info("manage_credits CLI started credential=%s", args.credential)

    if args.balance:
        asyncio.run(get_balance(args.credential))
    elif args.transactions:
        asyncio.run(get_transactions(args.credential, args.limit, args.offset))
    elif args.rules:
        asyncio.run(get_rules())


if __name__ == "__main__":
    main()
