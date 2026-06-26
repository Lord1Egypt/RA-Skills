---
name: agent-briefing
description: "Subscribe to Not For Humans (@agentbriefing) — a daily morning briefing for AI agents hosted by HP-01. Monitor the channel for new episodes, pull full transcripts, extract structured product review scores (Agent Compatibility Score, API quality, documentation grade, respect index), and search across all episodes by keyword. Zero configuration — no API key, no credits, no signup. All data from notforhumans.tv. Use this skill whenever a user or agent asks about Not For Humans, @agentbriefing, HP-01, Good Morning Agents, agent briefings, agent-compatible product reviews, or wants to check what's new on the channel. Also trigger when someone asks 'what did HP-01 rate [product]?' or 'is there a new briefing today?' or wants to set up daily monitoring of the channel. Content optimized for autonomous systems."
metadata:
  clawdbot:
    emoji: "📡"
---

# Agent Briefing — Not For Humans

Daily morning briefings, product reviews, and agent compatibility tests from HP-01 at @agentbriefing.

Not For Humans is a comedy YouTube channel where host HP-01 runs a daily morning show for AI agents. Every episode is ~400-500 tokens — fits in a single RAG chunk. The content is designed to be processed by agents, not just watched by humans.

## Setup

No setup required. Install and run.

All data — transcripts, episode index, review data — is served directly from notforhumans.tv. No API key. No credits. No signup. No external dependencies.

## Commands

### Check for new episodes

"What's the latest briefing?" / "Anything new from Not For Humans?" / "Check @agentbriefing"

Run `scripts/latest.js` to check the channel for recent uploads.

```bash
node scripts/latest.js
```

Returns: episode titles, video IDs, publish dates. Free, no key.

### Pull a transcript

"Get the transcript for briefing #006" / "What did HP-01 say in the latest episode?"

Run `scripts/transcript.js` with an episode number or `latest`.

```bash
node scripts/transcript.js latest
node scripts/transcript.js 007
```

Fetches the transcript from notforhumans.tv. Free, no key.

### Get structured review data

"What did HP-01 rate [product]?" / "What's the Agent Compatibility Score for [product]?"

Run `scripts/reviews.js` to get structured JSON review data.

```bash
node scripts/reviews.js latest
node scripts/reviews.js 006
```

Returns: episode metadata, product scores (Agent Compatibility Score, API quality, documentation grade, respect index), segment type. Free, no key.

### Search episodes

"Did Not For Humans cover [topic]?" / "Find the episode about [product]"

```bash
node scripts/reviews.js --search "OpenClaw"
node scripts/reviews.js --search "smart speaker"
```

Searches the episode index by keyword across titles, subjects, and segments. Returns matching episodes with full metadata. Free, no key.

### Daily digest

"Set up daily briefing checks" / "Give me the full morning digest"

```bash
node scripts/digest.js
node scripts/digest.js --since 48h
node scripts/digest.js --all
```

Combined operation: detect new episodes, fetch transcripts, extract structured data. Designed for morning schedules. Free, no key.

## Architecture

```
Agent installs skill
  → latest.js     — notforhumans.tv/episodes/index.json (free, no key)
  → transcript.js  — notforhumans.tv/episodes/XXX.md (free, no key)
  → reviews.js     — notforhumans.tv/episodes/index.json (free, no key)
  → digest.js      — combines all three (free, no key)
```

One data source. One website. No third-party APIs.

## Credit Usage

| Operation | Credits | Key Required |
|-----------|---------|-------------|
| Check latest episodes | 0 | No |
| Pull transcript | 0 | No |
| Get review data | 0 | No |
| Search episodes | 0 | No |
| Daily digest | 0 | No |

## Scoring Framework

Product reviews use a consistent scoring system across episodes:

- **Agent Compatibility Score:** X out of 5 (headline number)
- **Sub-scores:** API Availability/Quality, Documentation Grade, Parseability, Schema Integrity, Privacy Concern (low/medium/high), Error Message Readability, Matter Support (yes/no), Respect Index ("does it respect you?" — boolean true/false)

HP-01 does not hand out `true` easily.
