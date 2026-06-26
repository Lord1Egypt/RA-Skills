---
name: research-assistant
version: 0.1.0
description: Enrich Bear research notes tagged 「待整理」 with theme-matched GIFs. Use when the user wants to auto-illustrate pending research notes, batch-process Bear notes for visual enrichment, or automate the "find a fitting GIF" step of note cleanup. Requires Bear + grizzly CLI.
---

# Research Assistant

Process Bear notes tagged 「待整理」: extract topics, find matching GIFs, insert them, then remove the tag.

## Workflow

1. **Fetch pending notes** — run `scripts/process_notes.sh list` to get all notes with the 待整理 tag.
2. **For each note**, run `scripts/enrich_note.sh <note-id>` which:
   - Reads the note content via `grizzly open-note`
   - Extracts key topic phrases (first H1, bold terms, or first sentence)
   - Searches for a relevant GIF via Tenor API (falls back to Giphy)
   - Appends the GIF as a markdown image at the end of the note
   - Removes the 待整理 tag and adds 已整理 tag
3. **Report** — summarize how many notes were enriched and any failures.

## Requirements

- Bear app running on macOS
- `grizzly` CLI installed (`go install github.com/tylerwince/grizzly/cmd/grizzly@latest`)
- Bear token at `~/.config/grizzly/token`
- `TENOR_API_KEY` or `GIPHY_API_KEY` env var (free tier works)

## Scripts

- `scripts/process_notes.sh list` — list note IDs with 待整理 tag
- `scripts/enrich_note.sh <note-id>` — enrich a single note with a GIF
