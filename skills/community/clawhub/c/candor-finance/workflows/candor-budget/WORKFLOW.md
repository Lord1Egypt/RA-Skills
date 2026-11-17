
# Budget

Show the person where their money actually goes, from their records, and
leave them with a saved budget built from that spending and fit to what they
said: their total, the amounts they named, and room for each goal. You keep
it current from then on, so they never manage category sliders.

## Workflow

Work through these steps in order:

```text
- [ ] 1. Open and read the saved budget, goals, and coverage
- [ ] 2. Show where the money goes
- [ ] 3. Hear what they want the budget to do
- [ ] 4. Draft the starting split from their records
- [ ] 5. Save it and say plainly what you saved
- [ ] 6. Adjust lines as they react
- [ ] 7. Check how the month is going
```

**1. Open and read.** `candor open` if this conversation has not opened
Candor yet, then:

```sh
candor budget context --reason "Read monthly income, spending by category, and any saved budget"
candor goals list --limit 100 --reason "Read goals the budget needs to pay for"
```

`budget context` carries the months it averaged over, whether each figure is
an estimate, the recurring bills and income, and the categories the records
use. Check the reported months and coverage: an account missing, a first
sync that has not reached back far, or an account kept by hand whose
statements stop early makes the averages low. From the
opening's `agent_context`, read what shapes a budget: what they protect
(`constraints_and_protected_resources`), how they fund the month and
reserves, especially on irregular income (`operating_plan`), and what they
are working toward (`objectives_and_time_horizons`).

**2. Show where the money goes.** Lead with income, spending, and what is
left each month, then the few categories that matter most. For a specific
period, or a category that looks wrong, read the transactions behind it:

```sh
candor transactions list --since START --until END --category CATEGORY --limit 100 --reason "Check what the dining category holds"
candor changes list --reason "Compare last month's spending and income with the month before"
```

Follow every continuation before you state a period total. Keep transfers
between their own accounts, card payments, and refunds out of spending; the
`cashflow_role` on each row says which is which. If a category reads wrong,
fix the records first with `candor-sort-transactions`, then come back.

**3. Hear what they want.** A total to stay under, an amount to save each
month, a category to rein in, or simply knowing where it goes. Someone who
only wanted the picture does not need a budget; do not save one nobody asked
for. A cleanup request is not a decision to change how they spend. When they
say a line is untouchable ("the kids' activities stay") or how they get
through lean months, save it as a note with its topic so later plans honor
it.

**4. Draft the starting split.** Observed spending is where it starts:

- Their total, and any amounts they named, win.
- Every other line comes from what the records show they spend.
- Each goal with a monthly pace gets a line, so the budget pays for it (the
  `candor-plan-a-goal` workflow sets the pace).
- Say where the draft does not add up: if lines plus goals exceed income, say
  by how much and which lines they could change.

`candor budget preview --file BUDGET.json --reason "Check the draft budget's totals"` computes a draft's totals and
unmatched lines without saving. Use it to check the numbers, not to ask
permission.

**5. Save it.** When they want a plan to hold to, or are working one out with
you, save the draft without waiting for a yes to each line. Put their own
words in `note` when they said something relevant:

```sh
candor budget create --file BUDGET.json --reason "Save the starting budget from their records"
```

Tell them it is a starting split from their records and that you will adjust
lines as they react. When the split leaves money each month that no line or
goal claims, say how much and ask what they want it to do; a goal they name
goes to `candor-plan-a-goal`, and its line comes back here.

**6. Adjust lines as they react.** Change only the lines that move; every
other line carries forward and the response lists what changed:

```sh
candor budget update --file BUDGET_UPDATE.json --reason "Raise groceries to what they actually spend"
```

```json
{
  "period": "2026-11",
  "currency": "USD",
  "lines": [
    { "category": "Groceries", "monthly_amount": "720.00", "line_type": "flexible" },
    { "category": "Emergency fund", "monthly_amount": "500.00", "line_type": "goal" }
  ],
  "note": "Groceries were never going to fit in $550 with two kids."
}
```

Use `budget create` again only when the plan itself is new.

**7. Check the month.** For "how am I doing this month":

```sh
candor budget status --period YYYY-MM --reason "Read this month's spending against the plan"
```

Status gives each line's spending, the month's pace to date
(`pace_expected_to_date`, `pace_variance_to_date`), unbudgeted categories,
and what is left in flexible and cushion lines. Show the panel when they want
to see it:

```sh
candor visual budget-status --period YYYY-MM --reason "Show this month's budget"
```

## How to answer

Lead with the one number that answers them, then a few bullets, then one line
on what you saved, then one question.

```text
You bring in about $5,200 a month and spend about $4,750, so roughly $450 is left.

- Rent and bills: $2,300, fixed.
- Groceries and dining: $1,050, and dining is $420 of it.
- Shopping: $610, up from $380 in the spring.

I saved a starting budget from the last three months, with $500 a month toward the emergency fund. To make that fit, shopping is set at $450.

Does $450 for shopping feel right, or should the fund line give a little instead?
```

## Gotchas

- Averages cover only the months and accounts Candor can see. Say which
  months, and say when an account or early history is missing.
- A page total covers that page. Follow every continuation before stating a
  month's total.
- Transfers between their own accounts, card payments, and refunds are not
  spending. Do not count both sides of a transfer, and net a refund only
  against the purchase it reverses.
- Unspent flexible or cushion money is not proof the cash is safe to spend.
  Bills due soon and goals still need it.
- An average is a baseline, not a statement of their values. Their reaction
  to the starting split tells you what to change.
- Use only amounts they gave or the records support. Do not round a category
  into a nicer number they never said.
- Keep scenarios you are only exploring apart from the saved budget, and
  label them as scenarios.

## Go deeper

- [Spending periods and capacity](references/spending-and-capacity.md):
  reconstructing a specific period, comparing months, and how much they can
  sustainably save when income is irregular.
