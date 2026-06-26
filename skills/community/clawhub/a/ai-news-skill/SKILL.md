---
name: ai-news
description: AI industry news aggregation from curated RSS feeds. Catches model releases from major labs.
homepage: https://github.com/tensakulabs/ai-news-skill
user-invocable: true
metadata:
  openclaw:
    emoji: "📰"
    requires:
      bins: []
      env: []
---

# AI News Skill

Fetch and summarize AI industry news from curated RSS feeds. Designed to catch major model releases (GPT, Claude, Gemini, Grok, GLM, etc.) and important AI news.

## Usage

Invoke with `/ai-news` or ask for "AI news", "morning briefing", "what's new in AI".

## Feeds

This skill fetches from 15 curated sources:

**Aggregators** (daily/weekly digests):
- TLDR AI — Daily AI industry digest
- Hacker News — Breaking tech news
- The Decoder — AI-focused site
- Last Week in AI — Weekly roundup
- Marktechpost — Research coverage

**Lab Blogs** (via [Olshansk/rss-feeds](https://github.com/Olshansk/rss-feeds)):
- Anthropic News — Company announcements
- Claude Blog — Product updates and guides
- Anthropic Red Team — Safety research
- OpenAI Research — GPT releases (⚠️ currently empty)
- xAI News — Grok releases (⚠️ stale since Sept 2025)
- Google AI — Gemini/DeepMind
- Claude Code Changelog — CLI updates

**AI Coding Tools** (via [Olshansk/rss-feeds](https://github.com/Olshansk/rss-feeds)):
- Cursor Blog — Cursor editor releases
- Windsurf Blog — Windsurf/Codeium releases
- Ollama Blog — Local model runner updates

## Instructions

### Step 0: Idempotency Check (Save Mode Only)

If `--save` was requested AND `--regenerate` was NOT specified:
1. Determine today's briefing path (same logic as Step 7.5)
2. Check if `ai-news-YYYY-MM-DD.md` already exists at that path
3. If it exists → read and return its contents to the user with note: `(Cached — run with --regenerate to refresh)`
4. If it does not exist → proceed to Step 1

If `--save` was NOT requested, skip this step entirely.

### Step 1: Load Feed Configuration

Read the feed list from `feeds.json` in this skill directory.

### Step 2: Fetch Feeds (Parallel)

For each feed in `feeds.aggregators`, `feeds.labs`, and `feeds.tools`, use `web_fetch` to retrieve the RSS content:

```
web_fetch(url: "<feed_url>", extractMode: "text")
```

Fetch priority 1 feeds first, then priority 2.

### Step 3: Parse RSS Items

RSS feeds are XML. Extract items using these patterns:

```
<item>
  <title>...</title>
  <link>...</link>
  <pubDate>...</pubDate>
  <description>...</description>
</item>
```

For Atom feeds:
```
<entry>
  <title>...</title>
  <link href="..."/>
  <published>...</published>
  <summary>...</summary>
</entry>
```

### Step 4: Filter by Date

Compute `cutoff = current datetime - exactly 86400 seconds (24 hours)`.
Discard any item where `pubDate` or `published` is earlier than `cutoff`.
Do not round or approximate — if an item is 25 hours old, it is excluded.

Weekly mode (user says "week" or "last 7 days"): use 604800 seconds instead.

### Step 5: Deduplicate

Same story may appear in multiple feeds. Dedupe by:
1. Exact title match
2. Similar title (>80% overlap)
3. Same link URL

Keep the version from the highest-priority source.

### Step 6: Categorize

Assign each item to a category:

| Category | Keywords |
|----------|----------|
| Model Releases | "release", "launch", "announce", model names (GPT, Claude, Gemini, Grok, GLM, Llama) |
| Research | "paper", "research", "study", "benchmark" |
| Industry | "funding", "acquisition", "hire", "layoff", "IPO" |
| Product | "feature", "update", "API", "pricing" |
| Opinion | "think", "believe", "future", "prediction" |

### Step 7: Format Output

```markdown
# AI News Briefing
**Date:** [today's date]
**Sources:** [count] feeds checked
**Period:** Last 24 hours

---

## Model Releases
1. **[Title]** — [1 sentence summary]. [Source]
2. ...

## Research
1. **[Title]** — [1 sentence summary]. [Source]
...

## Industry News
1. **[Title]** — [1 sentence summary]. [Source]
...

---

**Coverage Gap:** Chinese AI labs (Zhipu, DeepSeek, Baidu, Alibaba) don't publish RSS. Check manually for major releases.
```

### Step 7.5: Save to File (Optional)

Only activate this step if the user explicitly requested it — via `--save`, `save to file`, or similar phrasing. Do NOT save by default.

If saving is requested:
1. Determine the save directory:
   - If the user specified a path in their request, use that path exactly
   - Otherwise default to `~/ai-news/` where date is today's date in YYYY-MM-DD format
2. Write the full formatted briefing to `<dir>/ai-news-YYYY-MM-DD.md` using the Write tool
3. Write a links reference file to `<dir>/ai-news-YYYY-MM-DD-links.md` using the Write tool:
   ```markdown
   # AI News Links — YYYY-MM-DD
   ## Model Releases
   - [Title](url)
   ## Research
   - [Title](url)
   ## Industry News
   - [Title](url)
   ```
   Include every item from the briefing with its source URL.
4. Confirm to the user:
   ```
   Saved to <dir>/ai-news-YYYY-MM-DD.md
   Links  → <dir>/ai-news-YYYY-MM-DD-links.md
   ```

### Step 8: Handle Errors

If a feed fails to fetch:
- Log the error
- Continue with remaining feeds
- Note failed sources in output

## Customization

Edit `feeds.json` to add/remove feeds, change priorities, or enable optional feeds. See `README.md` for cron integration and full documentation.
