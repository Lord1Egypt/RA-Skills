---
name: competitor-intelligence
description: Compare companies or products using Crawlora website extraction, traffic estimates, reviews, product listings, and hiring data. Use for competitor briefs, positioning and pricing comparisons, or evidence-backed competitive battlecards.
---

# Competitor intelligence

Produce a comparison that separates company claims, third-party observations,
and your interpretation. Choose sources for the user's decision; a short pricing
comparison does not require every source in this skill.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1` and prints JSON.
Keep the key in the environment. Read [reference/endpoints.md](reference/endpoints.md)
for the selected tools and their exact parameters.

## Workflow

1. Establish the competitors, audience/use case, market, and decision criteria.
   If only a category is supplied, use Bing or Product Hunt search to propose a
   small candidate set and explain the selection. Resolve each official domain,
   product, parent company, and regional variant before combining evidence.
2. Read official product/pricing pages with `/web/scrape`, or extract specific
   fields with `/extract`. Both use flat JSON bodies (`url` plus `formats`, or
   `url` plus `schema`), not the catalog's body-label wrapper. Preserve billing
   interval, currency, per-seat/usage basis, minimum commitments, promotional
   conditions, and retrieval date. Missing published pricing means unknown.
3. Add only the sources relevant to the brief:

   | Evidence | Discovery and follow-up |
   |---|---|
   | Product positioning | `/producthunt/search` with `query`, then the returned product ID's detail/alternatives/launches |
   | Business reputation | `/trustpilot/business-units/search` with `q`, then the returned business slug's detail/reviews |
   | Software feedback | `/capterra/search` with `q`, then `/capterra/product` and `/product/reviews` with `product_id` |
   | Traffic | `/similarweb/search` to resolve a domain, then `/similarweb/web/{domain}` |
   | Hiring | `/datasets/jobs/companies` with `q`, then `/datasets/jobs/search` with `company`; verify domain/name before attribution |

4. Build a claim ledger: competitor, dimension, claim, source URL, source date,
   retrieval time, and evidence type. Verify disputed/high-impact claims against
   the primary page. Retain disagreements and unknowns rather than averaging
   incompatible numbers or treating marketing language as measured performance.
5. Return the requested brief or comparison matrix, followed by the supported
   advantages, gaps, and questions that remain. Link each material claim to its
   source. Prioritize findings by the user's use case, not a universal score.

```sh
scripts/crawlora.sh /producthunt/search query="project management"
scripts/crawlora.sh /datasets/jobs/companies q=Atlassian page_size=5
```

## Interpretation and bounds

- SimilarWeb figures are estimates. Compare the same period, geography, and
  device scope where returned; visits are not customers, revenue, or market share.
- Job listings are hiring signals, not proof of headcount growth or buying intent.
  Indexed listings may be stale. Mark dataset observations separately from live checks.
- Reviews are selected samples. Record source, rating filters, dates, and sample
  size; a complaint theme is not a measured defect rate across all customers.
  Trustpilot date filters are currently rejected upstream: filter returned dates
  locally and disclose the pages examined instead of passing `date_from`/`date_to`.
- Product Hunt alternatives and search rankings aid discovery, not proof that
  products serve the same audience. Check actual capabilities on official pages.
- Bound pages and enrichments to the brief. Retry a transient `5xx` once and
  back off on `429`; stop on `401`/`403`. Check application `code` before using
  `data`. Preserve successful sources and identify missing ones.
- A one-time brief does not create monitoring jobs or send material to others.
  Set up recurring tracking or distribution only when requested.
