---
name: airdrop-eligibility-tracker
description: Scores a crypto wallet's on-chain activity across Ethereum, Arbitrum, Base, Optimism, and Polygon against common retroactive airdrop farming heuristics (transaction count, multi-chain diversity, wallet balance, account activity) using free public JSON-RPC endpoints with no API key required. Useful for crypto airdrop farming, defi power users, whale-style multi-wallet trackers, passive income seekers, python developers, and ai agent operators who want a quick 0-100 eligibility health-check before a snapshot. Supports scoring a single wallet or comparing several wallets side by side to see which ones have the strongest multi-chain footprint. Built from the generic criteria protocols like Arbitrum, Optimism, zkSync, and Blast have historically leaned on — cross-chain tx volume, distinct chain presence, and account age/balance — not any single project's unpublished real snapshot rules.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Airdrop Eligibility Tracker

Pulls transaction count, native balance, and contract-deployment status for
a wallet across five EVM chains (Ethereum, Arbitrum, Base, Optimism,
Polygon) via free public RPC endpoints, then produces a 0-100 heuristic
"airdrop farming health" score plus a plain-language tier.

## When to use this skill

- The user wants to check whether a wallet "looks active enough" for
  retroactive airdrop snapshots before an announcement.
- The user is running multiple farming wallets and wants to compare them
  side by side to find weak ones that need more activity.
- The user asks "how is my airdrop farming going" or "which of my wallets
  has the best multi-chain footprint."

## How to run it

```bash
python3 scripts/airdrop_tracker.py score 0xYourAddress
python3 scripts/airdrop_tracker.py score 0xYourAddress --json
python3 scripts/airdrop_tracker.py score 0xYourAddress --chains ethereum,arbitrum,base
python3 scripts/airdrop_tracker.py compare 0xAddr1 0xAddr2 0xAddr3
```

## Scoring model (0-100)

- **Tx volume (0-40 pts)**: total transaction count summed across scanned
  chains, capped at 200 total tx.
- **Chain diversity (0-35 pts)**: number of chains with at least one
  transaction, weighted heavily because most L2 airdrops (ARB, OP) have
  historically rewarded cross-chain / bridge activity specifically.
- **Balance signal (0-25 pts)**: flat bonus if any scanned chain holds more
  than 0.01 of its native token, as a rough sybil-vs-real-user signal.

Tiers: STRONG (75+), MODERATE (45-74), WEAK (15-44), DORMANT (<15).

## Important limitation — read this before trusting the score

This tool has **no knowledge of any specific project's actual, often
unpublished, snapshot criteria**. Real airdrops frequently filter on things
this script cannot see: Discord/Twitter engagement, governance votes,
specific protocol interactions (e.g. "used Uniswap 5+ times"), Sybil
clustering analysis, or a hard minimum spend threshold. Treat the score as
a rough directional health-check ("is this wallet obviously dormant or
obviously active"), never as a guarantee of eligibility for any real
airdrop.

## Requirements

- Python 3.8+, standard library only.
- Outbound HTTPS access to `*.publicnode.com` RPC endpoints (free, no key).
