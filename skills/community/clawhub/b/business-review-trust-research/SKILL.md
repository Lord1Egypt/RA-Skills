---
name: business-review-trust-research
description: Researches software/SaaS products, business reputation, and crowdfunding campaigns via the Crawlora API — Product Hunt launches/makers/alternatives, Trustpilot business reviews, TrustMRR revenue-verified startups, Capterra software reviews, BBB (Better Business Bureau) business profiles/complaint history/Scam Tracker reports, and Kickstarter campaign discovery/funding/updates/comments — returning clean JSON. Use when the user wants a product's launch/review history, a company's Trustpilot or BBB reputation, a startup's verified revenue, software alternatives/reviews before buying, or a crowdfunding campaign's funding status and backer updates.
---

# Business & software review research

Look up product launches, business reputation, verified startup revenue,
software reviews, and crowdfunding campaigns across six platforms as
normalized JSON from the Crawlora API — no scraping review-site pages.

## When to use this skill

- "What did this product launch as on Product Hunt? Who made it?"
- "What are people saying about <company> on Trustpilot?"
- "How much revenue does this startup actually make?" (TrustMRR — payment-provider-verified)
- "What are the reviews / alternatives for this software?" (Capterra)
- "Is this business BBB accredited? What's its rating, and any complaints or scam reports against it?" (BBB)
- "How's this Kickstarter campaign doing? What updates has the creator posted?"
- Vendor due-diligence before buying or partnering.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Product Hunt** — `/producthunt/search` (`query`) to find a product
   `id`; `/producthunt/product/{id}` for detail (+ `/about`, `/makers`,
   `/launches`, `/reviews`, `/alternatives`, `/customers`).
   `/producthunt/leaderboard` and `/producthunt/category/{slug}/products`
   cover browsing/trending.
2. **Trustpilot** — `/trustpilot/business-units/search` (`q`) to find a
   business `slug`; `/trustpilot/business/{slug}` for the profile (+
   `/reviews`, `/related`). `/trustpilot/categories` / `/categories/search`
   browse by industry.
3. **TrustMRR** — `/trustmrr/startups` to browse, or `/trustmrr/startup/{slug}`
   for one company's payment-provider-verified revenue profile (see also
   the `crawlora-datasets` skill's `trustmrr` dataset for bulk/aggregate
   queries). `/trustmrr/leaderboard` ranks by MRR; `/trustmrr/categories`
   browses by category.
4. **Capterra** — `/capterra/search` (`q`) to find a `product_id`, then
   `/capterra/product` for detail and `/capterra/product/reviews` for user reviews.
5. **BBB (Better Business Bureau)** — `/bbb/search` (`q`) to find a business
   profile URL, then `/bbb/business` for the profile (rating, accreditation)
   plus `/bbb/business/reviews`, `/bbb/business/complaints`, and
   `/bbb/business/more-info` for rating reasons and service area.
   `/bbb/category` browses by industry; `/bbb/scamtracker/search` and
   `/bbb/scamtracker/{id}` cover consumer-reported scam listings, with
   `/bbb/scamtracker/state-stats` for state/province aggregates.
6. **Kickstarter** — `/kickstarter/discover` (`term` free-text and/or
   `category_id`, plus `state`/`sort`/`staff_pick_only`) to browse or
   search campaigns, then `/kickstarter/project` (`creator`+`slug`, both
   the corresponding path segments of the campaign URL) for the funding
   snapshot (goal, pledged, percent funded, backers, status).
   `/kickstarter/updates` and `/kickstarter/comments` (same `creator`+`slug`)
   cover the creator's update feed and the campaign's comment thread.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Product Hunt:
scripts/crawlora.sh /producthunt/search query="AI coding assistant" | jq '.'

# Trustpilot:
scripts/crawlora.sh /trustpilot/business-units/search q="acmecorp.com" | jq '.'
scripts/crawlora.sh /trustpilot/business/acmecorp.com/reviews | jq '.'

# TrustMRR:
scripts/crawlora.sh /trustmrr/leaderboard | jq '.'

# Capterra:
scripts/crawlora.sh /capterra/search q="project management software" | jq '.'

# BBB:
scripts/crawlora.sh /bbb/search query="plumbing" location="Austin, TX" | jq '.'

# Kickstarter:
scripts/crawlora.sh /kickstarter/discover term="board game" | jq '.'
scripts/crawlora.sh /kickstarter/project creator=<creator-slug> slug=<project-slug> | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Product
Hunt, Trustpilot, TrustMRR, Capterra, BBB, and Kickstarter endpoint this
skill uses.

## Examples

- **Vendor due diligence:** `/trustpilot/business/{slug}` (reputation) +
  `/capterra/product` + `/capterra/product/reviews` (feature-level
  feedback) before signing a software contract.
- **Launch retrospective:** `/producthunt/product/{id}` + `/launches` +
  `/makers` to see how a product performed and who built it.
- **Bootstrapped-revenue research:** `/trustmrr/startup/{slug}` for one
  company's verified MRR trend, or `/trustmrr/leaderboard` for the top
  earners in a category.
- **Local-business trust check:** `/bbb/search` + `/bbb/business` (rating,
  accreditation) + `/bbb/business/complaints` before hiring a contractor
  or vendor; cross-check `/bbb/scamtracker/search` for reported scams.
- **Campaign due diligence:** `/kickstarter/project` (funding snapshot) +
  `/kickstarter/updates` (has the creator been communicating?) before
  backing a campaign.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public listing/review pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Trustpilot's `slug` is usually the business's domain** (e.g.
  `acmecorp.com`), not a display name — resolve via
  `/trustpilot/business-units/search` if unsure.
- **Kickstarter's `creator`+`slug` are the two path segments of a project
  URL** (`kickstarter.com/projects/{creator}/{slug}`) — copy them directly
  from a campaign link or a `/kickstarter/discover` result rather than
  guessing.
- Reviews/lists are paginated — pass `page` to walk beyond the first page.
