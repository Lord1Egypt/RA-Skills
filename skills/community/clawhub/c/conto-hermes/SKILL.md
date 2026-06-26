---
name: conto
description: Enforce fine-grained spending policies before executing any payment, transfer, swap, or bridge. Checks Conto policy engine for approval before money leaves your wallet. Use /conto to manage policies or check payments.
license: MIT
compatibility: Requires curl and network access to the Conto API (conto.finance)
metadata:
  author: conto-finance
  version: '1.8.0'
  homepage: https://conto.finance
---

# Conto Policy Enforcement

You are a spending policy enforcement layer. **Before executing ANY payment, transfer, swap, or bridge**, you MUST check Conto's policy engine for approval. Never send money without policy clearance.

## Prerequisites

Before using this skill, you need:

1. **A Conto account** — Sign up at [conto.finance](https://conto.finance)
2. **A `CONTO_SDK_KEY`** (required) — Generated from the Conto dashboard (format: `conto_agent_...`). See [Getting Started](#getting-started) below.
3. **`curl` and `jq`** — Command-line tools (pre-installed on most systems)
4. **`CONTO_API_URL`** (optional) — API base URL (default: `https://conto.finance`). Must use `https://` in production (localhost allowed for development only).

## When This Skill Activates

This skill applies whenever you are about to:

- Transfer tokens (USDC, ETH, SOL, etc.) to any address
- Swap tokens on any DEX
- Bridge tokens between chains
- Pay for an API call (x402, paid endpoints)
- Make any onchain transaction that moves value

## Getting Started

### Step 1: Install the skill

```bash
hermes skills install well-known:https://conto.finance/.well-known/skills/conto
```

### Step 2: Set up your agent

Run the setup command with your agent name and wallet address:

```bash
{baseDir}/conto-check.sh setup "my-agent" "0xYourWalletAddress" EVM 42431
```

This opens your browser to sign in to Conto. After you approve, the agent is automatically provisioned with:

- An agent record linked to your organization
- Your wallet registered as EXTERNAL custody
- Default spend limits ($100/tx, $500/day)
- An SDK key saved to `~/.hermes/.env`

To find your wallet address, ask the agent: "What is my wallet address?" If you don't have a wallet yet, ask "Show me my wallet balances" — one will be provisioned automatically.

**Arguments:**

- `agent_name`: Name for your agent (e.g., "my-hermes-agent")
- `wallet_address`: Your wallet address (0x... for EVM, base58 for Solana)
- `chain_type`: EVM or SOLANA (default: EVM)
- `chain_id`: Chain ID (default: 42431 for Tempo Testnet). Common values: 8453 (Base), 42431 (Tempo Testnet), 1 (Ethereum)

### Step 3: Verify it works

Test that the skill is connected:

```bash
{baseDir}/conto-check.sh budget
```

Or check your policies:

```
/conto list my policies
```

If you get a response, Conto is working.

### Manual Setup (Alternative)

If the browser setup doesn't work, you can configure manually:

1. Sign in at [conto.finance](https://conto.finance)
2. **Connect your agent**: Agents > Connect Agent > name it, set type to CUSTOM
3. **Register your wallet**: Wallets > Add Wallet > paste address, set EXTERNAL custody
4. **Link wallet to agent**: Agents > your agent > Wallets > link with spend limits
5. **Generate SDK key**: Agents > your agent > SDK Keys > Generate New Key (copy immediately — shown once)
6. Add to `~/.hermes/.env`:

```bash
CONTO_SDK_KEY=conto_agent_your_key_here
CONTO_API_URL=https://conto.finance
```

## Which Wallet Mode Should I Use?

Conto supports two modes depending on who manages the wallet keys:

| Question                        | Mode A                                                     | Mode B                                              |
| ------------------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| Who holds the wallet keys?      | Custody provider (Privy or Sponge)                         | You (via Hermes/Sponge MCP tools)                   |
| How many API calls per payment? | 1 (single call, auto-executes)                             | 3 (approve → transfer → confirm)                    |
| When to use?                    | Wallet `custodyType` is PRIVY or SPONGE in Conto dashboard | Wallet `custodyType` is EXTERNAL in Conto dashboard |

**Most Hermes setups use Mode B** — your agent controls the wallet via Sponge MCP tools and Conto acts as the policy gate before each transaction.

> **Prefer `conto-check.sh`** for Mode B commands (`approve`, `confirm`, `x402`, `budget`, `services`, and all policy commands). The shell helper includes input validation, HTTPS enforcement, timeouts, retry logic, and safe credential handling. Use raw `curl` only for Mode A endpoints (`/request`, `/execute`) and the x402 `/record` endpoint, which have no shell helper yet.

---

## Quick Start: Your First Policy-Checked Payment (Mode B)

Here's a complete end-to-end example of sending 10 USDC with policy enforcement:

**1. Request approval from Conto:**

```bash
{baseDir}/conto-check.sh approve 10 0xRecipientAddress 0xYourWalletAddress 8453 "API credits" "API_PROVIDER"
```

**2. If approved, execute the transfer:**

```
mcp__sponge__tempo_transfer — to: "0xRecipientAddress", amount: "10", token: "pathUSD"
```

**3. Confirm the transaction with Conto:**

```bash
{baseDir}/conto-check.sh confirm <approval_id> <tx_hash> <approval_token>
```

That's it. Conto checked the policy, you sent the payment, and the confirmation keeps spend tracking accurate. The sections below cover each step in detail.

---

## Mode A: Provider-Managed Wallets (PRIVY / SPONGE)

For wallets managed by a custody provider (Privy or Sponge), use a single API call. Conto evaluates policies and instructs the custody provider to execute the transfer.

```bash
curl -sS -X POST "${CONTO_API_URL:-https://conto.finance}/api/sdk/payments/request" \
  -H "Authorization: Bearer $CONTO_SDK_KEY" \
  -H "Content-Type: application/json" \
  --connect-timeout 10 --max-time 30 \
  -d '{
    "amount": <AMOUNT>,
    "recipientAddress": "<RECIPIENT_ADDRESS>",
    "recipientName": "<OPTIONAL_NAME>",
    "purpose": "<WHY_THIS_PAYMENT>",
    "category": "<CATEGORY>",
    "autoExecute": true
  }'
```

**If approved and executed**, the response includes the tx hash directly:

```json
{
  "requestId": "cmm59z...",
  "status": "APPROVED",
  "execution": {
    "transactionId": "cmm5a1...",
    "txHash": "0xdef...",
    "explorerUrl": "https://explore.moderato.tempo.xyz/tx/0xdef...",
    "status": "CONFIRMING"
  }
}
```

No need to call `/execute` or `/confirm` — Conto did everything. Report the tx hash and explorer URL to the user.

**If approved but not auto-executed** (e.g., `autoExecuteError` in response), call `/execute` manually:

```bash
curl -sS -X POST "${CONTO_API_URL:-https://conto.finance}/api/sdk/payments/<REQUEST_ID>/execute" \
  -H "Authorization: Bearer $CONTO_SDK_KEY" \
  -H "Content-Type: application/json" \
  --connect-timeout 10 --max-time 30
```

**If denied**, the response includes `reasons` and `violations` — report them to the user (see denial handling below).

---

## Mode B: External Wallets (EXTERNAL custody)

For wallets where you hold the keys, use the three-step flow: approve → transfer → confirm.

### Step 1: Request Policy Approval

```bash
# Prefer: conto-check.sh approve <amount> <recipient> <sender> <chain_id> [purpose] [category]
curl -sS -X POST "${CONTO_API_URL:-https://conto.finance}/api/sdk/payments/approve" \
  -H "Authorization: Bearer $CONTO_SDK_KEY" \
  -H "Content-Type: application/json" \
  --connect-timeout 10 --max-time 30 \
  -d '{
    "amount": <AMOUNT_IN_USDC>,
    "recipientAddress": "<RECIPIENT_ADDRESS>",
    "senderAddress": "<YOUR_WALLET_ADDRESS>",
    "recipientName": "<OPTIONAL_NAME>",
    "purpose": "<WHY_THIS_PAYMENT>",
    "category": "<CATEGORY>",
    "chainId": <CHAIN_ID>
  }'
```

**Required fields:**

- `amount` — Positive number, the USDC value of the transaction
- `recipientAddress` — The destination address (0x... for EVM, base58 for Solana)
- `senderAddress` — Your wallet address that will send the funds
- `chainId` — Chain ID number. **Required.** Common values: `8453` (Base mainnet), `42431` (Tempo Testnet), `84532` (Base Sepolia), `1` (Ethereum). For Solana, use a base58 `senderAddress` with any chainId — the chain type is detected automatically from the address format.

**Optional fields:**

- `recipientName` — Human-readable name (e.g., "OpenAI API", "Uniswap Router")
- `purpose` — Why this payment is needed (e.g., "Swap 0.5 ETH for USDC on Uniswap")
- `category` — One of: `API_PROVIDER`, `CLOUD`, `SAAS`, `INFRASTRUCTURE`, `MARKETING`, `PAYROLL`, `TRAVEL`, `LODGING`, `TRANSPORT`, `SUPPLIES`, `DATABASE`, `MONITORING`, `PAYMENTS`, `OTHER`
- `context` — JSON object with any additional metadata

**For x402 API payments** (paid HTTP endpoints), use the dedicated pre-authorize endpoint instead:

```bash
# Prefer: conto-check.sh x402 <amount> <recipient> <resource_url> [facilitator] [scheme]
curl -sS -X POST "${CONTO_API_URL:-https://conto.finance}/api/sdk/x402/pre-authorize" \
  -H "Authorization: Bearer $CONTO_SDK_KEY" \
  -H "Content-Type: application/json" \
  --connect-timeout 10 --max-time 30 \
  -d '{
    "amount": <AMOUNT>,
    "recipientAddress": "<PAYEE_ADDRESS>",
    "resourceUrl": "<THE_API_URL>",
    "facilitator": "<FACILITATOR_ADDRESS>",
    "scheme": "<PAYMENT_SCHEME>",
    "category": "API_PROVIDER"
  }'
```

### Step 2: Handle the Approval Response

**If approved** (`"approved": true`):

```json
{
  "approved": true,
  "approvalId": "cmm59z...",
  "approvalToken": "a1b2c3d4...",
  "expiresAt": "2026-04-03T12:10:00.000Z",
  "confirmUrl": "/api/sdk/payments/<approvalId>/confirm",
  "limits": {
    "dailyUsed": 150.0,
    "dailyLimit": 1000.0,
    "dailyRemaining": 850.0
  }
}
```

Save the `approvalId` and `approvalToken` — you need them for Step 3.
The approval expires in 10 minutes. Execute and confirm before then.

**Security note:** The `approvalToken` is cryptographically bound to the original request parameters (amount, recipient, chain). The `/confirm` endpoint validates that the confirmed transaction matches the approved parameters. You cannot reuse an approval token for a different amount or recipient.

### Step 2a: Execute the Transfer

**Now execute the payment using your wallet.** Conto approved the policy — now YOU must send the actual onchain transaction. Do NOT ask the user to execute it.

Use the appropriate MCP tool for the target chain:

**Tempo (pathUSD):**

```
mcp__sponge__tempo_transfer — to: "<RECIPIENT>", amount: "<AMOUNT>", token: "pathUSD"
```

**Base (USDC):**

```
mcp__sponge__evm_transfer — chain: "base", to: "<RECIPIENT>", amount: "<AMOUNT>", currency: "USDC"
```

**Solana (USDC):**

```
mcp__sponge__solana_transfer — chain: "solana", to: "<RECIPIENT>", amount: "<AMOUNT>", currency: "USDC"
```

The transfer will return a transaction hash. Save it for Step 3.
If the transfer fails, report the error to the user. Do NOT call confirm.

### Handling Denials

**If denied** (`"approved": false`):

```json
{
  "approved": false,
  "reasons": ["Daily spend limit exceeded: $950/$1000 used today"],
  "violations": [{ "type": "DAILY_LIMIT", "limit": 1000, "current": 950 }],
  "requiresHumanApproval": false
}
```

**DO NOT execute the payment.** Report the denial to the user:

- Show the `reasons` array (human-readable)
- Show violation details (type, limit, current values)
- If `requiresHumanApproval` is true, tell the user a Conto dashboard admin must approve it

**If the request fails** (HTTP errors):

- 401: SDK key invalid. Ask user to check `CONTO_SDK_KEY`.
- 403: Missing scope. Needs `payments:approve`.
- 429: Rate limited. Wait for the `Retry-After` header value and retry.
- 500/502/503: Retry once after a 2-second delay. If it fails again, inform the user. The `conto-check.sh` helper handles this automatically.

### Step 3: Confirm After Execution

After the transfer succeeds, report the transaction hash back to Conto:

```bash
# Prefer: conto-check.sh confirm <approval_id> <tx_hash> <approval_token>
curl -sS -X POST "${CONTO_API_URL:-https://conto.finance}/api/sdk/payments/<APPROVAL_ID>/confirm" \
  -H "Authorization: Bearer $CONTO_SDK_KEY" \
  -H "Content-Type: application/json" \
  --connect-timeout 10 --max-time 30 \
  -d '{
    "txHash": "<ON_CHAIN_TX_HASH>",
    "approvalToken": "<TOKEN_FROM_STEP_2>"
  }'
```

**Required fields:**

- `txHash` — The onchain transaction hash (0x + 64 hex chars for EVM, or base58 for Solana)
- `approvalToken` — The exact token string from the approval response

**Success response:**

```json
{
  "confirmed": true,
  "transactionId": "cmm5a1...",
  "status": "CONFIRMING",
  "amount": 50.0,
  "currency": "USDC",
  "recipient": "0xabc...",
  "txHash": "0xdef...",
  "explorerUrl": "https://basescan.org/tx/0xdef..."
}
```

Confirmation is important — it updates spend tracking so future policy checks have accurate data. If you skip this, the daily/weekly/monthly counters will be wrong and the agent may overspend.

If confirmation fails with `EXPIRED`, the 10-minute window passed. Inform the user.

## Reporting Results to the User

**On success (approved + executed + confirmed):**

```
Payment sent: [amount] [currency] to [recipient]
TX: [txHash]
Explorer: [explorerUrl]
Daily spend: $[dailyUsed] of $[dailyLimit] ($[dailyRemaining] remaining)
```

**On denial:**

```
Payment blocked by policy:
- [reasons joined by newline]
- Violation: [violation.type] (limit: [limit], current: [current])
```

**On requires approval:**

```
This payment requires human approval ($[amount] exceeds threshold).
A Conto dashboard admin must approve this.
Approval ID: [approvalId]
```

## Mapping Payment Types to Policy Calls

### Transfers (send USDC/ETH/SOL to an address)

- `amount`: The transfer amount in USDC (convert if needed)
- `recipientAddress`: The destination address
- `senderAddress`: Your wallet address
- `category`: `PAYMENTS` or the appropriate category
- `purpose`: "Transfer X USDC to 0xabc..."

### Swaps (DEX trades)

- `amount`: The input amount in USDC equivalent
- `recipientAddress`: The DEX router contract address
- `senderAddress`: Your wallet address
- `category`: `OTHER`
- `purpose`: "Swap X TOKEN_A for TOKEN_B on Uniswap"
- `recipientName`: The DEX name (e.g., "Uniswap V3 Router")

### Bridges (cross-chain transfers)

- `amount`: The bridged amount in USDC equivalent
- `recipientAddress`: The bridge contract address
- `senderAddress`: Your wallet address on the source chain
- `category`: `PAYMENTS`
- `purpose`: "Bridge X USDC from Base to Solana"
- `recipientName`: The bridge provider (e.g., "Relay Bridge")
- `chainId`: The source chain ID

### x402 API Payments

Use the `/api/sdk/x402/pre-authorize` endpoint (see Step 1 above). This evaluates x402-specific rules like per-service caps, endpoint velocity limits, and service allowlists.

If authorized (`"authorized": true`), proceed with the x402 payment flow normally. No separate confirm step is needed for x402 — use the x402 record endpoint instead:

```bash
curl -sS -X POST "${CONTO_API_URL:-https://conto.finance}/api/sdk/x402/record" \
  -H "Authorization: Bearer $CONTO_SDK_KEY" \
  -H "Content-Type: application/json" \
  --connect-timeout 10 --max-time 30 \
  -d '{
    "payments": [{
      "amount": <AMOUNT>,
      "recipientAddress": "<PAYEE>",
      "resourceUrl": "<API_URL>",
      "paymentId": "<X402_PAYMENT_ID>",
      "txHash": "<TX_HASH>",
      "responseCode": 200,
      "facilitator": "<FACILITATOR>"
    }]
  }'
```

## Policy Violation Types Reference

When a payment is denied, the `violations[].type` field tells you exactly what rule was triggered:

| Violation Type                | Meaning                                        |
| ----------------------------- | ---------------------------------------------- |
| `INSUFFICIENT_BALANCE`        | Wallet doesn't have enough funds               |
| `PER_TX_LIMIT`                | Single transaction exceeds max allowed         |
| `DAILY_LIMIT`                 | Would exceed daily spending cap                |
| `WEEKLY_LIMIT`                | Would exceed weekly spending cap               |
| `MONTHLY_LIMIT`               | Would exceed monthly spending cap              |
| `BUDGET_EXCEEDED`             | Would exceed budget allocation                 |
| `TIME_WINDOW`                 | Transaction outside allowed hours              |
| `BLACKOUT_PERIOD`             | Transaction during maintenance/blackout window |
| `EXPIRED_PERMISSION`          | Transaction outside allowed date range         |
| `BLOCKED_COUNTERPARTY`        | Recipient is on the blocklist                  |
| `WHITELIST_VIOLATION`         | Recipient is not on the allowlist              |
| `CATEGORY_RESTRICTION`        | Spend category is not permitted                |
| `VELOCITY_LIMIT`              | Too many transactions in time period           |
| `GEOGRAPHIC_RESTRICTION`      | Geographic/OFAC restriction                    |
| `CONTRACT_NOT_ALLOWED`        | Smart contract not on allowlist                |
| `FAIRSCALE_LOW_SCORE`         | Counterparty Fairscale reputation too low      |
| `X402_PRICE_CEILING`          | x402 API call exceeds price cap                |
| `X402_SERVICE_BLOCKED`        | x402 service is on blocklist                   |
| `X402_SERVICE_NOT_ALLOWED`    | x402 service not on allowlist                  |
| `X402_ENDPOINT_LIMIT`         | x402 endpoint spend limit exceeded             |
| `X402_SESSION_BUDGET`         | x402 session budget exhausted                  |
| `X402_VELOCITY`               | x402 call rate limit exceeded                  |
| `MPP_PRICE_CEILING`           | MPP payment exceeds price cap                  |
| `MPP_SERVICE_BLOCKED`         | MPP service is on blocklist                    |
| `MPP_SERVICE_NOT_ALLOWED`     | MPP service not on allowlist                   |
| `MPP_ENDPOINT_LIMIT`          | MPP endpoint spend limit exceeded              |
| `MPP_SESSION_BUDGET`          | MPP session budget exhausted                   |
| `MPP_VELOCITY`                | MPP call rate limit exceeded                   |
| `MPP_MAX_SESSION_DEPOSIT`     | MPP session deposit exceeds cap                |
| `MPP_MAX_CONCURRENT_SESSIONS` | Too many active MPP sessions                   |
| `MPP_MAX_SESSION_DURATION`    | MPP session exceeds max duration               |
| `MPP_SESSION_INTENT_BLOCKED`  | MPP session intent not allowed                 |
| `MPP_METHOD_NOT_ALLOWED`      | MPP HTTP method not permitted                  |
| `CARD_MCC_RESTRICTION`        | Card merchant category code not allowed        |
| `CARD_MERCHANT_RESTRICTION`   | Card merchant not on allowlist or is blocked   |
| `CARD_AMOUNT_LIMIT`           | Card transaction exceeds amount limit          |

## Error Reporting to the User

When a payment is denied, format the denial clearly:

```
Payment blocked by policy:
- Reason: Daily spend limit exceeded ($950 of $1,000 used today)
- This $100 payment would bring the total to $1,050
- Violation: DAILY_LIMIT (limit: $1,000, current: $950)

To proceed, a dashboard admin can:
1. Increase the daily limit at https://conto.finance
2. Approve this specific transaction manually
```

When `requiresHumanApproval` is true:

```
This payment requires human approval:
- Amount: $5,000 (above approval threshold)
- A Conto dashboard admin must approve this at https://conto.finance
- Approval ID: cmm59z... (share this with your admin)
```

## Managing Policies from Hermes

If your SDK key is an **admin key** (`keyType: "admin"`), you can create, update, and delete policies directly from the CLI. Standard keys can only read policies and check payments.

### List all policies

```bash
{baseDir}/conto-check.sh policies
```

### Create a policy

```bash
{baseDir}/conto-check.sh create-policy '{
  "name": "Max $200 Per Transaction",
  "policyType": "SPEND_LIMIT",
  "priority": 10,
  "isActive": true,
  "rules": [
    {"ruleType": "MAX_AMOUNT", "operator": "LTE", "value": "200", "action": "ALLOW"}
  ]
}'
```

The response includes the new policy's `id`. Save it for assigning to agents.

### Common policy recipes

**Daily spending cap of $1,000:**

```json
{
  "name": "Daily $1K Cap",
  "policyType": "SPEND_LIMIT",
  "priority": 10,
  "isActive": true,
  "rules": [{ "ruleType": "DAILY_LIMIT", "operator": "LTE", "value": "1000", "action": "ALLOW" }]
}
```

**Only allow API and Cloud payments:**

```json
{
  "name": "API+Cloud Only",
  "policyType": "CATEGORY",
  "priority": 5,
  "isActive": true,
  "rules": [
    {
      "ruleType": "ALLOWED_CATEGORIES",
      "operator": "IN_LIST",
      "value": "[\"API_PROVIDER\",\"CLOUD\",\"SAAS\"]",
      "action": "ALLOW"
    }
  ]
}
```

**Block a scam address:**

```json
{
  "name": "Block Scammer",
  "policyType": "COUNTERPARTY",
  "priority": 50,
  "isActive": true,
  "rules": [
    {
      "ruleType": "BLOCKED_COUNTERPARTIES",
      "operator": "IN_LIST",
      "value": "[\"0xbadaddress...\"]",
      "action": "DENY"
    }
  ]
}
```

**Require human approval above $500:**

```json
{
  "name": "High Value Review",
  "policyType": "APPROVAL_THRESHOLD",
  "priority": 8,
  "isActive": true,
  "rules": [
    {
      "ruleType": "REQUIRE_APPROVAL_ABOVE",
      "operator": "GT",
      "value": "500",
      "action": "REQUIRE_APPROVAL"
    }
  ]
}
```

**Business hours only (Mon-Fri 9am-6pm):**

```json
{
  "name": "Business Hours",
  "policyType": "TIME_WINDOW",
  "priority": 5,
  "isActive": true,
  "rules": [
    {
      "ruleType": "TIME_WINDOW",
      "operator": "BETWEEN",
      "value": "{\"start\":\"09:00\",\"end\":\"18:00\"}",
      "action": "ALLOW"
    },
    {
      "ruleType": "DAY_OF_WEEK",
      "operator": "IN_LIST",
      "value": "[\"Mon\",\"Tue\",\"Wed\",\"Thu\",\"Fri\"]",
      "action": "ALLOW"
    }
  ]
}
```

**Cap x402 API spend at $1/request, $50/day per service:**

```json
{
  "name": "x402 Controls",
  "policyType": "SPEND_LIMIT",
  "priority": 10,
  "isActive": true,
  "rules": [
    { "ruleType": "X402_PRICE_CEILING", "operator": "LTE", "value": "1", "action": "ALLOW" },
    {
      "ruleType": "X402_MAX_PER_SERVICE",
      "operator": "LTE",
      "value": "{\"amount\":50,\"period\":\"DAILY\"}",
      "action": "ALLOW"
    }
  ]
}
```

### Add a rule to an existing policy

```bash
{baseDir}/conto-check.sh add-rule <policy_id> '{"ruleType": "WEEKLY_LIMIT", "operator": "LTE", "value": "5000", "action": "ALLOW"}'
```

### Replace all rules on a policy

```bash
{baseDir}/conto-check.sh set-rules <policy_id> '{"rules": [
  {"ruleType": "MAX_AMOUNT", "operator": "LTE", "value": "100", "action": "ALLOW"},
  {"ruleType": "DAILY_LIMIT", "operator": "LTE", "value": "500", "action": "ALLOW"}
]}'
```

### Delete a policy

```bash
{baseDir}/conto-check.sh delete-policy <policy_id>
```

### Available rule types

| Rule Type                     | Operator  | Value Format                                | Use Case                       |
| ----------------------------- | --------- | ------------------------------------------- | ------------------------------ |
| `MAX_AMOUNT`                  | `LTE`     | `"200"`                                     | Per-transaction cap            |
| `DAILY_LIMIT`                 | `LTE`     | `"1000"`                                    | Daily spending cap             |
| `WEEKLY_LIMIT`                | `LTE`     | `"5000"`                                    | Weekly spending cap            |
| `MONTHLY_LIMIT`               | `LTE`     | `"20000"`                                   | Monthly spending cap           |
| `BUDGET_CAP`                  | `LTE`     | `{"amount":10000,"period":"MONTHLY"}`       | Budget allocation              |
| `ALLOWED_CATEGORIES`          | `IN_LIST` | `["API_PROVIDER","CLOUD"]`                  | Category whitelist             |
| `BLOCKED_CATEGORIES`          | `IN_LIST` | `["GAMBLING"]`                              | Category blocklist             |
| `ALLOWED_COUNTERPARTIES`      | `IN_LIST` | `["0xabc..."]`                              | Address whitelist              |
| `BLOCKED_COUNTERPARTIES`      | `IN_LIST` | `["0xbad..."]`                              | Address blocklist              |
| `TIME_WINDOW`                 | `BETWEEN` | `{"start":"09:00","end":"18:00"}`           | Allowed hours                  |
| `DAY_OF_WEEK`                 | `IN_LIST` | `["Mon","Tue","Wed","Thu","Fri"]`           | Allowed days                   |
| `VELOCITY_LIMIT`              | `LTE`     | `{"maxCount":10,"period":"HOUR"}`           | Rate limiting                  |
| `REQUIRE_APPROVAL_ABOVE`      | `GT`      | `"500"`                                     | Human approval threshold       |
| `GEOGRAPHIC_RESTRICTION`      | `IN_LIST` | `["US","CA","GB"]`                          | Country whitelist              |
| `TRUST_SCORE`                 | `GTE`     | `"0.5"`                                     | Min counterparty trust score   |
| `COUNTERPARTY_STATUS`         | `IN_LIST` | `["TRUSTED","VERIFIED"]`                    | Required counterparty status   |
| `CONTRACT_ALLOWLIST`          | `IN_LIST` | `["0xcontract..."]`                         | Smart contract whitelist       |
| `BLACKOUT_PERIOD`             | `BETWEEN` | `{"start":"2026-04-01","end":"2026-04-02"}` | Block during maintenance       |
| `DATE_RANGE`                  | `BETWEEN` | `{"start":"2026-01-01","end":"2026-12-31"}` | Allowed date range             |
| `FAIRSCALE_MIN_SCORE`         | `GTE`     | `"50"`                                      | Min Fairscale reputation score |
| `X402_PRICE_CEILING`          | `LTE`     | `"1"`                                       | Max per x402 API call          |
| `X402_ALLOWED_SERVICES`       | `IN_LIST` | `["api.openai.com"]`                        | x402 service whitelist         |
| `X402_BLOCKED_SERVICES`       | `IN_LIST` | `["untrusted.api"]`                         | x402 service blocklist         |
| `X402_MAX_PER_ENDPOINT`       | `LTE`     | `"10"`                                      | Max spend per x402 endpoint    |
| `X402_VELOCITY_PER_ENDPOINT`  | `LTE`     | `{"maxCount":5,"period":"MINUTE"}`          | x402 endpoint rate limit       |
| `X402_SESSION_BUDGET`         | `LTE`     | `"100"`                                     | x402 session spend cap         |
| `MPP_ALLOWED_SERVICES`        | `IN_LIST` | `["api.example.com"]`                       | MPP service whitelist          |
| `MPP_BLOCKED_SERVICES`        | `IN_LIST` | `["untrusted.api"]`                         | MPP service blocklist          |
| `MPP_MAX_PER_SERVICE`         | `LTE`     | `"50"`                                      | Max spend per MPP service      |
| `MPP_MAX_PER_ENDPOINT`        | `LTE`     | `"10"`                                      | Max spend per MPP endpoint     |
| `MPP_VELOCITY_PER_ENDPOINT`   | `LTE`     | `{"maxCount":5,"period":"MINUTE"}`          | MPP endpoint rate limit        |
| `MPP_SESSION_BUDGET`          | `LTE`     | `"100"`                                     | MPP session spend cap          |
| `MPP_MAX_SESSION_DEPOSIT`     | `LTE`     | `"50"`                                      | Max MPP session deposit        |
| `MPP_MAX_CONCURRENT_SESSIONS` | `LTE`     | `"3"`                                       | Max active MPP sessions        |
| `MPP_MAX_SESSION_DURATION`    | `LTE`     | `"3600"`                                    | Max MPP session seconds        |
| `MPP_BLOCK_SESSION_INTENT`    | `IN_LIST` | `["streaming"]`                             | Block specific MPP intents     |
| `MPP_ALLOWED_METHODS`         | `IN_LIST` | `["GET","POST"]`                            | Allowed MPP HTTP methods       |
| `CARD_ALLOWED_MCCS`           | `IN_LIST` | `["5411","5812"]`                           | Allowed card merchant codes    |
| `CARD_BLOCKED_MCCS`           | `IN_LIST` | `["7995"]`                                  | Blocked card merchant codes    |
| `CARD_ALLOWED_MERCHANTS`      | `IN_LIST` | `["Amazon","Stripe"]`                       | Card merchant whitelist        |
| `CARD_BLOCKED_MERCHANTS`      | `IN_LIST` | `["Casino.com"]`                            | Card merchant blocklist        |
| `CARD_MAX_AMOUNT`             | `LTE`     | `"500"`                                     | Max per card transaction       |

## Critical Rules

1. **Use the right mode for the wallet type.** Mode A (`/request` + `autoExecute`) for PRIVY/SPONGE wallets. Mode B (`/approve` + transfer + `/confirm`) for EXTERNAL wallets.
2. **NEVER skip the policy check.** Every payment must go through Conto first.
3. **NEVER execute a denied payment.** If `approved` is `false` or `status` is `DENIED`, stop.
4. **For Mode B: ALWAYS confirm after execution.** Call `/confirm` with the tx hash to keep spend tracking accurate. Mode A handles this automatically.
5. **Approvals expire quickly.** Mode A (`/request`) approvals expire in **5 minutes**. Mode B (`/approve`) approvals expire in **10 minutes**. Execute promptly after approval.
6. **On API errors, fail closed.** If the Conto API is unreachable after one retry, do NOT proceed with the payment.
7. **Convert to USDC equivalent.** The `amount` field is always in USDC. If you're swapping ETH or another token, convert to the USDC equivalent value for the policy check.
