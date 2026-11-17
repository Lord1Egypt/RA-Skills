# Cash flow ahead

Use for "can I afford it", "will I make it to payday", runway, or a planned
big expense. The answer is usually the lowest balance ahead and its date.

## Build the baseline

```sh
candor coverage get --reason "Check balances and bills are current enough to project"
candor balances list --limit 50 --reason "Read starting balances"
candor recurring list --limit 100 --reason "Read bills and income in the horizon"
candor transactions list --since TODAY --until HORIZON_END --limit 100 --reason "Include pending and future-dated transactions"
candor notes list --after HORIZON_START_ISO --before HORIZON_END_ISO --limit 100 --reason "Recover expected one-offs saved earlier"
```

Notes take ISO timestamps (`2026-11-01T00:00:00.000Z`); transactions take
plain dates. Follow every continuation: a missed bill always makes the
projection look better than it is. If balances cover fewer accounts than
exist, say so before projecting.

1. Start from current balances, per account.
2. Add only `active` recurring series on their `predicted_next_date`.
   Candidates are not commitments. Do not rebuild a next date from the last
   payment; a null date is undated.
3. Take income from recurring inflows. Do not average past deposits into
   future income unless the person confirms it.
4. Count a bill already showing as pending once. Card payments and transfers
   move one account's balance even though they net out for the household.
5. Keep everyday spending as a stated range, apart from committed bills.
6. Report the lowest balance, its date, and the bills that drive it.

## A planned expense or a scenario

Get the amount, date, and account if any is missing. Re-run with the change
and compare the two low points; say plainly if it creates a shortfall. Save
the expense as a note with `revisit_at` on its date so later projections
include it. A scenario becomes the plan only when the person settles on it, as
a goal or budget change.

## Runway

Months of runway = cash they would live on divided by monthly spending. Use
the `cover` measure's figure when a reserve goal exists. Say what the figure
leaves out (irregular income, annual bills).
