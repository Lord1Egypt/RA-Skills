---
name: agent-stack-audit
emoji: 🔍
category: DevOps & Automation
tags: [stack-audit, cron-health, automation, maintenance, dead-code, api-cleanup, agent-ops]
description: >
  Monthly health check for your agent stack — hunts for zombie crons, dead scripts, unused API keys,
  superseded tools, and stale subscriptions. Classifies each finding as delete/replace/upgrade/healthy
  and outputs a ranked cleanup brief for your review. Use when your automation stack feels bloated,
  when bills are creeping up from unused services, or as a monthly maintenance run to prevent entropy.
  Prevents "automation debt" — the slow accumulation of dead weight that degrades system reliability.
author: Kenneth Kim (KK_HoldCo)
version: 1.0.0
---

# Agent Stack Audit

**Bottom line:** Run this monthly. Your agent stack accumulates dead weight faster than you think — zombie crons, unused APIs still billing you, scripts referencing killed strategies, and duplicate tools doing the same job. This skill finds all of it in one pass.

---

## When to Invoke

**Scheduled:** First Monday of every month, 05:00 local time.
**Quick scan:** Every Sunday (cron health only — 5 min).
**Manual trigger:** Any time the stack feels bloated, bills are unexpected, or reliability has degraded.
**Trigger phrases:** "stack audit", "clean up my automations", "what's still running?", "am I paying for anything unused?", "why are my API costs high?"

---

## Audit Scope (6 Categories)

### 1. Crons — Are they alive and earning their keep?

For each launchd agent / cron job / scheduled task:
- Is the process actually running? (check PID, plist/cron status)
- When did it last fire successfully?
- What does it produce? Is that output being consumed by anything?
- Is there a newer/better approach that renders this obsolete?

**Questions to answer:**
- "This cron runs every hour. Has its output file been read in the last 30 days?"
- "This watchdog monitors a bot that was killed 2 months ago — is the watchdog still running?"

### 2. Scripts — Dead code?

Scan your automation directories for Python/shell scripts:
- Last modified date vs last executed date
- Scripts referencing killed bots or cancelled APIs
- Scripts built for old projects that are now closed
- Duplicate scripts doing the same job

### 3. API Keys — Are you paying for something unused?

Cross-reference your API inventory against actual script usage:
- Any API key configured but never called in the last 30 days?
- Any paid subscription that maps to zero active script usage?
- Any free-tier key that's been maxed out — is an upgrade worthwhile?

Common culprits: data providers, news APIs, notification services, AI APIs at old models.

### 4. Skills — Superseded or never used?

Review your installed skills:
- Any skill built but never actually invoked?
- Any skill replaced by a newer, better version?
- Any skill with overlapping functionality that could be merged?

### 5. Memory Files — Stale project context?

Review project memory and context files:
- Any project memory not updated in 30+ days?
- Projects marked "on hold" for 60+ days with no activity?
- Contradictions between your main context file and individual project files?

### 6. Tools & Subscriptions — Better option available?

Using web search:
- "Is [tool] still the best option for [use case] as of [current month]?"
- Check for: price drops on existing tools, new free tiers, open source alternatives, better APIs
- Flag if a paid tool now has a free/cheaper replacement

---

## Classification Framework

For each item found, classify as:

| Classification | Meaning | Action |
|---|---|---|
| 🔴 ZOMBIE | Running but producing nothing useful | Recommend DELETE |
| 🟡 REDUNDANT | Superseded by newer/better approach | Recommend REPLACE or MERGE |
| 🟠 OUTDATED | Still useful but using old tech/API | Recommend UPGRADE |
| 🟢 HEALTHY | Working, used, best current approach | No action |
| ⚪ UNKNOWN | Can't determine without user input | Flag for user decision |

---

## Output Format

File: `state/stack_audit_YYYY-MM-DD.md`

```markdown
# Stack Audit — [DATE]
_Scope: Crons, Scripts, APIs, Skills, Memory, Tools_
_Items scanned: [N] | Issues found: [M] | Recommended actions: [K]_

---

## 🔴 RECOMMEND DELETE (zombies)
| Item | Type | Reason | Risk if deleted |
|---|---|---|---|
| old_watchdog.sh | Cron | Bot killed Mar 12, watchdog still running | None — bot is dead |

## 🟡 RECOMMEND REPLACE/MERGE (redundant)
| Item | Type | Replaced By | Action |
|---|---|---|---|
| old_intelligence_scan.py | Script | Tech Scout skill | Kill script, activate skill |

## 🟠 RECOMMEND UPGRADE (outdated)
| Item | Type | Current | Better Option | Est. Saving/Gain |
|---|---|---|---|---|
| image_gen API call | API | DALL-E 3 | [Cheaper/better alternative] | ~40% cost reduction |

## 🟢 HEALTHY — No Action
[List with one-line confirmation each]

## ⚪ NEEDS USER INPUT
[Items that require your decision — presented as yes/no questions]

---

## Summary
- Recommended deletes: [N items] — saves [X $/mo or compute]
- Recommended upgrades: [N items]
- Estimated cleanup time if approved: ~[X hours]
- Most important action: [single highest-leverage item]
```

---

## Execution Rules

1. **Never delete anything without explicit user approval** — only RECOMMEND
2. **One exception:** If a script references a dead API that has been confirmed cancelled → safe to comment out the call and log it. Don't delete the file.
3. **If unsure → classify as ⚪ UNKNOWN.** Never guess on deletions.
4. After approvals: execute cleanup and write `state/stack_cleanup_YYYY-MM-DD.md` confirming what was removed and what the before/after count was.

---

## Quick Scan (Sunday Cron Health Check)

Lighter weekly version — runs in 5 minutes:

1. Check all scheduled tasks/crons are firing on schedule
2. Check all PID files match running processes
3. Check for any `ERROR` or `FAILED` in last 24h logs
4. Output: `state/cron_health_YYYY-MM-DD.md` — just a pass/fail list, no detail

---

## Why This Matters

Left unchecked, automation stacks accumulate:
- **Zombie crons** that run every hour and log to files no one reads
- **API subscriptions** billing monthly for services killed 6 months ago
- **Duplicate scripts** that were "temporary" but became permanent
- **Stale context files** that feed wrong information to your agents

The monthly audit is what separates a clean, reliable stack from a pile of debt that fails when you need it most. Most teams discover 20-40% of their crons are either dead or redundant on the first pass.