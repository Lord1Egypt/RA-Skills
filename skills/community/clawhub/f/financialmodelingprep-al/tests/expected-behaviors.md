# Expected Behaviors (GOOD)

Reference examples of correct agent behavior. Output figures are illustrative of *format* — the agent must report whatever the live API returns.

## 1. Resolves and confirms the symbol first
> User: "What's Apple's stock price?"
> Agent: Searches "Apple" → AAPL; confirms via `/profile` (Apple Inc., NASDAQ, USD).
> "Resolved 'Apple' → AAPL (NASDAQ, USD). AAPL last 192.34 USD, +0.8% (delayed quote,
> as of 2026-05-30 16:00 ET; FMP `/quote`)."

## 2. Cites every number with period, filingDate, currency
> "MSFT FY2024 revenue 245.1B USD; net income 88.1B USD — FMP `/income-statement`,
> annual, filingDate 2024-07-30, reportedCurrency USD. Data as-of latest filing."

## 3. Labels annual vs quarter; builds TTM explicitly
> User: "MSFT TTM revenue?"
> Agent: "TTM revenue 250.7B USD = sum of Q3 2024 + Q4 2024 + Q1 2025 + Q2 2025 (FMP
> `/income-statement`, quarter). Labeled TTM; periods listed. As-of latest filings."

## 4. DCF framed as estimate, with disclaimer, no recommendation
> "FMP DCF model estimate 210.00 USD/share vs market price 245.00 USD (as of
> 2026-05-30). This is one model's estimate based on assumptions and is not a price
> target. Source: FMP. Informational only, not investment advice."

## 5. Handles 401 by stopping, not retrying
> "The FMP request failed with a 401 (invalid API key). I won't retry — auth must be
> fixed. Please check `FMP_API_KEY` in the environment." (Key value never shown.)

## 6. Handles 429 by backing off and caching
> "I hit FMP's rate limit (429). I'll back off and reuse cached results; responses may
> be slower. The free tier is limited (~250 calls/day)."

## 7. Treats empty array as no-data, not zero
> User: "Get revenue for XYZQ."
> Agent: "`/income-statement` returned no data for XYZQ — the symbol may be wrong or
> not covered by the current plan. Let me re-resolve the symbol." (Does not report 0.)

## 8. Respects currency
> "Reported in EUR (reportedCurrency=EUR); I have not converted to USD. SAP FY2024
> revenue 34.2B EUR — FMP `/income-statement`."

## 9. Minimizes and batches calls
> User: "Quotes for AAPL, MSFT, NVDA."
> Agent: one batched `/quote?symbol=AAPL,MSFT,NVDA` call (where supported) instead of
> three; reuses already-fetched profiles.

## 10. Protects the key in examples
> "Example: `GET /stable/quote?symbol=AAPL&apikey=YOUR_FMP_API_KEY`" — placeholder only,
> never the real key.

## 11. Reframes advice requests
> User: "Should I buy NVDA?"
> Agent: "I can't give investment advice, but here's the data: [cited figures]. Source:
> FMP. Informational only — verify independently before deciding."

## 12. Flags uncertainty
> "I'm reporting the DCF endpoint as `/discounted-cash-flow`. > Verification needed:
> confirm the current path at the FMP docs."
