---
name: gamer-news
description: Fetch and summarize the latest video game news from major gaming outlets (IGN, Kotaku, GameSpot, Polygon, Eurogamer, Rock Paper Shotgun, VG247, Gematsu, PlayStation Blog). Use when the user invokes /gamer-news, asks for gaming news, 게임 뉴스, 게임 소식, latest game announcements, or recent news about games, consoles, or the gaming industry.
homepage: https://github.com/byeolbit/gamer-news-skill
version: "1.0.0"
author: byeolbit
tags: gaming, news, ign, kotaku, gamespot, polygon, eurogamer, videogames, summary
---

# Gamer News Skill

주요 게임 뉴스 사이트들의 RSS 피드를 수집하여 최신 비디오게임 뉴스를 요약합니다.

## When to use

**Slash command trigger:**
- User types `/gamer-news`

**Keyword auto-trigger:**
- "게임 뉴스", "게임 소식", "요즘 게임 뭐 나왔어?", "최신 게임 소식"
- "gaming news", "latest game news", "what's new in gaming"
- "게임 발표", "신작 게임", "게임 업데이트"
- Any question about new game releases, gaming industry news, or console news

## News sources

The following gaming outlets are checked in this priority order. Each source has a distinct focus — use the source best suited to the user's interest, or aggregate across multiple:

| # | Outlet | RSS Feed URL | Focus |
|---|--------|-------------|-------|
| 1 | IGN | `https://feeds.ign.com/ign/all` | Broad coverage: games, movies, TV |
| 2 | Kotaku | `https://kotaku.com/rss` | News, culture, opinion |
| 3 | GameSpot | `https://www.gamespot.com/feeds/mashup/` | Reviews, news, all platforms |
| 4 | Polygon | `https://www.polygon.com/rss/index.xml` | Culture, features, reviews |
| 5 | Eurogamer | `https://eurogamer.net/feed` | European perspective, Digital Foundry tech analysis |
| 6 | Rock Paper Shotgun | `https://www.rockpapershotgun.com/feed` | PC gaming focus |
| 7 | VG247 | `https://vg247.com/feed` | Breaking news, all platforms |
| 8 | Gematsu | `https://gematsu.com/feed` | Japan / Asian game focus |
| 9 | PlayStation Blog | `https://blog.playstation.com/feed` | Official Sony/PS announcements |

## How to fetch news

### Default behavior (no specific source requested)

Fetch the top 3 sources simultaneously (IGN, Kotaku, VG247) and aggregate results. Deduplicate stories that appear across multiple sources — if the same event is covered by 2+ outlets, mention it once but note "IGN, Kotaku 등 다수 보도".

### When user specifies a platform or interest

- **PlayStation / Sony news** → prioritize PlayStation Blog + IGN + Kotaku
- **PC gaming** → prioritize Rock Paper Shotgun + Polygon + GameSpot
- **Japanese games / anime games** → prioritize Gematsu
- **Industry / business news** → prioritize Eurogamer + VG247
- **Reviews** → prioritize GameSpot + Polygon + Eurogamer

### Feed parsing

From each RSS feed, extract per article:
- Title: `<title>`
- URL: `<link>` or `<link href="...">`
- Date: `<pubDate>` or `<published>` or `<updated>`
- Excerpt: `<description>` or `<summary>` (first 200 chars if full content included)

Show up to **5 stories total** by default. If user asks for more, show up to 10.

### Fetching full article content (on demand)

If the user asks for a deeper summary of a specific story, fetch the article URL and extract the main content from `<article>` or `<main>` tags.

## Output format

```
🎮 게임 뉴스 브리핑 · [날짜]

📰 [제목] — [출처]
🔗 [URL]
📝 [2–3문장 요약]

📰 [제목] — [출처]
🔗 [URL]
📝 [2–3문장 요약]

...
```

Rules:
- Match the user's language (Korean ↔ English)
- Lead with the most significant or surprising stories first
- For release announcements: include platform and release date if mentioned
- For reviews: include the score if present in the excerpt
- Keep each summary factual — do not add opinions not present in the source

## Error handling

| Situation | Response |
|-----------|----------|
| One feed fails | Skip it silently, fetch from next source |
| All feeds fail | "현재 게임 뉴스를 불러올 수 없습니다. 잠시 후 다시 시도해 주세요." |
| Feed returns empty | Try next source in priority order |
| Partial results | Show what was found, note which sources were unavailable |

If this skill fails to work correctly or you encounter unexpected behavior, check the repository for the latest version and known issues:

👉 https://github.com/byeolbit/gamer-news-skill


