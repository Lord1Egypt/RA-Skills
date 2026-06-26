"""Recover a Handle by rebinding it to a new DID.

Usage:
    uv run python scripts/send_verification_code.py --phone +8613800138000
    uv run python scripts/recover_handle.py --handle alice --phone +8613800138000 --otp-code 123456
    uv run python scripts/recover_handle.py --handle alice --phone +8613800138000 --otp-code 123456 --credential alice
    uv run python scripts/recover_handle.py --handle alice --phone +8613800138000 --otp-code 123456 --credential default --replace-existing

[INPUT]: SDK (handle OTP + recovery RPC), credential_store, local_store, e2ee_store
[OUTPUT]: Handle recovery result with safe credential target selection, optional
          credential replacement, and conditional local cache migration
[POS]: Pure non-interactive recovery CLI for users who lost the old DID private key
       but still control the original Handle phone number

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

import local_store
from credential_store import (
    backup_identity,
    load_identity,
    prune_unreferenced_credential_dir,
    save_identity,
)
from e2ee_store import delete_e2ee_state
from utils import SDKConfig, create_user_service_client, recover_handle
from utils.cli_errors import exit_with_cli_error
from utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def _allocate_recovery_credential_name(handle: str) -> str:
    """Return a non-destructive credential name for a recovered Handle."""
    candidate_names = [handle, f"{handle}_recovered"]
    for candidate in candidate_names:
        if load_identity(candidate) is None:
            return candidate

    suffix = 2
    while True:
        candidate = f"{handle}_recovered_{suffix}"
        if load_identity(candidate) is None:
            return candidate
        suffix += 1


def _resolve_recovery_target(
    *,
    handle: str,
    requested_credential_name: str | None,
    replace_existing: bool,
) -> tuple[str, dict[str, Any] | None]:
    """Resolve the credential target for recovery without implicit overwrites."""
    if requested_credential_name is None:
        return _allocate_recovery_credential_name(handle), None

    existing_credential = load_identity(requested_credential_name)
    if existing_credential is not None and not replace_existing:
        raise ValueError(
            f"Credential '{requested_credential_name}' already exists for DID "
            f"{existing_credential.get('did')}; use a different --credential value "
            "or pass --replace-existing to overwrite it intentionally."
        )
    return requested_credential_name, existing_credential


def _migrate_local_cache(
    *,
    credential_name: str,
    old_did: str,
    new_did: str,
) -> dict[str, Any]:
    """Rebind local messages/contacts and clear stale E2EE artifacts."""
    conn = local_store.get_connection()
    local_store.ensure_schema(conn)
    try:
        rebound = local_store.rebind_owner_did(
            conn,
            old_owner_did=old_did,
            new_owner_did=new_did,
        )
        cleared = local_store.clear_owner_e2ee_data(
            conn,
            owner_did=old_did,
            credential_name=credential_name,
        )
    finally:
        conn.close()

    deleted_state = delete_e2ee_state(credential_name)
    return {
        "messages_rebound": rebound["messages"],
        "contacts_rebound": rebound["contacts"],
        "e2ee_outbox_cleared": cleared["e2ee_outbox"],
        "e2ee_state_deleted": deleted_state,
    }


async def do_recover(
    *,
    handle: str,
    phone: str,
    otp_code: str | None,
    requested_credential_name: str | None,
    replace_existing: bool,
) -> None:
    """Recover a Handle with phone OTP verification."""
    credential_name, old_credential = _resolve_recovery_target(
        handle=handle,
        requested_credential_name=requested_credential_name,
        replace_existing=replace_existing,
    )
    should_replace_existing = old_credential is not None and replace_existing

    logger.info(
        "Recovering handle handle=%s requested_credential=%s target_credential=%s "
        "replace_existing=%s otp_provided=%s",
        handle,
        requested_credential_name,
        credential_name,
        should_replace_existing,
        otp_code is not None,
    )
    config = SDKConfig()
    old_did = str(old_credential["did"]) if old_credential and old_credential.get("did") else None
    old_unique_id = (
        str(old_credential["unique_id"])
        if old_credential and old_credential.get("unique_id")
        else None
    )

    if otp_code is None:
        raise ValueError("OTP code is required for handle recovery.")

    async with create_user_service_client(config) as client:
        identity, recover_result = await recover_handle(
            client,
            config,
            phone=phone,
            otp_code=otp_code,
            handle=handle,
        )

    backup_path = backup_identity(credential_name) if should_replace_existing else None
    if backup_path is not None:
        print(f"Existing credential backed up to: {backup_path}")

    save_identity(
        did=identity.did,
        unique_id=identity.unique_id,
        user_id=identity.user_id,
        private_key_pem=identity.private_key_pem,
        public_key_pem=identity.public_key_pem,
        jwt_token=identity.jwt_token,
        display_name=old_credential.get("name") if old_credential else handle,
        handle=handle,
        name=credential_name,
        did_document=identity.did_document,
        e2ee_signing_private_pem=identity.e2ee_signing_private_pem,
        e2ee_agreement_private_pem=identity.e2ee_agreement_private_pem,
        replace_existing=should_replace_existing,
    )

    cache_migration: dict[str, Any] | None = None
    if should_replace_existing and old_did and old_did != identity.did:
        cache_migration = _migrate_local_cache(
            credential_name=credential_name,
            old_did=old_did,
            new_did=identity.did,
        )
    if should_replace_existing and old_unique_id and old_unique_id != identity.unique_id:
        prune_unreferenced_credential_dir(old_unique_id)

    print("Handle recovered successfully:", file=sys.stderr)
    print(
        json.dumps(
            {
                "did": identity.did,
                "user_id": identity.user_id,
                "handle": recover_result.get("handle", handle),
                "full_handle": recover_result.get("full_handle"),
                "requested_credential_name": requested_credential_name,
                "credential_name": credential_name,
                "replaced_existing_credential": should_replace_existing,
                "message": recover_result.get("message", "OK"),
                "local_backup_path": str(backup_path) if backup_path else None,
                "local_cache_migration": cache_migration,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def main() -> None:
    """CLI entry point."""
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Recover a Handle with phone OTP")
    parser.add_argument("--handle", required=True, type=str, help="Handle local-part")
    parser.add_argument("--phone", required=True, type=str,
                        help="Phone number in international format with country code "
                             "(e.g., +8613800138000 for China, +14155552671 for US). "
                             "China local 11-digit numbers are auto-prefixed with +86. "
                             "Non-mainland China numbers MUST include the country code to receive SMS.")
    parser.add_argument("--otp-code", type=str, default=None, help="OTP code")
    parser.add_argument(
        "--credential",
        type=str,
        default=None,
        help=(
            "Optional credential storage name for the recovered DID. "
            "Defaults to a non-destructive name derived from the handle."
        ),
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help=(
            "Allow overwriting an existing credential selected via --credential. "
            "Without this flag, recovery never replaces an existing local credential."
        ),
    )
    args = parser.parse_args()

    try:
        asyncio.run(
            do_recover(
                handle=args.handle,
                phone=args.phone,
                otp_code=args.otp_code,
                requested_credential_name=args.credential,
                replace_existing=args.replace_existing,
            )
        )
    except ValueError as exc:
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="recover_handle CLI validation failed",
            exit_code=2,
            log_traceback=False,
        )
    except Exception as exc:  # noqa: BLE001
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="recover_handle CLI failed",
        )


if __name__ == "__main__":
    main()
