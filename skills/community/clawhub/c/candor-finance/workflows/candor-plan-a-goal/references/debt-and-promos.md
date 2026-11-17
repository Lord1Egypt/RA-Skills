# Debt payoff and promo rates

## Read the debts

```sh
candor debts list --reason "Read balances, rates, minimums, and due dates"
candor data query account_terms --limit 100 --reason "Read card and loan terms with their sources"
candor transactions list --since START --until END --cashflow-role debt_payment --limit 100 --reason "Read the payments actually made"
```

`debts list` carries each balance with its effective APR, minimum, and due
date where known; `account_terms` says where each value came from and flags
conflicts or stale values. A card that shows nothing left unpaid and charged
no interest is not costing anything, whatever its rate.

## Fill missing terms

Never estimate a rate or minimum from transactions.

- From a statement or the lender's site: import it as a curated record (the
  `candor-add-records` workflow) so it joins the account's term history.
- From the person ("my card is 24.99%"): save it as an assertion with their
  words in `note`, preview first:

```sh
candor account-terms assertion preview --file ASSERTION.json --reason "Check the rate the person gave"
candor account-terms assertion set --file ASSERTION.json --reason "Save the rate the person gave"
```

Revert with `candor account-terms assertion revert ACCOUNT_IDENTITY_ID FIELD --reason "Drop the rate the person gave now that the statement shows it"`
when better evidence replaces it.

## Model the payoff

1. Model the current course (what they pay now) and at least one
   alternative: highest rate first (least interest), smallest balance first
   (fastest wins), or a fixed monthly amount.
2. State the assumptions: starting balances and their date, rates, payment
   amount and timing, fees, promo expiry, and that new charges are left out.
3. Show the payoff date, total interest, and the monthly cash each path
   needs. Show what happens if the payment drops or a rate rises.
4. Recommend an order for this person's cash and goals, and say why. Save
   the plan as a `debt_reduction` goal with a `debt` measure over the cards or
   loans it pays down.

## Promo deadlines

For a 0% or deferred-interest balance, confirm from the statement or issuer:
the balance covered, the end date, what happens after (deferred interest can
charge back to the start), the required payments, and what voids the promo.
Store the end date as an account term (import or assertion) so the opening
raises it 30 days ahead. Work back from the deadline with a few days of
processing buffer, and give the monthly amount that clears it in time.

A payment, balance transfer, refinance, or application is an action outside
Candor: do it only with the person's okay, through your own tools if you have
them, or give them the exact steps.
