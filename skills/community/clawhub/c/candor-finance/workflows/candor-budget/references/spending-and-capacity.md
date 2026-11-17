# Spending periods and capacity

## Reconstruct a period

1. Settle the period, the accounts included, and whether they want cash in
   and out or income against expenses.
2. Check coverage before any arithmetic:

```sh
candor coverage get --reason "Check the accounts and months the period can cover"
candor transactions list --since START --until END --limit 100 --reason "Read the period's transactions"
```

3. Drill into a large or unclear category with its own bounded read:

```sh
candor transactions list --category CATEGORY --since START --until END --limit 100 --reason "Check what this category holds"
```

4. Sort the rows by `cashflow_role`: income, expense, transfer, debt
   payment, refund. Only expense counts as spending and only income as
   income. Count one-time items apart from the monthly pattern.
5. Report totals with the months and accounts they cover and anything left
   out. Keep currencies apart; never combine them at an unstated rate.

Follow every `next_actions` continuation before you call a total complete.

## Compare months

```sh
candor changes list --since START --until END --comparison-since PRIOR_START --comparison-until PRIOR_END --reason "Compare spending this quarter with last quarter"
```

With no dates it compares the last complete calendar month with the one
before and states both ranges. These are recorded totals, not rates: a
five-week month is not a raise in spending. When history is incomplete,
Candor withholds the comparison; say so instead of building one by hand.

## How much they can save

1. Start from the reconstructed monthly figures, and compare several months
   when pay or spending is seasonal or irregular.
2. Read what is already committed:

```sh
candor recurring list --limit 100 --reason "Read bills and income the plan must carry"
candor debts list --reason "Read debt minimums the plan must carry"
candor budget context --reason "Compare the saved budget with what they spend"
candor goals list --limit 100 --reason "Read goals already competing for the money"
```

3. Give a usual month and a lean month: which income, bills, and one-time
   items differ between them, and what is left in each after goals.
4. A capacity estimate is a scenario until they settle on a plan. When they
   do, save it as a budget, or as a goal pace through `candor-plan-a-goal`.

## Irregular income

Gig, commission, seasonal, or self-employed pay makes a monthly average
misleading. Use the lean month for the budget's base, and treat the rest as
money to assign when it lands (a goal, the cushion, debt). Ask how they are
paid when the records cannot tell you, and keep their answer as a note tagged
`current_financial_situation`.
