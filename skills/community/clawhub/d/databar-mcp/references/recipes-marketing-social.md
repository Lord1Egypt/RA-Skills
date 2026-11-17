# Databar Recipes — Marketing, SEO & Social

Concrete recipes for marketing and social workflows. Enrichment IDs and prices were **verified August 2026** — always re-verify with `search_enrichments` before running; the catalog changes and prices shift. Waterfall identifiers (`email_getter`, etc.) are stable.

## Recipe M1 — Competitor keyword teardown (SEO + PPC)

Goal: know exactly what a competitor ranks for, buys, and is losing.

1. `search_enrichments(query="SEO keywords")` → SpyFu family: top SEO keywords (#971), PPC keywords (#900), lost-rank keywords (#904), newly-ranked (#903/#1378), transactional keywords by topic (#1484), top SEO competitors (#902). All 1–2 credits — cheap enough to run per competitor.
2. `run_bulk_enrichment` across a competitor domain list, or attach to a table's `domain` column.
3. Read `lost ranks` on a competitor + `newly ranked` on your own domain to find takeover gaps; `transactional keywords by topic` for landing-page/campaign targets.

## Recipe M2 — Ad-intelligence sweep

Goal: see what competitors are actually running.

1. `search_enrichments(query="ad library")` → LinkedIn ad library search (#1272) by keyword or company — active and past campaigns.
2. Combine with Recipe M1's PPC keywords: ads + paid keywords = the competitor's live acquisition strategy.
3. For brand-level social stats (follower counts, bios across platforms), `get brand social media data` (#716).

## Recipe M3 — Social listening & content mining

Goal: audience language, trending formats, engagement patterns.

1. X/Twitter: popular tweets by handle (#1294, 100 tweets), tweet details by link (#1295). Study what an influencer's audience actually engages with.
2. LinkedIn: search posts by keyword (#1929/#327 — text, author, likes, comments, date), person's posts (#1927), company page posts (#1928).
3. Reddit: search posts (#1273) or pull a subreddit's recent posts with engagement (#1274) — complaint threads and "what should I buy" posts are demand signals.
4. TikTok: profile data (#1243) for creator vetting and format research.
5. Telegram: posts by channel (#1102) for niche/community intel.
6. Hacker News: items by id (#15) — build-in-public and dev-tool conversation raw material.

## Recipe M4 — Review mining for positioning

Goal: what customers praise and hate about competitors.

1. `search_enrichments(query="reviews")` → Trustpilot (#721, 0.15 cr), Capterra (#1487, 1 cr), Google Play (#606, 2 cr), Shopify app reviews (#757, 8 cr).
2. `run_bulk_enrichment` on competitor product slugs/domains.
3. Cluster complaints by theme — recurring one-star reasons are your marketing angles and product roadmap in one pull. Google Play reviews are also a ready-made source of feature-request language for landing pages.

## Recipe M5 — E-commerce price & product watch

Goal: track competitor pricing, catalogue, and SKU movements.

1. Product details from any online store (#13, 1 cr) or by URL on Amazon (#95, 1 cr); Google Shopping keyword results (#144) and by GTIN/EAN (#56).
2. Table with a `product_url` column + attached enrichment + scheduled re-run with `run_strategy="run_all"` (fresh prices bill every run — price the cadence deliberately) → exporter to Sheets for a price dashboard.
3. `get brand social media data` (#716) adds follower trajectory next to pricing moves.

## Recipe M6 — News & PR monitoring

Goal: know when target companies make moves worth reacting to.

1. Company news feeds (Owler #697, 4 cr; PredictLeads #680, 7 cr — categorized: investments, acquisitions, partnerships) by domain.
2. Public companies: press releases (#1126) and stock news (#1119) by ticker, 1 cr each.
3. Attach to a target-company table on a schedule; funding and partnership events are outreach timing triggers ("congrats on the raise" emails land while the news is warm).

## Cross-cutting rules

- Price the full chain before running (see Cost discipline in SKILL.md).
- Bulk results are position-aligned — keep input order.
- Nothing is deleted without explicit instruction; `delete_*` tools are permanent.
- Respect platform ToS and privacy law for any contact or content data you collect.
