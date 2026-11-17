---
name: daily-standup-summarizer
description: >-
  Condense scattered chat messages, notes, or logs into a concise structured daily standup summary.
  Use when: (1) asked to summarize a team's daily standup from raw chat logs or messages,
  (2) converting unstructured notes into a standup format (What I did / What I'll do / Blockers),
  (3) preparing a standup report from multiple sources of team activity,
  (4) generating a daily progress update for agile/standup meetings.
---

# Daily Standup Summarizer

## Overview

Transform raw chat messages, notes, or logs from team members into a clean, structured standup summary with three sections: **Completed**, **Planned**, and **Blockers**.

## Quick Workflow

1. Gather the source material (chat export, notes file, or pasted messages).
2. Run the extraction script:

```bash
python3 scripts/extract_standup.py <input-file> [--format markdown|json]
```

3. Review the output and adjust wording for clarity or team conventions.
4. Deliver the summary to the team channel or meeting notes.

## Input Formats

- Plain text chat logs (one message per line or block)
- Slack/Discord-style exports with timestamp and author prefixes
- Free-form bullet notes

## Output Sections

Each item is categorized into:

| Section | Meaning |
|---------|---------|
| **Completed** | What was finished or made progress on since the last standup |
| **Planned** | What the person intends to work on next |
| **Blockers** | Anything blocking progress (needs input, waiting on someone, etc.) |

## Guidelines

- Keep each bullet to one sentence when possible.
- Preserve the original contributor's attribution.
- Merge duplicate or very similar items across contributors.
- If a message is ambiguous, place it in **Planned** rather than guessing.
- See [references/formatting.md](references/formatting.md) for output templates and team-specific conventions.

## Scripts

### `scripts/extract_standup.py`

Reads an input file and produces a structured standup summary.

```bash
# Markdown output (default)
python3 scripts/extract_standup.py chat_log.txt

# JSON output for programmatic use
python3 scripts/extract_standup.py chat_log.txt --format json
```
