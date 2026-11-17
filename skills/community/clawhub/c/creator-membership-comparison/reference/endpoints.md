# creator-membership-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 2 platform group(s).**

## Patreon (3)

### `patreon_creator`

- **HTTP:** `GET /patreon/creator`
- **What:** Get a public Patreon creator profile. Returns public profile metadata from a creator's Patreon page: creator identity, summary, images, membership and creation counts, public earnings snapshot, membership/RSS availability flags, and public external profile links. handle is the creator's page handle, e.g. CachyOS for patreon.com/CachyOS.
- **Params:** `handle` (string, **required**) — Creator page handle

### `patreon_creator_tiers`

- **HTTP:** `GET /patreon/creator/tiers`
- **What:** Get a creator's public Patreon membership tiers. Returns published membership tiers and their published benefits from a creator's public Patreon page. It excludes member-only entitlements, tier capacity, and member counts. handle is the creator's page handle, e.g. CachyOS for patreon.com/CachyOS.
- **Params:** `handle` (string, **required**) — Creator page handle

### `patreon_explore`

- **HTTP:** `GET /patreon/explore`
- **What:** Browse public Patreon creators by topic. Returns Patreon's public curated creator shelves for one topic: Top creators, Popular this week, and New on Patreon. topic must be one of podcasts_and_shows, visual_arts, tabletop_games, video_games, music, lifestyle, writing, handicrafts, apps_and_software, social_impact.
- **Params:** `topic` (string, **required**) — Public Explore topic. Allowed values: podcasts_and_shows, visual_arts, tabletop_games, video_games, music, lifestyle, writing, handicrafts, apps_and_software, social_impact

## Substack (4)

### `substack_categories`

- **HTTP:** `GET /substack/categories`
- **What:** List Substack categories. Returns every public Substack category, with the category id required by /substack/category. Ids span two spaces: 32 categories use a numeric id and one uses the string id `podcast`. Both are accepted by /substack/category.
- **Params:** _none_

### `substack_category`

- **HTTP:** `GET /substack/category`
- **What:** List the publications ranked in one Substack category. Returns one page of a category's public publication leaderboard. Each row carries the publication's subscriber signals and its full subscription offering (web plans with multi-currency pricing, App Store plans, and per-tier benefits). Subscriber totals are published to roughly three significant figures and are opt-in per writer; paid subscriber figures are only ever buckets. Upstream serves 25 publications per page and accepts pages 0-26, so at most 675 publications are reachable per category and type.
- **Params:** `category_id` (string, **required**) — Category id from /substack/categories. Numeric for 32 categories, or the string podcast.; `page` (integer, optional) — Zero-based page, 0-26; `type` (string, optional) — Ranking to read

### `substack_publication`

- **HTTP:** `GET /substack/publication`
- **What:** Get a Substack publication and its subscription offering. Returns a publication's public profile and its complete subscription offering: every purchasable web plan with per-currency pricing, the separately priced App Store plans, per-tier benefit copy, and the toggles governing which tiers are sold. Identify the publication by name (a subdomain such as semianalysis, or a custom domain such as www.thefp.com) or by numeric publication_id -- exactly one is required. Prefer publication_id when you have it: it reads a compact document, while resolving by name has to parse the publication's full homepage.
- **Params:** `publication` (string, optional) — Publication subdomain or custom domain. Provide this or publication_id.; `publication_id` (integer, optional) — Numeric publication id. Cheaper than resolving by name. Provide this or publication.

### `substack_search`

- **HTTP:** `GET /substack/search`
- **What:** Search posts and publications across Substack. Searches posts across all of Substack and returns the publications that also matched, unlike /substack/publication/posts which searches within a single publication. Set focus_publication_id to additionally receive that one publication's own matching posts in focused_posts alongside the site-wide results.
- **Params:** `focus_limit` (integer, optional) — Cap on focused_posts, 1-20. Requires focus_publication_id.; `focus_publication_id` (integer, optional) — Numeric publication id whose own matching posts are returned in focused_posts; `page` (integer, optional) — Zero-based page, 20 posts per page; `query` (string, **required**) — Search text
