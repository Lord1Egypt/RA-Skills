# FMP Best Practices (Distilled Checklist)

A condensed checklist. The full rationale lives in `SKILL.md`.

## Symbol resolution
- Resolve company name → ticker via `/search-name` or `/search-symbol` before any data pull.
- Confirm with `/profile` (exchange, currency, company name) match the user's intent.
- If multiple plausible matches, ask the user or state which you chose and why.
- Carry one resolved `symbol` through the whole task; don't guess.

## Period choice
- Always set `period` explicitly: `annual` or `quarter`.
- Label every figure with its period; never mix annual and quarterly unlabeled.
- TTM = sum of the last 4 quarters (or a TTM endpoint if available) — label it and list the periods used.
- Right-size `limit` to the periods you actually need.

## Numeric integrity
- Report only numbers the API returned. Never fabricate or recall from memory.
- Don't silently compute; if you derive a value, show inputs and label "derived" — prefer the API's own ratio/metric field.
- Show units and `reportedCurrency` on every figure; state scale (M/B).
- Treat `null`/missing as "not reported", and `[]` as "no data" (not zero).

## Citation & freshness
- Cite value + units/currency + symbol + endpoint + period + filingDate + as-of note.
- State that data is as-of the latest filing/timestamp and newer data may exist.
- Distinguish facts (API) from interpretation (yours).

## Caching & limits
- Free tier ~250 calls/day, US-only — treat calls as scarce. (Verification needed: confirm limits.)
- Cache and reuse profiles/quotes within a session.
- Batch multi-symbol quotes; avoid redundant pulls; plan the minimal endpoint set.
- On 429: back off and cache. On 401/suspended: stop, don't retry.

## Compliance
- Not investment advice — include a disclaimer for valuations/comparisons.
- No buy/sell/recommend language; present data, let the user decide.
- Respect data licensing; don't facilitate bulk redistribution/resale.
- Attribute data to FMP.

## Security
- Never expose `FMP_API_KEY` (answers, logs, citations, examples). Use `apikey=YOUR_FMP_API_KEY` in examples.
- Read the key only from the environment; don't store it in files or send it to non-FMP endpoints.

## Uncertainty
- Flag anything unconfirmed with "> Verification needed" and the docs link:
  https://site.financialmodelingprep.com/developer/docs
