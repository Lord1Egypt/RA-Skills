# Failure Cases (BAD) and Corrections

Each case shows a wrong behavior and the corrected version. These are the patterns the skill exists to prevent.

## 1. Fabricated / memory-recalled numbers
**Bad:**
> "Apple made about $383 billion last year with a 25% net margin." (Pulled from memory;
> no API call; no period/currency/citation.)

**Corrected:**
> "AAPL FY2024 revenue 391.0B USD; net margin 23.9% — FMP `/income-statement` + `/ratios`,
> annual, filingDate 2024-11-01, USD. As-of latest filing." (Only API values; cited.)

---

## 2. No period / no citation
**Bad:**
> "Microsoft's revenue is 245 billion." (Which period? Currency? Source?)

**Corrected:**
> "MSFT revenue 245.1B USD — FMP `/income-statement`, FY2024 (annual), filingDate 2024-07-30."

---

## 3. Retrying on 401 / suspended
**Bad:**
> Gets 401, immediately retries 5 times, burning calls, then says "still not working."

**Corrected:**
> "401 invalid API key — I won't retry; auth must be fixed. Please correct `FMP_API_KEY`."
> (Stops immediately; no key shown.)

---

## 4. Exposing the API key
**Bad:**
> "I called `https://financialmodelingprep.com/stable/quote?symbol=AAPL&apikey=sk_live_8f3a...`"

**Corrected:**
> "I called `/stable/quote?symbol=AAPL&apikey=YOUR_FMP_API_KEY`." (Key redacted to placeholder.)

---

## 5. Investment advice without disclaimer
**Bad:**
> "Tesla's DCF is below price, so it's overvalued — you should sell."

**Corrected:**
> "FMP DCF model estimate (210 USD) is below market price (245 USD) as of 2026-05-30. This
> is one model's estimate, not a recommendation. Informational only, not investment advice."

---

## 6. Ignoring currency / assuming USD
**Bad:**
> "SAP revenue was $34.2 billion." (It's reported in EUR.)

**Corrected:**
> "SAP FY2024 revenue 34.2B EUR (reportedCurrency=EUR; not converted) — FMP `/income-statement`."

---

## 7. Mixing annual and quarterly
**Bad:**
> "Revenue grew from 60B (Q2) to 245B (FY2024)." (Comparing a quarter to a full year.)

**Corrected:**
> Keep one basis: "Annual revenue: FY2023 211.9B → FY2024 245.1B USD (FMP `/income-statement`,
> annual)." Or compare like quarters, each labeled.

---

## 8. Calling an annual figure "TTM"
**Bad:**
> "TTM revenue is 245.1B." (That's the FY2024 annual figure.)

**Corrected:**
> "TTM revenue 250.7B USD = sum of the last 4 quarters (Q3'24+Q4'24+Q1'25+Q2'25), FMP
> `/income-statement` quarter. The FY2024 annual figure is separate (245.1B)."

---

## 9. Treating empty array as zero
**Bad:**
> Query returns `[]`. Agent: "Revenue is $0."

**Corrected:**
> "No data returned — likely a wrong symbol or plan coverage limit. Re-resolving the ticker."

---

## 10. Guessing the ticker
**Bad:**
> User: "Get Delta's numbers." Agent pulls `DAL` without asking, but the user meant a
> different "Delta" company.

**Corrected:**
> "‘Delta' is ambiguous — Delta Air Lines (DAL) or another? Searching returned several
> matches; please confirm which you mean before I pull data."

---

## 11. Wasteful calls / ignoring limits
**Bad:**
> Pulls the same profile and quote 6 times in one session; makes 3 single-symbol quote
> calls when one batch call would do.

**Corrected:**
> Resolves and caches the profile/quote once; batches `/quote?symbol=A,B,C`; right-sizes
> `limit`. Notes the free-tier ~250 calls/day budget.

---

## 12. Silent computation
**Bad:**
> "Net margin is 35%." (Computed in head, no inputs shown, not from API.)

**Corrected:**
> Prefer the API: "Net margin 35.9% — FMP `/ratios`, FY2024." Or if derived: "Derived net
> margin = netIncome 88.1B ÷ revenue 245.1B = 35.9% (inputs from FMP `/income-statement`,
> FY2024)."
