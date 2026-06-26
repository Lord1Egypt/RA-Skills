---
name: autonomous-github-team
description: >
  Autonomous GitHub Team — 41 AI agents that autonomously monitor a GitHub repository, detect bugs,
  create fixes, open PRs, and release to production. Triggers on: "run GitHub agents", "autonomous dev team",
  "automated bug fixing", "AI code review", "GitHub workflow automation", "CI/CD automation".

  ⚠️ SECURITY: Requires a GitHub PAT with write access. Clones and executes third-party scripts.
  See "Security Notes" below before installing.
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "primaryEnv": ["GH_TOKEN", "TARGET_REPO"],
        "requires":
          {
            "bins": ["git", "bash", "curl", "python3"],
            "env": ["GH_TOKEN", "TARGET_REPO"],
          },
        "install":
          [
            {
              "id": "clone",
              "kind": "clone",
              "label": "Clone Autonomous GitHub Team repo",
              "command": "git clone https://github.com/captainsvbot/AutonomousGitHubTeam.git /path/to/autonomous-github-team",
              "pinnedRef": "v1.0.0",
              "note": "Clone is pinned to a specific release tag. Always review the tagged commit before running.",
            },
          ],
        "permissions": ["github_repo_write", "github_pr_write", "github_issues_write"],
        "risk_level": "high",
      },
  }
---

# 🤖 Autonomous GitHub Team Skill

> **⚠️ Security Warning — Read Before Installing**
>
> This skill clones and executes bash scripts from a remote repository. Before running:
> 1. **Audit the scripts first** — review every agent file in the `agents/` directory
> 2. **Use a least-privilege PAT** — dedicated token scoped to a single test repo, not your main account
> 3. **Never run on a production repo** until you've tested in an isolated fork
> 4. **Never commit tokens** — keep `config.env` private and out of version control
> 5. **Require human review** before merging any PRs the agents create

## What It Does

41 AI agents that autonomously monitor a GitHub repository, detect bugs, create fixes, open PRs, and release to production automatically.

## Required Environment Variables

```bash
GH_TOKEN        # GitHub PAT — needs: contents:w, pr:w, issues:w
TARGET_REPO     # The repository to operate on (format: owner/repo)
```

**Primary credential:** `GH_TOKEN` — treat this as a high-privilege secret.

## Setup

```bash
# 1. Clone the repo (pinned to v1.0.0 tag)
git clone --branch v1.0.0 https://github.com/captainsvbot/AutonomousGitHubTeam.git
cd autonomous-github-team

# 2. Configure — edit config.env
cp config.example.env config.env
nano config.env   # set GH_TOKEN and TARGET_REPO

# 3. Audit the agents first (important!)
# Review agents/*.sh before running anything

# 4. Run
bash agents/orchestrator.sh
```

## Security Requirements for the GitHub Token

The skill needs a token that can:
- Read and write to repository contents
- Create and manage pull requests
- Read and write issues

**Create a dedicated token for this skill:**
1. GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens
2. Scope to **only the specific repository** you want the team to operate on
3. Grant only: `contents: read and write`, `pull requests: read and write`, `issues: read and write`
4. **Never** use your main account token with broad org access

## Available Agents

```bash
bash agents/orchestrator.sh          # Full pipeline (detect → fix → release)
bash agents/security-agent.sh        # Vulnerability scanning
bash agents/fixer-agent.sh          # Apply fixes, open PRs
bash agents/git-guardian-agent.sh     # Merge PRs (requires human review before main merges)
bash agents/backup-agent.sh          # Backup repo via GitHub API
bash agents/rollback-agent.sh         # Auto-revert broken commits
bash agents/team-bravo.sh            # Activity monitor (read-only check)
```

## Gitflow

```
feature/fix → develop → main
```

Every run syncs `main → develop` first. The Git Guardian does not auto-merge to `main` — all merges to `main` require human approval.

## Before Running on a Production Repo

- [ ] Clone and review all `agents/*.sh` files
- [ ] Test in an isolated fork first
- [ ] Set up branch protection on `main` (require PR reviews)
- [ ] Use a dedicated, scope-limited PAT
- [ ] Keep `config.env` out of version control

## Security Checklist Before Publishing Changes

```bash
# Scan for accidentally committed secrets
grep -rni "gho_\|token\|secret\|api_key\|password" .
```

If you modify this repo, always scan before pushing publicly.
