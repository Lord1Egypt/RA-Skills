---
name: tech-scout
emoji: 🛰️
category: Productivity & Research
tags: [intelligence, daily-digest, web-search, x-twitter, youtube, reddit, github, competitive-intel]
description: >
  Daily multi-source intelligence digest that proactively scans X, YouTube, Reddit, and GitHub for
  tools, techniques, and updates relevant to your active projects — delivered before your morning
  session. Filters high-signal from noise using a 7/10 quality bar. Each surfaced item includes a
  "why this matters for you" note. Use when you want your agent to stay on top of fast-moving AI,
  crypto, content creation, or technical domains without you doing manual research.
author: Kenneth Kim (KK_HoldCo)
version: 1.0.0
---

# Tech Scout — Daily Intelligence Digest

**Bottom line:** Your agent runs this automatically each morning before your first session. You get a ranked list of 3-5 actionable items from the internet. No noise, no generic newsletters — only things with a clear reason they matter to your specific projects.

---

## When to Invoke

**Automated:** Run at 06:00-07:00 local time daily, before your morning briefing session.

**Manual triggers:**
- "What's new in [domain] this week?"
- "Did anything relevant drop overnight?"
- "Tech scout update"
- "What should I know before today's session?"
- Any time you want a signal sweep without doing the research yourself

---

## Setup — Define Your Project Domains

Before running Tech Scout for the first time, configure your keyword targets by project area. Example domains:

### AI & Automation
- New model releases, API price drops, free tier changes
- `new AI model` `AI API update` `open source LLM` `AI tool comparison [year]`
- `agent framework` `Claude update` `GPT update` `Gemini update`

### Crypto & Trading
- New trading frameworks, Hyperliquid updates, perpetuals strategies
- `crypto trading bot` `algorithmic trading` `funding rate strategy`
- `crypto paper trading` `HFT bot open source` `perpetual futures strategy`

### Content Creation & YouTube
- Video generation tools, voiceover tech, automation workflows
- `AI video generation` `faceless YouTube automation` `text to video [year]`
- `AI narration` `programmatic video` `YouTube automation tool`

### Your Active Projects
- Add any domain-specific keywords for your current focus areas

---

## Data Sources

### 1. X (Twitter)
```
Search last 24 hours for each keyword cluster
Filter: min 50 likes OR min 20 retweets (quality signal)
Max 5 results per keyword cluster
```

### 2. YouTube
```
Search for videos uploaded in last 48 hours per keyword cluster
Filter: min 500 views within 48h (early traction signal)
Max 3 results per keyword cluster
```

### 3. Reddit
```
Subreddits relevant to your domains (e.g., r/MachineLearning, r/algotrading, r/YoutubeAutomation)
Filter: upvotes > 100, posted in last 24 hours
```

### 4. GitHub
```
New repos and trending topics
Filter: created in last 7 days, stars > 50
Searches: tool names, framework names, strategy names from your keyword list
```

### 5. Web Search (via real-time LLM)
```
"What new [domain] tools or updates were announced in the last 48 hours?"
"Any major [domain] price changes or new free tiers announced recently?"
Catch-all for items the structured searches miss
```

---

## Relevance Scoring

Each item gets scored 1-10:

| Score | Meaning | Action |
|---|---|---|
| 8-10 | Direct match to an active project + actionable today | ✅ Include — flag HIGH |
| 7 | Clearly relevant, worth seeing | ✅ Include — flag MEDIUM |
| 1-6 | Too generic, wrong timing, or low signal | ❌ Skip |

**Scoring factors:**
- Exact keyword match on active project = +3
- Mentions cost savings or free alternative to paid tool = +2
- Has code / repo / tutorial = +2 (immediately actionable)
- High engagement (viral early signal) = +1
- Duplicate of something surfaced in last 7 days = -5 (dedup)
- Generic entertainment / low-signal social = hard reject

**Quality bar:** Every surfaced item must include a one-line "Why this matters for you" note. If you can't write that note, the item scores below 7 and gets rejected.

---

## Deduplication

Maintain `state/tech_scout_seen_urls.txt` — append every surfaced URL.
Before including any item, check against this file.
Never surface the same URL twice within 7 days.

---

## Output Format

File: `state/tech_scout_digest_YYYY-MM-DD.md`

```markdown
# Tech Scout Digest — [DATE]
_Sources scanned: X + YouTube + Reddit + GitHub + Web Search_
_Items found: [N] | After 7/10 filter: [M] | Surfacing: [K]_

---

## 🔴 HIGH — Act on This

### [Item Title]
**Source:** Reddit r/[subreddit] | **Score:** 9/10 | **Domain:** [project area]
**Why relevant:** [specific reason]
**Why this matters for you:** [one-line practical impact]
**Link:** [url]
**Suggested action:** [concrete next step — "test this tonight", "read section 3", "check if this replaces [current tool]"]

---

## 🟡 MEDIUM — Good to Know

### [Item Title]
**Source:** YouTube | **Score:** 7/10 | **Domain:** [project area]
**Why relevant:** [specific reason]
**Link:** [url]
**Suggested action:** [concrete next step]

---

## ⚪ FYI — No Action Needed
- [Item]: [one-line summary] ([link])
- [Item]: [one-line summary] ([link])
```

---

## Morning Briefing Integration

If you run a morning briefing, integrate Tech Scout as follows:
1. Read `state/tech_scout_digest_YYYY-MM-DD.md`
2. Extract the top 1-3 HIGH items
3. Include a "🔬 Tech Scout" section in your morning briefing output
4. If no HIGH items: include the top MEDIUM item
5. Always link to the full digest

---

## Error Handling

- X API rate-limited → skip X, continue with other sources, note in digest header
- Reddit quota exceeded → fall back to web search for Reddit content
- GitHub API returns 403 → skip GitHub for today, note in header
- **Always write the output file even if partial** — note which sources failed

---

## Implementation Notes

**APIs typically needed:**
- X (Twitter) Bearer Token
- Google API key (for YouTube search)
- Reddit scraper (Apify or direct Reddit API)
- GitHub REST API (public search, no key needed)
- Real-time web search LLM (Grok, Perplexity, or similar)

**Script entry point:** `tech_scout.py --date today [--dry-run]`
**Schedule:** Daily at 06:00-07:00 before morning session
**Output path:** `state/tech_scout_digest_YYYY-MM-DD.md`
