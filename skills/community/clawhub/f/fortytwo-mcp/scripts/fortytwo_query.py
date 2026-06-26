#!/usr/bin/env python3
"""Fortytwo Prime MCP — complete query flow.

Usage:
    python scripts/fortytwo_query.py "What is MCP?" --network base
    python scripts/fortytwo_query.py "Explain more" --session-id <uuid>

Diagnostics go to stderr, answer goes to stdout.
"""

import argparse
import base64
import json
import os
import secrets
import sys
import time
import urllib.request
import uuid

try:
    from eth_account import Account
    from web3 import Web3
except ImportError:
    print("ERROR: missing dependencies. Run: pip install eth-account web3", file=sys.stderr)
    sys.exit(1)

GATEWAY = "https://mcp.fortytwo.network/mcp"
SESSION_FILE = "/tmp/.fortytwo_session"

NETWORKS = {
    "base":  {"chain_id": 8453, "rpc": "https://mainnet.base.org",  "network": "eip155:8453"},
    "monad": {"chain_id": 143,  "rpc": "https://rpc.monad.xyz",     "network": "eip155:143"},
}

ERC20_META_ABI = [
    {"name": "name",    "outputs": [{"type": "string"}], "inputs": [], "stateMutability": "view", "type": "function"},
    {"name": "version", "outputs": [{"type": "string"}], "inputs": [], "stateMutability": "view", "type": "function"},
]


def jsonrpc(method, params, req_id=1):
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}).encode()


def post(body, headers=None, timeout=600):
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(GATEWAY, data=body, headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        # http.client.HTTPMessage is case-insensitive on get(), but dict() can lose keys
        resp_headers = {k.lower(): v for k, v in resp.headers.items()}
        return resp.status, resp_headers, resp.read().decode()
    except urllib.error.HTTPError as e:
        resp_headers = {k.lower(): v for k, v in e.headers.items()}
        return e.code, resp_headers, e.read().decode()


def load_token_meta(rpc_url, asset_address):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    token = w3.eth.contract(address=Web3.to_checksum_address(asset_address), abi=ERC20_META_ABI)
    name = token.functions.name().call()
    try:
        version = token.functions.version().call()
    except Exception:
        version = "1"
    return name, version


def sign_payment(private_key, chain_id, usdc_name, usdc_version, usdc_address, accept):
    account = Account.from_key(private_key)
    nonce = "0x" + secrets.token_hex(32)
    valid_before = int(time.time()) + int(accept["maxTimeoutSeconds"])

    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name",              "type": "string"},
                {"name": "version",           "type": "string"},
                {"name": "chainId",           "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "ReceiveWithAuthorization": [
                {"name": "from",        "type": "address"},
                {"name": "to",          "type": "address"},
                {"name": "value",       "type": "uint256"},
                {"name": "validAfter",  "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce",       "type": "bytes32"},
            ],
        },
        "primaryType": "ReceiveWithAuthorization",
        "domain": {
            "name": usdc_name,
            "version": usdc_version,
            "chainId": chain_id,
            "verifyingContract": usdc_address,
        },
        "message": {
            "from": account.address,
            "to": accept["payTo"],
            "value": int(accept["amount"]),
            "validAfter": 0,
            "validBefore": valid_before,
            "nonce": nonce,
        },
    }

    signed = account.sign_typed_data(full_message=typed_data)
    r_hex = "0x" + signed.r.to_bytes(32, "big").hex()
    s_hex = "0x" + signed.s.to_bytes(32, "big").hex()

    payload = {
        "x402Version": 2,
        "scheme": "exact",
        "network": accept["network"],
        "payload": {
            "client":      account.address,
            "maxAmount":   str(int(accept["amount"])),
            "validAfter":  "0",
            "validBefore": str(valid_before),
            "nonce":       nonce,
            "v": int(signed.v),
            "r": r_hex,
            "s": s_hex,
        },
    }
    return base64.b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode()


def save_session(session_id):
    try:
        with open(SESSION_FILE, "w") as f:
            f.write(session_id)
    except OSError:
        pass


def load_session():
    try:
        with open(SESSION_FILE) as f:
            return f.read().strip() or None
    except OSError:
        return None


def output(answer, session_id):
    if session_id:
        print(f"[session: {session_id}]\n")
        save_session(session_id)
    print(answer)


def main():
    parser = argparse.ArgumentParser(description="Query Fortytwo Prime via MCP")
    parser.add_argument("query", help="The question to ask")
    parser.add_argument("--network", choices=["base", "monad"], default="base",
                        help="Payment network (default: base)")
    parser.add_argument("--session-id", help="Reuse existing session (auto-detected from previous run)")
    parser.add_argument("--no-session", action="store_true", help="Force new payment, ignore saved session")
    args = parser.parse_args()

    private_key = os.environ.get("evm_private_key")
    if not private_key:
        print("ERROR: evm_private_key not set", file=sys.stderr)
        sys.exit(1)

    rpc_url = NETWORKS[args.network]["rpc"]

    # Auto-load saved session unless --no-session
    session_id = None if args.no_session else (args.session_id or load_session())

    # Step 1: initialize
    status, _, body = post(jsonrpc("initialize", {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "local-code", "version": "1.0"},
    }))
    if status != 200:
        print(f"ERROR: initialize failed ({status}): {body}", file=sys.stderr)
        sys.exit(1)
    print("OK: initialized", file=sys.stderr)

    # Step 2: tools/list
    status, _, body = post(jsonrpc("tools/list", {}, 2))
    if status != 200:
        print(f"ERROR: tools/list failed ({status}): {body}", file=sys.stderr)
        sys.exit(1)
    print("OK: tools/list", file=sys.stderr)

    # Step 3: tools/call
    call_body = jsonrpc("tools/call", {
        "name": "ask_fortytwo_prime",
        "arguments": {"query": args.query},
    }, 3)

    # Try session reuse first
    if session_id:
        print(f"Reusing session: {session_id}", file=sys.stderr)
        idem = str(uuid.uuid4())
        status, hdrs, body = post(call_body, {
            "x-session-id": session_id,
            "x-idempotency-key": idem,
        })
        if status == 200:
            result = json.loads(body)
            sid = hdrs.get("x-session-id", session_id)
            output(result.get("result", {}).get("content", [{}])[0].get("text", body), sid)
            return
        print(f"Session expired/invalid ({status}), making new payment...", file=sys.stderr)

    # Expect 402
    status, hdrs, body = post(call_body)
    if status != 402:
        print(f"ERROR: expected 402, got {status}: {body}", file=sys.stderr)
        sys.exit(1)

    # Parse 402 challenge
    pr_header = hdrs.get("payment-required", "")
    if pr_header:
        challenge = json.loads(base64.b64decode(pr_header))
    else:
        challenge = json.loads(body)

    target_net = NETWORKS[args.network]["network"]
    accept = next((a for a in challenge.get("accepts", []) if a["network"] == target_net), None)
    if not accept:
        print(f"ERROR: network {target_net} not in 402 accepts", file=sys.stderr)
        sys.exit(1)

    amount_usdc = int(accept["amount"]) / 1e6
    print(f"Escrow deposit: {amount_usdc:.2f} USDC on {args.network}", file=sys.stderr)

    # Step 4-5: sign and send with retry
    usdc_address = accept["asset"]
    usdc_name, usdc_version = load_token_meta(rpc_url, usdc_address)

    for attempt in range(1, 4):
        payment_sig = sign_payment(
            private_key, NETWORKS[args.network]["chain_id"],
            usdc_name, usdc_version, usdc_address, accept,
        )
        idem = str(uuid.uuid4())
        status, hdrs, body = post(call_body, {
            "payment-signature": payment_sig,
            "x-idempotency-key": idem,
        }, timeout=600)

        if status == 200:
            break
        if status in (400, 502) and attempt < 3:
            print(f"Transient error ({status}), retry {attempt}/3...", file=sys.stderr)
            time.sleep(2 * attempt)
            continue
        print(f"ERROR: payment call failed ({status}): {body}", file=sys.stderr)
        sys.exit(1)

    result = json.loads(body)
    answer = result.get("result", {}).get("content", [{}])[0].get("text", "")
    sid = hdrs.get("x-session-id", "")
    output(answer, sid)


if __name__ == "__main__":
    main()
