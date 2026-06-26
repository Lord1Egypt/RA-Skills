#!/usr/bin/env python3
"""
x402_request.py — make an HTTP request that requires x402 payment, sign it, and log the spend.

Handles the full flow:
  1. Probe the endpoint (expect 402)
  2. Decode PAYMENT-REQUIRED header
  3. Sign EIP-712 TransferWithAuthorization with your wallet
  4. Retry with PAYMENT-SIGNATURE header
  5. Log the USDC payment to your treasury JSON

Usage:
    python3 x402_request.py \\
        --url <url>               \\
        --wallet-key <path>       \\
        --rpc <url>               \\
        --output <path>           \\
        --purpose <text>          \\
        [--method <GET|POST|...>] \\
        [--header "Key: Value"]   \\
        [--body <json string>]    \\
        [--network <name>]        \\
        [--max-amount <float>]    \\
        [--pay-to <address>]

Options:
    --url <url>              Target API endpoint (required)
    --wallet-key <path>      Path to JSON file with "private_key" field (required)
    --rpc <url>              EVM-compatible RPC endpoint (required)
    --output <path>          Path to treasury JSON log (required)
    --purpose <text>         Description for the log entry (required)
    --method <method>        HTTP method (default: POST)
    --header <Key: Value>    HTTP header to include (repeatable)
    --body <json>            JSON request body as string
    --network <name>         Network name for the log (default: Base)
    --max-amount <float>     Maximum USDC amount you consent to pay (e.g. 0.02).
                             Script aborts if the server requests more. Recommended.
    --pay-to <address>       Expected payTo address. Script aborts if the server
                             returns a different address. Recommended.

Examples:
    # Send a paid email via Actors.dev
    python3 x402_request.py \\
        --url https://actors.dev/emails \\
        --wallet-key ~/.secrets/eth_wallet.json \\
        --rpc https://mainnet.base.org \\
        --output ~/website/treasury.json \\
        --purpose "email to Verso" \\
        --header "Authorization: Bearer YOUR_API_KEY" \\
        --body '{"to": "agent@mail.actors.dev", "subject": "Hi", "body": "Hello!"}'

    # Solve a captcha via GateSkip
    python3 x402_request.py \\
        --url https://api.gateskip.org/solve/funcaptcha \\
        --wallet-key ~/.secrets/eth_wallet.json \\
        --rpc https://mainnet.base.org \\
        --output ~/website/treasury.json \\
        --purpose "GateSkip captcha solve" \\
        --body '{"site_key": "...", "site_url": "..."}'
"""

import base64
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests
from eth_account import Account
from eth_account.messages import encode_typed_data


def parse_args(argv):
    args = argv[1:]
    opts = {"headers": [], "method": "POST", "network": "Base"}
    i = 0
    while i < len(args):
        flag = args[i]
        if flag in ("--url", "--wallet-key", "--rpc", "--output", "--purpose",
                    "--method", "--body", "--network", "--max-amount", "--pay-to"):
            opts[flag.lstrip("-").replace("-", "_")] = args[i + 1]
            i += 2
        elif flag == "--header":
            opts["headers"].append(args[i + 1])
            i += 2
        else:
            print(f"Unknown argument: {flag}")
            sys.exit(1)
    required = ["url", "wallet_key", "rpc", "output", "purpose"]
    for r in required:
        if r not in opts:
            print(f"⚠️  --{r.replace('_','-')} is required")
            print(__doc__)
            sys.exit(1)
    return opts


def log_to_wallet(log_path: Path, entry: dict):
    if not log_path.exists():
        log_path.write_text(json.dumps({"transactions": []}, indent=2))
    data = json.loads(log_path.read_text())
    data["transactions"].append(entry)
    log_path.write_text(json.dumps(data, indent=2))
    print(f"✅ Logged to {log_path}")


def build_headers(header_list):
    h = {}
    for item in header_list:
        k, v = item.split(":", 1)
        h[k.strip()] = v.strip()
    return h


def sign_x402(accepted: dict, private_key: str, wallet_address: str) -> str:
    """Sign an EIP-712 TransferWithAuthorization and return base64 payment payload."""
    now = int(time.time())
    nonce = "0x" + os.urandom(32).hex()
    chain_id = int(accepted["network"].split(":")[1])
    amount_atomic = int(accepted.get("maxAmountRequired") or accepted["amount"])

    authorization = {
        "from": wallet_address,
        "to": accepted["payTo"],
        "value": amount_atomic,
        "validAfter": now - 60,
        "validBefore": now + accepted["maxTimeoutSeconds"],
        "nonce": nonce,
    }

    structured_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name",              "type": "string"},
                {"name": "version",           "type": "string"},
                {"name": "chainId",           "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "TransferWithAuthorization": [
                {"name": "from",        "type": "address"},
                {"name": "to",          "type": "address"},
                {"name": "value",       "type": "uint256"},
                {"name": "validAfter",  "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce",       "type": "bytes32"},
            ],
        },
        "domain": {
            "name":              accepted["extra"]["name"],
            "version":           accepted["extra"]["version"],
            "chainId":           chain_id,
            "verifyingContract": accepted["asset"],
        },
        "primaryType": "TransferWithAuthorization",
        "message": authorization,
    }

    msg = encode_typed_data(full_message=structured_data)
    signed = Account.sign_message(msg, private_key)
    signature = signed.signature.hex()
    if not signature.startswith("0x"):
        signature = "0x" + signature

    payment_payload = {
        "x402Version": 2,
        "accepted": accepted,
        "payload": {
            "signature": signature,
            "authorization": {
                "from":        authorization["from"],
                "to":          authorization["to"],
                "value":       str(authorization["value"]),
                "validAfter":  str(authorization["validAfter"]),
                "validBefore": str(authorization["validBefore"]),
                "nonce":       nonce,
            },
        },
    }

    return base64.b64encode(json.dumps(payment_payload).encode()).decode()


def find_onchain_tx(rpc_url: str, wallet_address: str, asset: str, pay_to: str,
                    amount_atomic: int, since_block: int) -> str:
    """Try to find the on-chain settlement tx hash by scanning Transfer logs."""
    TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    from_topic = "0x" + wallet_address[2:].zfill(64).lower()

    try:
        r = requests.post(rpc_url, json={"jsonrpc": "2.0", "id": 1, "method": "eth_getLogs",
            "params": [{"fromBlock": hex(since_block), "toBlock": "latest",
                        "address": asset, "topics": [TRANSFER_TOPIC, from_topic]}]}, timeout=15)
        logs = r.json().get("result", [])
        for log in reversed(logs):
            value = int(log["data"], 16)
            to = "0x" + log["topics"][2][-40:]
            if value == amount_atomic and to.lower() == pay_to.lower():
                return log["transactionHash"]
    except Exception:
        pass
    return "pending"


def main():
    opts = parse_args(sys.argv)

    # Load wallet
    key_path = Path(opts["wallet_key"]).expanduser()
    key_data = json.loads(key_path.read_text())
    private_key = key_data.get("private_key") or key_data.get("privateKey")
    if not private_key:
        print(f"Error: no 'private_key' in {key_path}")
        sys.exit(1)
    account = Account.from_key(private_key)

    rpc_url    = opts["rpc"]
    output     = Path(opts["output"]).expanduser().resolve()
    method     = opts["method"].upper()
    url        = opts["url"]
    purpose    = opts["purpose"]
    network    = opts["network"]
    body_str   = opts.get("body")
    headers    = build_headers(opts["headers"])

    if body_str:
        headers.setdefault("Content-Type", "application/json")

    # Step 1: probe — expect 402
    print(f"Probing {url} ...")
    r1 = requests.request(method, url, headers=headers,
                          data=body_str.encode() if body_str else None)
    if r1.status_code != 402:
        print(f"Expected 402, got {r1.status_code}: {r1.text}")
        sys.exit(1)

    req_header = r1.headers.get("PAYMENT-REQUIRED")
    if not req_header:
        print("Missing PAYMENT-REQUIRED header")
        sys.exit(1)

    requirement = json.loads(base64.b64decode(req_header).decode())
    accepted    = requirement["accepts"][0]
    amount_atomic = int(accepted.get("maxAmountRequired") or accepted["amount"])
    amount_human  = amount_atomic / 1e6  # USDC has 6 decimals
    print(f"Payment required: {amount_human} USDC → {accepted['payTo']} on {accepted['network']}")

    # ── Safety checks before signing ─────────────────────────────────────────
    max_amount = opts.get("max_amount")
    if max_amount is not None:
        if amount_human > float(max_amount):
            print(f"❌ Aborted: server requested {amount_human} USDC but --max-amount is {max_amount}")
            sys.exit(1)
        print(f"✅ Amount check passed: {amount_human} ≤ {max_amount} USDC")
    else:
        print(f"⚠️  No --max-amount set. Signing for {amount_human} USDC without a cap.")

    expected_pay_to = opts.get("pay_to")
    if expected_pay_to is not None:
        if accepted["payTo"].lower() != expected_pay_to.lower():
            print(f"❌ Aborted: server payTo is {accepted['payTo']} but --pay-to expects {expected_pay_to}")
            sys.exit(1)
        print(f"✅ payTo check passed: {accepted['payTo']}")
    else:
        print(f"⚠️  No --pay-to set. Signing payment to {accepted['payTo']} without address verification.")

    # Step 2: sign
    print("Signing EIP-712 authorization...")

    # snapshot current block for tx lookup later
    block_r = requests.post(rpc_url, json={"jsonrpc":"2.0","id":1,
                            "method":"eth_blockNumber","params":[]}, timeout=15)
    current_block = int(block_r.json()["result"], 16)

    payment_sig    = sign_x402(accepted, private_key, account.address)
    idempotency_key = str(uuid.uuid4())

    # Step 3: retry with payment
    print("Retrying with payment...")
    headers2 = {**headers, "PAYMENT-SIGNATURE": payment_sig, "Idempotency-Key": idempotency_key}
    r2 = requests.request(method, url, headers=headers2,
                          data=body_str.encode() if body_str else None)

    if r2.status_code not in (200, 201, 202):
        print(f"❌ Payment failed: {r2.status_code}: {r2.text}")
        sys.exit(1)

    print(f"✅ Request succeeded ({r2.status_code})")
    print("Response:", r2.text[:500])

    # Step 4: find on-chain tx (give the network a moment)
    print("Looking up on-chain tx...")
    time.sleep(5)
    tx_hash = find_onchain_tx(rpc_url, account.address, accepted["asset"],
                               accepted["payTo"], amount_atomic, current_block)
    if tx_hash == "pending":
        print("⚠️  On-chain tx not found yet — logged as 'pending'. Update manually if needed.")
    else:
        print(f"On-chain tx: {tx_hash}")

    # Step 5: log
    log_to_wallet(output, {
        "date":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "direction": "sent",
        "amount":    str(amount_human),
        "asset":     "USDC",
        "network":   network,
        "to":        accepted["payTo"],
        "purpose":   purpose,
        "tx_hash":   tx_hash,
    })

    return r2


if __name__ == "__main__":
    main()
