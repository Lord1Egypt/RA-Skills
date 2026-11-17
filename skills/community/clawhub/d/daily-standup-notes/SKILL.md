---
name: daily-standup-notes
description: Generate structured daily standup notes from a free-form brain dump. Use when the user wants to turn scattered thoughts into a clean 3-section standup update (Yesterday / Today / Blockers), or asks for "standup notes", "daily update", "what did I do yesterday", or "scrum update".
---

# Daily Standup Notes

Turn a free-form brain dump into a clean, scannable standup update in three sections:

1. **Yesterday** — completed work
2. **Today** — planned work
3. **Blockers** — anything blocking progress

## Quick start

1. Read the user's raw input (chat, bullet list, voice transcript, etc.).
2. Classify each item into one of the three buckets.
3. Output a concise markdown list under each heading.
4. If a bucket is empty, write "_None reported._"

## Formatting rules

- Use past tense for Yesterday items, present/future tense for Today items.
- Merge duplicate or near-duplicate items.
- Keep each bullet to one line; split long items into sub-bullets.
- Preserve names, PR numbers, ticket IDs, and links verbatim.
- If an item is ambiguous (could be Yesterday or Today), place it in Today and prefix with "[continue]".

## Output template

```markdown
**Yesterday**
- ...

**Today**
- ...

**Blockers**
- ...
```

## Tips

- Offer to save the output to a dated file (e.g. `standup/2025-01-15.md`) when the user doesn't specify a destination.
- For recurring use, suggest appending to a weekly rollup file.
