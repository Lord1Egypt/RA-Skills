# Investments and retirement

## What the records can show

```sh
candor accounts list --limit 100 --reason "Find investment and retirement accounts"
candor holdings list --limit 100 --reason "Read visible holdings"
candor portfolio snapshot --reason "Read investment balances and allocation"
candor data query investment_transactions --limit 100 --reason "Read investment activity"
```

- Current value is `market_value` for a quoted holding, `value` otherwise.
  `market_price_as_of` says how fresh the quote is; off hours it is the prior
  close. An account's `balance_basis` says whether its balance is
  market-valued.
- A holding with no symbol, or imported without `market: US`, keeps its
  source value and does not move with quotes.
- Use only `status: active` investment activity; removed rows are withdrawn
  evidence. `activity_kind` is Candor's shared meaning; `type` and `subtype`
  are the source's. A reinvestment is not an outside contribution.
- `investment_transactions` takes only cursor and limit: page through it and
  filter by account and date yourself. Follow every continuation before you
  call a year-to-date total complete, and check the connection's history
  reaches back that far.

Coverage notes: Plaid refreshes about 90 days of overlap and reconciles its
24-month window about monthly; a failed refresh keeps the last good window.
Read `latest_attempt_status` apart from `last_successful_sync_at`. When
coverage says `refresh_failed`, `candor sync refresh --force --reason "Resume the staged investment refresh"`
resumes it; repeating it cannot fix a bad record.

## Value over time

```sh
candor metrics history --metric investment_value --range 3m --reason "Review investment value history"
candor data query holding_valuations --holding-id HOLDING_ID --limit 100 --reason "Read one holding's daily values"
candor changes list --domain investments --reason "Review position changes"
```

A period figure is value change, not return: contributions, withdrawals,
dividends, and sales are inside it until activity is reconciled. Days with
`price_source: observed` are flat source values, not market moves. Daily
holding valuations start with the first nightly valuation after the account
joined and are never backfilled. Show the picture with
`candor visual investments --reason "Show investment value and allocation"`.

## Fees, cash drag, concentration

1. Confirm the exact fund share class or advisory arrangement.
2. Look up current expense ratios, advisory and platform fees from the
   prospectus or fee schedule; keep publisher, date, and which holding it
   applies to.
3. Estimate yearly cost from visible value and label it an estimate; do not
   add overlapping fees.
4. Weights by account, holding, and currency are facts. Suitability, risk
   fit, and a target allocation are not in the records: ask about goals, time
   horizon, and holdings elsewhere before judging fit.

A fee saving the person acts on is an impact worth recording (see the notes
reference in `candor-finance`). Any trade, rebalance, or transfer happens
outside Candor with their okay.

## Employer match and contributions

- A connected plan shows contributions in investment activity; otherwise
  they live on paystubs. Bank deposits show net pay, not contributions.
- Get the match formula, eligibility, vesting, and true-up from the plan
  document or HR. A deposit pattern cannot establish a formula, and an
  employer deposit is match only when labeled or reconciled to a paystub.
- With the formula and pay per period, compute: contribution at the current
  rate, match earned, maximum match, and match left unclaimed this year
  (capped by remaining room). Show the arithmetic.
- Contribution limits are external and yearly: name the tax year and the
  source, and separate the employee limit from the combined limit. 401(k) and
  403(b) deferrals share one limit across plans, including a former
  employer's this year; a governmental 457(b) has its own. Without
  year-to-date deferrals from every plan sharing the limit, do not state
  remaining room.
- Payroll facts (rate, YTD) have no typed record: keep them in a note with
  the paystub date and re-check from a fresh paystub before relying on them.
  Statement balances and holdings can be imported (`candor-add-records`).
- Save a contribution plan the person settles on as a goal: `tagged` on a
  contribution tag when contributions post to a visible account, otherwise
  `recorded`.
- After they change their election, save a note with the baseline and a
  `revisit_at` on the first paycheck that should show it; the gap is closed
  only when a paystub or contribution record shows the new amount.
