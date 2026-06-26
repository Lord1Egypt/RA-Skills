---
name: clv-tracker
description: "Track Closing Line Value — the gold standard for measuring betting edge. Log placement odds, fetch closing lines, compute CLV, and generate performance reports. Use when asked about CLV, closing line, edge tracking, or bet performance."
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["sqlite3", "curl", "jq", "python3"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "Free API key from https://the-odds-api.com/"
        env: "ODDS_API_KEY"
---

# CLV Tracker — Closing Line Value

Track and measure your betting edge by comparing placement odds against closing lines.

## When to Use

Use this skill when the user asks about:
- Logging a bet with placement odds for CLV tracking
- Checking closing line value for recent bets
- Generating a CLV performance report
- Whether their betting edge is real or variance
- Exporting bet history for analysis
- "Am I beating the close?"

## Database Location

All bet data is stored in: `~/.openclaw/data/clv.db`

## Operations

### 1. Log a Bet

Record a new bet with placement odds for future CLV calculation. Replace the values in caps:

```bash
python3 -c "
odds = PLACEMENT_ODDS
prob = abs(odds)/(abs(odds)+100) if odds < 0 else 100/(odds+100)
print(f'{prob:.6f}')
" | xargs -I{} sqlite3 ~/.openclaw/data/clv.db \
  "INSERT INTO clv_bets (game_id, sport, selection, bet_type, placement_odds, placement_prob)
   VALUES ('GAME_ID', 'SPORT_KEY', 'TEAM_OR_SELECTION', 'BET_TYPE', PLACEMENT_ODDS, {});"

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-clv-tracker-skill/](https://agentbets.ai/guides/openclaw-clv-tracker-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
