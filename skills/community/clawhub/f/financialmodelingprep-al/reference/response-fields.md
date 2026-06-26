# FMP Response Fields Reference

How to read and **cite** the most common fields. Rule: report only fields actually present in the response; show units and currency; treat `null`/missing as "not reported".

> Verification needed: exact field names vary by endpoint version. Confirm against https://site.financialmodelingprep.com/developer/docs.

---

## Search (`/search-symbol`, `/search-name`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `symbol` | The ticker. | The value you carry forward to all other calls. State it explicitly. |
| `name` / `companyName` | Company name. | Confirm it matches the user's intended company. |
| `exchange` / `exchangeShortName` | Listing venue. | Disambiguate cross-listings; pick the primary/expected one. |
| `currency` | Trading/reporting currency. | Flag non-USD early; carry into reporting. |

---

## Quote (`/quote`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `price` | Last (delayed) price. | Report with currency; note it's delayed, with `timestamp` as-of. |
| `change` / `changePercentage` | Absolute / percent change. | Report together; specify "vs previous close". |
| `dayLow` / `dayHigh` | Intraday range. | Optional context. |
| `yearLow` / `yearHigh` | 52-week range. | Optional context. |
| `marketCap` | Market capitalization. | Show units/currency; large number — state scale. |
| `volume` | Shares traded. | Context for liquidity. |
| `previousClose` / `open` | Prior close / open. | Baseline for change. |
| `timestamp` / `exchange` | As-of time / venue. | Use as the freshness anchor in citations. |

---

## Income statement (`/income-statement`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `date` | Period end date. | Anchor of the row. |
| `period` | `FY`, `Q1`...`Q4`. | Always label annual vs quarter. |
| `calendarYear` / `fiscalYear` | Year of the period. | Cite alongside `period`. |
| `reportedCurrency` | Currency of figures. | **Always show** — do not assume USD. |
| `filingDate` / `acceptedDate` | When filed/accepted. | Cite for freshness/auditability. |
| `revenue` | Top-line sales. | Report with currency + scale. |
| `costOfRevenue` / `grossProfit` | COGS / gross profit. | Derive margin only from these cited fields if needed. |
| `operatingIncome` | Operating profit. | — |
| `netIncome` | Bottom-line profit. | Headline profitability figure. |
| `eps` / `epsDiluted` | Earnings per share. | Per-share; report units. |

---

## Balance sheet (`/balance-sheet-statement`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `totalAssets` / `totalLiabilities` / `totalEquity` | Balance-sheet totals. | Currency + scale; cite period + filingDate. |
| `cashAndCashEquivalents` | Liquid cash. | Liquidity context. |
| `totalDebt` | Total debt. | Leverage context; prefer ratio endpoint for leverage ratios. |

---

## Cash flow (`/cashflow-statement`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `operatingCashFlow` | Cash from operations. | Quality-of-earnings context. |
| `capitalExpenditure` | CapEx (usually negative). | Watch sign convention. |
| `freeCashFlow` | OCF − CapEx (per FMP). | Prefer FMP's field over recomputing. |
| `netChangeInCash` | Net cash movement. | — |

---

## Ratios (`/ratios`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `priceEarningsRatio` | P/E. | Report as multiple ("x"); cite period. |
| `grossProfitMargin` / `netProfitMargin` | Margins. | Report as % ; prefer over hand-computing. |
| `returnOnEquity` / `returnOnAssets` | ROE / ROA. | % ; cite period. |
| `currentRatio` / `quickRatio` | Liquidity. | — |
| `debtEquityRatio` | Leverage. | — |

---

## Key metrics (`/key-metrics`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `marketCap` / `enterpriseValue` | Size measures. | Currency + scale. |
| `peRatio` / `evToSales` | Valuation multiples. | Report as "x"; cite period. |
| `revenuePerShare` / `netIncomePerShare` | Per-share figures. | Per-share units. |
| `freeCashFlowPerShare` / `bookValuePerShare` | Per-share FCF / book value. | — |

---

## Valuation (`/discounted-cash-flow`)

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `dcf` | Model intrinsic value/share. | **Estimate only** — caveat heavily; not advice. |
| `Stock Price` / `price` | Comparison market price. | Compare descriptively to `dcf`. |
| `date` | As-of date of the model run. | Cite for freshness. |

---

## Calendars & estimates

| Field | Meaning | How to use / cite |
|-------|---------|-------------------|
| `date` (earnings) | Earnings report date. | The monitored event. |
| `epsEstimated` / `epsActual` | Estimated vs reported EPS. | Distinguish forecast from actual. |
| `revenueEstimated` / `revenueActual` | Estimated vs reported revenue. | Same. |
| `estimatedEpsAvg` / `estimatedRevenueAvg` (analyst) | Consensus forecast. | Label as **forecast/consensus**, not fact. |

---

## Universal citation pattern

For any figure: **value + units/currency + symbol + endpoint + period + filingDate + as-of note.**
Example: "netIncome 96.99B USD — AAPL, `/income-statement`, FY2024, filingDate 2024-11-01 (FMP). As of latest filing."
