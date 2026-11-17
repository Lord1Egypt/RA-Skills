---
name: chain-store-footprint-analysis
description: Compare observed chain-store coverage using Crawlora Starbucks directories, live chain locators, and Google Maps business records. Use for branch counts, geographic overlap, amenity coverage, or footprint gaps within a defined area with source caps and identity uncertainty preserved.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Chain store footprint analysis

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Map observed branches for specified chains and geographic boundaries. Establish
brands/aliases, store versus kiosk/licensed location scope, cities or coordinate
boundaries, amenity criteria, source set, and collection budget before counting.
This describes observed supply, not sales, foot traffic, demand, or site profitability.

## Discover branches under matched geographic scopes

- Use stored Starbucks facets/search/nearby for brand-specific discovery and
  stable `store_number`. Dataset `country` is actual geography; `market=us/ca`
  records crawl-host provenance and must not be mistaken for a geographic filter.
  Preserve exact country/state/city and coordinate evidence.
- Refresh selected locations with live Starbucks locator/nearest-store calls.
  Either `place` or a coordinate pair is needed. Its cap is 50 without pagination;
  `result_capped` means the local result is incomplete. Distinguish a failed
  geocode (`place_not_found`) from a successful search with no returned branches.
  Canadian operational data should use the Canadian host when requested.
- Other brands can use stored Google Maps business search/facets/nearby, followed
  by selected live search/place verification. A name-text match is not a verified
  chain affiliation; check canonical brand/site, address, and location evidence.
  Google Maps category/country values differ from Starbucks taxonomy/codes.
- McDonald's coordinate locator is a separate source with its own accepted markets,
  cap, and radius in miles; dataset nearby radii are meters. Convert explicit
  geographic scopes rather than copying identical numeric radius values. A
  capped live locator alone cannot establish a whole-country store count.
- Keep a boundary/query ledger, requested/returned pages, cap flags, search result
  counts, and crawl times. The stored indexes are not automatically an official
  census of every branch or a proof that a competing chain is absent.

```sh
scripts/crawlora.sh /datasets/starbucks-stores/facets facet=country
scripts/crawlora.sh /datasets/starbucks-stores/search country=US city=Seattle page=1 page_size=100
scripts/crawlora.sh /starbucks/stores place="Seattle, WA" market=us
scripts/crawlora.sh /datasets/google-map-businesses/search q="Starbucks" city=Seattle page=1 page_size=10
```

## Reconcile locations and report coverage

Deduplicate the same brand/store ID first; cross-source matches need address and
coordinate corroboration. Similar names are not sufficient, and two units/kiosks
inside a complex can be distinct branches. Keep relocated, permanently-closed,
licensed, and company-operated locations explicit when fields support the labels.
An empty schedule/amenity field can mean not published for that market, not closed
or unsupported. Mobile-order readiness differs from static capability codes.

Use unique matched branches for area counts. For overlapping radius queries,
count each branch once and keep the union boundary explicit; dividing by the
sum of overlapping circle areas produces a misleading density. Area density
requires a defined area, and per-capita measures require a separately sourced
population with matching geography/date. Counts alone are not market share.

Return a branch evidence ledger, deduplicated area/brand matrix, source coverage,
observed amenity/ownership breakdowns, and unknown or incomplete areas. A missing
branch in a capped/partial sample is an observed coverage gap, not proof of closure
or unmet demand. Historical expansion/contraction claims require comparable
saved observations and verified changes. Do not contact stores, submit leads,
or choose an investment/site solely from this footprint.
