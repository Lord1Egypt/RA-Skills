---
name: design-platform-search
description: Run public design search flows on Dribbble, Pinterest, and Behance without login, and extract normalized result fields such as title, search-page cover image, author, source URL, and publish time when available. Use when Codex needs a reusable method for public inspiration retrieval across major design platforms, especially when the collection strategy should stay lightweight and search-page-first.
---

# Public Design Search

Use public search pages as the primary source of truth and keep the workflow login-free.

## Workflow

1. Choose search tags.
   - Prefer English tags for these three platforms unless a platform clearly supports another language.
   - Load [references/tag-taxonomy.md](references/tag-taxonomy.md) for generic tag-selection guidance and example category/tag patterns.
   - Keep tag choice independent from platform-specific extraction logic.

2. Build public search URLs.
   - Dribbble: `https://dribbble.com/search/<urlencoded-tag>`
   - Pinterest: `https://www.pinterest.com/search/pins/?q=<urlencoded-tag>&rs=typed`
   - Behance: `https://www.behance.net/search/projects?search=<urlencoded-tag>`

3. Collect candidate cards from the search page.
   - Prefer browser automation over raw HTTP for all three platforms.
   - Normalize search-card fields first: `title`, `source_url`, `cover_image_url`, `summary`, `author_name` when exposed, and `raw_metrics` when exposed.

4. Backfill sparingly.
   - Default: keep the search-page `cover_image_url`.
   - Use detail pages primarily for `publish_time`.
   - Only backfill `author_name` when the search card exposes nothing and the request budget allows it.
   - On constrained servers or proxy-heavy environments, disable Pinterest detail backfill entirely and rely on search-page results.

5. Return a normalized public-only record.
   - Keep unstable fields nullable.
   - Record the input tag or matched tag set when useful.
   - Do not fabricate authors, publish times, or engagement metrics.

## Extraction Priorities

- `title`: search-card title first, then safe public meta/title fallback.
- `cover_image_url`: search-page image first; only do light URL upgrades when the site uses obvious small fixed-size variants.
- `author_name`: search-card author first; leave `Unknown` if public search does not expose it reliably.
- `publish_time`: detail-page public metadata when available; otherwise `null`.
- `summary`: normalized title or short public snippet.

Platform-specific rules live in:

- [references/platform-methods.md](references/platform-methods.md)
- [references/tag-taxonomy.md](references/tag-taxonomy.md)

## Network Guidance

- Pinterest and Behance may require VPN or proxy access in restricted regions.
- Browser traffic may work best through SOCKS5 while image download or pHash download may need an HTTP proxy.
- Verify network reachability before changing selectors.
- If a platform is reachable only through unstable proxies, reduce detail backfill before changing the tag set.

## Guardrails

- Public pages only. No login-only APIs, cookies, or authenticated sessions.
- Prefer search-page fields over detail scraping whenever they are good enough.
- Do not chase high-resolution cover images unless the search-page image is clearly unusable.
- Treat missing metrics as normal.
- Expect DOM drift and anti-bot behavior.
- These three platforms are effectively English-first in most reusable workflows.

## Output Shape

Normalize results into a shape close to:

```json
{
  "title": "",
  "platform": "dribbble|pinterest|behance",
  "source_url": "",
  "cover_image_url": "",
  "author_name": "",
  "publish_time": null,
  "keyword": "",
  "matched_tags": []
}
```
