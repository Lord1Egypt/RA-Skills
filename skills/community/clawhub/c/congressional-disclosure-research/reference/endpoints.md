# congressional-disclosure-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**2 endpoints across 1 platform group(s).**

## Congress (2)

### `congress_report`

- **HTTP:** `GET /congress/report`
- **What:** Fetch and parse a congressional disclosure report. Returns one US Senate disclosure report from the `filing_url` found by the stock-disclosures search, passed as `url`. Supports annual reports, periodic transaction reports and due date extension notices. Output has filer, filing date, `parts` with their rows, and a `transactions` list. House PDFs and paper filings return a validation error.
- **Params:** `url` (string, **required**) — Filing URL, as returned by congress-stock-disclosures' filing_url field. Must be an efdsearch.senate.gov /search/view/annual/..., /search/view/ptr/..., or /search/view/extension-notice/regular/... URL.

### `congress_stock_disclosures`

- **HTTP:** `GET /congress/stock-disclosures`
- **What:** Search congressional stock-disclosure filings. Searches congressional stock-disclosure filings for the House (default) or the Senate via `chamber`. House needs `member`; Senate takes `first_name`, `last_name`, `filer_type`, state and `report_type` filters, and `from`/`to` dates. Each result has member, office, filing year, filing type and `filing_url`. Paged by `page` and `limit` (default 50, max 500).
- **Params:** `candidate_state` (string, optional) — Candidate state filter (Senate only, 2-letter code).; `chamber` (string, optional) — Chamber filter. Allowed values: house, senate.; `district` (string, optional) — House district filter (House only).; `election_year` (string, optional) — House candidate-search election year filter (requires filer_type=candidate).; `filer_type` (string, optional) — Filer-type filter, meaning differs by chamber. House: member (default) or candidate. Senate: comma-separated senator, candidate, former_senator, or the standalone all value. Defaults to senator when omitted.; `first_name` (string, optional) — Senate filer first-name prefix (Senate only; cannot be combined with member).; `from` (string, optional) — Minimum filing date. House accepts YYYY. Senate accepts YYYY or MM/DD/YYYY and defaults to 2012 when omitted.; `last_name` (string, optional) — Senate filer last-name prefix (Senate only; cannot be combined with member).; `limit` (integer, optional) — Max results (1-500).; `member` (string, optional) — Member name. Required for House. For Senate, this backward-compatible shorthand maps one word to last_name and maps the first word plus the complete remaining surname to first_name/last_name; it cannot be combined with either exact name field.; `page` (integer, optional) — 1-based result page (1-1000).; `report_type` (string, optional) — Comma-separated Senate report-type filter (Senate only). Allowed values: annual, periodic_transaction, due_date_extension, blind_trust, other. Defaults to all types when omitted.; `senator_state` (string, optional) — Senator state filter (Senate only, 2-letter code).; `sort` (string, optional) — Sort key. Allowed values: name_asc, name_desc, office_asc, office_desc, filing_year_asc, filing_year_desc.; `state` (string, optional) — State or territory filter (2-letter code). For Senate this backward-compatible shorthand applies to both Senator and Candidate states and cannot be combined with senator_state or candidate_state.; `ticker` (string, optional) — Deprecated unsupported parameter; any non-empty value returns a validation error and the parameter is planned for removal.; `to` (string, optional) — Maximum filing date. House accepts YYYY. Senate accepts YYYY or MM/DD/YYYY.
