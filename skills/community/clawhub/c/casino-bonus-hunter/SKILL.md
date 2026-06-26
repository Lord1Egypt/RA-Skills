---
name: casino-bonus-hunter
description: Scans 30+ online casinos, calculates the Expected Value of each welcome/reload/cashback bonus using optimal blackjack strategy, adjusts EV by casino reputation score, and outputs a ranked list so you know exactly which bonus to hunt next.
metadata:
  author: "Mibayy"
  version: "1.0.0"
  displayName: "Casino Bonus Hunter"
  difficulty: "beginner"
  type: "automaton"
---

# Casino Bonus Hunter

Ranks casino bonuses by **adjusted Expected Value** — EV calculated with optimal blackjack strategy (0.3% house edge), then multiplied by a reputation score (0-10) based on CasinoGuru ratings and payout history.

## What it does

1. Evaluates 30+ welcome, reload, and cashback bonuses from crypto and traditional casinos
2. Calculates EV: `bonus - (wagering * house_edge)` with optimal strategy
3. Adjusts EV by reputation: a $400 EV bonus at a shady casino scores lower than a $300 EV bonus at BitStarz (9.2/10)
4. Outputs ranked JSON + console table

## EV Formula

```
EV_gross = bonus_amount - (bonus * wagering_x / game_contribution * house_edge)
EV_adjusted = EV_gross * (reputation_score / 10)
```

Example — Stake $500 welcome (40x wagering, blackjack):
- Real wagering = $20,000
- Expected loss = $20,000 * 0.3% = $60
- EV_gross = $500 - $60 = **+$440**
- EV_adjusted = $440 * 9.1/10 = **+$400** (accounts for Stake's reliability)

## Output

Saves to `/tmp/casino_bonuses.json` with full details per bonus.

## Configuration (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| BONUS_MIN_REP | 0 | Minimum reputation score (e.g., 8 = reputable casinos only) |
| BONUS_MIN_EV | 0 | Minimum EV to include (e.g., 50 = only $50+ EV) |
| BONUS_TOP_N | 20 | Number of top bonuses to return |
| BONUS_OUTPUT_FILE | /tmp/casino_bonuses.json | Output file path |

## Runs every 6 hours (bonus data changes infrequently)

## Strategy notes

- Always play blackjack for wagering (0.3% edge vs 4%+ for slots)
- Check game contribution — some casinos count blackjack at only 10%
- Cashback bonuses have wagering x1 = almost free money
- Filter by `BONUS_MIN_REP=8` to avoid unreliable casinos
