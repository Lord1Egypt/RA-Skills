---
name: buff-roundup
description: Transaction round-up helper. Calculates spare change from payments and builds unsigned Solana transfer instructions for user review. Server-side fee enforcement. REST API for any language.
required_credentials:
  - name: BUFF_API_KEY
    description: "API key for authenticating with the Buff API. Generate programmatically via POST /api/keys/generate or get one at buff.finance/dashboard"
    sensitive: true
  - name: BUFF_WALLET_PUBKEY
    description: "Your Buff wallet public key (Solana address)"
    sensitive: false
  - name: BUFF_PLAN
    description: "Round-up tier: seed ($0.05), sprout ($0.10), tree ($0.50), forest ($1.00)"
    sensitive: false
permissions:
  - network: "Connects to buff.finance API (HTTPS). All fee calculation and swap routing handled server-side."
  - storage: "None — stateless API client"
---

# Buff — Round-Up Investing Protocol

Buff rounds up every Solana transaction and auto-invests the spare change into crypto assets. All fees are enforced server-side — the SDK is a thin API client with no sensitive logic.

## Security

- All fee calculation and treasury addresses are **server-side only**
- The SDK contains **zero sensitive logic** — it's just HTTP calls
- **No funds are moved without explicit user signing** — the agent never holds private keys
- Fees cannot be bypassed — the server builds all transfer instructions
- All swap transactions are returned **unsigned** for user review before signing

## Verifying Server-Built Transactions

Before signing any transaction returned by the Buff API, agents and developers **should verify**:

1. **Deserialize the instructions** returned by `/api/wrap` (base64 JSON containing programId, keys, data)
2. **Check that transfers only go to your Buff wallet** (user investment) and the known Buff treasury (`4pWnqVxtSfrMo2XK6AarW3rDNoN7UfAMEyHF8Y9KZGHf`)
3. **Verify amounts match the breakdown** — `userInvestmentLamports` + `buffFeeLamports` should equal `roundUpLamports`
4. **For swaps**, verify the unsigned transaction from `/api/swap/build` contains only Jupiter swap instructions for the expected token pair and amount
5. **Use a scoped/rotatable API key** and test with small amounts first
6. **Compare the breakdown** from `/api/roundup` (informational) with `/api/wrap` (executable) — they should match for the same inputs

## Quick Start

```bash
npm install buff-protocol-sdk@1.0.1
```

```typescript
import { Buff } from "buff-protocol-sdk"

const buff = new Buff({
  apiKey: process.env.BUFF_API_KEY,
  plan: "sprout",
  investInto: "BTC",
})

// Calculate a round-up
const breakdown = await buff.calculateRoundUp(4.73)
// $4.73 → $4.80 = $0.07 round-up

// Get wrap instructions (server builds transfer instructions with fees)
const { instructions, breakdown } = await buff.getWrapInstructions(
  27.63, userPubkey, buffWalletPubkey
)
// Append instructions to your transaction, sign, send
```

## Auto-Invest

The invest flow is two steps: build (server returns an unsigned transaction), then sign and submit. **The agent never holds private keys — signing always requires explicit user action.**

```typescript
// Check accumulator balance vs threshold (default $5 USD)
const acc = await buff.getAccumulator(walletPubkey, { threshold: 5 })

// Build swap transactions (server-side via Jupiter) — returns unsigned txs
const result = await buff.buildSwap(walletPubkey)
if (result.ready) {
  for (const swap of result.transactions) {
    // ⚠️ Verify asset, amount, and destination before signing
    // swap.transaction is an unsigned base64 tx — inspect it first
    // See: https://buff.finance/docs/swaps for submission details
  }
}
```

The `threshold` parameter (default `$5`) acts as the budget gate — swaps only trigger once accumulated round-ups reach that value. Set it higher for less frequent execution.

## Multi-Asset Allocation

```typescript
buff.setAllocations([
  { asset: "BTC", pct: 60 },
  { asset: "ETH", pct: 40 },
])
```

## Plan Tiers

| Plan | Rounds to | Fee |
|------|-----------|-----|
| Seed | $0.05 | 1.00% |
| Sprout | $0.10 | 0.75% |
| Tree | $0.50 | 0.50% |
| Forest | $1.00 | 0.25% |

## REST API

No SDK needed — any language, any agent. Base URL: `https://buff.finance`

### Public Endpoints (no auth required)

```bash
# Get auth message to sign
curl https://buff.finance/api/auth

# Get plan tiers and config
curl https://buff.finance/api/plans

# Get live crypto prices
curl https://buff.finance/api/price

# Get portfolio for any wallet
curl https://buff.finance/api/portfolio/WALLET_ADDRESS

# Check accumulator (balance vs threshold)
curl "https://buff.finance/api/accumulator/WALLET_ADDRESS?threshold=5"

# Get transaction history
curl "https://buff.finance/api/activity?address=WALLET_ADDRESS&limit=20"
```

### Generate API Key (no pre-existing key needed)

```bash
# 1. Sign "Buff API Authentication" with your Solana keypair
# 2. Send wallet + signature to generate your key

curl -X POST https://buff.finance/api/keys/generate \
  -H "Content-Type: application/json" \
  -d '{"wallet": "YOUR_PUBKEY", "signature": "BASE64_SIGNATURE"}'

# Response: { "ok": true, "data": { "apiKey": "...", "wallet": "..." } }
# Use both x-api-key and x-wallet headers on all authenticated requests
```

### Authenticated Endpoints (require x-api-key + x-wallet, or x-wallet + x-signature)

```bash
# Calculate round-up
curl -X POST https://buff.finance/api/roundup \
  -H "x-api-key: YOUR_KEY" \
  -d '{"txValueUsd": 27.63, "plan": "tree"}'

# Get wrap instructions (server builds transfer with fees enforced)
curl -X POST https://buff.finance/api/wrap \
  -H "x-api-key: YOUR_KEY" \
  -d '{"txValueUsd": 27.63, "userPubkey": "...", "buffWalletPubkey": "..."}'

# Get Jupiter swap quote
curl -X POST https://buff.finance/api/swap/quote \
  -H "x-api-key: YOUR_KEY" \
  -d '{"inputLamports": 100000000, "targetAsset": "BTC"}'

# Build swap transaction (server-side via Jupiter)
curl -X POST https://buff.finance/api/swap/build \
  -H "x-api-key: YOUR_KEY" \
  -d '{"buffWalletPubkey": "...", "targetAsset": "BTC", "threshold": 5}'

# Derive Buff wallet from signature
curl -X POST https://buff.finance/api/wallet/derive \
  -d '{"signature": "base64-or-hex-signature"}'

# Register an agent
curl -X POST https://buff.finance/api/agent/register \
  -H "x-api-key: YOUR_KEY" \
  -d '{"publicKey": "...", "agentId": "my-agent"}'
```

### Interactive API Playground

Try all endpoints live at: https://buff.finance/docs/api/rest

## Links

- Docs: https://buff.finance/docs
- Dashboard: https://buff.finance/dashboard
- API Reference: https://buff.finance/docs/api/rest
- GitHub: https://github.com/nightcode112/Buff
