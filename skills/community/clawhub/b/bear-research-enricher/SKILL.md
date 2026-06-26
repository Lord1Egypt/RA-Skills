---
name: research-assistant
description: Enrich Bear research notes tagged 「待整理」 with thematic GIFs. Use when the user wants to auto-illustrate or spruce up draft research notes in Bear, or mentions "待整理", "research notes", "add GIFs to notes", or "enrich notes".
version: 0.1.0
---

# Research Assistant

Read Bear notes tagged 「待整理」, extract key topics, search for matching GIFs via gifgrep, and insert them inline. When done, remove the 「待整理」 tag and add 「已整理」.

## Prerequisites

- Bear app running on macOS with a valid API token at `~/.config/grizzly/token`
- `grizzly` CLI installed (`go install github.com/tylerwince/grizzly/cmd/grizzly@latest`)
- `gifgrep` skill installed (provides GIF search)
- `curl` available

## Workflow

1. **Fetch notes**: Run `grizzly open-tag --name "待整理" --enable-callback --json --token-file ~/.config/grizzly/token` to list all notes with the tag.
2. **For each note**:
   a. Read note content via `grizzly open-note --id <NOTE_ID> --enable-callback --json --token-file ~/.config/grizzly/token`
   b. Extract 2–3 key topics or keywords from the note title and first paragraph.
   c. For each keyword, search GIFs using the gifgrep skill (or `curl "https://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&q=<keyword>&limit=3"` as fallback).
   d. Pick the most relevant GIF URL per keyword.
   e. Append GIFs to the note using `grizzly add-text`:
      ```
      echo -e "\n---\n![<keyword>](<gif_url>)" | grizzly add-text --id <NOTE_ID> --mode append --token-file ~/.config/grizzly/token
      ```
3. **Retag**: Remove 「待整理」 and add 「已整理」 by updating note tags via Bear's x-callback-url:
   ```
   open "bear://x-callback-url/add-tag?id=<NOTE_ID>&name=已整理"
   open "bear://x-callback-url/remove-tag?id=<NOTE_ID>&name=待整理"
   ```
4. **Report**: Summarize which notes were enriched and how many GIFs were added.

## Script

For batch processing, use `scripts/enrich_notes.sh`:

```bash
bash scripts/enrich_notes.sh
```

The script handles the full loop: fetch tagged notes → per-note topic extraction → GIF search → insert → retag.

## Notes

- If no notes carry the 「待整理」 tag, report that and exit.
- If GIF search returns no results for a keyword, skip that keyword rather than inserting a placeholder.
- Bear must be running; grizzly commands will fail silently otherwise.
- Rate-limit GIF API calls (1 request/second) to avoid throttling.
