# Storage layout

Use the following default local paths.

## Cookie file

Store Douban cookies at:

`.local/douban-self-taste/cookies/douban_cookies.json`

Expected format: a JSON array of browser-style cookie objects, for example:

```json
[
  {
    "name": "dbcl2",
    "value": "...",
    "domain": ".douban.com",
    "path": "/"
  }
]
```

## Crawl cache

Store normalized crawl outputs at:

`.local/douban-self-taste/cache/collections/<category>.json`

Recommended category files:

- `movie.json`
- `book.json`
- `music.json`
- `game.json`

Each cache file should contain:

- `platform`
- `owner`
- `subject_type`
- `fetched_at`
- `source.kind`
- `items`
- `count`

## Analysis outputs

Store analysis-ready summaries at:

`.local/douban-self-taste/analysis/`

Recommended files:

- `book-profile.json`
- `movie-profile.json`
- `music-profile.json`
- `game-profile.json`
- `all-profile.json`

## Freshness rule

Treat cache older than 7 days as stale.

Use the `fetched_at` field in the JSON cache file as the freshness source of truth.
