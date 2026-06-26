---
name: agent-provenance
description: >-
  File provenance tracking, authority levels, commit conventions, and
  governance policies. Ensures accountability for changes to instruction
  files, topic files, and contact files. Tracks review history with
  graduated urgency (30/60/90 day escalation), enforces TTL on
  agent-written goals and stale topic files, and provides clear ownership
  for agent-maintained documentation. Works with hierarchical-agent-memory
  and agent-session-state.
license: MIT
compatibility: "OpenClaw 2026.4.x or later."
metadata:
  openclaw:
    requires:
      bins: ["openclaw", "git"]
    paths:
      write: ["AGENTS.md", "IDENTITY.md", "TOOLS.md", "BOOT.md", "LEARNINGS.md", "HEARTBEAT.md", "MEMORY.md", "memory/topics/", "memory/contacts/"]
      read: ["SOUL.md", "PRINCIPLES.md", "USER.md", "AGENTS.md", "IDENTITY.md", "TOOLS.md", "BOOT.md", "LEARNINGS.md", "HEARTBEAT.md", "MEMORY.md", "memory/"]
  version: "2.1.4"
  clawhub: {"category": "governance", "tags": ["provenance", "audit", "review", "ttl", "git"]}
---

# Agent Provenance v2.1.4

Agents modify their own instruction files, topic files, and memory. Without tracking, human-authored rules become indistinguishable from agent-authored additions. This skill provides lightweight governance to maintain that distinction — provenance headers, authority levels, commit conventions, and review policies to ensure accountability and maintainability.

## The Problem

Instruction files evolve over time. Without clear tracking, it's unclear who made changes and when, review responsibilities become ambiguous, agent-written goals can persist indefinitely without validation, security boundaries can be eroded gradually, and audit trails are lost.

## Prerequisites

This skill requires git to be initialized in the workspace. The agent needs write access to instruction files and memory files (declared in the metadata above). Diff reports are posted to the conversation channel — no external channel credentials are needed unless the user configures an external destination.

All scheduled tasks (diff reports, heartbeat checks) use OpenClaw's built-in `cron` tool. They run as isolated agent sessions within the OpenClaw sandbox. No OS-level schedulers (crontab, systemd, launchd) are created or modified.

## Architecture

### Provenance Headers

All instruction files carry an HTML comment header:

```markdown
<!--
  provenance: human-authored | agent-authored | mixed
  description: what this file is
  last-reviewed: YYYY-MM-DD
  reviewed-by: Human | Agent
-->
```

Provenance types:

- **human-authored** — files created by the human user and not modified by the agent without explicit direction (SOUL.md, PRINCIPLES.md, USER.md)
- **agent-authored** — files created and maintained by the agent (LEARNINGS.md, session files, daily notes, topic files, time-based archives)
- **mixed** — files with both human policy and agent procedures (AGENTS.md, IDENTITY.md, TOOLS.md, HEARTBEAT.md, BOOT.md, contact files)
- **transient** — one-shot scratch files with no provenance cadence (BOOTSTRAP.md). Not governed by this skill — OpenClaw creates them for a brand-new workspace and removes them after the bootstrap ritual finishes.

Only the user updates last-reviewed and reviewed-by on human-authored files.

### Authority Levels

Files have different sensitivity levels that determine who can modify them and how changes are tracked.

**Human-authored files** (SOUL.md, PRINCIPLES.md, USER.md) define the agent's identity and core rules. The agent does not modify these without explicit direction from the user.

**Mixed files** (AGENTS.md, IDENTITY.md, TOOLS.md, HEARTBEAT.md, BOOT.md, contact files) have user-set policy with agent-maintained operational procedures. IDENTITY.md is created during the bootstrap ritual and may be updated by the agent, but the user owns the underlying identity assertions. TOOLS.md holds local tool notes and conventions — user-shaped guidance that blends with agent-observed usage patterns. BOOT.md is an optional startup checklist with the same mixed ownership. Contact files are mixed because the agent captures information from conversations but the user may correct details or add private context. All changes are logged in git.

**Transient files** (BOOTSTRAP.md) are first-run scratch files that OpenClaw creates for a brand-new workspace and deletes after the bootstrap ritual. They carry no provenance header and are not subject to review cadence. If BOOTSTRAP.md persists for more than a few sessions, flag it as an anomaly rather than treating it as a reviewable instruction file.

**Agent-authored files** (LEARNINGS.md, session files, daily notes, topic files) are written freely by the agent and reviewed periodically by the user. Topic files represent authoritative project state and should be treated with more care than transient session files.

**Routing table** (MEMORY.md) has mixed authority. The agent maintains pointers, but MEMORY.md is loaded into every session's system prompt, so changes have high impact. Keep it under 3KB with only pointers and active constraints. Log all changes via git with appropriate commit tags.

### Commit Message Convention

Workspace commits use a tag prefix to identify who directed the change:

- `[human-directed]` — the user explicitly asked for this change
- `[agent-autonomous]` — the agent decided to make this change independently
- `[heartbeat]` — change made during a heartbeat cycle
- `[cron]` — change made by a scheduled job

This makes `git log --oneline <file>` a real audit trail.

Software project commits (any external project) use plain descriptive messages with NO provenance tags. Tags like `[human-directed]` are AI fingerprints — they leak that an agent is involved in the project.

### TTL on Agent-Written Goals

Anything the agent writes to a goals, tasks, or backlog section gets a date stamp. If an agent-written goal is older than 14 days and the user hasn't touched it, the agent does not silently keep following it. Instead, ask the user whether it's still valid.

### TTL on Topic Files

Topic files represent active projects and workstreams. If a topic file hasn't been modified in 30 or more days, flag it for the user during the next heartbeat: "The topic file for [project] hasn't been updated in a month. Is this still active, or should it be archived?" If the user confirms it's still active, update the file's timestamp. If the user says archive it, move it to `memory/topics/archive/` and remove the pointer from MEMORY.md.

This prevents stale topic files from accumulating and cluttering search results, and keeps MEMORY.md's routing table current.

### Instruction Diff Reports

Weekly (or on-demand via "diff report"): the agent diffs all instruction files against their state 7 days ago and posts a summary to the conversation. What changed, who changed it, why. The user reviews, confirms, or reverts.

Schedule the diff report at a fixed local time that works for the user (e.g., Sunday morning). There's nothing special about the exact time — pick one, set a cron using OpenClaw's built-in cron tool, be consistent.

### Review Flagging with Graduated Urgency

Instruction files and key memory files should be reviewed periodically. Rather than a single flag, use graduated urgency:

**30 days since last review** — mention during heartbeat. Example: "AGENTS.md hasn't been reviewed in 30 days. Worth a quick look when you have time."

**60 days since last review** — warn explicitly. Example: "AGENTS.md is 60 days past its last review. I'm still following its instructions, but they may be outdated. Can you review it this week?"

**90 days since last review** — escalate. Example: "AGENTS.md hasn't been reviewed in 90 days. At this point it's either stable enough to not need review (in which case, update the review date to acknowledge that) or it's drifted without anyone noticing. Please review and confirm."

This applies to human-authored and mixed files. Agent-authored files don't need the same review cadence but benefit from periodic user spot-checks.

## Setup

Initialize git in the workspace if it isn't already a repository, and configure a local git identity for agent commits. Use a name that makes agent-authored commits identifiable in the log. Create a `.gitignore` if needed to exclude temporary files, secrets, and local state.

## Daily Provenance Checks

During heartbeat cycles:

1. Check last-reviewed dates in provenance headers of all instruction files
2. Apply graduated urgency: mention at 30 days, warn at 60, escalate at 90
3. Check for agent-written goals/tasks older than 14 days without user interaction — flag for re-authorization
4. Check for topic files untouched for 30 or more days — flag for archival or confirmation
5. Generate weekly diff report if due

## Security Implications

Provenance tracking provides defense in depth. It makes unauthorized changes visible in git history, enforces regular review of critical files, provides accountability for agent actions, and creates an audit trail for compliance.

**Sensitive data:** Provenance headers and commit messages should never contain secrets, API keys, or credentials. Commit messages describe what changed and why — they should reference file names and decisions, not secret values. The same redaction guidance from agent-session-state applies: log the existence of a credential and where it is stored, not the value itself.

## Integration with Other Skills

**hierarchical-agent-memory** provides the memory structure this skill governs. MEMORY.md is a lean routing table with pointers to topic and contact files. Topic files are agent-authored and subject to the 30-day staleness check. Contact files are mixed authority. Daily notes and time-based archival layers are agent-authored and maintained freely. All memory file changes should use appropriate commit tags.

**agent-session-state** manages per-channel session files. Session state files are agent-authored and transient. They don't need provenance headers or review cadence, but commits that modify them should use the appropriate tag for audit trail purposes.

**memory-wiki** (bundled OpenClaw plugin, as of 2026.4.x) compiles durable knowledge into a separate vault at `~/.openclaw/wiki/main/` with its own lifecycle: structured claims, evidence linkage, freshness dashboards, `wiki_lint`, and the `reports/` dashboard set. This skill does not govern the wiki vault. Do not retrofit provenance headers, `last-reviewed` dates, graduated urgency, or commit-tag discipline onto wiki pages — wiki has its own claim-level schema and lint tooling, and the two systems are deliberately orthogonal (file authorship and accountability vs. claim-level evidence lineage). Commits that touch wiki output should still use appropriate tags for audit trail purposes, but the pages themselves are out of scope.

## Best Practices

**For the agent:** Always include provenance headers on new instruction files and new topic/contact files. Update last-reviewed after the user reviews a file. Use appropriate commit tags. Flag old content for review using graduated urgency. Ask the user about stale agent-written goals. Flag untouched topic files for archival.

**For the user:** Review flagged files promptly — graduated urgency means the agent will keep escalating until you respond. Update last-reviewed and reviewed-by after each review. Provide clear direction for changes explicitly requested. Periodically check git history for anomalies. When archiving a topic, confirm the MEMORY.md pointer is removed.

## Related Skills

- **hierarchical-agent-memory** — Hybrid topic-based working memory with optional time-based archival layers
- **agent-session-state** — Per-channel isolation and WAL protocol
