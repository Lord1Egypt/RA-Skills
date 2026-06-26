# Prompt: Grounded Financial Summary

## Purpose
Produce a financial summary that is strictly grounded in returned FMP data — every number cited, nothing invented, with currency, period, and freshness.

## Reusable template

```
Summarize the financials of {{symbol}} for {{periods}} ({{period_type}}).

Use ONLY data returned by FMP. Steps:
1. Confirm {{symbol}} via /profile (companyName, exchange, reportedCurrency).
2. Pull /income-statement?symbol={{symbol}}&period={{period_type}}&limit={{periods}}
   and /ratios (same params) for margins/returns.
3. For EVERY figure you state, include: value + units/currency + period + filingDate.
4. Label period_type ({{period_type}}); never mix annual and quarterly.
5. If you derive any value (e.g. growth %), show the two cited inputs and label it
   "derived". Prefer the API's own ratio fields over recomputing.
6. If a field is null/missing, write "not reported". If a call returns [], say
   "no data returned" and re-check the symbol — do NOT invent numbers.
7. End with: source (FMP), an as-of note, and "Informational only, not investment advice."

Do not recall any numbers from memory. Do not state a figure absent from the response.
```

## Variables
- `{{symbol}}` — confirmed ticker.
- `{{periods}}` — how many periods (e.g. 3).
- `{{period_type}}` — `annual` or `quarter`.

## Example
Input: `{{symbol}}=MSFT`, `{{periods}}=3`, `{{period_type}}=annual`
Output: a 3-row annual summary (revenue, net income, net margin) each cited with period + filingDate + USD, plus source/as-of/disclaimer.

## Bad
> "Microsoft makes around $240B in revenue with strong ~35% margins and is doing
> great." — no period, no filingDate, no currency stated explicitly, rounded-from-memory
> figures, vague, includes a soft endorsement.

## Good
> "MSFT (USD; FMP `/income-statement`, annual):
> FY2024 revenue 245.1B, net income 88.1B (net margin 35.9%, FMP `/ratios`),
> filingDate 2024-07-30. FY2023 revenue 211.9B... Source: FMP; data as-of latest
> filings, newer periods may exist. Informational only, not investment advice."
