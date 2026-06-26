# Carbium Swap API Reference

Auth: `X-API-KEY` header on all requests

## API Versions

| Version | Base URL | Parameters | Status |
|---|---|---|---|
| **v2 (Q1)** | `https://api.carbium.io/api/v2` | `src_mint`, `dst_mint`, `amount_in`, `slippage_bps` | **Current** |
| v1 (legacy) | `https://api.carbium.io/api/v1` | `fromMint`, `toMint`, `amount`, `slippage` | Operational, legacy |

> **Do not mix parameter families across versions.** Sending `fromMint` to a v2 endpoint or `src_mint` to a v1 endpoint will fail or return bad results.

---

## v2 — GET /api/v2/quote (Q1 Engine)

Get optimized quote with optional executable transaction. **This is the recommended integration path.**

| Param | Type | Required | Description |
|---|---|---|---|
| `src_mint` | string | Yes | Input token mint address |
| `dst_mint` | string | Yes | Output token mint address |
| `amount_in` | integer | Yes | Input amount in smallest unit (lamports for SOL) |
| `slippage_bps` | integer | Yes | Slippage tolerance in basis points (100 = 1%) |
| `user_account` | string | No | User wallet address. If included, response includes `txn` field with base64 serialized transaction ready for signing |

**Response fields:**

| Field | Description |
|---|---|
| `srcAmountIn` | Confirmed raw input amount |
| `destAmountOut` | Expected output amount |
| `destAmountOutMin` | Minimum output after slippage |
| `priceImpactPct` | Price impact percentage |
| `routePlan` | Array of route steps (swap provider + percent) |
| `txn` | Base64 transaction payload (only when `user_account` is present) |

**Key insight:** Include `user_account` to get the executable transaction in the same call. No separate swap endpoint needed for v2 integrations.

---

## v1 — Legacy Endpoints

These endpoints are still operational and required for features not yet available on v2.

### GET /api/v1/quote

Provider-specific quote.

| Param | Type | Required | Description |
|---|---|---|---|
| `fromMint` | string | Yes | Input token mint address |
| `toMint` | string | Yes | Output token mint address |
| `amount` | integer | Yes | Input amount in smallest unit |
| `slippage` | integer | Yes | Slippage in basis points |
| `provider` | string | Yes | DEX provider to route through |
| `pool` | string | No | Custom pool address |

### GET /api/v1/quote/all

Compare quotes from all supported DEX providers simultaneously.

| Param | Type | Required | Description |
|---|---|---|---|
| `fromMint` | string | Yes | Input token mint address |
| `toMint` | string | Yes | Output token mint address |
| `amount` | integer | Yes | Input amount in smallest unit |
| `slippage` | integer | Yes | Slippage in basis points |

### GET /api/v1/swap

Get a serialized swap transaction for a specific provider.

| Param | Type | Required | Description |
|---|---|---|---|
| `owner` | string | Yes | Wallet address of the user (signer) |
| `fromMint` | string | Yes | Input token mint address |
| `toMint` | string | Yes | Output token mint address |
| `amount` | integer | Yes | Input amount in smallest unit |
| `slippage` | integer | Yes | Slippage in basis points |
| `provider` | string | Yes | DEX provider to route through |
| `pool` | string | No | Custom pool address for direct routing |
| `feeLamports` | integer | No | Custom fee amount in lamports |
| `feeReceiver` | string | No | Account receiving the custom fee (required if `feeLamports` set) |
| `priorityMicroLamports` | integer | No | Compute unit price for priority fees |
| `mevSafe` | boolean | No | If `true`, includes Jito tip instruction for MEV protection |
| `gasless` | boolean | No | If `true`, gasless swap. **Only valid if output token is SOL** |

**Response:** base64-encoded serialized `VersionedTransaction`. Deserialize → sign → submit via RPC.

### GET /api/v1/swap/bundle

Submit a signed transaction via Jito bundle for MEV protection.

| Param | Type | Required | Description |
|---|---|---|---|
| `signedTransaction` | string | Yes | Base64-encoded signed transaction |

**Response:** JSON with bundle ID and transaction hash.

### GET /api/v1/fee/custom

Generate a custom fee transfer transaction.

| Param | Type | Required | Description |
|---|---|---|---|
| `payer` | string | Yes | Address of the fee payer |
| `receiver` | string | Yes | Address of the fee receiver |
| `lamports` | integer | Yes | Fee amount in lamports |

**Response:** JSON with serialized transaction.

---

## Supported Providers

| Provider | ID | Type |
|---|---|---|
| Raydium | `raydium` | AMM |
| Raydium CPMM | `raydium-cpmm` | Constant Product |
| Orca | `orca` | CLMM |
| Meteora | `meteora` | AMM |
| Meteora DLMM | `meteora-dlmm` | Dynamic Liquidity |
| Pump.fun | `pump-fun` | Bonding Curve |
| Moonshot | `moonshot` | Bonding Curve |
| Stabble | `stabble` | Stable |
| PrintDEX | `printdex` | AMM |
| GooseFX | `goosefx` | AMM |

---

## Parameter Mapping Across Versions

| Concept | v2/Q1 (`/api/v2/quote`) | v1 (`/api/v1/*`) |
|---|---|---|
| Input token | `src_mint` | `fromMint` |
| Output token | `dst_mint` | `toMint` |
| Amount | `amount_in` | `amount` |
| Slippage | `slippage_bps` | `slippage` |
| Get executable tx | Include `user_account` in quote | Separate `/api/v1/swap` call |

---

## Slippage Recommendations

| Pair Type | BPS | Percentage |
|---|---|---|
| Stablecoin swaps | 5-10 | 0.05-0.1% |
| Major pairs (SOL/USDC) | 10-50 | 0.1-0.5% |
| Volatile tokens | 50-100 | 0.5-1% |
| Arbitrage | 10 | 0.1% |
