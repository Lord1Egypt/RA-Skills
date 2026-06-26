---
name: ai-trending-news
description: Fetches, ranks, and summarizes the top 10 trending AI news stories from trusted editorial, official, research, and community sources. Use when the user asks for the latest AI news, trending AI stories, AI launches, model updates, research breakthroughs, or a daily AI briefing.
license: Apache-2.0
compatibility: Requires network access, RSS/Atom parsing, and optional access to public APIs such as Hacker News, Reddit, arXiv, Google News, and GitHub.
metadata:
  author: OpenAI
  version: "1.0.0"
  category: news
  domain: artificial-intelligence
allowed-tools: Bash Python Read
---

# AI Trending News Skill

Generate a ranked list of the top 10 AI news items for the requested time window, with a strong bias toward reliable, timely, and non-duplicative coverage.

## What this skill does

This skill collects stories from a curated set of sources, deduplicates them, scores them for trend relevance, and returns a concise top-10 briefing.

Use this skill when the user asks for:

- latest AI news
- trending AI stories
- top AI announcements
- AI model releases
- AI research breakthroughs
- AI startup/news roundup
- a daily or weekly AI briefing

## Core principles

1. Prefer primary and reputable sources over viral reposts.
2. Treat source quality as more important than volume.
3. Use community signals only to identify trend velocity, not as the sole basis for a story.
4. Deduplicate aggressively across rewritten headlines.
5. Clearly separate confirmed facts from interpretation.

## Source policy

Use the source tiers in `references/sources.md`.

Recommended order:

1. Official lab/company blogs and release pages
2. Major editorial technology publications
3. Research sources and preprint feeds
4. Community trend signals such as Hacker News, GitHub, and Reddit

Do not rely on SEO-heavy listicles, scraped aggregators, or low-trust newsletters as primary evidence.

## Workflow

### 1) Select the time window

Default windows:

- "today" or "latest" -> last 24 hours
- "this week" -> last 7 days
- "daily briefing" -> last 24 hours
- unspecified -> last 48 hours

If the user requests a region, topic, or format, honor that in ranking and filtering.

### 2) Fetch candidate items

Pull from the sources listed in `references/sources.md`.

Prefer:

- RSS / Atom feeds for editorial and official blogs
- Public APIs for trend signals
- Reliable preprint feeds for research updates

### 3) Normalize stories

Convert each item into this internal shape:

```json
{
  "title": "",
  "url": "",
  "source": "",
  "published_at": "",
  "summary": "",
  "tags": ["ai", "model", "research"],
  "signal": {
    "coverage": 0,
    "engagement": 0,
    "freshness": 0,
    "source_reputation": 0
  }
}
```

### 4) Deduplicate

Merge items that refer to the same underlying story, even if headlines differ.

Treat these as duplicates when they clearly refer to the same announcement:

- identical model or product launch
- same paper or benchmark result
- same funding round or acquisition
- same policy or regulatory event

Keep the canonical record with:

- the best source URL
- the strongest headline
- the richest factual summary
- a list of all supporting sources

### 5) Score and rank

Use the scoring model in `references/ranking.md`.

The default ranking logic is:

- 35% freshness
- 30% source reputation
- 20% cross-source coverage
- 15% community engagement

Adjust the weights slightly when the user asks for a research-focused, enterprise-focused, or consumer-focused briefing.

### 6) Summarize each item

For each selected story, produce:

- title
- 1–2 sentence summary
- why it matters
- source names
- publication date
- URL

Keep each item concise. Do not invent facts not supported by the sources.

### 7) Produce the final top 10

Return exactly 10 items when there are at least 10 credible candidates.

If fewer than 10 high-confidence items exist, return the highest-confidence subset and say so explicitly.

## Output format

Preferred response shape:

1. A short lead sentence describing the time window and selection criteria.
2. A numbered top-10 list.
3. A short note about how the ranking was done.

For each item, include:

- **Headline**
- Source(s)
- Date
- One-line why-it-trends note

If the user asks for a newsletter-style version, expand the summaries but keep the ranking intact.

## Guardrails

- Never present rumors as confirmed.
- Never use a source that is clearly recycled, spammy, or AI-generated without attribution.
- If an item is only supported by a single weak source, mark it as low confidence or exclude it.
- If two items seem related, cluster them rather than inflating the list.
- If the topic is controversial or uncertain, say so plainly.

## Recommended source tiers

See `references/sources.md` for the canonical source list.

## Implementation notes

- Use `scripts/fetch_ai_news.py` to collect and normalize items.
- Keep source configuration in `references/sources.md` so the skill stays easy to maintain.
- Keep ranking logic in `references/ranking.md` so the skill can evolve without rewriting the main instructions.

## Example invocation behavior

If the user says:

- "Show me the top 10 AI trending news today"
- "Give me a daily AI briefing"
- "What are the biggest AI stories this week?"

then:

1. Fetch the relevant sources.
2. Deduplicate the items.
3. Rank by the scoring model.
4. Return the top 10 in descending score order.

## Minimal quality bar

Before finalizing, verify that each selected story has:

- a valid URL
- a publication date
- a trustworthy source
- a clear connection to AI

Exclude anything that fails those checks.
