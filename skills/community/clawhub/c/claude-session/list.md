# List Sessions

List all sessions in the current project (or all projects) with UUID, modification time, and size.

## When to Use

- `/session list` — list all sessions in current project (default)
- `/session list --all-projects` — list across all projects under `~/.claude/projects/`
- `/session list --limit 20` — show only the top N most recently modified sessions

Use for quick inspection before running `classify`, `purge`, `search`, or `compress`. Unlike those topics, `list` performs **no validation, classification, or destructive action** — it only enumerates.

## Comparison with Adjacent Topics

| Topic | Scope | Difference |
|-------|-------|------------|
| `list` | All sessions in project | No filter, no classification — raw enumeration |
| `classify` | Same scope | Adds A/B/C category (A=Delete Recommended, B=Keep, C=Extract then Delete) + recommendation |
| `purge` (dry-run) | Dead sessions only | Filters to `<=10 lines + no assistant response` |
| `rename --list` | Named sessions only | Filters to sessions with custom titles |
| `search` | Keyword match | Filters by keyword presence |

## Procedure

### Default — current project

1. Resolve current project directory from CWD: `~/.claude/projects/$(echo "$CWD" | sed 's|[^a-zA-Z0-9]|-|g')/`
2. Identify current session UUID (preferred: SessionStart hook injection, fallback: most recent `*.jsonl` by mtime)
3. Run:
   ```bash
   PROJ_DIR="$1"
   CURRENT_ID="$2"
   LIMIT="${3:-0}"   # 0 = no limit

   ls -lt "$PROJ_DIR"/*.jsonl 2>/dev/null | \
     awk -v cur="$CURRENT_ID" -v lim="$LIMIT" '
       BEGIN { count = 0 }
       {
         fname = $NF
         gsub(/.*\//, "", fname)
         gsub(/\.jsonl$/, "", fname)
         marker = (fname == cur ? "  ← current" : "")
         printf "| `%s` | %s %s %s | %s | %s |\n", fname, $6, $7, $8, $5, marker
         count++
         if (lim > 0 && count >= lim) exit
       }
     '
   ```
4. Wrap output in a markdown table with header:
   ```markdown
   | Session UUID | mtime | Size (bytes) | |
   |--------------|-------|--------------|--|
   ```
5. Append total count line: `Total: <N> sessions, <total bytes>`

### `--all-projects` flag

Replace step 1 with iteration over `~/.claude/projects/*/`:

```bash
for proj in ~/.claude/projects/*/; do
  proj_name=$(basename "$proj")
  session_count=$(ls "$proj"/*.jsonl 2>/dev/null | wc -l)
  total_bytes=$(du -sb "$proj"/*.jsonl 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
  printf "| %s | %d | %d |\n" "$proj_name" "$session_count" "$total_bytes"
done
```

Output header:
```markdown
| Project | Sessions | Total bytes |
|---------|----------|-------------|
```

Sort by `Sessions` descending.

### `--limit N` flag

Pass `N` to the `LIMIT` variable in the default procedure. Truncates output to the top N most recently modified sessions.

## Output Format

Always full UUID (not prefix). User explicitly requested full UUID for copy-paste into other commands (`/session move <uuid> <target>`, `/session analyze <uuid>`, etc.).

Example output for default mode:

```markdown
| Session UUID | mtime | Size (bytes) | |
|--------------|-------|--------------|--|
| `b16cc48a-4afe-4d2d-8f34-608ea4d06112` | May 23 15:23 | 7958286 | ← current |
| `fe3a5490-ddbc-4a6f-a3d4-831087f4b28a` | May 16 19:59 | 6822792 | |
| `8ef448db-21de-43f8-b2d3-938b7c7ff09e` | May 16 00:14 | 286523 | |

Total: 14 sessions, 23890604 bytes
```

## Current Session Marker

The current session is identified via:

1. **Preferred**: `Current session ID: <uuid>` from `~/.claude/hooks/session-id-inject.sh` (SessionStart hook injection — see `install.md`)
2. **Fallback**: Most recently modified `*.jsonl` in the current project directory

If `session-id-inject` hook is not installed, run `/session install` first to enable the marker. Without it, `list` still works but no `← current` annotation appears.

## Follow-up Suggestions

After running `list`, common next actions:

| Goal | Topic |
|------|-------|
| Categorize sessions for cleanup | `classify` |
| Remove dead sessions | `purge` |
| Find a specific session by keyword | `search` |
| Move session to a worktree project | `move` |
| Compress large sessions | `compress` |
| Inspect or summarize one session | `summarize` |

## Notes

- `list` is non-destructive — no file modification.
- For machine-readable output (JSON), pipe through `jq` after extracting fields. The default output is markdown for human reading.
- Sessions with `.jsonl.bak` or other suffixes are not listed — only `*.jsonl` exactly.
