# x402 Payment — EIP-712 ReceiveWithAuthorization

## Canonical helper

Use this as the source-of-truth implementation for building `payment-signature`.

Before signing, query the token contract on the selected network and use its actual:

- `name()`
- `version()`
- `decimals()`

Do not hardcode `"USD Coin"` or other mainnet assumptions. Some testnet USDC deployments return
`name() = "USDC"`, and using the wrong EIP-712 domain values will produce an invalid signature.

## Resolve token metadata on-chain

```python
from web3 import Web3

ERC20_META_ABI = [
    {"name": "name", "outputs": [{"type": "string"}], "inputs": [], "stateMutability": "view", "type": "function"},
    {"name": "version", "outputs": [{"type": "string"}], "inputs": [], "stateMutability": "view", "type": "function"},
    {"name": "decimals", "outputs": [{"type": "uint8"}], "inputs": [], "stateMutability": "view", "type": "function"},
]


def load_token_metadata(rpc_url: str, usdc_address: str) -> tuple[str, str, int]:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    token = w3.eth.contract(
        address=Web3.to_checksum_address(usdc_address),
        abi=ERC20_META_ABI,
    )
    name = token.functions.name().call()
    try:
        version = token.functions.version().call()
    except Exception:
        version = "1"  # fallback if version() not implemented on this deployment
    decimals = token.functions.decimals().call()
    return (name, version, decimals)
```

For the current Fortytwo USDC flow, `decimals` is expected to be `6`, so `2000000 = 2.0 USDC`.

```python
import base64
import json
import secrets
import time
from eth_account import Account


def build_payment_signature(
    private_key: str,
    chain_id: int,
    usdc_name: str,
    usdc_version: str,
    usdc_address: str,
    accept: dict,  # one item from payment-required.accepts
) -> str:
    account = Account.from_key(private_key)

    nonce = "0x" + secrets.token_hex(32)
    valid_after = 0
    valid_before = int(time.time()) + int(accept["maxTimeoutSeconds"])

    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "ReceiveWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
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
            "validAfter": valid_after,
            "validBefore": valid_before,
            "nonce": nonce,
        },
    }

    # Important: use full_message= keyword to pass the complete EIP-712 structure.
    # Do NOT use positional args like sign_typed_data(domain, types, message) —
    # the nonce field requires the full typed_data with EIP712Domain types included.
    signed = account.sign_typed_data(full_message=typed_data)
    r_hex = "0x" + signed.r.to_bytes(32, "big").hex()
    s_hex = "0x" + signed.s.to_bytes(32, "big").hex()

    payment_sig = {
        "x402Version": 2,
        "scheme": "exact",
        "network": accept["network"],  # e.g. "eip155:8453" (Base) or "eip155:143" (Monad)
        "payload": {
            "client": account.address,
            "maxAmount": str(int(accept["amount"])),
            "validAfter": str(valid_after),
            "validBefore": str(valid_before),
            "nonce": nonce,
            "v": int(signed.v),
            "r": r_hex,
            "s": s_hex,
        },
    }

    return base64.b64encode(
        json.dumps(payment_sig, separators=(",", ":")).encode()
    ).decode()
```

## Key Rules

- `nonce` — single-use `bytes32`, generate a fresh value for each payment
- `validBefore` — must be in the future at settle time (typically `now + maxTimeoutSeconds`)
- `amount` is passed as a string in `maxAmount`, parsed as int
- `amount` / `maxAmount` are in the token's smallest unit; for USDC, `2000000 = 2.0 USDC`
- `network` in `payment_sig` must match `accepts[n].network`
- `domain.name` and `domain.version` must come from the token contract on the chosen chain

## Common Mistakes

1. **Wrong payload structure** — the x402 payload for Fortytwo uses `{client, maxAmount, validAfter, validBefore, nonce, v, r, s}`. Do NOT use the standard EIP-3009 format `{signature, authorization: {from, to, value, ...}}` — the server will silently reject it with 402.

2. **Missing `x-idempotency-key` header** — required on every `tools/call`. The server generates a fallback UUID if omitted, but providing your own ensures idempotent retries on network errors.

3. **Using positional args for `sign_typed_data`** — use `account.sign_typed_data(full_message=typed_data)` with the complete EIP-712 structure (including `EIP712Domain` in `types`). The positional-args API `sign_typed_data(domain, types, message)` may handle the `bytes32` nonce field differently.

4. **Hardcoded token metadata** — always query `name()` and `version()` from the token contract on-chain. Different chains may return different values (e.g. `"USD Coin"` vs `"USDC"`). Wrong domain values produce a valid-looking but rejected signature.

5. **Wrong network** — verify the user has USDC on the selected chain before signing. Check balance with `balanceOf()` and offer to switch networks if insufficient.
