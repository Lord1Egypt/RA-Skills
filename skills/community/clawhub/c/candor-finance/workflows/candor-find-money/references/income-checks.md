# Income checks

Use when a paycheck, benefit, or client payment is late, smaller, missing, or
irregular.

## Build the baseline

```sh
candor coverage get --reason "Check the accounts and months the income check can see"
candor recurring list --direction inflow --cashflow-role income --limit 100 --reason "Read recurring income"
candor transactions list --since START --until END --direction inflow --limit 100 --reason "Read deposits around the expected payday"
candor changes list --domain income --limit 100 --reason "Compare recent income with the months before"
```

Search every account the money could land in and every name the payer uses.
Record the prior deposits: amounts, dates, account, cadence.

## Test before calling it missing or short

- A weekend or holiday shifted the posting date.
- The deposit is pending, or was reversed and reissued.
- It was split across two accounts.
- The payer's name changed in the description.
- It was a transfer, refund, reimbursement, interest, or a sale, not pay.
- The account changed, or coverage has a gap.

Quantify a change only from comparable deposits. A bank deposit is net cash;
it says nothing about gross pay, withholding, benefits, or hours, so do not
attribute a smaller check to any of them without a pay stub or the employer.

## Still not there

If the expected date has not passed, or coverage cannot confirm it, save a
note with a `watch` on the payer (`expect: deposit`) and a `revisit_at` for
the first day it should be visible. Contacting the employer, payer, or
benefits office is outside Candor and needs the person's okay.

## Irregular income

For gig, freelance, or commission pay, describe the observed range and the
months it covers, not an average presented as a salary. Planning on it
belongs in `candor-plan-a-goal`, with what the person expects.
