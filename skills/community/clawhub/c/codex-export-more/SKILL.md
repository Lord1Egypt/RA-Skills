---
name: codex-export
description: Export a Codex CLI or Codex Desktop (App) session to Markdown, HTML, or Obsidian notes. Use when the user asks to export, save, share, or review a past chat, session, or transcript. Supports --brief, --redact, --since/--until, --grep, --append (incremental), --interactive (message picker), --sessions (merge), --watch (auto-incremental), and --list. Works with both Codex CLI and Codex Desktop app sessions.
---

# codex-export

Export any Codex session (`$CODEX_HOME/sessions/**/*.jsonl`, default `~/.codex/sessions`) to a clean Markdown file.

## Usage

```bash
# List recent sessions (pick by number or copy the ID)
python3 scripts/export.py --list

# Export by session ID
python3 scripts/export.py <session-id> output.md

# Brief mode: user + assistant only, no tool calls
python3 scripts/export.py <session-id> output.md --brief

# Time range
python3 scripts/export.py <session-id> output.md --since 2026-08-10 --until 2026-08-11 --brief

# Content filter (a matched question pulls in its full turn)
python3 scripts/export.py <session-id> output.md --grep "Typora" --brief

# Incremental export: append only new messages, preserving manual edits
python3 scripts/export.py <session-id> output.md --brief --append

# Redact emails/tokens/paths for safe sharing
python3 scripts/export.py <session-id> output.md --brief --redact

# HTML or Obsidian output
python3 scripts/export.py <session-id> session.html --format html
python3 scripts/export.py <session-id> session.md --format obsidian

# Interactive picker
python3 scripts/export.py <session-id> picked.md --interactive

# Merge sessions
python3 scripts/export.py --sessions id1,id2 merged.md --brief

# Auto-incremental watch mode
python3 scripts/export.py <session-id> notes.md --brief --watch 60
```

## Notes

- Honors `$CODEX_HOME`; falls back to `~/.codex`
- Merges multi-rollout sessions and dedups by message ID
- Explicit UTF-8 I/O; works on Windows/zh-CN without `PYTHONUTF8`
- Injected system blocks (app-context, in-app-browser-context, etc.) are stripped
- System/developer messages and injected context blocks are filtered automatically
- Tool call outputs are included by default; use `--brief` to strip them
- Checkpoint for `--append` lives in `<output>.state.json`
