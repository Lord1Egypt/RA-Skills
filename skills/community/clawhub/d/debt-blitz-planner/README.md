# Debt Blitz Planner 💳→🔥

**Which debt should you pay off first — and when exactly will you be free?**

The average household carrying credit card debt holds thousands of dollars
across multiple cards at 20%+ APR. Everyone tells you to try "avalanche"
(highest rate first) or "snowball" (smallest balance first), but nobody runs
*your actual numbers*. This tool does — month by month, in cents, with freed
minimums cascading into the next debt like they do in real payoff journeys.

## What it does

- Simulates **minimum-only**, **avalanche**, and **snowball** side by side
- Exact **debt-free date**, total interest, and dollars saved per strategy
- **Freed-minimum cascade**: dead debts' minimums re-route to the next target
- Extra-payment or fixed-total-budget modes
- Detects **negative amortization** (minimums that can never win) and prints
  the minimum survivable payment
- Per-debt payoff order, yearly milestones, CSV/JSON export

## Quick start

```bash
python3 scripts/debt_payoff_planner.py \
  --debt "Visa,4200,22.9,105" \
  --debt "Mastercard,1800,19.9,56" \
  --debt "Car loan,9500,6.5,290" \
  --extra 150
```

```
min-only  :  77 months (6.4 yr) | interest $5,584.10 | (baseline)
avalanche :  33 months (2.8 yr) | interest $2,424.64 | saved $3,159.46
snowball  :  34 months (2.8 yr) | interest $2,681.42 | saved $2,902.68

avalanche vs snowball: avalanche saves $256.78 and finishes 1 month earlier
```

See whether the gap between the two famous strategies is $50 (pick either)
or $2,000 (stick to avalanche) for *your* debts.

## Why it matters

- Paying minimums on $15,500 across three debts costs **$5,584 in interest
  over 6.4 years**. The same $451 plus $150 extra, properly cascaded, clears
  it in 2.8 years for **$2,425** — a $3,159 difference from ordering alone.
- Behavioral research (HBS "Small Victories") shows snowball's early wins
  increase completion rates; this tool shows you the exact dollar cost of
  that motivation so you can choose with open eyes.

## Files

- `SKILL.md` — agent-facing usage guide
- `scripts/debt_payoff_planner.py` — the planner (stdlib only, Python 3.9+)
- `scripts/test_debt_payoff_planner.py` — self-tests (`python3` it directly)
- `references/payoff-math.md` — amortization model, research, consolidation
  modeling, pitfalls

## Test

```bash
python3 scripts/test_debt_payoff_planner.py
```

MIT © 2026 Denis Voronin
