# Authentication

ChainStream supports wallet signature and API key authentication. Choose the integration path that matches your agent's wallet setup.

## Agent Bootstrap Checklist

**Every ChainStream skill (data / defi / graphql) requires auth. Run these 3 steps before any API call:**

1. `npx @chainstream-io/cli config auth` — check login status
2. If NOT logged in: `npx @chainstream-io/cli login` (creates wallet + auto-grants nano trial: 50K CU free, 30 days)
3. `npx @chainstream-io/cli plan status` — verify subscription is active

After login, most new users can immediately use all API endpoints (nano trial is sufficient for typical queries). To upgrade: `bind-email` for micro (350K CU) or `plan purchase` for paid plans.

## Which Path to Use

| Your Agent Has | Integration Path | Auth | Payment Protocol |
|---------------|-----------------|------|-----------------|
| No wallet | CLI (`npx @chainstream-io/cli`) | CLI creates ChainStream Wallet (TEE-backed), signs automatically | x402 (USDC on Base/Solana) |
| Own wallet private key | CLI with `wallet set-raw` | CLI signs with imported key | x402 (USDC on Base/Solana) |
| Own wallet (embedded, MPC, etc.) | SDK (`@chainstream-io/sdk`) | Implement `WalletSigner` interface | x402 via `@x402/fetch` |
| Tempo wallet (USDC.e) | Tempo Wallet CLI (`tempo request`) | MPP 402 auto-handled | MPP (USDC.e on Tempo, chain ID 4217) |
| Dashboard API key (human user) | CLI or SDK with API Key | `X-API-KEY` header | Not applicable (pre-paid) |
| x402/MPP purchased API Key | CLI, SDK, or MCP | `X-API-KEY` header | Auto-returned on purchase |

**Supported payment chains**: Base (USDC), Solana (USDC), Tempo (USDC.e). See [shared/x402-payment.md](x402-payment.md) for protocol details.

API Key is the universal credential — works with MCP, CLI, and SDK. Agents that cannot use wallet signatures should obtain an API Key via x402 purchase, MPP purchase, or Dashboard.

## Path 1: CLI with Built-in Wallet (recommended)

For agents that don't have their own wallet. CLI creates a ChainStream TEE wallet on first login — no email, no registration form, no seed phrase.

```bash
# First time: creates EVM + Solana wallet (no email required)
npx @chainstream-io/cli login

# Output:
#   Welcome! Your ChainStream wallet has been created.
#     EVM:    0x...
#     Solana: ...

# All subsequent calls: auth + x402 payment handled automatically
npx @chainstream-io/cli token search --keyword PUMP --chain sol
```

What happens under the hood:
1. CLI generates a P-256 key pair locally (`~/.config/chainstream/keys/`)
2. Sends the public key to ChainStream auth service
3. Auth service creates a TEE-backed wallet with EVM + Solana addresses
4. CLI stores the organization ID and wallet addresses in `~/.config/chainstream/config.json`
5. All API calls use SIWX wallet signature auth; x402 payment uses EIP-3009 signed authorization

> New wallets are automatically granted a **nano trial plan** ($1, 50K CU, 30 days). No manual purchase needed — the plan is activated immediately. See [x402-payment.md](x402-payment.md#trial-plans-free-trial) for details.

### Session management

```bash
npx @chainstream-io/cli config auth              # Show auth status
npx @chainstream-io/cli config get               # Show all config
npx @chainstream-io/cli config get --key apiKey   # Show specific key
npx @chainstream-io/cli logout                    # Clear session (P-256 keys preserved)
```

### Optional: Bind email for recovery

After creating a wallet, you can optionally bind an email for account recovery. This also **auto-upgrades the trial plan to micro** ($5, 350K CU, 30 days; dedup by email — same email only grants once):

```bash
# Interactive (TTY terminal):
npx @chainstream-io/cli bind-email user@example.com
# Enter verification code: xxxxxx
# Email user@example.com bound successfully.

# Non-interactive (CI/CD, headless agent):
npx @chainstream-io/cli bind-email user@example.com
# Output: {"otpId":"...","email":"user@example.com","step":"verify"}
npx @chainstream-io/cli bind-email-verify --otp-id <otpId> --code <code> --email user@example.com
```

### Optional: Email OTP login

If you prefer email-based login (e.g., to recover an existing wallet on a new device). First-time email login also auto-upgrades the trial plan to micro ($5, 350K CU; dedup by email):

```bash
# Interactive (TTY terminal):
npx @chainstream-io/cli login --email user@example.com
# Enter OTP code: xxxxxx
# Logged in successfully.

# Non-interactive (CI/CD, piped, headless agent):
npx @chainstream-io/cli login user@example.com
# Output: {"otpId":"...","email":"user@example.com"}
npx @chainstream-io/cli verify --otp-id <otpId> --code <code> --email user@example.com
```

## Path 1b: CLI with Your Own Private Key

For agents that already have a Base (EVM) or Solana private key and want to use the CLI (no wallet creation, no email):

```bash
# Import Base (EVM) private key
npx @chainstream-io/cli wallet set-raw --chain base
# Enter private key: <your hex private key>

# Import Solana private key
npx @chainstream-io/cli wallet set-raw --chain sol
# Enter private key: <your base58 private key>

# Verify addresses
npx @chainstream-io/cli wallet address
# EVM:    0xYourAddress
# Solana: YourSolanaAddress

# Set payment chain to match your funded wallet
npx @chainstream-io/cli config set --key walletChain --value base  # if paying with Base USDC
npx @chainstream-io/cli config set --key walletChain --value sol    # if paying with Solana USDC

# All commands now use your imported key for auth + x402 payment
npx @chainstream-io/cli token search --keyword PUMP --chain sol
```

The CLI will use your private key for both SIWX authentication and x402 payment. This works with any standard Base (EVM) or Solana private key.

## Path 2: SDK with Your Own Wallet (agent already has wallet)

For agents using embedded wallet providers or your wallet provider of choice, as long as it supports `signMessage` + `signTypedData`.

**Two things your wallet must support:**
- `signMessage` (EIP-191 `personal_sign`) — for SIWX authentication on every API call
- `signTypedData` (EIP-712) — for x402 payment (one-time USDC plan purchase via EIP-3009)

### Full integration example

```typescript
import { ChainStreamClient, type WalletSigner } from "@chainstream-io/sdk";
import { x402Client } from "@x402/core/client";
import { wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";

// ── Step 1: Create WalletSigner for API authentication ──
// Adapt this to your wallet provider
const myWallet: WalletSigner = {
  chain: "evm",
  address: "0xYourAgentWalletAddress",
  signMessage: async (msg) => {
    // Must return EIP-191 personal_sign signature (65 bytes hex with 0x prefix)
    return yourWallet.signMessage(msg);
  },
};

// ── Step 2: Create SDK client (handles SIWX auth automatically) ──
const client = new ChainStreamClient("", {
  serverUrl: "https://api.chainstream.io",
  walletSigner: myWallet,
});

// ── Step 3: Set up x402 payment (handles 402 → sign → retry) ──
// ⚠️ x402 payment involves REAL USDC transfer (EIP-3009 signTypedData).
//    Always present plan options and get user confirmation before purchase.
const x402 = new x402Client();
// Register ONE payment scheme based on your wallet's chain:
// Base (USDC) — requires signTypedData (EIP-712)
x402.register("eip155:8453", new ExactEvmScheme(yourViemCompatibleAccount));
// Solana (USDC) — requires @solana/kit signer
x402.register("solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp", new ExactSvmScheme(solanaSigner));
const x402Fetch = wrapFetchWithPayment(fetch, x402);

// ── Step 4: Purchase quota if needed ──
// First API call may return 402 if no subscription exists.
// Plan name MUST come from user's explicit selection — NEVER hardcode a plan.
// Option A: x402Fetch automates the 402 → sign → retry flow
await x402Fetch("https://api.chainstream.io/x402/purchase?plan=<USER_CHOSEN_PLAN>");
// Option B: SDK calls — catch 402, purchase, retry
try {
  const tokens = await client.token.search({ q: "PUMP", chains: ["sol"] });
} catch (err) {
  if (err.message.includes("402") || err.message.includes("PAYMENT_REQUIRED")) {
    // Fetch plans first: GET /x402/pricing → present to user → get their choice
    await x402Fetch("https://api.chainstream.io/x402/purchase?plan=<USER_CHOSEN_PLAN>");
    const tokens = await client.token.search({ q: "PUMP", chains: ["sol"] });
  }
}
```

### Compatible wallet patterns

| Wallet pattern | signMessage | signTypedData | x402 integration |
|----------|-------------|---------------|------------|
| Embedded wallet (EVM) | `yourWallet.signMessage(msg)` | `yourWallet.signTypedData(...)` | your wallet provider's x402 integration |
| MPC wallet | Provider API | Provider API | Manual integration |
| Smart contract / AA wallet | Provider signing | EIP-712 intents | Manual integration |
| Any viem LocalAccount | `account.signMessage()` | `account.signTypedData()` | Native with `ExactEvmScheme` |

Required packages: `@chainstream-io/sdk`, `@x402/core`, `@x402/fetch`, `@x402/evm`, `viem`

## Path 3: MPP with Tempo Wallet (USDC.e on Tempo chain)

For agents that have USDC.e on the Tempo blockchain (Stripe's L1, EVM-compatible, chain ID 4217). No ChainStream wallet or SIWX auth needed — MPP purchase gives you an API Key directly.

Set up Tempo Wallet by reading `https://tempo.xyz/SKILL.md` or running `npx skills add tempoxyz/docs`. Passkey auth requires a one-time browser interaction; after that the session persists for agent use.

### Quick purchase via Tempo Wallet CLI

```bash
# Set up Tempo Wallet (one-time — requires browser passkey auth)
curl -fsSL https://tempo.xyz/install | bash
tempo wallet login

# View plans (no auth required)
curl https://api.chainstream.io/mpp/pricing

# Purchase user's chosen plan — auto-handles 402 → sign → retry → returns API Key
tempo request "https://api.chainstream.io/mpp/purchase?plan=<PLAN>"
# Output: { "status": "ok", "plan": "...", "apiKey": "cs_live_...", "expiresAt": "..." }

# Set the API Key in CLI
npx @chainstream-io/cli config set --key apiKey --value cs_live_...
```

### Tempo wallet options

Tempo is EVM-compatible (chain ID 4217). Any wallet holding USDC.e on Tempo works:
- **Tempo Wallet CLI** (`tempo request`) — recommended, passkey auth, built-in MPP support
- Any EVM wallet (MetaMask, Coinbase CDP, Turnkey, Privy) — add Tempo as custom network

## Path 4: API Key (dashboard users)

For human users with a dashboard account. Read-only operations only (DeFi requires wallet).

```bash
npx @chainstream-io/cli config set --key apiKey --value <key>
```

Get a key at [app.chainstream.io](https://app.chainstream.io).

> **Note**: API Keys obtained from x402 purchase, MPP purchase, or Dashboard are interchangeable. Once you have an API Key, the payment method used to obtain it doesn't matter.

## SIWX Authentication (Standard)

All wallet-based requests use SIWX (Sign-In-With-X) authentication. SDK/CLI handles this automatically.

**How it works**: Sign a SIWE/SIWS message once → get a token valid for 1 hour → include in every request.

```
Authorization: SIWX <base64(message)>.<signature>
```

The message follows EIP-4361 (SIWE for EVM, SIWS for Solana) format:
```
api.chainstream.io wants you to sign in with your Ethereum account:
0xYourAddress

Sign in to ChainStream API

URI: https://api.chainstream.io
Version: 1
Chain ID: 8453
Nonce: <random>
Issued At: <ISO 8601>
Expiration Time: <ISO 8601, default 1h>
```

Signing method: `personal_sign` (EIP-191 for EVM, ed25519 for Solana).

SDK/CLI automatically caches the token and refreshes before expiry. Agent never needs to manage token lifecycle.

## Auth Priority

Server checks in order: SIWX → API Key → JWT Bearer.

## Check Current Subscription

```bash
# CLI (auto-detects wallet chain and address from config)
npx @chainstream-io/cli plan status

# With explicit parameters
npx @chainstream-io/cli plan status --chain evm --address 0x...

# API (no auth required)
curl "https://api.chainstream.io/x402/status?chain=evm&address=0x..."
```

Returns current plan name, quota usage (used/total CU), expiry date, and active status. See [x402-payment.md](x402-payment.md#check-current-subscription) for full response format.

## Address Linking (Cross-Chain SIWX)

When a user has wallets on multiple chains (e.g., EVM + Solana via Turnkey embedded wallet), a single x402 payment only registers SIWX auth for the paying chain. **Address Linking** allows the user to associate additional chain addresses with the same subscription, so SIWX auth works regardless of which chain they sign with.

**How it works:**

- The paying chain's address is the **primary address** that determines the `orgId`
- After payment, the CLI automatically links all other available wallet addresses to the same `orgId`
- Each linked address gets its own `x402:access:{chain}:{address}` Redis record pointing to the same `orgId`
- All addresses share the same subscription quota and expiry

**Automatic linking (CLI):** After a successful x402 purchase, the CLI automatically detects other available wallet addresses (e.g., if payment was via EVM, it finds the Solana address) and calls `POST /x402/link-address` to link them. This is transparent to the user.

**Manual linking:**

```bash
# Link your Solana address to an existing subscription
npx @chainstream-io/cli wallet link --chain solana

# Link your EVM address to an existing subscription
npx @chainstream-io/cli wallet link --chain evm
```

Requires an active API Key (`chainstream config set --key apiKey --value <key>`).

**API endpoint:** `POST /x402/link-address`

```json
{
  "chain": "solana",
  "address": "53LKjHoRGSi3...",
  "message": "<SIWX message proving ownership>",
  "signature": "<signature>"
}
```

Header: `X-API-KEY: <your-api-key>`

**Supported chains:** `evm` (all EVM-compatible chains), `solana`. More chains will be added as supported.

**Storage:** Address-to-orgId mappings are stored in both Redis (hot path for auth-service) and PostgreSQL (`x402_address_link` table) for persistence. Redis can be rebuilt from DB if needed.

**API Key is always chain-agnostic.** Once you have an API Key, it works regardless of which chain was used for payment or SIWX. Address linking is specifically for users who rely on SIWX authentication across multiple chains.

## NEVER Do

- NEVER construct SIWX tokens manually — use SDK or CLI
- NEVER construct x402 `Payment-Signature` manually — use `@x402/fetch` or CLI
- NEVER expose wallet private keys in logs, command arguments, or chat messages
