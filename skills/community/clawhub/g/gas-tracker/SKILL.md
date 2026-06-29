---
name: gas-tracker
description: Monitor current Ethereum gas prices (Slow/Standard/Fast/Instant tiers) with Gwei values and estimated confirmation times. Use when user asks about ETH gas prices, wants to check if network is congested, or set gas alerts for transactions. Fetches from public RPC and explorer APIs with automatic fallbacks.
---

# Gas Tracker

Monitor Ethereum gas prices in Gwei across Slow / Standard / Fast / Instant tiers.

## Quick Use

```
python scripts/gas_tracker.py
python scripts/gas_tracker.py --fast
python scripts/gas_tracker.py --alert 30
python scripts/gas_tracker.py --json
```

## Output

```
  ETH Gas Tracker  |  Source: publicnode.com  |  Block #21345678
  Updated: 2026-06-23T07:10:00Z

  Tier      Gwei      ETA
  ------    ------    -------
  Slow      12.0 Gwei    ~15 min
  Standard  15.0 Gwei    ~5 min
  Fast      20.0 Gwei    ~2 min
  Instant   25.0 Gwei    ~30 sec

  Base Fee: 10.0 Gwei
  Status: LOW — Good time to transact
```

## Flags

| Flag | Description |
|------|-------------|
| `--slow` | Show slow tier only |
| `--standard` | Show standard tier only |
| `--fast` | Show fast tier only |
| `--instant` | Show instant tier only |
| `--alert GWEI` | Exit 0 if standard gas < GWEI, exit 1 if above |
| `--json` | Raw JSON output |

## Data Sources

Tries in order: `ethereum.publicnode.com` RPC → `api.blockscout.com` → `ethgas.info` → `api.ethgas.watch`. Uses the first available.

## Alert Script Example

Useful for cron jobs:
```
python scripts/gas_tracker.py --alert 30 && echo "Gas is low, good to swap!" || echo "Gas too high"
```
