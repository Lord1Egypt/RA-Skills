# SKILL: claw-janitor

## Description
A safe, zero-dependency, platform-aware system cleanup skill for OpenClaw. Use when disk space is low or cleanup is requested.

## Rules & Constraints
- Prefer `--dry-run` first when user confidence is low.
- Never force sudo/root; only do elevated/system cleanup when user explicitly wants it.
- Respect built-in safety boundaries (blacklists, symlink/mount protections, AI-cache no-auto-delete).

## Command

```bash
node /root/.openclaw/workspace/skills/claw-janitor/janitor.js [flags]
```

## Flags
- `--dry-run`: preview only
- `--deep`: aggressive cleanup mode
- `--json`: structured output
- `--no-color`: disable ANSI color
- `--report-file <path>`: write JSON summary to file
- `--only <group>`: run only one group (`ai-scan|packages|docker|system`)
- `--skip <group>`: skip one group (`ai-scan|packages|docker|system`)
- `-h, --help`: show usage

## Examples
- “Clean up my disk”
  - `node /root/.openclaw/workspace/skills/claw-janitor/janitor.js`
- “Show me first”
  - `node /root/.openclaw/workspace/skills/claw-janitor/janitor.js --dry-run`
- “Only clean package caches”
  - `node /root/.openclaw/workspace/skills/claw-janitor/janitor.js --dry-run --only packages`
- “Generate audit report”
  - `node /root/.openclaw/workspace/skills/claw-janitor/janitor.js --dry-run --json --report-file /tmp/janitor-report.json`
