<!-- Copyright (c) 2026 Yang Pengfei / Forklift Veteran. MIT License; see LICENSE.md. -->
# Forklift Tender and Contract-Award Bulletin

## Reporting window
Use explicit user dates. Otherwise use the calendar week containing the request date: Monday 00:00 to Sunday 23:59, stating the time zone. For example, 2026-09-12 belongs to September 7-13. Retrieve only notices published by the actual research cut-off; never imply future coverage. Label a rolling seven-day window explicitly.

If fewer than three entries are found, an optional prior-week supplement must have separate dates and heading. If none are found, report "No relevant notices found in the sources reviewed", without claiming there are none anywhere.

## Research and fields
Use original government or buyer notices. See [international-markets.md](international-markets.md) for UK Find a Tender and Contracts Finder, EU TED, US SAM.gov, CanadaBuys and AusTender. Disclose login, paywall and indexing limits. One search is not continuous monitoring.

| Field | Required detail |
|---|---|
| Project | Original title and project or notice identifier |
| Notice | Publication date; tender, award, opening, amendment, cancellation or inquiry |
| Buyer | Name, location and jurisdiction |
| Equipment | Truck type, quantity and disclosed configuration |
| Amount | Budget or award, original currency and tax basis if disclosed |
| Supplier | Winner only when publicly identified |
| Deadline | Date, time and time zone |
| Evidence | Original notice URL and retrieval date |

Use "Not disclosed" for missing fields; omit entries without a usable source link. Deduplicate project identifiers and link amendments to the parent. Do not count tender and award as two purchases, add different currencies together, or infer unit prices from bundled contract amounts.

## Standalone HTML
Save `forklift-tenders_YYYY-MM-DD.html` in an available user-writable output directory. Verify it exists before claiming it was saved. Use UTF-8, viewport metadata, inline CSS and inline SVG; no CDNs, external fonts, images or JavaScript. Colours: navy #1a2a4a, orange #ff6b35, green #2e7d32, red #d32f2f; maintain readable contrast. Below 640px use table cards with a `data-label` on each data cell.

Recommended sections:
1. Title, reporting window, market scope, time zone and research cut-off.
2. Overview: deduplicated projects and disclosed amounts grouped by currency.
3. Up to three key notices with sources.
4. Separate tender and award tables.
5. Amendments, cancellations and upcoming deadlines.
6. Supported trends, sources, limitations and attribution.

Verify dates, links, amounts, status, deduplication and mobile layout. Mark expired deadlines and cancellations. Do not invent notices, promise awards or advise collusion. Producing a bulletin does not authorize sending it to others.
