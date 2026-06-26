# Session ID

Finds the session ID (UUID) of the current conversation.

## How It Works

Claude's text output is recorded in session JSONL files. By leaving a unique marker in the conversation, you can grep for that marker to identify the current session file.

## Procedure

### 0. Check Context First (Preferred — no marker needed)

Before using the marker method, check if the session ID is already visible in the current context.

**Search order:**

1. **`session-id-inject.sh` hook output** — If installed and registered (`SessionStart` and/or `UserPromptSubmit` matcher in `~/.claude/settings.json`), look for "Current session ID: {uuid}" in conversation system-reminders. The `UserPromptSubmit` variant auto-fires on slash commands (`/session id`, `/cleanup`, or any namespace import command) AND on **keyword-triggered fallback** (prompt body contains `qdrant`, `rag`, or `session` as a bare word).
2. **`CLAUDE_CODE_SESSION_ID` env var** — Run `echo "$CLAUDE_CODE_SESSION_ID"` in a Bash tool call. Claude Code sets this on shell startup. Caveat: env may be set once per Bash subprocess; if the value contradicts other sources, prefer #1 (hook) or #4 (marker).
3. **File path UUIDs** in recent Bash/Read tool results (UUID pattern `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`):

| Source | Path pattern | Example |
|--------|-------------|---------|
| Subagent | `/Users/.../{session_id}/subagents/...` | `...3b86ae4e-4aaf-4f03.../subagents/...` |
| Task output | `/private/tmp/.../tasks/{session_id}/...` | `...tasks/3b86ae4e-4aaf-4f03.../bkvaevkqo.output` |
| Tool result | `.../{session_id}/tool-results/...` | — |
| Background task | `.../{session_id}/tasks/...` | output file paths from `run_in_background` |

**Procedure:**
1. Check for hook injection ("Current session ID: ..." in context) — if present, return directly
2. If absent, Bash `echo "$CLAUDE_CODE_SESSION_ID"` — if non-empty, return that
3. Otherwise, scan file paths in recent tool results for the UUID pattern
4. If found, return it — **skip the marker method (outer Steps 1-3) entirely**
5. If not found, **AskUserQuestion**: "session-id hook is not installed. Install it?"
   - "Install" → run `/session install`, then inform "auto-injected from next session". Current session falls through to the marker method (outer Step 1)
   - "Skip" → proceed to the marker method (outer Step 1)

### Forbidden heuristics (HARD STOP)

| # | Don't | Do |
|---|-------|-----|
| 1 | `ls -lt ~/.claude/projects/<key>/*.jsonl \| head -1` mtime "most recent = current session" | Use hook output → env var → file-path UUID → marker (the 4 ordered sources above) |
| 2 | "Most recently modified JSONL is the active session" assumption | After `/compact` and `/session split`, multiple JSONLs in the same project key can be modified within seconds of each other. mtime races are common — mtime can show a non-active JSONL as newer than the active one. Always confirm against the hook output or env var |
| 3 | Single-source conclusion (env var alone, or hook alone) when sources disagree | Cross-verify at least 2 sources. If hook says A and env says B, run a marker probe (outer Step 1-2) to break the tie |

### 1. Generate and Output Marker (only if Step 0 found nothing)

**Method A (recommended):** Generate a unique marker string directly in text output.

```
SESSION_MARKER_{random_uuid}
```

Example output:
```
Marker for finding session ID: SESSION_MARKER_a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Method B:** Let the script generate the marker automatically.

```bash
MARKER=$(bash scripts/find-session-id.sh)
echo "$MARKER"
```

When called without arguments, the script generates a unique marker (`SESSION_MARKER_{timestamp}_{pid}`) and prints it. The `echo` ensures the marker appears in text output and gets recorded in the JSONL.

### 2. Search with Marker

```bash
# Method A: pass the marker you generated
bash scripts/find-session-id.sh "SESSION_MARKER_a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# Method B: pass the script-generated marker
bash scripts/find-session-id.sh "$MARKER"
```

The script converts the CWD to a project name, then searches `~/.claude/projects/{project_name}/*.jsonl` for the marker and returns the session ID.

**Parent directory fallback**: If CWD-based project directory doesn't exist (e.g., CWD is a monorepo sub-package like `packages/vscode-extension`), the script walks up parent directories until a matching project is found.

### 3. Result

```
b5153827-a52c-4e83-b24a-8413e6aa418b
```

## Script

[find-session-id.sh](./scripts/find-session-id.sh)

- Input: `<marker>` (required), `[project_dir]` (optional, auto-derived from CWD if omitted)
- CWD → project name conversion rules:
  - Git-bash: `/c/Users/...` → `c--Users-...`
  - WSL: `/mnt/c/Users/...` → `-mnt-c-Users-...`
  - macOS: `/Users/...` → `-Users-...`
- sync-conflict files are automatically excluded

## Keyword Session Search

> Moved to [search.md](./search.md). `/session id <keyword>` is still accepted as a backward-compatible alias and routes to `/session search`.

## Usage Examples

```bash
/session id                          # look up current session ID
```

