# US expense categorization basics

Reference for the Expense Categorizer skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Normalization rules

- Trim processor suffixes such as the card ending digits and the terminal ID.
- Map every raw vendor string to one clean name before matching rules.
- Keep the original descriptor in a separate column for the audit trail.
- Match duplicates on date, normalized vendor and amount together.
- Watch for the same vendor spelled two ways after a merger or a rebrand.

## Category hygiene

- Keep the chart of accounts small enough that people actually use it.
- Split a category only when you report on it.
- Separate recurring software from one-time equipment.
- Keep payments to 1099 vendors out of the operating expense list.
- Track sales tax collected separately from the revenue it was collected on.

## Tax caution

- Meals and entertainment carry a federal deduction limit, so flag them.
- Mileage uses the IRS annual rate, not a number someone remembers.
- An owner confirms any deduction position with an accountant before it is claimed.
- A categorizer sorts transactions; it does not decide what is deductible.
