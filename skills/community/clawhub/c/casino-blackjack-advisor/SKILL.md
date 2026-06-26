---
name: casino-blackjack-advisor
description: Returns the mathematically optimal blackjack action (HIT/STAND/DOUBLE/SPLIT/SURRENDER) for any hand using perfect basic strategy (6 decks, S17). Reduces house edge to 0.3%. Pass player cards and dealer upcard, get instant JSON decision.
metadata:
  author: "Mibayy"
  version: "1.0.0"
  displayName: "Blackjack Basic Strategy Advisor"
  difficulty: "beginner"
  type: "automaton"
---

# Blackjack Basic Strategy Advisor

Perfect basic strategy for 6-deck blackjack (dealer stands on soft 17). Covers all hand types: hard, soft, and pairs. Reduces house edge to **0.3%** — the lowest achievable without card counting.

## Usage

```bash
# Single hand (outputs JSON)
python blackjack_advisor.py "8,6" "7"
python blackjack_advisor.py "A,7" "6"
python blackjack_advisor.py "9,9" "6"

# Demo (runs 7 test hands)
python blackjack_advisor.py
```

## Output

```json
{
  "action": "DOUBLE",
  "explain": "Double ta mise et prends UNE seule carte.",
  "hand_type": "soft 18",
  "total": 18,
  "confidence": "optimal"
}
```

Actions: `HIT` | `STAND` | `DOUBLE` | `SPLIT` | `SURRENDER` | `BLACKJACK`

## Strategy covered

- **Hard hands** (4–21): full matrix vs all dealer upcards 2–A
- **Soft hands** (A+2 through A+9): double/hit/stand decisions
- **Pairs** (2–A): split vs no-split vs double

## Rules assumed

- 6 decks
- Dealer stands on soft 17 (S17)
- Double after split allowed
- Surrender available (late surrender)

## No configuration required

No env vars, no API keys, no dependencies beyond Python stdlib.

## Why this matters

Playing slots or guessing costs 4–40x more per dollar wagered than using basic strategy. On a $5,000 wagering requirement: slots cost ~$200, basic strategy costs ~$15.
