# Payout — CLI Reference

## Overview

Payout lets the agent send USDC to any wallet address on Base network.

**Authorization model**: By default every payout requires **individual user authorization** via the FluxA Wallet UI before the onchain transaction executes. Since CLI 0.4.2, a payout can also carry a pre-signed intent mandate (`--mandate`) to skip the approval URL — same mechanism as x402. Without `--mandate`, user approval is always required.

## End-to-End Flow

```
1. Agent runs `payout` with recipient, amount, and unique payout_id
2. CLI returns status "pending_authorization" + approvalUrl
   (or status "authorized" with approvalUrl=null, if --mandate provided)
3. User opens approvalUrl to authorize  (skip if --mandate)
4. Agent polls `payout-status` until status is "succeeded"
```

## Command Reference

### Create Payout

```bash
fluxa-wallet payout \
  --to "0x4eb5b229d43c30fc629d92bf7ed415d6d7f0cabe" \
  --amount "1000000" \
  --id "reward_20260204_001"
```

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--to` | Yes | — | Recipient wallet address (0x + 40 hex chars) |
| `--amount` | Yes | — | Amount in atomic units (1 USDC = `1000000`) |
| `--id` | Yes | — | Unique payout ID (idempotency key) |
| `--network` | No | `base` | Network name |
| `--asset` | No | USDC address | Token contract address |
| `--mandate` | No | — | Signed mandate ID for auto-approval (skips `approvalUrl`) |
| `--biz-id` | No | — | External business ID for dedup, independent of `--id` |
| `--description` | No | — | Human-readable description stored with the payout |

**Output:**

```json
{
  "success": true,
  "data": {
    "payoutId": "reward_20260204_001",
    "status": "pending_authorization",
    "txHash": null,
    "approvalUrl": "https://wallet.fluxapay.xyz/authorize-payout/reward_20260204_001",
    "expiresAt": 1738713600
  }
}
```

**Opening the approval URL** (see [SKILL.md](SKILL.md) — "Opening Authorization URLs"):

1. Ask the user using `AskUserQuestion`:
   - Question: "I need to open the approval URL to authorize this payout."
   - Options: ["Yes, open the link", "No, show me the URL"]

2. If YES: Run `open "<approvalUrl>"` to open in their browser

3. Wait for user to confirm they've approved, then poll status in Step 2.

### Query Payout Status

```bash
fluxa-wallet payout-status --id "reward_20260204_001"
```

**Output (completed):**

```json
{
  "success": true,
  "data": {
    "payoutId": "reward_20260204_001",
    "status": "succeeded",
    "txHash": "0xabcdef1234567890..."
  }
}
```

### Payout Status Values

| Status | Meaning |
|--------|---------|
| `pending_authorization` | Waiting for user approval |
| `authorized` | Auto-approved via `--mandate`, onchain tx starting |
| `processing` | Approved, onchain tx in progress |
| `succeeded` | Done, `txHash` available |
| `failed` | Transaction failed |
| `expired` | User didn't approve in time |

### Autonomous Payout via Mandate

Pass a signed intent mandate to bypass the approval URL. Useful for scripted/scheduled payouts within a pre-approved budget. See [MANDATE-PLANNING.md](MANDATE-PLANNING.md) before creating a mandate.

```bash
# 1. Create mandate (user signs once)
fluxa-wallet mandate-create --desc "Weekly payout budget" --amount 10000000

# 2. Use the signed mandate on each payout
fluxa-wallet payout \
  --to "0x4eb5b229d43c30fc629d92bf7ed415d6d7f0cabe" \
  --amount "1000000" \
  --id "payroll_2026w16_001" \
  --mandate "mand_xxx" \
  --biz-id "payroll:2026-16:emp-42" \
  --description "Week 16 payroll"
```

Response has `status: "authorized"` and `approvalUrl: null` — agent can poll `payout-status` directly without any user interaction.

## Scripted Example

```bash
#!/bin/bash
CLI="fluxa-wallet"
RECIPIENT="0x4eb5b229d43c30fc629d92bf7ed415d6d7f0cabe"
AMOUNT="1000000"
PAYOUT_ID="payout_$(date +%s)"

# Create payout
RESULT=$($CLI payout --to "$RECIPIENT" --amount "$AMOUNT" --id "$PAYOUT_ID")

if echo "$RESULT" | jq -e '.success' > /dev/null 2>&1; then
  APPROVAL_URL=$(echo "$RESULT" | jq -r '.data.approvalUrl')
  echo "Please approve at: $APPROVAL_URL"

  # Poll for completion
  while true; do
    STATUS=$($CLI payout-status --id "$PAYOUT_ID" | jq -r '.data.status')
    echo "Status: $STATUS"
    [ "$STATUS" = "succeeded" ] || [ "$STATUS" = "failed" ] && break
    sleep 5
  done
else
  echo "Error: $(echo "$RESULT" | jq -r '.error')"
fi
```

## Important Notes

- **Idempotency**: Same `payout_id` returns existing status, not a duplicate.
- **Validate addresses**: Must match `0x[a-fA-F0-9]{40}`.
- **No rollback**: Once succeeded onchain, payouts cannot be reversed.
- **Amount**: Always atomic units. 1 USDC = `1000000`, 0.01 USDC = `10000`.
