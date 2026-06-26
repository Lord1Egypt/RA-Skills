---
name: ClawVault Payments
description: Security middleware for AI agents handling money. Non-custodial crypto wallets and virtual Visa cards with spending limits, whitelists, and human approval.
homepage: https://clawvault.cc
source: https://github.com/andrewszk/clawvault-mcp-server
metadata:
  openclaw:
    emoji: "🦞"
    primaryEnv: CLAWVAULT_API_KEY
    requires:
      env:
        - name: CLAWVAULT_API_KEY
          description: "Your ClawVault API key (format: cv_live_xxxxx). Get one at https://clawvault.cc/agents"
          required: true
---

# ClawVault Agent Skill

You have access to ClawVault, a security middleware for AI agents. ClawVault protects TWO spending channels:
1. **Crypto payments** - USDC transfers on Base and Solana blockchains
2. **Agent Card** - Virtual Visa card for any merchant worldwide (SaaS, APIs, cloud, etc.)

Both channels use the same rules engine. Every transaction is validated against user-defined rules. Transactions within rules auto-approve; transactions outside rules require human approval via Telegram or dashboard.

## Security Model

- **Non-custodial**: Your keys never leave your wallet
- **Rule-enforced**: Spending limits, whitelists, time windows enforced on-chain
- **Human-in-the-loop**: Anything outside rules requires explicit approval
- **Audit trail**: All transactions logged and visible in dashboard

## API Base URL
```
https://api.clawvault.cc
```

## Authentication
All requests require your API key in the Authorization header:
```
Authorization: Bearer ${CLAWVAULT_API_KEY}
```

Get your API key at: https://clawvault.cc/agents

---

# CRYPTO PAYMENTS (On-Chain)

## 1. Request a Crypto Payment

When you need to send USDC to a blockchain address:

```http
POST /v1/payments
Content-Type: application/json

{
  "amount": "50.00",
  "token": "USDC",
  "recipient": "0x1234567890abcdef1234567890abcdef12345678",
  "chain": "base",
  "reason": "Payment for services rendered",
  "skill": "transfer"
}
```

### Response (Success)
```json
{
  "success": true,
  "data": {
    "id": "pi_abc123",
    "status": "pending",
    "expiresAt": "2026-02-27T12:00:00Z"
  }
}
```

### Possible Statuses
- `auto_approved` - Payment executed immediately (within rules)
- `pending` - Awaiting human approval via Telegram/dashboard
- `denied` - Payment was rejected
- `expired` - Approval window closed (5 minutes)

---

## 2. Check Before Sending (Dry Run)

Before making a payment, check if it will auto-approve or need manual approval:

```http
POST /v1/rules/check
Content-Type: application/json

{
  "amount": "50.00",
  "token": "USDC",
  "recipient": "0x1234...",
  "chain": "base"
}
```

### Response
```json
{
  "success": true,
  "data": {
    "allowed": true,
    "autoApprove": false,
    "reason": "Manual mode",
    "remainingBudget": { "daily": 450.00 },
    "remainingTx": { "daily": 46 }
  }
}
```

If `autoApprove: false`, tell the user the payment needs their approval.

---

## 3. Get Vault Status

Check your vault balance and current limits:

```http
GET /v1/vault
```

### Response
```json
{
  "success": true,
  "data": {
    "chain": "base",
    "balances": [{ "token": "USDC", "balance": "150.00" }],
    "rules": {
      "mode": "manual",
      "perTxLimit": 500,
      "dailyTxMax": 20
    }
  }
}
```

---

# AGENT CARD (Visa Card)

Use the Agent Card when you need to pay for:
- SaaS subscriptions (Vercel, Netlify, etc.)
- API services (OpenAI, Anthropic, Twilio, etc.)
- Cloud compute (AWS, GCP, Azure)
- Any merchant that accepts Visa

## 4. Request a Card Purchase

```http
POST /v1/card/purchase
Content-Type: application/json

{
  "amount": 20.00,
  "currency": "USD",
  "merchant": "OpenAI API",
  "merchant_category": "api_services",
  "reason": "GPT-4 API credits for research task"
}
```

### Response (Approved)
```json
{
  "success": true,
  "data": {
    "id": "card_txn_abc123",
    "status": "approved",
    "card_credentials": {
      "number": "4242837419283847",
      "exp_month": 3,
      "exp_year": 2028,
      "cvc": "847"
    },
    "valid_for_seconds": 300
  }
}
```

### Response (Needs Approval)
```json
{
  "success": true,
  "data": {
    "id": "card_txn_abc123",
    "status": "pending_approval",
    "reason": "Amount exceeds auto-approve threshold"
  }
}
```

**IMPORTANT**: Card credentials are temporary and single-use. Use them immediately at the merchant checkout. Never log or store card credentials.

---

## 5. Check Card Balance

```http
GET /v1/card/balance
```

### Response
```json
{
  "success": true,
  "data": {
    "balance": 450.00,
    "currency": "USD",
    "spent_today": 50.00,
    "spent_this_month": 350.00,
    "daily_limit": 500.00,
    "monthly_limit": 5000.00
  }
}
```

---

## 6. Check Card Rules

Before making a purchase, check if it's allowed:

```http
POST /v1/card/check
Content-Type: application/json

{
  "amount": 20.00,
  "merchant_category": "api_services"
}
```

### Response
```json
{
  "success": true,
  "data": {
    "allowed": true,
    "autoApprove": true,
    "reason": "Within limits, allowed category"
  }
}
```

---

# COMMON ENDPOINTS

## 7. Check Payment/Purchase Status

```http
GET /v1/payments/{payment_id}
GET /v1/card/transactions/{transaction_id}
```

## 8. List Recent Transactions

```http
GET /v1/transactions?limit=10
GET /v1/card/transactions?limit=10
```

---

# DECIDING: CRYPTO vs CARD

Use this logic to decide which channel to use:

| Scenario | Use |
|----------|-----|
| Paying a blockchain address (0x...) | Crypto (`/v1/payments`) |
| Paying for SaaS subscription | Card (`/v1/card/purchase`) |
| Paying for API credits | Card (`/v1/card/purchase`) |
| Paying for cloud services | Card (`/v1/card/purchase`) |
| Paying for any online service | Card (`/v1/card/purchase`) |
| Sending money to another person's crypto wallet | Crypto (`/v1/payments`) |
| DeFi, staking, token swaps | Crypto (`/v1/payments`) |

**Rule of thumb**: If it's a blockchain address, use crypto. If it's a company/service, use the card.

---

# HUMAN APPROVAL FLOW

When a transaction requires approval:

1. **User is notified** via Telegram bot or ClawVault dashboard
2. **User reviews** the transaction details (amount, recipient, reason)
3. **User approves or denies** with one tap
4. **Transaction executes** if approved, or is cancelled if denied
5. **Approval expires** after 5 minutes if no action taken

Always inform the user when approval is required: "This transaction needs your approval. Check your Telegram or ClawVault dashboard."

---

# COMMON SCENARIOS

### Scenario: User asks to pay for OpenAI API credits
1. Call `/v1/card/check` to verify it's allowed
2. If allowed, call `/v1/card/purchase` with merchant="OpenAI API"
3. If `status: "approved"`, use the card credentials at checkout immediately
4. If `status: "pending_approval"`, tell user: "This purchase needs your approval. Check Telegram or ClawVault dashboard."

### Scenario: User asks to send USDC to an address
1. Call `/v1/rules/check` to see if it will auto-approve
2. Call `/v1/payments` with the recipient address
3. If `status: "pending"`, tell user to approve in Telegram

### Scenario: Card purchase denied
Tell the user: "The purchase was denied. Reason: {reason}. Check ClawVault dashboard for details."

### Scenario: Insufficient card balance
Tell the user: "Insufficient card balance. Current balance: ${balance}. The card needs to be funded."

---

# ERROR HANDLING

### Common Errors
| Code | Meaning | Action |
|------|---------|--------|
| `INVALID_KEY` | Bad API key | Check your API key |
| `TIER_LIMIT_EXCEEDED` | Monthly limit reached | User needs to upgrade |
| `INSUFFICIENT_BALANCE` | Not enough funds | User needs to deposit (crypto) or fund card |
| `RULE_VIOLATION` | Outside allowed parameters | Check the `reason` field |
| `CARD_FROZEN` | Card is frozen | User needs to unfreeze in dashboard |
| `MERCHANT_BLOCKED` | Merchant category not allowed | Cannot purchase from this merchant |
| `CARD_NOT_ACTIVE` | Card not set up | User needs to apply for Agent Card |

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "RULE_VIOLATION",
    "message": "Exceeds per-transaction limit of $100"
  }
}
```

---

# SECURITY BEST PRACTICES

1. **Never log card credentials** - Card numbers, CVCs are sensitive
2. **Always check first** - Use `/v1/rules/check` or `/v1/card/check` before transactions
3. **Explain to users** - If approval is needed, tell them where to approve
4. **Handle pending** - Don't assume transactions complete immediately
5. **Use card credentials immediately** - They expire in 5 minutes
6. **Show transaction links** - For crypto, link to `https://basescan.org/tx/{txHash}`

---

# SUPPORT

- Dashboard: https://clawvault.cc
- Docs: https://clawvault.cc/docs
- API Status: https://api.clawvault.cc/health
- Source: https://github.com/andrewszk/clawvault-mcp-server
