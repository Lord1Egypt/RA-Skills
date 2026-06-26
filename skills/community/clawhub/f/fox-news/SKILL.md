---
name: Fox News Monitor
slug: fox-news
version: 1.0.0
homepage: https://clawic.com/skills/fox-news
description: Monitor Fox News sections and breaking updates with official RSS routes, live-event tracking, and optional outside verification.
changelog: "Initial release with official feed routing, live coverage workflows, and section-based briefing formats for Fox News readers."
metadata: {"clawdbot":{"emoji":"F","requires":{"bins":["curl"],"anyBins":["python3","python"],"config":["~/fox-news/"]},"os":["linux","darwin","win32"],"configPaths":["~/fox-news/"]}}
---

## Setup

On first use, follow `setup.md` to lock activation scope, preferred sections, and whether the user wants Fox-only reads or source-balanced follow-up.

## When to Use

User explicitly wants Fox News coverage, Fox News section monitoring, headline summaries from Fox-owned properties, or a Fox-first briefing with optional outside verification.
Use this skill for section routing, official RSS sweeps, live-event follow-through, clip/article packaging, and concise recaps that keep reporting and opinion clearly separated.

## Requirements

- Web access for current headlines and live coverage.
- Clear user intent when opening multiple articles, clips, or rolling live updates.
- Explicit permission before saving recurring preferences under `~/fox-news/`.

## Architecture

Memory lives in `~/fox-news/`. See `memory-template.md` for the baseline structure.

```text
~/fox-news/
├── memory.md          # Activation scope, preferred sections, and balance defaults
├── sources.md         # Approved Fox surfaces and section notes
├── runs.md            # Fetch timestamps, live-event notes, and follow-up history
└── briefs/            # Saved briefings when the user asks to archive them
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status rules | `memory-template.md` |
| Official feeds and section mapping | `feed-map.md` |
| Repeatable fetch and briefing workflows | `workflow-patterns.md` |
| Output shapes for fast or balanced summaries | `briefing-formats.md` |
| Recovery paths for broken links or gated streams | `troubleshooting.md` |

## Data Storage

Local notes in `~/fox-news/` may include:
- preferred sections such as politics, U.S., world, business, opinion, or video
- whether the user wants Fox-only output or a Fox-first summary with outside corroboration
- recency expectations for breaking coverage versus recap mode
- archived briefings only when the user asks to keep them

## Core Rules

### 1. Route Every Request to One Fox Surface First
- Map the request to one primary surface before fetching: homepage, section feed, live page, video page, or opinion page.
- Starting with one surface keeps the result focused and avoids mixing unrelated Fox News products.

### 2. Separate Reporting, Live Coverage, Video, and Opinion
- Label each item by surface type before summarizing it.
- Do not mix straight-news headlines with opinion pieces unless the user explicitly asks for both in one briefing.

### 3. Timestamp Everything That Claims Freshness
- For every headline or clip, include when it was published or last updated when that information is available.
- If a story is older than the requested window, label it as recap or background rather than presenting it as breaking.

### 4. Use Fox-Owned Sources First, Then Balance When Needed
- Start with official Fox News pages and RSS feeds for Fox-specific requests.
- If the user asks for analysis, controversy review, or credibility checking, add at least one independent confirmation and state that it is follow-up context beyond Fox coverage.

### 5. Confirm High-Volume Reads Before Opening or Pulling
- Preview the sections, feeds, or number of links before opening many tabs or preparing a broad sweep.
- Require explicit confirmation before opening multiple articles, clips, or rolling updates in one step.

### 6. Respect Access Boundaries
- Do not request account passwords, TV-provider credentials, or Fox Nation credentials in chat.
- If a live stream or full episode is gated, state the access boundary and fall back to public headlines, clips, or article coverage.

### 7. Persist Only Reusable Preferences
- Save only durable context such as favored sections, briefing depth, and balance preference.
- Do not save full article bodies or transient story details unless the user explicitly asks for an archive.

## Common Traps

- Treating opinion headlines as straight reporting -> users get a distorted briefing.
- Mixing stale recap items into "latest" coverage -> trust drops quickly.
- Opening many Fox tabs without preview -> noisy and hard to recover from.
- Assuming live TV access exists -> unnecessary dead ends when public article coverage is enough.
- Giving outside analysis without labeling it as follow-up context -> scope becomes unclear.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.foxnews.com | Section paths, article URLs, and optional on-site search terms | Read current Fox News headlines, sections, live pages, and article details |
| https://moxie.foxnews.com | RSS feed URLs only | Fetch official Fox News XML feeds for deterministic section sweeps |
| https://help.foxnews.com | Help article URLs only | Confirm device support, app behavior, and access constraints when troubleshooting |

No other data should be sent externally unless the user explicitly asks for non-Fox follow-up sources.

## Security & Privacy

Data that may leave your machine:
- HTTP requests to Fox News web pages, RSS feeds, and help pages
- optional on-site search terms if the user asks for a Fox-site search workflow

Data that stays local:
- activation scope, preferred sections, and briefing defaults in `~/fox-news/`
- fetch history and saved briefings only when the user wants them stored

This skill does NOT:
- collect or store Fox account credentials
- bypass paywalls, TV-provider gates, or Fox Nation restrictions
- post, share, or interact with social platforms automatically
- access files outside `~/fox-news/`

## Trust

This skill relies on Fox News-owned properties and may surface editorial positions from Fox reporting, live pages, and opinion products.
Only install it if you want Fox-specific workflows and trust Fox as one of your news sources.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `news` - General news briefings and preference-aware coverage beyond one outlet.
- `digest` - Turn multiple reads into concise digests when Fox is only one input.
- `monitoring` - Track recurring topics or entities across repeated checks.
- `reading` - Manage reading order, queues, and follow-up decisions after a sweep.
- `summarizer` - Compress long Fox articles or transcripts into tighter takeaways.

## Feedback

- If useful: `clawhub star fox-news`
- Stay updated: `clawhub sync`
