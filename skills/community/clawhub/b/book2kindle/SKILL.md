---
name: book2kindle
description: Search Z-Library and send EPUBs to Kindle
disable-model-invocation: true
argument-hint: send "title" or search "title"
allowed-tools: Bash(.venv/bin/book2kindle *)
---

Run the book2kindle CLI to search Z-Library and send EPUBs to Kindle.

Execute: `.venv/bin/book2kindle $ARGUMENTS`

## Behavior

- If `$ARGUMENTS` is empty, run `.venv/bin/book2kindle --help` and present the available commands.
- For `search <title>`: run `.venv/bin/book2kindle search "<title>"` and display the results as a numbered list.
- For `send <title> --pick N`: run `.venv/bin/book2kindle send "<title>" --pick N` directly.
- For `send <title>` without `--pick`: first run `.venv/bin/book2kindle search "<title>"` to show results, then ask the user which one to send. Once they choose, run `.venv/bin/book2kindle send "<title>" --pick N`.
- Pass through any other flags the user provides (e.g. `--pick`, `--limit`).

## Output

Present CLI output conversationally. Summarize results clearly — show book title, author, format, and file size when available.
