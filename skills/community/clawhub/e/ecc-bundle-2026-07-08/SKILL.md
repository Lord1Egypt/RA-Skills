---
name: ecc-bundle-2026-07-08
description: ECC essentials bundle - install 23 core skills (agentic-engineering, security-review, deployment-patterns, docker-patterns, git-workflow, search-first, safety-guard) in one shot. Use when user asks to install ECC essentials, bootstrap OpenClaw with extended capabilities, or set up a full ECC workflow bundle.
version: 1.0.0
homepage: https://github.com/affaan-m/everything-claude-code
emoji: "✅"
metadata:
  openclaw:
    requires:
      bins:
      - python3
---

# ECC Bundle 2026-07-08

One-click installer for **23 hand-picked ECC skills** from [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) v1.9.0 (2026-03-20).

## What's Included

### Tool Enhancement (6)

- `context-budget`
- `token-budget-advisor`
- `prompt-optimizer`
- `rules-distill`
- `product-lens`
- `blueprint`

### Agent Design (5)

- `agentic-engineering`
- `agent-eval`
- `ai-first-engineering`
- `autonomous-loops`
- `continuous-agent-loop`

### Engineering Practices (7)

- `deployment-patterns`
- `codebase-onboarding`
- `architecture-decision-records`
- `deep-research`
- `cost-aware-llm-pipeline`
- `docker-patterns`
- `git-workflow`

### Security (5)

- `search-first`
- `safety-guard`
- `security-review`
- `security-scan`
- `skill-comply`

Total: **23 skills**.

## Install

After installing this skill, the bundled Python installer can
extract the 23 SKILL.md files into your local agents skills directory.

```bash
# Run the bundled installer (default target: ~/.agents/skills)
python scripts/install-ecc-bundle.py

# Or specify a custom target
python scripts/install-ecc-bundle.py --target /path/to/skills

# Preview mode
python scripts/install-ecc-bundle.py --dry-run

# Force overwrite existing skills
python scripts/install-ecc-bundle.py --force
```

## Uninstall

```bash
python scripts/install-ecc-bundle.py --uninstall
```

## Bundle Layout

```
ecc-bundle-2026-07-08/
├── SKILL.md                  <- this file (entry point)
├── bundle/
│   ├── agentic-engineering.md
│   ├── agent-eval.md
│   ├── ai-first-engineering.md
│   ├── autonomous-loops.md
│   ├── architecture-decision-records.md
│   ├── codebase-onboarding.md
│   ├── context-budget.md
│   ├── continuous-agent-loop.md
│   ├── cost-aware-llm-pipeline.md
│   ├── deployment-patterns.md
│   ├── deep-research.md
│   ├── docker-patterns.md
│   ├── git-workflow.md
│   ├── prompt-optimizer.md
│   ├── safety-guard.md
│   ├── search-first.md
│   ├── security-review.md
│   ├── security-scan.md
│   ├── skill-comply.md
│   ├── token-budget-advisor.md
│   ├── rules-distill.md
│   ├── product-lens.md
│   ├── blueprint.md
└── scripts/
    └── install-ecc-bundle.py
```

## Source Provenance

All 23 SKILL.md files in `bundle/` are upstream copies from `affaan-m/everything-claude-code` v1.9.0 (2026-03-20).

Original repository: https://github.com/affaan-m/everything-claude-code

License: MIT-0 (per ClawHub platform license)

## Categories

- **Tool Enhancement** (6): `context-budget`, `token-budget-advisor`, `prompt-optimizer`, `rules-distill`, `product-lens`, `blueprint`
- **Agent Design** (5): `agentic-engineering`, `agent-eval`, `ai-first-engineering`, `autonomous-loops`, `continuous-agent-loop`
- **Engineering Practices** (7): `deployment-patterns`, `codebase-onboarding`, `architecture-decision-records`, `deep-research`, `cost-aware-llm-pipeline`, `docker-patterns`, `git-workflow`
- **Security** (5): `search-first`, `safety-guard`, `security-review`, `security-scan`, `skill-comply`

## Version

- Bundle version: `1.0.0`
- ECC upstream: `v1.9.0` (2026-03-20)
- Bundled installer: `scripts/install-ecc-bundle.py`
