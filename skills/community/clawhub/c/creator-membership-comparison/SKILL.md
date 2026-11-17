---
name: creator-membership-comparison
description: Compare public Patreon tiers and Substack subscription plans through Crawlora. Use for a creator membership shortlist or offer benchmark with creator identity, published benefits, currency, cadence, web/in-app pricing, disabled plans, and hidden-count limits preserved.
---

# Creator membership comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare the public offers of selected creators/publications against the user's
content interests, benefits, budget/currency, and billing preferences. Public
benefit copy describes an advertised offer, not verified delivery or satisfaction.

## Resolve creators and active public offers

1. Discover Patreon creators by supported topic or use supplied handles. Resolve
   profile/handle identity and canonical URL before tiers. For Substack search or
   supplied publications, use exactly one of publication/name/domain or numeric
   publication ID; prefer a returned ID when available. A writer profile is not
   automatically the publication that sells a particular plan.
2. Fetch public Patreon creator tiers and the Substack publication's subscription
   object. Preserve tier/plan ID, title, declared benefits, amount/currency,
   cadence/interval count when available, active/disabled flags, platform, and
   source time. Patreon returns published tier benefits; member-only entitlements,
   capacity, and per-tier counts are unavailable. Missing cadence remains unknown.
3. Keep Substack web plans separate from App Store in-app SKUs and founding plans.
   `monthly_disabled`/`annual_disabled` can matter even when a plan is present;
   a stored plan object is not necessarily currently purchasable. Group discounts,
   trials, pledges, and invitations describe their own conditional offerings.
4. Amounts labeled cents use that declared scale and plan currency. Use an actual
   offered matching-currency price where possible, or a disclosed dated conversion
   basis. Never compare mixed currencies or infer taxes, fees, shipping, payment
   rules, or a subscriber's personalised checkout total from a base price.

```sh
scripts/crawlora.sh /patreon/explore topic=apps_and_software
scripts/crawlora.sh /substack/search query="software engineering" page=0
# Resolve returned creator/publication identity before offers:
# scripts/crawlora.sh /patreon/creator/tiers handle="$HANDLE"
# scripts/crawlora.sh /substack/publication publication_id="$PUBLICATION_ID"
```

## Build an offer and benefit matrix

Keep free, paid, founding, web, and in-app tiers distinct. Show total commitment
and renewal interval before a monthly equivalent: for a verified annual plan,
`monthly equivalent = plan amount / (12 × interval_count)` on the same currency
basis. That equivalent is not a month-to-month offer. Do not assume every Patreon
base tier price uses the same cadence or annual discount as a Substack plan.

Map advertised benefits to the user's requirements using supported, unclear,
and absent-from-public-copy states, with source excerpts. Community access,
physical perks, bonus content, archive access, and calls are different benefits;
missing public copy is not proof a private tier lacks them. Ratings/popularity
and public member/earnings snapshots do not verify fulfilment or future value.
Substack `total_hidden` differentiates a hidden count from zero; rough paid tiers
are not exact subscriber totals or revenue. Per-tier popularity is not available
from Patreon tier data.

Return creator/publication identity and offer matrices, billing/currency basis,
conditional/disabled offers, unmet evidence needs, and the user's fit tradeoffs.
Do not infer creator ownership from similar branding, fetch member-only content,
subscribe/pay, message creators, or change accounts from a comparison request.
