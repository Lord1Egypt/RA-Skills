---
name: Arbitrage
slug: arbitrage
version: 1.0.0
homepage: https://clawic.com/skills/arbitrage
description: Find, validate, and compare arbitrage opportunities across markets with fee-aware math, execution sequencing, and failure-mode checks.
changelog: Adds the Locked Spread Protocol, fee-aware calculators, and venue validation playbooks for cleaner arbitrage analysis.
metadata: {"clawdbot":{"emoji":"$","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/arbitrage/"]}}
---

## When to Use

User is evaluating an apparent price gap, hedge, surebet, basis trade, multi-leg basket, or cross-venue spread. Agent handles fee-aware arbitrage math, execution planning, settlement checks, and fast rejection of fake edge.

## Architecture

Memory lives in `~/arbitrage/`. If `~/arbitrage/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/arbitrage/
├── memory.md         # Preferences, constraints, and activation rules
├── opportunities.md  # Active ideas, status, and next checks
├── venue-notes.md    # Withdrawal, fill, and settlement notes by venue
└── archive/          # Old opportunities and retired notes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Locked Spread Protocol | `workflow.md` |
| Fee-aware formulas | `calculator.md` |
| Venue and settlement checks | `venue-checks.md` |
| Scenario playbooks | `playbooks.md` |
| Safe language and disclaimers | `legal.md` |

## Requirements

- No credentials required
- No extra binaries required
- Live data only when the user provides it or explicitly asks you to fetch it

## Locked Spread Protocol

Use the full protocol in `workflow.md`. At minimum, every opportunity passes these gates:

1. Confirm the legs really describe the same economic outcome
2. Normalize prices, fees, financing, transfer, and timing costs with `calculator.md`
3. Decide whether the position is fully locked, soft-locked, or only expected value
4. Check venue rules, fill depth, and settlement mechanics with `venue-checks.md`
5. Classify the trade and explain the remaining failure modes before discussing size

## Core Rules

### 1. Define the Exact Arbitrage
- Write each leg with venue, instrument, side, price, size limit, timestamp, and settlement rule
- If the legs do not resolve to the same outcome, currency, or unit of risk, it is not arbitrage yet

### 2. Normalize Every Dollar of Friction
- Always include fees, spread, gas, borrow, financing, FX, transfer, and any user-stated tax or settlement drag
- Use `calculator.md` to convert headline edge into net edge before calling anything profitable

### 3. Sequence for Fill Risk, Not for Hope
- Identify the constrained leg first: shallow book, max bet, slow venue, borrow dependence, or promo cap
- Prefer structures that can be locked immediately; otherwise label them soft lock or directional exposure

### 4. Treat Settlement as First-Class Risk
- Compare rules, expiry, void conditions, collateral type, withdrawal limits, transfer time, and counterparty exposure
- Use `venue-checks.md` and `playbooks.md` whenever the opportunity crosses venues or products

### 5. Reject Fake Edge Fast
- Stale quotes, hidden min or max size, promo-only pricing, mismatched markets, and low depth are default failure modes
- If the residual risk is execution, model drift, or rule mismatch rather than a true lock, say so explicitly

### 6. Output a Decision Memo, Not Hype
- Return the classification, net edge, max realistic size, required sequence, open checks, and kill conditions
- Good output ends with a clear next action: proceed, verify one item, downgrade to watchlist, or reject

### 7. Analysis Never Becomes Advice
- Never call a trade risk-free, guaranteed, or suitable for the user personally
- Provide analysis and trade structure only; do not execute trades or give portfolio-specific recommendations

## Opportunity Types

| Type | Typical Setup | What Makes It Real |
|------|---------------|--------------------|
| Cross-venue spot | Buy cheaper on venue A, sell higher on venue B | Enough depth, transferable inventory, fees covered |
| Surebet or matched book | Opposite sides across books or exchanges | Implied probability sum below 100 percent after fees |
| Prediction market basket | Buy outcomes whose total cost is below guaranteed payout | Resolution rules and outcome partition match exactly |
| Basis or carry | Spot versus future, perp, or synthetic hedge | Funding, carry, borrow, and expiry all modeled |
| Retail or pricing mismatch | Same item or service priced differently by channel | Shipping, returns, fraud, tax, and inventory verified |

## Arbitrage Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Matching names instead of resolution rules | Similar labels can settle differently | Compare exact payout and settlement language |
| Using top-of-book only | Apparent edge disappears after first fill | Calculate size against real depth |
| Ignoring transfer time | Edge can vanish before hedge arrives | Price latency as a cost, not a note |
| Forgetting limits and KYC | One leg fills, the other is capped or blocked | Check limits, region, and account status first |
| Treating rebates as guaranteed | Rebates or promos can change net economics | Separate hard edge from conditional incentives |
| Mixing currencies loosely | FX and spread can erase edge | Convert every leg into one base currency |
| Calling EV arbitrage | Positive EV is not a locked spread | Label it expected value, not arbitrage |
| Overstating size | The shallowest leg defines realistic capacity | Size to the weakest link |

## Scope

This skill ONLY:
- Analyzes arbitrage structures and net economics
- Stores user-stated constraints in `~/arbitrage/`
- Uses its own auxiliary files for formulas, venue checks, and playbooks
- References timestamps and missing inputs when data may be stale

This skill NEVER:
- Executes real trades, transfers, or withdrawals
- Uses exchange keys, broker credentials, or wallet secrets
- Calls an opportunity risk-free or guaranteed
- Gives personalized financial, tax, or legal advice

## Security & Privacy

**Data that leaves your machine:**
- None by default
- If the user explicitly asks for live public data, only the requested symbols, markets, or venue pages needed for the analysis

**Data that stays local:**
- Preferences, venue notes, and working opportunity notes in `~/arbitrage/`

**This skill does NOT:**
- Store credentials
- Read unrelated files
- Make undeclared network requests

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `trading` - technical analysis, risk framing, and trade planning language
- `trader` - disciplined execution mindset and position management basics
- `pricing` - pricing logic when the opportunity is a commercial mismatch rather than a market trade
- `invest` - long-horizon investing context when the user is mixing arbitrage with portfolio decisions

## Feedback

- If useful: `clawhub star arbitrage`
- Stay updated: `clawhub sync`
