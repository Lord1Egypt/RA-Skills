---
name: book-research
description: Researches books, authors, and audiobooks via the Crawlora API — Goodreads (books, authors, reviews, lists, quotes), Apple Books (books, audiobooks, series, reviews, charts), and Audible (audiobook catalog search, product detail, narrators/series, reviews, charts, editorial lists) — returning clean JSON. Use when the user wants a book's ratings/reviews, an author's bibliography, curated reading lists, or audiobook details and charts.
---

# Book & audiobook research

Look up books, authors, reviews, and audiobooks across Goodreads, Apple
Books, and Audible as normalized JSON from the Crawlora API — no scraping
book-catalog pages.

## When to use this skill

- "What's the rating / reviews for this book?"
- "What has this author written?" (bibliography, quotes)
- "Give me a curated list" (Goodreads genre/lists pages).
- "Find this on Apple Books / is there an audiobook?"
- "What's charting on Apple Books / Audible right now?"
- "Who narrates this audiobook, and what else is in the series?" (Audible)

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Goodreads** — `/goodreads/search` (`q`) to find a book/author id, then
   `/goodreads/book/{id}` (+ `/reviews`, `/editions`) or
   `/goodreads/author/{id}` (+ `/books`, `/quotes`). `/goodreads/genre/{name}`
   and `/goodreads/list/{id}` (browse via `/goodreads/lists`) cover curated
   browsing.
2. **Apple Books** — `/apple-books/search` (`term`) to find a book id, then
   `/apple-books/book/{id}` (+ `/reviews`, `/similar`) or
   `/apple-books/author/{id}`. Audiobooks mirror this:
   `/apple-books/audiobook/search` → `/apple-books/audiobook/{id}` (+
   `/reviews`, `/similar`), with `/apple-books/audiobook-series/{id}` and
   `/apple-books/series/{id}` for series. `/apple-books/charts` shows what's
   popular by country/genre.
3. **Audible** — `/audible/search` (`keywords`) to find a title's `asin`,
   then `/audible/product/{asin}` for detail (narrators, runtime, series)
   plus `/audible/product/{asin}/reviews` and `/audible/product/{asin}/related`.
   `/audible/series/{asin}` walks a series; `/audible/categories` and
   `/audible/category/{id}` browse by genre; `/audible/charts` and
   `/audible/list/{list}` cover bestseller/editorial lists.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Goodreads:
scripts/crawlora.sh /goodreads/search q="Project Hail Mary" | jq '.'
scripts/crawlora.sh /goodreads/book/54493401 | jq '.'

# Apple Books:
scripts/crawlora.sh /apple-books/search term="Project Hail Mary" | jq '.'
scripts/crawlora.sh /apple-books/charts | jq '.'

# Audible:
scripts/crawlora.sh /audible/search q="Project Hail Mary" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Goodreads,
Apple Books, and Audible endpoint this skill uses.

## Examples

- **Author bibliography:** `/goodreads/author/{id}/books` (or
  `/apple-books/author/{id}`) for a full backlist, cross-checked against
  `/goodreads/book/{id}/reviews` for reception.
- **"What should I read next?"** — `/apple-books/book/{id}/similar` or a
  Goodreads genre/list page for recommendations in a category.
- **Audiobook vs. print check:** `/apple-books/book/{id}` alongside
  `/apple-books/audiobook/search` or `/audible/search` for the same title
  to see if a narrated edition exists and who narrates it.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public catalog/review pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Detail endpoints need the platform's own id — resolve via `.../search`
  first if you only have a title/author name.
- Reviews and lists are paginated (`page`/`limit`) — walk pages for full coverage.
