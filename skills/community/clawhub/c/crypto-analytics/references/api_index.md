# API Reference Index

## Etherscan V2 API (Unified)

**Base URL:** `https://api.etherscan.io/v2`

**Authentication:** `apikey` query parameter (get free key from etherscan.io/apis)

**Architecture:**
- Single endpoint for 60+ Ethereum-compatible chains
- Use `chainid` parameter to specify network (e.g., `1` for Ethereum, `56` for BSC)
- Same module/action structure as V1

### Common Parameters

| Parameter | Description |
|-----------|-------------|
| `chainid` | Integer chain ID (see chains.md) |
| `module` | API module category (account, proxy, blocks, etc.) |
| `action` | Specific operation within module |
| `apikey` | Your API key |

### Account Module

**Get Balance:**
```
GET /v2?chainid={chainid}&module=account&action=balance&address={address}
Response: { "balance": "wei_amount" }
```

**Get Transactions:**
```
GET /v2?chainid={chainid}&module=account&action=txlist
    &address={address}&startblock=0&endblock=99999999&sort=desc
Response: Array of transaction objects
```

**Get ERC-20 Transfers:**
```
GET /v2?chainid={chainid}&module=account&action=tokentx
    &address={address}&sort=desc
Response: Array of token transfer events
```

### Proxy Module (JSON-RPC)

**Get Transaction by Hash:**
```
GET /v2?chainid={chainid}&module=proxy&action=eth_getTransactionByHash
    &txhash={hash}
Response: Transaction object
```

**Get Block by Number:**
```
GET /v2?chainid={chainid}&module=proxy&action=eth_getBlockByNumber
    &tag=latest&boolean=false
Response: Block object
```

**Get Gas Price:**
```
GET /v2?chainid={chainid}&module=proxy&action=eth_gasPrice
Response: { "result": "wei_per_gas" }
```

**Call (Contract read):**
```
GET /v2?chainid={chainid}&module=proxy&action=eth_call
    &to={contract}&data={calldata}&tag=latest
Response: { "result": "0x..." }
```

### Rate Limits

V2 uses unified quotas:
- **Free:** ~5 calls/sec, daily quota varies by chain (typically 5-100k/day)
- **With API key:** Higher quotas (check your dashboard)

### Migration from V1

V1 used different endpoints per chain (e.g., `api-opt/mainnet`). V2 simplifies:

**Old:**
```
https://api-optimistic.etherscan.io/api?module=account&action=balance&address=...
```

**New:**
```
https://api.etherscan.io/v2?chainid=10&module=account&action=balance&address=...
```

## Blockchair API

**Base URL:** `https://api.blockchair.com`

**Endpoints:**

### `{chain}/address`
- **GET** address overview
- Params: `address`
- Returns: `balance`, `transaction_count`, `received`, `spent`

### `{chain}/transactions`
- **GET** transactions for address
- Params: `address`, `limit` (default 25), `sort` (e.g., `desc(block_time)`)
- Returns: paginated list

### `{chain}/raw/transaction`
- **GET** transaction details
- Params: `hash`
- Returns: full transaction with inputs/outputs/scripts

**Supported chains:** bitcoin, bitcoincash, litecoin, dogecoin, dash, groestlcoin

**Rate limits:** 100 req/min, 4,000/day (free). Paid plans available.

## Solana JSON-RPC

**Public endpoints:**
- `https://api.mainnet-beta.solana.com`
- `https://solana-api.project-serum.com`

### Methods

| Method | Description |
|--------|-------------|
| `getAccountInfo` | Account data including lamports balance |
| `getTokenAccountsByOwner` | SPL token accounts for a wallet |
| `getBalance` | Simplified balance (use accountInfo for lamports) |
| `getTransaction` | Transaction details (limited) |

**Note:** For production transaction history, use Solscan API or Helius.

## Environment Configuration

### .env File

Create `.env` in workspace root:

```bash
ETHERSCAN_API_KEY=YourEtherscanV2Key
BLOCKCHAIR_API_KEY=OptionalBlockchairKey
```

### Key Features

- **Automatic loading:** `crypto_api.py` loads `.env` via `python-dotenv` (if installed) or `os.getenv`
- **Caching:** All responses cached (TTL: 5 min default) to respect rate limits
- **Error handling:** Graceful degradation when APIs fail or rate limit

## Testing Directly

```bash
# Check connection
python3 scripts/crypto_api.py balance 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45 ethereum

# Get transactions
python3 scripts/crypto_api.py txs 0x... ethereum 20

# Get tx details
python3 scripts/crypto_api.py tx 0x... ethereum

# Validate address
python3 scripts/crypto_analytics.py validate 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45
```

## Troubleshooting

**"Invalid API Key"** → Check `.env` file and regenerate key at etherscan.io

**"Rate limit exceeded"** → Reduce polling frequency; cache helps; consider paid key

**Chain not found** → Verify `chainid` is correct; see chains.md

**Empty results** → Address may be new, contract, or on wrong chain

**Timeout** → Public RPCs may be slow; retry or use paid endpoints
