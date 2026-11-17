---
name: debt-blitz-planner
description: "Compare debt payoff strategies with real amortization math: avalanche (highest APR first), snowball (smallest balance first), and minimum-only baseline. Shows exact debt-free dates, total interest paid, interest saved, and freed-minimum cascading. Use when the user has credit card debt, student loans, or multiple debts and asks which to pay first, how long until debt-free, or whether to pay off small balances or high rates first."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [finance, debt, credit-cards, loans, amortization, payoff, budgeting]
---

# Debt Blitz Planner 💳→🔥

Compute **exactly when you will be debt-free** and which payoff order saves the most money. Turns a pile of minimum payments into a concrete month-by-month battle plan using real amortization math — not hand-waving.

## Overview

The average household with credit card debt carries **over $7,000 at ~20%+ APR** and pays thousands in interest by just submitting minimums. The two famous strategies are:

- **Avalanche**: pay minimums everywhere, throw every spare cent at the **highest APR** debt. Mathematically optimal — minimizes total interest.
- **Snowball**: attack the **smallest balance** first. Costs slightly more interest but delivers quick wins that keep people motivated.

Everyone asks "which is right for me?" — the honest answer is **run both and look at the numbers**: how many months and how many dollars actually separate them for *your* debts. Usually the gap is smaller than people assume, and seeing that is genuinely decision-changing.

`scripts/debt_payoff_planner.py` implements a full month-by-month simulation:

- Correct per-month interest accrual (`balance × APR / 12`)
- **Freed-minimum cascading**: when a debt dies, its minimum is re-routed to the next target (the mechanism that makes these plans accelerate)
- Extra-payment scenarios (`--extra 200`) and total monthly budget mode
- Negative-amortization detection (your minimums don't even cover interest — flagged loudly with the minimum survivable payment)
- Side-by-side comparison of all strategies + per-debt payoff order + yearly milestones

## When to Use

- "I have 3 credit cards and a car loan — which should I pay off first?"
- "How long will it take to be debt-free if I pay $X extra per month?"
- "Avalanche vs snowball — what's the actual difference for my debts?"
- "I can put $800/month total toward debt. When's my debt-free date?"
- "Should I take a consolidation loan at Y%?" → run baseline, then model the loan as a single debt and compare

**Don't use for:** mortgage refinancing decisions with tax implications, investment-vs-payoff analysis (needs expected-return assumptions), or business accounting. This is personal-consumer-debt math.

## How It Works — Steps

1. **Gather debts**: name, current balance, APR (%, annual), minimum monthly payment. Find them on statements.
2. **Run the comparison** (all three strategies at once):
   ```bash
   python3 scripts/debt_payoff_planner.py \
     --debt "Visa,4200,22.9,105" \
     --debt "Mastercard,1800,19.9,56" \
     --debt "Car loan,9500,6.5,290" \
     --extra 150
   ```
3. **Read the table**: months to freedom, total interest, savings vs minimum-only.
4. **Model scenarios**: bump `--extra` and watch the debt-free date move — every extra $100/month at the start is worth several months at the end.
5. **Get the schedule** with `--json` or `--csv` for a spreadsheet; `--schedule` prints yearly milestones.

## Strategy Logic (exact rules)

1. Every month: interest accrues on every live balance.
2. Every debt receives its minimum payment (capped at payoff amount).
3. Freed minimums from dead debts + the user's `--extra` go to the **target** debt:
   - avalanche target = live debt with **max APR**
   - snowball target = live debt with **min balance** (ties broken by APR)
   - min-only = no target; extra never applied (baseline)
4. A debt is dead when balance ≤ 0; overflow payment rolls to the next month's pool.
5. Simulation caps at 600 months (50 years) — if hit, minimums are unsustainable.

## Worked Example

```
Debts: Visa $4,200 @ 22.9% (min $105)
       MC   $1,800 @ 19.9% (min $56)
       Car  $9,500 @  6.5% (min $290)
Extra: $150/month

min-only  : 77 months, $5,584 interest  (baseline)
avalanche : 33 months, $2,425 interest  (saves $3,159)
snowball  : 34 months, $2,681 interest  (saves $2,903)
```
Avalanche wins by ~$257 and 1 month here — small enough that snowball's psychological win may be worth it. **That insight is the product.**

## Common Pitfalls

1. **Minimum payments that don't cover interest** (balance grows forever). The tool detects this and prints the minimum survivable total payment — do not ignore it.
2. **Forgetting freed minimums.** Snowball/avalanche plans fail on paper when people keep paying dead debts' minimums to "be safe". Re-route them (the script does).
3. **APR vs APY confusion.** Statements show APR; the script uses monthly = APR/12 (standard for credit cards).
4. **Comparing strategies without the baseline.** Always include min-only — "saves $1,251" only means something relative to it.
5. **Paying extra while carrying no emergency fund.** A mathematical note the tool can't make for you: a $500 surprise on a maxed card can undo months of progress.
6. **Rounding drift.** The script computes in cents and rounds the display only; don't hand-replicate in a spreadsheet with floats.

## Verification Checklist

- [ ] Sum of minimums ≤ monthly budget (script errors otherwise)
- [ ] No debt shows negative amortization warning
- [ ] Avalanche interest ≤ snowball interest ≤ min-only interest (sanity invariant)
- [ ] Final month in schedule has all balances at 0
- [ ] Payoff order listed matches strategy (avalanche = APR descending; snowball = balance ascending)

## One-Shot Recipes

**Debt-free date on a fixed budget:**
```bash
python3 scripts/debt_payoff_planner.py --debt "Card1,6100,24.99,182" \
  --debt "Card2,2400,18.24,60" --budget 750
```

**Is the consolidation loan worth it?** Run baseline, then:
```bash
python3 scripts/debt_payoff_planner.py --debt "Consolidated,8500,11.9,283" --budget 750
```
Compare total interest + payoff date; add any loan fees manually.

**Export for a spreadsheet:**
```bash
python3 scripts/debt_payoff_planner.py --debt "Visa,4200,22.9,105" --csv plan.csv
```
