# airdrop-eligibility-tracker

Scores a wallet's on-chain footprint across five EVM chains against generic
airdrop-farming heuristics, using free public RPC endpoints (no API key).

## Why

Checking "is my wallet active enough" across five chains by hand means five
separate block explorer visits. This script pulls transaction count, native
balance, and contract status from each chain's public JSON-RPC in one call
and produces a single 0-100 score plus tier.

## Usage

```bash
# Score a single wallet across all 5 default chains
python3 scripts/airdrop_tracker.py score 0xYourAddress

# JSON output
python3 scripts/airdrop_tracker.py score 0xYourAddress --json

# Limit to specific chains
python3 scripts/airdrop_tracker.py score 0xYourAddress --chains ethereum,base

# Compare multiple wallets
python3 scripts/airdrop_tracker.py compare 0xAddr1 0xAddr2 0xAddr3
```

## Chains covered

Ethereum, Arbitrum, Base, Optimism, Polygon — all via free `publicnode.com`
RPC endpoints. No API key, no rate-limit tier required for light use.

## Scoring

0-100, weighted: tx volume (40%), chain diversity (35%), balance signal
(25%). See `SKILL.md` for the exact formula and important limitations —
this is a generic heuristic, not insider knowledge of any real snapshot.

## Requirements

- Python 3.8+, standard library only (`urllib`, `json`, `argparse`).
- Outbound HTTPS access to `*.publicnode.com`.

## Notes

Read-only. Never asks for or touches a private key — pass any public
wallet address as an argument.
