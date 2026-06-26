---
name: codex-mcp-dev
description: Use the local Codex CLI through mcporter and codex-mcp-server for real coding work in the current project. Use when the user asks to build features, fix bugs, refactor code, debug failures, write or update tests, review implementation options, or otherwise delegate non-trivial development work to the machine-local Codex installation.
---

# Codex MCP Dev

Use the local Codex installation through the wrapper script at `{baseDir}/scripts/codex_mcp.py`.
This gives a stable path:

OpenClaw → mcporter → codex-mcp-server → local `codex`

## Quick Setup

Install prerequisites first:

- `mcporter`
- local `codex`
- `codex-mcp`

Create the project MCP entry if `config/mcporter.json` does not exist yet:

```bash
mcporter config add codex-cli --scope project --command codex-mcp
```

This skill expects a workspace-local MCP server named `codex-cli`.

## Workflow

1. Use this skill for non-trivial coding tasks.
2. If it is the first use in a session or something looks broken, run:
   - `python3 {baseDir}/scripts/codex_mcp.py doctor`
3. Choose a mode:
   - **Analysis / planning / explanation:** use `ask` without `--full-auto`
   - **Implementation / refactor / test-writing:** use `ask --full-auto`
4. Always set `--cwd` to the target repo or project directory.
5. Give Codex a concrete prompt with files, constraints, and acceptance criteria.
6. After Codex responds, inspect files and run local tests yourself when feasible instead of trusting the tool output blindly.
7. Summarize changes, tests run, and any remaining risks.

## Good Uses

- Implementing features across multiple files
- Fixing bugs with real repo context
- Refactoring with constraints
- Writing or updating tests
- Debugging failing commands or stack traces
- Asking local Codex for a second implementation pass or review

## Command Patterns

### Health check

```bash
python3 {baseDir}/scripts/codex_mcp.py doctor
```

### Version info

```bash
python3 {baseDir}/scripts/codex_mcp.py version
```

### Normal implementation

```bash
python3 {baseDir}/scripts/codex_mcp.py ask \
  --cwd /absolute/path/to/repo \
  --full-auto \
  --prompt "Implement the requested change, update tests, and summarize what changed."
```

### Read-only analysis

```bash
python3 {baseDir}/scripts/codex_mcp.py ask \
  --cwd /absolute/path/to/repo \
  --sandbox-mode read-only \
  --approval-policy never \
  --prompt "Explain the bug, identify likely root cause, and propose the smallest safe fix."
```

### Long prompt from file

```bash
python3 {baseDir}/scripts/codex_mcp.py ask \
  --cwd /absolute/path/to/repo \
  --full-auto \
  --prompt-file /tmp/codex-task.txt
```

## Prompting Rules

Include as many of these as possible:

- Target files or directories
- Desired behavior
- Exact error messages or failing tests
- Constraints on scope
- Required test updates
- Expected output format

Prefer prompts like:

- "Fix the failing test in `tests/api.test.ts` without changing public behavior. Run the relevant tests and summarize the root cause."
- "Refactor `src/cache.py` for readability, keep behavior identical, and add regression tests for TTL edge cases."
- "Review the auth flow in `server/` and identify the top 3 correctness risks with concrete file references."

## Guardrails

- Prefer `--full-auto` for ordinary implementation work.
- Do **not** use `--yolo` unless the user explicitly wants aggressive execution.
- Use repo-specific `--cwd`; do not run against the wrong directory.
- Validate with local reads/tests when possible.
- If the task is tiny or surgical, skip this skill and edit directly.
