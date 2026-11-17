---
name: customer-feedback-analysis
description: Analyze public customer reviews and discussions through Crawlora to identify complaint themes, feature requests, praise, and competitive gaps. Use for voice-of-customer briefs and product-feedback comparisons with cited examples and explicit sample counts.
---

# Customer-feedback analysis

Turn a bounded sample of customer feedback into traceable themes and hypotheses.
Keep reviews and social discussion distinct: a Reddit commenter is not necessarily
a customer, and sentiment in a sample is not a population satisfaction measure.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1` and prints JSON.
Keep the key in the environment. Read [reference/endpoints.md](reference/endpoints.md)
for supported sources, discovery endpoints, IDs, and pagination.

## Collect a comparable sample

1. Define the product(s), question, market/language, time window, and sample
   bound from the brief. Resolve exact products before collecting feedback.
   Keep app versions, product models, and company-wide service reviews separate.
2. Choose relevant sources, rather than querying all of them:

   | Source | Identity and collection details |
   |---|---|
   | App Store | Search with `term`; reviews require numeric `id` or bundle `app_id`. Pages 1–10; `sort=mostRecent` or `mostHelpful`; specify `country`. |
   | Google Play | Search/details resolve package `app_id`. Reviews use `num` (max 1000), `country`, `lang`, and `sort=newest`, `helpfulness`, or `rating`. Read rows under `data.data` and follow `data.next_pagination_token` only within the sample bound. |
   | Stored app reviews | `/datasets/apps-reviews/search` uses `store=ios` or `android`, exact `app_id`, and `page_size` (max 100). This is indexed feedback, not a live refresh. |
   | Trustpilot | Search for the business slug, usually its domain; collect `/trustpilot/business/{slug}/reviews`. Preserve star/language filters. Date filters are currently rejected upstream: filter returned dates locally and disclose collection coverage. |
   | Capterra | Resolve numeric `product_id` through search, then `/capterra/product/reviews` with `page`. |
   | Adidas | Resolve `products[].model_number` through search. Fetch review topics for that model before applying `topic`; reviews accept `rating`, `locale`, and `page`. |
   | Reddit | Search for relevant discussions, then retrieve the returned post ID and comments. Normal comment mode can be text; use `include_metrics=true` only when structured comment identities/metrics are needed, with its higher documented credit cost. |

3. Save source IDs/URLs, dates, product/version, rating scale, text, and collection
   filters. Deduplicate by source review ID; use normalized text plus date/product
   only as a fallback, and avoid counting syndicated copies twice. Exclude brand
   replies from the customer-review denominator and report exclusions.
4. Label each review with one or more specific themes and distinguish an explicit
   feature request from an inferred product opportunity. Separate praise and
   complaints. Keep mixed/unclear sentiment instead of forcing a binary label.
5. Count unique eligible reviews mentioning each theme. Report `n/N` with the
   definition of N, by source/product. Multiple themes per review mean totals
   can exceed N. Do not combine incompatible star scales or compare differently
   filtered samples as though they were controlled measurements.

```sh
scripts/crawlora.sh /googleplay/reviews \
  app_id=com.openai.chatgpt country=us lang=en sort=newest num=10
```

## Deliverable and interpretation

Return a theme table with theme, source/product, unique-review count/denominator,
short attributed examples and links, observed impact, and a proposed follow-up.
Include dates, filters, deduplication rules, gaps, and untested hypotheses.
Use brief excerpts rather than republishing review archives. Do not export
reviewer contact details; only retain author identifiers when needed for provenance.

- A star-filtered, keyword-filtered, or helpfulness-ranked sample is biased
  toward its selection rule. It cannot establish overall complaint prevalence.
- Missing dates cannot prove a review belongs in the requested window. Mark
  undated records separately. Do not call comments verified purchases.
- No repeated pagination token/page progress means stop. For indexed app reviews,
  respect the 10,000-result window; there is a minimum-score filter, not a maximum.
- Stop when the bound or source end is reached. Back off on `429`, retry a
  transient `5xx` once, and stop on `401`/`403`. App Store `404` can mean the
  app is absent from that storefront; do not repeatedly retry it. Check the
  application envelope before treating an empty response as no feedback.
