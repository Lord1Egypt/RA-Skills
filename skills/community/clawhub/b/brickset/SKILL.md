---
name: brickset
description: Human-friendly Brickset API v3 access for LEGO set lookup and Brickset automation. Use when you need to search LEGO sets, browse themes, years, or subthemes, validate a Brickset API key, fetch building instructions or additional images, inspect API usage, or build scripts and agents on top of Brickset web services.
---

# Brickset

Use this skill for real Brickset API v3 operations with either raw JSON output or readable text summaries.

## Requirements

- `BRICKSET_API_KEY` must be set in the environment or workspace `.env`, or passed with `--api-key`
- Python 3.10+

## What works well

- `check-key` — validate the API key
- `usage-stats` — inspect 30-day API usage
- `themes` — list Brickset themes
- `subthemes` — list subthemes for a theme
- `years` — list release years, globally or per theme
- `search` — simple wrapper around `getSets`
- `get-sets` — raw `getSets` access with JSON params
- `instructions2` — fetch instructions by set number
- `additional-images` — fetch extra image URLs by Brickset `setID`
- `raw` — call any Brickset method directly when the built-in subcommands are not enough

## Output modes

- Default: JSON for scripting and automation
- `--format text`: readable summaries for humans

## Commands

```bash
# Validate key
python {{baseDir}}/scripts/brickset.py --format text check-key

# Usage stats
python {{baseDir}}/scripts/brickset.py --format text usage-stats

# Browse catalog metadata
python {{baseDir}}/scripts/brickset.py --format text themes
python {{baseDir}}/scripts/brickset.py --format text subthemes Technic
python {{baseDir}}/scripts/brickset.py --format text years
python {{baseDir}}/scripts/brickset.py --format text years --theme Space

# Search sets
python {{baseDir}}/scripts/brickset.py --format text search "Galaxy Explorer" --page-size 5
python {{baseDir}}/scripts/brickset.py --format text search Blacktron --theme Space --page-size 10 --order-by YearFromDESC
python {{baseDir}}/scripts/brickset.py get-sets --params '{"setNumber":"6990-1","extendedData":1}'

# Instructions and images
python {{baseDir}}/scripts/brickset.py --format text instructions2 10497-1
python {{baseDir}}/scripts/brickset.py --format text additional-images 1700

# Direct/raw API access
python {{baseDir}}/scripts/brickset.py raw getReviews --param setID=1700
python {{baseDir}}/scripts/brickset.py --format text raw getCollection --param userHash=<hash>
```

## Notes

- `getSets` consumes Brickset API quota.
- Brickset's `getSets` endpoint is happier when `userHash` is present, so the CLI sends an empty one automatically for anonymous searches.
- Use `raw` for methods like `login`, `checkUserHash`, `getReviews`, `getCollection`, or collection-management calls that are not wrapped yet.

## Reference

- Read `references/api.md` when you need the compact parameter guide for `getSets` or a reminder of which methods are available.

## Script

- `scripts/brickset.py` — main CLI entrypoint
