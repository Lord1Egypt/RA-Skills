"""BridgeNode x402 Python example — pay per request with Solana USDC.

Buyer-side example using the official x402 Python SDK (x402[svm,httpx]).

Setup:
    pip install "x402[svm,httpx]" "solana==0.39.0" python-dotenv
    cp .env.example .env   # fill SVM_PRIVATE_KEY

Run:
    python main.py

Flow: GET /v1/models (free) → POST /v1/chat/completions → 402 →
sign partial TX (USDC TransferChecked + Memo) → retry with PAYMENT-SIGNATURE →
200 + PAYMENT-RESPONSE.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

from x402 import x402Client
from x402.http import x402HTTPClient
from x402.http.clients import x402HttpxClient
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

load_dotenv()

BASE_URL = os.getenv("BRIDGENODE_URL", "https://bridgenode.cc")
CHAT_PATH = "/v1/chat/completions"
MODELS_PATH = "/v1/models"


def validate_environment() -> str:
    """Return the SVM private key or exit."""
    svm_private_key = os.getenv("SVM_PRIVATE_KEY")
    if not svm_private_key:
        print("Error: SVM_PRIVATE_KEY missing. Copy .env.example to .env and fill it in.")
        sys.exit(1)
    return svm_private_key


async def list_models(http: x402HttpxClient) -> None:
    """GET /v1/models — free, no payment needed."""
    response = await http.get(f"{BASE_URL}{MODELS_PATH}")
    await response.aread()
    print(f"Models & prices: {response.text[:400]}...")


async def chat(http: x402HttpxClient, settle_extractor) -> None:
    """POST /v1/chat/completions — paid via x402 (automatic)."""
    url = f"{BASE_URL}{CHAT_PATH}"
    body = {
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": "Say hello in one sentence."}],
        "max_tokens": 100,
    }
    print(f"\nPOST {url}")
    response = await http.post(url, json=body)
    await response.aread()

    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")

    # PAYMENT-RESPONSE header — settlement receipt (optional, for reconciliation)
    try:
        settle_response = settle_extractor(
            lambda name: response.headers.get(name)
        )
        print(f"\nPayment response: {settle_response.model_dump_json(indent=2)}")
    except ValueError:
        print("\nNo payment response header found")


async def main() -> None:
    """Main entry point."""
    svm_private_key = validate_environment()

    # x402 client (buyer side)
    client = x402Client()

    # Register Solana exact scheme with the agent's keypair
    signer = KeypairSigner.from_base58(svm_private_key)
    register_exact_svm_client(client, signer)
    print(f"Initialized SVM account: {signer.address}")

    http_client = x402HTTPClient(client)

    async with x402HttpxClient(client) as http:
        await list_models(http)
        await chat(http, http_client.get_payment_settle_response)


if __name__ == "__main__":
    asyncio.run(main())
