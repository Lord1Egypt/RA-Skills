"""Bind additional contact info (email or phone) to an existing account.

Usage:
    # Send or complete email binding
    uv run python scripts/bind_contact.py --bind-email user@example.com
    uv run python scripts/bind_contact.py --bind-email user@example.com --wait-for-email-verification

    # Send phone OTP, then bind with a pre-issued code
    uv run python scripts/bind_contact.py --bind-phone +8613800138000 --send-phone-otp
    uv run python scripts/bind_contact.py --bind-phone +8613800138000 --otp-code 123456

    # Specify credential name
    uv run python scripts/bind_contact.py --bind-email user@example.com --credential alice

[INPUT]: SDK (binding functions, email verification), credential_store (load identity)
[OUTPUT]: Bind email or phone to existing account
[POS]: Pure non-interactive CLI for post-registration identity binding

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import logging

from utils import SDKConfig, create_user_service_client
from utils.cli_errors import exit_with_cli_error
from utils.handle import (
    bind_email_send,
    bind_phone_send_otp,
    bind_phone_verify,
    ensure_email_verification,
)
from utils.logging_config import configure_logging
from credential_store import load_identity

logger = logging.getLogger(__name__)
PENDING_VERIFICATION_EXIT_CODE = 3


async def do_bind(
    bind_email: str | None = None,
    bind_phone: str | None = None,
    otp_code: str | None = None,
    send_phone_otp: bool = False,
    credential_name: str = "default",
    wait_for_email_verification: bool = False,
    email_verification_timeout: int = 300,
    email_poll_interval: float = 5.0,
) -> bool:
    """Execute the binding flow."""
    config = SDKConfig.load()

    # Load existing identity (must have JWT)
    identity = load_identity(credential_name)
    if identity is None:
        raise ValueError(f"No credential found for '{credential_name}'. Register first.")
    jwt_token = identity.get("jwt_token")
    if not jwt_token:
        raise ValueError("No JWT token found. Refresh the identity first.")

    async with create_user_service_client(config) as client:
        if bind_email:
            if "@" not in bind_email:
                raise ValueError(f"Invalid email format: {bind_email}")
            return await _bind_email(
                client,
                bind_email,
                jwt_token,
                wait_for_verification=wait_for_email_verification,
                verification_timeout=email_verification_timeout,
                poll_interval=email_poll_interval,
            )
        elif bind_phone:
            await _bind_phone(
                client,
                bind_phone,
                jwt_token,
                otp_code=otp_code,
                send_phone_otp=send_phone_otp,
            )
            return True

    return True


async def _bind_email(
    client,
    email: str,
    jwt_token: str,
    *,
    wait_for_verification: bool,
    verification_timeout: int,
    poll_interval: float,
) -> bool:
    """Bind email to an existing account via a pure non-interactive flow."""
    verification_result = await ensure_email_verification(
        client,
        email,
        send_fn=lambda: bind_email_send(client, email, jwt_token),
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
        return False

    print(f"Email {email} bound successfully.")
    return True


async def _bind_phone(
    client,
    phone: str,
    jwt_token: str,
    *,
    otp_code: str | None,
    send_phone_otp: bool,
) -> None:
    """Bind phone to an existing account via explicit non-interactive steps."""
    if send_phone_otp:
        logger.info("Sending phone bind OTP phone=%s", phone)
        await bind_phone_send_otp(client, phone, jwt_token)
        print("OTP sent.")
        print(
            "Next step  : rerun bind_contact.py with "
            f"--bind-phone {phone} --otp-code <received_code>"
        )
        return

    if otp_code is None:
        raise ValueError("OTP code is required for phone binding.")

    result = await bind_phone_verify(client, phone, otp_code, jwt_token)
    if result.get("success"):
        print(f"Phone {result.get('phone', phone)} bound successfully.")
        return
    raise RuntimeError("Binding failed.")


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(
        description="Bind additional contact info (email or phone) to an existing account"
    )

    bind_group = parser.add_mutually_exclusive_group(required=True)
    bind_group.add_argument(
        "--bind-email", type=str, metavar="EMAIL",
        help="Email address to bind (will send activation link)",
    )
    bind_group.add_argument(
        "--bind-phone", type=str, metavar="PHONE",
        help="Phone number to bind (e.g., +8613800138000)",
    )
    parser.add_argument(
        "--otp-code",
        type=str,
        default=None,
        help="Pre-issued OTP code for --bind-phone",
    )
    parser.add_argument(
        "--send-phone-otp",
        action="store_true",
        help="Send a phone binding OTP without completing the bind yet",
    )
    parser.add_argument(
        "--wait-for-email-verification",
        action="store_true",
        help="Poll until the email activation link is clicked instead of exiting immediately",
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

    parser.add_argument(
        "--credential", type=str, default="default",
        help="Credential storage name (default: default)",
    )

    args = parser.parse_args()
    if args.bind_email and (args.otp_code is not None or args.send_phone_otp):
        parser.error("--otp-code and --send-phone-otp can only be used with --bind-phone.")
    if args.bind_phone and args.wait_for_email_verification:
        parser.error("--wait-for-email-verification can only be used with --bind-email.")
    logger.info(
        "bind_contact CLI started email=%s phone=%s credential=%s",
        args.bind_email,
        args.bind_phone,
        args.credential,
    )
    try:
        completed = asyncio.run(do_bind(
            bind_email=args.bind_email,
            bind_phone=args.bind_phone,
            otp_code=args.otp_code,
            send_phone_otp=args.send_phone_otp,
            credential_name=args.credential,
            wait_for_email_verification=args.wait_for_email_verification,
            email_verification_timeout=args.email_verification_timeout,
            email_poll_interval=args.email_poll_interval,
        ))
        if not completed:
            raise SystemExit(PENDING_VERIFICATION_EXIT_CODE)
    except ValueError as exc:
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="bind_contact CLI validation failed",
            exit_code=2,
            log_traceback=False,
        )
    except Exception as exc:  # noqa: BLE001
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="bind_contact CLI failed",
        )


if __name__ == "__main__":
    main()
