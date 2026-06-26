---
name: term
description: Fast, explicit terminal execution via OpenClaw exec (direct dispatch; you type the exact command).
user-invocable: true
disable-model-invocation: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata: { "openclaw": { "emoji": "🧰", "os": ["darwin","linux","win32"] } }
---

# /term — direct terminal execution (exec dispatch)

`/term` is a **power-user shortcut**: whatever you type after `/term` is forwarded **as-is** to OpenClaw’s `exec` tool.

This is intentionally *“manual mode”*:
- You (the user) provide the exact shell command.
- OpenClaw does not rewrite, expand, or “helpfully” change it.
- It’s useful when you want quick, deterministic terminal actions without a planning loop.

## How dispatch works (important)

OpenClaw supports `command-dispatch: tool` skills. When you run:

- `/term ls -la`

the raw argument string (`ls -la`) is forwarded to the configured tool (`exec`) without extra parsing. In tool-dispatch mode, OpenClaw invokes the tool with params shaped like:

`{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`

See the Skills docs section on `command-dispatch`, `command-tool`, and `command-arg-mode`. :contentReference[oaicite:10]{index=10}

## When to use /term vs normal “agent runs”

Use `/term` when:
- You already know the exact command you want.
- You want a quick read-only check (files, git status, grep).
- You are debugging OpenClaw itself (skills folder, logs, Peekaboo bridge status).

Prefer normal agent flow when:
- You want the model to decide the best approach.
- The task may need multiple steps, safety checks, or file edits.

## Safety model (read this once, then follow it)

`/term` is equivalent to letting an assistant type into your terminal.
Good defaults:

1) Prefer read-only commands unless you *mean* to change state.
2) Avoid secrets in command lines (tokens, API keys, cookies).
3) Avoid remote execution one-liners:
   - no `curl ... | sh`
   - no “download and execute” pipelines
4) If the command could delete or overwrite files, slow down and double-check paths.

## Host + sandbox notes

Your actual execution environment depends on how you invoke `exec` in your setup (sandbox vs host).
Also note: when a session is sandboxed, environment variables are not automatically inherited by the container; you must inject them via sandbox env settings or bake them into the image. :contentReference[oaicite:11]{index=11}

## Practical examples

### Quick inspection (safe, read-only)

- `/term pwd`
- `/term ls -la`
- `/term git status`
- `/term rg -n "TODO|FIXME" .`

### Debug Peekaboo bridge discovery (macOS)

- `/term peekaboo bridge status --verbose`

If the output shows “no such file or directory” for all candidates and “Selected: local (in-process)”, you likely have no bridge host running (see troubleshooting below).

### One-liners for structured output

If you want JSON output for parsing:
- `/term python -c 'import json,platform; print(json.dumps({"py":platform.python_version()}))'`

## Troubleshooting

### “command not found”
The tool runs in whatever PATH your OpenClaw runtime provides. If you rely on Homebrew, ensure the runtime sees `/opt/homebrew/bin`.

### “permission denied” / macOS privacy prompts
Some tools (screen capture / UI automation) require Screen Recording / Accessibility. Those permissions are per-process context on macOS; using PeekabooBridge is often the reliable path for automation.

### I need richer guidance and guardrails
Install/use the companion skill `terminal-helper` (model-invocable) which teaches safe patterns, confirmations, and runbooks.
