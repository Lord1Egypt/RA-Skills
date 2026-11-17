---
name: film-box-office-comparison
description: Compare theatrical film grosses through Crawlora Box Office Mojo charts, title/release records, and stored data. Use for comparable-film briefs, domestic/international mix, release-window comparisons, or franchise performance with title, release, currency, and reporting basis preserved.
---

# Film box-office comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare theatrical performance for a selected film set, release window, market,
franchise, or genre. Define the comparison basis before retrieving data:
weekend/year versus lifetime, original run versus reissues, and reported estimates
versus updated figures are different measures.

## Resolve titles, release groups, and source scope

- Discover stored franchise/brand/genre/year facets before exact dataset filters.
  Hydrated records can include release groups and market tables; missing hydration
  or fields are coverage gaps, not zero gross. Store the source/crawl date.
- Dataset title IDs use the IMDb-style `tt…` namespace also used on Box Office
  Mojo title pages. A release (`rl…`) or release-group (`gr…`) ID is a different
  entity. Copy returned links/IDs before the corresponding live detail route;
  routes accepting `id`/`path`/`url` require exactly one of those alternatives.
- Keep each title's original run, rereleases, release groups, and geographic
  markets separate. A lifetime title figure can already include multiple runs;
  adding release-group figures to it double counts revenue. Similar titles and
  franchise branding do not establish the same film or release.
- Weekend endpoints use the site's year/week and returned date range, not a
  presumed ISO-week conversion. Keep weekend estimates separate from finalized
  observations and use the same collection cutoff. Annual charts measure that
  chart's year/basis; they are not interchangeable with lifetime rank/year records.

```sh
scripts/crawlora.sh /datasets/boxofficemojo/facets facet=genre_names
scripts/crawlora.sh /datasets/boxofficemojo/search q="science fiction" hydrated=true page=1 page_size=10
scripts/crawlora.sh /boxofficemojo/weekend/domestic year=2025 week=52
# Follow returned title/release IDs before fetching their detail.
```

## Compare equivalent grosses

Keep raw currency labels, numeric units, territories, dates, and reissue scope.
Dataset gross amounts are whole reported USD dollars; do not treat them as cents
or apply currency/inflation conversion without sourced assumptions. Nominal
figures across decades do not establish inflation-adjusted performance.

Where compatible figures are available, compute domestic share as
`domestic / worldwide` and international share as `international / worldwide`,
with nonzero denominators and matching dates/runs. Worldwide already includes
its geographic components: do not add domestic to worldwide. If totals differ
by reporting cutoff, show the discrepancy rather than forcing shares to sum to one.
A weekend drop requires consecutive comparable weekend figures for the same run,
not an estimate paired with an unrelated release's finalized figure.

Return an identity/release ledger and comparison table with scope, dates, sources,
grosses, formulas, coverage, and missing fields. Theatrical gross is not studio
net revenue or profit; budgets alone do not provide marketing, distribution,
exhibitor splits, financing, or other revenue/costs. Do not infer ROI or production
investment merit from incomplete cost data, chart ranks, or an observed genre sample.
