---
name: clipboard-memory
description: Recall what the user copied on this Mac via the local clipmem archive — text, commands, URLs, file paths, HTML, images, PDFs. Triggers on requests like "what was that command I copied?", "the URL I copied from Safari", "find that snippet before I restarted", or any paraphrase involving copy, paste, or clipboard. Offers ranked recall, chronological timeline, lexical / FTS search, raw-byte export for binary content, cursor pagination, and filters by app, kind, time window, and content shape. Use before reaching for generic web or repo search whenever the user is trying to recover something they previously had on the clipboard.
license: MIT
metadata: {"openclaw":{"emoji":"📋","os":["darwin"],"requires":{"bins":["clipmem"]},"install":[{"id":"brew","kind":"brew","label":"Install clipmem (brew)","bins":["clipmem"],"formula":"clipmem","tap":"tristanmanchester/tap"},{"id":"cargo","kind":"cargo","label":"Install clipmem (cargo)","bins":["clipmem"],"package":"clipmem"}],"version":"1.3.7"}}
---

Recall what the user copied on this Mac before reaching for generic search. `clipmem` maintains a local, privacy-preserving SQLite archive of every clipboard state macOS emits, and exposes a JSON-first CLI built for agents. This package is installed by `clipmem agents openclaw install-skill`; the canonical cross-agent source lives under `skills/clipboard-memory/`.

## Use this skill when

The user asks things like:

- "what was that command I copied?"
- "show me the URL I copied from Safari earlier"
- "find that snippet, path, note, or link I copied yesterday"
- "give me the exact text I copied, not a summary"
- "what did I copy before I restarted?"
- "paste me back that SQL I was looking at"
- "get the PDF I copied last week"
- "show me everything I copied from Xcode today"

## Do not use this skill for

- web search or current-events lookups
- searching the repository or local files the user never copied
- content the user typed but never copied to the clipboard
- anything on a non-macOS machine (`clipmem` captures `NSPasteboard` only)

## Prerequisites

Before querying, confirm the setup is healthy — otherwise empty results may be a stale watcher, not a true miss:

1. Background capture must be running. `clipmem setup` is the canonical fix; Homebrew users can also use `brew services start clipmem`.
2. The binary `clipmem` must be on PATH with write access to `~/Library/Application Support/clipmem/clipmem.sqlite3`.
3. Run [`scripts/check-setup.sh`](scripts/check-setup.sh) once per session when results look wrong. It exits `0` on a healthy host, `1` if the watcher is stale, `2` if the binary is missing, `3` if `clipmem doctor` fails. The prose equivalent is in [references/setup-check.md](references/setup-check.md).
4. If OpenClaw cannot see the binary, run `clipmem agents openclaw doctor` and follow its remediation lines.

## Command ladder

Always pick the narrowest command that answers the question, and always pass `--format json` (or `--format toon` for plain enumeration) so you can parse the response deterministically.

1. **`clipmem recall`** — best-first ranked answer with alternatives. Start here for almost every request.
2. **`clipmem timeline`** — chronological capture events (one row per copy), including repeated copies of the same content. Use for "today", "yesterday", "in order", or "every time".
3. **`clipmem search`** — direct lexical / FTS matching. Use when you need precise substring hits or the user gave you an exact phrase.
4. **`clipmem get <snapshot_id>`** — nested item/representation detail for a single snapshot already in hand.
5. **`clipmem export <snapshot_id> --item <n> --uti <uti> --out <path> [--force]`** — raw bytes. Use when the stored content is binary/image/PDF and `best_text` is empty or partial. Prefer a fresh output path; use `--force` only to replace an existing regular file.
6. **`clipmem ocr candidates`, `clipmem ocr get`, `clipmem ocr clear`, and `clipmem storage image-candidates`** — inspect queued OCR or image optimization work before running batch workflows, or clear one stale OCR result.
7. **`clipmem settings reset --format json`** — reset capture policy and ignored apps when the user explicitly asks to restore defaults.
8. **`clipmem service providers --format json`** — inspect service provider state without starting or stopping capture.
9. **`clipmem service revision --format json`** — inspect archive revision counters without probing service providers.
10. **`clipmem app settings`, `clipmem app launch-at-login`, `clipmem app update-check run`, or `clipmem app quit` with `--format json`** — inspect or change menu bar app preferences and app-owned state when the user asks about app defaults, update checks, or quitting the app.
11. **`clipmem agents context --format json`** — compact health, settings, app state, recent activity, revision, stats, privacy, and capability context before multi-step work.

## Primitive command taxonomy

Primitive commands expose one bounded read or mutation that can be composed
directly. Convenience workflows such as `recall`, `setup`, `purge`, `ocr run`, and
`storage optimize-images` remain useful, but verify uncertain results with
`search`, `recent`, `timeline`, or `get`, and preview broad mutations with
candidate or dry-run commands when available.

The full flag reference, JSON envelope, and kind values live in [references/commands.md](references/commands.md), [references/json-schema.md](references/json-schema.md), and [references/examples.md](references/examples.md).

## Critical behaviour rules

- Before answering from a stale, empty, or ambiguous archive, run `clipmem agents context --format json` and use `generated_at`, health, settings, app state, recent activity, revision, stats, privacy, and capability fields to decide whether to broaden search or diagnose setup.
- Always use `--format json` when you will parse the response. `--format toon` is for token-efficient enumeration only. `--format jsonl` is for streaming many rows into a pipeline. Never parse `md` or `text`.
- Treat `recall` as a convenience ranking helper, not an authority. For uncertain cases, compose primitive commands in this order: `search`, `recent`, `timeline`, `get`, then OS follow-through such as `pbcopy`, `open`, or `open -R`.
- Never claim "nothing found" until you have broadened the search once and checked `truncated` / `next_cursor`.
- When `best_match_confidence` is `"low"` or there are several plausible hits, present the top candidates instead of pretending certainty.
- For exact-text requests, quote `best_text` verbatim. Do not paraphrase commands, SQL, code, URLs, or file paths unless the user asked for a summary.

## Capability map

The repo-side agent-native action parity contract lives in `docs/action-parity.md`. Use it when you need the maintained map from user-visible outcomes to agent-accessible commands, entity CRUD expectations, and derived-cache boundaries.

## Output format rule

- `--format json` — structured output. Retrieval envelopes are stable within `schema_version: 2`; management and inspection commands use command-specific JSON shapes, so parse documented keys directly.
- `--format toon` — flat, token-efficient list. Prefer for high-cardinality enumeration (`timeline`, `search`, `recent`, `recall`) when you only need the top fields. Note: `get` does **not** support `toon`.
- `--format jsonl` — newline-delimited records. Use when streaming many rows into a pipeline.
- `--format md` / `--format text` — human-readable previews only; never parse these.

`--json` is an alias for `--format json` on `search`, `recent`, `timeline`, `get`, `service revision`, `capture-once`, and `doctor`.

## Which command for which intent

| User intent | First command |
|---|---|
| "what was that thing I copied" (no time cue) | `recall "<query>" --format json` |
| "what did I copy today / yesterday / in order" | `timeline --hours <N> --format json` |
| "recent unique things I copied" | `recent --hours <N> --format json` |
| exact substring or punctuation-heavy query | `search --mode literal "<query>" --format json` |
| already have a snapshot id | `get <id> --format json` |
| need raw image / PDF bytes | `get <id>` then `export <id> --item <n> --uti <uti> --out <path>` |

`recall` vs `recent` vs `timeline`:

- `recall` ranks across the archive and returns a best candidate plus alternatives.
- `recent` deduplicates by snapshot — identical copies collapse into one row.
- `timeline` is event-centric — every capture event is its own row, even if the content repeats.

## Quick examples

```bash
# best-first answer
clipmem recall "that command I copied" --format json --limit 5

# Safari today, token-efficient
clipmem recall --prefer-recent --app safari --hours 24 --format toon

# exact URL yesterday
clipmem recall "url" --has-url --hours 48 --format json

# chronological sweep, paginated
clipmem timeline --hours 24 --limit 25 --format json
clipmem timeline --hours 24 --limit 25 --cursor "<next_cursor>" --format json

# recover an image
clipmem get 42 --format json
clipmem export 42 --item 0 --uti public.png --out ./clipboard.png
clipmem export 42 --item 0 --uti public.png --out ./clipboard.png --force
```

## Reading the response

Read these JSON fields first; walk nested `items[].representations[]` only after a `get` call:

- `best_candidate.best_text` — the flattened primary text.
- `best_candidate.urls` — URL array (empty when none).
- `best_candidate.file_paths` — file-URL array.
- `why_selected`, `best_match_confidence`, `alternatives` (only on `recall`).
- `next_cursor`, `truncated` — pagination state.
- `schema_version` — pin to `2` for stability.

Full schema in [references/json-schema.md](references/json-schema.md).

## Troubleshooting

If `recall` looks empty or weak, widen `--hours`, drop source filters, or switch to `timeline` / `search`. For setup issues, sandbox PATH problems, or binary-only snapshots, see [references/troubleshooting.md](references/troubleshooting.md).

## Exit codes

`0` success · `1` uncategorized runtime · `2` invalid args · `3` not found · `4` unsupported format · `5` database error · `6` platform error.
