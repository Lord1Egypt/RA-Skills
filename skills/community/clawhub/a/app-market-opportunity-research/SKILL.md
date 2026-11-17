---
name: app-market-opportunity-research
description: Research app-market opportunities using Crawlora app catalogs, historical charts, live store listings, release notes, reviews, and Google Trends. Use for app niche assessments, competitor maps, chart-movement analysis, and evidence-backed unmet-need hypotheses.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# App market opportunity research

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Assess a defined app niche using competing products, observed distribution
signals, release activity, and customer evidence. Separate an opportunity
hypothesis from demonstrated demand, market size, or a revenue forecast.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
selected dataset, store, review, and Trends calls.

## Map the niche and test the signals

1. Define the user problem, storefront/country, device, language, and comparison
   period. Discover candidates with `/datasets/apps/search` and relevant live
   App Store/Google Play searches and similar-app results. Validate actual product
   capabilities; search rank and category membership alone do not prove rivalry.
2. Resolve store identities: iOS numeric track ID versus bundle ID, and Android
   package name. Verify publisher/official site before merging cross-store apps.
   Preserve country/device variants. The apps dataset uses repeatable `platforms`
   filters; chart history uses singular `platform` for iOS only. Missing platform
   classifications mean unknown coverage, not incompatibility.
3. For `/datasets/apps-charts/search`, hold store, country, chart type, category,
   and device constant. `chart_type` is `top_free`, `top_paid`, `top_grossing`, or
   `new`; underlying store collection names differ. An ordinary request resolves
   the latest available `snapshot_date`, which may lag today. For app history,
   pass exact `app_id` with `sort=date_desc` and omit `date`.
4. Compare ranks only within the same chart definition and dates. Deduplicate
   chart × snapshot × app observations. Missing dates or absent chart entries
   mean unobserved/unranked within coverage, not rank zero or zero downloads.
   Do not infer download/revenue volumes from ordinal ranks or cross-store ranks.
5. Refresh a bounded shortlist with `/appstore/app` and `/googleplay/app`.
   Dataset `price_cents` is in cents; do not compare it directly with live-store
   prices in major currency units. Compare currency, subscriptions/in-app purchases,
   rating counts, positioning, and updates. A free install is not free ongoing
   use. iOS has no install count here; Android install figures are not current
   monthly active users. Use `/appstore/version-history/{id}` for numeric iOS
   IDs; Google Play's latest update field alone is not a full release history.
6. Read a comparable review sample from each product. App Store reviews use
   `country`, `sort=mostRecent`, and pages; Google Play uses `country`, `lang`,
   `sort=newest`, `num`, and returned pagination tokens. Count unique eligible
   reviews by theme (`n/N`), keep dates/version/source, and link short excerpts.
   A complaint frequency in a selected sample is not population prevalence.
7. Use Google Trends only when it adds evidence about the underlying problem.
   Discover values through `/google/trends/enums`, `/locations`, and `/categories`
   under the same prefix. POST flat JSON to `/google/trends/explore/interest-over-time`
   with 1–5 `keywords`, `geo`, `time_range`, and `type=web`. Compare terms in one
   request; scores are relative, not app installs or absolute demand.

```sh
scripts/crawlora.sh /datasets/apps/search \
  q="habit tracker" store=ios country=us page_size=5
scripts/crawlora.sh /datasets/apps-charts/search \
  store=ios app_id=6448311069 country=us platform=phone \
  chart_type=top_free sort=date_desc page_size=20
```

## Synthesize an opportunity brief

Return the user problem, competitor matrix, matched chart trajectories, release
evidence, review themes, and gaps. For each opportunity hypothesis, show supporting
and conflicting evidence plus a concrete next validation step. Keep data freshness,
sampling bounds, unknowns, and assumptions visible.

- Do not turn a small indexed category count into a total market size, or a
  review/rank spike into proof that a particular release caused growth.
- Store labels and category IDs differ; use returned values and included discovery
  calls rather than transferring Apple's numeric IDs to Google Play.
- Keep Trends normalization and missing-data flags; separate independently scaled
  requests. See [Google's data FAQ](https://support.google.com/trends/answer/4365533?hl=en).
- Dataset pages max at 100 with a 10,000-result window. Stop on repeated pages or
  tokens. Back off on `429`, retry transient `5xx` once, stop on `401`/`403`, and
  check application `code`. Report unavailable sources without inventing results.
