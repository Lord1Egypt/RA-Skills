# Declutter — Full Procedure

## Overview

Inventory all installed skills, assess usage, identify redundancy, and recommend cleanup. Unused skills waste disk space, and always-loaded skills (those matching broad trigger patterns) consume context tokens every session.

## Step 1: Inventory Skills

1. List all directories in `~/.openclaw/skills/` (user-installed skills)
2. Check global skill paths (e.g., `/opt/homebrew/lib/node_modules/openclaw/skills/`)
3. For each skill, extract from SKILL.md frontmatter:
   - Name
   - Description
   - Version
   - Triggers (commands and patterns)
4. Calculate disk usage: `du -sh` on each skill directory
5. Count files per skill

Build the inventory table:

```
| Skill | Version | Files | Size | Triggers |
|---|---|---|---|---|
| clawspa | 1.0.0 | 8 | 24KB | /spa, pattern:health check |
```

## Step 2: Assess Usage

Determine when each skill was last used:

**Direct evidence:**
- Search recent daily memory files (last 30 days) for skill command mentions (`/spa`, `/gh-issues`, etc.)
- Check `memory/spa-reports/` for ClawSpa-specific history
- Look for skill names mentioned in session context

**Indirect evidence:**
- Skills with heartbeat/cron triggers may run silently. Check HEARTBEAT.md for references.
- Skills bundled with OpenClaw (system skills) may be used without explicit commands

**Categorize:**
- 🟢 **Active**: Used within last 7 days
- 🟡 **Idle**: Last used 8-30 days ago
- 🔴 **Dormant**: Not used in 30+ days, or no usage evidence found

## Step 3: Detect Overlapping Skills

Compare skill descriptions and triggers for functional overlap:

Common overlaps to check:
- Multiple SEO/content skills covering similar functionality
- Multiple memory/maintenance skills (janitor, self-improving, context-anchor, clawspa)
- Multiple coding agent skills
- Skills that wrap the same underlying tool (e.g., two different GitHub skills)

For each overlap pair, note:
- Which skill is more comprehensive
- Which has been used more recently
- Whether they can coexist or conflict

## Step 4: Estimate Context Impact

Skills that load into context affect available tokens. Estimate impact:

1. Read each skill's SKILL.md and count characters (tokens ~ chars / 4)
2. Check if the skill's description is always loaded (it is, during skill matching)
3. Note skills with very broad trigger patterns (these activate more often, loading their full SKILL.md more frequently)

Flag skills where:
- Description alone is >500 tokens (bloated metadata)
- SKILL.md body is >2000 tokens (heavy context load when triggered)
- Trigger patterns are overly broad (e.g., pattern: "help" would match almost everything)

## Step 5: Generate Recommendations

For each skill, recommend one action:

- **Keep**: Active, unique functionality, reasonable size
- **Review**: Idle but potentially useful, or has overlaps
- **Remove**: Dormant, duplicated by another skill, or excessive size for minimal functionality
- **Optimize**: Useful but oversized. SKILL.md could be trimmed or content moved to references/

## Step 6: Present Report

```
🧹 DECLUTTER REPORT
====================
Total skills: X | Total disk: X MB

🟢 ACTIVE (X skills)
- [name] — last used [date], [size]

🟡 IDLE (X skills)
- [name] — last used [date], [size] — [recommendation]

🔴 DORMANT (X skills)
- [name] — never used / last used [date], [size] — [recommendation]

⚠️ OVERLAPS DETECTED
- [skill A] and [skill B]: both handle [function]. Recommend keeping [preferred].

📐 CONTEXT IMPACT
- Heaviest skill descriptions: [name] (~X tokens always loaded)
- Broadest triggers: [name] (matches: [patterns])

RECOMMENDED ACTIONS:
1. Remove [skill] — dormant, saves X KB
2. Remove [skill] — duplicated by [other skill]
3. Optimize [skill] — SKILL.md is X tokens, could be trimmed

Total potential savings: X KB disk, ~X tokens context
```

## Safeguards

- Never uninstall a skill without explicit user approval
- Before recommending removal, verify no other skill or config depends on it
- System/bundled skills (shipped with OpenClaw) should be flagged as "system" and not recommended for removal unless the user specifically asks
- If unsure about usage, categorize as 🟡 Idle, not 🔴 Dormant
