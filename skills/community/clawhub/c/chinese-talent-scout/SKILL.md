---
name: chinese-talent-scout
description: >
  Discover, score, and monitor Chinese GitHub developers with GitHub signals,
  rule-based processing, optional OpenClaw AI evaluation, shortlist queries,
  cron management, workspace export, and controlled config-change requests.
license: MIT
compatibility: Requires Node.js 22+, gh CLI, openclaw CLI, internet access to GitHub/OpenClaw, and a local workspace-data directory. Channel delivery and AI evaluation depend on OpenClaw-side accounts and provider credentials configured outside this skill.
metadata:
  author: presence-io
  repository: https://github.com/presence-io/talent-scout
  entrypoint: scripts/talent-scout.sh
  security-reference: references/security.md
  credentials-reference: references/credentials.md
---

# Chinese Talent Scout Skill

Unified skill entry for the AI Talent Scout system. This skill exposes collection,
processing, evaluation, and querying capabilities through a single command surface,
suitable for OpenClaw agent scheduling and ClawHub distribution.

Run commands through `scripts/talent-scout.sh <command> ...`.

## Safety Summary

- GitHub collection is executed through the local `gh` CLI. This skill does not parse or store GitHub tokens itself.
- AI evaluation, channel delivery, and cron operations are delegated to the local `openclaw` CLI. Provider credentials and channel accounts are managed by OpenClaw, not embedded in this skill.
- `config request` sends only a relative config reference (`workspace-data/talents.yaml`) plus the requested change. It does not send absolute local filesystem paths.
- `export workspace` creates a local ZIP and prints its path. It does not upload files or send attachments by itself.

See [Security Notes](references/security.md) and [Credential Model](references/credentials.md) before publishing or installing in production.

## Commands

### Pipeline

- **collect** — Run data collection from GitHub signals, community repos, and stargazers.
- **process** — Merge, deduplicate, identify, and score collected candidates.
- **evaluate** — Run AI-assisted evaluation on processed candidates.
- **pipeline** — Run the full collect → process → evaluate pipeline.

### Query

- **query shortlist** — List the current shortlist of evaluated candidates.
- **query candidate `<username>`** — Show details for a specific candidate.
- **query stats** — Show run statistics and distributions.

### Config

- **config request** — Send a channel message asking AI to update `workspace-data/talents.yaml` without disclosing absolute local paths.

### Export

- **export workspace** — Package the current `workspace-data/` directory as a ZIP and return the local archive path.

### Cron

- **cron status** — Show configured cron jobs.
- **cron sync** — Sync cron jobs to OpenClaw.
- **cron runs** — Show recent OpenClaw cron run history.
- **cron run `<name>`** — Show details for a specific cron run.
- **cron disable `<name>`** — Disable a cron job.
- **cron enable `<name>`** — Enable a cron job.

## Data Flow

```
GitHub API → data-collector → output/raw/
  → data-processor → output/processed/
  → ai-evaluator → output/evaluated/
  → dashboard / skills query
```

## Configuration

Mutable workspace configuration lives in `workspace-data/talents.yaml`.
The file is seeded from the packaged template on first use.

Do not store long-lived secrets in `workspace-data/talents.yaml`. `export workspace`
packages that file into the local archive it creates.

## References

- [Architecture](references/architecture.md)
- [Credential Model](references/credentials.md)
- [Data Sources](references/data-sources.md)
- [Identity Detection](references/identity.md)
- [Evaluation Model](references/evaluation.md)
- [Security Notes](references/security.md)
