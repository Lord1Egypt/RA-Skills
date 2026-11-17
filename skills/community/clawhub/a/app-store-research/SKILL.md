---
name: app-store-research
description: Researches apps and browser extensions across the Apple App Store, Google Play, and Chrome Web Store using the Crawlora API, returning clean JSON. Use for app discovery, publisher and product comparisons, ratings and reviews, permissions, privacy, similar products, rankings, and release-history research.
---

# App store research

Compare public app and extension listings across the Apple App Store, Google
Play, and Chrome Web Store as normalized JSON from the Crawlora API. Use this
skill for discovery and evidence gathering; it does not install software or
access private developer accounts.

## When to use this skill

- Find apps or extensions for a problem, category, publisher, or market.
- Compare ratings, review themes, similar products, rankings, and update history.
- Check public permissions, privacy disclosures, and data-safety statements.
- Build an app competitor map across iOS, Android, and Chrome.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper sends requests only to `https://api.crawlora.net/api/v1` and keeps
  the key out of command-line arguments.

## Research workflow

1. Search each store separately with `/appstore/search`, `/googleplay/search`,
   or `/chromewebstore/search`. Store identifiers are not interchangeable.
2. Resolve a candidate with its platform detail endpoint before comparing it.
   Apple uses numeric IDs, Google Play uses package names, and Chrome uses
   extension IDs or store URLs.
3. Pull reviews with the matching platform endpoint and preserve country,
   language, sort, page, and source. A selected review sample is not population
   sentiment.
4. Compare public ratings, rating counts, price, publisher, version/update
   dates, category, and platform availability. Do not infer downloads, revenue,
   retention, or market share from a rank or review count.
5. Use permissions, privacy, and data-safety endpoints as reported disclosures.
   They are evidence about the listing, not an independent security audit.

## Examples

```sh
scripts/crawlora.sh /appstore/search term="habit tracker" country=us | jq '.'
scripts/crawlora.sh /googleplay/search q="habit tracker" country=us | jq '.'
scripts/crawlora.sh /chromewebstore/search q="password manager" | jq '.'
scripts/crawlora.sh /appstore/reviews id=6448311069 country=us sort=mostRecent | jq '.'
```

## Notes and limits

- Public listings and reviews only; no installs, purchases, logins, or account
  actions are performed.
- Keep iOS numeric IDs, Android package names, and Chrome extension IDs in
  separate fields when joining records.
- Preserve country and language because store availability and review samples
  vary by locale.
- Stop on `401`/`403`, back off on `429`, and report missing or partial sources
  instead of treating them as zero results.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.
