# Cesto API Reference — Endpoint Details

Base URL: `https://backend.cesto.co`

Most endpoints are public GET requests returning JSON with no authentication required. Authenticated endpoints are noted individually.

## Table of Contents

- [1. List All Baskets](#1-list-all-baskets) — `GET /products`
- [2. Basket Detail](#2-basket-detail) — `GET /products/{slug}`
- [3. Token Analysis](#3-token-analysis) — `GET /products/{id}/analyze`
- [4. Historical Graph](#4-historical-graph) — `GET /products/{id}/graph`
- [5. Analytics Summary](#5-analytics-summary) — `GET /products/analytics`
- [6. Simulate Portfolio Graph](#6-simulate-portfolio-graph) — `POST /agent/simulate-graph`

---

## 1. List All Baskets

**`GET /products`**

Returns an array of all baskets (published and unpublished).

### Response Structure

Returns: `Array<Basket>`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` (UUID) | Unique basket identifier. Use for `/analyze`, `/graph`, and `/analytics` endpoints. |
| `slug` | `string` | URL-friendly name (e.g., `"war-mode"`). Use for `/products/{slug}` endpoint. |
| `name` | `string` | Display name (e.g., `"War Mode"`) |
| `description` | `string` | Short summary of the basket strategy |
| `logoUrl` | `string` | URL to the basket's logo image |
| `category` | `string` | Basket type: `"swap"`, `"staking"`, `"prediction"`, `"lending"`, or `"strategy"` |
| `tags` | `string[]` | Descriptive tags (e.g., `["swap", "diversification", "defense"]`) |
| `isActive` | `boolean` | Whether the basket is currently active |
| `isPublished` | `boolean` | Whether the basket is publicly visible. Filter to `true` for user-facing data. |
| `viewBlockedCountries` | `string[]` | Country codes blocked from viewing |
| `investmentBlockedCountries` | `string[]` | Country codes blocked from investing |
| `pointMultiplier` | `integer` | Points multiplier for the basket |
| `latestVersion` | `object` | Current version details (see below) |
| `geoStatus` | `object` | Geo-restriction status |
| `ondoTradingStatus` | `object \| null` | Ondo trading availability |

### `latestVersion` Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` (UUID) | Version identifier |
| `version` | `integer` | Version number |
| `label` | `string` | Version label (e.g., `"v1.0.0"`) |
| `estimatedApy` | `number \| null` | Estimated APY if available |
| `riskLevel` | `string` | API-provided risk level: `"LOW"`, `"MEDIUM"`, or `"HIGH"` |
| `minimumInvestment` | `string` | Minimum investment in smallest unit. Divide by `1,000,000` for USDC. |
| `isStable` | `boolean` | Whether the basket uses stable assets |
| `activePositionCount` | `integer` | Number of active investors |

### Example Response (truncated)

```json
[
  {
    "id": "adb0abe3-5ce0-40b0-80a4-e7a39f21807a",
    "slug": "war-mode",
    "name": "War Mode",
    "description": "When the world gets scary, defense stocks print money...",
    "logoUrl": "https://res.cloudinary.com/dcyihhgo6/image/upload/...",
    "category": "swap",
    "tags": ["swap", "diversification", "multi-token", "defense"],
    "isActive": true,
    "isPublished": true,
    "viewBlockedCountries": [],
    "investmentBlockedCountries": [],
    "pointMultiplier": 3,
    "latestVersion": {
      "id": "5bbce7b9-a6c6-431a-a68e-635766783919",
      "version": 2,
      "label": "v1.0.0",
      "estimatedApy": null,
      "riskLevel": "MEDIUM",
      "minimumInvestment": "20000000",
      "isStable": true,
      "activePositionCount": 1
    }
  }
]
```

---

## 2. Basket Detail

**`GET /products/{slug}`**

Returns full detail for a single basket, including strategy definition, token allocations, and performance data.

### Response Structure

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` (UUID) | Basket identifier |
| `version` | `integer` | Current version number |
| `riskLevel` | `string` | `"LOW"`, `"MEDIUM"`, or `"HIGH"` |
| `minimumInvestment` | `string` | In smallest unit (divide by 1,000,000 for USDC) |
| `tradingSchedule` | `object` | Trading window schedule (`openCron`, `timezone`, `durationMinutes`) |
| `isActive` | `boolean` | Whether currently active |
| `name` | `string` | Basket display name |
| `slug` | `string` | URL slug |
| `logoUrl` | `string` | Logo image URL |
| `category` | `string` | Basket type |
| `tags` | `string[]` | Descriptive tags |
| `description` | `string` | Short description |
| `tokensInvolved` | `string[]` | Array of token mint addresses used |
| `protocolsInvolved` | `string[]` | Protocols used (e.g., `["jupiter"]`, `["kamino", "dflow"]`) |
| `tokenPerformance` | `object` | 1-year performance (see below) |
| `tokenPerformance7d` | `object \| null` | 7-day performance. `null` if unavailable. |
| `tokenPerformance30d` | `object \| null` | 30-day performance. `null` if unavailable. |
| `definition` | `object` | Strategy definition (see below) |
| `geoStatus` | `object` | `{ canView, canInvest }` |
| `ondoTradingStatus` | `object` | Ondo token trading status |

### `tokenPerformance` Object

| Field | Type | Description |
|-------|------|-------------|
| `avgPercentChange` | `number` | Average percent change |
| `daysAvailable` | `integer` | Number of days of data |
| `startDate` | `string` (ISO 8601) | Performance period start |
| `endDate` | `string` (ISO 8601) | Performance period end |
| `annualizedReturn` | `number` | Annualized return percentage |
| `netPnL` | `number` | Net profit/loss percentage |
| `pricePnL` | `number` | Price-based PnL |
| `netAPY` | `number \| null` | Net APY (for staking baskets) |
| `priceAPY` | `number` | Price-based APY |
| `yieldBreakdown` | `object \| null` | Yield breakdown (for staking baskets) |

### `tokenPerformance7d` / `tokenPerformance30d` Object

| Field | Type | Description |
|-------|------|-------------|
| `return` | `number` | Period return percentage |
| `avgPercentChange` | `number` | Average percent change |
| `daysAvailable` | `integer` | Days in period (7 or 30) |
| `startDate` | `string` (ISO 8601) | Period start |
| `endDate` | `string` (ISO 8601) | Period end |
| `netPnL` | `number` | Net PnL |
| `pricePnL` | `number` | Price PnL |
| `netAPY` | `number \| null` | Net APY |
| `priceAPY` | `number` | Price APY |

### `definition` Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Definition identifier |
| `name` | `string` | Definition name |
| `type` | `string` | Definition type |
| `about` | `string` | Strategy description (plain text) |
| `risk` | `string` | Risk assessment (markdown) |
| `tokenMint` | `string` | Primary token mint address |
| `tokenDecimal` | `integer` | Token decimal places |
| `nodes` | `Array<Node>` | Swap/action steps (see below) |
| `tokenAllocations` | `Array<Allocation>` | Token allocation breakdown (see below) |
| `connections` | `Array<Connection>` | Node connections (`{ source, target }`) |

### `definition.nodes[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Node identifier (e.g., `"swap-to-lmt"`) |
| `label` | `string` | Human-readable name (e.g., `"Buy Lockheed Martin"`) |
| `nodeType` | `string` | Node type (e.g., `"swap.token"`) |
| `protocols` | `string[]` | Protocols used by this node |
| `parameters` | `object` | Node parameters including `toToken` |
| `description` | `string` | Node description |

### `definition.tokenAllocations[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `mint` | `string` | Token mint address |
| `token` | `string` | Token identifier |
| `nodeId` | `string` | References `nodes[].id` for readable name mapping |
| `percentage` | `number` | Allocation percentage (e.g., `22` for 22%) |

### Example Response (truncated)

```json
{
  "id": "adb0abe3-5ce0-40b0-80a4-e7a39f21807a",
  "version": 2,
  "riskLevel": "MEDIUM",
  "minimumInvestment": "20000000",
  "name": "War Mode",
  "slug": "war-mode",
  "category": "swap",
  "protocolsInvolved": ["jupiter"],
  "tokenPerformance": {
    "annualizedReturn": 53.55,
    "netPnL": 53.33,
    "daysAvailable": 365,
    "startDate": "2025-03-18T00:00:00.000Z",
    "endDate": "2026-03-18T00:00:00.000Z"
  },
  "tokenPerformance7d": null,
  "tokenPerformance30d": null,
  "definition": {
    "about": "Defense primes + AI/cyber barbell...",
    "risk": "## War Mode Strategy\n\n...",
    "nodes": [
      {
        "id": "swap-to-lmt",
        "label": "Buy Lockheed Martin",
        "nodeType": "swap.token",
        "protocols": ["jupiter"]
      }
    ],
    "tokenAllocations": [
      { "mint": "EoReHwUnGG...", "nodeId": "swap-to-lmt", "percentage": 22 }
    ]
  }
}
```

---

## 3. Token Analysis

**`GET /products/{id}/analyze`**

Returns per-token market data and aggregated performance for a basket. Use the basket `id` (UUID), not the slug.

### Response Structure

| Field | Type | Description |
|-------|------|-------------|
| `nodeAnalyses` | `Array<NodeAnalysis>` | Per-token analysis data |
| `aggregates` | `object` | Aggregated basket-level metrics |

### `nodeAnalyses[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `category` | `string` | Node category (e.g., `"swap"`) |
| `nodeType` | `string` | Node type (e.g., `"swap.token"`) |
| `protocol` | `string` | Protocol used (e.g., `"jupiter"`) |
| `id` | `string` | Node identifier (matches `definition.nodes[].id`) |
| `timestamp` | `number` | Analysis timestamp (epoch ms) |
| `version` | `integer` | Analysis version |
| `inputSymbol` | `string` | Input token symbol (e.g., `"USDC"`) |
| `outputSymbol` | `string` | Output token symbol (e.g., `"LMTon"`) |
| `configuration` | `object` | Swap configuration (inputToken, outputToken, inputAmount, slippage, chain) |
| `marketData` | `object` | Market data including token performance (see below) |
| `fees` | `object` | Fee data: `{ gasFee, totalUSD }` |
| `yieldData` | `object \| null` | Yield data for staking nodes |

### `marketData` Object

| Field | Type | Description |
|-------|------|-------------|
| `outputAmount` | `string` | Expected output amount |
| `exchangeRate` | `string` | Current exchange rate |
| `priceImpact` | `string` | Expected price impact |
| `tokenPerformance` | `object` | Price performance data (see below) |

### `marketData.tokenPerformance` Object

| Field | Type | Description |
|-------|------|-------------|
| `currentPrice` | `number` | Current token price in USD |
| `priceChange24h` | `number` | 24-hour price change (decimal, multiply by 100 for %) |
| `priceChange7d` | `number` | 7-day price change (decimal) |
| `priceChange30d` | `number` | 30-day price change (decimal) |
| `priceChange60d` | `number` | 60-day price change (decimal) |
| `priceChange90d` | `number` | 90-day price change (decimal) |
| `priceChange180d` | `number` | 180-day price change (decimal) |
| `priceChange1y` | `number` | 1-year price change (decimal) |

### `aggregates` Object

| Field | Type | Description |
|-------|------|-------------|
| `tokensInvolved` | `string[]` | Array of all token mint addresses |
| `tokenPerformance` | `object` | 1-year aggregated performance (same structure as basket detail) |
| `tokenPerformance7d` | `object \| null` | 7-day aggregated performance |
| `tokenPerformance30d` | `object \| null` | 30-day aggregated performance |

### Example Response (truncated)

```json
{
  "nodeAnalyses": [
    {
      "category": "swap",
      "nodeType": "swap.token",
      "protocol": "jupiter",
      "id": "swap-to-lmt",
      "inputSymbol": "USDC",
      "outputSymbol": "LMTon",
      "configuration": {
        "inputToken": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "outputToken": "EoReHwUnGG...",
        "inputAmount": "0.22",
        "slippage": 100,
        "chain": "sol"
      },
      "marketData": {
        "tokenPerformance": {
          "currentPrice": 636.33,
          "priceChange24h": 0,
          "priceChange7d": -0.0202,
          "priceChange30d": -0.0198,
          "priceChange1y": 0.393
        }
      },
      "fees": { "gasFee": 0.005, "totalUSD": 0.5 }
    }
  ],
  "aggregates": {
    "tokensInvolved": ["EPjFWdd5...", "EoReHw..."],
    "tokenPerformance": {
      "annualizedReturn": 48.25,
      "netPnL": 48.21,
      "daysAvailable": 365
    },
    "tokenPerformance7d": { "return": -1.83 },
    "tokenPerformance30d": { "return": 1.23 }
  }
}
```

---

## 4. Historical Graph

**`GET /products/{id}/graph`**

Returns daily historical time series comparing basket performance against S&P 500 benchmark. Both start at 1000. Use the basket `id` (UUID).

### Response Structure

| Field | Type | Description |
|-------|------|-------------|
| `workflowId` | `string` (UUID) | Workflow identifier |
| `name` | `string` | Basket name |
| `timeSeries` | `Array<DataPoint>` | Daily data points (~365 entries) |
| `metrics` | `object` | Pre-computed metrics (see below) |
| `assetPerformance` | `Array<AssetReturn>` | Per-asset return percentages |
| `contributions` | `Array<Contribution>` | Per-asset contribution to total return |
| `assetSparklines` | `Array<Sparkline>` | Per-asset daily value history |
| `liquidationInfo` | `object` | Liquidation event data (see below) |

### `timeSeries[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `string` (ISO 8601) | Date |
| `portfolioValue` | `number` | Basket value (starts at 1000) |
| `sp500Value` | `number` | S&P 500 benchmark value (starts at 1000) |
| `isLiquidated` | `boolean` | Whether a liquidation event occurred on this date |

### `metrics` Object

| Field | Type | Description |
|-------|------|-------------|
| `totalReturn` | `number` | Total return percentage |
| `cagr` | `number` | Compound annual growth rate |
| `volatility` | `number` | Annualized volatility |
| `maxDrawdown` | `number` | Maximum peak-to-trough decline (%) |

### `assetPerformance[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `token` | `string` | Token symbol |
| `mint` | `string` | Token mint address |
| `returnPct` | `number` | Individual asset return percentage |

### `contributions[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `token` | `string` | Token symbol |
| `mint` | `string` | Token mint address |
| `contribution` | `number` | Contribution to portfolio return (percentage points) |

### `liquidationInfo` Object

| Field | Type | Description |
|-------|------|-------------|
| `hasLiquidations` | `boolean` | Whether any liquidation events occurred |
| `liquidationEvents` | `array` | List of liquidation events (empty if none) |
| `liquidationThresholds` | `array` | Liquidation threshold data |

### Example Response (truncated)

```json
{
  "workflowId": "e3b58de4-c860-40fc-8f8a-9adecddd3df5",
  "name": "War Mode",
  "timeSeries": [
    {
      "timestamp": "2025-03-18T00:00:00.000Z",
      "portfolioValue": 1000,
      "sp500Value": 1000,
      "isLiquidated": false
    },
    {
      "timestamp": "2025-03-19T00:00:00.000Z",
      "portfolioValue": 1002.7,
      "sp500Value": 1003.1,
      "isLiquidated": false
    }
  ],
  "metrics": {
    "totalReturn": 48.21,
    "cagr": 48.25,
    "volatility": 25.26,
    "maxDrawdown": 16.34
  },
  "assetPerformance": [
    { "token": "LMTon", "mint": "EoReHwUnGG...", "returnPct": 40.05 }
  ],
  "contributions": [
    { "token": "LMTon", "mint": "EoReHwUnGG...", "contribution": 8.23 }
  ],
  "liquidationInfo": {
    "hasLiquidations": false,
    "liquidationEvents": [],
    "liquidationThresholds": []
  }
}
```

---

## 5. Analytics Summary

**`GET /products/analytics`**

Returns a summary analytics object keyed by product ID. Covers all baskets (published and unpublished).

### Response Structure

Returns: `Object<productId, AnalyticsEntry>`

Each entry is keyed by the basket's `id` (UUID).

### `AnalyticsEntry` Object

| Field | Type | Description |
|-------|------|-------------|
| `protocolsInvolved` | `string[]` | Protocols used by the basket |
| `tokensInvolved` | `string[]` | Token mint addresses |
| `tokenPerformance` | `object \| null` | 1-year performance (same structure as basket detail). `null` for prediction baskets. |
| `tokenPerformance7d` | `object \| null` | 7-day performance |
| `tokenPerformance30d` | `object \| null` | 30-day performance |
| `priceChange24h` | `number` | 24-hour basket price change percentage |
| `tokenPriceChanges` | `object` | Per-token 24h price changes, keyed by mint address |

### Example Response (truncated)

```json
{
  "adb0abe3-5ce0-40b0-80a4-e7a39f21807a": {
    "protocolsInvolved": ["jupiter"],
    "tokensInvolved": ["EPjFWdd5...", "EoReHwUnGG..."],
    "tokenPerformance": {
      "annualizedReturn": 48.25,
      "netPnL": 48.21
    },
    "tokenPerformance7d": { "return": -1.83 },
    "tokenPerformance30d": { "return": 1.23 },
    "priceChange24h": 0.5,
    "tokenPriceChanges": {
      "EoReHwUnGG...": 0.3
    }
  }
}
```

---

## 6. Simulate Portfolio Graph

**`POST /agent/simulate-graph`**

Simulates historical performance of a custom token allocation and compares it against the S&P 500 benchmark. Both start at 1000.

**Authentication required.** Use `scripts/api_request.py` which handles session headers internally.

### Request

**Headers:** Handled by `api_request.py`. Only the body needs to be provided.

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |

**Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `allocations` | `Array<Allocation>` | Yes | Token allocations (min 1 item) |
| `allocations[].token` | `string` | Yes | Token symbol (e.g. `"SOL"`, `"USDC"`) |
| `allocations[].mint` | `string` | Yes | Solana mint address |
| `allocations[].weight` | `number` | Yes | Allocation weight/percentage |
| `name` | `string` | Yes | Portfolio name |

### Example Request

```json
{
  "allocations": [
    {
      "token": "SOL",
      "mint": "So11111111111111111111111111111111111111112",
      "weight": 50
    },
    {
      "token": "USDC",
      "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "weight": 50
    }
  ],
  "name": "My Portfolio"
}
```

### Response Structure

| Field | Type | Description |
|-------|------|-------------|
| `workflowId` | `string` | Always `"agent-simulation"` |
| `name` | `string` | Portfolio name from request |
| `timeSeries` | `Array<DataPoint>` | Daily historical simulation data |
| `allocations` | `Array<Allocation>` | Token allocations from request |

### `timeSeries[]` Item

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `string` (ISO 8601) | Date |
| `portfolioValue` | `number` | Simulated portfolio value (starts at 1000) |
| `sp500Value` | `number` | S&P 500 benchmark value (starts at 1000) |
| `isLiquidated` | `boolean` | Whether portfolio was liquidated |

### Example Response (truncated)

```json
{
  "workflowId": "agent-simulation",
  "name": "My Portfolio",
  "timeSeries": [
    {
      "timestamp": "2025-03-20T00:00:00.000Z",
      "portfolioValue": 1000,
      "sp500Value": 1000,
      "isLiquidated": false
    },
    {
      "timestamp": "2025-03-21T00:00:00.000Z",
      "portfolioValue": 969.88,
      "sp500Value": 1000.33,
      "isLiquidated": false
    }
  ],
  "allocations": [
    {
      "token": "SOL",
      "mint": "So11111111111111111111111111111111111111112",
      "weight": 50
    },
    {
      "token": "USDC",
      "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "weight": 50
    }
  ]
}
```

### Error Responses

| Status | When |
|--------|------|
| 400 | Missing/invalid fields (empty allocations, missing name, etc.) |
| 403 | No valid session or API key provided |
