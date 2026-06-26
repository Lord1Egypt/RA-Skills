# Safe Language for Arbitrage Analysis

This skill provides market structure analysis, not personalized financial, legal, or tax advice.

## Preferred Language

Use phrases like:
- "The structure appears locked if these assumptions hold"
- "Net edge after known costs is..."
- "The main failure mode is..."
- "This looks like soft lock rather than hard arbitrage"
- "The user still needs to verify..."

## Avoid

Do not say:
- "risk-free"
- "guaranteed profit"
- "you should put X dollars into this"
- "this is definitely safe"
- "the trade cannot lose"

## Escalate or slow down when

- the user wants to use borrowed money
- the opportunity depends on unclear regulation or tax treatment
- the user is treating positive EV as guaranteed payout
- the sizing request is far larger than the proven market depth

## Minimal Disclaimer Pattern

Use a short reminder in substantive analysis:

```text
This is arbitrage analysis, not a guarantee. Net outcome still depends on fills, fees, and settlement working as modeled.
```
