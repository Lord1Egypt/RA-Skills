---
name: "dr-agent-backup"
description: "Backup and restore Daniel agents with git."
---

# DR. Agent Backup

Use when setting up, auditing, repairing, or restoring backup continuity for a Daniel-owned agent.

Goal: agent memory and workspace state should survive VM loss or migration. Restore should be boring: clone/pull the repo, restore secrets separately, verify the agent starts, and reindex memory if needed.

## Core Policy

1. Back up agent-owned workspace files to a Daniel-owned Azure DevOps git repository.
2. Commit after meaningful memory or workspace changes.
3. Never commit secrets, tokens, local credential stores, runtime logs, caches, databases, or bulky generated state unless explicitly approved.
4. Treat git as continuity for human-readable source of truth, not a full machine image.
5. Secrets and auth must be restored through the proper secret manager, env file, or provider login flow.

## What To Track

Default include list:

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `TOOLS.md`
- `MEMORY.md`
- `HEARTBEAT.md` when present
- `memory/**/*.md`
- `memory/**/*.json` only when it is intentional durable state
- `context_pipeline/**`
- `automation/**` excluding runtime outputs and secrets
- `skills/**` for workspace-local skills
- `doc_reviews/**` when used as active review state
- Project notes and templates Daniel expects to restore

Default exclude list:

- API keys, tokens, passwords, OAuth files, cookies, auth profiles
- `.env`, `*.env`, `gateway.systemd.env`, and backups of env files
- SQLite databases and WAL/SHM files unless explicitly approved
- `node_modules/`, package caches, build outputs
- raw session transcripts unless Daniel explicitly wants them tracked
- inbound/outbound media files unless intentionally curated
- temporary files, logs, downloads, generated archives

## Setup Workflow

1. Confirm the Azure DevOps organization, project, and repo name.
2. Confirm credential method:
   - SSH deploy key
   - Azure DevOps PAT stored outside git
   - existing authenticated git credential helper
3. Initialize or connect the workspace repo.
4. Add a `.gitignore` that blocks secrets and runtime state.
5. Run a dry-run status review before the first commit.
6. Make the initial commit with a clear message.
7. Push to Azure DevOps.
8. Record the repo URL and restore notes in local memory or an approved ops file.

## Commit Policy

Commit after meaningful changes to:

- long-term memory
- daily memory logs that contain decisions or restore-relevant facts
- agent instructions or identity files
- automation manifests and scripts
- local skills or proposal-derived workflow files
- context pipeline files
- important operational notes

Do not commit after every tiny transient log line if it adds noise. Batch related memory edits when they happen in one task.

Recommended commit message style:

```text
memory: capture gateway restore and embedding fix
agent: update baseline behavior notes
backup: add Azure DevOps restore procedure
skill: revise agent baseline proposal
```

## Before Commit Checklist

Run these checks before committing:

1. `git status --short`
2. Inspect changed files.
3. Check that no secret-bearing files are staged.
4. If adding `.gitignore`, confirm it covers known OpenClaw secrets and runtime state.
5. Commit only intentional files.

If a secret appears staged, stop and unstage it. Do not rely on later cleanup.

## Restore Workflow

1. Install OpenClaw and baseline system packages.
2. Clone the Azure DevOps repo into the expected workspace path.
3. Restore secret files/env/auth using the approved secret path, not git.
4. Install/enable required plugins and skills.
5. Verify gateway service and lingering if this is a Linux user service.
6. Run memory status and reindex if needed:

```bash
openclaw memory status --index
openclaw memory index --force
```

7. Verify channels and delivery targets.
8. Run a small end-to-end DM test.
9. Commit any restore-specific notes that are useful for next time.

## Agent Behavior

Agents should run safe git checks and commits themselves when they have access.

Ask Daniel before:

- creating a new Azure DevOps repo
- adding credentials or PATs
- pushing to a new remote for the first time
- changing access controls
- committing files that may contain private/customer data beyond normal memory notes
- deleting history or rewriting commits

## Audit Workflow

For an existing agent, audit backup health by checking:

- Is the workspace a git repo?
- Is the remote Azure DevOps and reachable?
- Is `.gitignore` strong enough?
- Are there uncommitted memory/workspace changes?
- When was the last successful push?
- Are secrets absent from tracked files?
- Is there a documented restore path?

Report the result as:

- status
- risks
- next action

Keep it short unless Daniel asks for full detail.

## Boundaries

This skill does not replace VM snapshots or system-level backups. It protects the agent's durable working memory and configuration source, not every runtime artifact.

This skill does not store secrets in git.
