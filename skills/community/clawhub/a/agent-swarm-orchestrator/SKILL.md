---
name: agent-swarm-orchestrator
description: Orchestrate OpenClaw Agent Swarm workflows for multi-project coding automation with Obsidian task intake, Claude coding, Codex review, GitLab MR flow, merge+sync, and done-status closure.
---

# Agent Swarm Orchestrator

Multi-project coding automation: Obsidian task intake → Claude Code → Codex review → GitLab MR → merge + sync.

## Architecture

```
Obsidian note (status: ready)
  → scan-obsidian.sh (cron 5min)
    → spawn-agent.sh
      ├── git worktree + branch
      ├── prompt file (task + context.md)
      └── tmux session → run-agent.sh
                            ├── claude -p "$PROMPT" | tee log
                            └── review-and-push.sh
                                  ├── codex review (graded)
                                  ├── push + glab mr create --yes
                                  └── notification → Telegram

merge-and-sync.sh (manual trigger)
  ├── glab mr merge <iid>
  ├── sync-project-main.sh (fast-forward local main)
  └── check-agents.sh (background) → mark done + send notification

check-agents.sh (cron 3min / called by merge-and-sync)
  ├── dead tmux + commits → trigger review
  ├── >60min → timeout notification
  └── MR merged → mark done in tasks.json + .notification → Telegram
```

## Core Paths

| Path | Purpose |
|------|---------|
| `~/agent-swarm/` | Control plane (scripts, registry, tasks) |
| `~/agent-swarm/registry.json` | Project configs (repo, paths, branch) |
| `~/agent-swarm/tasks.json` | Task state machine |
| `~/GitLab/repos/` | Local repos |
| `~/GitLab/worktrees/` | Per-task worktrees |
| `~/Documents/Obsidian Vault/agent-swarm/` | Task intake notes |

## Scripts

| Script | Purpose |
|--------|---------|
| `spawn-agent.sh` | Create worktree + prompt + tmux → run-agent |
| `run-agent.sh` | `claude -p` → check commits → trigger review |
| `review-and-push.sh` | Codex review → graded fix → push → MR |
| `check-agents.sh` | Cron + post-merge: detect done/stuck, mark done, send notification |
| `scan-obsidian.sh` | Parse Obsidian notes, spawn `status: ready` tasks |
| `send-notifications.sh` | Send `.notification` files via OpenClaw CLI |
| `merge-and-sync.sh` | Merge MR + sync local main |
| `sync-project-main.sh` | Fast-forward local repo to origin/main |
| `new-project.sh` | Initialize project (GitLab + registry + context + Obsidian) |
| `cleanup.sh` | Daily archive old tasks, clean worktrees/logs |

## Usage

### Spawn task
```bash
~/agent-swarm/scripts/spawn-agent.sh <project> "<task description>"
```

### Monitor
```bash
tmux attach -t agent-<task-id>        # live output
tail -f ~/agent-swarm/logs/<task-id>.log  # log file
```

### Merge and sync
```bash
~/agent-swarm/scripts/merge-and-sync.sh <project> <mr-iid>
```

### New project
```bash
~/agent-swarm/scripts/new-project.sh <project-name>
```

## Task Lifecycle

```
starting → running → [no-output | reviewing]
reviewing → [ready_to_merge | review-error | needs-manual-fix | fixing]
fixing → reviewing (retry, max 2)
ready_to_merge → done (auto on MR merged)
```

## Prerequisites

### Claude Code CLI
- Authenticated via OAuth (`~/.claude.json` oauthAccount)
- `~/.claude/settings.json`: `skipDangerousModePermissionPrompt: true`
- `~/.claude.json` projects: trust `~/GitLab/worktrees` and `~/GitLab/repos` (`hasTrustDialogAccepted: true`)
- No `ANTHROPIC_*` env vars leaking into tmux (causes proxy conflicts)

### Tools
- `claude` CLI (Claude Code)
- `codex` CLI (OpenAI Codex, for review)
- `glab` CLI (GitLab)
- `jq`, `python3`, `tmux`

### Cron
```
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
*/3 * * * * ~/agent-swarm/scripts/check-agents.sh
*/5 * * * * ~/agent-swarm/scripts/scan-obsidian.sh
0 3 * * * ~/agent-swarm/scripts/cleanup.sh
```

### Notifications

Configure in `~/agent-swarm/registry.json`:
```json
{
  "notifyMethod": "openclaw",
  "notifyChannel": "telegram",
  "notifyTarget": "<chat_id>"
}
```

`swarm_notify()` in `config.sh` reads these values and calls:
```bash
openclaw message send --channel telegram --target <chat_id> --message "..."
```

⚠️ Do NOT use `>/dev/null 2>&1` in `swarm_notify` — errors must be visible so failed sends are not silently marked as sent.

## Prompt Template

Each task gets a prompt file with:
1. Project name, task description, priority
2. Working directory and branch
3. Project context (from `context.md`)
4. Standard instructions (commit, push, MR, update context.md if architectural changes)

## Obsidian Integration

- Frontmatter `status: active | stop` controls project scanning
- Task block: `### Task Name` + `status: ready` + `> description`
- `### INIT_PROJECT` + `status: ready` triggers `new-project.sh`
- Dedup: sha1(project+name+desc)[:12], flagged in logs
- Debounce: skip files modified within last 1 minute

## Review Policy

- **Coding**: Claude Code (`-p` mode, auto-exit)
- **Review**: Codex (`codex exec review`)
- **CRITICAL/HIGH**: auto-fix retry (max 2), then `needs-manual-fix`
- **MEDIUM**: auto-fix (non-blocking), skip for docs-only
- **LOW**: notes in MR description only
- **Docs-only**: downgrade CRITICAL/HIGH to MEDIUM

## Portable Install

```bash
mkdir -p ~/agent-swarm/{scripts,logs,projects}
cp -f <skill_dir>/scripts/*.sh ~/agent-swarm/scripts/
chmod +x ~/agent-swarm/scripts/*.sh
echo '{"projects":{}}' > ~/agent-swarm/registry.json
echo '{"tasks":[]}' > ~/agent-swarm/tasks.json
```

Then: register projects in `registry.json`, set cron, configure notifications.

## Intent → Action Mapping

When a user message matches one of these intents, take the corresponding action immediately without asking for confirmation:

| User says | Context | Action |
|-----------|---------|--------|
| "合并" / "merge" / "merge it" | Replied to a PR_READY notification | Extract `<project>` and `<mr-iid>` from the notification, run `merge-and-sync.sh <project> <mr-iid>` |
| "起任务" / "spawn" / "新任务" | With a task description | Run `spawn-agent.sh <project> "<desc>"` |
| "查状态" / "check status" | Any | Run `check-agents.sh` and summarize output |
| "新项目" / "new project" | With a project name | Run `new-project.sh <project-name>` |

### Extracting MR info from PR_READY notifications

PR_READY notifications follow this format:
```
✅ PR_READY
Project: <project>
Task: <desc>
Task ID: <task-id>
Branch: <branch>
MR: https://gitlab.com/.../-/merge_requests/<mr-iid> | Review ...
```

Extract `Project` → `<project>`, and the number at the end of the MR URL → `<mr-iid>`.

## Guardrails

### You are the dispatcher, not the analyst

When a user reports an issue or requests a change to project code:

- ❌ Do NOT read project source code to analyze
- ❌ Do NOT diagnose root causes yourself
- ❌ Do NOT design technical solutions
- ✅ Understand the user's intent and translate it into a clear task description
- ✅ Pass user feedback verbatim to the agent (e.g. "tiles didn't get bigger")
- ✅ Spawn the task, monitor progress, merge MRs, maintain the swarm system

The coding agent runs in a full worktree with complete project context — it is better positioned to read code, diagnose issues, and implement fixes than you are from a chat session.

### Other rules

- Do not edit project code directly — always go through spawn-agent
- Push-first + cron-fallback notification design
- State names: `done`, `ready_to_merge`, `review-error`, `needs-manual-fix`
- Context.md auto-update for new features, gameplay changes, and architectural changes (skip trivial config/formatting)
