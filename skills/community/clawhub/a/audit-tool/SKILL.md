---
name: skill-auditor
description: "Deep audit for installed ClawHub skills — usage analysis, permission review, conflict detection"
---

# Skill Auditor (skill-auditor)

Audits all installed skills in the local OpenClaw environment. Scans metadata, files, permissions, dependencies, and usage history. Generates a health score, identifies zombie / duplicative / over-privileged skills, and produces cleanup scripts.

## Workflow

1. Scan installation — list all skills under `~/.openclaw/skills/` and installed packages. Read each `SKILL.md` for: name, description, allowed-tools, user-invocable, dependencies, license.
2. Usage analysis — parse session logs or call-frequency data over a configurable window (default 30 days). Compute: total invocations, trend (increasing / stable / declining / zero), last-used timestamp. Flag zombies (no usage in N days).
3. Security audit — for each skill, check:
   - Permission reasonability: does the skill's `allowed-tools` match actual tool usage? Flag over-privileged skills (e.g. a greeting skill with `exec` access).
   - Sensitive tool access: identify skills with `exec`, `web_fetch`, `script` access.
   - Excessive cross-skill access.
4. Conflict detection — pairwise comparison:
   - Overlapping `description` / `name` (duplicate functionality).
   - Conflicting tool or file namespace (two skills defining the same helper).
   - Circular dependencies.
5. Health score (0-100) — five dimensions weighted equally:
   - **Activity** (usage frequency / recency, 0-20)
   - **Security** (permission score, 0-20)
   - **Stability** (error rate / completeness, 0-20)
   - **Maintainability** (doc quality, file count, size, 0-20)
   - **Docs** (description clarity, sample prompts, 0-20)
6. Optimization suggestions — per skill:
   - Uninstall: zombie skills with no value
   - Suspend: rarely used but potentially useful
   - Permission downgrade: over-permissioned
   - Merge: overlapping skills into one
   - Upgrade: missing metadata or outdated format
7. Cleanup script — generate a shell script to: uninstall selected skills, disable (rename to `.disabled`), suspend (archive). Provide dry-run mode.
8. Output report — structured Markdown report with: executive summary, per-skill audit card (health score + flags), conflict matrix, cleanup script path. Optionally export as HTML dashboard.

## Sample prompts

- `skill-auditor audit`
- `skill-auditor audit --days 90 --min-activity 3`
- `skill-auditor audit --focus security`
- `skill-auditor cleanup --dry-run`
