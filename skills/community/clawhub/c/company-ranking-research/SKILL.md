---
name: company-ranking-research
description: Research Fortune company directories and ranking editions and Forbes public billionaire/person records with Crawlora. Use to compare ranked companies, build a source-attributed business shortlist, or inspect ranking and wealth-profile evidence with year and methodology context.
---

# Company rankings and public profiles

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Use Fortune's directories/rankings and Forbes' public person records for
source-attributed business research. Rankings have different populations and
methods; ranks from separate lists are not interchangeable scores.

## Discover edition-specific values

1. Start with the requested geography, company/person scope, ranking, and year.
   Discover Fortune lists, then that list's years, then filters for the exact
   list/year pair. Never carry one edition's field IDs into another edition.
2. Fetch a bounded ranking page using discovered filter fields/values and sort
   metadata. Repeat `filter=field:value` for multiple criteria; values for one
   field are ORed and different fields are ANDed. Preserve `total`, offset,
   limit, search fields, and sortable fields when available.
3. For directory searches, use `fortune_company_filters` before country, industry,
   or ranking filters. Directory pagination is separate from ranking pagination.
   Resolve returned company slug or canonical URL before `fortune_company`;
   at least one is needed even though both are individually optional in schema.
4. Forbes billionaire results are another source and unit of analysis. Resolve
   the returned person `uri` before profile detail; do not identify people solely
   by similar names or equate an individual's wealth with company revenue.
   Forbes categories/headlines/article/author routes support public context.

```sh
scripts/crawlora.sh /fortune/ranking/lists
# Use a discovered list, year, then that edition's filters:
# scripts/crawlora.sh /fortune/ranking/years list="$LIST"
# scripts/crawlora.sh /fortune/ranking/filters list="$LIST" year="$YEAR"
# scripts/crawlora.sh /fortune/ranking list="$LIST" year="$YEAR" limit=20
scripts/crawlora.sh /fortune/companies/filters
scripts/crawlora.sh /fortune/companies search="Microsoft" page=1
scripts/crawlora.sh /forbes/billionaires
```

## Compare and deliver

Retain edition/year, source URL, source-specific company/person identifiers,
metric labels and units, and collection time. Fortune directory revenue filters
use millions of dollars; convert explicitly before comparison. Separate ranking
publication year from financial reporting period. Preserve missing/ambiguous
values and reported versus estimated figures; a person profile or ranking
appearance is not proof of ownership, solvency, investment merit, or misconduct.
Return a sourced shortlist or edition comparison with pagination coverage and
methodology limits. For change claims, match entities and editions across actual
saved/retrieved historical observations rather than comparing two current feeds.
