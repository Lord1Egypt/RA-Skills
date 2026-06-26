---
name: ev-calculator
description: "Calculate expected value for any sports bet or prediction market position. Supports American odds, decimal odds, implied probability, and Kalshi contract prices. Use when asked about expected value, EV, whether a bet is worth it, +EV opportunities, or breakeven probability."
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
---

# Expected Value Calculator

Calculate the expected value of any bet given offered odds and your estimated true probability.

## When to Use

Use this skill when the user asks about:
- Expected value of a bet
- Whether a bet is +EV or -EV
- Is this bet worth taking at these odds
- Breakeven probability for given odds
- Comparing EV across multiple bets
- Finding the best value bets on a slate
- How much edge they have on a line

## Odds Conversion Reference

Before computing EV, convert all inputs to decimal odds:

| Format | Example | To Decimal Odds |
|--------|---------|-----------------|
| American (+) | +150 | 1 + odds/100 = 2.50 |
| American (-) | -200 | 1 + 100/|odds| = 1.50 |
| Decimal | 2.50 | Already decimal |
| Implied Prob | 40% | 1/prob = 2.50 |
| Kalshi price | $0.40 | 1/price = 2.50 |

## Operations

### 1. Single Bet EV

Calculate expected value for one bet. User must provide: odds (any format) and their estimated true probability.

```bash
python3 -c "
import sys

odds_input = sys.argv[1]
true_prob = float(sys.argv[2]) / 100 if float(sys.argv[2]) > 1 else float(sys.argv[2])

# Convert to decimal odds
if odds_input.startswith('+'):
    decimal_odds = 1 + int(odds_input) / 100
elif odds_input.startswith('-'):
    decimal_odds = 1 + 100 / abs(int(odds_input))
elif odds_input.startswith('$') or odds_input.startswith('0.'):
    price = float(odds_input.replace('$', ''))
    decimal_odds = 1 / price
else:
    decimal_odds = float(odds_input)

implied_prob = 1 / decimal_odds
ev_per_dollar = true_prob * decimal_odds - 1
edge = true_prob - implied_prob

print(f'Offered odds: {odds_input} (decimal {decimal_odds:.3f})')
print(f'Implied probability: {implied_prob:.1%}')
print(f'Your true probability: {true_prob:.1%}')
print(f'Edge: {edge:+.1%}')
print(f'EV per \$1: {ev_per_dollar:+.4f}')
print(f'EV per \$100: {ev_per_dollar * 100:+.2f}')
print(f'Verdict: {\"✅ +EV — BET\" if ev_per_dollar > 0 else \"❌ -EV — PASS\"} ')
" "ODDS" "TRUE_PROB_PERCENT"

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-ev-calculator-skill/](https://agentbets.ai/guides/openclaw-ev-calculator-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
