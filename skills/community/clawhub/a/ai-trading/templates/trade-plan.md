# Trade plan - [TICKER]

**Prepared (ET):** [YYYY-MM-DD HH:MM ET]  **Status:** DRAFT - awaiting human approval

## Setup

| Field | Value |
| --- | --- |
| Symbol / exchange | |
| Side | long / short |
| Thesis (one sentence) | |
| Catalyst | |
| Time horizon | |
| Setup type | breakout / pullback / mean reversion / earnings / seasonal / other |

## Levels

| Level | Price | Note |
| --- | --- | --- |
| Entry | | |
| Stop (invalidation) | |
| Target 1 | | |
| Target 2 | | |
| Prior swing high / low | | |

## Size

| Field | Value |
| --- | --- |
| Account equity | |
| Risk per trade (%) | |
| Risk budget ($) | |
| Distance entry-to-stop (%) | |
| Size (shares) | |
| Position value | |
| Dollar risk | |
| R multiple to target | |
| Portfolio heat after trade | |
| Sector exposure after trade | |

Command used:

```bash
python3 scripts/portfolio_risk.py \
  --equity [EQUITY] --risk-pct [RISK] \
  --entry [ENTRY] --stop [STOP] --target [TARGET] \
  --sector [SECTOR] --open-positions positions.csv
```

## Pre-flight checklist

- [ ] Market open status checked (ET clock + holiday calendar)
- [ ] Earnings date checked
- [ ] Average dollar volume at least 20x the order size
- [ ] Stop is at a structural level, not an arbitrary percentage
- [ ] Size derived from the stop, not from conviction
- [ ] Single-position, sector, and heat caps respected
- [ ] Drawdown rules respected for the current account state
- [ ] Journal entry written before entry
- [ ] **Human approved and typed the order in their own broker**

## Exit plan

- [ ] Partial at [level] (___%)
- [ ] Partial at [level] (___%)
- [ ] Stop moved to breakeven only after [condition]
- [ ] Invalidation: [what proves the thesis wrong]

## Notes

[Anything unusual: halts, gaps, borrow availability, sector news, macro events
on the day.]

> This plan is research output for review. It is not investment advice, and no
> order is placed by this tool.
