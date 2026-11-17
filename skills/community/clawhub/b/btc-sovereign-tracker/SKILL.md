---
name: btc-sovereign-tracker
description: Track BTC self-custody metrics — COLDCARD Q vault health, mempool fee estimation, UTXO management, and on-chain verification. Designed for sovereign holders who verify, don't trust.
homepage: https://gitlab.com/1Beekeeper/zk-bankir
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq"]
    os: ["linux", "darwin"]
---

# BTC Sovereign Tracker

Track and verify your Bitcoin self-custody setup. This skill monitors COLDCARD Q vault health, fetches real-time mempool fees, inspects UTXOs, and verifies on-chain balances — all read-only. Never exposes private keys. Trust, but verify (Gebud 3).

## Prerequisites

- `curl` and `jq` on PATH
- Bitcoin address(es) to monitor (watch-only, no private keys)
- Optional: local Bitcoin Core or Electrum server for full privacy

## Core Commands

### Mempool Fee Estimation

Get current fee rates from mempool.space:

```bash
curl -s https://mempool.space/api/v1/fees/recommended | jq .
```

Response: `{"fastestFee": N, "halfHourFee": N, "hourFee": N, "economyFee": N, "minimumFee": N}`

Fees are in sat/vB. Multiply by tx size (~140 vB for segwit) to get total fee in sats.

### Address Balance & UTXOs

Check balance and UTXOs for a watch-only address:

```bash
ADDR="bc1q..."  # watch-only address
curl -s "https://mempool.space/api/address/$ADDR" | jq '{balance: .chain_stats.funded_txo_sum - .chain_stats.spent_txo_sum, tx_count: .chain_stats.tx_count}'
curl -s "https://membpool.space/api/address/$ADDR/utxo" | jq '.[] | {txid: .txid, vout: .vout, value: .value}'
```

**Privacy note:** mempool.space is a third party. For maximum sovereignty, run your own mempool instance or use a local Bitcoin Core node with `bitcoin-cli`.

### Block Height & Network Health

```bash
curl -s https://mempool.space/api/blocks/tip/height
```

Compare against your local node to verify chain sync.

### Price Oracle (CoinGecko)

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,eur,sek" | jq .
```

### COLDCARD Vault Health (via ZK-Bankir)

Query the ZK-Bankir treasury endpoint for BTC vault status:

```bash
ZK_HOST="${ZK_BANKIR_HOST:-http://localhost:3000}"
curl -s "$ZK_HOST/api/v1/treasury/btc" -H "Accept: application/json" | jq .
```

Expected:
```json
{
  "asset": "BTC",
  "balance": "1.5",
  "address": "bc1q...",
  "vault": "COLDCARD Q",
  "type": "watch-only"
}
```

### UTXO Consolidation Planning

List all UTXOs and identify dust or consolidation candidates:

```bash
ADDR="bc1q..."
curl -s "https://mempool.space/api/address/$ADDR/utxo" | jq '
  [.[] | {
    txid: .txid[0:8],
    vout: .vout,
    value_sats: .value,
    value_btc: (.value / 100000000),
    dust: (.value < 10000)
  }] | sort_by(.value_sats)
'
```

UTXOs below 10,000 sats (~$10) are dust and may cost more to spend than they're worth during high-fee periods.

## Usage Patterns

### Daily Sovereignty Check

When the user asks for a BTC sovereignty status:

1. **Mempool fees** — current fee environment (low/medium/high)
2. **Address balance** — confirmed balance vs expected
3. **Block height** — chain tip verification
4. **BTC price** — current fiat value
5. **Vault health** — COLDCARD status from ZK-Bankir

### Pre-Transaction Fee Planning

When the user considers a transaction:

1. Fetch current recommended fees
2. Calculate fee ranges: economy (~0.5h), hour (~2h), half-hour (~30min), fastest (~next block)
3. Show fee in sats and fiat equivalent
4. Flag if any UTXOs would become dust after spending

### UTXO Management Audit

When the user asks about UTXO health:

1. List all UTXOs sorted by value
2. Flag dust UTXOs (value < fee to spend)
3. Recommend consolidation targets (fewer UTXOs = lower future fees)
4. Warn if address reuse detected

## Sovereignty Principles

This skill follows ZK-Bankir's Gebuden:

- **§1 Sovereignty First** — prefers local node over third-party APIs when available
- **§3 Trust, but Verify** — cross-checks mempool.space with CoinGecko and ZK-Bankir
- **§5 Watch-Only by Default** — never requires, stores, or transmits private keys
- **§7 Privacy Per Design** — warns when using third-party APIs, recommends local alternatives

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `BTC_WATCH_ADDRESS` | (required) | Bitcoin address to monitor (watch-only) |
| `MEMPOOL_API` | `https://mempool.space/api` | Mempool API base (change for self-hosted) |
| `COINGECKO_API` | `https://api.coingecko.com/api/v3` | Price API base |
| `ZK_BANKIR_HOST` | `http://localhost:3000` | ZK-Bankir server for vault status |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Empty UTXO list | Address has no transactions | Verify address on a block explorer |
| Rate limit on mempool.space | Too many requests | Use local mempool instance or add delays |
| ZK-Bankir BTC endpoint 404 | Server not running | Start ZK-Bankir or use direct mempool queries |
| Dust warnings on all UTXOs | High fee environment | Wait for lower fees before consolidating |

## Security

- **Read-only** — queries on-chain data, never signs transactions
- **No key exposure** — all addresses are watch-only public keys
- **Third-party aware** — clearly labels when using external APIs vs local node
- **COLDCARD Q remains air-gapped** — this skill queries balances through ZK-Bankir's watch-only API
