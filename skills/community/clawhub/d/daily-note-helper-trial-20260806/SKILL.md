---
name: daily-note-helper
description: Create and organize daily work notes with consistent structure, date-based filenames, and lightweight summaries. Use when the user wants to start a daily log, append structured entries to today's note, review recent notes, or generate a concise recap from multiple daily files.
---

# Daily Note Helper

Create or update daily notes under `memory/` using a predictable structure.

## Workflow

1. Determine today's date in the user's local timezone when available; otherwise use the runtime timezone.
2. Use the filename pattern `memory/YYYY-MM-DD.md`.
3. If the file does not exist, create it with the template in `references/note-template.md`.
4. Append new entries under the appropriate section heading.
5. Keep entries concise, timestamped, and action-oriented.
6. When asked for a recap, read the requested date range and summarize decisions, blockers, and follow-ups.

## Entry format

Use this bullet format:

```markdown
- HH:MM — Topic: what happened; any next step.
```

## Guidelines

- Prefer appending over rewriting.
- Preserve existing content exactly unless the user asks to reorganize.
- Do not duplicate the same event across sections.
- Store durable facts in `MEMORY.md`; keep raw chronological detail in daily files.
- If `memory/` does not exist, create it.

## Resources

- Read `references/note-template.md` before creating a new daily file.
- Run `scripts/new_note.py <YYYY-MM-DD>` to scaffold a note safely.
