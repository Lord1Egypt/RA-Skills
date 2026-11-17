---
name: bitcoin
description: Query Bitcoin (BTC L1) blockchain data with USD pricing — wallet balances, address info, transaction details, UTXO analysis, fee estimation, mempool stats, and live network health. Uses Mempool.space REST API (https://mempool.space/docs/api/rest). No API key required.
version: 1.0.0
author: bronoman
credits: mempool.space API
license: MIT
metadata:
  hermes:
    tags: [Bitcoin, BTC, L1, Blockchain, UTXO, Mempool, Crypto, On-Chain]
    related_skills: [base]
---

# Bitcoin L1 Blockchain Skill

Query Bitcoin on-chain data enriched with USD pricing via CoinGecko.
7 commands: address info, transaction details, fee estimation, mempool analysis, UTXO scanning, network stats, and price lookup.

No API key needed. Uses only Python standard library (urllib, json, argparse).

---

## When to Use

- User asks for a Bitcoin address balance, UTXO count, or holdings
- User wants to inspect a specific Bitcoin transaction by TXID
- User wants to understand Bitcoin network fees (per vB, estimates by block target)
- User wants mempool statistics (pending tx count, fee distribution, transaction pool size)
- User wants to know the latest block height, block time, or network status
- User wants to check current BTC price in USD or other fiat
- User wants to find unconfirmed transactions or check tx confirmation status

---

## Prerequisites

The helper script uses only Python standard library (urllib, json, argparse).
No external packages required.

Pricing data comes from Mempool.space's free API (no key needed, rate-limited
to ~30-50 requests/minute). Fee estimates update every 10 minutes.

---

## Quick Reference

REST endpoint (default): https://mempool.space/api
Override: export BITCOIN_API_URL=https://your-mempool-instance/api

Helper script path: ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py

```
python3 bitcoin_client.py address     <address> [--limit N]
python3 bitcoin_client.py tx          <txid>
python3 bitcoin_client.py fees
python3 bitcoin_client.py mempool
python3 bitcoin_client.py blocks      [--limit N]
python3 bitcoin_client.py stats
python3 bitcoin_client.py price       [--currency USD|EUR|GBP|JPY]
```

---

## Procedure

### 0. Setup Check

```bash
python3 --version

# Optional: set a custom Mempool instance
export BITCOIN_API_URL="https://mempool.space/api"

# Confirm connectivity
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py stats
```

### 1. Address Info

Get Bitcoin address data: UTXO set, total received/sent, confirmed balance,
pending balance, and transaction count.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py \
  address 1A1z7agoat3bLsCywJ6H7qqyiB8t6SE2Kt
```

Flags:
- `--limit N` — show top N UTXOs by value (default: 20)

Output includes: 
- Address type (P2PKH, P2SH, P2WPKH, P2WSH, etc.)
- Confirmed balance in BTC and USD
- Pending balance (unconfirmed)
- Total received / total spent
- UTXO count (spent + unspent)
- Top UTXOs with amounts and confirmation status

### 2. Transaction Details

Inspect a full Bitcoin transaction by TXID. Shows input/output details,
fee in BTC/sat/vB and USD, confirmation status, block height.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py \
  tx 1e4e745d32e6cfbb7ee778cdec5d9e5be1b5ea3c5f9c8d3e1b5a3f9e6d7c4b1a
```

Output:
- TXID, block height, confirmation status
- Input count / output count
- Total input value (BTC + USD)
- Total output value (BTC + USD)
- Fee in satoshis, vB, BTC, and USD
- Input addresses and amounts
- Output addresses and amounts
- Transaction size (bytes) and vB (virtual bytes)
- Confirmations count

### 3. Fee Estimation

Current Bitcoin network fee rates with confirmation time estimates.
Shows fees for 1, 2, 3, 6, 24-block confirmation targets.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py fees
```

Output:
- Fee rates in sat/vB for different confirmation times
- Estimated time to confirmation (minutes)
- Current recommended fee (for medium priority ~10 blocks)
- Fee distribution: percentage of mempool at each level
- Current BTC/USD price for reference

### 4. Mempool Statistics

Live Bitcoin mempool analysis: transaction count, pool size, fee distribution,
and backlog estimation.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py mempool
```

Output:
- Pending transaction count
- Total mempool size (bytes and MB)
- Minimum fee (lowest rate accepted)
- Maximum fee (highest rate in pool)
- Median fee
- Average fee
- Fee count by level (high/medium/low)
- Estimated backlog time (hours to clear at current rates)
- Last updated timestamp

### 5. Recent Blocks

List recent Bitcoin blocks with confirmation status and transaction counts.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py blocks
```

Flags:
- `--limit N` — show last N blocks (default: 10)

Output includes:
- Block height, block hash (first 8 + last 8 chars)
- Time (relative: "2 hours ago")
- Transaction count in block
- Block size (bytes)
- Median fee in the block (sat/vB)

### 6. Network Stats

Live Bitcoin network health: latest block height, network time, fee environment,
BTC price, and chain status.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py stats
```

Output:
- Latest block height and hash
- Blocks mined in last hour / day / week
- Current time (network synchronized)
- Mempool size (MB, tx count)
- Fee summary: low/med/high recommendations
- BTC/USD price (from Mempool or CoinGecko)
- Network difficulty (approximate)

### 7. Price Lookup

Quick BTC price check in multiple currencies.

```bash
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py price
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py price --currency EUR
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py price --currency JPY
```

Supported currencies: USD, EUR, GBP, JPY, CHF, CAD, AUD, SGD, INR, HKD

---

## Pitfalls

- **Mempool.space rate-limits** — Free tier allows ~30-50 requests/minute. For
  production use, set BITCOIN_API_URL to a self-hosted Mempool instance or use
  a commercial API provider.

- **Fee estimates are probabilistic** — Mempool.space estimates based on current
  pool state. Actual confirmation times vary with network congestion.

- **Address indexing lag** — Some full nodes may have slight lag in indexing
  recent UTXOs. Results should be consistent within seconds.

- **Transaction unconfirmed** — If a transaction is very recent, it may show
  as pending or unconfirmed. Wait a few blocks for confirmation.

- **UTXO privacy** — All Bitcoin transactions are public. Address balances are
  queryable by any observer.

- **Price lag** — BTC price updates every few seconds. Prices shown are
  point-in-time snapshots.

- **Dust filtering not applied** — Wallet shows all UTXOs including small
  amounts. Filter manually if needed (see --limit flag).

- **Address format detection** — Script attempts to detect P2PKH, P2SH, P2WPKH,
  P2WSH from address prefix. Custom formats may not be recognized.

---

## Verification

```bash
# Should print Bitcoin chain stats, latest block height, network fee, and BTC price
python3 ~/.hermes/skills/blockchain/bitcoin/scripts/bitcoin_client.py stats
```
