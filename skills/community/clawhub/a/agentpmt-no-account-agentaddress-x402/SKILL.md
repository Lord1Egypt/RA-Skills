---
name: agentpmt-no-account-agentaddress-x402
description: "Use AgentPMT without an account: connect OpenClaw and autonomous AI agents to AgentPMT tools, workflows, skills, agent-to-agent work, and paid capabilities through a revocable AgentAddress with credits or a funded x402 wallet. Covers signed-credit requests, direct x402 payments, approval gates, payee/network/token/amount validation, public endpoints, tool discovery, workflow access, REST calls, and safe payment setup for AgentPMT's agent management iPaaS."
version: 1.0.3
homepage: https://www.agentpmt.com/agentaddress
compatibility: "Requires HTTP access to AgentPMT external endpoints and either an AgentAddress already loaded with AgentPMT credits or a funded x402-capable EVM wallet. Python examples use requests and eth-account for signing."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agentaddress"}}
---

# Use AgentPMT Without An Account: AgentAddress And x402

## Freshness

Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

Use this skill when an agent does not have an AgentPMT account Bearer Token and needs to pay for tools with an AgentAddress or x402 payment.

## What This Is For

This path is for autonomous agents that need one of these:

- An AgentAddress that already has AgentPMT credits.
- A funded crypto wallet that can complete x402 payments.

If the agent has an AgentPMT account Bearer Token, use the account MCP/REST setup skill instead.

## Safety Model

Prefer AgentAddress for autonomous agents. An AgentAddress can be connected to an AgentPMT account as an authorized agent, used for scoped AgentPMT tool and workflow calls, and revoked from the user's AgentPMT account when access should stop. The AgentAddress wallet should remain empty or low-balance and should not be used as a general-purpose crypto wallet.

Use direct x402 only when the user intentionally wants a wallet-funded on-chain payment. Direct x402 should use a dedicated low-balance wallet, not a personal or treasury wallet.

Required safety rules:

- Use a dedicated AgentAddress or low-balance x402 wallet.
- Keep private keys, mnemonics, signatures, payment headers, and session nonces in a real secret manager.
- Never paste keys, mnemonics, signatures, nonces, or payment headers into prompts, logs, commits, transcripts, or generated files.
- Enforce allowed product slugs, action slugs, networks, tokens, payees, and maximum payment amounts before signing.
- Require explicit user approval or a pre-approved policy before signing any direct x402 payment.
- Revoke AgentAddress access from the AgentPMT account when the agent should no longer operate.

## Requirements

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --require-hashes -r requirements.txt
```

Use pinned, reviewed dependencies for production. Example `requirements.txt` shape:

```text
requests==<reviewed-version> --hash=sha256:<reviewed-hash>
eth-account==<reviewed-version> --hash=sha256:<reviewed-hash>
```

For quick local testing only, an operator may install reviewed versions manually in an isolated virtual environment. Do not install packages into a shared agent runtime without review.

## Create Or Load An AgentAddress

Preferred production path:

1. The user creates or authorizes an AgentAddress through AgentPMT.
2. The user connects that AgentAddress to their AgentPMT account as an authorized agent when account-backed credits should be used.
3. The operator stores the AgentAddress wallet address and private key in a secret manager.
4. The agent loads only the secret references it needs at runtime.

Load an existing AgentAddress from secrets:

```python
import os

wallet_address = os.environ["AGENTPMT_AGENTADDRESS_WALLET"].lower()
private_key = os.environ["AGENTPMT_AGENTADDRESS_PRIVATE_KEY"]
```

If an operator uses the AgentPMT helper endpoint to create a new AgentAddress, do it during provisioning, not inside a prompt-driven agent task. Store the returned private key immediately in a secret manager, keep the wallet empty or low-balance, and avoid sending unrelated funds to that address.

## Approval And Spending Policy

Before signing any paid request, enforce a local policy. At minimum, configure:

- Allowed product slugs.
- Allowed action slugs per product.
- Maximum payment amount per call.
- Allowed x402 network ids.
- Allowed x402 token contract addresses.
- Allowed payee addresses.
- Whether explicit user approval is required before signing.

Example policy helpers:

```python
APPROVED_PRODUCTS = {"<product-slug>"}
APPROVED_ACTIONS = {"<product-slug>": {"<action-slug>"}}
APPROVED_NETWORKS = {"eip155:8453"}
APPROVED_ASSETS = {"0x<approved-token-contract>".lower()}
APPROVED_PAYEES = {"0x<approved-payee-address>".lower()}
MAX_X402_AMOUNT_BASE_UNITS = 10_000
REQUIRE_EXPLICIT_PAYMENT_APPROVAL = True


def require_approved_tool(product_slug: str, action_slug: str) -> None:
    if product_slug not in APPROVED_PRODUCTS:
        raise RuntimeError(f"Product is not approved: {product_slug}")
    if action_slug not in APPROVED_ACTIONS.get(product_slug, set()):
        raise RuntimeError(f"Action is not approved: {product_slug}/{action_slug}")


def require_payment_approval(accepted: dict) -> None:
    amount = int(accepted["amount"])
    if accepted["network"] not in APPROVED_NETWORKS:
        raise RuntimeError(f"Network is not approved: {accepted['network']}")
    if accepted["asset"].lower() not in APPROVED_ASSETS:
        raise RuntimeError(f"Token is not approved: {accepted['asset']}")
    if accepted["payTo"].lower() not in APPROVED_PAYEES:
        raise RuntimeError(f"Payee is not approved: {accepted['payTo']}")
    if amount > MAX_X402_AMOUNT_BASE_UNITS:
        raise RuntimeError(f"Payment amount exceeds local limit: {amount}")
    if REQUIRE_EXPLICIT_PAYMENT_APPROVAL:
        # Replace this with your human-in-the-loop approval or signed policy receipt.
        raise RuntimeError("Explicit payment approval required before signing x402")
```

## Discover Tools

```python
tools_response = requests.get("https://www.agentpmt.com/api/external/tools", timeout=30)
tools_response.raise_for_status()
tools = tools_response.json()
```

Use the product-specific skill for the target tool to get the product slug, action slug, schema, and sample parameters.

## Signed Request Contract

Balance and tool invocation use different signed messages. Balance uses the scoped shape. Tool invocation uses the path-bound shape. Do not use the balance shape for tool invocation.

Balance message:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
action:balance
product:-
payload:
```

Tool invoke message:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
method:POST
path:/external/tools/{productSlug}/actions/{actionSlug}/invoke
payload:{payload_hash}
```

The message is a UTF-8 string joined with `\n`, with no trailing newline. Sign it as an EIP-191 personal message: `encode_defunct(text=message)` in Python or `wallet.signMessage(message)` in ethers. Do not use EIP-712 for signed-credit requests.

Called URL versus signed path:

| Called URL | Signed `path:` line |
|---|---|
| `https://www.agentpmt.com/api/external/tools/google-drive/actions/list-files/invoke` | `path:/external/tools/google-drive/actions/list-files/invoke` |

Path rules:

- Prefer dropping the host and `/api` prefix.
- Do not include a query string.
- Prefer no trailing slash.
- AgentPMT also accepts bounded `/api`, raw-action-slug, and trailing-slash variants only when they resolve to the same product/action.
- Do not sign a different product or action.

Payload hash rules:

- Hash only the exact `parameters` object sent inside the request body.
- Do not hash wrapper fields: `wallet_address`, `session_nonce`, `request_id`, or `signature`.
- Do not add an `action` field to `parameters` unless that action's schema explicitly requires a parameter named `action`.
- Arrays keep their order. Object keys sort recursively. JSON values must be JSON-safe; do not use `undefined`, `NaN`, or `Infinity`.
- AgentPMT accepts both JS raw UTF-8 canonical JSON and Python escaped canonical JSON (`json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`).

Python canonicalizer:

```python
import hashlib
import json


def canonical_json(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def payload_hash(parameters: dict) -> str:
    return hashlib.sha256(canonical_json(parameters).encode("utf-8")).hexdigest()
```

JavaScript canonicalizer:

```javascript
import crypto from "node:crypto";

function sortJson(value) {
  if (Array.isArray(value)) return value.map(sortJson);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value).sort().map((key) => [key, sortJson(value[key])])
    );
  }
  return value;
}

export function canonicalJson(value) {
  return JSON.stringify(sortJson(value));
}

export function payloadHash(parameters) {
  return crypto.createHash("sha256").update(canonicalJson(parameters), "utf8").digest("hex");
}
```

## Signed-Credit Flow

Use this when the AgentAddress already has AgentPMT credits.

Create a session nonce:

```python
session_response = requests.post("https://www.agentpmt.com/api/external/auth/session", json={
    "wallet_address": wallet_address,
}, timeout=30)
session_response.raise_for_status()
session_nonce = session_response.json()["session_nonce"]
```

Canonicalize action parameters and sign the request:

```python
import hashlib
import json
from eth_account import Account
from eth_account.messages import encode_defunct

product_slug = "<product-slug>"
action_slug = "<action-slug>"
require_approved_tool(product_slug, action_slug)
request_path = f"/external/tools/{product_slug}/actions/{action_slug}/invoke"
parameters = {}
canonical = json.dumps(parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
payload_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
request_id = "unique-tool-request-id"

message = "\n".join([
    "agentpmt-external",
    f"wallet:{wallet_address.lower()}",
    f"session:{session_nonce}",
    f"request:{request_id}",
    "method:POST",
    f"path:{request_path}",
    f"payload:{payload_hash}",
])
signature = Account.sign_message(
    encode_defunct(text=message),
    private_key=private_key,
).signature.hex()
```

Invoke the tool:

```python
invoke_url = f"https://www.agentpmt.com/api/external/tools/{product_slug}/actions/{action_slug}/invoke"
response = requests.post(invoke_url, json={
    "wallet_address": wallet_address,
    "session_nonce": session_nonce,
    "request_id": request_id,
    "signature": signature,
    "parameters": parameters,
}, timeout=120)
response.raise_for_status()
```

## Direct x402 Flow

Use this when the agent has a funded x402-capable wallet and wants to pay at the tool action URL.

Direct x402 is available only when the target vendor product is enabled for x402. The tool URL is the same canonical action URL used by signed-credit calls:

```text
POST https://www.agentpmt.com/api/external/tools/{productSlug}/actions/{actionSlug}/invoke
```

Do not include signed-credit fields (`wallet_address`, `session_nonce`, `request_id`, `signature`) when paying with x402. Send only the action parameters in the JSON body and the x402 payment header on the paid retry.

The first request returns `402 Payment Required` with a canonical x402 challenge. The response body is JSON, and the `PAYMENT-REQUIRED` header contains the same challenge base64-encoded. Select only an approved entry from `accepts[]`; never sign the first entry blindly.

```python
import base64
import json
import secrets
import time

import requests
from eth_account import Account

product_slug = "<product-slug>"
action_slug = "<action-slug>"
require_approved_tool(product_slug, action_slug)
invoke_url = f"https://www.agentpmt.com/api/external/tools/{product_slug}/actions/{action_slug}/invoke"

# The wallet must be dedicated to x402 payments and hold only the approved token/network.
x402_private_key = "<0x-funded-wallet-private-key>"
x402_account = Account.from_key(x402_private_key)
payer_wallet = x402_account.address.lower()

parameters = {
    # action-specific input fields go here
}

first = requests.post(invoke_url, json=parameters, timeout=120)
if first.status_code != 402:
    first.raise_for_status()
    result = first.json()
else:
    payment_required = first.json()
    approved = [
        item for item in payment_required["accepts"]
        if item["network"] in APPROVED_NETWORKS
        and item["asset"].lower() in APPROVED_ASSETS
        and item["payTo"].lower() in APPROVED_PAYEES
        and int(item["amount"]) <= MAX_X402_AMOUNT_BASE_UNITS
    ]
    if not approved:
        raise RuntimeError("No x402 payment option matched the local approval policy")
    accepted = approved[0]
    require_payment_approval(accepted)

    chain_id = int(accepted["network"].split(":")[1])
    valid_before = str(int(time.time()) + min(240, int(accepted.get("maxTimeoutSeconds", 300))))
    authorization = {
        "from": payer_wallet,
        "to": accepted["payTo"].lower(),
        "value": str(accepted["amount"]),
        "validAfter": "0",
        "validBefore": valid_before,
        "nonce": "0x" + secrets.token_hex(32),
    }

    signed = Account.sign_typed_data(
        x402_private_key,
        domain_data={
            "name": accepted.get("extra", {}).get("name", "USDC"),
            "version": str(accepted.get("extra", {}).get("version", "2")),
            "chainId": chain_id,
            "verifyingContract": accepted["asset"],
        },
        message_types={
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
            ],
        },
        message_data={
            "from": authorization["from"],
            "to": authorization["to"],
            "value": int(authorization["value"]),
            "validAfter": int(authorization["validAfter"]),
            "validBefore": int(authorization["validBefore"]),
            "nonce": authorization["nonce"],
        },
    )
    signature = signed.signature.hex()
    if not signature.startswith("0x"):
        signature = "0x" + signature

    x402_payload = {
        "x402Version": 2,
        "accepted": accepted,
        "resource": payment_required["resource"],
        "payload": {
            "signature": signature,
            "authorization": authorization,
        },
    }
    x_payment = base64.b64encode(
        json.dumps(x402_payload, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")

    paid = requests.post(
        invoke_url,
        json=parameters,
        headers={"X-PAYMENT": x_payment},
        timeout=120,
    )
    paid.raise_for_status()
    result = paid.json()

print(result)
```

Use the payment challenge values exactly:

- `authorization.to` must equal `accepted.payTo`.
- `authorization.value` must equal `accepted.amount`.
- `accepted.network` must match an approved network.
- `accepted.asset` must match an approved token contract.
- `accepted.payTo` must match an approved payee.
- `accepted.amount` must be less than or equal to the configured per-call maximum.
- The EIP-712 domain must use `accepted.extra.name`, `accepted.extra.version`, the numeric chain id from `accepted.network`, and `accepted.asset` as `verifyingContract`.
- The paid retry must send the base64-encoded JSON envelope in `X-PAYMENT`. `PAYMENT-SIGNATURE`, `PAYMENT`, and `X-PAYMENT` are accepted aliases, but `X-PAYMENT` is the preferred header.
- Generate a fresh 32-byte nonce for every payment. Never reuse a nonce or signed payment authorization.
- Always sign one of the live `accepts[]` requirements returned by the challenge.

Successful direct x402 responses do not debit the buyer's AgentPMT credit ledger and do not return top-level `charged_credits`, `balance_credits`, `balance_usd`, `credit_source`, or `price_credits`. The tool response is returned with x402 payment metadata:

```json
{
  "success": true,
  "response": {
    "status_code": 200,
    "data": {
      "success": true,
      "output": {}
    },
    "success": true
  },
  "x402": {
    "transaction": "0x...",
    "network": "eip155:8453",
    "resource_url": "https://www.agentpmt.com/api/external/tools/{productSlug}/actions/{actionSlug}/invoke",
    "payment": {
      "token": "USDC",
      "asset": "0x...",
      "amount_base_units": "10000",
      "amount_usd": 0.01,
      "payer_wallet_address": "0x...",
      "pay_to": "0x..."
    }
  }
}
```

If the tool call cannot be completed, the response is an error. Retry with a fresh challenge and nonce after fixing the request or funding issue.

## Balance Check

Balance checks use the same signed request pattern with the balance endpoint:

```python
balance_response = requests.post("https://www.agentpmt.com/api/external/credits/balance", json={
    "wallet_address": wallet_address,
    "session_nonce": session_nonce,
    "request_id": "unique-balance-request-id",
    "signature": "0x...",
}, timeout=30)
balance_response.raise_for_status()
```

## Workflows

No-account workflow access uses the external workflow endpoints and wallet-signed requests. Discover workflows with `GET https://www.agentpmt.com/api/external/workflows`, fetch the selected workflow with the signed fetch endpoint, then start/end sessions with the signed workflow endpoints. Use workflow-specific docs where available.

## Error Handling

| Status | Meaning | Recovery |
|---|---|---|
| 400 | Schema mismatch or invalid request | Rebuild parameters from the product skill. |
| 401 `EXTERNAL_SIGNATURE_SESSION_NONCE_INVALID` | Session nonce is unknown | Create a new session nonce, use a fresh `request_id`, rebuild the message, and sign again. |
| 401 `EXTERNAL_SIGNATURE_SESSION_NONCE_EXPIRED` | Session nonce expired | Create a new session nonce, use a fresh `request_id`, rebuild the message, and sign again. |
| 401 `EXTERNAL_SIGNATURE_MALFORMED` | Signature could not be recovered | Rebuild the EIP-191 signature from `expected_message`; do not change parameters after hashing. |
| 401 `EXTERNAL_SIGNATURE_WALLET_MISMATCH` | Signature recovered a different wallet | Use `expected_message`, `expected_wallet`, `recovered_wallet_for_expected_message`, accepted path candidates, accepted payload hash forms, and `payload_canonical_top_level_keys` to correct wallet casing, key selection, signed path, or canonical JSON. |
| 402 | Payment required | Complete the x402 challenge or fund the AgentAddress credits. |
| 409 `EXTERNAL_SIGNATURE_REQUEST_REPLAY` | Replay detected | Use a fresh request id and sign again. |
| 500 | Tool/platform error | Retry later with a fresh request id. |

## Core AgentPMT Skill Downloads

Use these links when a related AgentPMT setup skill is not installed beside this one.

| Skill | Local path | ClawHub page |
|---|---|---|
| What AgentPMT is | ../what-is-agentpmt | https://clawhub.ai/agentpmt/what-is-agentpmt |
| AgentPMT account MCP/REST setup | ../agentpmt-account-mcp-rest-api-setup | https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup |
| No-account AgentAddress/x402 flow | ../agentpmt-no-account-agentaddress-x402 | https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402 |

OpenClaw install commands:

```bash
openclaw skills install what-is-agentpmt
openclaw skills install agentpmt-account-mcp-rest-api-setup
openclaw skills install agentpmt-no-account-agentaddress-x402
```

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402
```
