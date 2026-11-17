---
name: anicult
description: Search, discover, and get streaming links for anime. Trigger when user asks about anime info, recommendations, trending/popular anime, episode details, or wants to find where to watch anime. Uses AniList GraphQL API (metadata) + Anikoto API (streaming sources via megaplay.buzz). Commands: anime search <title>, anime trending [--page N], anime popular [--page N], anime detail <id> [--episodes], anime recent [--page N], anime random [--genre GENRE]. Streaming embeds: megaplay.buzz, anixo.buzz. Legal streaming: Crunchyroll links when available from AniList. Detail command outputs direct megaplay.buzz stream URLs (megaplay.buzz/stream/ani/{id}/{ep}/sub) — tap to open in browser for streaming.
---

# AniCult Skill — SKILL.md

## Deskripsi
Skill untuk search, discovery, dan streaming info anime via CLI. Tidak perlu browser — langsung query AniList GraphQL API + Anikoto API.

**Sumber data:**
- **AniList GraphQL** → metadata anime (search, trending, details, score, genres)
- **Anikoto API** → episode list + streaming URLs (megaplay.buzz, anixo.buzz)
- **Streaming embeds:** megaplay.buzz, anixo.buzz
- **Legal streaming:** Crunchyroll, Funimation (dari AniList)

## Trigger
- Rizki/user bertanya tentang anime tertentu (sinopsis, genre, score, episode)
- Minta rekomendasi anime trending/popular
- Cari anime untuk ditonton
- Keywords: `anime`, `nonton`, `episode`, `streaming`, `trending anime`, `rekomendasi anime`, nama anime

## CLI Commands

```bash
# Search anime by name
python3 ~/.qclaw-oversea/skills/anicult/anime.py search "Naruto"

# Trending anime (with pagination)
python3 ~/.qclaw-oversea/skills/anicult/anime.py trending --page 1 --limit 10

# Popular anime
python3 ~/.qclaw-oversea/skills/anicult/anime.py popular --limit 10

# Anime detail by AniList ID (get ID from search first)
python3 ~/.qclaw-oversea/skills/anicult/anime.py detail 21

# Detail + episode list (from Anikoto streaming sources)
python3 ~/.qclaw-oversea/skills/anicult/anime.py detail 21 --episodes

# Recently updated anime (from Anikoto)
python3 ~/.qclaw-oversea/skills/anicult/anime.py recent --limit 10

# Random anime pick
python3 ~/.qclaw-oversea/skills/anicult/anime.py random

# Filter random by genre
python3 ~/.qclaw-oversea/skills/anicult/anime.py random --genre "Romance"

# JSON output (for programmatic use)
python3 ~/.qclaw-oversea/skills/anicult/anime.py search "One Piece" --json
```

## AniList GraphQL API
- Endpoint: `https://graphql.anilist.co`
- No API key needed (public API)
- Rate limit: 90 requests/minute per IP

## Anikoto API
- Endpoint: `https://anikotoapi.site`
- Endpoints: `/recent-anime`, `/series/{id}`
- No API key needed
- Provides episode streaming URLs (megaplay.buzz embeds)

## Output Format
- Telegram-friendly markdown (bold, italic, links)
- No ANSI color codes by default
- `--json` flag for machine-readable output
- AniList ID included for deep linking

## Example Workflow
1. `anime.py search "Attack on Titan"` → get AniList IDs
2. `anime.py detail 16498` → full details + streaming links
3. Open megaplay.buzz link in browser to watch
