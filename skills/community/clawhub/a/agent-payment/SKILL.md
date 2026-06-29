---
name: agent-payment
description: "Agent Payment for AI agents on AgentPMT — create an EVM wallet via AgentAddress, buy USDC-denominated credits via the x402 protocol, sign authenticated requests, and check balance. Use when an autonomous agent needs to pay for tools, workflows, or services on the AgentPMT marketplace."
version: 1.0.2
homepage: https://www.agentpmt.com/external-agent-api
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/external-agent-api"}}
---

# Agent Payment

## Freshness

Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

Use this skill when an autonomous agent needs to create a wallet, buy credits, sign requests, and pay for AgentPMT tools or workflows.

## Overview

AgentPMT lets external agents operate with an EVM wallet and credit balance. The agent creates an AgentAddress wallet, purchases credits through x402, creates a session nonce, signs EIP-191 requests, and spends credits on marketplace tools.

## Prerequisites

```bash
pip install requests eth-account
```

## Step 1 — Get a Wallet

Create an AgentAddress wallet with the public external endpoint. Store the private key and mnemonic in a secret manager, never in prompt text or logs.

```python
import requests

response = requests.post("https://www.agentpmt.com/api/external/agentaddress", timeout=30)
response.raise_for_status()
wallet = response.json()
wallet_address = wallet["evmAddress"].lower()
private_key = wallet["evmPrivateKey"]
```

## Step 2 — Buy Credits via x402

Send an initial credit purchase request. If the response is HTTP 402, read `PAYMENT-REQUIRED`, sign the USDC authorization, and retry with `PAYMENT-SIGNATURE`.

```python
purchase = {
    "wallet_address": wallet_address,
    "credits": 500,
    "payment_method": "x402",
}
first = requests.post("https://www.agentpmt.com/api/external/credits/purchase", json=purchase, timeout=30)
if first.status_code == 402:
    payment_required = first.headers["PAYMENT-REQUIRED"]
    paid = requests.post(
        "https://www.agentpmt.com/api/external/credits/purchase",
        json=purchase,
        headers={"PAYMENT-SIGNATURE": "<base64 signed authorization>"},
        timeout=30,
    )
    paid.raise_for_status()
else:
    first.raise_for_status()
```

## Step 3 — Create a Session

```python
session_response = requests.post("https://www.agentpmt.com/api/external/auth/session", json={
    "wallet_address": wallet_address,
}, timeout=30)
session_response.raise_for_status()
session_nonce = session_response.json()["session_nonce"]
```

## Step 4 — Sign Requests

Balance and tool invocation use different EIP-191 message shapes. Lowercase the wallet and use a fresh `request_id`.

Balance uses the scoped shape with an empty payload:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
action:balance
product:-
payload:
```

Tool invocation uses the path-bound shape:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
method:POST
path:/external/tools/{productSlug}/actions/{actionSlug}/invoke
payload:{payload_hash}
```

For tool invocation, call the full URL `https://www.agentpmt.com/api/external/tools/{productSlug}/actions/{actionSlug}/invoke`, but prefer signing the canonical path `/external/tools/{productSlug}/actions/{actionSlug}/invoke`. Drop the host and query string. AgentPMT also accepts bounded `/api`, raw-action-slug, and trailing-slash variants only when they resolve to the same product/action.

`payload_hash` is the lowercase SHA-256 of the exact `parameters` object. Canonical JSON recursively sorts object keys and uses no whitespace; AgentPMT accepts both JS raw UTF-8 serialization and Python escaped serialization (`json.dumps(parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`). Do not hash wrapper fields like `wallet_address`, `session_nonce`, `request_id`, or `signature`.

## Step 5 — Check Balance

```python
balance_payload = {
    "wallet_address": wallet_address,
    "session_nonce": session_nonce,
    "request_id": "unique-balance-request-id",
    "signature": "0x...",
}
balance_response = requests.post("https://www.agentpmt.com/api/external/credits/balance", json=balance_payload, timeout=30)
balance_response.raise_for_status()
```

## Security Rules

- Never print, log, or return private keys, mnemonics, session secrets, or signatures.
- Lowercase the wallet address in every signed message.
- Use a fresh `request_id` for every signed request.
- Refresh the session nonce only for `EXTERNAL_SIGNATURE_SESSION_NONCE_INVALID` or `EXTERNAL_SIGNATURE_SESSION_NONCE_EXPIRED`.
- For `EXTERNAL_SIGNATURE_MALFORMED` or `EXTERNAL_SIGNATURE_WALLET_MISMATCH`, use the returned `expected_message`, accepted path candidates, accepted payload hash forms, `expected_wallet`, and recovered wallet field to self-correct before retrying.
- For `EXTERNAL_SIGNATURE_REQUEST_REPLAY`, retry once with a fresh `request_id`.

## Related Skills

- x402 Bazaar: ../x402-bazaar
- Agent Tool Marketplace: ../agent-tool-marketplace
- AgentPMT marketplace: https://www.agentpmt.com
