---
name: douban-self-taste-skill
description: Collect, refresh, normalize, and analyze the user's own Douban history for taste analysis and recommendation reasoning. Use when the task involves the user's own Douban shelves, ratings, tags, comments, reviews, or recent activity, especially when you need to decide whether local cache is fresh enough, re-crawl logged-in data with cookies, store refreshed results locally, and then analyze them by category.
---

# Douban Self Taste Skill

Collect the user's own Douban history, keep a local cache fresh, and analyze it carefully.

## Scope

Use this skill only for the user's own Douban data, including:

- the user's own movie / book / music / game shelves
- the user's own ratings, tags, short comments, reviews, and dates
- local exports, saved HTML pages, or cached JSON derived from the user's own account
- fresh re-crawls of the user's own logged-in pages when cache is missing or stale

Do not use this skill for public-user scraping, whole-site crawling, hidden/private data claims, or MCP-server design.

## Storage layout

Use these paths unless the user explicitly asks for a different layout:

- cookies: `.local/douban-self-taste/cookies/douban_cookies.json`
- crawl cache: `.local/douban-self-taste/cache/collections/`
- analysis outputs: `.local/douban-self-taste/analysis/`

Treat the cache as reusable local working data. Do not scatter generated files across the repo.

Read `references/storage-layout.md` for exact file naming conventions.

## Required workflow

Follow this order.

### 1. Decide whether crawling is needed

Check whether local crawl cache already exists for the requested category.

- If no cache exists, crawling is needed.
- If cache exists but its `fetched_at` timestamp is older than 7 days, crawling is needed.
- Otherwise, reuse the local cache.

Prefer the smallest sufficient refresh.

- If the user asks about books, prioritize book cache.
- If the user asks about movies, prioritize movie cache.
- You may use small amounts of other categories as weak supplementary context, but keep the requested category primary.

### 2. If crawling is needed, verify cookie availability

Check whether the cookie file exists and is plausibly usable.

Treat cookies as unavailable when:

- the cookie file is missing
- the cookie file is empty or malformed
- the crawl clearly redirects to login or otherwise fails due to authentication

If cookies are unavailable or expired, ask the user for fresh cookies before crawling.

Do not pretend a crawl succeeded when authentication failed.

### 3. Crawl and persist locally

When cookies are available, crawl the user's own Douban shelves and store the refreshed result in local JSON cache files.

Use `scripts/crawl_douban_self_history.py` for logged-in crawling.
Use `scripts/extract_douban_self_history.py` when the user already has saved HTML files.

After crawling:

- save normalized JSON to the cache directory
- include `fetched_at`
- keep category and status explicit
- preserve raw comments and rating information

### 4. Analyze after data is ready

Only start analysis after confirming that either:

- fresh cache exists, or
- a successful new crawl has been saved locally

Use `scripts/build_taste_profile.py` to build an analysis-ready summary when helpful.
Write the summary into `.local/douban-self-taste/analysis/` when the user wants a reusable analysis artifact.

## Analysis priorities

Always pay extra attention to:

- items with comments
- high-rated items
- low-rated items
- recent items
- category boundaries

For `scripts/build_taste_profile.py`, use these summary rules:

- Do not include the full `items` array in the profile output; keep full records in the crawl cache.
- Keep the rest of the summary reasonably rich; avoid large deletions unless the user asks.
- Define `recent_items` as the newest dated items sorted by date descending, capped at 20 items.
- Define `high_rated_items` as all items tied at the user's highest observed rating within the focused dataset; if there are more than 20, keep only the most recent 20 by date.
- Define `low_rated_items` as all items tied at the user's lowest observed rating within the focused dataset; if there are more than 20, keep only the most recent 20 by date.
- Treat game tag analysis separately from creator analysis; games may have useful genre/platform-like tags but often do not have reliable creators.
- Filter noisy book creators when obvious publisher / bookstore / distribution-style strings appear.
- Prefer category-specific cleaning over one generic parser when extracting tags or creators.

When the user asks about one category, analyze that category first.

Examples:

- Book questions → use books as primary evidence; only lightly reference movies/music/games if they add meaningful support.
- Movie questions → use movies as primary evidence.

Separate:

- stable preferences
- weak signals
- aversions / anti-preferences
- recent shifts

Do not overfit from tiny samples.

## Output expectations

Start with factual scope:

1. what data was used
2. whether it came from cache or a fresh crawl
3. cache age
4. category coverage
5. obvious data gaps

Then provide analysis.
Keep generated profile files compact enough for downstream LLM analysis; prefer concise summaries over repeating the entire dataset.

## Bundled resources

- Read `references/storage-layout.md` for local file locations.
- Read `references/data-sources.md` for cache/cookie refresh logic.
- Read `references/output-schema.md` for normalized JSON structure.
- Read `references/analysis-rubric.md` before writing conclusions.
- Use `scripts/crawl_douban_self_history.py` to refresh local cache from logged-in pages.
- Use `scripts/extract_douban_self_history.py` to convert saved HTML files into normalized JSON.
- Use `scripts/build_taste_profile.py` to generate category-aware summaries.
