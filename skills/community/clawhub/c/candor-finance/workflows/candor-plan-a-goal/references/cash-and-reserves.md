# Cash, reserves, and spare money

## How much is really available

```sh
candor liquidity summary --reason "Read visible cash and what is owed"
candor accounts list --limit 100 --reason "Check which accounts hold the cash"
candor recurring list --due-within 45 --limit 100 --reason "Read bills due before the cash is free"
candor budget status --period YYYY-MM --reason "Read budget lines this month still needs"
candor goals list --limit 100 --reason "Read money already set toward goals"
```

Available = visible cash minus what it still has to cover: bills due soon,
the rest of this month's budget, and money other goals already hold. Count
each commitment once; a bill or a goal contribution that already has a budget
line is inside the budget figure, not a second subtraction. Leave out cash that is
restricted, pending, someone else's, or for a business. One good month is not
a raise. If an account's role is wrong (a joint or business account counted as
personal), fix it with `candor accounts policy set --file POLICY_FILE --reason "Set the account role the person described"` when
the person says so.

## Emergency fund

Ask what it should cover (job loss, a car repair, a gap between gigs) rather
than reciting a number of months. Read monthly spending from Candor; the
`cover` measure counts months of that spending across the accounts they would
live on, and an account can back several goals this way. Save it as a
`reserve` goal with `cover` (and `target_months` when they think in months).

## Idle cash and interest rates

Read each deposit account's rate from `account_terms`. For a better rate,
look up current offers from the bank's own page, and keep the date you looked.
Compare after fees, minimums, access limits, and deposit insurance. Do not
compare an insured savings account with an investment as if they carry the
same risk. Save a changing rate you found only as a note with a near-term
`revisit_at`.

## What to do with extra money

List only the real options, with the current course: keep it liquid, fund a
saved goal, pay down a debt with a known rate, hold it for a known bill.
Compare amount, timing, whether it can be undone, liquidity, the verified
return or avoided interest, and effort. If one option fits what the person
told you, recommend it and say what would change your answer. If a missing
preference decides it, ask that one question.

Moving money is an action outside Candor and needs their okay.
