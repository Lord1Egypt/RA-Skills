# Source Extraction Patterns

How to extract useful content from each source type. Read this during Phase 3 when processing discovered sources.

---

## Table of Contents
1. [Reddit Thread Extraction](#reddit-thread-extraction)
2. [YouTube Transcript Processing](#youtube-transcript-processing)
3. [Wiki & Article Extraction](#wiki--article-extraction)
4. [Interactive Database Navigation](#interactive-database-navigation)
5. [Twitter/X Processing](#twitterx-processing)
6. [Content Summarization](#content-summarization)

---

## Reddit Thread Extraction

Reddit threads are often the most valuable source — real players sharing tested strategies with community validation via upvotes.

### Scraping Approach
1. Convert URL to `old.reddit.com` format (cleaner HTML, better scraping):
   - `https://www.reddit.com/r/...` → `https://old.reddit.com/r/...`
2. Use `node {baseDir}/scripts/bright-scrape.mjs` for multiple threads at once
3. Fallback: `node {baseDir}/scripts/exa-contents.mjs`

### What to Extract
- **Original post (OP)**: The core question or guide content
- **Top-voted comments (first 10-15)**: Community-validated responses
- **Any comment with specific data**: Stats, percentages, exact item names, build specs
- **Comments with awards or many upvotes**: Strongest community endorsement
- **OP responses/edits**: Often contain refined or corrected information

### What to Ignore
- Comments with 0 or negative votes (unless they contain useful corrections)
- Pure joke/meme responses without substance
- Deleted/removed content
- Off-topic tangents
- "Bumping" or "same question" comments

### Reddit-Specific Patterns
- **Build posts**: Look for formatted lists, tables, or "loadout:" sections
- **Tier list posts**: Often use formatting like `S: [items], A: [items]`
- **Discussion threads**: The real value is in comment disagreements — note when the community is split
- **Megathreads**: These are gold for meta discussions but are long; focus on top-level comments with highest votes
- **Patch reaction threads**: Sort comments by relevance — top comments usually have the best analysis

### Handling Multiple Subreddits
Some games have specialized subreddits that are more valuable than the main one:
- `r/[Game]University` or `r/[Game]Meta` — deeper strategy discussion
- `r/Competitive[Game]` — higher-level play insights
- `r/[Game]Builds` — build-specific discussions

---

## YouTube Transcript Processing

YouTube guide videos are the densest source of gaming knowledge — a 15-minute video may contain what takes 30+ minutes to piece together from text sources.

### Extraction Flow
1. Use the YouTube Transcript MCP tool with the video URL
2. If transcript is unavailable (no captions), fall back to:
   - Bright Data scrape of the YouTube page for the video description + pinned comment
   - Bright Data scrape of the YouTube page for the description + pinned comment

### Processing the Transcript
Transcripts are raw, unstructured text. Look for these patterns:

**Section markers** (creators often structure their videos):
- "First/second/third..." — sequential builds or tips
- "Number one/two/three..." — ranked lists
- "Let's talk about..." — topic transitions
- "The build is..." / "Here's the loadout..." — build specifications
- "S tier / A tier / B tier..." — tier placements
- "After the patch..." / "Since the update..." — patch-related analysis

**Data extraction targets**:
- Item/weapon names (often said multiple times)
- Stat numbers ("does 150 damage", "25% crit chance")
- Specific combinations ("pair X with Y")
- Caveats ("this doesn't work in PvP", "only above rank X")

### Handling Long Transcripts
For videos over 15 minutes, the transcript may be very long. Strategies:
- Scan for the data-rich sections (build specs, tier placements) rather than reading the entire intro/outro
- Look for timestamp-like patterns if available
- Focus on the first 60-70% of the video — outros are usually self-promotion

### Video Description & Comments
Even when a transcript is available, also check:
- **Video description**: Often contains a written build summary, timestamps, and links
- **Pinned comment**: Creators often pin corrections or updates
- **Top comments**: "Actually since patch X, you should use Y instead" — real-time community correction

---

## Wiki & Article Extraction

Wikis are authoritative for factual/stat data. Articles are good for analysis and guides.

### Wiki Pages
Use Exa content extraction or ``node {baseDir}/scripts/bright-scrape.mjs``.

**Fextralife** (Souls-like games):
- Item pages have stat tables at the top, descriptions, locations
- Build pages list equipment with requirements
- Look for "Notes" sections — community-contributed interactions and tips

**Fandom/Wikia** (many games):
- Data is in infobox tables (stats, requirements, locations)
- Trivia sections sometimes contain useful mechanic details
- Pages can be bloated with ads — the markdown extraction filters most of these

**Game-specific wikis** (poewiki.net, helldivers.wiki.gg, etc.):
- Usually cleaner than Fandom
- Data tables are more structured
- Patch history sections show when items were changed

### Guide Articles
Sources: maxroll.gg, mobalytics.gg, game8.co, icy-veins.com, etc.

**Extraction focus**:
- Build specifications (gear, skills, talents)
- Tier placements with reasoning
- Pros/cons lists
- "Updated for patch X" header — confirms recency
- Author credentials if mentioned

**Watch out for**:
- SEO-farming sites with thin content (check if the article has specifics or is just generic)
- Outdated guides that haven't been updated for current patches
- Guides sponsored by the game developer (may not reflect community meta)

---

## Interactive / JS-Heavy Game Databases

Some game databases require JavaScript rendering. Most still return useful content via scraping.

### Scraping Strategy
1. Try `node {baseDir}/scripts/bright-scrape.mjs` first — Bright Data's Web Unlocker handles most JS-rendered sites
2. If content is missing, try `node {baseDir}/scripts/exa-contents.mjs` — Exa has its own rendering
3. For sites that truly require interaction, direct the user to check manually and provide specifics

### Site-Specific Tips

**op.gg / u.gg** (League of Legends):
- Most data renders server-side — scraping works for overview pages
- Champion pages with default filters contain win rates, builds, runes

**light.gg** (Destiny 2):
- Individual weapon pages scrape well (perk recommendations, community ratings)

**poe.ninja** (Path of Exile):
- Build data is API-backed — scraping the main page gets top builds
- For filtered views, add URL parameters: `?class=Necromancer&skill=Summon-Raging-Spirits`

**maxroll.gg** (Diablo 4):
- Static guide pages scrape cleanly — build specs, gear, skills all render server-side

---

## Twitter/X Processing

Twitter provides real-time community sentiment and pro player opinions that other sources lag behind on.

### Getting Twitter Posts

Use the Bright Data Twitter script to pull posts from profiles or specific tweets:

```bash
# Get recent posts from a pro player
node {baseDir}/scripts/bright-twitter.mjs "https://x.com/username" --posts 10 --since 2026-01-01

# Get a specific tweet/thread
node {baseDir}/scripts/bright-twitter.mjs "https://x.com/user/status/123456"
```

Alternatively, search for tweets via Exa:
```bash
node {baseDir}/scripts/exa-search.mjs "[game] [topic] meta" --domain twitter.com --category tweet -n 5
```

### Evaluation Criteria
Weight Twitter content by:
1. **Account type**: Pro players > content creators > community figures > random users
2. **Engagement**: High like/retweet count signals community agreement
3. **Recency**: Twitter's strength is real-time — prioritize last 1-2 weeks
4. **Specificity**: Tweets with specific claims ("X weapon does Y damage") > vague opinions

### What Twitter Is Best For
- Immediate patch reactions (day-of analysis)
- Pro player loadout reveals
- Community consensus shifts ("everyone is switching to X")
- Bug/exploit discoveries
- Hot takes that haven't made it to guides yet

### What Twitter Is NOT Good For
- Detailed build specifications (too short-form)
- Deep mechanic explanations (use wiki/Reddit instead)
- Evergreen strategy content (tweets are ephemeral)

---

## Content Summarization

As you extract from each source, immediately distill to a structured summary rather than keeping raw scraped content in context.

### Per-Source Summary Template
```
**Source**: [URL]
**Type**: Reddit thread / YouTube video / Wiki page / Article / Tweet
**Date**: [publication date or "unknown"]
**Patch/Version**: [if mentioned]
**Key Findings**:
- [Finding 1]
- [Finding 2]
- [Finding 3]
**Specific Data**: [exact numbers, item names, build specs]
**Caveats**: [any limitations, conditions, or contradictions noted]
**Confidence**: [How authoritative is this source for this topic?]
```

This format enables efficient cross-referencing in Phase 4 without keeping raw content in the context window.
