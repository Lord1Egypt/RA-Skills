# Debt Payoff Math — Reference

## 1. The amortization model

Credit cards, personal loans, and auto loans accrue interest monthly:

```
monthly_interest = balance × (APR / 100) / 12
```

This monthly-rate convention (`APR/12`) is how revolving credit lines actually
compute finance charges in the US/EU. (Mortgages use the same convention on a
daily or monthly basis depending on the contract — this tool is not a mortgage
calculator.)

**Simulation loop, per month:**

1. Accrue interest on every live balance (rounded to the cent each month —
   this mirrors how issuers round).
2. Pool available cash = sum of minimums of *live* debts + user extra.
3. Pay each live debt its minimum, capped at the payoff amount.
4. Dead debts free their minimum — it stays in the pool.
5. All remaining pool cash goes to the strategy *target* debt, capped at its
   payoff amount; any overflow stays for next month.

All arithmetic is done in integer cents. Floating-point dollar math over
hundreds of months drifts by real money; cents don't.

## 2. Why freed minimums matter (the cascade)

Most naive plans (and many spreadsheet templates) keep paying the same extra
to the same debt forever. The actual engine of both avalanche and snowball is
**cascading**: when the Visa dies, its $105 minimum joins the attack on the
next debt. Compounding works against you while balances are high; the cascade
makes it work *for* you as debts fall.

For a $15,500 three-debt stack at $601/month total commitment, cascading is
the difference between 77 months (min-only) and 33 months (avalanche with
$150 extra). The $150 extra alone, without cascading, would take ~60 months.

## 3. Avalanche vs snowball — what the research says

- **Avalanche is mathematically optimal** for total interest. Proof sketch:
  at any moment, a dollar of payment reduces future interest most when
  applied to the highest-rate balance; the greedy allocation is optimal
  because interest accrual is linear in each balance.
- **Snowball wins on behavior.** Studies (e.g., Kellogg School / Harvard
  Business School working paper *"Small Victories: Creating Intrinsic
  Motivation in Task Completion"*, Kettle et al.) find people who pay off
  small accounts first are *more likely* to eventually clear all debt — the
  win closes the loop on motivation.
- **Practical rule:** if the interest gap between strategies is under ~$200
  or a couple of months, choose snowball; above that, choose avalanche —
  unless you know yourself to be a "quick wins" person, in which case the
  completed plan beats the abandoned optimal one every time. The tool prints
  this comparison explicitly.

## 4. Negative amortization

If `minimum < monthly interest` on a debt, the balance grows each month even
while paying — the debt is *unsolvable* by payment plan. Card issuers'
minimums (interest + 1% of principal, per CARD Act 2009) are designed to
avoid this, but near-limit balances at penalty APRs (29.99%+) can still cross
the line. The simulator detects non-convergence by month 600 and reports:

- the fact, loudly
- the minimum survivable payment (≈ highest single-debt interest + all other
  minimums)

Options at that point: consolidation loan, balance transfer, credit
counseling (nonprofit agencies negotiate minimums), or bankruptcy consult.

## 5. Modeling a consolidation loan / balance transfer

Model the proposed loan as a single debt with its APR and required payment:

```bash
python3 scripts/debt_payoff_planner.py --debt "Consolidated,15500,11.9,350" --budget 601
```

Compare **total interest** and **payoff month** against the avalanche row of
your current plan. Add origination/balance-transfer fees (typically 3–5%) to
the loan's interest total manually. A 0% APR teaser is only a win if the
balance is cleared before the teaser expires — run the plan and check the
balance at that month.

## 6. Minimum payment assumptions

- Statements change minimums as balances fall (often `interest + max(1% of
  balance, $25)`). This tool uses the **stated minimum, held flat**, which
  slightly overstates minimum-only payoff speed but is irrelevant for
  budget-driven plans.
- For budget mode, minimums only determine *allocation order*, not cash —
  results stay accurate.

## 7. What this tool does NOT do

- Investment-vs-payoff comparisons (needs assumed market returns).
- Mortgage/tax interplay, student-loan forgiveness programs (IBR/PSLF),
  origination math, or currency other than the one you type.
- Negotiate with creditors. (But the printed plan is a good script for a
  hardship-call: "I can commit $601/month.")

## 8. Formula summary

| Quantity | Formula |
|---|---|
| Monthly interest | `balance × APR/12` |
| Months to freedom | simulation (closed forms only exist for fixed payments) |
| Interest saved | `interest(min-only) − interest(strategy)` |
| Rule of 78 quick check | total interest ≈ `avg_balance × APR × years/2` |
