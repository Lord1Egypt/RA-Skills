# US company data sources

Ordered by how a US B2B team should treat them: primary first, licensed
second, and never the gray market.

## Primary public sources (free, authoritative)

| Source | URL | Use |
| --- | --- | --- |
| SEC EDGAR full-text search | https://efts.sec.gov/LATEST/search-index?q= | Filings for public companies |
| SEC company tickers (CIK map) | https://www.sec.gov/files/company_tickers.json | Ticker to CIK |
| SEC company facts (XBRL) | https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json | Revenue, margins, debt |
| SEC submissions | https://data.sec.gov/submissions/CIK##########.json | Filing history, Form 4, 8-K |
| SBA Dynamic Small Business Search | https://sam.gov/search/?index=ei | Federal contractors, NAICS, employee bands |
| SAM.gov entity search | https://sam.gov/search/ | Registrations, points of contact |
| USPTO trademark search | https://tmsearch.uspto.gov/ | Brand names, owner city/state |
| State Secretary of State registries | state-specific | Entity status, registered agent |
| State licensing boards | state-specific | Contractors, healthcare, trades |
| USAspending.gov | https://www.usaspending.gov/ | Federal contract awards and amounts |
| Grants.gov | https://www.grants.gov/ | Grant recipients (nonprofits, vendors) |
| Census business patterns | https://data.census.gov/ | Industry and county-level business counts |
| FRED (St. Louis Fed) | https://fred.stlouisfed.org/ | Macro series for a research memo |
| CourtListener (RECAP) | https://www.courtlistener.com/ | Public court filings for company research |

The SEC requires a descriptive `User-Agent` header with a contact email.

## Public company research (free, no API key)

- Company newsroom and press release pages.
- Business Wire and PR Newswire public release pages.
- Investor relations pages: earnings releases, decks, shareholder letters.
- Public job postings on the company's own careers page (many ATS pages are
  public: Workday, Greenhouse, Lever, Ashby).
- Podcast and webinar pages that describe the product.
- Product changelogs and status pages.
- Public review sites (G2, Capterra) for category and competitive context -
  respect their terms, read publicly available pages only.

## Government and nonprofit buyers (public)

- SAM.gov contract opportunities and award history.
- Grants.gov awards.
- State and county procurement portals (usually under a .gov domain).
- City council minutes and budget documents (public record).

## Licensed providers (pay, terms apply)

| Provider | Strength | Typical use |
| --- | --- | --- |
| Apollo.io | US company + contact database, sequences | list building with license |
| Clay | enrichment and orchestration | waterfall enrichment |
| ZoomInfo | firmographics and org charts | enterprise accounts |
| HubSpot Breeze Intelligence | firmographics inside the CRM | sales workflows |
| Hunter | email pattern + deliverability | verifying business emails |
| RocketReach | contact accuracy | direct dials and emails |
| LinkedIn Sales Navigator | account and people search | manual prospecting only |
| Cognism / Uplead | mobile numbers (with consent signals) | phone-first teams |

Rules for licensed providers:

- Use them under the license. Export limits, usage rights, and "do not
  resell" clauses matter.
- Verify anything that drives an email: pattern guesses still need a
  deliverability check.
- Keep the provider's source attribution and date with each record.
- Do not use a provider to build a list you would be embarrassed to have
  audited.

## Sources to avoid (and why)

| Source | Why not |
| --- | --- |
| Breach dumps and leaked databases | Illegal to use, and it will burn the domain and the company |
| Scraped personal profile data | Platform terms violation, privacy risk |
| "Verified" bought email lists | Stale, catch-all heavy, kills deliverability |
| Free "email finder" sites that harvest | ToS violations, malicious redirects |
| Any source that hides where the data came from | You cannot prove consent to a regulator |

## Data hygiene rules for every record

```
company        | legal or trading name
domain         | normalized root domain
employees      | integer, with source and date
industry       | NAICS-aligned label
state/country  | US state code
trigger        | one sentence with the source URL
source_url     | where the fact came from
researched_on  | ISO date
```

Every row in a scored sheet must have a source URL and a date. A row without
them is not research, it is a guess.
