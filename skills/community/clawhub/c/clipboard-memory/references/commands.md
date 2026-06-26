# Clipboard Memory — Commands Reference

Full flag and subcommand reference for `clipmem`. This file is kept byte-identical across the OpenClaw-native and portable skill packages.

---

## Decision ladder

Pick the narrowest command that answers the question. Always pass `--format json` (or `--format toon` for plain enumeration) when parsing programmatically.

1. `clipmem recall "<query>" --format json` — best-first ranked answer with alternatives. **Start here.**
2. `clipmem timeline --hours <N> --format json` — chronological capture events. Use when the user says "today", "yesterday", "in order", or "every time".
3. `clipmem recent --hours <N> --format json` — deduplicated recent snapshots. Use for "recent unique things".
4. `clipmem search "<query>" --format json` — direct lexical / FTS match. Use when you need precise substring hits.
5. `clipmem get <snapshot_id> --format json` — nested item/representation detail for a snapshot you already have.
6. `clipmem restore <snapshot_id>` — restore the full stored representation set for a snapshot back onto the macOS clipboard.
7. `clipmem export <snapshot_id> --item <n> --uti <uti> --out <path> [--force]` — raw bytes for binary/image/PDF payloads.
8. `clipmem forget <snapshot_id>` — hard-delete one snapshot and its capture history.
9. `clipmem purge --older-than <duration> [--dry-run]` — prune by `last_observed_at`.
10. `clipmem storage compact [--dry-run] --format json` — reclaim SQLite/WAL disk space without changing content.
11. `clipmem storage image-candidates --format json` — inspect image rows eligible for optimization without rewriting bytes.
12. `clipmem storage optimize-images [--dry-run] [--no-compact] [--limit N] [--format json|--progress jsonl]` — convert eligible stored images to lossless WebP and compact by default.
13. `clipmem service providers --format json` — inspect service provider availability without starting or stopping capture.
14. `clipmem service revision --format json` — read archive revision counters without probing service providers.
15. `clipmem settings show --format json` — inspect persistent capture policy.
16. `clipmem app settings show --format json` — inspect menu bar app preferences.
17. `clipmem app settings set KEY VALUE --format json` / `clear KEY --format json` — change app-local preferences and bump app preference revision.
18. `clipmem app launch-at-login show|set|clear --format json` — inspect or change the app-owned launch-at-login preference bridge.
19. `clipmem app update-check show|run|clear --format json` — inspect, run, or clear app update-check state.
20. `clipmem app quit --format json` — request the menu bar app to quit.
21. `clipmem agents context --format json` — one-call agent context: generated_at, service health, settings, app state, recent activity metadata, revision, stats, privacy guidance, and capability summary.
22. `clipmem ocr status --format json` — inspect local OCR queue and result counts.
23. `clipmem ocr candidates --format json` — inspect pending OCR candidates without running OCR.
24. `clipmem ocr get <raw-sha256> --format json` / `clear <raw-sha256> --format json` — inspect or clear one OCR result.
25. `clipmem ocr run [--limit N] [--snapshot ID]` — backfill OCR for image snapshots.

Primitive commands are the direct read/list/get/set/delete/start/stop surfaces
above. Convenience workflows are still supported but should be classified
honestly: `recall` ranks likely answers, `setup` composes initialization plus
service startup, `ocr run` processes a bounded OCR batch, and
`storage optimize-images` scans and rewrites eligible image rows. Use
candidate, dry-run, or detail commands before broad workflow mutations when the
user has not explicitly asked to proceed.

---

## Subcommand matrix

| Subcommand | Default `--format` | Supports `toon`? | Purpose |
|---|---|---|---|
| `recall [QUERY]` | `md` | yes | Ranked best-first answer with alternatives |
| `search <QUERY>` | `text` | yes | Lexical / FTS match over the archive |
| `recent` | `text` | yes | Recent unique snapshots (deduplicated) |
| `timeline` | `text` | yes | Chronological capture events (not deduped) |
| `get <SNAPSHOT_ID>` | `text` | **no** | Nested detail for one snapshot |
| `restore <SNAPSHOT_ID>` | text | — | Restore a stored snapshot back onto the clipboard |
| `export <SNAPSHOT_ID>` | — (raw bytes) | — | Write one representation to disk |
| `forget <SNAPSHOT_ID>` | text | — | Hard-delete one snapshot and its capture history |
| `purge` | text | — | Delete old snapshots by `last_observed_at` |
| `storage compact` | text (`json` supported) | — | Reclaim SQLite/WAL disk space |
| `storage image-candidates` | text (`json` supported) | — | List image rows eligible for optimization without mutation |
| `storage optimize-images` | text (`json` supported, progress JSONL available) | — | Convert eligible images to lossless WebP |
| `settings show` | `text` | **no** | Show persistent pause / retention / ignore-list policy |
| `settings pause` | text | — | Persistently pause or resume capture; supports `json` and `human` |
| `settings api-key-filter` | text | — | Enable or disable API key filtering; supports `json` and `human` |
| `settings ocr` | text | — | Enable or disable local OCR for new image captures; supports `json` and `human` |
| `settings retention` | text | — | Set retention to a duration or `forever`; supports `json` and `human` |
| `settings reset` | text (`json` supported) | — | Reset capture policy and ignored apps to defaults |
| `settings ignore add/remove/list` | text | **no** | Manage ignored bundle identifiers; supports `json` and `human` |
| `app settings show` | text (`json` supported) | — | Show menu bar app preferences |
| `app settings set` | text (`json` supported) | — | Set one menu bar app preference |
| `app settings clear` | text (`json` supported) | — | Clear one menu bar app preference |
| `app launch-at-login show/set/clear` | text (`json` supported) | — | Manage the app-owned launch-at-login preference bridge |
| `app update-check show/run/clear` | text (`json` supported) | — | Show, run, or clear app update-check state |
| `app quit` | text (`json` supported) | — | Request the menu bar app to quit |
| `agents context` | text (`json` supported) | — | Agent context bundle: generated_at, health, settings, app state, recent activity, revision, stats, privacy, capabilities |
| `ocr status` | text (`json` supported) | — | Local OCR queue and result counts |
| `ocr candidates` | text (`json` supported) | — | Pending OCR candidate hashes without processing |
| `ocr get` | text (`json` supported) | — | One OCR result by raw representation hash |
| `ocr clear` | text (`json` supported) | — | Delete one OCR result and rebuild affected OCR cache |
| `ocr run` | text (`json` supported) | — | Backfill OCR for stored image snapshots |
| `capture-once` | — | — | Single clipboard capture (setup / ad-hoc) |
| `watch` | — | — | Background daemon; usually a LaunchAgent |
| `setup` | — | — | Seed one capture and start background capture |
| `service status` | text (or `--json`) | — | Background provider state + capture freshness |
| `service providers` | text (`json` supported) | — | Service provider availability without mutation |
| `service revision` | text (`json` supported) | — | Archive revision counters without provider probes |
| `service start` / `stop` / `uninstall` | — | — | Manage the background watcher service |
| `doctor` | text (or `--json`) | — | SQLite / FTS5 diagnostics |
| `agents openclaw doctor` | text | — | Integration health: PATH, workspace, sandbox |
| `agents openclaw install-skill` | — | — | Write packaged skill files to disk |
| `agents openclaw print-skill` | — | — | Print embedded `SKILL.md` to stdout |
| `agents openclaw uninstall-skill` | — | — | Remove installed skill directory |
| `agents hermes doctor` | text | — | Hermes integration health: PATH, skill discovery |
| `agents hermes install-skill` | — | — | Write packaged Hermes skill to disk |
| `agents hermes print-skill` | — | — | Print embedded Hermes `SKILL.md` to stdout |
| `agents hermes uninstall-skill` | — | — | Remove installed Hermes skill directory |

`--json` is a compatibility alias for `--format json` on `search`, `recent`, `timeline`, `get`, `agents context`, `storage compact`, `storage optimize-images`, `ocr status`, `ocr run`, `capture-once`, and `doctor`.

---

## Output formats

All retrieval commands share the same `--format` set except `get`, which omits `toon`:

- `text` — human-oriented terminal output. Default for `search`, `recent`, `timeline`, `get`. **Do not parse.**
- `md` — compact markdown. Default for `recall`. Human-oriented. **Do not parse.**
- `json` — single structured object with a stable envelope. Parse this.
- `jsonl` — newline-delimited rows. Prefer when streaming many results through a pipe.
- `toon` — flat token-efficient list. Prefer for `timeline`, `search`, `recent`, and `recall` when you only need the top fields. Unsupported on `get`.

---

## Shared retrieval filters

`search`, `recent`, `timeline`, and `recall` accept the same filter set. `get` and `export` accept them as guards against the explicitly targeted snapshot.

**Time window:**

- `--since <RFC3339>` — captures at or after this timestamp (e.g. `2026-04-16T09:00:00Z`).
- `--until <RFC3339>` — captures at or before this timestamp.
- `--hours <N>` — last N hours. `--since` wins if both are provided.

**Source:**

- `--app <name>` — case-insensitive substring match on the recorded frontmost app name.
- `--bundle-id <id>` — case-insensitive exact match on bundle identifier (e.g. `com.apple.Safari`).

**Content shape:**

- `--kind text|html|rtf|url|file|image|pdf|binary|other`. One value per invocation.
- `--has-text`, `--has-url`, `--has-file-url`, `--has-image`, `--has-pdf` — additive presence flags (AND semantics).

**Size:**

- `--min-bytes <N>` / `--max-bytes <N>` — applied to the total snapshot byte count.

### `--kind` values

| Value | Matches |
|---|---|
| `text` | plain text representations |
| `html` | HTML clipboard payloads |
| `rtf` | rich-text format |
| `url` | web URLs |
| `file` | **file URLs (Finder paths)** — not regular files on disk |
| `image` | image blobs (PNG, JPEG, TIFF, etc.) |
| `pdf` | PDF documents |
| `binary` | opaque binary that has no safe text projection |
| `other` | mixed or empty snapshots |

`--kind file` is a common pitfall: it matches clipboard-as-file-URL payloads (things dragged from Finder), not arbitrary files the user happened to reference.

---

## Pagination

List commands (`search`, `recent`, `timeline`) accept `--limit` and `--cursor`:

- `--limit <N>` — 1–250, default 10.
- `--cursor <opaque>` — resume from a `next_cursor` returned by a prior response.

Cursors are tied to the active query, mode, and filters. Changing any of those while paginating will reject the cursor. When a response includes `"truncated": true` and a non-null `next_cursor`, there are more rows.

```bash
clipmem search "git status" --format json --limit 25
clipmem search "git status" --format json --limit 25 --cursor "<next_cursor>"
```

---

## Search modes (`search`, `recall`)

`--mode auto|fts|literal`, default `auto`.

- `auto` — picks FTS or literal per query. Prefers literal for URLs, paths, bundle ids, dotted identifiers, and shell fragments (`--flag=value`, pipes, subshells). Plain prose queries try FTS first.
- `fts` — strict SQLite FTS5. Use when you want to compose boolean queries: `"launchctl" AND bootstrap`.
- `literal` — exact substring match. Use for punctuation-heavy strings like `50%`, `Co-Authored-By:`, or URL fragments.

Rules of thumb:

- Query contains `"`, `AND`, `OR`, `NOT` → `--mode fts`.
- Query contains `/`, `.`, `:`, `%`, or shell metacharacters → `--mode literal`.
- Short natural-language query → let `--mode auto` pick.

---

## `recall` extras

On top of the shared filters:

- `--format md|json|toon` (default `md`).
- `--limit <N>` — ranked candidates to consider (default 5).
- `--full` — expand the best candidate text instead of the compact form.
- `--quote` — force quoted best-text output.
- `--min-score <0.0-1.0>` — threshold below which a query alone is not trusted; falls back to recency / filters.
- `--prefer-recent` — bias ranking toward recency.
- `--prefer-app <name>` — bias toward matching app or bundle id.
- `--hours <N>` — window for the recent-fallback when a query is weak.

If the user has no query but said "the thing I just copied":

```bash
clipmem recall --prefer-recent --hours 24 --format json --limit 5
```

---

## `get`, `restore`, and `export`

```bash
clipmem get <snapshot_id> --format json        # nested representation detail
clipmem get <snapshot_id> --events <N>         # include last N capture events (default 10)
clipmem restore <snapshot_id>                  # restore the whole snapshot to the clipboard
clipmem export <snapshot_id> --item <index> --uti <uti> --out <path> [--force]
```

`get --format json` flattens the common text fields on the root snapshot so agents don't have to walk the representation tree. `get` does **not** support `--format toon`.

`restore` is macOS-only and writes the full stored item/UTI/raw-byte set back onto the general pasteboard. This is a whole-snapshot restore, not a text-only approximation.

`export` writes raw bytes to `--out` and supports `--format json` for structured confirmation. By default it creates a new file and refuses to replace an existing destination; pass `--force` only to replace an existing regular file. Symlink destinations are rejected. Required arguments: `--item` (0-based), `--uti` (e.g. `public.png`, `public.utf8-plain-text`, `com.adobe.pdf`), `--out`. Inspect `items[].representations[].uti` and `size_bytes` in a prior `get --format json` to choose the right combination.

---

## `forget`, `purge`, `storage`, and `settings`

```bash
clipmem forget <snapshot_id>
clipmem purge --older-than 30d [--dry-run]
clipmem storage compact [--dry-run] [--format json]
clipmem storage image-candidates [--limit N] [--format json]
clipmem storage optimize-images [--dry-run] [--no-compact] [--limit N] [--format json|--progress jsonl]
clipmem settings show [--format json]
clipmem settings pause on|off [--format json]
clipmem settings api-key-filter on|off [--format json]
clipmem settings ocr on|off [--format json]
clipmem settings retention <duration|forever> [--format json]
clipmem settings reset [--format json]
clipmem settings ignore add <bundle_id> [--format json]
clipmem settings ignore remove <bundle_id> [--format json]
clipmem settings ignore list [--format json]
clipmem app settings show [--format json]
clipmem app settings set binary-path-override <path> [--format json]
clipmem app settings set database-path-override <path> [--format json]
clipmem app settings set default-recent-hours <hours> [--format json]
clipmem app settings set default-query-mode recall|search|recent|timeline|diagnostics [--format json]
clipmem app settings set hotkey-enabled true|false [--format json]
clipmem app settings clear <key> [--format json]
clipmem app launch-at-login show [--format json]
clipmem app launch-at-login set on|off [--format json]
clipmem app launch-at-login clear [--format json]
clipmem app update-check show [--format json]
clipmem app update-check run [--format json]
clipmem app update-check clear [--format json]
clipmem app quit [--format json]
clipmem service revision [--format json]
clipmem ocr status [--format json]
clipmem ocr candidates [--limit N] [--snapshot ID] [--format json]
clipmem ocr get <raw-sha256> [--format json]
clipmem ocr clear <raw-sha256> [--format json]
clipmem ocr run [--limit N] [--snapshot ID] [--retry-failed] [--format json]
```

`forget` is a hard delete. It removes the snapshot row, all child items/representations, and all capture events for that snapshot id via foreign-key cascades. OCR results with no remaining representation referencing their image hash are also removed.

`purge` computes age from `snapshot_stats.last_observed_at`, not `snapshots.created_at`. Duration grammar is a single integer plus one unit: `Nd`, `Nh`, or `Nm`.

`storage compact` checkpoints WAL state and vacuums SQLite pages back to the filesystem. It never changes clipboard content. `storage image-candidates` lists the same eligible image rows that `storage optimize-images` would scan, without rewriting bytes or marking rows. `storage optimize-images` rewrites eligible image representations to lossless WebP only when doing so saves meaningful space, then compacts SQLite storage by default; already compressed or skipped rows are not retried by normal runs. Use `--progress jsonl` for streamed `started`, `scanning`, `compacting`, and `complete` progress events. Use `--no-compact` only when batching optimization runs and compacting once at the end.

`ocr candidates` lists pending OCR hashes and affected snapshot counts without invoking Apple Vision. Use it before `ocr run` when an agent needs to inspect queue work.

`settings` is the persistent capture-policy entrypoint. Ignore matching is exact, case-insensitive bundle-id matching only. OCR is opt-in, runs locally through Apple Vision on macOS, and stores text/status separately from raw image bytes.

`app settings`, `app launch-at-login`, and `app update-check` are menu bar app state bridges. They read and write app-local preferences without changing archive capture policy. Mutating commands bump `app_preferences_revision` so an open app can observe external agent changes. Launch-at-login writes the desired app-owned preference; the menu bar app applies it through `SMAppService`. `app update-check run` performs the live latest-stable-release lookup and updates the same cache the app reads. `app quit` requests the menu bar app to terminate through the app bundle identifier.

`clipmem agents context --format json` is safe as a first call in agent sessions. It includes `generated_at`, service health, capture policy, archive revision, bounded recent activity, menu bar app state, capability discovery, and privacy guidance. It excludes raw clipboard content and representation bytes, but includes operational metadata such as app names, timestamps, counts, paths, and app preference state.

`clipmem service revision --format json` is the lightweight polling path for change detection. It reads the same archive revision counters surfaced in service status and agent context without checking Homebrew, LaunchAgent, or other service providers.

---

## Global flags

- `--db <path>` — override the SQLite database path. Default: `~/Library/Application Support/clipmem/clipmem.sqlite3` on macOS. Use this only when pointing at an alternate archive (tests, backups).

## Environment

- `CLIPMEM_OPENCLAW_WORKSPACE` — overrides the OpenClaw workspace root used by `agents openclaw install-skill` and `agents openclaw doctor`. Falls back to `openclaw config get agents.defaults.workspace`, then `~/.openclaw/workspace`.
- `HOME` — resolves `~/` in default paths.

---

## Exit codes

- `0` — success
- `1` — uncategorized runtime failure
- `2` — invalid args
- `3` — not found (e.g. snapshot id, representation)
- `4` — unsupported format for this subcommand (e.g. `--format toon` on `get`)
- `5` — database error
- `6` — platform error (macOS API / filesystem)

Scripts can rely on these to distinguish "no such snapshot" (retriable with a different id) from "database locked" (retry with backoff) from "wrong format" (agent bug).

---

## Script-friendly guarantees

- stdout contains only the requested command output.
- stderr contains diagnostics only.
- No interactive prompts anywhere in the CLI.
- List commands use bounded `--limit` defaults and opaque cursor pagination.
- Retrieval JSON envelopes (`search`, `recent`, `timeline`, `get`, `recall`, and mutation confirmations that include `schema_version`) are stable within `schema_version: 2`. Management and inspection commands such as `agents context`, `app`, `service`, `ocr`, and `storage image-candidates` have command-specific JSON shapes; parse their documented keys directly and do not require `schema_version: 2` unless the command emits it.
