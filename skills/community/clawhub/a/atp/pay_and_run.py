#!/usr/bin/env python3
"""
Bundled helper for the ATP OpenClaw skill (see SKILL.md) -- makes a real,
paid x402 call to ATP. Exists because plain `curl` cannot pay: hitting the
x402 endpoint with bare curl gets back a 402 with a price and stops there,
since curl has no way to sign the payment authorization the response asks
for. This script does that signing step, using the `x402` package's own
client (not custom crypto).

Usage:
    ATP_WALLET_PRIVATE_KEY=0x... python3 pay_and_run.py '{"fn_name":"...","kind":"constant",...}'

Requires: pip install "x402[evm,httpx]"

Network: targets eip155:84532 (Base Sepolia TESTNET) to match this
project's current live deployment (see docs/deploy/render.md /
ATP_X402_NETWORK) -- update BASE_SEPOLIA below if/when the deployment
moves to a mainnet-funded ATP_X402_PAY_TO. That's an operator decision on
the ATP side, not something this script can detect on its own.

The wallet behind ATP_WALLET_PRIVATE_KEY needs real (or, right now,
testnet) USDC on that network to actually pay -- generate a fresh wallet
for this, never reuse one holding anything you can't afford to lose, and
never commit this key anywhere.
"""

import asyncio
import json
import os
import sys

BASE_SEPOLIA = "eip155:84532"
API_URL = "https://atp-api-mor3.onrender.com/x402/tasks/run"


async def main():
    if len(sys.argv) != 2:
        print("usage: pay_and_run.py '<json task body>'", file=sys.stderr)
        sys.exit(1)

    try:
        body = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"argument is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    private_key = os.environ.get("ATP_WALLET_PRIVATE_KEY")
    if not private_key:
        print("ATP_WALLET_PRIVATE_KEY is not set", file=sys.stderr)
        sys.exit(1)

    from eth_account import Account
    from x402 import x402Client
    from x402.mechanisms.evm.exact import ExactEvmScheme
    from x402.http.clients import x402HttpxClient

    signer = Account.from_key(private_key)
    client = x402Client()
    client.register(BASE_SEPOLIA, ExactEvmScheme(signer=signer))

    async with x402HttpxClient(client) as http:
        resp = await http.post(API_URL, json=body)
        print(resp.text)
        if resp.status_code >= 400:
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
