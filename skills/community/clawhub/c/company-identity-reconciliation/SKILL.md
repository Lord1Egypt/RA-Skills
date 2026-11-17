---
name: company-identity-reconciliation
description: Reconcile company and brand identities across Crawlora public domains, LinkedIn profiles, SEC registrants, and employer records. Use to deduplicate company lists or build a provenance-aware ID mapping with parent/brand/subsidiary, ambiguous names, time, and ownership limits preserved.
---

# Company identity reconciliation

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Produce an inspectable mapping for supplied company/brand records or an explicitly
bounded discovery set. Define whether the canonical entity means legal registrant,
operating company, brand, employer, branch or parent before joining sources.

## Resolve candidate identities with corroborating evidence

- Preserve original names, URLs, domains, addresses/country, supplied IDs and
  source dates. Normalize case/spacing/domain format for candidate matching,
  but retain aliases, subdomains and distinctions that can identify different
  branches, legal entities, divisions or products. Name similarity is not a merge rule.
- Use brand extraction for homepage/schema/social/legal-link leads. Its title/logo
  reflects site branding, not a corporate register. `maxSpeed=true` skips some
  identity evidence; `maxAgeMs` can return cached observations, so record source
  and freshness rather than calling every response current.
- SEC search/submissions can corroborate registrant CIK, ticker/name/aliases and
  filing identity; a brand need not have its own CIK, and absence from SEC is not
  absence of a business. Tickers can be ambiguous or change; preserve source/date.
- Employer datasets/ATS company search and a supplied/verified LinkedIn company
  ID offer other role-specific identifiers. Do not convert a URL slug into an
  invented numeric/company ID. A careers host or parent profile can serve several
  subsidiaries; shared infrastructure does not establish one legal entity.
- Read actually discovered official about/legal/filing pages where needed, using
  flat `web_scrape` options. Treat their relationship wording as an attributed
  claim with date/scope. A site footer, identical logo, shared address or linked
  social profile alone does not prove current ownership or an acquisition outcome.

```sh
scripts/crawlora.sh /sec/company/search q="Microsoft"
scripts/crawlora.sh /datasets/jobs/companies q="Microsoft" page=1 page_size=5
# Use supplied/verified domains and IDs for targeted brand/profile lookups.
```

## Build a reversible mapping rather than forcing duplicates together

For each candidate join retain both source records, source-specific IDs, evidence,
observed relationship, date, and decision: confirmed same scoped entity, related
but distinct, unresolved, or contradictory. A parent/brand relationship belongs
in a relationship field, not a silent ID collapse. Public company/person names
and similarly named regional businesses need careful disambiguation.

Use multiple corroborating identity signals or an explicit authoritative
relationship statement, preserving source limitations. Keep histories/rebrands
separate from current equivalence; a rename does not resolve all subsidiary,
country or product records. Confidence should reflect actual evidence, not
name similarity rendered as an unexplained percentage. Retain original rows
and a change ledger so a mapping can be reviewed and undone.

Return the scoped canonical-record table, alias/ID crosswalk, relationship
and evidence ledger, conflicts and missing lookups. Do not infer legal ownership,
solvency, endorsement or legitimacy beyond sources. Producing a mapping does
not authorise overwriting a CRM/database, contacting companies or publishing it.
