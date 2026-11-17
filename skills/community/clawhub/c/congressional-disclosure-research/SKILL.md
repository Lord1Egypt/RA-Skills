---
name: congressional-disclosure-research
description: Research House and Senate public financial-disclosure filings through Crawlora and parse supported Senate reports. Use for filing inventories or transaction evidence briefs with owner, reporting dates, amount ranges, duplicates, and document availability preserved.
---

# Congressional disclosure research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound pages and calls by the requested scope and credit budget.
Preserve source IDs, URLs, retrieval times, and source dates where supplied.

Build a filing inventory or evidence brief from public disclosures. Define
chamber, filer identity/type, requested filing window, and whether the question
concerns filings, reported assets, or transactions before interpreting results.

## Search filings using chamber-specific semantics

- House requires `member`; its default filer type is `member`, while candidates
  use `filer_type=candidate` and `election_year`. House `from`/`to` take years;
  candidate rows use `year_kind=election`, not an exact filing date. House list
  results do not supply `filed_at`, so do not invent one from the year.
- Senate supports name prefixes or the `member` shorthand, but not both together.
  `state` cannot be combined with `senator_state`/`candidate_state`. Filer and
  report types follow the exact reference; `all` cannot be combined with other
  filer values. Senate `from`/`to` accept years or `MM/DD/YYYY` filing dates.
- `ticker` is an unsupported compatibility parameter: a nonempty value returns
  validation error. For an asset question, collect a bounded relevant filing
  sample, then filter returned transaction rows locally. Do not promise a
  complete Congress-wide ticker search from the filing index.

```sh
scripts/crawlora.sh /congress/stock-disclosures chamber=senate report_type=periodic_transaction from=2026 to=2026 page=1 limit=10
# Use a supported Senate filing_url returned above:
# scripts/crawlora.sh /congress/report url="$FILING_URL"
```

## Retrieve supported documents and retain their evidence

`congress_report` supports Senate Annual, PTR, and regular extension-notice HTML
URLs. House PDFs, Senate paper/image filings, blind-trust and other reports are
unsupported by this parser; retain their source links and mark body/transactions
unavailable. A filing row is evidence the filing was indexed, not that its
transaction details were retrieved. An extension notice's `body` is a notice,
not an asset or transaction table; its structured filer/date fields can be blank.

For supported reports use normalized `transactions` while retaining
`parts[].rows`, `source_part`, and row number for verification. Preserve displayed
transaction dates, owners (self/spouse/dependent), transaction types, asset names,
tickers, amount ranges, comments, and `--` placeholders. Separate transaction,
reporting-period, filing, and retrieval dates. Filing-window filters do not select
an equivalent transaction window; filter parsed transactions separately if needed.

## Reconcile and report

Match filers by chamber and available identity evidence rather than name alone.
The same transaction may appear in Annual and PTR reports: compare owner, asset,
date, type, and range, retain both source rows, and label probable duplicates
without collapsing uncertain matches. Keep amendments and original versions
traceable; do not infer replacement without document evidence. Do not turn amount
ranges into exact values or sum open-ended ranges as precise trade totals.
A sale is not a realised profit, an asset entry is not a trade, and a spouse's
reported transaction is not automatically the filer's own decision.

Return filing coverage, parsed/unavailable documents, a transaction evidence
ledger, unresolved duplicates, and explicit date/range limitations. The sample
cannot establish a current portfolio, trading intent, legal wrongdoing, or
investment returns. Do not derive legal filing deadlines or recommendations to
trade from this workflow.
