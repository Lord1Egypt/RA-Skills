"""Create or restore a DID identity.

Create a new identity and save it locally on first use; reuse saved identities thereafter.

Usage:
    # Create a new identity
    uv run python scripts/setup_identity.py --name MyAgent

    # Load a saved identity
    uv run python scripts/setup_identity.py --load default

    # List all saved identities
    uv run python scripts/setup_identity.py --list

    # Delete a saved identity
    uv run python scripts/setup_identity.py --delete myid

[INPUT]: SDK (identity creation, registration, authentication), credential_store
         (credential persistence + authenticator factory), logging_config
[OUTPUT]: Create/load/list/delete DID identities with automatic JWT
          bootstrap/refresh during load
[POS]: Identity management entry script; must be called before first use

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

from utils import (
    SDKConfig,
    create_identity,
    create_user_service_client,
    register_did,
    get_jwt_via_wba,
    create_authenticated_identity,
    authenticated_rpc_call,
    rpc_call,
)
from utils.logging_config import configure_logging
from credential_store import (
    save_identity,
    load_identity,
    list_identities,
    delete_identity,
    update_jwt,
    create_authenticator,
)

logger = logging.getLogger(__name__)


async def create_new_identity(
    name: str,
    display_name: str | None = None,
    credential_name: str = "default",
    is_agent: bool = False,
) -> None:
    """Create a new DID identity and save it."""
    logger.info(
        "Creating new identity credential=%s display_name=%s is_agent=%s",
        credential_name,
        display_name or name,
        is_agent,
    )
    config = SDKConfig()
    print(f"Service configuration:")
    print(f"  user-service: {config.user_service_url}")
    print(f"  DID domain  : {config.did_domain}")

    async with create_user_service_client(config) as client:
        print(f"\nCreating DID identity...")
        identity = await create_authenticated_identity(
            client=client,
            config=config,
            name=display_name or name,
            is_agent=is_agent,
        )

        print(f"  DID       : {identity.did}")
        print(f"  unique_id : {identity.unique_id}")
        print(f"  user_id   : {identity.user_id}")
        print(f"  JWT token : {identity.jwt_token[:50]}...")

        # Save credential
        path = save_identity(
            did=identity.did,
            unique_id=identity.unique_id,
            user_id=identity.user_id,
            private_key_pem=identity.private_key_pem,
            public_key_pem=identity.public_key_pem,
            jwt_token=identity.jwt_token,
            display_name=display_name or name,
            name=credential_name,
            did_document=identity.did_document,
            e2ee_signing_private_pem=identity.e2ee_signing_private_pem,
            e2ee_agreement_private_pem=identity.e2ee_agreement_private_pem,
        )
        print(f"\nCredential saved to: {path}")
        print(f"Credential name: {credential_name}")


async def load_saved_identity(credential_name: str = "default") -> None:
    """Load a saved identity and verify it."""
    logger.info("Loading saved identity credential=%s", credential_name)
    data = load_identity(credential_name)
    if data is None:
        print(f"Credential '{credential_name}' not found")
        print(
            "Create an identity first: uv run python scripts/setup_identity.py "
            "--name MyAgent"
        )
        sys.exit(1)

    print(f"Loaded credential: {credential_name}")
    print(f"  DID       : {data['did']}")
    print(f"  unique_id : {data['unique_id']}")
    print(f"  user_id   : {data.get('user_id', 'N/A')}")
    print(f"  Created at: {data.get('created_at', 'N/A')}")

    config = SDKConfig()

    # Try using DIDWbaAuthHeader for automatic authentication
    auth_result = create_authenticator(credential_name, config)
    if auth_result is not None:
        auth, _ = auth_result
        old_token = data.get("jwt_token")
        async with create_user_service_client(config) as client:
            try:
                me = await authenticated_rpc_call(
                    client,
                    "/user-service/did-auth/rpc",
                    "get_me",
                    auth=auth,
                    credential_name=credential_name,
                )
                refreshed_data = load_identity(credential_name) or {}
                new_token = refreshed_data.get("jwt_token")
                if not old_token and new_token:
                    print("\n  JWT bootstrap succeeded and was saved automatically.")
                elif old_token and new_token and new_token != old_token:
                    print("\n  JWT refresh succeeded and was saved automatically.")
                else:
                    print("\n  JWT verification succeeded.")
                print("  Current identity:")
                print(f"    DID: {me.get('did', 'N/A')}")
                print(f"    Name: {me.get('name', 'N/A')}")
            except Exception as e:
                print(f"\n  JWT verification/refresh failed: {e}")
                print("  You may need to recreate the identity")
    else:
        if not data.get("jwt_token"):
            print("\n  No JWT token is saved and DID auth files are missing.")
            print("  Please recreate the identity to enable automatic authentication:")
            print(
                "    uv run python scripts/setup_identity.py --name "
                f"\"{data.get('name', 'MyAgent')}\" --credential {credential_name}"
            )
            return

        # Legacy credential without did_document; fall back to direct verification
        async with create_user_service_client(config) as client:
            client.headers["Authorization"] = f"Bearer {data['jwt_token']}"
            try:
                me = await rpc_call(client, "/user-service/did-auth/rpc", "get_me")
                print(f"\n  JWT verification succeeded! Current identity:")
                print(f"    DID: {me.get('did', 'N/A')}")
                print(f"    Name: {me.get('name', 'N/A')}")
            except Exception:
                print(
                    "\n  JWT expired. Please recreate the identity to enable "
                    "auto-refresh:"
                )
                print(
                    "    uv run python scripts/setup_identity.py --name "
                    f"\"{data.get('name', 'MyAgent')}\" --credential {credential_name}"
                )


def show_identities() -> None:
    """Show all saved identities."""
    logger.info("Listing saved identities")
    identities = list_identities()
    if not identities:
        print("No saved identities")
        print("Create an identity: uv run python scripts/setup_identity.py --name MyAgent")
        return

    print(f"Saved identities ({len(identities)}):")
    print("-" * 70)
    for ident in identities:
        jwt_status = "yes" if ident["has_jwt"] else "no"
        print(f"  [{ident['credential_name']}]")
        print(f"    DID       : {ident['did']}")
        print(f"    Name      : {ident.get('name', 'N/A')}")
        print(f"    user_id   : {ident.get('user_id', 'N/A')}")
        print(f"    JWT       : {jwt_status}")
        print(f"    Created at: {ident.get('created_at', 'N/A')}")
        print()


def remove_identity(credential_name: str) -> None:
    """Delete a saved identity."""
    logger.info("Deleting identity credential=%s", credential_name)
    if delete_identity(credential_name):
        print(f"Deleted credential: {credential_name}")
    else:
        print(f"Credential '{credential_name}' not found")


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="DID identity management")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", type=str, help="Create a new identity with display name")
    group.add_argument("--load", type=str, nargs="?", const="default",
                       help="Load a saved identity (default: default)")
    group.add_argument("--list", action="store_true", help="List all saved identities")
    group.add_argument("--delete", type=str, help="Delete a saved identity")

    parser.add_argument("--credential", type=str, default="default",
                        help="Credential storage name (default: default)")
    parser.add_argument("--agent", action="store_true",
                        help="Mark as AI Agent identity")

    args = parser.parse_args()
    logger.info(
        "setup_identity CLI started action=%s credential=%s",
        "list" if args.list else "delete" if args.delete else "load" if args.load is not None else "create",
        args.credential if args.name else args.delete or args.load or "default",
    )

    if args.list:
        show_identities()
    elif args.delete:
        remove_identity(args.delete)
    elif args.load is not None:
        asyncio.run(load_saved_identity(args.load))
    elif args.name:
        asyncio.run(create_new_identity(
            name=args.name,
            display_name=args.name,
            credential_name=args.credential,
            is_agent=args.agent,
        ))


if __name__ == "__main__":
    main()
