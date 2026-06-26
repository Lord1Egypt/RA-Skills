---
name: agent-friendly-cli
description: Design and audit CLIs for agent usability. Use when building a new CLI tool, auditing an existing CLI for agent compatibility, reviewing CLI UX for AI agents, or adding agent-friendly patterns to command-line interfaces. Covers non-interactive design, progressive help discovery, pipeline support, idempotency, error handling, and structured output. Based on Cursor team research and field-tested patterns.
---

# Agent-Friendly CLI Design

Checklist and patterns for building CLIs that agents can use effectively. Most CLIs assume a human at the keyboard — these patterns close the gap.

## Core Principles

### 1. Non-Interactive by Default

Every input must be passable as a flag. Interactive prompts block agents.

```bash
# ❌ Blocks agents
$ mycli deploy
? Which environment? (use arrow keys)

# ✅ Works
$ mycli deploy --env staging
```

Keep interactive mode as fallback when flags are missing, never the primary path.

### 2. Progressive Help Discovery

Don't dump all docs upfront. Let agents discover via `--help` per subcommand.

```bash
# Agent runs top-level, sees subcommands
$ mycli --help

# Picks one, gets specific help
$ mycli deploy --help
```

An agent wastes no context on commands it won't use.

### 3. Useful --help with Examples

Every subcommand gets `--help`. Every `--help` includes examples. Agents pattern-match off examples faster than descriptions.

```
$ mycli deploy --help
Options:
  --env     Target environment (staging, production)
  --tag     Image tag (default: latest)
  --force   Skip confirmation

Examples:
  mycli deploy --env staging
  mycli deploy --env production --tag v1.2.3
  mycli deploy --env staging --force
```

### 4. Flags and stdin for Everything

Agents think in pipelines. Support chaining and piping.

```bash
cat config.json | mycli config import --stdin
mycli deploy --env staging --tag $(mycli build --output tag-only)
```

Don't require positional args in weird orders. Don't fall back to interactive prompts for missing values.

### 5. Fail Fast with Actionable Errors

Missing flag? Error immediately with correct invocation. Don't hang or print vague messages.

```bash
# ❌ Bad
$ mycli deploy
Error: missing required arguments

# ✅ Good
$ mycli deploy
Error: --env is required
Usage: mycli deploy --env <staging|production> [--tag <version>]
```

Agents self-correct when given something to work with.

### 6. Idempotent Commands

Agents retry constantly — network timeouts, context loss mid-task. Running the same command twice should be safe.

```bash
$ mycli deploy --env staging --tag v1.2.3
✓ Deployed v1.2.3 to staging

$ mycli deploy --env staging --tag v1.2.3
✓ Already deployed, no-op
```

### 7. --dry-run for Destructive Actions

Let agents preview before committing.

```bash
$ mycli deploy --env production --tag v1.2.3 --dry-run
Would deploy v1.2.3 to production
  - Stop 3 running instances
  - Pull image registry.io/app:v1.2.3
  - Start 3 new instances
No changes made.
```

### 8. --yes / --force to Skip Confirmations

Humans get "are you sure?" — agents pass `--yes`.

```bash
$ mycli delete-all --yes
```

Make the safe path the default but allow bypassing.

### 9. Predictable Command Structure

Pick a pattern and use it everywhere. If an agent learns one, it can guess the rest.

```bash
# resource + verb pattern
mycli service list
mycli deploy list
mycli config list
```

### 10. Structured Output on Success

Return actionable data, not just decorative messages.

```bash
# ❌ Cute but unhelpful
$ mycli deploy
🚀 Deployed successfully!

# ✅ Actionable
$ mycli deploy --env staging --tag v1.2.3
deployed v1.2.3 to staging
url: https://staging.myapp.com
deploy_id: dep_abc123
duration: 34s
```

Support `--json` for machine-readable output when possible.

### 11. Consistent Exit Codes

- `0` = success
- `1` = general error
- `2` = usage error (bad args)

Agents use exit codes to decide next steps.

## Audit Checklist

When reviewing an existing CLI for agent compatibility, check each item:

| # | Pattern | Check |
|---|---------|-------|
| 1 | Non-interactive | Can every input be passed as a flag? |
| 2 | Progressive help | Does each subcommand have its own `--help`? |
| 3 | Examples in help | Does `--help` include usage examples? |
| 4 | Stdin support | Can data be piped in via `--stdin` or `-`? |
| 5 | Fast failures | Do missing args error immediately with usage hint? |
| 6 | Idempotency | Is running the same command twice safe? |
| 7 | Dry run | Do destructive commands support `--dry-run`? |
| 8 | Skip prompts | Is there `--yes` / `--force` for confirmations? |
| 9 | Predictable structure | Is command naming consistent (resource + verb)? |
| 10 | Structured output | Does success output include actionable data? |
| 11 | JSON output | Is `--json` available for machine parsing? |
| 12 | Exit codes | Are exit codes consistent (0/1/2)? |

## When Designing a New CLI

1. Start with the flag-only interface. Add interactive prompts later as convenience.
2. Write the `--help` examples before writing the implementation.
3. Default to `--json` output internally, add human-friendly formatting on top.
4. Every write operation gets `--dry-run`. No exceptions.
5. Test by having an agent use it. Watch where it gets stuck.

## Source

Based on Eric Zakariasson's (Cursor) "Building CLIs for agents" (March 2026), field-tested across ClawVault, WorkGraph, and Versatly CLI ecosystem.
