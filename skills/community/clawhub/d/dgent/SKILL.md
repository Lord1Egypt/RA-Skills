---
name: dgent
description: De-agent your code. Run dgent to check files and commit messages for AI tells before committing — flags naming patterns, catch-rethrow, AI vocabulary, emoji, trailers. Use when finishing work, before commits, or when asked to clean up agent output.
version: 0.1.0
homepage: https://github.com/ItsCodejac/dgent
metadata: { "openclaw": { "requires": { "bins": ["dgent"] }, "install": [{ "kind": "node", "package": "@itscojac/dgent", "bins": ["dgent"], "label": "Install dgent (npm)" }], "emoji": "broom", "homepage": "https://github.com/ItsCodejac/dgent", "os": ["darwin", "linux"] } }
---

# dgent — de-agent your code

Clean AI tells from code and commit messages. Runs as git hooks automatically, or on-demand via CLI.

## When to use

- Before committing code written by an AI agent
- When asked to "clean up" or "de-agent" output
- To check if code has AI naming patterns, catch-rethrow, section headers, or noise comments
- To check if a commit message has AI vocabulary, emoji, or trailers

## Quick check a file

```bash
dgent run --json <file>
```

Returns JSON with `clean`, `fixes[]`, `flags[]`, and `output` (cleaned content). Exit codes: 0 = clean or fixes applied, 1 = flags found.

## Quick check — exit code only

```bash
dgent run --check <file>
```

Silent. Exit 0 if clean or fixes applied, 1 if flags found. Use in pre-commit scripts.

## Scan entire directory

```bash
dgent scan --json [dir]
```

Returns JSON with per-file results. Use before committing multi-file changes.

## Fix a file in place

```bash
dgent run --fix <file>
```

Applies all deterministic fix rules (strip trailers, emoji, section headers) and writes back.

## Check a commit message

```bash
echo "your message" | dgent run --json --commit-msg -
```

Stdin with short non-code input auto-detects as commit-msg. Returns fixes (emoji, trailers) and flags (AI vocabulary).

## Get the full rule catalog

```bash
dgent rules --json
```

Returns every rule with name, phase, type, enabled status, and complete pattern lists. Use this to know exactly what to avoid.

## Patterns to avoid

These trigger flags (from `dgent rules --json`):

**Commit message words:** enhance, streamline, comprehensive, utilize, leverage, facilitate, robust, optimize

**Commit message phrases:** "this commit", "this change", "in order to", "aims to", "is designed to"

**Naming suffixes:** Manager, Handler, Processor, Service, Factory, Builder, Validator, Controller, Orchestrator, Coordinator

**Identifier length:** over 40 characters

**Catch-rethrow:** `catch (e) { console.error(e); throw e; }` — either handle the error or let it propagate

## Suppress a specific flag

```typescript
// dgent-ignore flag-naming
class DataProcessor { ... }  // not flagged
```

Supports `// dgent-ignore`, `// dgent-ignore-next-line`, `// dgent-ignore <rule1> <rule2>`.

## Workflow for agents

1. Write code
2. Run `dgent run --json <file>` on each modified file
3. Fix any flags (rename identifiers, remove catch-rethrow, etc.)
4. Run `echo "commit message" | dgent run --json --commit-msg -` on the message
5. Fix any message flags (remove AI vocabulary, rephrase)
6. Commit — dgent hooks will clean trailers and emoji automatically
