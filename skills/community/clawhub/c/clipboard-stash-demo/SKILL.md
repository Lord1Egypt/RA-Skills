---
name: clipboard-stash
description: Stash and recall short text snippets in a local file-backed clipboard. Use when the user wants to save a quick note or quote ("记一下"/"先放着"/"待会儿用") and retrieve it later in the same workspace without setting up a database or external service.
metadata:
  requires:
    bins: ["bash"]
---

# clipboard-stash

A tiny, dependency-free "scratch clipboard" backed by `~/.cache/clipboard-stash/stash.tsv`.
Each entry has a slug, timestamp, and one-line content. Multi-line text is preserved
via `\n` escaping inside the TSV.

## When to use

- The user says "stash this", "记一下这段", "先放着待会用", or asks to recall a previous snippet.
- You need a session-spanning scratch buffer that survives shell restarts but does
  not deserve a real note in `MEMORY.md`.

## When NOT to use

- For long-term knowledge that belongs in `MEMORY.md` or `memory/YYYY-MM-DD.md`.
- For binary content, files, or anything > ~4 KB per entry.
- For secrets — the stash file is plaintext.

## Commands

All commands are pure bash one-liners — no install needed.

### Save a snippet

```bash
mkdir -p ~/.cache/clipboard-stash
slug="$1"; shift; content="$*"
printf '%s\t%s\t%s\n' "$slug" "$(date -Is)" "${content//$'\n'/\\n}" \
  >> ~/.cache/clipboard-stash/stash.tsv
```

### List recent snippets

```bash
tail -n 20 ~/.cache/clipboard-stash/stash.tsv | column -t -s $'\t'
```

### Recall by slug (latest match)

```bash
slug="$1"
awk -F'\t' -v s="$slug" '$1==s {last=$0} END {print last}' \
  ~/.cache/clipboard-stash/stash.tsv \
  | awk -F'\t' '{gsub(/\\n/, "\n", $3); print $3}'
```

### Clear all

```bash
: > ~/.cache/clipboard-stash/stash.tsv
```

## Notes

- TSV columns: `slug \t iso8601 \t content` (newlines escaped as `\n`).
- Slugs are not unique — recall returns the latest matching entry.
- Safe to `cat` the file directly to inspect history.
