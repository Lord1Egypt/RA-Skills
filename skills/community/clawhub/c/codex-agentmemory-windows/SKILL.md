---
name: codex-agentmemory-windows
description: Configure, repair, and validate agentmemory integration for Codex App on Windows. Use when Codex needs to set up agentmemory hooks, fix Windows PowerShell hook failures, create an agentmemory-hook.cmd wrapper, update ~/.codex/hooks.json and trusted_hash entries, fix missing Codex additionalContext memory injection, repair stale/frozen agentmemory knowledge graph updates, backfill graph nodes/edges, or troubleshoot Codex App agentmemory MCP/hook configuration.
---

# Codex Agentmemory Windows

## Goal

Set up agentmemory for Codex App on Windows with PowerShell-safe hook commands, Codex-native memory injection, stable data paths, working Stop finalizers, healthy knowledge graph updates, and repeatable validation. Prefer the bundled scripts for deterministic repair.

## Quick Repair

Run the helper when the user wants an automatic fix:

```powershell
python scripts/configure_agentmemory_windows.py --codex-home "$env:USERPROFILE\.codex"
```

Use these options when needed:

```powershell
python scripts/configure_agentmemory_windows.py --secret "<agentmemory-secret>"
python scripts/configure_agentmemory_windows.py --url "http://localhost:3111" --secret "<agentmemory-secret>"
python scripts/configure_agentmemory_windows.py --preserve-other-hooks
python scripts/configure_agentmemory_windows.py --absolute-data-dir "$env:USERPROFILE\data"
python scripts/configure_agentmemory_windows.py --patch-codex-scratch-context
python scripts/configure_agentmemory_windows.py --skip-injection-patch
python scripts/configure_agentmemory_windows.py --dry-run
```

The script backs up changed files, creates `agentmemory-hook.cmd`, writes Windows-safe hook commands, updates Codex hook trust hashes, configures the agentmemory MCP section, patches hook scripts to emit Codex `additionalContext` JSON, filters Codex Desktop background suggestion sessions, optionally pins agentmemory's data store to an absolute path, and validates the hook commands.

After repair, rerun with `--dry-run`; it should print only environment/path information and no `would update:` lines. If `hooks.json` was edited manually, treat any trusted-hash drift as a configuration repair, not a one-line hash tweak: rerun the helper so `hooks.json`, `config.toml`, wrapper paths, and patched hook scripts stay aligned.

## Knowledge Graph Repair

Use this when the viewer graph is tiny, stale, or frozen even though observations/summaries keep growing.

First inspect without changing files:

```powershell
python scripts/repair_agentmemory_graph_windows.py --dry-run
```

Then apply the full repair:

```powershell
python scripts/repair_agentmemory_graph_windows.py --all --restart-service
```

The graph repair script:

- patches every discovered `stop.mjs` so Codex Stop finalizes the session, checks server-side `GRAPH_EXTRACTION_ENABLED`, and posts `graph/extract` in small batches;
- patches installed `dist\index.mjs` so `graph-extract` remaps edges from temporary extracted node IDs to persisted node IDs after node deduplication;
- backs up `mem%3Agraph%3Anodes.bin` and `mem%3Agraph%3Aedges.bin` before writing backfill data;
- backfills a deterministic graph from existing compressed observations using file/concept/title metadata instead of expensive full LLM extraction;
- validates via `/agentmemory/graph/stats` after import.

Default backfill settings are intentionally conservative: `--min-importance 5 --max-files 2 --max-concepts 3`. Raise or lower them only when the user explicitly wants a denser or smaller graph.

## Manual Workflow

1. Inspect `%USERPROFILE%\.codex\hooks.json`, `%USERPROFILE%\.codex\config.toml`, and `%USERPROFILE%\.codex\agentmemory-hook.cmd`.
2. Locate the installed agentmemory plugin root, usually `%USERPROFILE%\.codex\plugins\cache\agentmemory\agentmemory\<version>`.
3. Locate `node.exe`; prefer an absolute path from `Get-Command node.exe`, `C:\Program Files\nodejs\node.exe`, or Codex bundled `node.exe`.
4. Read `AGENTMEMORY_SECRET` and `AGENTMEMORY_URL` from existing config or environment. Do not hardcode another user's secret.
5. Create a wrapper at `%USERPROFILE%\.codex\agentmemory-hook.cmd`:

```cmd
@echo off
set "AGENTMEMORY_URL=http://localhost:3111"
set "AGENTMEMORY_SECRET=<secret>"
set "AGENTMEMORY_INJECT_CONTEXT=true"
if "%~1"=="" exit /b 2
"C:\Path\To\node.exe" "C:\Path\To\agentmemory\scripts\%~1"
exit /b %ERRORLEVEL%
```

6. Write hook commands through `cmd.exe`, not direct quoted PowerShell invocation:

```text
cmd.exe /d /s /c ""C:\Users\<user>\.codex\agentmemory-hook.cmd" session-start.mjs"
```

7. Use this event-to-script map:

| Codex hook event | Script |
| --- | --- |
| `PreToolUse` | `pre-tool-use.mjs` |
| `PostToolUse` | `post-tool-use.mjs` |
| `SessionStart` | `session-start.mjs` |
| `UserPromptSubmit` | `prompt-submit.mjs` |
| `Stop` | `stop.mjs` |
| `PreCompact` | `pre-compact.mjs` |

8. Update `config.toml` `[hooks.state.'...\hooks.json:<event_key>:0:0']` entries with `enabled = true` and `trusted_hash = "sha256:<sha256 of exact command string>"`.
9. Disable duplicated plugin-provided hooks under `agentmemory@agentmemory:hooks/hooks.codex.json` if the global `hooks.json` wrapper is used.
10. Patch `session-start.mjs`, `prompt-submit.mjs`, and `pre-tool-use.mjs` so any injected memory is returned as Codex hook JSON:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<agentmemory-context>...</agentmemory-context>"
  },
  "suppressOutput": true
}
```

Use `hookEventName: "UserPromptSubmit"` for `prompt-submit.mjs` and `hookEventName: "PreToolUse"` for `pre-tool-use.mjs`. Raw `<agentmemory-context>` text on stdout is not enough for reliable Codex App injection.
11. If starting agentmemory from different working directories can create multiple `./data` stores, edit each installed `dist\iii-config.yaml` so `state_store.db` and `stream_store` use absolute paths such as `%USERPROFILE%\data\state_store.db` and `%USERPROFILE%\data\stream_store`.
12. For graph updates, patch `stop.mjs` to query `/agentmemory/config/flags` instead of trusting Codex process env vars, then call `/agentmemory/graph/extract` in batches after `/agentmemory/session/end`.
13. Patch service-side `graph-extract` if needed so merged nodes update edge source/target IDs before edge persistence.
14. Validate by piping sample hook JSON into every command through PowerShell and requiring exit code `0`.

## Missing Injection Checklist

Use this when capture and summaries work but new conversations do not receive memory:

1. Confirm `agentmemory status` shows nonzero observations or memories and `AGENTMEMORY_INJECT_CONTEXT` is enabled.
2. Call the context endpoint or `session-start.mjs` manually. If it returns a non-empty `<agentmemory-context>`, agentmemory has data and the remaining issue is Codex hook delivery.
3. Inspect the newest `%USERPROFILE%\.codex\sessions\YYYY\MM\DD\*.jsonl`. A successful injection appears as a `developer` message containing `<agentmemory-context ...>`.
4. If manual hook output is raw XML/text but the JSONL has no developer context message, patch the hook scripts to use `hookSpecificOutput.additionalContext`.
5. If a new Codex scratch folder like `%USERPROFILE%\Documents\Codex\YYYY-MM-DD\hi-3` gets empty context while `hi-2` has memory, patch the agentmemory service bundle so `mem::context` matches the daily Codex scratch root instead of exact `session.project === data.project`.
6. If `agentmemory status` suddenly shows `0` observations or memories after restart, check for accidental data stores under the current workspace or package directory and pin `iii-config.yaml` to an absolute data directory.

## Duplicate Session Checklist

Use this when Codex App shows one visible conversation but agentmemory shows many sessions with the same title:

1. Inspect recent sessions. If repeated `firstPrompt` starts with `# Overview Generate 0 to 3 hyperpersonalized suggestions...`, these are Codex Desktop background recommendation jobs, not duplicate user chats.
2. Treat this as capture noise: the hook is recording every Codex session-like run, including hidden background jobs.
3. Patch `prompt-submit.mjs` to detect that exact prompt prefix, record the session id in a temp ignore file, call `/agentmemory/forget` for the pre-created background session, and return without observing.
4. Patch `pre-tool-use.mjs`, `post-tool-use.mjs`, `stop.mjs`, and `pre-compact.mjs` to skip any session id in that temp ignore file.
5. Add a service-side fallback in installed `@agentmemory/agentmemory/dist/src-*.mjs` and `dist/index.mjs`: `mem::observe` should ignore this prompt pattern and delete the pre-created session; `/agentmemory/session/start` should also ignore the pattern if it arrives as a title.
6. Restart agentmemory after service-bundle changes.
7. Do not delete old repeated sessions automatically. Ask the user first, then use `/agentmemory/forget` for sessions whose prompt clearly matches the background suggestion pattern.

## Codex Scratch Project Matching

agentmemory v0.9.x may match session context by exact project path. Codex App often creates per-chat scratch folders under:

```text
%USERPROFILE%\Documents\Codex\YYYY-MM-DD\<chat-folder>
```

For shared daily scratch context, patch `mem::context` in the installed agentmemory service bundle (`dist\src-*.mjs` and `dist\index.mjs`) to:

- normalize Windows paths case-insensitively and slash-insensitively;
- treat the same `%USERPROFILE%\Documents\Codex\YYYY-MM-DD` parent as one context root;
- include semantic memories only when their fact text contains the current project leaf hint, to avoid injecting unrelated project facts.

The helper applies this with `--patch-codex-scratch-context` when the installed bundle still has the original exact-project matcher.

## Why This Fixes Windows Hook Errors

PowerShell treats `"C:\path\agentmemory-hook.cmd"` as a string. If arguments follow it directly, PowerShell can fail with `Unexpected token 'session-start.mjs'`. The stable Windows form is either:

```powershell
& "C:\path\agentmemory-hook.cmd" session-start.mjs
```

or, more robust for Codex hook runners:

```text
cmd.exe /d /s /c ""C:\path\agentmemory-hook.cmd" session-start.mjs"
```

Use the `cmd.exe` form in `hooks.json`.

## Validation Commands

Use this after manual edits:

```powershell
$payload = '{"session_id":"test","cwd":"C:\\Temp","prompt":"test"}'
$hooks = Get-Content "$env:USERPROFILE\.codex\hooks.json" -Raw | ConvertFrom-Json
foreach ($event in $hooks.hooks.PSObject.Properties.Name) {
  $cmd = $hooks.hooks.$event[0].hooks[0].command
  $payload | powershell.exe -NoProfile -Command $cmd
  Write-Host "$event exit=$LASTEXITCODE"
}
```

All events should return `exit=0`.

For injection-specific verification, parse hook stdout as JSON and check:

```powershell
$payload = '{"session_id":"test","cwd":"C:\\Temp","hook_event_name":"SessionStart"}'
$out = $payload | & "$env:USERPROFILE\.codex\agentmemory-hook.cmd" session-start.mjs
$json = $out | ConvertFrom-Json
$json.hookSpecificOutput.additionalContext
```

If this contains `<agentmemory-context`, open a fresh Codex conversation and confirm the newest session JSONL has a `developer` message containing the same tag.

For graph-specific verification:

```powershell
Invoke-WebRequest -Uri "http://localhost:3111/agentmemory/graph/stats" -UseBasicParsing |
  Select-Object -ExpandProperty Content
```

If `totalNodes` and `totalEdges` stay unchanged across multiple content-rich sessions, run:

```powershell
python scripts/repair_agentmemory_graph_windows.py --dry-run
```

Then apply with `--all --restart-service` only after checking the dry-run delta.

## Common Non-Blocking Warnings

Do not confuse these with hook command failures:

- `Shell snapshot not supported yet for PowerShell`: Codex shell snapshot limitation, not an agentmemory hook failure.
- `chatgpt authentication required for remote plugin catalog`: remote plugin sync warning, not local hook execution.
- `GitHub API rate limit exceeded`: curated plugin sync warning, not agentmemory hook execution.
- `resources/list` or `resources/templates/list` unknown for agentmemory MCP: MCP capability warning, not hook capture failure.

## Upgrade Warning

Upgrading or reinstalling `@agentmemory/agentmemory` can overwrite patched `stop.mjs` and `dist\index.mjs`. After an upgrade, rerun:

```powershell
python scripts/repair_agentmemory_graph_windows.py --dry-run --patch-hooks --patch-service
```

If it reports pending patches, run the same command without `--dry-run` and restart agentmemory.
