---
name: agent-portability-checker
description: >
  Audit agent skills for platform lock-in and cross-agent compatibility. Use when checking
  if a skill is portable, making a skill work across multiple agents (OpenClaw, Claude Code,
  Codex, etc.), fixing hardcoded paths, or preparing a skill for multi-platform distribution.
  Checks for hardcoded platform paths, missing env var support, and platform-specific
  dependencies.
---

# Agent Portability Checker 🔌

Audit an agent skill for platform lock-in. Auto-fixes what it can, flags what needs manual attention.

## Why

Skills with hardcoded paths only work on one platform. This tool catches those issues and fixes them — making your skills work everywhere agents run.

## When to Use

- "Is this skill portable?"
- "Make this skill cross-platform"
- "Check for hardcoded paths"
- "Prepare a skill for other agents"

## How to Run

```
python3 scripts/audit.py <skill_dir>          # audit only
python3 scripts/audit.py <skill_dir> --fix    # auto-fix + audit
python3 scripts/audit.py <skill_dir> --json   # structured output
```

## What It Checks

```
📍 Hardcoded paths     — platform-specific dirs like ~/.<platform>/ in scripts
🔧 SKILL_DATA_DIR      — env var support for data dir resolution
📦 XDG fallback        — ~/.config/<skill>/ fallback path
🔌 Platform CLI deps    — external binary dependencies (e.g. clawhub, gh)
🏷️  User-Agent strings — platform names in HTTP headers
📄 SKILL.md paths      — platform-specific path references in docs
🖥️  Headless setup     — OAuth scripts without --no-browser flag
🔑 Credential env vars — file-only credentials with no env var alternative
```

## Output Example

```
❌ github-growth-tracker — 8 errors, 9 warnings (9 auto-fixable)

📍 Hardcoded Paths
  ❌ scripts/github_tracker.py:28: ~/.<platform>/ [auto-fix]
  ❌ scripts/github_tracker.py:31: ~/.<platform>/ [auto-fix]

🔧 SKILL_DATA_DIR: Not supported — scripts use hardcoded paths
🔧 XDG Fallback: Missing ~/.config/ fallback path
```

## Two-Phase Flow

1. **Audit** — show all findings (auto-fixable + manual)
2. **Fix** — apply auto-fixes, show brief "what changed" confirmation

The agent reads the script output and formats it for the current channel. See `references/formatting.md` for Slack/WhatsApp/Discord styling.

## Auto-Fixes

- Replaces `~/.<platform>/credentials/` with `$SKILL_DATA_DIR`
- Replaces `~/.<platform>/workspace/data/<skill>/` with `$SKILL_DATA_DIR/<skill>/`
- Strips platform names from User-Agent strings
- Replaces hardcoded paths in SKILL.md with `<DATA_DIR>` placeholder

⚠ **Output styling is never modified.** Emojis, formatting, and visual elements in script output are preserved exactly as-is.

Manual flags require human review (platform CLI deps, headless setup, env var alternatives).

## Formatting

Read `references/formatting.md` for channel-specific styling (Slack, WhatsApp, Discord, terminal).

## The Portability Pattern

Skills that work everywhere follow this:

```
1. Resolve data dir via $SKILL_DATA_DIR (set by agent platform)
2. Fall back to ~/.config/<skill>/ (XDG-compliant, works everywhere)
3. Accept credentials via env var OR file (env var preferred)
4. Output to stdout — no platform messaging APIs
5. Self-contained scripts — no platform SDK imports
```
