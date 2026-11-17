<div align="center">

# Context Archive

### Take control of your AI conversation context

[English](#english) | [中文](./README_CN.md)

</div>

---

## English

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that lets users actively manage conversation lifecycle: **archive → free context → recall on demand**.

### The Problem

If you use a single agent session for everything, your context window fills up. Old topics pollute new conversations. The agent loses focus. Tokens get wasted on irrelevant history.

### The Solution

Context Archive gives you three simple actions:

| Action | What it does |
|--------|-------------|
| **Archive** | Summarizes a chunk of conversation into a named `.md` file |
| **List** | Shows all archives with titles, dates, and summaries |
| **Recall** | Loads an archive back into the current context |

### Usage

```
You: Archive the recent laser projection discussion
AI: [generates summary] Here's the summary. Any important details missing?
You: Keep the IMU drift solution part
AI: Updated. Suggested title: 2026-07-31-Laser-Projection. Confirm?
You: Confirm
AI: Archived to archives/2026-07-31-Laser-Projection.md

--- later ---

You: Show archives
AI: 1. 2026-07-31-Laser-Projection → Laser tracking display comparison
    2. 2026-07-15-GitHub-Stats → Repo stars and traffic analysis

You: Load the first one
AI: Loaded archive: Laser Projection. Key information restored.
```

### Archive Triggers

- **Topic-based**: "archive the discussion about X"
- **Relative time**: "archive the last 2 hours"
- **Absolute time**: "archive July 21, 3pm to 5pm"
- **Entire day**: "archive today's conversation"
- **Recent (default)**: "archive recent conversation"

### Detail Check

After generating a summary, the agent asks if any important details were missed. You can point to specific conversation segments and the agent will incorporate them. This runs up to two rounds to ensure nothing critical is lost.

### Installation

```bash
clawhub install Thomaszhou22/context-archive-skill
```

Or manually copy `SKILL.md` into your OpenClaw skills directory.

### Archive File Format

Each archive is a structured Markdown file:

```markdown
# Title

> Archived: 2026-07-31 23:49
> Period: 23:00 — 23:49
> Messages: 15

## Summary
{narrative summary}

## Key Points
- {important facts}

## User-Supplied Details
- {details flagged by user during detail check}

## Decisions
- {choices made}

## Files Modified
- path/to/file: what changed

## Keywords
tag1, tag2, tag3
```

### Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) v2.0+
- Write access to workspace `archives/` directory

### Tech Stack

- No dependencies. Pure skill definition.
- Works with OpenClaw's built-in `memory_search`, `read`, and `write` tools.

### License

MIT
