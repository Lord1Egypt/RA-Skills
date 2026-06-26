# Supported Blockchain Networks

## EVM Chains (via Etherscan V2)

The following chains are supported through the unified Etherscan V2 API using `chainid`:

| Chain | Chain ID | Native Token | Explorer |
|-------|----------|--------------|----------|
| Ethereum Mainnet | 1 | ETH | etherscan.io |
| Sepolia Testnet | 11155111 | ETH (test) | sepolia.etherscan.io |
| BNB Smart Chain (BSC) | 56 | BNB | bscscan.com |
| Polygon | 137 | MATIC | polygonscan.com |
| Arbitrum One | 42161 | ETH | arbitrum.etherscan.io |
| Base | 8453 | ETH | basescan.org |
| Optimism | 10 | ETH | optimism.etherscan.io |
| Avalanche C-Chain | 43114 | AVAX | snowtrace.io |
| Gnosis Chain | 100 | xDAI | gnosisscan.io |
| Fantom | 250 | FTM | ftmscan.com |
| Linea | 59144 | ETH | linea.etherscan.io |
| Scroll | 534352 | ETH | scrollscan.xyz |
| zkSync Era | 324 | ETH | zkscan.io |
| Mantle | 5000 | MNT | mantlescan.xyz |
| Cronos | 25 | CRO | cronoscan.com |
| KCC | 321 | KCS | kcc.etherscan.io |
| Metis | 1088 | METIS | explorer.metis.io |
| Harmony | 1666600000 | ONE | explorer.harmony.one |
| IoTeX | 4689 | IOTX | iotexscan.io |
| OKC | 66 | OKT | oklink.com |
| And 40+ more... | | | |

Full list: https://docs.etherscan.io/v2-migration

## Non-EVM Chains

| Chain | Type | Native Token | Explorer | Status |
|-------|------|--------------|----------|--------|
| Bitcoin | UTXO | BTC | blockchair.com/bitcoin | ✅ Active |
| Solana | Account-based | SOL | solscan.io | ⚠️ Partial (balance only) |
| Litecoin | UTXO | LTC | blockchair.com/litecoin | ✅ Blockchair |
| Dogecoin | UTXO | DOGE | blockchair.com/dogecoin | ✅ Blockchair |
| Dash | UTXO | DASH | blockchair.com/dash | ✅ Blockchair |

**Limitations:**
- Solana transaction history requires specialized indexing API
- Non-EVM chains use Blockchair API (rate limited) or specialized RPCs

## Address Format Reference

### EVM Addresses
```
Format: 0x + 40 hex characters (case insensitive)
Example: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45
Normalized: 0x742d35cc6634c0532925a3b8d4c9db96c4b4db45 (lowercase)
```

### Bitcoin
- **Legacy (P2PKH):** `1...` (34 characters)
- **Nested SegWit (P2SH):** `3...` (34 characters)
- **Native SegWit (Bech32):** `bc1...` (39-59 characters)

### Solana
- **Format:** Base58 encoded public key
- **Length:** 32-44 characters (no prefix)
- **Example:** `7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU`

## Rate Limits

| Service | Free Tier | Paid Tiers |
|---------|-----------|------------|
| Etherscan V2 | 5 calls/sec, depends on daily quota | Higher with API key |
| Blockchair | 100 req/min, 4k/day | 100k-1M/day plans |
| Solana RPC | Varies by endpoint (conservative: 2/sec) | Premium RPC providers |

All API calls are cached for 5 minutes by default.

## Getting API Keys

**Etherscan V2:**
- Visit: https://etherscan.io/apis
- Create account → Get API key (free)
- Set in `.env`: `ETHERSCAN_API_KEY=your_key_here`

**Blockchair:**
- https://blockchair.com/api
- Free tier works without key (limited)
- Paid keys increase limits

## Automatic Chain Detection

The `validate` command automatically detects chain from address format:

1. `0x...` → One of the EVM chains (defaults to Ethereum if unspecified)
2. `1...`, `3...`, `bc1...` → Bitcoin
3. Base58 (no `0x`) → Solana

When querying a specific chain, pass the chain identifier (e.g., `bsc`, `polygon`, `arbitrum`) to use the correct `chainid`.

## Example Usage

```bash
# Get ETH balance on Ethereum
crypto-analytics balance 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45 ethereum

# Get BNB balance on BSC
crypto-analytics balance 0x... bsc

# Get Bitcoin balance
crypto-analytics balance 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa bitcoin

# Validate address
crypto-analytics validate 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45

# List all supported chains
crypto-analytics chains
```
