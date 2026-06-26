---
name: bangumi-explorer
description: Query Bangumi (bgm.tv) for anime, manga, light novels, games, and music. Search subjects, view details and episode lists, browse seasonal anime charts, rating rankings, and look up voice actors / staff. No authentication required.
---

# Bangumi Explorer

Query Bangumi (bgm.tv) for anime, manga, light novels, games, and music.

## When to Use

Use this skill when the user asks about:
- Anime search, manga search, game search
- New anime this season, season chart
- Anime ranking, anime details, episode list
- Voice actor / seiyuu lookup
- Bangumi, bgm, or any ACGN subject inquiry

## Environment Check

Before using this skill, check if Python is available:

```bash
python --version  # or python3 --version
```

**If Python 3.9+ is available:** Use the commands below with `bangumi.py` script (recommended, token-efficient).

**If Python is NOT available:** Use the fallback method — call Bangumi API directly via `web_fetch` or `browser`. This works without Python but consumes significantly more tokens (~3-5x) and is slower.

### Fallback API Reference

- **API Base**: `https://api.bgm.tv/v0`
- **User-Agent Required**: `MountLynx/bangumi_skill (https://github.com/MountLynx/bangumi_skill)`
- **Rate Limit**: 0.5s between requests
- **OpenAPI Spec**: https://github.com/bangumi/api/blob/master/open-api/v0.yaml
- **API Docs**: https://github.com/bangumi/api

## Steps

1. Check Python environment availability
2. If Python available: Run `bangumi.py` commands via `exec`
3. If Python not available: Use fallback API calls via `web_fetch` or `browser`
4. Present script output as-is — do not reformat

## Commands

Run `bangumi.py` via `exec` in the skill directory:

```bash
# Search subjects (default: anime)
python bangumi.py search "<keyword>" [--type anime|book|game|music|real] [--limit 10]

# Subject details
python bangumi.py info <subject_id>

# Episode list
python bangumi.py episodes <subject_id>

# Seasonal chart (default: current season)
python bangumi.py season [--year 2026] [--month 4]

# Rating ranking
python bangumi.py rank [--type anime|book|game|music|real] [--top 20]

# Person search (voice actors, staff)
python bangumi.py person "<keyword>"

# Daily broadcast calendar
python bangumi.py calendar

# Character search
python bangumi.py character "<keyword>"
```

## Parameters

| Flag | Values | Default |
|------|--------|---------|
| `--type` | anime, book, game, music, real | anime |
| `--limit` / `--top` | integer | 10 / 20 |
| `--year` / `--month` | integer | current year / season start month |

## Notes

- No authentication needed. Does not support collections or progress tracking.
- Script caches API responses in `~/.bangumi/cache/` (auto-expires, auto-cleans).
- Requires Python 3.9+. Zero third-party dependencies (stdlib only).
- Rate-limited to 0.5s between requests to respect Bangumi API.
- Search API is experimental — use precise keywords for best results.
- Episode descriptions may be in Japanese.
