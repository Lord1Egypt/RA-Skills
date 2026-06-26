# Clipboard Memory — Troubleshooting

Diagnose before reinterpreting. Most "nothing found" outcomes are a stale watcher or a mismatched filter, not a true miss.

Start by running `scripts/check-setup.sh` (installed alongside this skill) or the prose in [setup-check.md](setup-check.md).

---

## Empty or weak `recall` result

Do these in order, stopping when the result improves:

1. **Widen the time window.** `--hours 72`, or drop `--hours` entirely.
2. **Remove source filters.** The user's memory of which app doesn't always match what `clipmem` recorded as the frontmost process.
3. **Switch to `timeline`.** If the user said "today" or "yesterday", chronological order + filters often finds things `recall`'s ranker misses.
4. **Switch to `search`.** For exact phrases or punctuation-heavy strings, try `--mode literal`.
5. **Loosen content shape.** Drop `--kind`, `--has-url`, `--has-text` flags — they may be excluding the right snapshot.

```bash
clipmem recall "<query>" --hours 72 --format json
clipmem timeline --hours 72 --format json --limit 25
clipmem search "<query>" --mode literal --format json
```

---

## Watcher not running

Symptom: `clipmem timeline --hours 1` returns zero rows despite the user having copied recently.

```bash
clipmem service status --json
```

If `stale: true` or neither the Homebrew service nor the direct LaunchAgent is running:

```bash
clipmem setup
# or, for Homebrew-native management:
brew services start clipmem
```

---

## FTS mode failures

`clipmem search "..." --mode fts` errors with `fts5: syntax error` or similar:

- Punctuation in the query confuses FTS5. Switch to `--mode literal`.
- Check `clipmem doctor --json` for `"fts5_create_virtual_table_ok": true`. If false, the SQLite build lacks usable FTS5 — every `--mode fts` call will fail.
- Mix of quotes and operators (`"foo" AND bar`) should parse in FTS5. Unbalanced quotes do not.

---

## Binary-only snapshots (images, PDFs, opaque blobs)

Symptom: `best_text` is `null` or empty, yet `total_bytes > 0` and `kind` is `image`, `pdf`, or `binary`.

This is expected — those clipboards have no safe text projection. To recover the content:

1. Call `clipmem get <snapshot_id> --format json`.
2. Inspect `items[].representations[]` for a useful `uti` (e.g. `public.png`, `com.adobe.pdf`).
3. Call `clipmem export <snapshot_id> --item <index> --uti <uti> --out <path>`.

When no usable `best_text` exists, report the metadata honestly:

> "I found the clipboard item (snapshot 901, PNG from CleanShot X at 10:12 today). It has no stored text — I'd need to export the raw image to recover the content."

Do **not** invent exact text that was never captured as text.

---

## OpenClaw sandbox / PATH issues

Symptom: OpenClaw cannot execute `clipmem` even though it runs fine in the user's shell.

```bash
clipmem agents openclaw doctor
```

Interpret the output:

- `[OK] clipmem on PATH` — binary visible to OpenClaw.
- `[FAIL] clipmem on PATH` — the binary exists on the user's shell PATH but not the sandbox's. Add the install directory (usually `~/.local/bin` or `/opt/homebrew/bin`) to the sandbox PATH.
- `[OK] workspace resolved` — `CLIPMEM_OPENCLAW_WORKSPACE` or `openclaw config get agents.defaults.workspace` is set.
- `[FAIL] skill files present` — the skill was never installed. Run `clipmem agents openclaw install-skill`.

Also useful:

```bash
openclaw sandbox explain   # when available; prints visible PATH and file-access scope
```

If the binary was installed **after** the sandbox was created, recreate the sandbox image and retry.

---

## Locked or corrupt database

Symptom: `clipmem doctor --json` includes errors, or retrieval commands exit with code `5`.

```bash
clipmem doctor --json
```

- `database is locked` — another writer is holding the lock. Usually the watcher under heavy load; try again in a few seconds.
- `incompatible prerelease schema` — an older archive format is being mistaken for the current DB. Move the file aside, then run `clipmem setup`.
- `malformed` or `corrupt` — SQLite detected structural damage. Back up `~/Library/Application Support/clipmem/clipmem.sqlite3`, then delete and let `clipmem capture-once` rebuild. You will lose history.
- `permission denied` — the database file is not writable by the current user. Check `0600` on the file and `0700` on the containing directory (`~/Library/Application Support/clipmem/`).

---

## Exit code reference

| Code | Meaning | Typical response |
|---|---|---|
| `0` | success | continue |
| `1` | uncategorized runtime failure | inspect stderr; try again |
| `2` | invalid args | agent bug — check flags and re-invoke |
| `3` | not found | snapshot id, representation, or query returned no hits |
| `4` | unsupported format | wrong `--format` for this subcommand (e.g. `toon` on `get`) |
| `5` | database error | see "Locked or corrupt database" above |
| `6` | platform error | macOS API / filesystem issue; user action likely needed |

---

## When to give up gracefully

If after all of the above the archive genuinely has no match:

- Say so plainly. Don't hallucinate.
- Quote the nearest metadata hits: `app_name`, `observed_at`, `kind`.
- Suggest the user copy the item again and retry — `clipmem` captures in real time.
