---
name: agent-provenance
description: >-
  File authorship tracking, authority levels, commit conventions, and
  governance policies for agent workspaces. Ensures accountability for
  changes to instruction files, topic files, and contact files. Tracks
  review history with graduated urgency (30/60/90 day escalation), flags
  stale agent-written aspirations and topic files, and provides clear
  ownership for agent-maintained documentation. Run /agent_provenance check
  for an on-demand review. Works with hierarchical-agent-memory and
  agent-session-state.
license: MIT-0
compatibility: "OpenClaw 2026.4.x or later."
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: ["openclaw", "git"]
    paths:
      write: ["AGENTS.md", "IDENTITY.md", "USER.md", "BOOT.md", "TOOLS.md", "HEARTBEAT.md", "LEARNINGS.md", "MEMORY.md", "memory/topics/", "memory/contacts/"]
      read: ["SOUL.md", "PRINCIPLES.md", "USER.md", "AGENTS.md", "IDENTITY.md", "BOOT.md", "TOOLS.md", "HEARTBEAT.md", "LEARNINGS.md", "MEMORY.md", "memory/", "users/"]
  version: "2.3.0"
  clawhub: {"category": "governance", "tags": ["provenance", "audit", "review", "ttl", "git"]}
---

# Agent Provenance v2.3.0

Agents modify their own instruction files, topic files, and memory. Without tracking, human-authored rules become indistinguishable from agent-authored additions. This skill provides lightweight governance to maintain that distinction: provenance headers, authority levels, commit conventions, and review policies that keep instruction files accountable and maintainable.

## At a glance: what OpenClaw tracks, and what this skill tracks

OpenClaw now uses the word "provenance" for something different, so be precise about the layer. OpenClaw's memory provenance records where memory *content* came from and whether it can be trusted: every indexed chunk carries an origin class (owner, agent, untrusted, or system), dreaming keeps per-entry origins so `openclaw memory forget` can remove what a session contributed (2026.8.1 and later), a write observer records curated writes to memory files, and workspace provenance records decide whether `MEMORY.md` and `USER.md` are even injected into a session. That machinery answers "which conversation did this fact come from, and is it safe to promote?"

This skill answers a different question: who is responsible for each workspace *file*, when did a human last review it, and did the agent change it on its own or on request. OpenClaw's memory tier model assumes instruction files are "human only"; in practice an agent maintains procedures inside AGENTS.md, updates IDENTITY.md and USER.md on request, and writes topic files freely. This skill makes that mixed reality visible and reviewable. The two layers complement each other; neither replaces the other.

Three bundled plugins sit nearby and are worth knowing about. The **policy** plugin (2026.5.20 and later, `openclaw plugins enable policy`) checks configuration posture against a `policy.jsonc` you author, reports drift through `openclaw doctor --lint`, and produces attestation hashes; it governs config and the `## Tools` metadata in AGENTS.md, not the review state of instruction content. The **agent-guidance** plugin (recent mainline) injects shared instruction files from an operator-controlled directory outside any agent-writable workspace; for rules the agent must never be able to edit, that is the stronger control, and this skill's headers then cover the files that must live in the workspace. The **diffs** plugin renders before/after text as a viewable diff; where it is installed, the agent may use it to present a diff report. Enterprise users typically run policy and this skill together: policy for config conformance, this skill for instruction-content review.

## The Problem

Instruction files evolve over time. Without clear tracking, it's unclear who made changes and when, review responsibilities become ambiguous, agent-written aspirations can persist indefinitely without validation, security boundaries can be eroded gradually, and audit trails are lost.

## Slash commands

The skill is user-invocable. Where your channel registers skill commands natively, the command appears as `/agent_provenance` (the skill name with characters outside letters, digits, and underscores replaced). The generic form `/skill agent-provenance <command>` always works. Skill commands route through the model, so the agent follows the matching section of this file. Supported commands:

- `check` (default when no argument is given) runs a full provenance check as described under Provenance Checks and posts the result to the conversation.
- `diff [days]` posts an instruction diff report for the last N days (default 7).
- `review <file>` records that the user has just reviewed the named file: updates `last-reviewed` and `reviewed-by: Human` in its header, and commits with a `[human-directed]` tag.
- `stale` lists only the TTL findings: aspirations older than 14 days and topic files untouched for 30 or more days.
- `tags` shows the commit-tag convention and the last ten workspace commits with their tags, so the user can see whether the convention is being followed.

## Prerequisites

This skill requires git in the workspace. OpenClaw initializes a git repository automatically for brand-new workspaces when git is installed; for older workspaces, see Setup. The agent needs write access to instruction files and memory files (declared in the metadata above). Diff reports are posted to the conversation; no external channel credentials are needed unless the user configures another destination.

This skill creates no scheduled jobs on its own. Provenance checks and diff reports run when the user asks. A weekly scheduled check is optional and is only created after the user explicitly agrees to it (see Provenance Checks). If created, it uses OpenClaw's built-in `automations` tool (named `cron` before 2026.8.1) and runs as an isolated agent session within the OpenClaw sandbox. No OS-level schedulers are created or modified.

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

- **human-authored**: files created by the human user and not modified by the agent without explicit direction (SOUL.md, PRINCIPLES.md)
- **agent-authored**: files created and maintained by the agent (LEARNINGS.md, session files, daily notes, topic files, time-based archives)
- **mixed**: files with both human policy and agent procedures (AGENTS.md, IDENTITY.md, USER.md, BOOT.md, contact files, and TOOLS.md and HEARTBEAT.md where your OpenClaw version still uses them)
- **transient**: one-shot scratch files with no provenance cadence (BOOTSTRAP.md). Not governed by this skill; OpenClaw creates them for a brand-new workspace and removes them after the bootstrap ritual.

Only the user updates last-reviewed and reviewed-by on human-authored files.

**USER.md carries its own metadata.** OpenClaw's user-model format puts a `<!-- observed: YYYY-MM-DD | status: active|superseded -->` line above each directive. Those per-directive lines are the source of truth for when a preference was observed and whether it still applies; this skill's file-level header records only when a human last reviewed the file as a whole. Never rewrite the per-directive lines during a provenance check, and never add this skill's header to a personal `users/<profile-id>/USER.md` on a multi-user gateway; those files belong to the person who owns them.

### Authority Levels

Files have different sensitivity levels that determine who can modify them and how changes are tracked.

**Human-authored files** (SOUL.md, PRINCIPLES.md) define the agent's identity and core rules. The agent does not modify these without explicit direction from the user. In multi-agent setups, rules that the agent must never be able to touch are better served from an operator-controlled directory through the agent-guidance plugin; this skill's header then documents that the workspace copy, if any, is a mirror.

**Mixed files** (AGENTS.md, IDENTITY.md, USER.md, BOOT.md, contact files) have user-set policy with agent-maintained operational procedures. IDENTITY.md is created during the bootstrap ritual and may be updated by the agent, but the user owns the underlying identity assertions. USER.md is OpenClaw's user model: the user owns what it says, and the agent updates it when the user asks (or, on multi-user gateways, through the `personal_instructions` tool). AGENTS.md also holds local tool notes in its `## Tools` section, which the policy plugin can govern separately. BOOT.md is an optional startup checklist with the same mixed ownership. Contact files are mixed because the agent captures information from conversations but the user may correct details or add private context. All changes are logged in git.

TOOLS.md and HEARTBEAT.md depend on your OpenClaw version. OpenClaw 2026.8.1 retired HEARTBEAT.md (its checklist moved into automation scratch), and by 2026.9.7 TOOLS.md was retired (its content moved into the `## Tools` section of AGENTS.md, and the runtime no longer recognizes it as a bootstrap file). Extended-stable releases from before 2026.8.1 still read both files. Check the version with `openclaw --version`. If either file exists and your version still reads it, govern it as a mixed file. If your version has retired it, tell the user that `openclaw doctor --fix` migrates it. Do not run doctor yourself.

**Transient files** (BOOTSTRAP.md) are first-run scratch files that OpenClaw creates for a brand-new workspace and deletes after the bootstrap ritual. They carry no provenance header and are not subject to review cadence. If BOOTSTRAP.md persists for more than a few sessions, flag it as an anomaly rather than treating it as a reviewable instruction file.

**Agent-authored files** (LEARNINGS.md, session files, daily notes, topic files) are written freely by the agent and reviewed periodically by the user. Topic files represent authoritative project state and should be treated with more care than transient session files. Daily notes live at `memory/YYYY-MM-DD.md`.

**Routing table** (MEMORY.md) has mixed authority. The agent maintains pointers, but MEMORY.md is loaded into the main session's system prompt, so changes have high impact. Keep the hand-maintained part under 3KB with only pointers and active constraints. From 2026.8.1, dreaming also writes entries here, marked with `<!-- trigger: … -->` and `<!-- importance: N -->` comments and a `Source:` reference; those entries are machine-authored. Do not retrofit headers or review dates onto them, and in a diff report attribute them to dreaming rather than to the agent. Log all hand changes via git with appropriate commit tags.

### Commit Message Convention

Workspace commits use a tag prefix to identify who directed the change:

- `[human-directed]`: the user explicitly asked for this change
- `[agent-autonomous]`: the agent decided to make this change independently
- `[heartbeat]`: change made during a heartbeat cycle
- `[automation]`: change made by a scheduled job (`[cron]` is accepted as a synonym, and is the natural spelling on releases before 2026.8.1)
- `[dreaming]`: change made by OpenClaw's dreaming sweep, when the user's backup routine commits MEMORY.md after a sweep

This makes `git log --oneline <file>` a real audit trail. If a nightly backup routine commits everything under one generic message, the convention is not being followed; `/agent_provenance tags` makes that visible, and the fix is to have the agent commit its own changes with tags before the backup runs.

Software project commits (any external project) use plain descriptive messages with NO provenance tags. Tags like `[human-directed]` are AI fingerprints; they leak that an agent is involved in the project.

### TTL on Agent-Written Aspirations

OpenClaw now has native homes for two kinds of future intention: the per-session `goal` (2026.5.31 and later) has an explicit lifecycle with pause, block, complete, and clear, and standing intents (`intent` tool, recent mainline) carry their own expiry, fire budget, and explicit cancellation. This skill does not put a TTL on either; they manage themselves. What remains is the third kind, which OpenClaw's own docs call an aspiration: "improve the release checklist this quarter", written into MEMORY.md, a topic file, or a goals or backlog section with no trigger and no clock.

Anything the agent writes as an aspiration gets a date stamp. If an agent-written aspiration is older than 14 days and the user hasn't touched it, the agent does not silently keep following it. Instead, ask the user whether it's still valid. Where the `intent` tool exists and the aspiration is really event-conditioned, offer to convert it into a standing intent so it gains a real expiry.

### TTL on Topic Files

Topic files represent active projects and workstreams. If a topic file hasn't been modified in 30 or more days, flag it for the user during the next provenance check: "The topic file for [project] hasn't been updated in a month. Is this still active, or should it be archived?" If the user confirms it's still active, update the file's timestamp. If the user says archive it, move it to `memory/topics/archive/` and remove the pointer from MEMORY.md.

This prevents stale topic files from accumulating and cluttering search results, and keeps MEMORY.md's routing table current.

### Instruction Diff Reports

On request (`/agent_provenance diff`, "diff report"), or as part of the optional weekly check: the agent diffs all instruction files against their state N days ago (default 7) and posts a summary to the conversation. What changed, who changed it (by commit tag, or "dreaming" for marked MEMORY.md entries), why. The user reviews, confirms, or reverts. Reports go to the conversation only, unless the user explicitly configures another destination. Where the `diffs` tool is available, the agent may attach a rendered diff for the largest change.

### Review Flagging with Graduated Urgency

Instruction files and key memory files should be reviewed periodically. Rather than a single flag, use graduated urgency:

**30 days since last review**: mention during the next provenance check. Example: "AGENTS.md hasn't been reviewed in 30 days. Worth a quick look when you have time."

**60 days since last review**: warn explicitly. Example: "AGENTS.md is 60 days past its last review. I'm still following its instructions, but they may be outdated. Can you review it this week?"

**90 days since last review**: escalate. Example: "AGENTS.md hasn't been reviewed in 90 days. At this point it's either stable enough to not need review (in which case, update the review date to acknowledge that) or it's drifted without anyone noticing. Please review and confirm."

This applies to human-authored and mixed files. Agent-authored files don't need the same review cadence but benefit from periodic user spot-checks. When the user confirms a review, `/agent_provenance review <file>` records it.

**Stale startup checklists.** A common finding on long-lived workspaces is an AGENTS.md whose startup steps reference files that no longer exist or moved: `memory/daily/`, `memory/working-buffer.md`, lowercase channel-named session files, `TOOLS.md` on a release that retired it. During a check, compare the startup steps against what is actually in the workspace and report each mismatch as a review item. Do not fix AGENTS.md yourself; show the user the replacement lines.

## Setup

If the workspace is not already a git repository (brand-new workspaces are initialized automatically when git is installed), initialize one and configure a local git identity for agent commits. Use a name that makes agent-authored commits identifiable in the log. Create a `.gitignore` if needed to exclude temporary files, secrets, and local state.

## Provenance Checks

Run a provenance check when the user asks for one (`/agent_provenance check`, "provenance check", "diff report"). A check covers:

1. Check last-reviewed dates in provenance headers of all instruction files
2. Apply graduated urgency: mention at 30 days, warn at 60, escalate at 90
3. Check for agent-written aspirations older than 14 days without user interaction; flag for re-authorization
4. Check for topic files untouched for 30 or more days; flag for archival or confirmation
5. Compare the AGENTS.md startup checklist against the actual workspace layout and report mismatches
6. Where available, list standing intents (`intent` list) and the current `/goal` status, so the user sees every live intention in one place; this skill reports them and does not change them
7. Generate the diff report

### Optional weekly check

From OpenClaw 2026.8.1, heartbeat no longer runs skill-defined tasks, so this skill does not rely on heartbeat on any version. If the user wants checks without asking, the agent may offer one weekly scheduled check. The rules for it:

- Ask first. Create the job only after the user explicitly agrees, and let the user choose the day and time.
- Before creating it, tell the user what it reads (the files listed in this skill's metadata), what it writes (nothing, apart from posting the report to the conversation), and where the report goes.
- Name it `agent-provenance weekly check`, and create only one.
- Tell the user how to manage it: `openclaw automations list --query agent-provenance` to find it, `openclaw automations disable <job-id>` to pause it, `openclaw automations remove <job-id>` to delete it. On releases before 2026.8.1, use `openclaw cron` in place of `openclaw automations`.
- Recurring jobs have no built-in expiry. The job runs until the user disables or removes it. If the user says to stop the checks, remove the job immediately.

## Security Implications

Provenance tracking provides defense in depth. It makes unauthorized changes visible in git history, enforces regular review of critical files, provides accountability for agent actions, and creates an audit trail for compliance. It is a review discipline, not an enforcement mechanism: an agent with unrestricted file tools can still edit any workspace file. For hard limits, pair this skill with `tools.fs.workspaceOnly`, sandboxing, the policy plugin's conformance checks, and agent-guidance for rules that must sit outside the writable workspace.

**Sensitive data:** Provenance headers and commit messages should never contain secrets, API keys, or credentials. Commit messages describe what changed and why; they should reference file names and decisions, not secret values. The same redaction guidance from agent-session-state applies: log the existence of a credential and where it is stored, not the value itself.

## Version notes

This skill is written for whichever OpenClaw release the user runs, including the monthly extended-stable lines (`2026.N.35`). Check `openclaw --version` once per session when a version-dependent instruction matters. Git-backed workspaces, provenance headers, and user-invocable skill commands work on every supported release. The policy plugin exists from 2026.5.20, the `/goal` command from 2026.5.31. From 2026.8.1: dreaming writes MEMORY.md by default, `openclaw memory forget` exists, the scheduler is `automations`, and HEARTBEAT.md is retired; by 2026.9.7 TOOLS.md is retired. The `intent` tool, personal USER files (2026.9.6), agent-guidance, and the `diffs` tool are recent mainline additions: detect them by presence rather than assuming them.

## Integration with Other Skills

**hierarchical-agent-memory** provides the memory structure this skill governs. MEMORY.md is a lean routing table with pointers to topic and contact files. Topic files are agent-authored and subject to the 30-day staleness check. Contact files are mixed authority. Daily notes and time-based archival layers are agent-authored and maintained freely. All memory file changes should use appropriate commit tags.

**agent-session-state** manages per-conversation session files. Session state files are agent-authored and transient. They don't need provenance headers or review cadence, but commits that modify them should use the appropriate tag for audit trail purposes.

**memory-wiki** (bundled OpenClaw plugin, enabled with `openclaw plugins enable memory-wiki`) compiles durable knowledge into a separate vault outside the workspace with its own lifecycle: structured claims, evidence linkage, freshness dashboards, `wiki_lint`, and the `reports/` dashboard set. This skill does not govern the wiki vault. Do not retrofit provenance headers, `last-reviewed` dates, graduated urgency, or commit-tag discipline onto wiki pages; wiki has its own claim-level schema and lint tooling, and the two systems are deliberately orthogonal (file authorship and accountability versus claim-level evidence lineage). Commits that touch wiki output should still use appropriate tags for audit trail purposes, but the pages themselves are out of scope.

**OpenClaw memory provenance** (`docs/concepts/memory-provenance.md` and `docs/concepts/memory-architecture.md`) records which sessions automatically ingested memories came from, classifies every indexed chunk by trust, and lets `openclaw memory forget` remove session-derived memories. That traces where memory content came from. This skill tracks who authored each workspace file and when it was last reviewed. They complement each other; use `openclaw memory forget` for deleting session-derived memories, and this skill's diff report for seeing what changed in the files.

## Best Practices

**For the agent:** Always include provenance headers on new instruction files and new topic/contact files. Update last-reviewed after the user reviews a file. Use appropriate commit tags and commit your own changes before any generic backup job runs. Flag old content for review using graduated urgency. Ask the user about stale aspirations. Flag untouched topic files for archival. Leave dreaming's MEMORY.md entries and USER.md's per-directive metadata alone.

**For the user:** Review flagged files promptly; graduated urgency means the agent will keep escalating until you respond. Update last-reviewed and reviewed-by after each review, or run `/agent_provenance review <file>`. Provide clear direction for changes explicitly requested. Periodically check git history for anomalies. When archiving a topic, confirm the MEMORY.md pointer is removed.

## Related Skills

- **hierarchical-agent-memory**: hybrid topic-based working memory with optional time-based archival layers
- **agent-session-state**: per-conversation session files and the WAL protocol
