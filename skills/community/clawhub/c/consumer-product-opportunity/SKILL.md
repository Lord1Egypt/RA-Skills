---
name: consumer-product-opportunity
description: Assess a physical consumer-product idea using public search-interest signals, marketplace listings, and sampled customer feedback in a specified market. Use for product-launch hypotheses, not one-off shopping, market-size estimates, or profit forecasts.
---

# Consumer product opportunity

Evaluate a physical product idea with separate evidence for customer interest,
visible marketplace supply, and sampled customer complaints or praise. This is
a public-data screening workflow, not a substitute for Amazon's seller-only
Product Opportunity Explorer or a forecast of sales.

## Scope the decision

Start with the product concept, customer need, target country, likely selling
channel, important attributes, and acceptable price band. If the country or
channel is missing, state a narrow default such as Amazon US and avoid
generalizing the result to other markets. Keep size, material, capacity, bundle
count, and other variants explicit.

Use this skill for a physical consumer product launch or line-extension
hypothesis. For broad search or discussion demand without product listings, use
topic-demand-validation. For a one-off product or seller comparison, use
product-price-research. For matched catalogs from named retailers and a
user-supplied assortment, use retail-assortment-gap-analysis. Apps and SaaS use
app-market-opportunity-research or software-vendor-shortlisting.

## Collect demand and supply signals

1. Expand the user's seed phrase with Google Suggest and, when useful, Amazon
   autocomplete. Preserve the exact prefix and returned phrasing; completions
   are not search-volume estimates.
2. Compare at most five selected phrases in one Google Trends request. Hold the
   country, range, and search type constant. Trends scores are normalized and
   relative to that request; they are not query counts or product demand.
3. For Amazon, discover chart categories first. Use charts for a bounded rank
   sample, then search the same phrase and record distinct ASINs, prices,
   ratings, review counts, sponsored status, and any displayed bought-in-last-
   month label. A chart rank or label is only a platform signal, not units sold.
4. Cross-check a small sample on AliExpress or Jumia only when those storefronts
   serve the target market. AliExpress uses its anonymous US English/USD locale
   and returns sold text; retain that text as-is. Jumia requires a supported
   country and returns prices in that storefront's currency. Do not convert
   prices without a stated exchange-rate source and date.
5. Fetch detail or review evidence for a few representative products. Amazon
   detail can include inline review samples; AliExpress has a separate review
   page. Use Reddit search and selected post comments only to understand
   expressed needs, objections, or use cases. Record the search, date, and
   sample size; a small selected sample is not population sentiment.

## Interpret without inventing sales

- Treat search rank, visible listing counts, ratings, and review counts as
  separate observations. Marketplace search pages are ranked samples, not
  exhaustive category inventories.
- Amazon's public listing fields do not include the authenticated niche search,
  purchase, conversion, or return metrics in Product Opportunity Explorer.
  Do not claim access to those private seller metrics.
- A positive trend or high ranking does not prove demand for a particular
  variant. A low listing count may reflect query wording, filters, source
  coverage, or an unsupported market.
- Do not create a numeric opportunity score, sales estimate, margin forecast,
  or launch recommendation. State what supports, contradicts, or remains
  unknown about the hypothesis, then propose one concrete next validation step.

## Deliverable

Return a compact opportunity matrix with product attributes, market, query set,
retrieval dates, sampled listings, visible price ranges and currencies, demand
signals, review themes, and evidence limits. Separate observed facts from the
launch hypothesis. Do not advise the user to buy inventory, invest, or enter a
market based on these proxies alone.

~~~sh
scripts/crawlora.sh /google/suggest q='insulated lunch bag' source=shopping
scripts/crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["insulated lunch bag","thermal lunch tote"],"geo":"US","time_range":"today 5-y","type":"web"}'
scripts/crawlora.sh /amazon/charts/categories chart=best_sellers
scripts/crawlora.sh /amazon/charts chart=best_sellers department=DEPARTMENT_FROM_CATEGORIES
scripts/crawlora.sh /amazon/search k='insulated lunch bag'
scripts/crawlora.sh /amazon/suggest/mug | jq '.'
scripts/crawlora.sh /aliexpress/search q='insulated lunch bag'
scripts/crawlora.sh /jumia/countries
scripts/crawlora.sh /jumia/search country=ng q='insulated lunch bag'
scripts/crawlora.sh /reddit/search q='insulated lunch bag review' sort=comments time=year
~~~
