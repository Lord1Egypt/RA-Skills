---
name: earnings-event-research
description: Build sourced pre- or post-earnings briefs through Crawlora by joining Yahoo Finance event, estimate, reported-result, and daily-price data with SEC filings and normalized financials. Use for upcoming earnings previews, earnings-surprise checks, quarter-over-quarter or year-over-year result comparisons, and bounded post-results reaction briefs.
---

# Earnings event research

Build a dated event brief with a traceable estimate baseline, reported results,
primary SEC evidence, comparable fiscal periods, and a clearly defined daily
price window. Keep management claims, reported facts, estimates, calculations,
and interpretation separate.

## Setup

Set `CRAWLORA_API_KEY` to your key from
[crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for the
selected Yahoo Finance and SEC tools and their exact parameters.

## Resolve the event and evidence

1. Resolve a company name with `/yahoo-finance/search` and
   `/sec/company/search`. Preserve the exact symbol, exchange, legal issuer,
   and CIK. Do not merge similarly named issuers or assume a ticker identifies
   the same security in every market.
2. Establish the event before comparing numbers. Use
   `/yahoo-finance/calendars/earnings` for a bounded date window and
   `/yahoo-finance/ticker/{symbol}/calendar` for symbol-specific timing. Record
   the returned event date, time, timezone, and before/after-market designation.
   If any is missing, label it unknown rather than inferring it from a price move.
   Treat opaque labels such as `TAS` as raw source values unless their session
   meaning is documented. The earnings-dates source can also return non-earnings
   events such as shareholder meetings; verify the event name and earnings fields.
3. Capture the expectation baseline before interpreting the result. Use
   `/yahoo-finance/ticker/{symbol}/earnings` and
   `/yahoo-finance/ticker/{symbol}/earnings-dates`; retain the estimate's
   metric, period, source fields, and retrieval time. Keep estimates distinct
   from reported values, and do not call a difference a surprise unless the two
   values refer to the same metric and fiscal period. A current page's old-period
   estimate is retrospective data, not proof that the value was the consensus
   immediately before the event; only a saved or explicitly dated pre-event
   snapshot can establish that historical baseline.
4. Locate the corresponding 8-K, 10-Q, or 10-K with
   `/sec/company/submissions`. Filing dates are not fiscal period end dates.
   Preserve accession, form, filing date, report date, and primary-document URL.
   Use `/sec/filing/sections` on the returned accession when the relevant item is
   extractable. Item 2.02 commonly covers results of operations, but inspect the
   returned item labels and exhibits instead of assuming every filing has it.
5. Compare reported financials through `/sec/financials`. Match statement,
   currency, units, fiscal quarter/year, period start/end, duration when returned,
   and form.
   Prefer the same fiscal quarter a year earlier for seasonal businesses. A
   sequential-quarter comparison answers a different question and must be named.
   A row labeled quarterly can contain a cumulative year-to-date fact when a
   standalone duration is unavailable. Do not calculate standalone-quarter or
   sequential-quarter growth unless the fact's standalone duration is verified;
   otherwise label it unverified/YTD and omit that calculation. Matching the
   submission's report date does not prove a standalone duration. Normalized
   values can also reflect later restatements, so they may differ from what was
   known on the event date. Cross-check the end date against the matched
   submission's report date; if the issuer, fiscal label, or dates conflict, do
   not use that row in calculations.
6. Treat adjusted or non-GAAP figures as management-defined measures. Name the
   definition and reconciliation when present, and keep the comparable GAAP
   figure alongside it. Never combine a non-GAAP estimate with a GAAP actual in
   a surprise calculation. Show a percentage surprise's formula and denominator.
   Prefer `(actual - estimate) / abs(estimate) * 100` when the estimate is nonzero;
   when it is zero, report only the absolute difference. Explain rather than
   rank percentage surprises built on negative estimates.
7. If market response is requested, fetch
   `/yahoo-finance/ticker/{symbol}/history` with
   explicit `start`, `end`, `interval=1d`, and adjustment choice. State the exact
   close-to-close or open-to-close formula and trading dates. Daily bars cannot
   establish an intraday reaction or causality. If event session is unknown, show
   the dated prices without labeling any interval "the market reaction."

```sh
scripts/crawlora.sh /yahoo-finance/search q="NVIDIA" quotes_count=5 news_count=0
scripts/crawlora.sh /yahoo-finance/ticker/NVDA/earnings-dates limit=8
scripts/crawlora.sh /yahoo-finance/ticker/NVDA/history \
  start=2026-08-24 end=2026-08-31 interval=1d auto_adjust=false
scripts/crawlora.sh /sec/company/submissions \
  ticker=NVDA form=8-K from=2026-08-24 to=2026-08-31 limit=20
ACCESSION="replace-with-accession-returned-above"
# Do not reuse a stale example accession.
scripts/crawlora.sh /sec/filing/sections \
  ticker=NVDA "accession=$ACCESSION" items=2.02,9.01 max_chars=50000
scripts/crawlora.sh /sec/financials \
  ticker=NVDA statement=income period=quarterly limit=8
```

## Deliverable and limits

Return the requested preview or recap with issuer identity, event timing and its
uncertainty, estimate baseline, reported metric, GAAP/non-GAAP label, fiscal
period, comparable-period result, filing accession and source URL, price-window
definition, calculations, retrieval time, and material gaps. A compact evidence
ledger is preferable when several numbers come from different snapshots.

- Calendar rows and Yahoo earnings modules can be missing, stale, revised, or
  internally inconsistent. Preserve each source timestamp and report conflicts.
  Historical rows served today do not reconstruct what users saw before the event.
- An earnings release can precede the periodic filing and may summarize results
  differently. Absence from an extracted section is not proof the issuer omitted
  the disclosure; section extraction can be truncated or the exhibit may carry it.
- Adjusted daily prices incorporate transformations chosen by the history tool;
  unadjusted prices can be affected by splits and dividends. State the choice.
- A price change around earnings is an association over the stated window, not
  proof earnings caused the move. Do not turn this research into a buy/sell call.
- Back off on `429`, retry a transient `5xx` once, stop on `401`/`403`, and check
  the application `code`. Preserve successful evidence when another source fails.
