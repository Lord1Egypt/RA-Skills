---
name: Betting
slug: betting
version: 1.0.0
homepage: https://clawic.com/skills/betting
description: Evaluate betting opportunities with line shopping, bankroll discipline, market checks, and risk filters before any stake is placed.
changelog: Introduces the Clean Ticket Protocol, bankroll sizing rules, and fast rejection checks for weak bets.
metadata: {"clawdbot":{"emoji":"$","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/betting/"]}}
---

## When to Use

Betting questions involving sports, props, parlays, exchanges, or prediction-style tickets where price, edge, and stake size matter. Agent handles market normalization, implied probability math, line comparison, sizing discipline, and quick rejection of bad bets.

## Architecture

Memory lives in `~/betting/`. If `~/betting/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/betting/
├── memory.md        # Preferences, books, and activation rules
├── tickets.md       # Active or reviewed bets and follow-ups
├── market-notes.md  # Sports, books, and recurring edge notes
└── archive/         # Old tickets and retired observations
```

## Data Storage

- `~/betting/memory.md` stores activation rules, preferred sports, and user-stated constraints
- `~/betting/tickets.md` stores active or reviewed ticket notes when the user wants tracking
- `~/betting/market-notes.md` stores recurring market observations that improve future analysis
- `~/betting/archive/` stores older notes that no longer need to stay hot

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Clean Ticket Protocol | `workflow.md` |
| Market integrity checks | `market-checks.md` |
| Bankroll and sizing rules | `sizing.md` |
| Reusable ticket memo | `ticket-template.md` |
| Fast rejection list | `red-flags.md` |

## Requirements

- No account auth required
- No extra binaries required
- Live odds or injury news only when the user provides data or explicitly asks to fetch public information
- The user is responsible for legal age, jurisdiction, operator rules, and local compliance

## Clean Ticket Protocol

Use the full workflow in `workflow.md`. Every ticket should pass this order:

1. Define the exact market, book, line, price, stake, and settlement rule
2. Normalize odds and break-even probability with `sizing.md`
3. Check market integrity, limits, and void rules with `market-checks.md`
4. Run the fast rejection list in `red-flags.md`
5. Return an analysis memo using `ticket-template.md`: positive edge, reduce size, wait, or pass

## Core Rules

### 1. Price Comes Before Opinion
- Convert every bet into implied probability and break-even price before discussing narratives
- If the user only has a take and no number, build the number first or state that the edge is unproven

### 2. Markets Must Match Exactly
- Team names, alternate lines, overtime rules, void rules, and player participation terms must refer to the same economic outcome
- If two tickets settle differently, they cannot be compared as if they were the same bet

### 3. Size Last, Not First
- Do not discuss stake sizing until price, edge, limits, and failure modes are clear
- Use `sizing.md` to frame analytical stake ranges, capped units, or pass; default conservative when inputs are weak

### 4. Default to No Bet Under Unclear Edge
- Missing injury status, stale odds, unknown limits, or hand-wavy probability estimates should end in wait or pass
- Good betting analysis is often the discipline to reject action, not to force it

### 5. Parlays Need Independent Legs
- Treat correlated legs, same-game parlays, and market boosts as separate risk products, not free multiplier math
- If independence is unclear, label correlation risk and avoid fake expected value claims

### 6. Live Betting Needs Latency Awareness
- For live markets, ask when the quote was seen, what triggered the move, and whether the book can still be hit
- If latency or suspension likely invalidates the number, downgrade the ticket immediately

### 7. Output a Ticket Memo, Not Hype
- End with fair price, book price, edge estimate, maximum analytical size, kill conditions, and next action
- Never call a bet guaranteed, safe, lawful, or suitable for the user personally

## Legal and Responsible Use

- This skill provides informational analysis only, not legal, tax, financial, licensing, or gambling-compliance advice
- Do not help minors, self-excluded users, or users in prohibited jurisdictions place or access bets
- Do not suggest ways around KYC, AML, geo-blocking, self-exclusion, deposit limits, or operator rules
- Do not promote bonus abuse, affiliate links, referral deals, or language that frames gambling as income, investing, or debt recovery
- If legality, licensing, or operator compliance is unclear, stop at general information and tell the user to check local law or licensed counsel

## Market Lens

| Market Type | What to Check First | Typical Failure Mode |
|-------------|---------------------|----------------------|
| Side or moneyline | Closing context, overtime grading, price drift | Paying extra vig for a story everyone already knows |
| Spread or handicap | Key numbers, hooks, alternate lines | Comparing different point lines as if price alone mattered |
| Total | Pace, weather, lineup status, overtime rule | Using stale assumptions after lineup or weather news |
| Props | Minutes, role, book limits, stat source | Tiny limits or rules that void on limited participation |
| Parlays | Correlation, leg quality, hidden margin | Multiple bad prices packaged as one exciting ticket |
| Exchange or prediction market | Fees, liquidity, resolution language | Calling thin or ambiguous markets "edge" |

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Starting with "Who wins?" | Opinion without price does not tell whether the bet is good | Ask for line and odds first |
| Comparing +120 to +120 across books blindly | Rules and limits may differ | Match settlement and max stake before comparing |
| Using full Kelly on shaky estimates | Small model error can blow up bankroll | Downshift to fractional Kelly or flat-unit size |
| Treating promos as pure value | Hidden rollover, min odds, or stake caps distort edge | Separate hard edge from promo-only edge |
| Chasing after line movement | Late price often means the value is already gone | Reprice at current odds or pass |
| Ignoring correlation in parlays | Legs can move together and kill expected value | Price legs independently and label correlation risk |
| Confusing entertainment with edge | Action bias hides weak numbers | Be explicit when the ticket is only for fun |

## Scope

This skill ONLY:
- Analyzes bets, prices, and sizing discipline
- Stores user-stated preferences and notes in `~/betting/`
- Uses `workflow.md`, `market-checks.md`, `sizing.md`, `ticket-template.md`, and `red-flags.md` for repeatable analysis
- Identifies when the right answer is no bet, smaller size, or wait

This skill NEVER:
- Places bets, logs into books, or moves funds
- Stores login details, wallet recovery phrases, or account recovery data
- Helps bypass age, jurisdiction, KYC, AML, or self-exclusion controls
- Promotes profit, certainty, or personalized financial suitability
- Hides uncertainty when lines, rules, or data are incomplete

## Security & Privacy

**Data that leaves your machine:**
- None by default
- If the user explicitly asks for live public information, only the markets, teams, players, or books needed for that request

**Data that stays local:**
- Preferences, tickets, and notes in `~/betting/`

**This skill does NOT:**
- Store login details
- Read unrelated files
- Make undeclared network requests

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `decide` - structure tradeoffs and pass-or-proceed decisions without hype
- `legal` - tighten wording when the user asks about compliance, terms, or risk boundaries
- `pricing` - reason about price quality when the user needs cleaner expected value language
- `trader` - frame discipline, journaling, and risk control for repeated decision making

## Feedback

- If useful: `clawhub star betting`
- Stay updated: `clawhub sync`
