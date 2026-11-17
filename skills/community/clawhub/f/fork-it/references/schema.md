# fork-it — Script Reference

Field-level detail for the two scripts. Read this only when you need the exact JSON
shape or a flag you don't remember; the SKILL.md method is enough for normal use.

## github-search.mjs

```bash
node scripts/github-search.mjs "query" \
  [--language js] [--min-stars N] [--max-stars N] \
  [--updated-within N] [--created-after YYYY-MM-DD] \
  [--sort stars] [--order desc] [--limit 10]
```

### Return JSON (status: "ok")

```json
{
  "status": "ok",
  "query": "pomodoro timer",
  "total_count": 1234,
  "returned_count": 10,
  "items": [
    {
      "rank": 1,
      "full_name": "user/repo",
      "description": "A pomodoro timer app",
      "url": "https://github.com/user/repo",
      "stars": 12300,
      "forks": 1200,
      "language": "TypeScript",
      "pushed_days_ago": 3,
      "created_at": "2024-01-01",
      "topics": ["productivity", "timer"],
      "license": "MIT"
    }
  ]
}
```

### Return JSON (status: "error")

```json
{ "status": "error", "code": "RATE_LIMITED", "message": "..." }
```

Generate a friendly, user-language message from `code` and `message`.

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `query` | Search keyword (positional, required) | — |
| `--language, -l` | Repository language filter | none |
| `--min-stars` | Minimum stars (0 = no floor) | 0 |
| `--max-stars` | Maximum stars | none |
| `--updated-within` | Updated within N days (0 = no limit) | 0 |
| `--created-after` | Created after date (YYYY-MM-DD) | none |
| `--sort` | Sort field | stars |
| `--order` | Sort order | desc |
| `--limit, -n` | Result limit | 10 |

## repo-detail.mjs

```bash
node scripts/repo-detail.mjs "owner/repo"
```

Returns detailed repo info (README excerpt, topics, latest release, etc.) as JSON
with `status: "ok"`. On failure: `{"status":"error","code":"...","message":"..."}`.

## Display rules

- `stars: 12300` → "12.3k" (or "1.23万" in Chinese)
- `pushed_days_ago: 3` → "3 days ago" / "3天前"
- Always translate `description` and your commentary into the user's language.
