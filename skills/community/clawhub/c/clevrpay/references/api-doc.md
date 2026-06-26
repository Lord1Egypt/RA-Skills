# Clevr Pay Skills API Documentation

## Overview

The Cleanverse Skills API is designed for integration with Large Language Models (LLMs), supporting the following capabilities:

- Retrieve A-Pass registration URL (magic link)
- Query A-Pass account information by blockchain address
- Query deposit wallet addresses (USDC, USDT)
- Query supported chain configuration (RPC, explorer, tokens, A-Pass addresses)
- Query deposit-eligible institution whitelist for supported tokens
- Register user wallet address and receive deposit address mapping
- Query user registration status, deposit address, and blacklist info

---

## Base URL

- **Sandbox**: `https://uatapi.cleanverse.com/api/skills`
- **Production**: `https://api.cleanverse.com/api/skills`

---

## API Update Notice

> **Update Date**: 2026-04-01
>
> All endpoints **no longer require** the `orgId` field:
>
> - `get_magiclink`: Does not require `orgId`
> - `query_apass`: No longer requires `orgId`
> - `query_deposit_address`: Does not require `orgId`
> - `query_chain_config`: Does not require `orgId`
> - `query_deposit_institutions`: Does not require `orgId`
> - `register_data`: Does not require `orgId`
> - `query_user`: Does not require `orgId`

---

## API Endpoints

### 1. get_magiclink

Retrieves the A-Pass registration URL (magic link).

**When to Use**: When the user asks how to register for A-Pass, needs a registration link, or signup link.

#### Endpoint

```
POST /api/skills/get_magiclink
```

#### Request

No request body, no parameters required.

#### Response

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Response code (0000 = success) |
| `message` | string | Response message |
| `data.register_url` | string | A-Pass registration URL |

#### Response Example

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "register_url": "https://..."
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "get_magiclink",
  "description": "Retrieve the A-Pass registration (magic link) URL. Use when user asks how to register for A-Pass or needs a signup link.",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

---

### 2. query_apass

Retrieves A-Pass basic information by blockchain address, including tier, expiration time, status, and KYC hash.

**When to Use**: When the user asks about A-Pass status, tier, expiration time, or verification.

#### Endpoint

```
POST /api/skills/query_apass
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain` | string | Yes | Blockchain name (e.g., solana, base) |
| `address` | string | Yes | Wallet address on the chain |
| `symbol` | string | No | Token symbol (optional) |

#### Request Example

```json
{
  "chain": "base",
  "address": "0x121C439ff356e806C3da108eE794c4Dd485984d3"
}
```

#### Response Data

| Field | Type | Description |
|-------|------|-------------|
| `cvRecordId` | string | CV record ID |
| `expirationTime` | long | Expiration timestamp (seconds) |
| `tier` | string | Tier level |
| `subTier` | integer | Sub tier |
| `group` | string | Group |
| `subGroup` | string | Sub group |
| `state` | integer | Status (1=active, 2=frozen) |
| `currentKycHash` | string | Current KYC data hash |

#### Response Example

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "cvRecordId": "2018305464961933312",
    "expirationTime": 1769046782,
    "tier": "4",
    "subTier": 1,
    "group": "AB",
    "subGroup": "AB",
    "state": 1,
    "currentKycHash": "3557683c1e62fb7dc8ef438e81cb4ffdf4c6077f..."
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "query_apass",
  "description": "Retrieve A-Pass basic information by blockchain address. Returns tier, expiration time, status, and KYC hash. Use when user asks to check A-Pass status, tier, or expiration for an address.",
  "parameters": {
    "type": "object",
    "properties": {
      "chain": { "type": "string", "description": "Blockchain (e.g., solana, base)" },
      "address": { "type": "string", "description": "Wallet address on the chain" },
      "symbol": { "type": "string", "description": "Token symbol (optional)" }
    },
    "required": ["chain", "address"]
  }
}
```

---

### 3. query_deposit_address

Retrieves USDC and USDT deposit wallet addresses by blockchain address. For Solana chain, returns both USDC and USDT deposit addresses.

**When to Use**: When the user asks for deposit addresses or USDC/USDT recharge addresses.

#### Endpoint

```
POST /api/skills/query_deposit_address
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain` | string | Yes | Blockchain name (e.g., solana, base) |
| `address` | string | Yes | Wallet address on the chain |
| `symbol` | string | No | Token symbol (optional; Solana returns both USDC and USDT) |

#### Request Example

```json
{
  "chain": "solana",
  "address": "9wF7Yp8MZk2J6qX4R5GQKxE3P7H8YyNQ1JZVfA6mB2c"
}
```

#### Response Data

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Wallet address |
| `chain` | string | Blockchain network |
| `txHash` | string | Transaction hash (nullable) |
| `aPassAddress` | string | A-Pass NFT address |
| `depositUSDCWallet` | string | USDC deposit wallet address |
| `depositUSDTWallet` | string | USDT deposit wallet address |

#### Response Example

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "address": "9wF7Yp8MZk2J6qX4R5GQKxE3P7H8YyNQ1JZVfA6mB2c",
    "chain": "solana",
    "txHash": null,
    "aPassAddress": "9fbL76x8kfX7g2LpxXYdYM1zQMvWbw7btpKTciDvrPSK",
    "depositUSDCWallet": "2q2d2L1eZEhgVFv2nLz8hWbPPWGP7aXGkjD8uZd7mDGV",
    "depositUSDTWallet": "GxZvXqgQ4CWBSAvZxLSe1k97P7RY2cDST2oCwVazbM11"
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "query_deposit_address",
  "description": "Retrieve deposit wallet addresses for USDC and USDT by blockchain address. Use when user asks for deposit address, where to send USDC/USDT, or similar.",
  "parameters": {
    "type": "object",
    "properties": {
      "chain": { "type": "string", "description": "Blockchain (e.g., solana, base)" },
      "address": { "type": "string", "description": "Wallet address on the chain" },
      "symbol": { "type": "string", "description": "Token symbol (optional)" }
    },
    "required": ["chain", "address"]
  }
}
```

---

### 4. query_chain_config

Returns supported chain configuration for all networks: chain id, display name, block explorer, EVM flag, RPC URL, operational addresses, A-Pass address, and token lists.

**When to Use**: When the user asks about supported chains, which networks, token lists, RPC URLs, explorer links, or chain configuration.

#### Endpoint

```
GET/POST /api/skills/query_chain_config
```

#### Request

No request body. No parameters required. Supports both GET and POST.

#### Response Data

| Field | Type | Description |
|-------|------|-------------|
| `data.chains` | array | Array of chain configuration objects |

#### Chain Object (`chains[]`)

| Field | Type | Description |
|-------|------|-------------|
| `chain` | string | Chain key |
| `chain_id` | integer | Numeric chain id (e.g., -1 for Solana) |
| `chain_name` | string | Display name |
| `explorer` | string | Block explorer base URL |
| `is_evm` | boolean | Whether chain is EVM |
| `rpc_url` | string | RPC endpoint |
| `operator_address` | string | Operator address |
| `fee_pay_address` | string | Fee payer address |
| `fee_receive_address` | string | Fee receiver address |
| `rent_payer_address` | string | Rent payer (Solana; may be empty) |
| `apass_address` | string | A-Pass program or NFT address |
| `wallet_core` | string | Wallet core address (may be empty) |
| `tokens` | array | Configured tokens for this chain |

#### Token Object (`tokens[]`)

| Field | Type | Description |
|-------|------|-------------|
| `chain` | string | Chain key |
| `symbol` | string | Origin symbol |
| `a_symbol` | string | A-Token symbol |
| `token_address` | string | Token mint/contract address |
| `name` | string | Display name |
| `decimals` | integer | Decimals |
| `icon` | string | Icon URL |
| `token_category` | string | Category (e.g., token) |
| `access_core` | string | Access core (may be empty) |
| `deposit_gateway` | string | Deposit gateway (may be empty) |

#### Response Example

```json
{
  "code": "0000",
  "message": "ok",
  "data": {
    "chains": [
      {
        "chain": "solana",
        "chain_id": -1,
        "chain_name": "Solana",
        "explorer": "https://solscan.io/?cluster=devnet",
        "is_evm": false,
        "rpc_url": "https://solana-devnet.g.alchemy.com/v2/_ztkT79iUO-dFpkTNDBFB",
        "operator_address": "FGthroQzf5DknSBucMURs32WBuGGDwXG3e41ngC1x5ci",
        "fee_pay_address": "356xTRu5phdyTeKAprYBus8BL5CDXmzP8QZYEMfQ1sPK",
        "fee_receive_address": "BqN271U5bJxy73ybJi7wY5H2LDLc99n9Ew3te4yQPgz8",
        "rent_payer_address": "",
        "apass_address": "APASSjT9ADM1vXG9jwzgJmGoff8HNVsreQm9pASgncdp",
        "wallet_core": "",
        "tokens": [
          {
            "chain": "solana",
            "symbol": "usdc",
            "a_symbol": "ausdc",
            "token_address": "Gh9ZwEmdLJ8DscKNTkTqPbNwLNNBjuSzaG9Vp2KGtKJr",
            "name": "USDC",
            "decimals": 6,
            "icon": "https://images.cleanverse.com/app/token_icon/USDC.svg",
            "token_category": "token",
            "access_core": "",
            "deposit_gateway": ""
          }
        ]
      }
    ]
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "query_chain_config",
  "description": "Get supported chain configuration for all networks: explorer, RPC, EVM flag, operational addresses, A-Pass address, and token lists. No parameters required.",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

---

### 5. query_deposit_institutions

Returns the list of institutions allowed for deposit (whitelist) grouped by origin token and A-Token pair.

**When to Use**: When the user asks about which institutions can deposit, deposit whitelist, supported custodians for USDT/USDC.

#### Endpoint

```
POST /api/skills/query_deposit_institutions
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain` | string | Yes | Blockchain name (e.g., solana, base) |
| `symbol` | string | Yes | Token symbol (e.g., usdt, usdc) |

#### Request Example

```json
{
  "chain": "solana",
  "symbol": "usdt"
}
```

#### Response Data

| Field | Type | Description |
|-------|------|-------------|
| `chain` | string | Chain key (may be empty) |
| `token_whitelist` | array | Entries per origin/A-Token pair |

#### Token Whitelist Object (`token_whitelist[]`)

| Field | Type | Description |
|-------|------|-------------|
| `origin_symbol` | string | Origin token symbol |
| `origin_token_address` | string | Origin token address |
| `atoken_symbol` | string | A-Token symbol |
| `atoken_address` | string | A-Token address |
| `whitelist` | array | Whitelisted institutions |

#### Institution Object (`whitelist[]`)

| Field | Type | Description |
|-------|------|-------------|
| `service_name` | string | Service display name |
| `entity_name` | string | Legal entity name |
| `category` | string | Business category |
| `icon` | string | Icon URL |

#### Response Example

```json
{
  "code": "0000",
  "message": "ok",
  "data": {
    "chain": "",
    "token_whitelist": [
      {
        "origin_symbol": "usdt",
        "origin_token_address": "0xdae5FbCEc935ac14195cd377bBC0672C72Af93d6",
        "atoken_symbol": "ausdt",
        "atoken_address": "0xB5f430eA34d743694A4BF12F8d5917d7668232B7",
        "whitelist": [
          {
            "service_name": "Anchorage Digital",
            "entity_name": "Anchorage Digital NY, LLC",
            "category": "Infrastructure",
            "icon": "https://images.cleanverse.com/member/ANCHORAGE DIGITAL SINGAPORE Pte. Ltd..png"
          }
        ]
      }
    ]
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "query_deposit_institutions",
  "description": "Get the list of institutions whitelisted for token deposit for the given chain and token symbol. Use when user asks which partners or custodians can deposit, or for deposit whitelist information.",
  "parameters": {
    "type": "object",
    "properties": {
      "chain": { "type": "string", "description": "Blockchain (e.g., solana, base)" },
      "symbol": { "type": "string", "description": "Token symbol (e.g., usdt, usdc)" }
    },
    "required": ["chain", "symbol"]
  }
}
```

---

### 6. register_data

Registers (writes) a user wallet address for the given chain and token. Returns the user address and associated deposit address.

**When to Use**: When the user wants to save, register, or bind their wallet for deposits, or submit a user address to obtain a Cleanverse deposit address.

#### Endpoint

```
POST /api/skills/register_data
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain` | string | Yes | Blockchain name (e.g., base) |
| `symbol` | string | Yes | Token symbol (e.g., usdc) |
| `address` | string | Yes | User wallet address |

#### Request Example

```json
{
  "chain": "base",
  "symbol": "usdc",
  "address": "0x543b96420d072BF587B63C41C0B0922762E986Ce"
}
```

#### Response Data

| Field | Type | Description |
|-------|------|-------------|
| `user_address` | string | Registered user wallet address |
| `deposit_address` | string | Mapped Cleanverse deposit address |
| `chain` | string | Blockchain |
| `symbol` | string | Token symbol (may be empty string) |

#### Response Example

```json
{
  "code": "0000",
  "message": "ok",
  "data": {
    "user_address": "0x543b96420d072BF587B63C41C0B0922762E986Ce",
    "deposit_address": "0xd771AeB7942DA6226fb6cd75f26393C648361E3d",
    "chain": "base",
    "symbol": ""
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "register_data",
  "description": "Register or write a user wallet address for a chain and token; returns user_address and deposit_address. Use when user wants to bind or save their address for deposits.",
  "parameters": {
    "type": "object",
    "properties": {
      "chain": { "type": "string", "description": "Blockchain (e.g., base)" },
      "symbol": { "type": "string", "description": "Token symbol (e.g., usdc)" },
      "address": { "type": "string", "description": "User wallet address" }
    },
    "required": ["chain", "symbol", "address"]
  }
}
```

---

### 7. query_user

Queries a registered user by chain, token symbol, and address. Returns deposit address, deposit status, account status, and blacklist reason when applicable.

**When to Use**: When the user asks to check their registration, deposit address status, if they are blacklisted, or to look up an existing user + token mapping.

#### Endpoint

```
POST /api/skills/query_user
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain` | string | Yes | Blockchain name (e.g., base) |
| `symbol` | string | Yes | Token symbol (e.g., usdc) |
| `address` | string | Yes | User wallet address |

#### Request Example

```json
{
  "chain": "base",
  "symbol": "usdc",
  "address": "0x543b96420d072BF587B63C41C0B0922762E986Ce"
}
```

#### Response Data

| Field | Type | Description |
|-------|------|-------------|
| `chain` | string | Blockchain |
| `symbol` | string | Token symbol (may be empty string) |
| `user_address` | string | User wallet address |
| `deposit_address` | string | Deposit address |
| `deposit_address_status` | string | Deposit address status (may be empty) |
| `status` | integer | User/account status (e.g., 0) |
| `blacklist_reason` | string | Blacklist reason if applicable (may be empty) |

#### Response Example

```json
{
  "code": "0000",
  "message": "ok",
  "data": {
    "chain": "base",
    "symbol": "",
    "user_address": "0x543b96420d072BF587B63C41C0B0922762E986Ce",
    "deposit_address": "0xd771AeB7942DA6226fb6cd75f26393C648361E3d",
    "deposit_address_status": "",
    "status": 0,
    "blacklist_reason": ""
  }
}
```

#### LLM Tool Schema

```json
{
  "name": "query_user",
  "description": "Query registered user info: deposit address, deposit status, account status, blacklist reason. Use after register_data or when user asks about their registration or deposit mapping.",
  "parameters": {
    "type": "object",
    "properties": {
      "chain": { "type": "string", "description": "Blockchain (e.g., base)" },
      "symbol": { "type": "string", "description": "Token symbol (e.g., usdc)" },
      "address": { "type": "string", "description": "User wallet address" }
    },
    "required": ["chain", "symbol", "address"]
  }
}
```

---

## Response Codes

| Code | Description |
|------|-------------|
| `0000` | Success |
| `0001` | Parameter error |
| `0002` | General failure |

---

## Appendix: Usage Examples

### Example 1: Get A-Pass Registration Link

```
User: How do I register for A-Pass?
Assistant: [Call get_magiclink]
Assistant: Please visit the following link to register: {register_url}
```

### Example 2: Query A-Pass Status

```
User: Check A-Pass status for this address: 0x121C439ff356e806C3da108eE794c4Dd485984d3 (Base chain)
Assistant: [Call query_apass, parameters: chain="base", address="0x121C439ff356e806C3da108eE794c4Dd485984d3"]
Assistant: A-Pass information for this address: Tier 4, status active, expiration time...
```

### Example 3: Query Deposit Address

```
User: What is the USDC deposit address for Solana address 9wF7Yp8MZk2J6qX4R5GQKxE3P7H8YyNQ1JZVfA6mB2c?
Assistant: [Call query_deposit_address, parameters: chain="solana", address="9wF7Yp8MZk2J6qX4R5GQKxE3P7H8YyNQ1JZVfA6mB2c"]
Assistant: Your USDC deposit address is: 2q2d2L1eZEhgVFv2nLz8hWbPPWGP7aXGkjD8uZd7mDGV
```

### Example 4: Query Chain Configuration

```
User: What chains and tokens are supported in Cleanverse?
Assistant: [Call query_chain_config]
Assistant: Cleanverse supports the following chains:
- Solana (non-EVM): USDC
- Base (EVM): USDC
- Ethereum (EVM): USDC, USDT
- Polygon (EVM): USDC, USDT
- Arbitrum (EVM): USDC, USDT
```

### Example 5: Query Deposit Institutions

```
User: Which institutions can I deposit USDT from on Base chain?
Assistant: [Call query_deposit_institutions, parameters: chain="base", symbol="usdt"]
Assistant: The following institutions support USDT deposits on Base:
- Anchorage Digital (Anchorage Digital NY, LLC)
```

### Example 6: Register User Address

```
User: I want to register my wallet for USDC deposits on Base
Assistant: [Call register_data, parameters: chain="base", symbol="usdc", address="0x543b..."]
Assistant: Your wallet has been registered. Your deposit address is: 0xd771...
```

### Example 7: Query User Registration Status

```
User: Check my registration status for USDC on Base
Assistant: [Call query_user, parameters: chain="base", symbol="usdc", address="0x543b..."]
Assistant: Your registration info:
- User Address: 0x543b...
- Deposit Address: 0xd771...
- Status: Active
```
