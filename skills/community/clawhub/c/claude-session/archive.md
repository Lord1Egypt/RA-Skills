# Archive

Move a completed session out of an active project key to a long-term archive location under `~/.claude/projects/.bak/`, preserving the session's `.jsonl` and any associated metadata (custom-title, agent-name records that live inside the file itself).

**Convention parity**: archived sessions live in the **same `projects/.bak/` directory** as transient backups (clean-profanity / ralph-prompt-collapse output), but use the **flat naming** `<project-key>_<uuid>.jsonl` (vs. the timestamped `<uuid>.<timestamp>.jsonl` for transient backups). This keeps a single backup root and avoids splitting session storage across `.archive/` and `projects/.bak/`.

## When to Use

- Session work is finished, but the transcript should be kept (not purged)
- The active project listing is getting noisy (too many old completed sessions)
- A specific session needs to be quoted/referenced later but not auto-loaded by Claude Code

## When NOT to Use

| Situation | Use instead |
|-----------|-------------|
| Session is dead (no assistant response, < 10 lines) | `purge` — permanent deletion is appropriate |
| Active session, just want a custom title | `rename` — keeps it loadable |
| Moving between active projects (not archiving) | `move` |
| Generic file archive (not a session `.jsonl`) | general-purpose `/archive` skill (`.bak/` move) |

## Destination

`~/.claude/projects/.bak/<project-key>_<uuid>.jsonl`

- Under `.bak` (dotfile), so not picked up by Claude Code's session loader, but still readable via `Read` / `jq`
- Filename embeds the original project key as a prefix (e.g., `-Users-david-ghq-github-com-es6kr_a1b2c3d4-....jsonl`) so the source context is retrievable from filename alone — no subdirectory
- UUID portion preserved unchanged — URL references and chain links remain valid

## Procedure

### 1. Identify source

```bash
SESSION_ID="<uuid>"
SRC=$(find ~/.claude/projects -name "${SESSION_ID}.jsonl" -type f 2>/dev/null | head -1)
test -n "$SRC" || { echo "Session not found: $SESSION_ID"; exit 1; }
PROJECT_KEY=$(basename "$(dirname "$SRC")")
echo "Source: $SRC"
echo "Project: $PROJECT_KEY"
```

### 2. Verify session is archive-worthy

| Check | Command | Pass condition |
|-------|---------|----------------|
| File size > 0 | `[ -s "$SRC" ]` | Non-empty |
| Has assistant response | `jq -r 'select(.type=="assistant")' "$SRC" \| head -1` | Output non-empty |
| Not the current session | Compare `SESSION_ID` to `~/.claude/hooks/session-id-inject.sh` output | Must differ |

If the session is the **currently active** session (Claude Code has it open), the harness may rewrite the file at any moment. Defer archive until the user ends that session.

### 2.5. RAG dispatch — auto-supply when a receiver is available (abstract contract)

Archive moves the JSONL out of the active project, so post-archive recall depends on whatever external index the caller wants populated (semantic index, full-text store, summary cache, etc.). This skill stays **vendor-agnostic** — it only declares the dispatch surface; implementations live in vendor skills.

#### Auto-supply is the default (HARD STOP)

`--rag` is **not** an opt-in extra. When a RAG receiver is available in the environment, the caller **must auto-supply** `--rag=<skill>:<topic>`. File-move-only is correct **only** when no receiver is available **or** the user passed `--no-rag`. This mirrors the always-on caller-side dispatch rule (`skill-usage.md` caller-side "auto-supply available vendor dispatch" rule); archive executes it as a **procedure step**, not as caller discretion.

Run the 3-axis receiver scan **before reporting the archive result**:

1. **MCP server** — is a vector-store tool registered (`mcp__<vendor>__*-store` / `*-find`)? → candidate vendor skill
2. **Skill registry** — does a skill expose a RAG-store topic (e.g. `es6kr:qdrant-import`)? (MCP absent does not mean receiver absent)
3. **Reachability** — does the receiver endpoint answer (`curl -m 8 <endpoint>/healthz`)?

Branch:
- 0 receivers → file move only
- 1 receiver reachable → **auto-supply `--rag=<skill>:<topic>`** (do not ask, do not present it as optional)
- 2+ → AskUserQuestion to pick
- Uncertain → ask; do not silently skip

| # | Don't | Do |
|---|-------|-----|
| 1 | Finish with file-move-only + "run with `--rag` if you want" while a receiver is available | Auto-supply `--rag` as the default. Offering it as optional = regression |
| 2 | Read the "abstract contract" framing and treat dispatch as skippable | "optional" describes the flag's omittability at the contract layer, not the caller's choice. With a receiver present, supply is mandatory |
| 3 | Skip the 3-axis scan because the archive script has no `--rag` flag | Script lacking the flag → do the dispatch manually after the move (see the qdrant-import receiver). The scan + dispatch is still mandatory |

#### Flag

```text
/session archive <session-id> --rag=<skill>:<topic>
```

- `<skill>` — name of a registered skill that owns a RAG-store topic
- `<topic>` — topic within that skill responsible for accepting archived content
- When the flag is omitted, archive performs file move only — but **callers are expected to auto-supply the flag** when a receiver is available in the environment (see `skill-usage.md` caller-side dispatch rule)

#### Contract for receivers (vendor skills implement this)

Caller (this skill) passes payload via environment variables; receiver skill chooses inline or file mode by which env vars are set:

| Mode | Env vars set by caller | Use |
|------|------------------------|-----|
| inline | `ARCHIVE_RAG_FILE` (absolute path), `ARCHIVE_RAG_METADATA_JSON` (serialized metadata) | Small payload; metadata fits a single env string |
| file   | `ARCHIVE_RAG_INPUT_JSON` (path to JSON `{file_path, metadata}`) | Large payload or when caller needs to clean up |

Receivers consult vendor-side documentation for their accepted metadata keys, chunking strategy, and idempotency rules. This skill does **not** define those — see the targeted skill's docs.

#### Skip conditions

- Session is dead (< 10 lines, no assistant response) — use `purge`, no archival value
- User explicitly omits `--rag` — file move only
- Caller-specified `<skill>:<topic>` not available in this environment — abort with a clear error; do not silently skip the move

**Why abstract**: archived sessions stay readable via `Read`, but discoverability collapses (outside Claude Code's session list, no `/session search` reach). External indexing is the only content-level recall path. Naming a specific index vendor here would couple this generic skill to one environment's stack; the flag keeps the coupling at the call site.

### 3. Pre-flight preview

```bash
DST_DIR="$HOME/.claude/projects/.bak"
DST="$DST_DIR/${PROJECT_KEY}_${SESSION_ID}.jsonl"

echo "Will move:"
echo "  FROM: $SRC ($(wc -c < "$SRC") bytes)"
echo "  TO:   $DST"
[ -e "$DST" ] && echo "WARN: destination already exists — abort"
```

Always show the preview before invoking the destructive move.

### 4. Execute archive

Use the script:

```bash
bash ~/.claude/skills/claude-session/scripts/archive-session.sh <session_id>
```

Or inline (single session):

```bash
mkdir -p "$DST_DIR"
mv "$SRC" "$DST"
```

### 5. Verify

```bash
[ -f "$DST" ] && [ ! -f "$SRC" ] && echo "OK: archived" || echo "FAIL"
ls -la "$DST"
```

### 6. Optional — record archive ledger

Append an entry to `~/.claude/projects/.bak/INDEX.md` so you can grep what was archived when:

```bash
LEDGER="$HOME/.claude/projects/.bak/INDEX.md"
mkdir -p "$(dirname "$LEDGER")"
echo "- $(date +%Y-%m-%d) ${PROJECT_KEY}_${SESSION_ID} — $(jq -r 'select(.type=="custom-title") | .customTitle' "$DST" 2>/dev/null | head -1)" >> "$LEDGER"
```

## Restoration

To bring an archived session back as an active project entry:

```bash
SESSION_ID="<uuid>"
PROJECT_KEY="<project>"
SRC="$HOME/.claude/projects/.bak/${PROJECT_KEY}_${SESSION_ID}.jsonl"
DST="$HOME/.claude/projects/$PROJECT_KEY/${SESSION_ID}.jsonl"
mkdir -p "$(dirname "$DST")"
mv "$SRC" "$DST"
```

After restore, Claude Code's session list will pick it up on next refresh.

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Use `rm` after `cp` ("safe-copy-first") | `mv` — atomic, mv failure preserves source |
| 2 | Rename the file (UUID prefix, date suffix, etc.) | Keep `<uuid>.jsonl` — chain links + `/session url` rely on the UUID |
| 3 | Use a project subdirectory (e.g., `<project-key>/<uuid>.jsonl`) — splits storage across `.archive/` and `.bak/` | Use flat naming `<project-key>_<uuid>.jsonl` under `.bak/` — single backup root; source context is recoverable from the filename prefix |
| 4 | Archive the **currently active** session | Wait until the session is closed; harness can rewrite an open file |
| 5 | Archive multiple sessions in a `find ... -exec` loop without preview | Single-session at a time; archive script reports each result |
| 6 | Hardcode a specific RAG vendor (URL, skill name, MCP tool name) in this generic skill | Use `--rag=<skill>:<topic>` flag at the call site; vendor skill implements the receiver protocol |

## Self-check (before invoking)

1. Is the session file actually present in `~/.claude/projects/`?
2. Is the session **not** the current session (`/session id` differs)?
3. Has the destination path been previewed and confirmed not to already exist?
4. Did you preserve the UUID filename (no rename)?
5. Is the destination under `~/.claude/projects/.bak/` using the flat `<project-key>_<uuid>.jsonl` naming?
6. Is a RAG receiver available in this environment (3-axis scan: MCP store tool / skill RAG-store topic / endpoint reachable)? If yes, did you **auto-supply** `--rag=<skill>:<topic>`? File-move-only is correct only with no receiver or an explicit `--no-rag`. (This skill does not pick a default vendor, but auto-supply is mandatory when a receiver exists — see §2.5 "Auto-supply is the default".)
