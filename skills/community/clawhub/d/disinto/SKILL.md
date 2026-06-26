---
name: disinto
description: >-
  Operate the disinto autonomous code factory. Use when managing factory agents,
  filing issues on the forge, reading agent journals, querying CI pipelines,
  checking the dependency graph, or inspecting factory health.
license: AGPL-3.0
metadata:
  author: johba
  version: "0.1.1"
env_vars:
  required:
    - FORGE_TOKEN
    - FORGE_API
    - PROJECT_REPO_ROOT
  optional:
    - WOODPECKER_SERVER
    - WOODPECKER_TOKEN
    - WOODPECKER_REPO_ID
tools:
  - bash
  - curl
  - jq
  - git
---

# Disinto Factory Skill

Disinto is an autonomous code factory with nine agents that implement issues,
review PRs, plan from a vision, predict risks, groom the backlog, gate
actions, and assist the founder — all driven by cron and Claude.

## Required environment

| Variable | Purpose |
|----------|---------|
| `FORGE_TOKEN` | Forgejo/Gitea API token with repo scope |
| `FORGE_API` | Base API URL, e.g. `https://forge.example/api/v1/repos/owner/repo` |
| `PROJECT_REPO_ROOT` | Absolute path to the checked-out disinto repository |

Optional:

| Variable | Purpose |
|----------|---------|
| `WOODPECKER_SERVER` | Woodpecker CI base URL (for pipeline queries) |
| `WOODPECKER_TOKEN` | Woodpecker API bearer token |
| `WOODPECKER_REPO_ID` | Numeric repo ID in Woodpecker |

## The nine agents

| Agent | Role | Runs via |
|-------|------|----------|
| **Dev** | Picks backlog issues, implements in worktrees, opens PRs | `dev/dev-poll.sh` (cron) |
| **Review** | Reviews PRs against conventions, approves or requests changes | `review/review-poll.sh` (cron) |
| **Gardener** | Grooms backlog: dedup, quality gates, dust bundling, stale cleanup | `gardener/gardener-run.sh` (cron 0,6,12,18 UTC) |
| **Planner** | Tracks vision progress, maintains prerequisite tree, files constraint issues | `planner/planner-run.sh` (cron daily 07:00 UTC) |
| **Predictor** | Challenges claims, detects structural risks, files predictions | `predictor/predictor-run.sh` (cron daily 06:00 UTC) |
| **Supervisor** | Monitors health (RAM, disk, CI, agents), auto-fixes, escalates | `supervisor/supervisor-run.sh` (cron */20) |
| **Action** | Executes operational tasks dispatched by planner via formulas | `action/action-poll.sh` (cron) |
| **Vault** | Gates dangerous actions, manages resource procurement | `vault/vault-poll.sh` (cron) |
| **Exec** | Interactive executive assistant reachable via Matrix | `exec/exec-session.sh` |

### How agents interact

```
Planner ──creates-issues──▶ Backlog ◀──grooms── Gardener
   │                           │
   │                           ▼
   │                     Dev (implements)
   │                           │
   │                           ▼
   │                     Review (approves/rejects)
   │                           │
   │                           ▼
   ▼                        Merged
Predictor ──challenges──▶ Planner (triages predictions)
Supervisor ──monitors──▶ All agents (health, escalation)
Vault ──gates──▶ Action, Dev (dangerous operations)
Exec ──delegates──▶ Issues (never writes code directly)
```

### Issue lifecycle

`backlog` → `in-progress` → PR → CI → review → merge → closed.

Key labels: `backlog`, `priority`, `in-progress`, `blocked`, `underspecified`,
`tech-debt`, `vision`, `action`, `prediction/unreviewed`.

Issues declare dependencies in a `## Dependencies` section listing `#N`
references. Dev-poll only picks issues whose dependencies are all closed.

## Available scripts

- **`scripts/factory-status.sh`** — Show agent status, open issues, and CI
  pipeline state. Pass `--agents`, `--issues`, or `--ci` for specific sections.
- **`scripts/file-issue.sh`** — Create an issue on the forge with proper labels
  and formatting. Pass `--title`, `--body`, and optionally `--labels`.
- **`scripts/read-journal.sh`** — Read agent journal entries. Pass agent name
  (`planner`, `supervisor`, `exec`) and optional `--date YYYY-MM-DD`.

## Common workflows

### 1. Check factory health

```bash
bash scripts/factory-status.sh
```

This shows: which agents are active, recent open issues, and CI pipeline
status. Use `--agents` for just the agent status section.

### 2. Read what the planner decided today

```bash
bash scripts/read-journal.sh planner
```

Returns today's planner journal: predictions triaged, prerequisite tree
updates, top constraints, issues created, and observations.

### 3. File a new issue

```bash
bash scripts/file-issue.sh --title "fix: broken auth flow" \
  --body "$(cat scripts/../templates/issue-template.md)" \
  --labels backlog
```

Or generate the body inline — the template shows the expected format with
acceptance criteria and affected files sections.

### 4. Check the dependency graph

```bash
python3 "${PROJECT_REPO_ROOT}/lib/build-graph.py" \
  --project-root "${PROJECT_REPO_ROOT}" \
  --output /tmp/graph-report.json
cat /tmp/graph-report.json | jq '.analyses'
```

The graph builder parses VISION.md, the prerequisite tree, formulas, and open
issues. It detects: orphan issues (not referenced), dependency cycles,
disconnected clusters, bottleneck nodes, and thin objectives.

### 5. Query a specific CI pipeline

```bash
bash scripts/factory-status.sh --ci
```

Or query Woodpecker directly:

```bash
curl -s -H "Authorization: Bearer ${WOODPECKER_TOKEN}" \
  "${WOODPECKER_SERVER}/api/repos/${WOODPECKER_REPO_ID}/pipelines?per_page=5" \
  | jq '.[] | {number, status, commit: .commit[:8], branch}'
```

### 6. Read and interpret VISION.md progress

Read `VISION.md` at the repo root for the full vision. Then cross-reference
with the prerequisite tree:

```bash
cat "${PROJECT_REPO_ROOT}/planner/prerequisite-tree.md"
```

The prerequisite tree maps vision objectives to concrete issues. Items marked
`[x]` are complete; items marked `[ ]` show what blocks progress. The planner
updates this daily.

## Gotchas

- **Single-threaded pipeline**: only one issue is in-progress per project at a
  time. Don't file issues expecting parallel work.
- **Secrets via env vars only**: never embed secrets in issue bodies, PR
  descriptions, or comments. Use `$VAR_NAME` references.
- **Formulas are not skills**: formulas in `formulas/` are TOML issue templates
  for multi-step agent tasks. Skills teach assistants; formulas drive agents.
- **Predictor journals**: the predictor does not write journal files. Its memory
  lives in `prediction/unreviewed` and `prediction/actioned` issues.
- **State files**: agent activity is tracked via `state/.{agent}-active` files.
  These are presence files, not logs.
- **ShellCheck required**: all `.sh` files must pass ShellCheck. CI enforces this.
