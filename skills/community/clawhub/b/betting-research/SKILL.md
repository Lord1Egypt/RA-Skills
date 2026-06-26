---
name: betting-research
description: Multi-source sports betting research tool. Aggregates odds, team form, head-to-head history, weather conditions, and injury data to identify value betting opportunities. Use when user asks about specific matches, wants betting analysis, or needs data-driven predictions for sports betting.
---

# Betting Research

Multi-source data aggregator for sports betting analysis. Pulls from free and paid APIs to give you an edge.

## Data Sources

| Source | Data | Cost | Rate Limit |
|--------|------|------|------------|
| TheSportsDB | Fixtures, results, H2H, team info | **Free** | No limit |
| API-Football | Lineups, injuries, player stats, xG | **100 calls/day free** | 100/day |
| Open-Meteo | Weather (precipitation, wind) | **Free** | No limit |
| The Odds API | Current odds, bookmaker prices | **500 calls/month free** | 500/mo |

## Quick Start

```bash
# Research a specific match
python3 ~/.openclaw/workspace/skills/betting-research/scripts/betting_research.py "Liverpool vs Everton"

# Research a team
python3 ~/.openclaw/workspace/skills/betting-research/scripts/betting_research.py --team "Bolton Wanderers"
```

## What You Get

### Basic Analysis (Free APIs)
- ✅ Team form (last 5 matches)
- ✅ Win/draw/loss record
- ✅ Goals scored/conceded
- ✅ Upcoming fixtures
- ✅ Head-to-head history
- ✅ Weather conditions

### Pro Analysis (with API-Football key)
- ⭐ Confirmed lineups (1 hour before kickoff)
- ⭐ Injury/suspension reports
- ⭐ Expected goals (xG) data
- ⭐ Player form and ratings
- ⭐ Manager tactics info

## Setup

### The Odds API (already have)
Key stored at: `~/.config/the-odds-api/key`

### API-Football (optional, for pro features)
1. Sign up: https://www.api-football.com/pricing
2. Get free tier: 100 calls/day
3. Save key:
```bash
mkdir -p ~/.config/api-football
echo '{"api_key": "YOUR_KEY"}' > ~/.config/api-football/config.json
```

## Usage Examples

**Pre-match research:**
```bash
python3 ~/.openclaw/workspace/skills/betting-research/scripts/betting_research.py "Bolton vs Plymouth"
```

**Full analysis (uses more API calls):**
```bash
python3 ~/.openclaw/workspace/skills/betting-research/scripts/betting_research.py "Liverpool vs Man City" --full
```

**Check multiple games efficiently:**
```bash
# Uses only 3-4 API calls per match
# 100 calls = ~25 matches per day
```

## Interpreting Results

### Value Indicators
- **Form streaks** — teams on hot/cold runs
- **H2H dominance** — historical advantage
- **Weather impact** — rain = lower scoring
- **Odds mispricing** — bookie odds vs. true probability

### What NOT to Expect
- ❌ Guaranteed winners
- ❌ "Bet on this" tips
- ❌ Inside information

### What TO Expect
- ✅ Data patterns
- ✅ Value opportunities
- ✅ Informed decisions

## Pro Tips

1. **Check lineups 1 hour before kickoff** — key players resting = different bet
2. **Weather matters** — rain, wind affect totals (under value)
3. **H2H at this venue** — home advantage varies by team
4. **Motivation check** — cup games, relegation battles

## API Call Budgeting

| Task | Calls |
|------|-------|
| Basic match research | 3-4 |
| Full analysis + lineups | 8-10 |
| Team form check | 2-3 |
| Odds comparison | 1 |

**100 calls/day = 10-15 full match analyses**

See [references/data-sources.md](references/data-sources.md) for API details.
