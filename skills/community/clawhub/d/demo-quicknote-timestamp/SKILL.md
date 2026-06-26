---
name: quicknote
description: Quickly append a timestamped note to a local markdown file. Use when you need to jot down a fleeting thought, observation, or reminder without leaving the current workflow.
metadata: { "openclaw": { "emoji": "📝" } }
---

# QuickNote

Append a timestamped line to a note file.

## Usage

1. Pick or create a target file (default: `notes.md` in workspace root).
2. Append the note with an ISO timestamp prefix.
3. Done — no further action needed.

## Example

```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) — Draft the weekly summary" >> notes.md
```
