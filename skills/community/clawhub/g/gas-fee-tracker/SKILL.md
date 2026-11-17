---
name: gas-fee-tracker
description: Track live EVM gas fees across Ethereum, Base, Polygon, and Arbitrum using free public RPC endpoints with no API key required. Classifies current gas as low, medium, or high against configurable thresholds, logs snapshots to a JSONL history file over time, and supports threshold alerts for scripting into automations. Useful for crypto trading, defi, smart contract deployment, and passive income bots that need to time on-chain transactions to avoid overpaying for gas. Complements whale-tracking and defi yield-farming workflows by timing execution around cheap gas windows.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Gas Fee Tracker

Live gas price snapshots across four EVM chains, using only free public RPC
endpoints — no API key, no rate-limit signup required.

## When to use this skill

- Timing a contract deployment or large transaction batch for a cheap gas
  window
- Building an automation that only executes a transaction when gas drops
  below a threshold
- Logging gas price history over time to spot patterns (e.g. daily/weekly
  cycles) before scheduling recurring on-chain jobs

## How to use it

Snapshot all chains:
```
python3 scripts/gas_tracker.py
```

Single chain, JSON output for scripting:
```
python3 scripts/gas_tracker.py --chain ethereum --json
```

Append to a running history log:
```
python3 scripts/gas_tracker.py --log gas_history.jsonl
```

Use as a gate in an automation (exits 0 only if gas is at/below threshold):
```
python3 scripts/gas_tracker.py --chain base --alert-below 0.1 && echo "cheap gas, proceed"
```

## Supported chains

Ethereum mainnet, Base, Polygon, Arbitrum One — each with its own
low/high gwei thresholds tuned to that chain's typical range.

## Limitations

- Reports the current `eth_gasPrice` legacy gas price, not EIP-1559
  base-fee/priority-fee breakdown or a predictive estimate of future blocks
- Public RPC endpoints can occasionally rate-limit or time out; the script
  reports per-chain errors rather than failing the whole run
