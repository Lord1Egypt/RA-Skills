#!/usr/bin/env python3
from pathlib import Path

TEMPLATE = """# RapidAPI
RAPIDAPI_KEY=
RAPIDAPI_HOST=cryptexai-buy-sell-signals.p.rapidapi.com

# dYdX v4
DYDX_ADDRESS=
DYDX_SUBACCOUNT=0
DYDX_MNEMONIC_PATH=
DYDX_API_KEY=
DYDX_API_PASSPHRASE=
DYDX_API_SECRET=

# Risk / runtime
MAX_OPEN_POSITIONS=3
ORDER_MARGIN_USD=50
DESIRED_LEVERAGE=5
CLOSE_AFTER_HOURS=72
POLL_INTERVAL_MIN=30

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_IDS=
"""


def main():
    out = Path(".env.crypto-signals")
    if out.exists():
        print(f"Exists: {out}")
        return
    out.write_text(TEMPLATE)
    print(f"Wrote {out}")
    print("Run: chmod 600 .env.crypto-signals")


if __name__ == "__main__":
    main()
