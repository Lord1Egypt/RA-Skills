# chords-fetcher 🎸

Fetch clean guitar chords and lyrics from popular websites.

This skill searches chord websites (mychords.net, ultimate-guitar.com, amdm.ru), extracts the pure text with chords, strips out unnecessary tabs, and formats it beautifully. Perfect for AI agents that help musicians.

## Features
- **Multi-source search:** Searches `mychords.net`, `ultimate-guitar.com`, and `amdm.ru` via DuckDuckGo.
- **Tab stripping:** Removes ASCII guitar tabs (`e|---`, `B|---`) to keep output clean and readable on mobile devices.
- **Smart formatting:** Fixes spacing where chords are glued to lyrics (e.g., turns `AmWhite snow` into `Am White snow`).
- **Fallback mechanism:** If one site doesn't have the song, it seamlessly tries the next one.

## Requirements
- Python 3.10+
- `uv` (recommended for dependency management)

Dependencies (auto-installed by `uv`):
- `beautifulsoup4`
- `ddgs`

## Usage

```bash
uv run python chords.py <song_name_and_artist>
```

**Examples:**
```bash
uv run python chords.py metallica unforgiven 2
uv run python chords.py кино звезда по имени солнце
```

## Integration with AI Agents

Drop this folder into your agent's skills directory. The included `SKILL.md` tells your agent how to use it. When you ask for chords, the agent runs the script and returns clean formatted text.
