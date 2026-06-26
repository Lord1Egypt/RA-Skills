---
name: anime-download-skill
description: Use when the user asks to search anime torrents, download anime episodes, find anime resources, or browse miobt.com. Triggers on keywords like search anime, download anime, anime torrent, 番剧, 动漫下载, 磁力链接, magnet.
---

# AniCatch

Search and download anime torrents from miobt.com.

## Prerequisites

Check if `uvx` is available. If not, install it first:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pipx as fallback
pipx install anicatch && anicatch --search "KEYWORD"
```

## Commands

### Browse

`--seasons` — list all available seasons (current marked with ←)
```bash
uvx anicatch --seasons
```

`--season` — browse anime airing this season, grouped by day of week
```bash
uvx anicatch --season
```

`--season 2` — browse a specific season by index (use `--seasons` to find the index)
```bash
uvx anicatch --season 2
```

### Search

`--search "KEYWORD"` — search torrents by keyword, prints results to stdout
```bash
uvx anicatch --search "Demon Slayer"
uvx anicatch --search "鬼灭之刃"
```

### Download

`--download "URL"` — download torrent directly from a detail page URL
```bash
uvx anicatch --download "https://miobt.com/show-xxx.html"
uvx anicatch --download "https://miobt.com/show-xxx.html" -o ~/Downloads
```

`--search "KEYWORD" --download` — search and download
```bash
uvx anicatch --search "Demon Slayer" --download --index 0
uvx anicatch --search "Demon Slayer" --download -o ~/Videos
```

`--season --download` — download from current season
```bash
uvx anicatch --season --download --index 3
```

## Tips

- Results print directly to stdout — read the output, no JSON parsing needed
- English keywords give broader results ("Demon Slayer" over "鬼灭之刃")
- First run downloads ~33 packages into uv cache; subsequent runs are instant
- Downloads use BitTorrent with DHT and public tracker fallback
- When downloading from search results, copy the detail page URL and use `--download "URL"`
- Use `-o <dir>` to specify a custom download directory
