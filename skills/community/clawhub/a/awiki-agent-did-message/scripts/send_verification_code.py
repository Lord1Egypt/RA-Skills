"""Send a Handle OTP verification code.

Usage:
    uv run python scripts/send_verification_code.py --phone +8613800138000

[INPUT]: SDK (handle OTP send), logging_config
[OUTPUT]: Sends one OTP code and prints the next-step guidance for
          register_handle.py / recover_handle.py
[POS]: Non-interactive CLI for pre-issuing Handle OTP codes

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import argparse
import asyncio
import logging

from utils import SDKConfig, create_user_service_client, send_otp
from utils.cli_errors import exit_with_cli_error
from utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


async def do_send(phone: str) -> None:
    """Send one OTP code to the requested phone number."""
    config = SDKConfig()
    logger.info("Sending handle OTP phone=%s", phone)

    async with create_user_service_client(config) as client:
        await send_otp(client, phone)

    print("Verification code sent successfully.")
    print(f"Phone      : {phone}")
    print("Next step  : rerun register_handle.py or recover_handle.py with --otp-code <received_code>")


def main() -> None:
    """CLI entry point."""
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Send a Handle OTP verification code")
    parser.add_argument(
        "--phone",
        required=True,
        type=str,
        help=(
            "Phone number in international format with country code "
            "(e.g., +8613800138000 for China, +14155552671 for US). "
            "China local 11-digit numbers are auto-prefixed with +86. "
            "Non-mainland China numbers MUST include the country code to receive SMS."
        ),
    )
    args = parser.parse_args()

    try:
        asyncio.run(do_send(args.phone))
    except Exception as exc:  # noqa: BLE001
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="send_verification_code CLI failed",
        )


if __name__ == "__main__":
    main()
