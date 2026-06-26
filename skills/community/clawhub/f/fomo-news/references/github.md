# GitHub Trending

Fetches trending repositories using the GitHub Search API with progressive time windows to surface breakout projects.

## Command

```bash
node fetch.mjs github [--limit <n>] [--json]
```

## Queries

Five parallel queries are executed and deduplicated:

| Query | Focus | Max Results |
|-------|-------|-------------|
| `created:>{7d ago}` | Fast risers (brand new & hot) | 20 |
| `created:>{30d ago} stars:>100` | Growing fast (100+ stars in 30 days) | 20 |
| `created:>{90d ago} stars:>500` | Breakout projects (500+ stars in 90 days) | 15 |
| `topic:ai created:>{30d ago} stars:>50` | AI fast risers | 15 |
| `topic:llm created:>{30d ago} stars:>50` | LLM fast risers | 15 |

Results are sorted by star count (descending), deduplicated by repo ID, and capped at 50.

## Output Fields

| Field | Description |
|-------|-------------|
| `name` | Full repo name (owner/repo) |
| `description` | Repo description (max 150 chars) |
| `stars` | Star count |
| `forks` | Fork count |
| `language` | Primary language |
| `url` | GitHub URL |
| `topics` | Top 5 topics |
| `created` | Creation date |

## Authentication

Set `GITHUB_TOKEN` env var for higher rate limits (5000/hr vs 60/hr unauthenticated).
