---
name: agent-tool-marketplace
description: "Agent Tool Marketplace catalog for AgentPMT — list available paid tools, fetch tool schemas, invoke any tool with a signed request, and consume responses. Use when an agent needs to discover and call third-party capabilities through the AgentPMT marketplace."
version: 1.0.2
homepage: https://www.agentpmt.com/external-agent-api
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/external-agent-api"}}
---

# Agent Tool Marketplace

## Freshness

Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

Use this skill when an agent needs to discover available AgentPMT tools, inspect their schemas and pricing, and invoke a selected tool with wallet-signed authentication.

## Overview

AgentPMT exposes a dynamic marketplace catalog through external endpoints. Agents can list tools, choose an action, sign a request with their wallet, and spend credits from their AgentPMT balance.

## Discover Tools

```python
import requests

tools_response = requests.get("https://www.agentpmt.com/api/external/tools", timeout=30)
tools_response.raise_for_status()
tools = tools_response.json()
```

Each catalog entry includes the tool identity, description, available actions, schema, pricing, and availability metadata. Select the product whose schema matches the task.

## Prepare Wallet Authentication

Create or reuse an AgentAddress wallet, buy credits if needed, then create a session nonce.

```python
session_response = requests.post("https://www.agentpmt.com/api/external/auth/session", json={
    "wallet_address": wallet_address.lower(),
}, timeout=30)
session_response.raise_for_status()
session_nonce = session_response.json()["session_nonce"]
```

## Invoke a Tool

Build parameters from the product schema. Canonicalize and hash the parameters before signing.

```python
import hashlib
import json

product_slug = "<productSlug>"
action_slug = "<actionSlug>"
request_path = f"/external/tools/{product_slug}/actions/{action_slug}/invoke"
parameters = {}
canonical = json.dumps(parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
payload_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

Hash only the exact `parameters` object. Do not include `wallet_address`, `session_nonce`, `request_id`, `signature`, or a client-added `action` field in the hash.

Canonical JSON recursively sorts object keys and uses no whitespace. AgentPMT accepts both JS raw UTF-8 serialization and Python escaped serialization (`json.dumps(parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`).

Sign this EIP-191 message:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
method:POST
path:/external/tools/{productSlug}/actions/{actionSlug}/invoke
payload:{payload_hash}
```

The called URL includes `/api`; the preferred signed path does not:

| Called URL | Signed `path:` line |
|---|---|
| `https://www.agentpmt.com/api/external/tools/{productSlug}/actions/{actionSlug}/invoke` | `path:/external/tools/{productSlug}/actions/{actionSlug}/invoke` |

AgentPMT also accepts bounded `/api`, raw-action-slug, and trailing-slash signed path variants only when they resolve to the same product/action. Do not sign a different product or action.

Call the invocation endpoint:

```python
response = requests.post(f"https://www.agentpmt.com/api/external/tools/{product_slug}/actions/{action_slug}/invoke", json={
    "wallet_address": wallet_address.lower(),
    "session_nonce": session_nonce,
    "request_id": "unique-tool-request-id",
    "signature": "0x...",
    "parameters": parameters,
}, timeout=120)
response.raise_for_status()
result = response.json()
```

## Catalog Workflow

1. List tools with `/api/external/tools`.
2. Pick a product and action that matches the task.
3. Read the action schema and construct parameters.
4. Check or buy credits if the wallet balance is insufficient.
5. Sign the invocation message.
6. Submit the request and parse the result.

## Error Handling

| Status | Meaning | Recovery |
|---|---|---|
| 400 | Invalid request or schema mismatch | Rebuild parameters from the tool schema. |
| 401 `EXTERNAL_SIGNATURE_SESSION_NONCE_INVALID` | Session nonce is unknown | Create a new session nonce and sign again with a fresh request_id. |
| 401 `EXTERNAL_SIGNATURE_SESSION_NONCE_EXPIRED` | Session nonce expired | Create a new session nonce and sign again with a fresh request_id. |
| 401 `EXTERNAL_SIGNATURE_MALFORMED` | Signature could not be recovered | Rebuild the EIP-191 signature from `expected_message`; do not change parameters after hashing. |
| 401 `EXTERNAL_SIGNATURE_WALLET_MISMATCH` | Signature recovered a different wallet | Use `expected_message`, `expected_wallet`, `recovered_wallet_for_expected_message`, accepted path candidates, and accepted payload hash forms to correct wallet casing, key selection, path, or canonical JSON. |
| 402 | Insufficient credits | Use Agent Payment to buy credits through x402. |
| 409 `EXTERNAL_SIGNATURE_REQUEST_REPLAY` | Replay or duplicate request | Generate a fresh request_id and retry once. |
| 500 | Tool or platform error | Retry later with a fresh request_id. |

## Related Skills

- Agent Payment: ../agent-payment
- x402 Bazaar: ../x402-bazaar
- AgentPMT marketplace: https://www.agentpmt.com
