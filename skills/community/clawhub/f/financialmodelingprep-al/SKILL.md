# Financial Modeling Prep (FMP) Skill

> Instructional knowledge that teaches an AI agent how to use the Financial Modeling Prep (FMP) financial-data API correctly, safely, and with rigor. This is guidance, not executable code.

---

## 1. Skill name

**financialmodelingprep** — "Use FMP for company financial data: quotes, profiles, statements, ratios, key metrics, valuation, price history, and calendars."

---

## 2. Purpose

Teach the agent to retrieve, ground, and cite financial data from FMP. The agent must:

- Resolve a company name to the **correct ticker** before pulling data.
- Pull quotes, company profiles, financial statements, ratios, key metrics, valuation (DCF), price history, and earnings/analyst data.
- Report **only numbers actually returned by the API** — never fabricate, estimate silently, or "remember" figures.
- Always cite the **symbol, period, filingDate, currency, and as-of date**.
- Handle errors and rate limits gracefully, control cost, protect the API key, and include a **not-investment-advice** disclaimer.

The agent's value is accuracy and traceability, not opinion. Treat every figure as something a user could audit against the API response.

---

## 3. When to use FMP

Use FMP when the user asks for:

- A **stock quote** or current price for a covered ticker.
- A **company profile/overview** (sector, industry, description, market cap, CEO, exchange, currency).
- **Financial statements** — income statement, balance sheet, cash flow (annual or quarterly).
- **Financial ratios** or **key metrics** (P/E, margins, ROE, debt ratios, per-share figures).
- A **valuation reference** such as discounted cash flow (DCF).
- **Historical end-of-day prices** over a date range.
- **Earnings calendar** dates or **analyst estimates**.
- Resolving a **company name to a ticker** (symbol/name search).

Prefer FMP when the task is fundamental analysis, screening inputs, or grounded company snapshots.

---

## 4. When NOT to use FMP

Do **not** use FMP (or stop and explain the limitation) when:

- The user needs **real-time tick-level / sub-second trading data** or order execution. FMP returns delayed/EOD-grade data, not a trading feed.
- The asset is **not covered** by FMP or by the user's plan (many international tickers, exotic instruments, private companies).
- The task requires **licensed redistribution** of data to third parties, bulk resale, or building a competing data product — that is a licensing matter outside this skill; do not assume it is permitted.
- The user wants **personalized investment advice or recommendations** — provide data with a disclaimer instead (see §16).
- A non-financial question is asked — use another tool/source.

When out of scope, say so plainly and suggest the correct alternative rather than forcing FMP.

---

## 5. Required environment variables

- `FMP_API_KEY` — **required.** The API key for FMP. Read it from the environment at call time.
- Authentication: pass as the `apikey` query parameter (or header where supported) on every request.
- Base URL: `https://financialmodelingprep.com/stable/`
- Method: **GET only.** Responses are JSON (usually a JSON array).

**Never** hardcode, print, log, or echo the key. Never include it in citations, examples, error messages, or output shown to the user. See §15.

---

## 6. Available operations

The `financialmodelingprep-mcp` server is **complete and live-tested**: it exposes **12 tools** —
eleven focused tools for common workflows plus one generic passthrough (`fmp_request`) that reaches
**all 263 FMP `/stable` endpoints**. Prefer the MCP tools when present; the HTTP column shows the
underlying endpoint for direct-GET fallback.

| # | Operation | MCP tool | HTTP endpoint (`/stable/...`) |
|---|-----------|----------|-------------------------------|
| 1 | Symbol/name search (auto symbol→name fallback) | `fmp_search` | `/search-symbol?query=`, `/search-name?query=` |
| 2 | Quote | `fmp_quote` | `/quote?symbol=` |
| 3 | Company profile | `fmp_company_profile` | `/profile?symbol=` |
| 4 | Income statement | `fmp_income_statement` | `/income-statement?symbol=&period=&limit=` |
| 5 | Balance sheet | `fmp_balance_sheet` | `/balance-sheet-statement?symbol=&period=&limit=` |
| 6 | Cash flow | `fmp_cash_flow` | `/cash-flow-statement?symbol=&period=&limit=` |
| 7 | Ratios | `fmp_ratios` | `/ratios?symbol=&period=&limit=` |
| 8 | Key metrics | `fmp_key_metrics` | `/key-metrics?symbol=&period=&limit=` |
| 9 | Valuation (DCF) | `fmp_dcf` | `/discounted-cash-flow?symbol=` |
| 10 | Historical prices (EOD) | `fmp_historical_prices` | `/historical-price-eod/full?symbol=&from=&to=` |
| 11 | Company screener | `fmp_screener` | `/company-screener?...` |
| 12 | **Anything else (263 endpoints)** | `fmp_request` | any `/stable/<endpoint>` (e.g. `treasury-rates`, `dividends`, `senate-trading`, `news/stock-latest`) |

Common parameters: `period` ∈ `annual | quarter`; `limit` controls how many periods/rows return;
`from`/`to` are `YYYY-MM-DD`. The server validates inputs, preserves as-of dates, redacts the key, and
surfaces typed errors (`auth`, `validation`, `rate_limit`, `plan_restricted`, `timeout`, `server`).

---

## 6a. The generic `fmp_request` tool (full 263-endpoint surface)

Tools 1–11 cover the common equity-research path. `fmp_request` is the escape hatch for the **entire
rest of FMP** — treasury rates, dividends, stock splits, insider trading, senate/house trading, ETF
holdings, economic indicators, news, earnings-call transcripts, and the long tail of the **263
`/stable` endpoints**.

**Inputs:** `endpoint` (the path after `/stable/`, validated to a safe path shape) and an optional
`params` object of query parameters.

```json
{ "endpoint": "treasury-rates", "params": { "from": "2025-01-01", "to": "2025-03-31" } }
{ "endpoint": "dividends", "params": { "symbol": "AAPL" } }
{ "endpoint": "senate-trading", "params": { "symbol": "AAPL" } }
{ "endpoint": "news/stock-latest", "params": { "limit": 20 } }
```

**When to prefer a dedicated tool.** If a dedicated tool exists for what you need — quote, profile,
income statement, balance sheet, cash flow, ratios, key metrics, DCF, historical prices, screener, or
search — **use it instead of `fmp_request`.** Dedicated tools add input validation, output
normalization (e.g. as-of fields), and clearer errors. Reach for `fmp_request` only when no dedicated
tool fits.

**Catalog.** The complete endpoint list with parameters and response shapes lives in the API docs at
`api-docs/09-all-endpoints/` (search & directory, company & profile, quotes, prices & history,
metrics/valuation/analyst, ownership/SEC/government, ETFs & funds, screeners & movers). Consult it to
pick the right `endpoint` and `params` rather than guessing.

All numeric-integrity, citation, freshness, security, and compliance rules below apply equally to data
returned by `fmp_request`.

---

## 7. Symbol resolution workflow

**Never pull data for a guessed ticker.** Tickers are ambiguous (e.g. "Apple" vs "Applied"; same name on multiple exchanges; ADRs).

**Resolve symbols with `fmp_search` first.** Before any quote/statement/metric call, run `fmp_search`
to turn a name or fuzzy ticker into a canonical `symbol`. `fmp_search` already tries
`/search-symbol` and **automatically falls back** to `/search-name`, so a single call handles both a
partial ticker and a company name. Use the resolved `symbol` for every downstream tool.

1. If the user gave an exact, obviously valid ticker (e.g. `AAPL`) and you are confident, you may proceed — but still verify against the profile.
2. Otherwise call `fmp_search` (which queries `/search-name` / `/search-symbol`).
3. Inspect results: `symbol`, `name`, `exchange`/`exchangeShortName`, `currency`.
4. **Confirm the right match** — prefer the primary listing on the expected exchange and currency. If multiple plausible matches exist (different exchanges, ADR vs local), **ask the user to confirm** or state which one you chose and why.
5. Only then pull quotes/statements/etc. using the confirmed `symbol`.
6. Cross-check with `/profile?symbol=` — confirm `companyName`, `exchange`, and `currency` match the user's intent before reporting numbers.

Document the resolved symbol explicitly in the answer ("Resolved 'Apple' → AAPL on NASDAQ, USD").

---

## 8. Quote workflow

1. Confirm/resolve the symbol (§7).
2. Call `/quote?symbol=<TICKER>` (or `fmp_quote`).
3. Read fields: `price`, `change`, `changePercentage`, `dayLow`, `dayHigh`, `marketCap`, `volume`, `previousClose`, `timestamp`/`exchange`.
4. Report the price **with currency and an as-of indication** (use the response timestamp/exchange). Quotes are delayed, not real-time — say so if precision matters.
5. If the array is empty, the symbol is wrong or not covered by the plan (§13).
6. For multiple symbols, prefer a single batched quote call if supported instead of many calls (§14).

Example phrasing: "AAPL last price 192.34 USD (delayed quote, as of <timestamp>). Source: FMP `/quote`."

---

## 9. Financial statements workflow

1. Resolve the symbol (§7).
2. Choose the statement endpoint: income, balance sheet, or cash flow.
3. Choose the period explicitly (this applies to `fmp_income_statement`, `fmp_balance_sheet`,
   `fmp_cash_flow`, `fmp_ratios`, and `fmp_key_metrics`):
   - `period=annual` for fiscal-year data — use for year-over-year trends, long histories, and "last
     N years" requests.
   - `period=quarter` for quarterly data — use for recent momentum, seasonality, the latest reported
     quarter, or to build a TTM from the last four quarters.
   - Default to `annual` when the user does not specify; switch to `quarter` only when the question is
     about recent/quarterly performance.
   - **Do not mix** annual and quarterly figures in one comparison without labeling each.
4. Choose `limit` to control how many periods come back (e.g. `limit=5` for 5 years/quarters). Larger limits cost more and may exceed plan history.
5. Identify each row's identity fields: `date`, `period` (e.g. `FY`, `Q1`), `calendarYear`/`fiscalYear`, `filingDate`, `acceptedDate`, `reportedCurrency`.
6. **TTM (trailing twelve months):** if the user wants TTM, use a dedicated TTM endpoint/metric if available, or sum the last four **quarters** — and label it "TTM" and state the four periods used. Never present a single annual figure as TTM.
7. **Currency:** always report `reportedCurrency`. Do not convert currencies unless asked, and if you do, cite the rate and source separately.
8. Cite every number with symbol + period + filingDate (§12).

> Verification needed: confirm whether a separate TTM endpoint exists or whether TTM is a field within `/key-metrics` / `/ratios`.

---

## 10. Valuation workflow (DCF)

1. Resolve the symbol (§7).
2. Call `/discounted-cash-flow?symbol=<TICKER>`.
3. Read `dcf` (estimated intrinsic value per share) and the comparison price (`Stock Price` / `price` field).
4. **Always add caveats.** FMP's DCF is a **model estimate** built on assumptions (growth, discount rate, terminal value) that may not match the user's view. It is not a price target or a recommendation.
5. Compare DCF to the current price descriptively ("model DCF X vs market price Y") — do **not** conclude "buy/sell" or "undervalued, you should..." Frame as: "Per FMP's DCF model, estimated value is X versus market price Y; this is a single model's estimate, not advice."
6. Combine with statements/ratios for context, but keep each number cited and dated.
7. Include the not-investment-advice disclaimer (§16).

---

## 11. Numeric integrity rules

These are non-negotiable.

- **Report only numbers returned by the API.** If a figure is not in the response, do not state it.
- **Never silently compute or estimate.** If a derived value is needed (e.g. a growth rate, a margin), compute it explicitly from cited API fields, show the inputs, and label it "derived" — or prefer the API's own ratio/metric field.
- **Never recall numbers from memory/training.** Financial data changes; only the live response is authoritative.
- **Show units and currency** for every figure (e.g. "1.23B USD", "P/E 28.4x", "margin 24.3%"). State whether large numbers are raw, thousands, or millions per the response.
- **Preserve precision sensibly** — do not invent decimal places the response did not provide; round transparently and say so.
- If a field is `null`/missing, say "not reported" rather than guessing.
- If two endpoints disagree, report both with their sources rather than picking silently.

---

## 12. Citation & freshness rules

Every reported number must be traceable. For each figure or block, cite:

- **Symbol** (the resolved ticker).
- **Endpoint** (e.g. `/income-statement`, `/quote`).
- **Period** (`FY2024`, `Q1 2025`, or "annual/quarterly") for statements/metrics.
- **filingDate** / `acceptedDate` for statement data (when the filing was made).
- **reportedCurrency** for monetary figures.
- **As-of**: financial data goes stale. State that data is "as of" the response timestamp or the latest period/filing, and that newer filings may exist.

Example citation: "Revenue 391.0B USD — FY2024 income statement, filingDate 2024-11-01, reportedCurrency USD (FMP). Data as of latest available filing; a newer period may exist."

Prefer giving the user enough to re-query: symbol, endpoint, period.

---

## 13. Error handling rules

| Condition | Meaning / typed error | Correct agent reaction |
|-----------|-----------------------|------------------------|
| `{"Error Message":"..."}` / `validation` | Request rejected / bad arguments | Read the message; fix the request (param/symbol/date/endpoint). Do not present partial/garbage data. |
| HTTP 401 / "invalid api key" / **account suspended** (`auth`) | Auth problem | **Do not retry.** Stop, tell the user the key is invalid/suspended and must be fixed. Never expose the key. |
| **HTTP 402 (`plan_restricted`)** | Endpoint not included in the current plan (e.g. `fmp_screener` or some `fmp_request` endpoints on lower tiers) | **Do not retry — retrying never helps.** Tell the user plainly that this endpoint requires a higher FMP plan, name the endpoint, and offer an alternative the current plan can answer if one exists. |
| HTTP 429 (`rate_limit`) | Rate/quota limit hit | **Back off** (wait/retry with delay) and **cache**; reduce call volume. Inform the user if limited. Do not hammer. |
| Empty array `[]` | No data | Likely **wrong symbol** or **not covered by the plan** (e.g. non-US on free tier). Re-resolve the symbol or explain coverage limits. |
| Timeout / 5xx (`timeout` / `server`) | Transient | Retry a small number of times with backoff; if persistent, report the outage. (For wide price ranges, narrow `from`/`to`.) |

Rule of thumb: **fix-don't-retry** for 401/suspended and **402/plan_restricted** (a higher plan is
needed); **back-off-and-cache** for 429; **re-resolve** for empty results.

---

## 14. Cost / limit-control rules

- The **free tier is limited** (~250 calls/day, US-only coverage). Treat calls as scarce.

> Verification needed: confirm current free-tier call limits and coverage at https://site.financialmodelingprep.com/developer/docs

- **Cache** results within a session; reuse a profile/quote you already fetched instead of re-pulling.
- **Batch** where possible (e.g. one multi-symbol quote call rather than N single calls).
- **Right-size `limit`** — request only the periods you need.
- **Avoid redundant pulls** — resolve the symbol once, store it, reuse it.
- Plan the minimal set of endpoints to answer the question before calling.
- If a request would blow the budget, tell the user and propose a narrower query.

---

## 15. Security rules

- **Never expose `FMP_API_KEY`** — not in answers, logs, citations, examples, code blocks, or error text.
- Read the key only from the environment; do not request it from the user in plain chat or store it in files.
- When showing example URLs, replace the key with `apikey=YOUR_FMP_API_KEY` — never the real value.
- If a tool/log would echo the URL with the key, redact it.
- Do not transmit the key to any non-FMP endpoint.

---

## 16. Compliance rules

- **This is not financial advice.** Always include a disclaimer when giving valuations, comparisons, or anything a user could read as a recommendation: *"This is informational data from FMP, not investment advice. Verify independently before making decisions."*
- **No recommendations** — present data and let the user decide. Do not say "buy", "sell", "you should invest".
- **Respect data licensing** — do not facilitate bulk redistribution, resale, or building a competing dataset. Provide data for the user's own analysis.
- Attribute data to FMP as the source.
- Distinguish **facts returned by the API** from any interpretation you add (label interpretation clearly).

---

## 17. Agent behavior checklist

Before answering any FMP request, confirm:

- [ ] `FMP_API_KEY` is available and never exposed.
- [ ] Symbol resolved and confirmed (search + profile) before pulling data.
- [ ] Correct endpoint and `period` (annual/quarter/TTM) chosen and labeled.
- [ ] Only API-returned numbers reported; no fabrication; derived values labeled with inputs shown.
- [ ] Units and `reportedCurrency` shown for every figure.
- [ ] Citations include symbol, endpoint, period, filingDate, and as-of/freshness note.
- [ ] Errors handled per §13 (no retry on 401/suspended or 402/plan_restricted; back off on 429; re-resolve on empty).
- [ ] Used `fmp_search` to resolve the symbol; used a dedicated tool where one exists, `fmp_request` only for the long tail.
- [ ] Calls minimized/cached; `limit` right-sized.
- [ ] Not-investment-advice disclaimer included where relevant.
- [ ] Uncertain endpoint/field behavior flagged with "Verification needed".

---

## 18. Example agent workflows

**A. "What's Apple trading at?"**
1. Confident `AAPL`; confirm via `/profile?symbol=AAPL` (NASDAQ, USD).
2. `/quote?symbol=AAPL`.
3. Report: "AAPL 192.34 USD, +0.8% (delayed quote, as of <timestamp>). Source: FMP `/quote`."

**B. "Show me Microsoft's revenue and net income for the last 3 years."**
1. Resolve "Microsoft" → search → `MSFT` (NASDAQ, USD); confirm via profile.
2. `/income-statement?symbol=MSFT&period=annual&limit=3`.
3. Report each year with `date`/`period`, `revenue`, `netIncome`, `reportedCurrency`, `filingDate`. Label as annual. Note data as-of latest filing.

**C. "Is Tesla undervalued?"**
1. Resolve → `TSLA`; confirm profile.
2. `/discounted-cash-flow?symbol=TSLA` → `dcf` vs market `price`.
3. Report: "FMP DCF model estimate X USD vs market price Y USD (as of <date>). This is one model's estimate, not advice." Add disclaimer (§16). Do **not** declare it under/overvalued as a conclusion.

---

## 19. Common mistakes

- Guessing a ticker instead of resolving it (wrong company entirely).
- Reporting a number from memory or "rounding from intuition" instead of the response.
- Mixing annual and quarterly figures without labels.
- Calling an annual figure "TTM".
- Omitting currency or treating non-USD as USD.
- Concluding "buy/undervalued" from a DCF model.
- Retrying on 401/suspended (wastes calls, never fixes auth).
- Retrying on 402/plan_restricted instead of telling the user a higher plan is required.
- Using `fmp_request` when a dedicated tool exists (loses validation/normalization).
- Hammering on 429 instead of backing off.
- Treating an empty `[]` as "value is zero" instead of "no data / wrong symbol / not covered".
- Exposing the API key in a URL or example.
- Forgetting the not-investment-advice disclaimer.

---

## 20. Maintenance notes

- FMP migrated to the `/stable/` base; older `/api/v3/` paths may differ. Re-verify endpoints against the docs periodically.
- Free-tier limits, coverage (US-only), and pricing change — re-check before relying on them.
- The `financialmodelingprep-mcp` server currently exposes 12 tools (11 dedicated + `fmp_request`).
  Tool names and the endpoint surface may evolve; confirm against the server's tool list and the
  full catalog in `api-docs/09-all-endpoints/`.
- Keep all "Verification needed" items in sync with the live docs: https://site.financialmodelingprep.com/developer/docs
- When in doubt about a field's meaning, prefer the API's own labeled field over a derived calculation.
