# Gas Fee Tracker

A zero-signup Python tool that fetches live gas prices across four EVM
chains using free public RPC nodes.

## What it does

- Queries `eth_gasPrice` on Ethereum, Base, Polygon, and Arbitrum
- Converts wei → gwei and classifies each chain as LOW / MEDIUM / HIGH
  against per-chain thresholds
- Prints a table (or JSON with `--json`)
- Appends a timestamped snapshot to a JSONL log file with `--log`
- Can act as a threshold gate in scripts/automations with `--alert-below`

## Quick start

```bash
python3 scripts/gas_tracker.py
python3 scripts/gas_tracker.py --chain ethereum --json
python3 scripts/gas_tracker.py --log gas_history.jsonl
```

## Dependencies

```
pip install requests
```

## Notes

Uses `publicnode.com` RPC endpoints, which are free and require no API
key. If a chain's RPC is temporarily unavailable, that chain reports an
error while the others still succeed.
