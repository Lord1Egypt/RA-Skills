---
name: game-scout
description: >-
  Video game strategy specialist. Amalgamates tactics, builds, guides, and meta
  knowledge from Reddit, YouTube creators, wikis, Twitter/X, and game databases
  to unlock a higher gaming experience. Trigger on: builds, loadouts, tier lists,
  meta, strategy, "best build for", "what's meta in", "how to play", "is X still
  good", "what does X do", patch notes, weapon stats, item guides, pro play, or
  any question mentioning a video game by name.
version: 0.1.0
metadata: {"openclaw":{"emoji":"🎮","requires":{"bins":["node","python3","yt-dlp"],"env":["EXA_API_KEY","BRIGHTDATA_API_KEY","BRIGHTDATA_ZONE"]},"install":[{"id":"yt-dlp","kind":"brew","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (brew)"}]}}
---

# Game Tips — Multi-Source Research Pipeline

Deliver real, tested, actionable, current gaming insight by orchestrating parallel research across multiple sources. The goal is to replace hours of searching and watching content with a single, well-sourced answer that gives the player a competitive edge.

## Available Scripts

| Script | What It Does |
|--------|-------------|
| `node {baseDir}/scripts/exa-search.mjs "query"` | Semantic web search via Exa AI (understands intent, handles negation) |
| `node {baseDir}/scripts/exa-contents.mjs <url> [url2...]` | Extract clean text content from URLs |
| `node {baseDir}/scripts/exa-similar.mjs <url>` | Find pages similar to a given URL |
| `node {baseDir}/scripts/bright-scrape.mjs <url> [url2...]` | Scrape URLs to markdown via Bright Data (bypasses bot detection, great for Reddit) |
| `node {baseDir}/scripts/bright-twitter.mjs <profile-or-post-url>` | Get Twitter/X posts via Bright Data |
| `python3 {baseDir}/scripts/yt-transcript.py <youtube-url>` | Extract YouTube video transcript + metadata |

### Script Options Quick Reference

**exa-search.mjs**: `-n 10` (results count), `--domain reddit.com` (limit to domain), `--exclude bad.com`, `--after 2026-01-01` (date filter), `--contents` (include page text), `--summary` (include AI summary), `--category tweet|news`

**exa-contents.mjs**: Multiple URLs supported. `--summary "question"` for targeted summary.

**exa-similar.mjs**: `-n 10`, `--domain`, `--after`, `--contents`

**bright-scrape.mjs**: Multiple URLs supported. `--country us` for geo-targeting.

**bright-twitter.mjs**: Pass one or more tweet URLs. `--timeout 60` (wait time in seconds). Collects by URL — find tweet URLs first via Exa search.

**yt-transcript.py**: `--no-meta` to skip metadata.

---

## Phase 1 — Query Analysis

Before searching, analyze the user's question to determine the research strategy.

### Identify These Elements

1. **Game**: Exact title. Resolve abbreviations (PoE = Path of Exile, ER = Elden Ring, Val = Valorant, D2 = Destiny 2 or Diablo 2 depending on context, LoL = League of Legends, WoW = World of Warcraft, MH = Monster Hunter, FFXIV = Final Fantasy XIV).

2. **Topic Type**:
   - **Build/Loadout**: Weapon, armor, skill, talent, or gear combinations
   - **Strategy/Guide**: How to approach encounters, modes, or progression
   - **Mechanic/Interaction**: How a specific system, item, or ability works
   - **Meta/Tier List**: What's currently strongest or most popular
   - **Patch/Balance**: Recent changes and their impact
   - **Pro Play/Esports**: What competitive or high-level players are using

3. **Recency Requirements**:
   - **Critical** (live-service games with frequent patches): Must find current-patch info
   - **Moderate** (games with periodic updates): Recent info preferred, older is OK
   - **Low** (stable/single-player games): Evergreen guides are fine

4. **Scope**:
   - **Narrow** ("does X proc bleed?"): Target wiki/database, skip broad search
   - **Broad** ("best builds for class X"): Full pipeline

### Decision Table

| Scope | Recency | Action |
|-------|---------|--------|
| Narrow + Low | Skip to Phase 3: scrape relevant wiki directly |
| Narrow + Critical | Phase 2 (limited) + Phase 3: wiki + Reddit for patch confirmation |
| Broad + Any | Full pipeline: Phase 2 → 3 → 4 → 5 |

---

## Phase 2 — Parallel Discovery

Cast a wide net. Run multiple search commands to discover the best sources.

Read `references/search-strategies.md` for game-specific query templates and community hub URLs.

### A. Exa AI Semantic Search (2-3 queries)

Exa understands intent — phrase queries naturally. Run these in parallel:

```bash
# Primary search
node {baseDir}/scripts/exa-search.mjs "best [topic] for [game] [current patch/season]" -n 10 --after 2026-01-01

# Reddit-focused
node {baseDir}/scripts/exa-search.mjs "[game] [topic] discussion recommendations" -n 5 --domain reddit.com --after 2025-06-01

# YouTube video discovery
node {baseDir}/scripts/exa-search.mjs "[game] [topic] guide tutorial" -n 5 --domain youtube.com --after 2025-06-01
```

### B. Twitter/X (recent community takes)

First find tweet URLs via Exa, then extract full data via Bright Data:

```bash
# Step 1: Find relevant tweets via Exa search
node {baseDir}/scripts/exa-search.mjs "[game] [topic] meta" --domain twitter.com -n 5

# Step 2: Extract full tweet data for the URLs found
node {baseDir}/scripts/bright-twitter.mjs "https://x.com/user/status/123" "https://x.com/user/status/456"
```

### Evaluate Discovery Results

From all results, identify the **best 5-8 sources** to extract in depth:
- Prefer recent content (check dates)
- Prefer high-engagement Reddit threads
- Prefer YouTube videos from known guide creators
- Prefer wiki/database pages for factual/stat questions
- Include at least 2 different source types for cross-referencing

---

## Phase 3 — Deep Extraction

Go deep on the best sources. Run extraction commands for each source type.

Read `references/source-extraction.md` for detailed extraction patterns.

### Reddit Threads

Use Bright Data scraper — it bypasses Reddit's bot detection. Prepend `old.` for cleaner scrapes:

```bash
node {baseDir}/scripts/bright-scrape.mjs "https://old.reddit.com/r/[sub]/comments/[id]/[slug]" "https://old.reddit.com/r/[sub]/comments/[id2]/[slug2]"
```

Focus on: OP content, top-voted comments, comments with specific data. Discard: jokes, deleted comments, tangents.

### YouTube Videos

```bash
python3 {baseDir}/scripts/yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

In the transcript, look for: section markers ("first/second/third"), build specifications, stat numbers, specific item/weapon names, caveats.

**Fallback** if no subtitles: scrape the YouTube page for description + comments:
```bash
node {baseDir}/scripts/bright-scrape.mjs "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Articles & Wiki Pages

Use Exa for clean extraction (works best on articles/wikis):
```bash
node {baseDir}/scripts/exa-contents.mjs "https://fextralife.com/..." "https://maxroll.gg/..." --summary "What build is recommended?"
```

For sites that block Exa, fall back to Bright Data:
```bash
node {baseDir}/scripts/bright-scrape.mjs "https://example.com/guide"
```

### Context Management

Summarize extracted content as you go. For each source, distill to:
- Key recommendations/findings
- Specific data points (stats, percentages, item names)
- Date/patch version
- Source URL for attribution

---

## Phase 4 — Synthesis & Validation

Cross-reference extracted information to deliver validated insights.

### Cross-Reference Protocol

1. **Identify consensus**: Do 3+ sources agree? That's high confidence.
2. **Spot conflicts**: If sources disagree, note both perspectives and explain why (different patch versions, skill levels, game modes).
3. **Check recency**: Is the advice from the current patch/season? If a source predates a relevant patch, flag it.
4. **Validate specifics**: If a build claims specific stats, verify against wiki/database data when possible.

### Confidence Assessment

| Level | Criteria |
|-------|----------|
| **HIGH** | 3+ recent sources agree, current patch confirmed, community consensus |
| **MEDIUM** | 2 sources agree, or sources are slightly dated but no known nerfs/buffs |
| **LOW** | Single source, pre-patch info, or actively contested in community |

### Red Flags
- Source is from a previous patch and the topic is affected by balance changes
- Reddit thread has top comments disagreeing with OP
- YouTube video has comments saying "this was nerfed"
- Conflicting info between wiki and community — community is usually more current

---

## Phase 5 — Structured Response

Deliver the answer in a format adapted to the query type.

### Universal Structure

1. **TL;DR**: One to three sentences with the direct answer
2. **The Details**: Actionable specifics (build specs, step-by-step, tier placements)
3. **Why This Works**: The underlying mechanic or synergy that makes it effective
4. **Caveats**: Patch dependency, skill floor, mode-specific, rank-dependent considerations
5. **Sources**: Numbered list with links, creator names, and dates
6. **Confidence**: HIGH/MEDIUM/LOW with brief reasoning

### Format by Query Type

**Build/Loadout queries**: Use a table or structured list with alternatives.

**Meta/Tier list queries**: Use S/A/B tier format with explanations per tier.

**Mechanic/Interaction queries**: Direct yes/no answer first, then detailed breakdown.

**Strategy/Guide queries**: Numbered step-by-step with reasoning per step.

See `examples/sample-queries.md` for full format examples of each type.

---

## Fallbacks & Error Handling

If a script fails, degrade gracefully rather than abandoning the research.

| Script Failing | Fallback |
|----------------|----------|
| exa-search | Use `summarize` CLI if available, or ask user to provide URLs |
| bright-scrape | Use exa-contents for the same URLs |
| bright-twitter | Search Twitter via exa-search with `--domain twitter.com --category tweet` |
| yt-transcript | Use bright-scrape on the YouTube URL for description + comments |
| exa-contents | Use bright-scrape for the same URLs |

If a search returns no relevant results, broaden the query or try alternative phrasing before giving up.

---

## Reference Files

- **`references/search-strategies.md`** — Read when formulating search queries. Contains game-specific community hubs, subreddit names, and query templates by topic type.
- **`references/source-extraction.md`** — Read when extracting content from sources. Contains patterns for Reddit parsing, YouTube transcript processing, and wiki extraction.
- **`references/game-databases.md`** — Read when the query involves specific game data or interactive build planners. Contains URLs and navigation hints per game.
- **`examples/sample-queries.md`** — Read for calibration. Shows the full pipeline applied to four different query types.
