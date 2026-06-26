---
name: butter-swap
version: 1.0.0
description: |
  Butter Network DEX Aggregator for cross-chain token swaps. Get swap quotes, route transaction data, and cross-chain routing information.
  Use this skill whenever the user wants to swap tokens across different blockchain networks, needs cross-chain swap quotes, or wants to build cross-chain DEX aggregation features.
  Trigger: "cross-chain swap", "Butter Router", "swap tokens", "bridge tokens", "/route", "/swap", "get swap route", "get swap transaction", "ButterSwap"
repository: https://github.com/butternetwork/butter-swap-skill
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# Butter Swap

This skill provides integration with Butter Router API for cross-chain token swaps. It aggregates DEX routes across multiple chains to find optimal swap paths.

## Base URL

```
BASE_URL=https://bs-router-v3.chainservice.io
```

All API endpoints use `{BASE_URL}` as the base.

## API Response Format

All responses follow this structure:

```json
{
  "errno": 0,
  "message": "success",
  "data": [{ ... }]  // data is an array
}
```

**Note:** The `data` field is always an array `[{...}]`, not an object.

| errno | Meaning                                                       |
| ----- | ------------------------------------------------------------- |
| 0     | Success                                                       |
| 2000  | Parameter error (e.g., missing entrance parameter)            |
| 2003  | No Route Found (liquidity insufficient or pair not supported) |
| 2004  | Insufficient Liquidity (amount exceeds max)                   |
| other | Error (check message)                                         |

## Common Use Cases

### 1. Get Supported Chains

**Goal:** Find out which blockchains are supported for cross-chain swaps.

**Endpoint:** `GET /supportedChainInfo`

**Example:**

```bash
curl -X GET "{BASE_URL}/supportedChainInfo"
```

---

### 2. Find Token Information

**Goal:** Look up token details by contract address.

**Endpoint:** `GET /findToken`

**Example:**

```bash
curl -X GET "{BASE_URL}/findToken?address=0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
```

**Response includes:** chainId, address, name, symbol, decimals, usdPrice, image

---

### 3. Get Swap Route

**Goal:** Query optimal routes for cross-chain token swaps and get quote.

**Endpoint:** `GET /route`

**Parameters:**

| Parameter       | Type   | Required | Description                                                                       |
| --------------- | ------ | -------- | --------------------------------------------------------------------------------- |
| fromChainId     | number | Yes      | Source chain ID (e.g., 1 for Ethereum, 56 for BSC)                                |
| toChainId       | number | Yes      | Destination chain ID                                                              |
| amount          | string | Yes      | Amount to swap (human readable, e.g., "100" for 100 USDT, NOT wei)                |
| tokenInAddress  | string | Yes      | Input token address (use `0x0000000000000000000000000000000000000000` for native) |
| tokenOutAddress | string | Yes      | Output token address on destination chain                                         |
| type            | string | No       | "exactIn" or "exactOut" (default: exactIn)                                        |
| slippage        | number | No       | Slippage in bps, default 100 (1%)                                                 |
| entrance        | string | No       | Router entrance (default: "agent")                                                |

**Example:**

```bash
curl -X GET "{BASE_URL}/route?fromChainId=1&toChainId=56&amount=100&tokenInAddress=0xdAC17F958D2ee523a2206206994597C13D831ec7&tokenOutAddress=0x55d398326f99059fF775485246999027B3197955&type=exactIn&slippage=100&entrance=agent"
```

**Note:** Use human-readable amount (e.g., "100" for 100 USDT), NOT wei units. If the `entrance` parameter is not provided, it defaults to "agent".

**Response includes:**

- `hash`: Route identifier for getting swap transaction
- `amountIn` / `amountOut`: Expected input/output amounts
- `bridgeFee`: Fee for bridging
- `gasFee`: Estimated gas cost
- `srcChain` / `dstChain`: Chain details with token addresses

---

### 4. Get Swap Transaction

**Goal:** Assemble transaction data for executing a swap using the route hash.

**Endpoint:** `GET /swap`

**Parameters:**

| Parameter | Type   | Required | Description                              |
| --------- | ------ | -------- | ---------------------------------------- |
| hash      | string | Yes      | Route hash from /route response          |
| from      | string | Yes      | Sender wallet address                    |
| receiver  | string | Yes      | Receiver address                         |
| slippage  | number | no       | Slippage in bps (100 = 1%, default: 100) |

**Example:**

```bash
curl -X GET "{BASE_URL}/swap?hash=0xabc123...&slippage=100&from=0x123...&receiver=0x456..."
```

**Response includes:**

- `to`: Contract address to call
- `data`: Calldata for the transaction
- `value`: Native token value to send (if any)
- `chainId`: Target chain ID

---

### 5. Get Complete Swap (Route + Swap TX)

**Goal:** Get route and swap transaction data in one call.

**Endpoint:** `GET /routeAndSwap`

Combines `/route` and `/swap` endpoints. Parameters are the same as `/route` plus `from` and `receiver`.

**Example:**

```bash
curl -X GET "{BASE_URL}/routeAndSwap?fromChainId=1&toChainId=56&amount=100&tokenInAddress=0xdAC17F958D2ee523a2206206994597C13D831ec7&tokenOutAddress=0x55d398326f99059fF775485246999027B3197955&type=exactIn&slippage=100&entrance=agent&from=0xA015d9e9206859c13201BB3D6B324d6634276534&receiver=0xA015d9e9206859c13201BB3D6B324d6634276534"
```

**Response includes:**

- `route`: Same as /route response
- `txParam`: Transaction data (to, data, value, chainId)
- `error`: If swap fails, contains error details

---

## Common Workflows

### Cross-Chain Swap Flow

1. **Get supported chains**: Call `/supportedChainInfo` to see available networks
2. **Find tokens**: Use `/findToken` to get token addresses and decimals
3. **Get quote**: Call `/route` to get optimal route and expected output
4. **Get transaction**: Use hash from route to call `/swap` for transaction data
5. **Execute**: User signs and submits the transaction

### One-Call Swap

Use `/routeAndSwap` to skip step 3-4 and get everything in one request.

---

## Common Chain IDs

| Chain     | Chain ID |
| --------- | -------- |
| Ethereum  | 1        |
| BSC       | 56       |
| Polygon   | 137      |
| Arbitrum  | 42161    |
| Optimism  | 10       |
| Base      | 8453     |
| Avalanche | 43114    |
| Solana    | 7560     |

---

## MCP Tools

This skill uses butter-router-mcp for tool-based access:

### get_supported_chain_info

Query all supported blockchains.

### find_token

Find token information by token address.

### get_route

Query best routes for cross-chain token swap.

- `fromChainId`: Source chain ID
- `toChainId`: Destination chain ID
- `amount`: Amount in human readable format (e.g., "100" for 100 USDT, NOT wei)
- `tokenInAddress`: Input token address (use `0x000...0000` for native)
- `tokenOutAddress`: Output token address
- `type`: "exactIn" or "exactOut"
- `slippage`: Slippage in bps (default: 100 = 1%)
- `entrance`: Required, must be "agent"

**Important:** The response `data` is an **array** that may contain multiple routes. You MUST handle this as follows:

1. If `data.length === 0`: No routes found - inform user
2. If `data.length === 1`: Use the single route
3. If `data.length > 1`: Present all routes to user for selection

**When multiple routes are available, display each route with:**

- Route index (1, 2, 3...)
- `hash`: Route identifier
- `bridgeFee`: Bridge fee amount and symbol
- `gasFee`: Gas fee amount and symbol
- `dex`: The DEX exchange path used (e.g., "UniV3 > PancakeV3")
- `srcChain.totalAmountIn`: Input amount
- `dstChain.totalAmountOut`: Output amount (after fees)
- `minAmountOut`: Minimum output amount (with slippage protection)

**Always include the `dex` field in the display - this shows which DEX or path was used for the swap.**

**Then ask user to select** which route to use by entering the route number (1, 2, 3...).

After user selects a route, use the selected route's `hash` to call `get_swap` for transaction data.

**When calling get_swap, ask user for slippage preference:**

- If user specifies slippage (e.g., 100 = 1%, 50 = 0.5%, 500 = 5%), use that value
- If user does not specify, use default slippage = 100 (1%)

### get_swap

Assemble transaction data based on route hash.

**Parameters:**

| Parameter    | Type   | Required | Default | Description                                       |
| ------------ | ------ | -------- | ------- | ------------------------------------------------- |
| hash         | string | Yes      | -       | Route hash from getRoute response                 |
| slippage     | number | No       | 100     | Slippage in bps (e.g., 100 = 1%)                  |
| from         | string | Yes      | -       | Sender wallet address                             |
| receiver     | string | Yes      | -       | Receiver address on destination chain             |
| refundAddr   | string | No       | from    | Refund address if transaction fails               |
| feeToken     | string | No       | -       | Address of token to pay protocol fees (optional)  |
| destGasLimit | string | No       | -       | Custom gas limit for destination chain (optional) |

**Display real transaction data to user, including:**

- `to`: Contract address to call
- `data`: Full calldata (show full hex, not truncated)
- `value`: Native token value in hex and human readable
- `chainId`: Target chain ID
- `method`: Contract method name

---

## Example Response

### Route Response

```json
{
  "errno": 0,
  "message": "success",
  "data": [
    {
      "hash": "0xcbb224a6ecb83a32a17643877941d27df226784be9688ba8f7833f256c5170ec",
      "bridgeFee": { "amount": "0.449954", "symbol": "USDT" },
      "gasFee": { "amount": "0.00006751415372", "symbol": "ETH" },
      "dex": "UniV3 > PancakeV3",
      "srcChain": {
        "chainId": "1",
        "totalAmountIn": "100.0",
        "totalAmountOut": "100.0"
      },
      "dstChain": {
        "chainId": "56",
        "totalAmountIn": "99.550046",
        "totalAmountOut": "99.550046"
      },
      "minAmountOut": { "amount": "99.550046", "symbol": "USDT" }
    }
  ]
}
```

### Swap Transaction

```json
{
  "errno": 0,
  "message": "success",
  "data": [
    {
      "to": "0xEE0319cF0BCa5d09333f9F6277743E8De31bD69A",
      "data": "0x6e1537da000000000000000000000000766f3377497C66c31a5692A435cF3E72Dcc2d4Fc000000000000000000000000766f3377497C66c31a5692A435cF3E72Dcc2d4Fc...",
      "value": "0x0f43fc2c04ee0000",
      "chainId": "1",
      "method": "swapAndBridge"
    }
  ]
}
```

### Common Errors

| errno | Message                           | Solution                                    |
| ----- | --------------------------------- | ------------------------------------------- |
| 2000  | Parameter error: Missing entrance | Add `entrance=Butter%2B` parameter          |
| 2003  | No Route Found                    | Try different token pair or chain           |
| 2004  | Insufficient Liquidity            | Amount exceeds max liquidity, reduce amount |

### API Documentation

For detailed API documentation, visit: https://docs.butternetwork.io/butter-swap-integration/integration-guide
