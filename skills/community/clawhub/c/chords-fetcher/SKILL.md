---
name: chords-fetcher
description: Fetch clean guitar chords and lyrics from popular sites (mychords.net, amdm.ru, ultimate-guitar.com). Strips tabs, fixes formatting.
---

# Chords Fetcher

Fetch clean guitar chords and lyrics without ads, pop-ups, or messy guitar tabs.

## Usage

When the user asks for chords to a song (e.g., "аккорды Кино Звезда по имени Солнце", "chords behind blue eyes"), use the `exec` tool to run the fetcher script.

```bash
uv run python chords.py <song_name_and_artist>
```

## Features
- Searches across multiple sources: mychords.net, ultimate-guitar.com, amdm.ru via DuckDuckGo.
- Strips out guitar tabs (e|---, B|---, etc.) to keep the output clean.
- Fixes spacing where chords are glued to lyrics (e.g., `AmWhite snow` → `Am White snow`).
- Falls back to the next source if one is unavailable.

## Dependencies
- `beautifulsoup4`
- `ddgs` (DuckDuckGo Search)

## Notes
- Run the script from the skill's directory.
- If the script returns an error or cannot find the song, inform the user.
