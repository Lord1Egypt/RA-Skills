# Payment Protocols

ChainStream supports **two payment protocols** for purchasing subscription plans. Both return an API Key on success — use whichever your wallet supports.

| Protocol | Chains & Currency | Purchase Endpoint | Pricing Endpoint | Client Tool |
|----------|------------------|-------------------|-----------------|-------------|
| **x402** | Base (USDC) / Solana (USDC) | `/x402/purchase` | `/x402/pricing` | `@x402/fetch` or CLI |
| **MPP** | Tempo (USDC.e) | `/mpp/purchase` | `/mpp/pricing` | `tempo request` |

Plans and pricing are **identical** across both protocols. The only difference is which chain/token you pay with.

## Trial Plans (Free Trial)

New users are **automatically granted a subscription plan** on login — no manual purchase needed:

| Action | Auto-granted Plan | Quota | Dedup |
|--------|------------------|-------|-------|
| `chainstream login` (new wallet created) | nano ($1) | 50,000 CU / 30 days | Per wallet (Turnkey org) |
| `chainstream bind-email` or `chainstream login --email` | micro ($5) | 350,000 CU / 30 days | Per email address |

- **Key-based users**: auto-receive nano plan (50K CU) immediately on first login
- **Email-verified users**: auto-upgraded to micro plan (350K CU) on `bind-email` or `login --email`
- **Dedup by email**: same email address only grants the micro upgrade once, even if bound to multiple wallets
- **No manual purchase step**: the plan is activated server-side; `plan status` will show the active trial plan
- **Upgrade behavior**: email verification replaces the nano plan with micro (quota is reset to micro's full allocation)

Trial plans are **server-side only** — no on-chain transaction occurs. Agents do not need to change their workflow; the user already has API access after `chainstream login`.

```bash
# Check active plan after login
npx @chainstream-io/cli plan status --json
# Output: { "plan": "nano", "quota": { "used": 0, "total": 50000 }, "active": true }
```

## Plans

Plans and pricing are dynamic. **Always fetch the latest from the API — do NOT hardcode plan names or prices.**

```bash
# x402 pricing (no auth required)
curl https://api.chainstream.io/x402/pricing

# MPP pricing (no auth required, same plans + shows supported payment methods)
curl https://api.chainstream.io/mpp/pricing

# CLI
npx @chainstream-io/cli wallet pricing
```

### Agent behavior when payment is needed (MUST follow)

When a user needs to purchase a subscription:

1. **Fetch available plans**: call `GET /x402/pricing` or `GET /mpp/pricing`
2. **Present ALL plans to the user** with name, price, quota (CU), and duration — let them choose. **NEVER auto-select a plan. NEVER default to any plan. The user MUST explicitly choose.**
3. **Explain what it means**: "A subscription gives you a pool of **Compute Units (CU)**. Each API call consumes CU from the pool — the amount varies by endpoint complexity and response size. CU is NOT the same as API call count. The quota is valid for 30 days." **Always use "CU" as the unit — NEVER say "calls" or "requests" when describing quota.**
4. **Check wallet balance** (x402 only): `wallet balance --chain base` and/or `--chain sol` to confirm USDC is available. Also run `plan status` — if a trial plan is already active and sufficient, no purchase may be needed
5. **Ask which payment method the user has**:
   - USDC on Base or Solana → use x402
   - USDC.e on Tempo → use MPP
   - No crypto wallet → obtain API Key from Dashboard
6. **Set payment chain** (x402 only, default is `base`):
   - User has USDC on Base → no action needed (default)
   - User has USDC on Solana → `npx @chainstream-io/cli config set --key walletChain --value sol`
7. **Wait for the user to confirm** both the plan and payment chain
8. **Execute the purchase**: `plan purchase --plan <USER_CHOSEN> --json` (x402) or `tempo request .../mpp/purchase?plan=<USER_CHOSEN>` (MPP)

**NEVER hardcode a plan name in the URL.** The `?plan=` parameter MUST come from the user's explicit selection. Do NOT say "you need the nano plan" — always show all options and let the user decide.

### Purchase flow (CLI)

`plan purchase` uses the configured `walletChain` for payment. **Default is `base`** (set after `chainstream login`). If your USDC is on Solana, you must set `walletChain` to `sol` before purchasing.

```bash
# Step 1: Check existing subscription
npx @chainstream-io/cli plan status --json

# Step 2: Show plans — present ALL to user, let them choose
npx @chainstream-io/cli wallet pricing --json

# Step 3: Check wallet balance to confirm USDC is on the right chain
npx @chainstream-io/cli wallet balance --chain base --json   # check Base
npx @chainstream-io/cli wallet balance --chain sol --json    # check Solana
# Default payment chain is base. If USDC is on Solana:
npx @chainstream-io/cli config set --key walletChain --value sol

# Step 4: Purchase (real USDC payment via EIP-3009; not needed if trial plan is already active)
npx @chainstream-io/cli plan purchase --plan <USER_CHOSEN> --json
# Output: { "plan": "nano", "apiKey": "cs_live_...", "expiresAt": "..." }
# API Key auto-saved to config.
```

Always present plans and get explicit user confirmation before calling `plan purchase`.

For MPP (USDC.e on Tempo), `plan purchase` is not available — use `tempo request` instead (see MPP section below).

## API Key Auto-Return

When purchase succeeds (via either protocol), the response includes an `apiKey` field:

```json
{
  "status": "ok",
  "plan": "nano",
  "expiresAt": "2026-04-23T00:00:00Z",
  "apiKey": "cs_live_..."
}
```

This API Key works with MCP Server, CLI, and SDK — no wallet signature needed for subsequent calls. The CLI automatically saves it to `~/.config/chainstream/config.json`.

---

## x402 Protocol (Base / Solana)

### Supported Networks

- **Base**: mainnet — USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`), chain ID `eip155:8453`
- **Solana**: mainnet — USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`)

### IMPORTANT: Use CLI or @x402/fetch — Do NOT manually construct payments

x402 uses **EIP-3009 `transferWithAuthorization`** (off-chain signed authorization), NOT a simple USDC transfer. Manual curl construction will fail.

### Method 1: CLI `plan purchase` (recommended)

Purchase a subscription using the dedicated CLI command. This involves a **real USDC payment** — an EIP-3009 `signTypedData` that authorizes fund transfer from the wallet. Always present plan options and get user confirmation before purchasing.

```bash
# View plans
npx @chainstream-io/cli wallet pricing --json

# Purchase (signs EIP-3009, pays USDC, returns API Key — auto-saved to config)
npx @chainstream-io/cli plan purchase --plan <USER_CHOSEN> --json
```

Under the hood, the CLI uses `@x402/fetch` to:
1. Send GET to `/x402/purchase?plan=<name>`
2. Receive 402 + payment requirements
3. Sign EIP-3009 typed data with wallet (requires `signTypedData`, not `signMessage`) — **this authorizes real USDC transfer**
4. Retry with `Payment-Signature` header
5. Return the API response with `apiKey` after payment completes

If a data command (e.g. `token search`) is called without a subscription, the CLI returns a 402 error with instructions to run `plan purchase`.

### Method 2: Standard x402 GET (any x402-compatible wallet)

```
GET https://api.chainstream.io/x402/purchase?plan=<PLAN>
→ 402 + Payment-Required header → client signs → retries with Payment-Signature → 200
```

Replace `<PLAN>` with the user's chosen plan name (e.g., nano, micro, starter, growth, pro, business).

### Method 3: @x402/fetch (programmatic)

```javascript
import { x402Client } from "@x402/core/client";
import { wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";

const client = new x402Client();

// Register ONE payment scheme based on your wallet's chain:
// Base (USDC)
client.register("eip155:8453", new ExactEvmScheme(viemAccount));
// Solana (USDC)
client.register("solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp", new ExactSvmScheme(solanaSigner));

const x402Fetch = wrapFetchWithPayment(fetch, client);
const resp = await x402Fetch("https://api.chainstream.io/x402/purchase?plan=<PLAN>");
```

Required packages: `@x402/core`, `@x402/fetch`, `@x402/evm` (for Base), `@x402/svm` (for Solana)

CLI auto-payment supports both Base and Solana equally. The payment chain is determined by your wallet config:

- `walletChain: "base"` → pay with USDC on Base (default after `chainstream login`)
- `walletChain: "sol"` → pay with USDC on Solana

To switch payment chain:

```bash
npx @chainstream-io/cli config set --key walletChain --value sol   # use Solana USDC
npx @chainstream-io/cli config set --key walletChain --value base  # use Base USDC
```

---

## MPP Protocol (Tempo)

MPP (Machine Payments Protocol) is an open standard by Stripe and Tempo for machine-to-machine payments via HTTP 402.

### Supported Network

- **Tempo**: Stripe's L1 blockchain (EVM-compatible, chain ID 4217) — pays with **USDC.e** (bridged Circle USDC, 1:1 USD pegged). **Tempo does NOT need a separate gas token — gas fees are paid in the same USDC.e. Do NOT tell users they need ETH or pathUSD for gas.**

### How it works

```
Agent → GET /mpp/purchase?plan=<PLAN>
     → 402 + WWW-Authenticate: Payment (challenge with amount, currency, recipient)
     → Agent signs Tempo transaction (via Tempo Wallet)
     → GET /mpp/purchase?plan=<PLAN> + Authorization: Payment (credential)
     → 200 { apiKey, plan, expiresAt }
```

Unlike x402, MPP does NOT need an external facilitator — verification and settlement happen on-chain directly.

### Method 1: Tempo Wallet CLI (recommended)

Set up the Tempo Wallet using the official skill. Paste this into your agent:

```
Read https://tempo.xyz/SKILL.md and set up Tempo Wallet
```

Or install the Tempo docs skill:

```bash
npx skills add tempoxyz/docs
```

Then purchase a plan:

```bash
# Tempo Wallet handles 402 → sign → retry automatically
tempo request "https://api.chainstream.io/mpp/purchase?plan=<PLAN>"
```

Tempo Wallet uses passkey (WebAuthn) authentication — the user needs to complete a one-time browser auth on first setup. After that, the session persists and agent operations work without further browser interaction.

### Method 2: Any EVM wallet with USDC.e on Tempo

Any wallet holding USDC.e on Tempo (chain ID 4217) can call the purchase endpoint directly:

```
GET https://api.chainstream.io/mpp/purchase?plan=<PLAN>
→ 402 + WWW-Authenticate: Payment challenge
→ Sign and retry with Authorization: Payment credential
→ 200 { apiKey, plan, expiresAt }
```

Compatible wallets: Tempo Wallet, MetaMask (custom network), Coinbase CDP, Turnkey, Privy, or any EVM wallet on Tempo chain.

---

## Choosing a Protocol

| Your wallet has | Use protocol | Command |
|----------------|-------------|---------|
| USDC on **Base** | x402 | CLI auto-handles, or `@x402/fetch` |
| USDC on **Solana** | x402 | CLI with `walletChain: "sol"` |
| USDC.e on **Tempo** | MPP | `tempo request .../mpp/purchase?plan=<PLAN>` |
| **No crypto wallet** | — | Get API Key from [Dashboard](https://app.chainstream.io) |

If unsure, ask the user which chain their wallet is on. If they say "Tempo" or "Stripe" → MPP. If they say "Base", "Solana", or "USDC" → x402.

## Check Current Subscription

To check whether a wallet has an active subscription and view quota usage:

```bash
# CLI (auto-detects wallet from config)
npx @chainstream-io/cli plan status

# CLI with explicit chain/address
npx @chainstream-io/cli plan status --chain evm --address 0x...

# API (no auth required)
curl "https://api.chainstream.io/x402/status?chain=evm&address=0x..."
```

Response:

```json
{
  "plan": "pro",
  "quota": { "used": 12500, "total": 500000 },
  "expiresAt": "2026-05-01T00:00:00.000Z",
  "active": true
}
```

- `plan`: current plan name (null if no subscription)
- `quota.used` / `quota.total`: compute units consumed / total (total = -1 means unlimited)
- `expiresAt`: subscription expiry (ISO 8601)
- `active`: whether the subscription is currently valid

## Error Recovery

- If payment fails (insufficient funds): tell user how much is needed and on which network, show wallet address
- If 402 persists after payment: wait 5s for settlement, then retry
- To check available plans: `GET /x402/pricing` or `GET /mpp/pricing` (no auth required)
- To check current subscription: `GET /x402/status?chain=...&address=...` or `npx @chainstream-io/cli plan status`
- x402-specific: ensure wallet has USDC on Base or Solana
- MPP-specific: ensure Tempo Wallet has USDC.e (`tempo wallet balance` to check). Tempo uses USD stablecoins for gas — no separate gas token needed.
