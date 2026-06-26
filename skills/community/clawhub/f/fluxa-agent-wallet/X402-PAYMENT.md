# x402 Payment — Reference

## Overview

x402 is an HTTP-native payment protocol. When an agent requests a paid API, the server responds with HTTP 402 and payment requirements. The agent signs a payment via FluxA Wallet and retries with a payment header.

The CLI supports both **x402 v1** and **x402 v2** formats automatically:

| Version | 402 Response Format | Retry Header | Detection |
|---------|-------------------|--------------|-----------|
| v1 | Response body (JSON) | `X-Payment` | Default (no `x402Version` or `x402Version !== 2`) |
| v2 | `PAYMENT-REQUIRED` header (base64) | `PAYMENT-SIGNATURE` | `x402Version === 2` in payload |

Both versions use **intent mandates**: the user pre-approves a spending plan (budget + time window), then the agent can make autonomous payments within those limits.

This document uses the **CLI** method.

## When to Use This Document

| Scenario | Document |
|----------|----------|
| Pay for a paid API (HTTP 402) | **This document** |
| Send USDC to a wallet address | [PAYOUT.md](PAYOUT.md) |

## End-to-End Flow

```
1. Create an intent mandate → user signs at authorizationUrl
2. Agent hits paid API → receives HTTP 402
3. Agent inspects 402 response:
   - Has PAYMENT-REQUIRED header? → x402 v2 (use header value as payload)
   - No header? → x402 v1 (use response body as payload)
4. Agent calls fluxa-wallet x402 with mandateId + payload
5. Agent retries API with payment header → gets data
   - v1: X-Payment header (use xPaymentB64)
   - v2: PAYMENT-SIGNATURE header (use paymentPayloadB64)
```

**Important**: The `x402` command requires both `--mandate` and `--payload`. You must create a mandate first (Step 1) before executing payments.

## Step 0 — Mandate Planning

Before create intent mandate, mandate planning must be completed to estimate the required budget. read MANDATE-PLANNING.md

## Step 1 — Create Intent Mandate

```bash
fluxa-wallet mandate-create \
  --desc "Spend up to 0.10 USDC for Polymarket recommendations for 30 days" \
  --amount 100000 \
  --seconds 2592000 \
  --category trading_data
```

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--desc` | Yes | — | Natural language description of the spend plan |
| `--amount` | Yes | — | Budget limit in atomic units |
| `--seconds` | No | `28800` (8h) | Validity duration in seconds |
| `--category` | No | `general` | Category tag |
| `--currency` | No | `USDC` | Currency. Supported: `USDC`, `XRP`, `FLUXA_MONETIZE_CREDITS` (aliases: `credits`, `fluxa-monetize-credits`) |

**Output:**

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "mandateId": "mand_xxxxxxxxxxxxx",
    "authorizationUrl": "https://wallet.fluxapay.xyz/onboard/intent?oid=...",
    "expiresAt": "2026-02-04T00:10:00.000Z",
    "agentStatus": "ready"
  }
}
```

**Opening the authorization URL** (see [SKILL.md](SKILL.md) — "Opening Authorization URLs"):

1. Ask the user using `AskUserQuestion`:
   - Question: "I need to open the authorization URL to sign the spending mandate."
   - Options: ["Yes, open the link", "No, show me the URL"]

2. If YES: Run `open "<authorizationUrl>"` to open in their browser

3. Wait for user to confirm they've signed (TTL: 10 minutes), then proceed to Step 2.

## Step 2 — Check Mandate Status

**Important:** Use `--id`, not `--mandate`:

```bash
fluxa-wallet mandate-status --id mand_xxxxxxxxxxxxx
```

**Output:**

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "mandate": {
      "mandateId": "mand_xxxxxxxxxxxxx",
      "status": "signed",
      "naturalLanguage": "Spend up to 0.10 USDC...",
      "currency": "USDC",
      "limitAmount": "100000",
      "spentAmount": "0",
      "remainingAmount": "100000",
      "validFrom": "2026-02-04T00:00:00.000Z",
      "validUntil": "2026-03-06T00:00:00.000Z"
    }
  }
}
```

Wait until `mandate.status` is `"signed"`.

## Step 3 — Handle 402 Response & Make Payment

When you receive an HTTP 402 response, determine the x402 version:

### Detecting the version

```
HTTP 402 received
  ├─ Has PAYMENT-REQUIRED header? → x402 v2
  │    payload = header value (base64 string)
  └─ No header? → x402 v1
       payload = response body (JSON string)
```

### Making the payment

The same CLI command handles both versions. Pass the payload as-is — the CLI auto-detects v2 (by checking `x402Version === 2` in the decoded payload).

```bash
fluxa-wallet x402 \
  --mandate mand_xxxxxxxxxxxxx \
  --payload "$PAYLOAD"
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--mandate` | Yes | Mandate ID from Step 1 |
| `--payload` | Yes | The 402 payload — either JSON string or base64-encoded string |

**`--payload` accepts both formats:**
- Raw JSON: `'{"accepts":[...]}'` (v1) or `'{"x402Version":2,"resource":{...},"accepts":[...]}'` (v2)
- Base64: `'eyJ4NDAyVmVyc2lvbi...'` (e.g. raw `PAYMENT-REQUIRED` header value)

**Currency matching (v1 only):** The CLI automatically selects the `accepts` entry that matches the mandate's currency. If the 402 response contains multiple entries (e.g., USDC + FLUXA_MONETIZE_CREDITS), only the one matching the mandate currency is used. For v2, asset selection is handled by the server.

**Critical:** Do NOT extract individual fields. Pass the entire 402 payload:

**Wrong:**
```bash
# This will fail with "Invalid payload: missing accepts array"
--payload '{"maxAmountRequired":"10000","payTo":"0x..."}'
```

**Correct:**
```bash
# Pass the full 402 payload with accepts array
--payload '{"accepts":[{...}]}'
```

### v1 output

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "xPaymentB64": "eyJ4NDAyVmVyc2lvbi...",
    "xPayment": { "x402Version": 1, "scheme": "exact", "network": "base", "payload": { "..." } },
    "paymentRecordId": 123,
    "expiresAt": 1700000060
  }
}
```

### v2 output

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "paymentPayloadB64": "eyJ4NDAyVmVyc2lvbi...",
    "paymentRecordId": 42,
    "expiresAt": 1711000300
  }
}
```

Note: v2 output does not include `paymentPayload` (filtered by CLI). Use `paymentPayloadB64` directly.

## Step 4 — Retry with Payment Header

Use the correct header name based on the x402 version:

**v1 server** (uses `X-Payment`):
```bash
curl -H "X-Payment: <xPaymentB64>" \
  https://fluxa-x402-api.gmlgtm.workers.dev/polymarket_recommendations_last_1h
```

**v2 server** (uses `PAYMENT-SIGNATURE`):
```bash
curl -H "PAYMENT-SIGNATURE: <paymentPayloadB64>" \
  https://laso.finance/auth
```

## Mandate Ownership Caveat

Mandates are tied to the agent that created them. A mandate created via CLI belongs to the CLI's configured agent, while a mandate created via API belongs to the API-authenticated agent (identified by JWT).

If using both methods, ensure you're using the same agent identity.

## Scripted Example (CLI)

```bash
#!/bin/bash
CLI="fluxa-wallet"
API_URL="https://example.com/paid-endpoint"
MANDATE_ID="mand_xxxxxxxxxxxxx"

# Hit the API, capture headers and body separately
HTTP_RESPONSE=$(curl -s -D /tmp/x402_headers -w "\n%{http_code}" "$API_URL")
HTTP_CODE=$(echo "$HTTP_RESPONSE" | tail -n1)
BODY=$(echo "$HTTP_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "402" ]; then
  # Check for PAYMENT-REQUIRED header (x402 v2)
  PR_HEADER=$(grep -i '^payment-required:' /tmp/x402_headers | sed 's/^[^:]*: *//' | tr -d '\r')

  if [ -n "$PR_HEADER" ]; then
    # v2: use header value (base64) as payload
    PAYLOAD="$PR_HEADER"
    HEADER_NAME="PAYMENT-SIGNATURE"
    FIELD="paymentPayloadB64"
  else
    # v1: use response body as payload
    PAYLOAD="$BODY"
    HEADER_NAME="X-Payment"
    FIELD="xPaymentB64"
  fi

  # Sign payment
  RESULT=$($CLI x402 --mandate "$MANDATE_ID" --payload "$PAYLOAD")
  TOKEN=$(echo "$RESULT" | jq -r ".data.$FIELD")

  # Retry with payment header
  curl -H "$HEADER_NAME: $TOKEN" "$API_URL"
fi
```

## Error Handling

| Error in output | Meaning | Action |
|----------------|---------|--------|
| `Missing required parameters: --desc, --amount` | mandate-create called without required flags | Add both `--desc "..."` and `--amount <number>` |
| `Missing required parameter: --id` | mandate-status called with wrong flag | Use `--id`, not `--mandate` |
| `Missing required parameters: --mandate, --payload` | x402 called without prerequisites | Create a mandate first using `mandate-create` |
| `Invalid payload: missing accepts array` | Payload is incomplete or malformed | Pass the **complete** 402 payload including `accepts` array |
| `Invalid --payload: not valid JSON or base64-encoded JSON` | Payload is neither valid JSON nor valid base64 | Check the payload string |
| `Invalid v2 payload: missing resource.url` | v2 payload missing `resource.url` object | Ensure the v2 payload has `resource: { url: "..." }` |
| `mandate_not_signed` | User hasn't signed yet | Ask user to open `authorizationUrl` |
| `mandate_expired` | Time window passed | Create a new mandate |
| `mandate_budget_exceeded` | Budget exhausted | Create a new mandate with higher limit |
| `mandate_insufficient_budget` | Payment amount exceeds remaining budget | Create a new mandate with higher limit |
| `mandate_not_found` | Mandate ID doesn't exist or belongs to different agent | Verify mandate ID and agent identity |
| `currency_mismatch` / `No accepts entry matches mandate currency` | v1: 402 payload has no entry for the mandate's currency | Ensure the mandate currency matches one of the 402 `accepts` currencies |
| `no_supported_payment_option` | v2: no `accepts` entry matches supported assets | Check that the 402 server supports Base USDC |
| `invalid_payment_request` | v2: payload structure invalid | Verify `x402Version`, `resource`, and `accepts` fields |
| `agent_not_registered` | No Agent ID | Run `init` first |

## Network Format Note

The 402 response may use different network formats:
- `eip155:8453` — Chain ID format (EIP-155), typically used by x402 v2
- `base` — Human-readable network name, typically used by x402 v1

Both refer to Base network. The CLI and API accept either format.
