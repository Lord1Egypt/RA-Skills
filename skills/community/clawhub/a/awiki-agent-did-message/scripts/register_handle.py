"""Register a Handle (human-readable DID alias).

Usage:
    # Send OTP first, then register with phone
    uv run python scripts/send_verification_code.py --phone +8613800138000
    uv run python scripts/register_handle.py --handle alice --phone +8613800138000 --otp-code 123456

    # Register with email (pure non-interactive flow)
    uv run python scripts/register_handle.py --handle alice --email user@example.com
    uv run python scripts/register_handle.py --handle alice --email user@example.com --wait-for-email-verification

    # With invite code (for short handles <= 4 chars)
    uv run python scripts/register_handle.py --handle bob --phone +8613800138000 --otp-code 123456 --invite-code ABC123

    # Specify credential name
    uv run python scripts/register_handle.py --handle alice --phone +8613800138000 --otp-code 123456 --credential myhandle

[INPUT]: SDK (handle registration, OTP, email verification), credential_store (save identity),
         logging_config
[OUTPUT]: Register Handle + DID identity and save credentials
[POS]: Pure non-interactive CLI for Handle registration (phone OTP or email activation link)

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import logging
import sys

from utils import SDKConfig, create_user_service_client, register_handle
from utils.cli_errors import exit_with_cli_error
from utils.handle import (
    ensure_email_verification,
    register_handle_with_email,
)
from utils.logging_config import configure_logging
from credential_store import save_identity

logger = logging.getLogger(__name__)
PENDING_VERIFICATION_EXIT_CODE = 3


async def do_register(
    handle: str,
    phone: str | None = None,
    email: str | None = None,
    otp_code: str | None = None,
    invite_code: str | None = None,
    name: str | None = None,
    credential_name: str = "default",
    wait_for_email_verification: bool = False,
    email_verification_timeout: int = 300,
    email_poll_interval: float = 5.0,
) -> bool:
    """Register a Handle with a pure non-interactive flow."""
    logger.info(
        "Registering handle handle=%s credential=%s phone=%s email=%s "
        "invite_code_present=%s wait_for_email_verification=%s",
        handle,
        credential_name,
        bool(phone),
        bool(email),
        bool(invite_code),
        wait_for_email_verification,
    )
    config = SDKConfig.load()
    logger.info(
        "Using service configuration user_service=%s did_domain=%s",
        config.user_service_url,
        config.did_domain,
    )

    # In email mode, OTP is not used even if provided.
    if email and otp_code:
        print("Warning: --otp-code is ignored in email registration mode.")

    async with create_user_service_client(config) as client:
        if email:
            identity = await _register_with_email(
                client,
                config,
                handle,
                email,
                invite_code,
                name,
                wait_for_verification=wait_for_email_verification,
                verification_timeout=email_verification_timeout,
                poll_interval=email_poll_interval,
            )
        elif phone:
            identity = await _register_with_phone(
                client, config, handle, phone, otp_code, invite_code, name,
            )
        else:
            print("Error: either --phone or --email is required.")
            sys.exit(1)

        if identity is None:
            return False

        print(f"  Handle    : {handle}.{config.did_domain}")
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
            display_name=name or handle,
            handle=handle,
            name=credential_name,
            did_document=identity.did_document,
            e2ee_signing_private_pem=identity.e2ee_signing_private_pem,
            e2ee_agreement_private_pem=identity.e2ee_agreement_private_pem,
        )
        print(f"\nCredential saved to: {path}")
        print(f"Credential name: {credential_name}")
        return True


async def _register_with_phone(client, config, handle, phone, otp_code, invite_code, name):
    """Phone-based registration with a pre-issued OTP code."""
    if otp_code is None:
        raise ValueError("OTP code is required for phone registration.")

    logger.info("Registering handle via phone handle=%s phone=%s", handle, phone)
    return await register_handle(
        client=client,
        config=config,
        phone=phone,
        otp_code=otp_code,
        handle=handle,
        invite_code=invite_code,
        name=name or handle,
        is_public=True,
    )


async def _register_with_email(
    client,
    config,
    handle,
    email,
    invite_code,
    name,
    *,
    wait_for_verification: bool,
    verification_timeout: int,
    poll_interval: float,
):
    """Email-based registration with optional polling."""
    verification_result = await ensure_email_verification(
        client,
        email,
        wait=wait_for_verification,
        timeout=verification_timeout,
        poll_interval=poll_interval,
    )

    if not verification_result.verified:
        if wait_for_verification:
            print(
                "Email verification timed out. Click the activation link and rerun "
                "the same command, or increase --email-verification-timeout."
            )
        else:
            print(
                "Email verification pending. Click the activation link, then rerun "
                "the same command. Or pass --wait-for-email-verification to poll "
                "automatically."
            )
        return None

    logger.info("Registering handle via email handle=%s email=%s", handle, email)
    return await register_handle_with_email(
        client=client,
        config=config,
        email=email,
        handle=handle,
        invite_code=invite_code,
        name=name or handle,
        is_public=True,
    )


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Register a Handle (human-readable DID alias)")
    parser.add_argument("--handle", required=True, type=str,
                        help="Handle local-part (e.g., alice)")

    # Phone or email (mutually exclusive group)
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument("--phone", type=str,
                            help="Phone number in international format with country code "
                                 "(e.g., +8613800138000 for China, +14155552671 for US). "
                                 "China local 11-digit numbers are auto-prefixed with +86.")
    auth_group.add_argument("--email", type=str,
                            help="Email address (will send activation link if not yet verified)")

    parser.add_argument("--otp-code", type=str, default=None,
                        help="Pre-issued OTP code (phone mode only; required for non-interactive use)")
    parser.add_argument("--invite-code", type=str, default=None,
                        help="Invite code (required for short handles <= 4 chars)")
    parser.add_argument("--name", type=str, default=None,
                        help="Display name (defaults to handle)")
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential storage name (default: default)")
    parser.add_argument(
        "--wait-for-email-verification",
        action="store_true",
        help="Poll until the activation link is clicked instead of exiting immediately",
    )
    parser.add_argument(
        "--email-verification-timeout",
        type=int,
        default=300,
        help="Seconds to wait when --wait-for-email-verification is set (default: 300)",
    )
    parser.add_argument(
        "--email-poll-interval",
        type=float,
        default=5.0,
        help="Polling interval in seconds for email verification (default: 5.0)",
    )

    args = parser.parse_args()
    logger.info(
        "register_handle CLI started handle=%s credential=%s",
        args.handle,
        args.credential,
    )
    try:
        completed = asyncio.run(
            do_register(
                handle=args.handle,
                phone=args.phone,
                email=args.email,
                otp_code=args.otp_code,
                invite_code=args.invite_code,
                name=args.name,
                credential_name=args.credential,
                wait_for_email_verification=args.wait_for_email_verification,
                email_verification_timeout=args.email_verification_timeout,
                email_poll_interval=args.email_poll_interval,
            )
        )
        if not completed:
            raise SystemExit(PENDING_VERIFICATION_EXIT_CODE)
    except ValueError as exc:
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="register_handle CLI validation failed",
            exit_code=2,
            log_traceback=False,
        )
    except Exception as exc:  # noqa: BLE001
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="register_handle CLI failed",
        )


if __name__ == "__main__":
    main()
