# x402 Wallet Authentication

Keyless access to ChainStream APIs using USDC on Base or Solana. No account registration needed.

> Full details: [shared/authentication.md](../../shared/authentication.md) and [shared/x402-payment.md](../../shared/x402-payment.md)

## How It Works

1. Purchase a USDC plan once — get a pool of Compute Units (CU)
2. API calls consume CU from the pool (different endpoints cost different CU)
3. Quota is valid for 30 days from purchase

Only the initial plan purchase involves a blockchain transaction. Subsequent API calls just need SIWX wallet signature (no on-chain payment per request).

## Plans

Plans are dynamic. Query the latest:

```bash
npx @chainstream-io/cli wallet pricing
# or: curl https://api.chainstream.io/x402/pricing
```

CLI always shows all plans and prompts the user to choose — there is no default plan.

## CLI: x402 Payment Flow

Purchase a subscription using `plan purchase`. This involves a **real USDC payment** — an EIP-3009 `signTypedData` that authorizes fund transfer from the user's wallet.

`plan purchase` uses the configured `walletChain` for payment. **Default is `base`**. If USDC is on Solana, set `walletChain` to `sol` first.

```bash
# 1. Show plans — present ALL to user, let them choose
npx @chainstream-io/cli wallet pricing --json

# 2. Check wallet balance to find USDC
npx @chainstream-io/cli wallet balance --chain base --json   # check Base
npx @chainstream-io/cli wallet balance --chain sol --json    # check Solana

# 3. Set payment chain if USDC is on Solana (default is base)
npx @chainstream-io/cli config set --key walletChain --value sol

# 4. Purchase (signs EIP-3009 authorization, pays USDC, returns API Key)
npx @chainstream-io/cli plan purchase --plan <USER_CHOSEN> --json
# Output: { "plan": "nano", "apiKey": "cs_live_...", "expiresAt": "..." }
# API Key auto-saved to config.
```

If a data command returns 402 without a subscription, the CLI shows an error guiding you to run `plan purchase`. Always present plans and get user confirmation before purchasing.

## SDK: `@x402/fetch`

When using the SDK with your own wallet:

```typescript
import { x402Client } from "@x402/core/client";
import { wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";

const x402 = new x402Client();

// Register ONE payment scheme based on your wallet's chain:
// Base (USDC)
x402.register("eip155:8453", new ExactEvmScheme(yourViemAccount));
// Solana (USDC)
x402.register("solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp", new ExactSvmScheme(solanaSigner));

const x402Fetch = wrapFetchWithPayment(fetch, x402);

// Purchase — plan name MUST come from user's explicit selection
const resp = await x402Fetch("https://api.chainstream.io/x402/purchase?plan=<USER_CHOSEN_PLAN>");
```

Base payment requires `signTypedData` (EIP-712). Solana payment requires a `@solana/kit` signer. Both involve **real USDC transfer** — always confirm with user first.

## Authentication After Purchase

After purchasing a plan, all API calls use **SIWX** (Sign-In-With-X) authentication:

```
Authorization: SIWX <base64(message)>.<signature>
```

The SDK/CLI handles SIWX token creation and caching automatically. See [authentication.md](../../shared/authentication.md) for details.

## Check Current Subscription

```bash
# CLI (auto-detects wallet from config)
npx @chainstream-io/cli plan status

# API
curl "https://api.chainstream.io/x402/status?chain=evm&address=0x..."
```

Returns plan name, quota usage, expiry, and active status. See [x402-payment.md](../../shared/x402-payment.md#check-current-subscription) for response format.

## Supported Networks

| Network | Chain ID | USDC Contract |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Solana | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
