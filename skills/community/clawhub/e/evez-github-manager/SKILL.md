---
name: evez-github-manager
description: Manage GitHub repositories, pull requests, issues, and workflows from OpenClaw. Use when reviewing PRs, managing issues, automating GitHub Actions, syncing repos, or coordinating multi-repo workflows. Covers PR review automation, issue triage, branch management, and release coordination.
---

# GitHub PR Manager

Manage GitHub repos, PRs, and issues directly from OpenClaw.

## Quick Start

```bash
python3 scripts/github_manager.py prs --repo EvezArt/evez-api
python3 scripts/github_manager.py issues --repo EvezArt/clawbreak
python3 scripts/github_manager.py review --repo EvezArt/evez-api --pr 42
```

## Features

- **PR Management**: List, review, merge, comment on PRs
- **Issue Triage**: List, label, assign, close issues
- **Branch Management**: List, create, delete branches
- **Release Coordination**: Create releases, upload assets
- **Workflow Status**: Check GitHub Actions run status
- **Multi-Repo Sync**: Apply changes across multiple repos

## Auth

Requires `GITHUB_TOKEN` env var. Get one at https://github.com/settings/tokens

Or use Composio integration (already configured).
