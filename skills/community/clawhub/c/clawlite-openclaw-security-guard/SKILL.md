---
name: openclaw-security-guard
description: This skill should be used when the user asks to harden agent workflows, audit prompts/commands/URLs/paths, scan a third-party skill before install or publish, review a skill folder for secrets or unsafe scripts, or add a lightweight local security guard before OpenClaw publishing and automation.
---

# OpenClaw Security Guard

Use this skill to run **fast local security checks** before trusting or publishing automation.

## What this skill is for

Run this skill when you need to:
- scan suspicious text for prompt injection / secret leakage patterns
- validate shell commands before automation or publishing
- validate URLs for SSRF / localhost / metadata access risks
- validate file paths for traversal / sensitive file access
- audit a skill folder for dangerous scripts, hardcoded secrets, exfiltration patterns, or unsafe install/publish flows
- add a lightweight self-defense layer before using external skills

## Workflow

1. Choose the narrowest check needed.
2. Run one of the bundled scripts.
3. Treat `BLOCK` as stop-work until reviewed.
4. Treat `WARN` as requiring human review or a narrower sandbox.
5. For skill audits, review the flagged file lines before install/publish.

## Bundled scripts

### 1) Quick text / command / URL / path checks

```bash
node {baseDir}/scripts/security-check.mjs text "<content>"
node {baseDir}/scripts/security-check.mjs command "<shell command>"
node {baseDir}/scripts/security-check.mjs url "<url>"
node {baseDir}/scripts/security-check.mjs path "<path>"
```

### 2) Skill / folder audit

```bash
node {baseDir}/scripts/audit-skill-dir.mjs /absolute/or/relative/path/to/skill
```

### 3) Write audit into Obsidian vault

```bash
node {baseDir}/scripts/write-obsidian-audit.mjs /tmp/audit.json "Skill Audit - my-skill"
```

This writes a markdown audit note into the ClawLite Obsidian vault under `Security Audits/`.

### 4) Install lightweight local hook wrapper

```bash
bash {baseDir}/scripts/install-hooks.sh
```

This installs a reusable workspace script for prepublish checks.

This audits for:
- hardcoded secrets / tokens
- curl|bash / wget|sh installers
- destructive shell patterns
- risky exfiltration / webhook / netcat usage
- suspicious file targets like `~/.ssh`, `/etc/passwd`, `.env`, `id_rsa`

## Verdicts

- `ALLOW` — no high-risk pattern found in this lightweight pass
- `WARN` — review manually before proceeding
- `BLOCK` — do not trust / run / publish until reviewed

## Important limits

- This is a **lightweight guard**, not a full sandbox.
- Regex-based detection catches common dangerous patterns, not all attacks.
- A clean result does **not** prove safety.
- For high-risk code, still prefer human review and runtime isolation.

## Publishing / install guard

Before publishing or installing a skill from GitHub / ClawHub:
1. run `audit-skill-dir.mjs`
2. inspect every `WARN` / `BLOCK`
3. only proceed when the remaining risk is understood

## References

If you need the audit categories / philosophy, read:
- `{baseDir}/references/checklist.md`
