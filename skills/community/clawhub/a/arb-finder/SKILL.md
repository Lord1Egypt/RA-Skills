---
name: arb-finder
description: "Detect guaranteed-profit arbitrage opportunities across sportsbooks and prediction markets. Compares odds from 20+ bookmakers, Polymarket, and Kalshi. Calculates optimal stake distribution. Use when asked about arbs, arbitrage, guaranteed profit, or cross-market pricing."
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      bins: ["curl", "jq", "python3"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "Free API key from https://the-odds-api.com/"
        env: "ODDS_API_KEY"
---

# Arbitrage Finder

Detect cross-market arbitrage opportunities across sportsbooks and prediction markets.

## When to Use

Use this skill when the user asks about:
- Finding arbitrage or arb opportunities
- Guaranteed profit bets
- Cross-market pricing discrepancies
- Comparing sportsbook odds vs prediction market prices
- Calculating optimal stake distribution for an arb
- Whether a specific event has an arb available

## Operations

### 1. Scan Sportsbook Arbs

Scan a sport for two-way moneyline arbs across bookmakers. Replace SPORT_KEY with the appropriate key (e.g., basketball_nba, americanfootball_nfl):

```bash
curl -s "https://api.the-odds-api.com/v4/sports/SPORT_KEY/odds?apiKey=$ODDS_API_KEY&regions=us&markets=h2h&oddsFormat=american" \
  | jq '[.[] | {
    game: "\(.away_team) @ \(.home_team)",
    start: .commence_time,
    away_team: .away_team,
    home_team: .home_team,
    best_away: (.bookmakers | map({book: .title, odds: ((.markets[] | select(.key=="h2h")).outcomes[] | select(.name == .away_team) | .price)}) | sort_by(-.odds) | first),
    best_home: (.bookmakers | map({book: .title, odds: ((.markets[] | select(.key=="h2h")).outcomes[] | select(.name == .home_team) | .price)}) | sort_by(-.odds) | first)
  } | . + {
    ip_away: (if .best_away.odds > 0 then 100/(.best_away.odds+100) else (-.best_away.odds)/(-.best_away.odds+100) end),
    ip_home: (if .best_home.odds > 0 then 100/(.best_home.odds+100) else (-.best_home.odds)/(-.best_home.odds+100) end)
  } | . + {
    total_ip: (.ip_away + .ip_home),
    is_arb: ((.ip_away + .ip_home) < 1)
  } | select(.is_arb == true) | {
    game, start,
    away: {team: .away_team, odds: .best_away.odds, book: .best_away.book},
    home: {team: .home_team, odds: .best_home.odds, book: .best_home.book},
    margin: ((1 - .total_ip) * 100 | . * 100 | round / 100 | tostring + "%")
  }]'
```

### 2. Cross-Market Arb Scan — Sportsbooks vs Polymarket

Compare sportsbook moneylines against Polymarket event prices. First fetch Polymarket events, then compare:

Fetch Polymarket active sports/politics events:

```bash
curl -s "https://gamma-api.polymarket.com/events?closed=false&limit=50&order=volume24hr&ascending=false" \
  | jq '[.[] | {
    id: .id,
    title: .title,
    markets: [.markets[] | {
      question: .question,
      outcomes: .outcomes,
      outcomePrices: .outcomePrices,
      volume24hr: .volume24hr
    }]
  }]'
```

For a specific Polymarket market, get the current prices and convert to implied odds:

```bash
curl -s "https://gamma-api.polymarket.com/markets?id=MARKET_ID" \
  | jq '.[0] | {
    question: .question,
    outcomes: [.outcomes as $o | .outcomePrices | split(",") | to_entries[] | {
      outcome: ($o | split(",") | .[.key]),
      price: (. .value | tonumber),
      implied_pct: ((. .value | tonumber) * 100 | round | tostring + "%"),
      american_equiv: (if (.value | tonumber) >= 0.5
        then (-((.value | tonumber) / (1 - (.value | tonumber)) * 100) | round)
        else (((1 - (.value | tonumber)) / (.value | tonumber) * 100) | round)
        end)
    }]
  }'
```

To check for a cross-market arb, compare the Polymarket implied probability for one side against the sportsbook odds for the other side. If the sum of the best available implied probabilities across platforms is below 100%, an arb exists.

### 3. Scan Kalshi Event Contracts

Fetch Kalshi markets for comparison:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/events?status=open&limit=50&with_nested_markets=true" \
  | jq '[.events[] | {
    title: .title,
    category: .category,
    markets: [.markets[]? | {
      ticker: .ticker,
      title: .title,
      yes_price: .yes_ask,
      no_price: .no_ask,
      volume: .volume,
      yes_implied: ((.yes_ask // 0) * 100 | round | tostring + "%"),
      no_implied: ((.no_ask // 0) * 100 | round | tostring + "%")
    }]
  }]'
```

Kalshi contract prices are already probabilities (e.g., $0.65 = 65% implied). Convert to American odds for comparison:

```bash
python3 -c "
price = 0.65  # Replace with actual Kalshi contract price
if price >= 0.5:
    american = -(price / (1 - price)) * 100
else:
    american = ((1 - price) / price) * 100
print(f'Kalshi price: \${price:.2f}')
print(f'Implied prob: {price*100:.1f}%')
print(f'American odds: {american:+.0f}')
"
```

### 4. Calculate Optimal Stake Distribution

Given an arb opportunity, calculate exact stakes for equal profit across all legs:

```bash
python3 -c "
import sys, json

# Input: best odds per outcome and total bankroll
odds_1 = 150    # American odds for outcome 1 (e.g., +150)
odds_2 = -130   # American odds for outcome 2 (e.g., -130)
bankroll = 1000  # Total amount to deploy

# Convert American odds to implied probability
def american_to_ip(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)

# Convert American odds to decimal
def american_to_decimal(odds):
    if odds > 0:
        return (odds / 100) + 1
    else:
        return (100 / abs(odds)) + 1

ip1 = american_to_ip(odds_1)
ip2 = american_to_ip(odds_2)
total_ip = ip1 + ip2

if total_ip >= 1:
    print('NO ARB: Total implied probability >= 100%')
    print(f'Total IP: {total_ip*100:.2f}%')
    sys.exit(0)

dec1 = american_to_decimal(odds_1)
dec2 = american_to_decimal(odds_2)

# Equal-profit stake distribution
stake1 = bankroll / (1 + dec1 / dec2)
stake2 = bankroll - stake1

payout1 = stake1 * dec1
payout2 = stake2 * dec2
profit = payout1 - bankroll

margin = (1 - total_ip) * 100

print(f'=== ARB FOUND ===')
print(f'Margin: {margin:.2f}%')
print(f'Outcome 1: odds {odds_1:+d} → stake \${stake1:.2f} → payout \${payout1:.2f}')
print(f'Outcome 2: odds {odds_2:+d} → stake \${stake2:.2f} → payout \${payout2:.2f}')
print(f'Total staked: \${bankroll:.2f}')
print(f'Guaranteed profit: \${profit:.2f} ({profit/bankroll*100:.2f}%)')
"
```

Replace the `odds_1`, `odds_2`, and `bankroll` values with the actual arb opportunity found in Operations 1-3. For three-way markets (e.g., soccer), extend the calculation to three outcomes.

## Output Rules

1. Always show the event, both sides, and which platform/book has the best price per side
2. Display the arb margin as a percentage (e.g., "3.5% margin")
3. For stake calculations, show exact dollar amounts and guaranteed profit
4. Sort arb opportunities by margin (highest first)
5. If no arbs are found, report the closest near-arb (lowest total implied probability)
6. Always note that arb windows are time-sensitive and lines may have moved
7. Report remaining Odds API quota after sportsbook scans

## Error Handling

- If ODDS_API_KEY is not set, tell the user to get a free key at https://the-odds-api.com/
- If Polymarket API returns empty, the event may not be listed on Polymarket
- If Kalshi API returns empty, check that the event category is available on Kalshi
- If no arbs found, report the tightest market (lowest combined IP) as a near-arb
- If rate limited on any API, report which source hit the limit and suggest waiting

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-arb-finder-skill/](https://agentbets.ai/guides/openclaw-arb-finder-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
