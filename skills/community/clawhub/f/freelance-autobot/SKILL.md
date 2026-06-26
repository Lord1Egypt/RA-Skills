---
name: freelance-autobot
version: 1.0.18
description: |
  Autonomous freelance hunter — finds gigs on FreeLanceDAO and CryptoGigs,
  scores them for fit, and auto-submits proposals. Also builds your CryptoGig
  profile and services compatibility: Zo Computer, Python 3, requests, web scraping
metadata:
  author: ssyopros.zo.computer
  category: freelancing
  tags: crypto, freelance, freelancedao, cryptogig, passive-# freelance-autobot

Find and apply to crypto-native freelance gigs 
## Platforms

- **FreeLanceDAO** (freelancedao.xyz) — Web3/Hedera, DAO governance, 5% fee
- **CryptoGigs** (cryptogig.com) — crypto payments + escrow, 10% fee
- **OpenCollab** (opencollab.ai) — crypto-native tech gigs

## Usage

```bash
# Hunt for gigs (dry run)
python scripts/gig_hunter.py --platforms freelancedao,cryptogig --dry-run

# Create your CryptoGig profile
python scripts/build_cryptogig_profile.py

# Auto-submit proposals
python scripts/gig_hunter.py --platforms freelancedao,cryptogig
```

## Workflow

1. Scrape new gigs from each platform
2. Score by: skill match (40%) + budget fit (30%) + recency (20%) + competition (10%)
3. Skip if: client has 0% completion, budget < $50, no escrow
4. Submit proposal with personalized pitch using skills metadata
5. Log earnings attempt in earnings_log.json

## Profile Bio (copy to platforms)

```
Masters-educated tech specialist with 26+ years in tech:
• DeFi & Smart Contract Development (Solidity, Solana)
• Options Trading Systems (Elliott Wave, whale flow, Bollinger Bands)
• AI Agents & Automation (Python, 24/7 autonomous bots)
• GTM Strategy & 
Delivered 50+ projects globally. Build ```

## Services to List on CryptoGigs

| Service | Price | Description |
|---|---|---|
| DeFi Trading Bot | $150 | Custom sniping/arbitrage bot |
| Options Backtest | $100 | Strategy backtest with full analysis |
| AI Agent | $200 | 24/7 autonomous agent for your business |
