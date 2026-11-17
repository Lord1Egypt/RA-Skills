---
name: "dr-agent-backup"
description: "Set up, audit, repair, or restore a six-hour Azure DevOps workspace backup."
---

# DR. Agent Backup

Use when setting up, auditing, repairing, or restoring backup continuity for a Daniel-owned agent.

## Outcome

One deterministic, non-LLM systemd user timer is the only process allowed to commit and push workspace backups. Every six hours it stages safe restore-relevant files, commits when needed, and pushes to the approved Azure DevOps remote. A failed run invokes one rate-limited failure notifier. Conversational agents and health checks never run an independent `git push`.

## Required design

1. Use Pattern B1: a manifest-backed runner, not an agent/LLM or OpenClaw cron.
2. Use one `systemd --user` timer with `OnBootSec=5min`, `OnUnitActiveSec=6h`, `AccuracySec=5min`, and `Persistent=true`.
3. Make the runner load its manifest and credential contract at run time, set `GIT_TERMINAL_PROMPT=0`, and use the approved askpass helper.
4. Stage only allowlisted restore-relevant paths. Exclude credentials, env files, auth profiles, databases, logs, caches, media, raw transcripts, dreaming/reflection output, temporary/download/archive files, generated artifacts, and state migrations.
5. Scan staged names and text for high-risk credential patterns before committing.
6. Commit only intentional staged changes, push the approved existing remote and branch, write a local ledger outside Git, and exit non-zero on any credential, staging, commit, remote, or push failure.
7. Wire `OnFailure=` to one deterministic notifier. It sends an immediate concise failure message, suppresses identical repeats for 24 hours, and never sends success messages.
8. Do not run a scheduled health monitor by default. Add one only when its distinct detection value is documented and it cannot push or commit.

## Ownership rule

The backup runner exclusively owns routine Git commit/push for the workspace. Agents may edit approved durable files but must leave them for the next runner. Do not use plain `git push` from an agent runtime; it does not inherit the runner's credential contract and creates false backup failures.

## Preflight

Before enabling or manually running a new or repaired runner:

1. Confirm the existing approved Azure DevOps remote, branch, credential method, and valid provider target for failure notifications.
2. Inspect `git status --short` and classify each restore-relevant dirty path as intentional durable content, intentional deletion, generated/runtime artifact, or unresolved.
3. Keep raw session exports and state-migration artifacts untracked; do not broadly exclude curated daily memory files.
4. Refuse to arm a runner over unresolved or sensitive content. Correct the manifest, exclusions, or worktree first.
5. Verify the credential file exists with mode `600`, required key names are present without exposing values, and the askpass helper is executable.

## Setup and repair

1. Audit the existing manifest, runner, installed service/timer, failure handler, Git remote/branch, and worktree.
2. Create or repair the manifest, runner, local ledger, service, timer, failure notifier, and focused tests.
3. Validate JSON, Python/shell syntax, unit rendering, and `systemd-analyze --user verify`.
4. Dry-run notification rendering without live delivery.
5. Run one real backup after preflight is clean; verify its commit/push, ledger, and remote alignment.
6. Install and enable the timer; verify it is enabled/active and has a next trigger.
7. Retire duplicate backup timers, health checks, or agent-driven push paths after confirming the new owner is live.

## Default tracked scope

Include: `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md` when present, `MEMORY.md`, comments-only `HEARTBEAT.md`, curated `memory/**/*.md` and intentional durable JSON, `context_pipeline/**`, `automation/**` excluding runtime output, workspace-local `skills/**`, and active `doc_reviews/**/*.md`.

## Approval boundaries

Ask Daniel before creating a repo or remote, changing credentials/PATs or access controls, using a new notification target or changing its cooldown, committing sensitive/customer data, deleting history, or rewriting commits.

## Shared release

This is a shared fleet skill. Follow the shared-skill source-of-truth rule in `dr-agent-baseline`: after a behavior change, publish a new ClawHub version, verify the registry resolves it, then install/apply that exact release on each in-scope agent. Do not present a local Workshop or workspace revision as canonical.

## Completion evidence

Report the runner and timer state, next trigger, real commit/push and remote alignment, notification policy, tracked/excluded scope, validation results, and any limitation. For a skill revision, also report the ClawHub version and verified fleet-application status. This skill does not replace VM snapshots or system backups.
