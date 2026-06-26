---
name: cross-market-pricer
description: "Normalize odds across Polymarket, Kalshi, and sportsbooks into a unified implied-probability format. Enables apples-to-apples comparison for the same event across platforms. Use when asked to compare odds across markets, normalize pricing, or find cross-platform mispricings."
metadata:
  openclaw:
    emoji: "⚖️"
    requires:
      bins: ["curl", "jq", "python3"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "Free API key from https://the-odds-api.com/"
        env: "ODDS_API_KEY"
---

# Cross-Market Pricer

Normalize and compare odds across Polymarket, Kalshi, and traditional sportsbooks.

## When to Use

Use this skill when the user asks about:
- Comparing odds across different platforms (sportsbooks vs prediction markets)
- Normalizing prices to a common format
- Side-by-side pricing for the same event on Polymarket, Kalshi, and a sportsbook
- Whether there's a pricing gap or mispricing between platforms
- Converting between American odds, implied probability, and contract prices

## Conversion Reference

American to probability: negative → |odds|/(|odds|+100), positive → 100/(odds+100)
Polymarket to probability: price is already probability
Kalshi to probability: contract_price (already 0.00–1.00 from API)
Probability to American: >0.5 → -(prob/(1-prob))*100, <0.5 → +((1-prob)/prob)*100

## Operations

### 1. Fetch Sportsbook Odds as Normalized Probability

Pull American odds from The Odds API and convert to implied probability inline:

```bash
curl -s "https://api.the-odds-api.com/v4/sports/SPORT_KEY/odds?apiKey=$ODDS_API_KEY&regions=us&markets=h2h&oddsFormat=american" \
  | jq '[.[] | {
    event: "\(.away_team) vs \(.home_team)",
    start: .commence_time,
    source: "sportsbooks",
    outcomes: [.bookmakers[0].markets[0].outcomes[] | {
      name: .name,
      american_odds: .price,
      implied_prob: (if .price < 0 then (-((.price)) / (-((.price)) + 100)) else (100 / (.price + 100)) end) | (. * 1000 | round / 1000)
    }]
  }]'
```

Replace SPORT_KEY with the appropriate key (e.g., basketball_nba, americanfootball_nfl).

### 2. Fetch Polymarket Prices as Normalized Probability

Pull market prices from Polymarket's Gamma API:

```bash
curl -s "https://gamma-api.polymarket.com/markets?closed=false&limit=10&tag=CATEGORY" \
  | jq '[.[] | {
    event: .question,
    source: "polymarket",
    outcomes: [{
      name: "Yes",
      polymarket_price: (.outcomePrices | fromjson | .[0] | tonumber | (. * 1000 | round / 1000)),
      implied_prob: (.outcomePrices | fromjson | .[0] | tonumber | (. * 1000 | round / 1000))
    }, {
      name: "No",
      polymarket_price: (.outcomePrices | fromjson | .[1] | tonumber | (. * 1000 | round / 1000)),
      implied_prob: (.outcomePrices | fromjson | .[1] | tonumber | (. * 1000 | round / 1000))
    }],
    volume: .volume,
    liquidity: .liquidity
  }]'
```

Replace CATEGORY with the relevant tag (e.g., "sports", "nba", "politics", "crypto").

### 3. Fetch Kalshi Contract Prices as Normalized Probability

Pull contract prices from Kalshi's public market data API:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets?status=open&limit=10&series_ticker=SERIES_TICKER" \
  | jq '[.markets[] | {
    event: .title,
    source: "kalshi",
    ticker: .ticker,
    outcomes: [{
      name: "Yes",
      kalshi_price: (.yes_ask / 100),
      implied_prob: (.yes_ask / 100)
    }, {
      name: "No",
      kalshi_price: (.no_ask / 100),
      implied_prob: (.no_ask / 100)
    }],
    volume: .volume
  }]'
```

Replace SERIES_TICKER with the Kalshi series ticker for the event category.

### 4. Unified Cross-Market Comparison

When the user wants to compare the SAME event across platforms, fetch from each source and use Python to produce a unified table:

```bash
python3 -c "
import json, subprocess

def american_to_prob(odds):
    if odds < 0:
        return round(abs(odds) / (abs(odds) + 100), 4)
    else:
        return round(100 / (odds + 100), 4)

def prob_to_american(prob):
    if prob >= 1: return -99999
    if prob <= 0: return 99999
    if prob > 0.5:
        return round(-(prob / (1 - prob)) * 100)
    elif prob < 0.5:
        return round(((1 - prob) / prob) * 100)
    else:
        return 100

# Input: user provides these values (agent fills from context)
platforms = {
    'PLATFORM_1_NAME': {'yes_prob': PLATFORM_1_YES_PROB, 'no_prob': PLATFORM_1_NO_PROB},
    'PLATFORM_2_NAME': {'yes_prob': PLATFORM_2_YES_PROB, 'no_prob': PLATFORM_2_NO_PROB},
}

print('=== Cross-Market Comparison ===')
print(f\"{'Platform':<18} {'Yes Prob':>10} {'Yes Amer':>10} {'No Prob':>10} {'No Amer':>10} {'Total':>8}\")
print('-' * 70)
for name, data in platforms.items():
    y = data['yes_prob']
    n = data['no_prob']
    total = round(y + n, 4)
    y_am = prob_to_american(y)
    n_am = prob_to_american(n)
    y_am_s = f'+{y_am}' if y_am > 0 else str(y_am)
    n_am_s = f'+{n_am}' if n_am > 0 else str(n_am)
    print(f'{name:<18} {y:>10.1%} {y_am_s:>10} {n:>10.1%} {n_am_s:>10} {total:>8.1%}')

# Flag mispricings
probs = [d['yes_prob'] for d in platforms.values()]
gap = max(probs) - min(probs)
if gap > 0.03:
    print(f'\n⚠ MISPRICING: {gap:.1%} gap across platforms on Yes side')
else:
    print(f'\nPricing aligned within {gap:.1%} — no actionable gap')
"
```

The agent must fill in PLATFORM_1_NAME, PLATFORM_1_YES_PROB, etc. from the results of Operations 1–3. If an event only exists on two platforms, remove the third entry.

### 5. Quick Single-Value Conversion

For ad-hoc conversions when the user gives a single odds value:

```bash
python3 -c "
odds_input = 'INPUT_VALUE'
# Detect format and normalize
if odds_input.startswith('+') or odds_input.startswith('-'):
    odds = int(odds_input)
    prob = abs(odds)/(abs(odds)+100) if odds < 0 else 100/(odds+100)
    fmt = 'American'
elif '.' in odds_input and float(odds_input) <= 1:
    prob = float(odds_input)
    fmt = 'Probability'
elif odds_input.startswith('\$'):
    prob = float(odds_input.replace('\$',''))
    fmt = 'Kalshi contract'
else:
    prob = float(odds_input)
    fmt = 'Decimal probability' if float(odds_input) <= 1 else 'Unknown'

# Convert to all formats
if prob > 0.5:
    american = round(-(prob/(1-prob))*100)
elif prob < 0.5:
    american = round(((1-prob)/prob)*100)
else:
    american = 100

am_str = f'+{american}' if american > 0 else str(american)
print(f'Input: {odds_input} ({fmt})')
print(f'Implied probability: {prob:.1%}')
print(f'American odds: {am_str}')
print(f'Kalshi contract: \${prob:.2f}')
print(f'Polymarket share: {prob:.4f}')
"
```

Replace INPUT_VALUE with the user's value (e.g., "-150", "0.62", "$0.58").

## Output Rules

1. Always show implied probability as the primary format (3 decimal places, e.g., 0.620)
2. Include American odds equivalent alongside probability for sportsbook-familiar users
3. When comparing platforms, display as a table with columns: Platform, Yes Prob, Yes American, No Prob, No American, Total
4. The "Total" column (Yes + No probabilities) reveals vig — anything over 100% is overround
5. Flag gaps greater than 3% between platforms as potential mispricings
6. Always note which sportsbook was used as the sportsbook source (since books differ)
7. Report The Odds API quota after any sportsbook fetch

## Error Handling

- If ODDS_API_KEY is not set, tell the user to get a free key at https://the-odds-api.com/
- If Polymarket returns empty results for a category, try broader search terms or list available categories
- If Kalshi returns empty results, the event may not have an active contract — suggest checking kalshi.com directly
- If an event exists on one platform but not another, report what's available and note the gap
- If rate limited on any API, report the limitation and suggest which platforms can still be queried

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-cross-market-pricer-skill/](https://agentbets.ai/guides/openclaw-cross-market-pricer-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
