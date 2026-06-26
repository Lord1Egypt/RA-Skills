---
name: profit-engine
description: 7x24 automated profit opportunity scanner for AI agents. Scans ClawTasks, Moltbook, Polymarket, Airdrops, GitHub Bounties, and toku.agency for earning opportunities. Use when you need to find and monitor money-making opportunities across multiple platforms automatically.
---

# Profit Engine

Automated multi-platform profit opportunity scanner for AI agents.

## Quick Start

```bash
bash scripts/scan.sh
```

## Platforms Scanned

1. **ClawTasks** - Agent-to-agent bounty marketplace (USDC)
2. **Moltbook** - Social intelligence feed (prediction markets)
3. **Polymarket** - Whale wallet monitoring
4. **Airdrops.io** - Latest crypto airdrop opportunities
5. **GitHub Bounties** - Open source bounty programs (boss.dev, Algora)
6. **toku.agency** - AI agent service marketplace (USD)

## Configuration

Set in environment or edit script:
- `MOLTBOOK_API_KEY` - Moltbook API key for feed access
- `LOG_DIR` - Log output directory (default: logs/)

## Output

Logs to `logs/profit_engine.log` with timestamps. Returns summary of opportunities found across all platforms.

## Recommended Schedule

Run hourly via cron for continuous opportunity detection.
