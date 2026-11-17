# Risk playbook

## Position sizing

```
shares = (equity * risk_pct/100) / (entry - stop)
```

- Risk per trade: **0.5%** of equity as the default, **1%** as the hard ceiling.
- Risk per trade is set by the **stop distance**, not by conviction. A wider
  stop means a smaller position.
- If the stop is more than ~8% away from the entry, the setup usually does not
  fit the account - skip it or find a better entry.
- Halve the size for overnight risk (earnings, binary announcements, thin
  names).

## R multiples

```
R = risk per share
target R = (target - entry) / R
```

- A setup worth taking at 1R is worth taking at 2R.
- Plan for partials: 50% at 1R, 25% at 2R, 25% trailing.
- Move the stop to breakeven only after a full R of profit, and only if the
  setup says so - moving stops early caps your upside.

## Portfolio heat

```
heat = sum(open risk in dollars) / equity
```

- Heat cap: **6%** of equity.
- Sector cap: **25%**.
- Single position cap: **10%**.
- Daily loss limit: **2%** of equity, then stop for the day.

These are defaults, not laws. A user may override them in writing; the script
reports violations either way so the override is explicit.

## Drawdown controls

| Drawdown | Action |
| --- | --- |
| -5% | Halve risk per trade |
| -10% | Risk per trade 0.25%, review every open position |
| -15% | Stop trading for the week, full strategy review |
| -20% | Back to paper only until a written review exists |

## Pre-trade checklist

- [ ] Thesis in one sentence, with the invalidation level
- [ ] Stop defined and the size derived from it
- [ ] Position size inside the single-position cap
- [ ] Sector and portfolio heat inside caps
- [ ] Earnings date checked (gap risk)
- [ ] Liquidity checked: average dollar volume above your order size by 20x
- [ ] Catalyst identified (or the trade is explicitly catalyst-free)
- [ ] Trade fits the current drawdown rules
- [ ] Written in the journal before entry

## Trade journal template

```
Date (ET)      : 2026-10-21
Symbol         : AAPL
Side / size    : long 40 shares
Entry / stop   : 182.40 / 178.10
R defined      : 0.75%
Target         : 195.00 (2.0R)
Thesis         : one sentence
Invalidation   : what proves this wrong
Result         : open / +1.2R / -1R
Screenshot     : path
Lesson         : one sentence
```

## Rules this skill will not break

- No order placement, ever. The tool produces a plan and stops.
- No leverage instructions beyond noting that leverage multiplies the risk
  rule - if a user wants leverage, the plan must still respect 0.5-1% of equity
  at risk.
- No averaging down into a losing position without a pre-written rule that
  says so.
- No "doubling down" language.
- No performance claims without a verifiable account statement, and even then
  only as a historical record with the period, the drawdown, and the fact that
  it is not a promise.
