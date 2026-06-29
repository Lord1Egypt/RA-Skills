# Blockchain Scanner Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `blockchain-scanner`

x402 availability: not enabled for this product.

## `balance`

Action slug: `balance`

Price: `5` credits

Get native token balance (ETH or MATIC) for one or more wallet addresses. Returns balance in both native units and wei.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `array` | yes | Ethereum address(es) to query. Must be 0x-prefixed 42-character hex strings. 1 to 20 addresses allowed. |
| `chain` | `string` | no | Blockchain network to query. Default: ethereum. |

Sample parameters:

```json
{
  "address": [
    "example addre"
  ],
  "chain": "ethereum"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Ethereum address(es) to query. Must be 0x-prefixed 42-character hex strings. 1 to 20 addresses allowed.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "chain": {
    "description": "Blockchain network to query. Default: ethereum.",
    "enum": [
      "ethereum",
      "base",
      "base_sepolia",
      "polygon",
      "arbitrum",
      "optimism"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `contract_abi`

Action slug: `contract-abi`

Price: `5` credits

Retrieve the ABI (Application Binary Interface) JSON for a verified smart contract. Returns the full ABI array plus counts of functions and events.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `array` | yes | Exactly 1 contract address to query. Must be 0x-prefixed 42-character hex string. |
| `chain` | `string` | no | Blockchain network to query. Default: ethereum. |

Sample parameters:

```json
{
  "address": [
    "example addre"
  ],
  "chain": "ethereum"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Exactly 1 contract address to query. Must be 0x-prefixed 42-character hex string.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "chain": {
    "description": "Blockchain network to query. Default: ethereum.",
    "enum": [
      "ethereum",
      "base",
      "base_sepolia",
      "polygon",
      "arbitrum",
      "optimism"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `gas_oracle`

Action slug: `gas-oracle`

Price: `5` credits

Get current gas price estimates (safe/standard/fast) for a blockchain network. Returns prices in Gwei with EIP-1559 base fee suggestions.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | `string` | no | Blockchain network to query. Default: ethereum. |

Sample parameters:

```json
{
  "chain": "ethereum"
}
```

Generated JSON parameter schema:

```json
{
  "chain": {
    "description": "Blockchain network to query. Default: ethereum.",
    "enum": [
      "ethereum",
      "base",
      "base_sepolia",
      "polygon",
      "arbitrum",
      "optimism"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `token_balance`

Action slug: `token-balance`

Price: `5` credits

Get ERC-20 token balances for one or more wallet addresses. Supports major stablecoins and wrapped tokens across all supported chains.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `array` | yes | Ethereum address(es) to query. Must be 0x-prefixed 42-character hex strings. 1 to 20 addresses allowed. |
| `chain` | `string` | no | Blockchain network to query. Default: ethereum. |
| `token` | `string` | no | Token symbol to query (e.g., 'USDC', 'USDT', 'PYUSD', 'DAI', 'WETH'). Use 'all' to get all supported tokens on the selected chain. Defaults to 'all' if not provided. |

Sample parameters:

```json
{
  "address": [
    "example addre"
  ],
  "chain": "ethereum",
  "token": "example token"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Ethereum address(es) to query. Must be 0x-prefixed 42-character hex strings. 1 to 20 addresses allowed.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "chain": {
    "description": "Blockchain network to query. Default: ethereum.",
    "enum": [
      "ethereum",
      "base",
      "base_sepolia",
      "polygon",
      "arbitrum",
      "optimism"
    ],
    "required": false,
    "type": "string"
  },
  "token": {
    "description": "Token symbol to query (e.g., 'USDC', 'USDT', 'PYUSD', 'DAI', 'WETH'). Use 'all' to get all supported tokens on the selected chain. Defaults to 'all' if not provided.",
    "required": false,
    "type": "string"
  }
}
```

## `transactions`

Action slug: `transactions`

Price: `5` credits

Get paginated transaction history for a single address. Returns 100 transactions per request sorted by most recent first.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `array` | yes | Exactly 1 wallet address to query. Must be 0x-prefixed 42-character hex string. |
| `chain` | `string` | no | Blockchain network to query. Default: ethereum. |
| `transaction_range` | `array` | no | Range of transactions to fetch as [start, end] integers. Must span exactly 100 transactions. Index 1 = most recent. Default: [1, 100]. |

Sample parameters:

```json
{
  "address": [
    "example addre"
  ],
  "chain": "ethereum",
  "transaction_range": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Exactly 1 wallet address to query. Must be 0x-prefixed 42-character hex string.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "chain": {
    "description": "Blockchain network to query. Default: ethereum.",
    "enum": [
      "ethereum",
      "base",
      "base_sepolia",
      "polygon",
      "arbitrum",
      "optimism"
    ],
    "required": false,
    "type": "string"
  },
  "transaction_range": {
    "description": "Range of transactions to fetch as [start, end] integers. Must span exactly 100 transactions. Index 1 = most recent. Default: [1, 100].",
    "items": {
      "type": "integer"
    },
    "required": false,
    "type": "array"
  }
}
```
