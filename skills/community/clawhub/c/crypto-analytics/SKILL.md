---
name: crypto-analytics
slug: crypto-analytics
version: 1.0.3
homepage: https://clawhub.com/skills/crypto-analytics
repository: https://github.com/yourusername/crypto-analytics
description: "Multi-chain blockchain analytics for wallet balances, transaction history, and address validation. Supports 60+ EVM chains via Etherscan V2, plus Bitcoin and Solana. Use to check wallet balances, view transactions, get transaction details, validate addresses, or list supported chains."
changelog: "v1.0.3: Fixed privacy section to accurately describe local caching (may store queried addresses). Improved .env loading to only use workspace root (AGENTS.md/.git detection). v1.0.2: Published version before false-positive appeal. v1.0.1: Added missing 'tokens' command handler. Fixed CHAINS typo in get_wallet_tokens."
---

# Crypto Analytics

## Overview

A comprehensive multi-chain blockchain analysis tool using live API data:

- **EVM networks:** 60+ chains via unified Etherscan V2 (Ethereum, Sepolia testnet, BSC, Polygon, Arbitrum, Base, Optimism, Avalanche, etc.)
- **Bitcoin:** Via Blockchair API
- **Solana:** Balance via public RPC (tx history requires external service)
- Built-in rate limiting and 5-minute caching
- No credentials needed for basic usage (API key increases Etherscan limits)

**All commands return JSON with optional human-readable formatting.**

---

## Privacy & Data Handling

This skill respects your privacy and operates transparently:

- **External data collection:** None. Only standard blockchain APIs receive your queries:
  - `api.etherscan.io` (Etherscan V2)
  - `blockchair.com` (Blockchair)
  - Public Solana RPC endpoints
- **Local caching:** API responses are cached for 5 minutes to respect rate limits. Cache files are stored in `~/.openclaw/cache/crypto-analytics/api_responses/` and may contain queried addresses, transaction hashes, and other public blockchain data you requested. Files are automatically expired and can be manually deleted. This data never leaves your machine.
- **Environment variables:** Optionally reads `ETHERSCAN_API_KEY` from a `.env` file located in the OpenClaw workspace root. No other environment variables are accessed.
- **No subprocesses or dynamic code execution:** Pure Python with `requests` library only.

You can audit the source code in `scripts/crypto_api.py` – it's straightforward HTTP + JSON.

---

## Configuration (Optional)

Set `ETHERSCAN_API_KEY` to increase rate limits (free tier: 5 calls/sec). Get a key from https://etherscan.io/apis

```bash
export ETHERSCAN_API_KEY=your_key_here
# Or add to ~/.openclaw/workspace/.env
```

## Core Commands

### `balance <address> [chain]`
Get native token balance for a wallet.

**Parameters:**
- `address` - Blockchain address
- `chain` (optional) - Chain identifier. Auto-detects from address format if omitted.
  - EVM: `ethereum`, `sepolia`, `bsc`, `polygon`, `arbitrum`, `base`, `optimism`, `avalanche`, and more
  - Non-EVM: `bitcoin`, `solana`

**Example:**
```bash
crypto-analytics balance 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45 ethereum
```

**Output:**
```json
{
  "chain": "ethereum",
  "chainid": 1,
  "address": "0x742d35cc6634c0532925a3b8d4c9db96c4b4db45",
  "balance_wei": 1234567890000000000,
  "balance_native": 1.23456789,
  "formatted_balance": "1.234568 ETH"
}
```

### `transactions <address> [chain] [limit=20]`
Get recent transaction history.

**Parameters:**
- `address` - Wallet address
- `chain` (optional) - Chain identifier (auto-detected if omitted)
- `limit` (optional) - Maximum transactions to return (default 20, max 100)

**Example:**
```bash
crypto-analytics transactions 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45 bsc 50
```

**Output:**
```json
{
  "chain": "bsc",
  "chainid": 56,
  "address": "...",
  "count": 150,
  "transactions": [ /* array of tx objects */ ]
}
```

### `tx <txhash> <chain>`
Get full transaction details.

**Parameters:**
- `txhash` - Transaction hash
- `chain` - Chain identifier (required)

**Example:**
```bash
crypto-analytics tx 0x123abc... ethereum
```

**Output:**
```json
{
  "chain": "ethereum",
  "chainid": 1,
  "txhash": "0x123abc...",
  "transaction": { /* full tx object */ }
}
```

### `validate <address>`
Check address validity and detect chain.

**Parameters:**
- `address` - Address to validate

**Example:**
```bash
crypto-analytics validate bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
```

**Output:**
```json
{
  "valid": true,
  "chain": "bitcoin",
  "normalized": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "error": null
}
```

### `chains`
List all supported blockchains with their specs.

**Example:**
```bash
crypto-analytics chains
```

### `gas [chain=ethereum]`
Get current gas price estimates including Safe, Standard, and Fast rates, plus base fee (EIP-1559).

**Parameters:**
- `chain` (optional) - Chain identifier (default: ethereum)

**Example:**
```bash
crypto-analytics gas ethereum
```

**Output:**
```json
{
  "chain": "ethereum",
  "chainid": 1,
  "low": 20000000000,
  "standard": 50000000000,
  "fast": 80000000000,
  "base_fee": 15000000000,
  "timestamp": 1700000000,
  "formatted": "=== Gas Price Tracker ===\nSafe: 20.00 Gwei\nStandard: 50.00 Gwei\nFast: 80.00 Gwei\nBase Fee: 15.00 Gwei\nUpdated: 2023-11-14 10:00:00 UTC"
}
```

### `token <address> <token_contract> [chain]`
Get ERC-20 token balance for a specific token contract, with symbol and formatted human-readable value.

**Parameters:**
- `address` - Wallet address
- `token_contract` - ERC-20 token contract address
- `chain` (optional) - Chain identifier (auto-detected if omitted)

**Example:**
```bash
crypto-analytics token 0xYourAddress 0xA0b86991c6218b36c1d19D4a2e9bB0e3606EB48 ethereum
```

**Output:**
```json
{
  "chain": "ethereum",
  "contract": "0xa0b86991c6218b36c1d19d4a2e9bb0e3606eb48",
  "owner": "0xYourAddress",
  "balance": 1000000,
  "symbol": "USDC",
  "name": "USD Coin",
  "decimals": 6,
  "formatted": "=== Token Balances ===\nUSDC (USD Coin)\n  Balance: 1.000000\n  Contract: 0xa0b86991c6218b36c1d19d4a2e9bb0e3606eb48\n"
}
```

### `tokens <address> [chain] [limit=20]`
Get all ERC-20 token balances for a wallet by auto-discovering tokens from recent transfer history. Returns non-zero balances with symbols and decimals.

**Parameters:**
- `address` - Wallet address
- `chain` (optional) - Chain identifier (auto-detected if omitted)
- `limit` (optional) - Maximum number of tokens to check (default 20)

**Example:**
```bash
crypto-analytics tokens 0xYourAddress ethereum 10
```

**Output:**
```json
{
  "chain": "ethereum",
  "address": "0xYourAddress",
  "count": 2,
  "tokens": [
    {
      "contract": "0xa0b86991c6218b36c1d19d4a2e9bb0e3606eb48",
      "balance": 1000000,
      "symbol": "USDC",
      "name": "USD Coin",
      "decimals": 6
    },
    {
      "contract": "0xdac17f958d2ee523a2206206994597c13d831ec7",
      "balance": 500000,
      "symbol": "USDT",
      "name": "Tether USD",
      "decimals": 6
    }
  ],
  "formatted": "=== Token Balances ===\nUSDC (USD Coin)\n  Balance: 1.000000\n  Contract: 0xa0b8...\nUSDT (Tether USD)\n  Balance: 0.500000\n  Contract: 0xdac1..."
}
```

### `spl-tokens <owner>`
Get SPL token accounts for a Solana wallet. Returns mint addresses and token amounts (human-readable).

**Parameters:**
- `owner` - Solana wallet address (Base58)

**Example:**
```bash
crypto-analytics spl-tokens 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

**Output:**
```json
{
  "owner": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
  "tokens": [
    {
      "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "amount": 10.5,
      "decimals": 9
    }
  ],
  "formatted": "Owner: 7xKX...\\nToken count: 1\\n  EPjF...: 10.50000000\\n"
}
```

## When to Use This Skill

Use `crypto-analytics` when you need to:

- Check wallet balances across multiple blockchains
- Investigate wallet activity and transaction patterns
- Look up specific transaction details
- Validate blockchain addresses
- Determine which chains are supported
- Integrate live blockchain data into OpenClaw automations

## Example Scenarios

> "Check my ETH balance"  
> `balance 0x... ethereum` or auto-detect if address starts with 0x

> "How much BNB do I have on BSC?"  
> `balance 0x... bsc`

> "Show me recent transactions for this Bitcoin address"  
> `transactions 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa bitcoin`

> "Is this a valid address and what chain is it on?"  
> `validate <address>`

> "What chains do you support?"  
> `chains`

> "Get details for tx 0xabc... on Arbitrum"  
> `tx 0xabc... arbitrum`

> "Check my USDC balance on Ethereum"  
> `token 0x... 0xA0b86991c6218b36c1d19D4a2e9bB0e3606EB48 ethereum`

> "Show all tokens I have on Ethereum"  
> `tokens 0x... ethereum`

> "What's the current gas price on Arbitrum?"  
> `gas arbitrum`

## Implementation Notes

### API Providers

- **Etherscan V2:** Unified endpoint for 60+ EVM chains. Free tier: ~5 calls/sec, 5k-100k/day depending on chain. API key significantly increases limits.
- **Blockchair:** Bitcoin, Litecoin, Dogecoin, etc. Free: 100 req/min, 4k/day.
- **Solana RPC:** Public endpoints (rate-limited) for balances only.

### Caching & Rate Limiting

- **TTL:** 300 seconds (5 minutes)
- **Cache location:** `~/.openclaw/cache/crypto-analytics/api_responses/`
- **Rate delays:** Enforced to stay within free tier limits
- **Batching:** Multiple queries in same session use cache

### Configuration

Set API keys in `.env`:

```bash
ETHERSCAN_API_KEY=YourEtherscanKeyHere
```

Key optional for low-volume usage but recommended.

See `references/api_index.md` for full API documentation and `references/chains.md` for chain specifications.

## Limitations & Future

**Current limitations:**
- Solana transaction history requires specialized indexer (Solscan API)
- Solana token metadata (symbol, name) not available; only mint addresses are shown
- No batch multi-address queries
- Free tier rate limits apply

**Planned enhancements:**
- Transaction tracing and money flow analysis
- Contract ABI decoding for read calls
- Additional chain-specific features
- Enhanced Solana token metadata (via token list)

## Resources

This skill bundles useful reference material:

- `references/chains.md` - Chain specifications, address formats, explorers
- `references/api_index.md` - API endpoints, parameters, examples

These files are loaded into context only when needed.
