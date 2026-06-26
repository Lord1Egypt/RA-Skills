---
name: dapplooker-ai
description: DeFi intelligence suite — token metrics, perp trading data, technical analysis, smart money flows, staking yields, and AI-powered market research across Base, Solana, and 10+ perp DEXs
emoji: 🔮
homepage: https://docs.dapplooker.com/products/api-endpoints
version: 1.0.1
---

# DappLooker DeFi Intelligence

Access production-grade DeFi market intelligence via DappLooker's x402 API.

## Payment & Spending Safeguards

All endpoints require x402 payment in **USDC** on **Polygon** (Chain ID: 137).
**CRITICAL:** Always use Polygon for payments, even when querying Base or Solana data. The user's wallet is only funded on Polygon.

### Per-Call Pricing

| Function | Cost per Call |
|----------|-------------|
| `token_intelligence` | $0.005 |
| `perp_intelligence` | $0.005 |
| `historical_market_data` | $0.005 |
| `token_ta` | $0.005 |
| `trending_tokens` | $0.005 |
| `smart_money_trends` | $0.005 |
| `staking_intelligence` | $0.005 |
| `token_directory` | $0.005 |
| `market_mcp` | $0.10 |
| `live_perp_strategy` | $0.50 |

### Spending Rules
- **Always confirm with the user before making paid calls.** Tell them which endpoint you are calling and its cost.
- **Do not retry failed paid calls** without user approval.
- **Batch wisely:** If the user asks a broad question, prefer a single `market_mcp` call ($0.10) over multiple individual calls.
- **Session budget:** Unless the user explicitly raises it, assume a default spending cap of **$1.00 per conversation**. Alert the user if cumulative spending approaches this limit.

Payment is handled automatically via the OpenClaw Gateway. If you receive a 402, the Gateway handles payment and retries. Simply wait for the tool call to complete.

**Note:** All endpoints accept an optional `api_key` query parameter as an alternative to x402 payment. All endpoint URLs require a trailing slash where shown.

---

## Functions

### token_intelligence

**URL:** `GET https://api.dapplooker.com/v1/crypto-market/`

**Use when:** User asks about token price, market cap, volume, holders, social mindshare, or technical levels.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `base` or `solana` |
| `token_tickers` | string | No | Comma-separated tickers (e.g., `AIXBT,VIRTUAL`) |
| `token_addresses` | string | No | Comma-separated contract addresses |
| `token_ids` | string | No | Comma-separated internal IDs |
| `ecosystem` | string | No | Filter by ecosystem (e.g., `virtuals`) |
| `page` | number | No | Pagination page number |

**Note:** Provide at least one of `token_tickers`, `token_addresses`, `token_ids`, or `ecosystem`.

**Returns:** Token price, market cap, FDV, volume, supply, holder forensics (top 10/50/100 concentration), smart money buy/sell, dev wallet safety, technical levels (support/resistance/RSI/SMA), and X social metrics (mindshare, engagement, follower counts).

**Example:** "What's the price of AIXBT on Base?"

---

### perp_intelligence

**URL:** `GET https://api.dapplooker.com/v1/perp-intelligence/`

**Use when:** User asks about perp mark price, funding rates, open interest, orderbook liquidity, or technicals for a token on a specific DEX.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dex` | string | Yes | `hyperliquid`, `nado`, `paradex`, `pacifica`, `avantis`, `lighter`, `aster`, `grvt`, `variational`, `extended` |
| `token_ticker` | string | Yes | Token symbol (e.g., `BTC`, `ETH`, `SOL`) |

**Returns:** Mark/mid price, 24h change, bid-ask spread, orderbook liquidity & imbalance, open interest (with 1h/6h/24h changes), funding rate (current + trajectory), technicals (RSI, ATR, ADX, OBV, MACD at multiple intervals), structure (swing high/low, VWAP, EMA distance, Bollinger bands).

**Example:** "What's the BTC funding rate on Hyperliquid?"

---

### historical_market_data

**URL:** `GET https://api.dapplooker.com/v1/crypto-market-historical`

**Use when:** User wants time-series price, volume, and market cap data.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `base` or `solana` |
| `token_ticker` | string | No | Use one of ticker, address, or id |
| `token_address` | string | No | Token contract address |
| `token_id` | string | No | Internal token identifier |
| `start_date` | string | No | `YYYY-MM-DD` format |
| `end_date` | string | No | `YYYY-MM-DD` format |
| `page` | number | No | Pagination page number |

**Returns:** Daily records with date, price, volume, and market cap. Includes pagination metadata.

**Example:** "Show me VIRTUAL price history on Base"

---

### token_ta

**URL:** `GET https://api.dapplooker.com/v1/token-ta`

**Use when:** User asks about RSI, SMA, or support/resistance levels.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `base` or `solana` |
| `token_tickers` | string | No | Comma-separated tickers |
| `token_addresses` | string | No | Comma-separated contract addresses |
| `token_ids` | string | No | Comma-separated internal IDs |
| `ecosystem` | string | No | Filter by ecosystem |
| `page` | number | No | Pagination page number |

**Returns:** Support/resistance, RSI, and SMA at 1m, 5m, 15m, 1h, 4h, 1d, 1w intervals. Price change percentages across all intervals.

**Example:** "What are the RSI levels for AIXBT?"

---

### trending_tokens

**URL:** `GET https://api.dapplooker.com/v1/trending`

**Use when:** User wants to discover hot tokens by volume, market cap, or smart money activity.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `base` or `solana` |
| `strategy` | string | No | `mcap` (default), `volume_and_staking`, or `volume_and_smartmoney` |

**Returns:** Ranked tokens with volume, liquidity, market cap, and 1h/24h price changes.

**Example:** "What tokens are trending on Base?"

---

### smart_money_trends

**URL:** `GET https://api.dapplooker.com/v1/smart-money-trends/`

**Use when:** User asks about whale accumulation or smart money flows for a token.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `token_tickers` | string | No | Comma-separated tickers. Provide at least one filter. |
| `token_addresses` | string | No | Comma-separated contract addresses |

**Returns:** Net inflow/outflow by smart wallets at 24h, 7d, and 30d intervals (in USD and token amounts).

**Example:** "Are whales buying or selling VIRTUAL?"

---

### staking_intelligence

**URL:** `GET https://api.dapplooker.com/v1/stake-trends/`

**Use when:** User asks about staking TVL, yields, retention, or recent stake/unstake activity.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `token_tickers` | string | No | Comma-separated tickers. Provide at least one filter. |
| `token_addresses` | string | No | Comma-separated contract addresses |

**Returns:** Staking details (TVL, retention %, net staked, total stakers, holders), 24h stake/unstake trends, and recent staking activity with wallet types (regular, smart_money, dev).

**Example:** "How much is staked in 1000X?"

---

### market_mcp

**URL:** `POST https://api.dapplooker.com/v1/mcp`

**Use when:** User has a complex market question requiring AI-synthesized analysis from multiple data sources.

**Request body (JSON):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | Natural language market question |

**Returns:** AI-generated markdown analysis (`nlpResponse`) with data-backed insights. Present the `nlpResponse` directly to the user. Response time may be 5–15 seconds.

**Example:** "Compare mindshare of AIXBT vs VIRTUAL"

---

### live_perp_strategy

**URL:** `GET https://api.dapplooker.com/v1/live-perp-strategy/`

**Use when:** User wants AI-generated perp trading strategies.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `modelId` | string | No | AI model ID for inference |
| `promptId` | string | No | Strategy prompt ID |
| `category` | string | No | Token category filter (e.g., `trending`) |

**Returns:** AI-generated trading recommendations with risk analysis and actionable insights.

**Example:** "Give me a live perp trading strategy"

---

### token_directory

**URL:** `GET https://api.dapplooker.com/v1/crypto-metainfo/`

**Use when:** User wants to look up token metadata (name, ticker, contract address) across chains or ecosystems.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | No | `base` or `solana` |
| `ecosystem` | string | No | Filter by ecosystem (e.g., `virtuals`) |
| `token_addresses` | string | No | Comma-separated token contract addresses |
| `page` | number | No | Pagination page number |

**Returns:** Token objects with id, symbol, name, address, chain, and ecosystem. Includes pagination.

**Example:** "List all tokens in the Virtuals ecosystem on Base"

---

## Supported Chains

| Chain | Token Intel | TA | Historical | Trending | Smart Money | Staking |
|-------|-----------|-----|------------|----------|-------------|---------|
| Base | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Solana | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

## Supported Perp DEXs

Hyperliquid, Nado, Paradex, Pacifica, Avantis, Lighter, Aster, GRVT, Variational, Extended

---

## Documentation

Full API documentation: https://docs.dapplooker.com/products/api-endpoints
