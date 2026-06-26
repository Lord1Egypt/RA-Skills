---
name: bankroll-manager
description: "Track bankroll across sportsbooks and prediction markets. Log bets, record results, calculate ROI, generate P&L reports, and enforce risk limits. Use when asked about bankroll, P&L, bet logging, ROI, units, risk limits, or money management."
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["sqlite3", "python3"]
---

# Bankroll Manager — Cross-Platform P&L Tracker

Track bankroll, log bets, calculate ROI, and enforce risk limits across all betting platforms.

## When to Use

Use this skill when the user asks about:
- Logging a new bet or recording a bet result
- Current bankroll balance or P&L
- Daily, weekly, or per-platform P&L reports
- ROI or units won/lost
- Whether a bet is within their risk limits
- "How much am I up/down?"
- "Can I afford this bet?"
- Setting or adjusting risk limits

## Database Location

All bankroll data is stored in: `~/.openclaw/data/bankroll.db`

## Operations

### 1. Log a Bet

Record a new bet. Replace values in caps:

```bash
sqlite3 ~/.openclaw/data/bankroll.db \
  "INSERT INTO bets (platform, sport, selection, bet_type, stake, odds, notes)
   VALUES ('PLATFORM', 'SPORT_KEY', 'SELECTION', 'BET_TYPE', STAKE, ODDS, 'NOTES');"

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-bankroll-manager-skill/](https://agentbets.ai/guides/openclaw-bankroll-manager-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
