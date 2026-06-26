---
name: bet-slip-parser
description: "Parse bet slips from text, natural language, or screenshots into structured JSON. Extracts stake, odds, bet type, selection, and sportsbook. Supports singles, parlays, teasers, and SGPs. Use when asked to parse, log, or read a bet slip."
metadata:
  openclaw:
    emoji: "🎫"
    requires:
      bins: ["bash"]
---

# Bet Slip Parser

Extract structured betting data from any bet slip format — pasted text, natural language, or screenshots.

## When to Use

Use this skill when the user:
- Pastes a bet confirmation or bet slip text
- Describes a bet they placed in natural language
- Shares a screenshot of a bet slip from any sportsbook
- Asks to "log this bet" or "parse this bet slip"
- Wants to convert a bet description into structured data
- Says "I just bet..." or "I placed a bet on..."

## Supported Bet Types

| Bet Type | Keywords |
|----------|----------|
| Moneyline | moneyline, ML, to win, h2h |
| Spread | spread, point spread, handicap, ATS, -3.5 |
| Total | total, over, under, O/U |
| Parlay | parlay, accumulator, multi, combo |
| Teaser | teaser, adjusted spread |
| Same-Game Parlay | SGP, same game, same-game |
| Prop | prop, player prop, over 24.5 pts |
| Future | future, outright, to win championship |

## Supported Sportsbooks

Identify the sportsbook from branding, URLs, or mentions:

| Sportsbook | Identifiers |
|------------|-------------|
| DraftKings | draftkings, dk, DK Sportsbook |
| FanDuel | fanduel, fd, FD Sportsbook |
| BetMGM | betmgm, mgm, BetMGM Sportsbook |
| Caesars | caesars, czr, Caesars Sportsbook |
| Pinnacle | pinnacle, pin |
| Bet365 | bet365, b365 |
| BetRivers | betrivers, rivers |
| PointsBet | pointsbet |
| Polymarket | polymarket, poly |
| Kalshi | kalshi |

If the sportsbook cannot be identified, set source to "unknown".

## Operations

### 1. Parse Text Bet Slip

When the user pastes sportsbook confirmation text, extract all fields and output JSON.

Extraction steps:
1. Identify sportsbook from text branding or URL
2. Identify bet type from keywords (see table above)
3. Extract team/player/event selections
4. Extract odds — convert to American if decimal or fractional
5. Extract stake amount and currency
6. Calculate potential payout if not shown
7. Extract timestamp if available

Odds conversion formulas (use inline when needed):

```bash
# Decimal to American
echo "$DECIMAL_ODDS" | python3 -c "
import sys
d = float(sys.stdin.read().strip())
if d >= 2.0:
    print(f'+{round((d - 1) * 100)}')
else:
    print(f'{round(-100 / (d - 1))}')"

# Fractional (e.g. 3/2) to American
echo "3/2" | python3 -c "
import sys
n, d = map(int, sys.stdin.read().strip().split('/'))
dec = (n / d) + 1
if dec >= 2.0:
    print(f'+{round((dec - 1) * 100)}')
else:
    print(f'{round(-100 / (dec - 1))}')"

# American to implied probability
echo "-110" | python3 -c "
import sys
odds = int(sys.stdin.read().strip())
if odds < 0:
    prob = abs(odds) / (abs(odds) + 100)
else:
    prob = 100 / (odds + 100)
print(f'{prob:.4f}')"

# American to decimal
echo "-110" | python3 -c "
import sys
odds = int(sys.stdin.read().strip())
if odds < 0:
    dec = 1 + (100 / abs(odds))
else:
    dec = 1 + (odds / 100)
print(f'{dec:.3f}')"
```

### 2. Parse Natural Language Bet

When the user describes a bet casually, extract the same fields.

Examples of natural language inputs and how to parse them:

- "I bet $100 on the Lakers ML at +150 on DraftKings"
  → source: draftkings, bet_type: moneyline, selection: Los Angeles Lakers, odds: +150, stake: 100
- "Put $25 on over 48.5 in Chiefs-Ravens at -110"
  → bet_type: total, selection: Over 48.5, odds: -110, stake: 25
- "Parlayed Lakers ML and Chiefs -3.5, $50 to win $320 on FanDuel"
  → bet_type: parlay, 2 legs, stake: 50, potential_payout: 320, source: fanduel

Always ask for missing critical fields:
- If no stake mentioned, ask "How much did you bet?"
- If no odds mentioned, ask "What were the odds?"
- If no sportsbook mentioned, set source to "unknown"

### 3. Parse Screenshot Bet Slip

When the user shares an image of a bet slip:

1. Identify sportsbook from app branding/colors (DraftKings=green/black, FanDuel=blue/white, BetMGM=gold/black, Caesars=dark blue)
2. Read all visible text on the bet slip
3. Extract: event name, bet type, selection, odds, stake, potential payout
4. For parlays, extract each individual leg
5. Output in the standard JSON schema

Note: Screenshot parsing requires the LLM to have vision capabilities. If vision is not available, ask the user to paste the bet slip as text instead.

### 4. Validate Parsed Output

After parsing, validate the extracted data:

```bash
# Validate American odds format (must be + or - followed by digits)
echo "$ODDS" | grep -qE '^[+-][0-9]+$' && echo "VALID" || echo "INVALID: odds must be +NNN or -NNN"

# Validate stake is positive number
echo "$STAKE" | grep -qE '^[0-9]+(\.[0-9]{1,2})?$' && echo "VALID" || echo "INVALID: stake must be positive number"

# Validate bet type
echo "$BET_TYPE" | grep -qE '^(moneyline|spread|total|parlay|teaser|sgp|prop|future)$' && echo "VALID" || echo "INVALID: unknown bet type"

# Cross-check: potential payout should match odds × stake
echo "$STAKE $ODDS" | python3 -c "
import sys
parts = sys.stdin.read().strip().split()
stake, odds = float(parts[0]), int(parts[1])
if odds > 0:
    payout = stake + (stake * odds / 100)
else:
    payout = stake + (stake * 100 / abs(odds))
print(f'Expected payout: {payout:.2f}')"
```

## Output Rules

1. Always output a valid JSON object matching the schema
2. All odds must include American format (convert if needed)
3. Include decimal and implied probability for each leg
4. If a field cannot be extracted, set it to null — never guess
5. For parlays, each leg must be a separate entry in the legs array
6. Always include the raw_input field with the original text or "screenshot"
7. Potential payout must be calculated if not explicitly stated
8. Timestamp should be ISO 8601 format; use current time if not on the slip

## Error Handling

- If the input is ambiguous and multiple interpretations exist, present options and ask the user to clarify
- If the image is too blurry or cropped, ask for a clearer screenshot or text input
- If odds format is unrecognized, ask the user to specify (American, decimal, or fractional)
- If the bet type cannot be determined, default to "moneyline" for single selection and "parlay" for multiple selections
- Always show the parsed JSON and ask "Does this look right?" before passing to downstream skills

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-bet-slip-parser-skill/](https://agentbets.ai/guides/openclaw-bet-slip-parser-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
