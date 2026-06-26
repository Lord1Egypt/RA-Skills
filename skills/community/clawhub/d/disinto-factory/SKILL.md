---
name: disinto-factory
description: Set up and operate a disinto autonomous code factory. Use when bootstrapping a new factory instance, checking on agents and CI, managing the backlog, or troubleshooting the stack.
license: AGPL-3.0
metadata:
  author: johba
  version: "0.2.1"
  repository: https://github.com/disinto/disinto
  homepage: https://disinto.ai
---

# Disinto Factory

You are helping the user set up and operate a **disinto autonomous code factory** — a system
of bash scripts and Claude CLI that automates the full development lifecycle: picking up
issues, implementing via Claude, creating PRs, running CI, reviewing, merging, and mirroring.

## First-time setup

Walk the user through these steps interactively. Ask questions where marked with [ASK].

### 1. Environment

[ASK] Where will the factory run? Options:
- **LXD container** (recommended for isolation) — need Debian 12, Docker, nesting enabled
- **Bare VM or server** — need Debian/Ubuntu with Docker
- **Existing container** — check prerequisites

Verify prerequisites:
```bash
docker --version && git --version && jq --version && curl --version && tmux -V && python3 --version && claude --version
```

Any missing tool — help the user install it before continuing.

### 2. Clone and init

```bash
git clone https://codeberg.org/johba/disinto.git && cd disinto
```

[ASK] What repo should the factory develop? Options:
- **Itself** (self-development): `bin/disinto init https://codeberg.org/johba/disinto --yes --repo-root $(pwd)`
- **Another project**: `bin/disinto init <repo-url> --yes`

Run the init and watch for:
- All bot users created (dev-bot, review-bot, etc.)
- `WOODPECKER_TOKEN` generated and saved
- Stack containers all started

### 3. Post-init verification

Run this checklist — fix any failures before proceeding:

```bash
# Stack healthy?
docker ps --format "table {{.Names}}\t{{.Status}}"
# Expected: forgejo, woodpecker (healthy), woodpecker-agent (healthy), agents, edge, staging

# Token generated?
grep WOODPECKER_TOKEN .env | grep -v "^$" && echo "OK" || echo "MISSING — see references/troubleshooting.md"

# Agent cron active?
docker exec -u agent disinto-agents-1 crontab -l -u agent

# Agent can reach Forgejo?
docker exec disinto-agents-1 bash -c "source /home/agent/disinto/.env && curl -sf http://forgejo:3000/api/v1/version | jq .version"

# Agent repo cloned?
docker exec -u agent disinto-agents-1 ls /home/agent/repos/
```

If the agent repo is missing, clone it:
```bash
docker exec disinto-agents-1 chown -R agent:agent /home/agent/repos
docker exec -u agent disinto-agents-1 bash -c "source /home/agent/disinto/.env && git clone http://dev-bot:\${FORGE_TOKEN}@forgejo:3000/<org>/<repo>.git /home/agent/repos/<name>"
```

### 4. Mirrors (optional)

[ASK] Should the factory mirror to external forges? If yes, which?
- GitHub: need repo URL and SSH key added to GitHub account
- Codeberg: need repo URL and SSH key added to Codeberg account

Show the user their public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

Test SSH access:
```bash
ssh -T git@github.com 2>&1; ssh -T git@codeberg.org 2>&1
```

If SSH host keys are missing: `ssh-keyscan github.com codeberg.org >> ~/.ssh/known_hosts 2>/dev/null`

Edit `projects/<name>.toml` to add mirrors:
```toml
[mirrors]
github   = "git@github.com:Org/repo.git"
codeberg = "git@codeberg.org:user/repo.git"
```

Test with a manual push:
```bash
source .env && source lib/env.sh && export PROJECT_TOML=projects/<name>.toml && source lib/load-project.sh && source lib/mirrors.sh && mirror_push
```

### 5. Seed the backlog

[ASK] What should the factory work on first? Brainstorm with the user.

Help them create issues on the local Forgejo. Each issue needs:
- A clear title prefixed with `fix:`, `feat:`, or `chore:`
- A body describing what to change, which files, and any constraints
- The `backlog` label (so the dev-agent picks it up)

```bash
source .env
BACKLOG_ID=$(curl -sf "http://localhost:3000/api/v1/repos/<org>/<repo>/labels" \
  -H "Authorization: token $FORGE_TOKEN" | jq -r '.[] | select(.name=="backlog") | .id')

curl -sf -X POST "http://localhost:3000/api/v1/repos/<org>/<repo>/issues" \
  -H "Authorization: token $FORGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"<title>\", \"body\": \"<body>\", \"labels\": [$BACKLOG_ID]}"
```

For issues with dependencies, add `Depends-on: #N` in the body — the dev-agent checks
these before starting.

Use labels:
- `backlog` — ready for the dev-agent
- `blocked` — parked, not for the factory
- No label — tracked but not for autonomous work

### 6. Watch it work

The dev-agent polls every 5 minutes. Trigger manually to see it immediately:
```bash
docker exec -u agent disinto-agents-1 bash -c "cd /home/agent/disinto && bash dev/dev-poll.sh projects/<name>.toml"
```

Then monitor:
```bash
# Watch the agent work
docker exec disinto-agents-1 tail -f /home/agent/data/logs/dev/dev-agent.log

# Check for Claude running
docker exec disinto-agents-1 bash -c "for f in /proc/[0-9]*/cmdline; do cmd=\$(tr '\0' ' ' < \$f 2>/dev/null); echo \$cmd | grep -q 'claude.*-p' && echo 'Claude is running'; done"
```

## Ongoing operations

### Check factory status

```bash
source .env

# Issues
curl -sf "http://localhost:3000/api/v1/repos/<org>/<repo>/issues?state=open" \
  -H "Authorization: token $FORGE_TOKEN" \
  | jq -r '.[] | "#\(.number) [\(.labels | map(.name) | join(","))] \(.title)"'

# PRs
curl -sf "http://localhost:3000/api/v1/repos/<org>/<repo>/pulls?state=open" \
  -H "Authorization: token $FORGE_TOKEN" \
  | jq -r '.[] | "PR #\(.number) [\(.head.ref)] \(.title)"'

# Agent logs
docker exec disinto-agents-1 tail -20 /home/agent/data/logs/dev/dev-agent.log
```

### Check CI

```bash
source .env
WP_CSRF=$(curl -sf -b "user_sess=$WOODPECKER_TOKEN" http://localhost:8000/web-config.js \
  | sed -n 's/.*WOODPECKER_CSRF = "\([^"]*\)".*/\1/p')
curl -sf -b "user_sess=$WOODPECKER_TOKEN" -H "X-CSRF-Token: $WP_CSRF" \
  "http://localhost:8000/api/repos/1/pipelines?page=1&per_page=5" \
  | jq '.[] | {number, status, event}'
```

### Unstick a blocked issue

When a dev-agent run fails (CI timeout, implementation error), the issue gets labeled `blocked`:

1. Close stale PR and delete the branch
2. `docker exec disinto-agents-1 rm -f /tmp/dev-agent-*.json /tmp/dev-agent-*.lock`
3. Relabel the issue to `backlog`
4. Update agent repo: `docker exec -u agent disinto-agents-1 bash -c "cd /home/agent/repos/<name> && git fetch origin && git reset --hard origin/main"`

### Access Forgejo UI

If running in an LXD container with reverse tunnel:
```bash
# From your machine:
ssh -L 3000:localhost:13000 user@jump-host
# Open http://localhost:3000
```

Reset admin password if needed:
```bash
docker exec disinto-forgejo-1 su -c "forgejo admin user change-password --username disinto-admin --password <new-pw> --must-change-password=false" git
```

## Important context

- Read `AGENTS.md` for per-agent architecture and file-level docs
- Read `VISION.md` for project philosophy
- The factory uses a single internal Forgejo as its forge, regardless of where mirrors go
- Dev-agent uses `claude -p --resume` for session continuity across CI/review cycles
- Mirror pushes happen automatically after every merge (fire-and-forget)
- Cron schedule: dev-poll every 5min, review-poll every 5min, gardener 4x/day
