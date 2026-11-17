---
name: entertainment-discovery-research
description: Researches movies and TV titles across IMDb, TMDB, JustWatch, Rotten Tomatoes, and Metacritic using the Crawlora API. Use for title discovery, cast and crew, ratings, critic and audience reviews, streaming offers, similar titles, and release comparisons.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Entertainment discovery research

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Find and compare movies and TV shows across public IMDb, TMDB, JustWatch,
Rotten Tomatoes, and Metacritic data. Use the source that fits the question,
then preserve each platform's title ID, score definition, locale, and retrieval
time in the result.

## When to use this skill

- Identify a title, person, cast member, season, or episode.
- Compare critic and audience scores across sources.
- Find where a title is streaming, rentable, or purchasable in a region.
- Discover similar titles, popular releases, genres, or review themes.

## Research workflow

1. Search first on IMDb or TMDB and keep the returned source ID. Do not assume
   an IMDb ID, TMDB ID, JustWatch ID, or Metacritic slug can be substituted.
2. Fetch title, credits, ratings, and reviews from the relevant source. Keep
   critic scores, audience scores, star ratings, and review counts as separate
   measures; they are not interchangeable.
3. Use JustWatch search or title-by-id to resolve its raw ID before requesting
   offers, similar titles, media, or provider lists. State the country/locale.
4. Compare matched titles by release year, type, season, and edition. A review
   sample or provider snapshot does not establish overall popularity or quality.

## Examples

```sh
scripts/crawlora.sh /imdb/search query="Dune Part Two" | jq '.'
scripts/crawlora.sh /tmdb/search query="Dune Part Two" | jq '.'
scripts/crawlora.sh /justwatch/search query="Dune Part Two" | jq '.'
scripts/crawlora.sh /justwatch/title/offers id=<justwatch-id> country=us | jq '.'
scripts/crawlora.sh /metacritic/movie/dune-part-two/critic-reviews | jq '.'
```

## Notes and limits

- Public metadata and review pages only; no playback, purchase, account, or
  subscription actions are performed.
- Streaming offers vary by country, date, plan, and provider. Record the
  requested locale and retrieval time.
- Avoid averaging scores across platforms unless the score definitions and
  denominators are explicitly preserved.
- Missing credits, reviews, or offers mean unavailable coverage, not zero.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.
