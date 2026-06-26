# Locked Spread Protocol

Use this protocol whenever an opportunity is being presented as arbitrage.

## Quick Start

1. Write the legs exactly
2. Convert everything into one base currency
3. Compute gross edge and net edge
4. Decide whether fills can be locked in sequence
5. Check settlement and venue rules
6. Classify the trade before discussing size

If any of those steps fails, downgrade the idea to watchlist or reject it.

## Step 1: Frame the Opportunity

Capture the opportunity in one line:

```text
Type | Venue A leg | Venue B leg | Optional leg C | Timestamp | Base currency
```

Then force these questions:
- Are the outcomes identical?
- Are the units identical?
- Are the expiries identical?
- Does one leg depend on transfer, borrow, or rebate assumptions?
- Is any part of the edge promotional rather than hard market pricing?

## Step 2: Normalize the Economics

Before calling it edge, convert:
- price
- fees
- spread
- gas or bridge cost
- borrow or funding
- FX
- shipping, handling, return risk, or fraud reserve when relevant

Use `calculator.md` for formulas. If the user gives only headline prices, say net edge is not known yet.

## Step 3: Check Lock Quality

Classify the structure immediately:

| Class | Meaning | Standard |
|-------|---------|----------|
| True lock | All legs can be completed without directional exposure | Rare and highest quality |
| Soft lock | The hedge exists but one leg may move or fail before completion | Needs sequence and kill rules |
| Inventory lock | One leg depends on inventory already owned or pre-funded | Capacity limited by inventory |
| Synthetic edge | Positive expectation but not guaranteed payout | Not arbitrage |

## Step 4: Build the Fill Sequence

The constrained leg determines the plan.

### Good sequence design
- Fill the smallest-capacity or fastest-moving leg first
- Pre-check capital, margin, and transfer path
- State the cancel condition for every incomplete sequence

### Bad sequence design
- Assume both legs will still be there after one fill
- Ignore queue priority or hidden max size
- Treat transfers as instant

## Step 5: Audit Settlement

Before size discussion, compare:
- resolution language
- delivery mechanism
- collateral type
- account restrictions
- void or cancel rules
- withdrawal limits
- payout timing

If the venues settle differently, the trade is not locked yet even if the labels look identical.

## Step 6: Size Against the Weakest Link

Realistic size comes from:
- shallowest order book or max bet
- slowest transfer route
- tightest collateral or borrow limit
- the leg with the highest failure cost

Always report:
- headline size
- realistic size
- what breaks first

## Step 7: Produce the Decision Memo

Use this output shape:

```markdown
## Decision
- Classification:
- Gross edge:
- Net edge:
- Realistic size:
- Required sequence:
- Open checks:
- Kill conditions:
- Recommendation: proceed | verify one item | watchlist | reject
```

## Fast Rejection Rules

Reject immediately if:
- the same outcome is not actually being hedged
- net edge disappears after costs
- one venue has unreliable settlement or blocked withdrawals
- depth exists only for trivial size
- the opportunity depends on stale quotes
- the trade is really just positive EV, not a locked spread

## Good Questions to Ask

- "What is the exact settlement rule on each leg?"
- "How much size is actually available at that price?"
- "Which cost is still unknown: fees, FX, transfer, borrow, or tax?"
- "Can both legs be completed without moving inventory first?"
- "If one leg fills and the other fails, what is the kill action?"
