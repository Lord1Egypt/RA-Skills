---
name: fpl-assistant
description: Fantasy Premier League (FPL) assistant for squad management, transfer planning, captain selection, and chip strategy. Use when users ask about FPL lineup decisions, transfer suggestions, captain picks, gameweek analysis, FPL rules, or anything related to Fantasy Premier League. Triggers on "FPL", "fantasy premier league", "fantasy", "GW" (gameweek), "captain", "transfer", "chip", "wildcard", "free hit", "bench boost", "triple captain".
---

# FPL Assistant

## Overview

Assist with Fantasy Premier League decisions: squad analysis, transfers, captaincy, chip timing, and gameweek planning. Combine FPL API data with multi-dimensional analysis (not just FDR).

## Core Workflow

### 1. Gather Context

Before making recommendations, collect:
- User's current 15-player squad (with buy prices)
- Remaining budget (ITB)
- Available free transfers
- Chips status (wildcard, free hit, bench boost, triple captain)
- Current GW number

### 2. Fetch Live Data via FPL API

Use `curl` against the public FPL API. No auth needed.

```bash
# Bootstrap data (teams, players, events)
curl -s 'https://fantasy.premierleague.com/api/bootstrap-static/'

# GW fixtures with difficulty ratings
curl -s 'https://fantasy.premierleague.com/api/fixtures/?event={gw}'

# Player detail (history, fixtures)
curl -s 'https://fantasy.premierleague.com/api/element-summary/{player_id}/'

# Manager team
curl -s 'https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gw}/picks/'
```

See `references/api.md` for full API reference.

### 3. Multi-Dimensional Analysis

**Do NOT rely solely on FDR (Fixture Difficulty Rating).** FDR is a season-long aggregate and misses short-term dynamics. Layer these factors:

| Factor | What to Check | Source |
|--------|--------------|--------|
| Recent form | Last 4-6 GW results, player form rating | FPL API `form` field, recent results |
| League position & motivation | Top 4/6 (European race), bottom 3 (relegation), mid-table dead rubber | League table |
| Fixture congestion | Midweek European/FA Cup matches, travel load | Schedule check |
| Head-to-head | Recent meetings between the two teams | Historical data |
| Home/away split | Some teams significantly better at home | Season stats |
| Injury/rotation risk | Flagged players, midweek match recovery | FPL API `status`, news |
| Expected stats | xG, xA, shots, key passes vs actual returns | Advanced stats sites |

### 4. Transfer Strategy

- **1 free transfer**: Use only if clear upgrade; otherwise roll it to next GW for 2 FTs
- **2 free transfers**: Can address multiple weak spots or make a coordinated pair of moves
- **-4 hit**: Only if expected point gain exceeds 4+ over multiple GWs
- Prioritize: remove players with bad fixtures AND bad form > remove only bad fixtures
- Consider value (selling price vs current price) when transferring out

### 5. Captain Selection

Priority factors:
1. Fixture difficulty (FDR ≤ 2 strongly preferred)
2. Player form (recent goals/assists)
3. Home advantage
4. Set-piece duty (penalties, free kicks)
5. Expected minutes (rotation risk)
6. Ownership & rank protection vs differential

### 6. Chip Strategy

- **Wildcard**: Best used before a fixture swing or when squad needs major overhaul
- **Free Hit**: Ideal for blank/double gameweeks where normal squad is affected
- **Bench Boost**: Save for double gameweeks when all 15 players play
- **Triple Captain**: Use on a premium player with excellent fixture in a single or double GW

## Output Format

Provide recommendations as:
1. **Analysis summary** (key factors for the GW)
2. **Starting XI** with formation
3. **Bench order**
4. **Captain / Vice-captain**
5. **Transfer suggestions** (with reasoning)
6. **Chip recommendation** (if applicable)

## Reference Files

- `references/rules.md` — Full FPL scoring rules and squad constraints
- `references/api.md` — FPL API endpoints and data structures
- `references/strategy.md` — Advanced selection methodology
