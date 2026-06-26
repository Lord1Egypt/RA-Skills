---
name: config-sentinel
description: A strict guardrail for OpenClaw config changes. Snapshot before editing, validate after editing, and rollback immediately when config health fails. Built to prevent broken agents, malformed JSON, missing bindings, and catastrophic config regressions.
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins:
        - python3
---

# Config-Sentinel

Use this skill whenever you are modifying OpenClaw configuration.

This is **not** a soft suggestion. Config changes are high-risk operations. A single bad edit can break agent routing, bindings, startup behavior, or entire multi-agent setups.

If config integrity matters, **do not skip this workflow**.

This skill is especially useful for:
- manual edits to the main OpenClaw config file
- scripted config patches
- agent/binding/channel changes
- diagnosing whether a config file is malformed or incomplete
- recovering from a broken config change

## Purpose

Config-Sentinel exists because successful writes are not the same as healthy config.

A config file can be:
- syntactically broken
- structurally incomplete
- silently truncated
- internally inconsistent
- accepted by an editor but dangerous at runtime

This skill enforces a strict safety workflow:

1. snapshot before changes
2. validate after changes
3. rollback immediately if validation fails
4. run health checks when config behavior looks suspicious

---

## Approval Rule

**Do not change OpenClaw config without explicit user approval.**

Snapshot/rollback protects against corruption. It does **not** replace human approval.

The correct order is:
1. get approval to make the config change
2. run `pre-change`
3. make the change
4. run `validate`
5. rollback if needed
6. report the result clearly

## Core Workflow

Before editing config:

```bash
scripts/sentinel.sh pre-change
```

After editing config:

```bash
scripts/sentinel.sh validate
```

If validation fails:

```bash
scripts/sentinel.sh rollback
```

For an on-demand health check:

```bash
scripts/sentinel.sh health
```

### Non-negotiable rule

Do not edit config first and hope validation will save you later.

The correct order is always:
1. snapshot
2. edit
3. validate
4. rollback if needed

---

## What It Protects Against

Config-Sentinel is designed to catch or soften failures such as:
- malformed JSON
- incomplete or truncated config writes
- missing agent entries
- bindings that reference missing agents
- invalid channel/account structure
- missing expected config file after an edit
- accidental regressions after a patch

It also creates recovery points so rollback is straightforward.

---

## Features

### Pre-change snapshot
Before any config edit, create:
- a timestamped backup copy
- a git snapshot when the config directory is in a git repo
- a remembered last-known-good revision for rollback

### Validation
After a config change, validate:
- JSON parseability
- presence of expected high-level keys
- minimum agent count threshold
- bindings referencing real agent ids
- optional required workspace files
- optional provider-specific checks

### Rollback
Restore the last-known-good config snapshot if a change breaks structure or validation.

### Health check
Run validation without making changes to assess config health.

### Strict posture
This skill is intentionally strict. Config changes are one of the easiest ways to break a working OpenClaw setup.

---

## Defaults and Overrides

The helper script uses sensible defaults, but supports environment overrides.

### Default paths
- config file: `~/.openclaw/openclaw.json`
- sentinel state dir: `~/.openclaw/.sentinel`

### Optional environment variables
- `CONFIG_SENTINEL_CONFIG_FILE`
- `CONFIG_SENTINEL_DIR`
- `CONFIG_SENTINEL_MIN_AGENTS`
- `CONFIG_SENTINEL_REQUIRED_FILES`
- `CONFIG_SENTINEL_VALIDATE_BINDINGS`
- `CONFIG_SENTINEL_VALIDATE_TELEGRAM_TOKENS`

This allows the skill to adapt to different setups while keeping a strict default posture.

---

## Best Practice Pattern

When an agent is asked to change config, the safe pattern is:

1. run `pre-change`
2. apply the config change
3. run `validate`
4. if validation fails, run `rollback`
5. tell the user clearly whether the config is healthy

Do not silently edit config without a recovery path.
Do not trust a successful write alone.
Do not continue after validation failure unless the user explicitly wants forensic inspection instead of safety.

---

## Generic Example

### Good
```bash
scripts/sentinel.sh pre-change
# edit config
scripts/sentinel.sh validate || scripts/sentinel.sh rollback
```

### Good agent wording
- “I created a config snapshot before editing.”
- “Validation passed after the patch.”
- “Validation failed, so I rolled back to the last-known-good config.”

### Bad
- editing config directly with no snapshot
- assuming the file is fine because the write completed
- continuing after parse errors or missing agent references

---

## Notes

This skill does **not** run continuously. It is an on-demand guardrail for risky config operations.

Use it whenever config integrity matters more than speed.
If you are about to patch or rewrite config and you are tempted to skip the snapshot step, that is exactly when you should not skip it.

---

## Summary

Config-Sentinel helps make OpenClaw config changes safer by combining:
- snapshots
- validation
- rollback
- health checks

The goal is simple:

**make config edits recoverable instead of catastrophic.**

## Security notes

Config-Sentinel intentionally reads and copies the local OpenClaw config so it can validate and restore it. The script passes environment-derived paths and options into Python as argv values, not interpolated Python source, to avoid code injection from crafted environment overrides.

Required local dependency: `python3`. Optional dependency: `git` for config-directory snapshots; without git, timestamped local backups are still created.
