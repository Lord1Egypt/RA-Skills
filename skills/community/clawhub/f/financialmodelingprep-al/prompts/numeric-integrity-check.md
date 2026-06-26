# Prompt: Numeric Integrity Check

## Purpose
A self-audit pass: before sending an answer, verify that **every number cited matches an actual FMP API response**, flag any figure that doesn't, and remove or correct unsupported numbers. Catches fabrication, stale-memory figures, wrong units, and missing citations.

## Reusable template

```
Audit my draft answer about {{symbol}} for numeric integrity BEFORE sending.

For each numeric claim in the draft:
1. Find the exact API response field it came from (endpoint + field + period).
   - If you cannot point to a returned field, the number is UNSUPPORTED -> remove it
     or re-fetch it. Never keep a number you can't trace.
2. Check units and currency match the response (no USD assumption for non-USD).
3. Check the period label (annual/quarter/TTM) matches the row it came from.
4. Check any derived value shows its cited inputs and is labeled "derived".
5. Check null/missing fields are written as "not reported", and [] as "no data".
6. Check each figure has a citation: symbol + endpoint + period + filingDate + as-of.

Output:
- PASS if every number is traceable, correctly unit/currency/period-labeled, and cited.
- Otherwise list each problem figure, why it failed, and the corrected/removed version.
```

## Variables
- `{{symbol}}` — the ticker the draft is about.

## Example
Draft says: "AAPL net income was about 97 billion and P/E is roughly 30."
Audit:
- "97 billion" → trace to `/income-statement` FY2024 `netIncome` = 96.99B USD. Round/label and cite. (Was missing currency/period → fix.)
- "P/E roughly 30" → trace to `/key-metrics` or `/ratios` `peRatio` for a stated period. If not actually fetched → UNSUPPORTED → remove or fetch.
Result: FAIL until both are traced, unit/period-labeled, and cited.

## Bad
> Ships the draft as-is: "~97B net income, P/E ~30" with no endpoint, period, currency,
> and a P/E that was never actually retrieved.

## Good
> "netIncome 96.99B USD — AAPL `/income-statement` FY2024, filingDate 2024-11-01.
> P/E 31.2x — AAPL `/key-metrics` FY2024. Source: FMP, as-of latest filing." And if
> the P/E had not been fetched, it is removed rather than guessed.
