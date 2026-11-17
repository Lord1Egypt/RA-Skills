# Benefits and insurance

Medical spending in the records is a cue to look at benefits, not proof of
eligibility. Plan rules come from the plan document and current government
sources, with the plan year and date.

## HSA and FSA

```sh
candor accounts list --limit 100 --reason "Find benefit accounts"
candor transactions list --category CATEGORY --since START --until END --limit 100 --reason "Read health spending for the plan year"
```

Use the exact category names Candor returns. Check the plan year, account
type, contribution limit (name the year), carryover or grace period, and the
reimbursement deadline. Build a dated checklist only from rules the sources
support. Save a contribution plan the person settles on as a goal (`recorded`
unless contributions post to a visible account).

## A reimbursement that has not come

1. Get the receipt, explanation of benefits, or claim record: expected
   amount, payer, account, submission date, processing window.
2. Search for the credit conservatively:
   `candor transactions list --direction inflow --since START --until END --limit 100 --reason "Look for the benefit reimbursement"`.
3. Not due yet: save a note about the original charge with a deposit watch
   on the payer and a `revisit_at` at the end of the window.

## Insurance and plan-year cost

```sh
candor transactions list --merchant MERCHANT --since START --until END --limit 100 --reason "Read premiums and care costs for the plan year"
```

Separate premiums, out-of-pocket costs, reimbursements, and refunds.
Transactions never show coverage, deductible credit, or claim status; those
come from the policy and insurer.

To compare plans: get premiums, deductible, copays or coinsurance,
out-of-pocket maximum, network, and employer contribution from current
documents. Ask how much care they expect rather than inferring it. Model
low, expected, and high use: premium plus out-of-pocket for each, with
coverage differences listed apart.

## Renewal

Work back from the enrollment deadline to the last day to decide. Save a note
with the deadline, sources, missing facts, and what is left to decide, with
`revisit_at` a week or two before. Enrollment, changes, cancellations, and
claims happen outside Candor with the person's okay; you can file or call
for them if you have the tools.
