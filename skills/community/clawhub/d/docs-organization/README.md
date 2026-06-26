# docs-organization

Practical documentation structure templates for AI-assisted projects. Helps AI coding agents (and humans) organize project docs by size, audience, and freshness.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What it does

Answers the question every project eventually asks: *where should this doc go?*

Given a project, this skill:
1. **Assesses project size** (small / medium / large) using a simple rubric
2. **Recommends a directory structure** with templates for each size
3. **Classifies existing docs** by audience (agent, operator, user) and freshness (canonical, snapshot, archived)
4. **Slims bloated CLAUDE.md/AGENTS.md** by extracting reference material into dedicated files
5. **Prevents drift** with single-source-of-truth principles and doc metadata conventions

Works with any AI coding agent: Claude Code, OpenClaw, Codex CLI, Gemini CLI, Cursor, Copilot.

## Quick Start

```bash
# Universal (npx skills)
npx skills add zning1994/docs-organization

# OpenClaw ClawHub
openclaw skills install docs-organization

# Standalone
git clone https://github.com/zning1994/docs-organization
```

## When to use

- Setting up docs for a new project
- Reorganizing a messy `docs/` folder
- CLAUDE.md or AGENTS.md is over 250 lines
- Same information duplicated across multiple markdown files
- Not sure where a new doc should live
- Need to archive old design specs or research notes

## Core Principles

### 1. Single Source of Truth

Every fact lives in exactly one place. Other docs *link* to it, never *copy* it.

### 2. CLAUDE.md Is a Routing Table

Keep CLAUDE.md under 250 lines. It tells AI agents where to find things, not what things are. Extract API tables, deploy procedures, and changelogs into `docs/`.

### 3. Organize by Audience + Freshness

| Directory | Status | Contains |
|-----------|--------|----------|
| `reference/` | canonical | API, DB schema, config |
| `runbooks/` | canonical | Deploy, ops, incidents |
| `guides/` | canonical | How-to for users |
| `product/` | canonical | Roadmap, direction |
| `design/` | snapshot | Feature design specs |
| `plans/` | snapshot | Implementation plans |
| `research/` | snapshot | Investigations, audits |
| `archive/` | archived | Superseded docs |

### 4. No Cross-Doc Mirroring

After changes, update the one canonical doc. Not two, not three — one.

## Project Size Templates

### Small (< 5 source files)
```
project/
├── CLAUDE.md    # 50-100 lines
└── README.md
```

### Medium (has API, deployment)
```
project/
├── CLAUDE.md    # 100-200 lines
└── docs/
    ├── reference/
    ├── design/
    └── plans/
```

### Large (multi-service, continuous ops)
```
project/
├── CLAUDE.md    # 200-250 lines
└── docs/
    ├── reference/
    ├── runbooks/
    ├── guides/
    ├── product/
    ├── design/
    ├── plans/
    ├── research/
    ├── decisions/
    └── archive/
```

## Document Metadata

Add to the top of any non-trivial doc:

```yaml
---
status: canonical | snapshot | archived
audience: agent | operator | user | contributor
last_reviewed: YYYY-MM-DD
---
```

## Anti-Patterns

| Problem | Fix |
|---------|-----|
| Same fact in 3+ files | Pick one canonical location |
| 2000-line CLAUDE.md | Extract to `docs/`, keep < 250 lines |
| Flat `docs/` with 20+ files | Group by audience/purpose |
| "Always update these 4 files" | Update the one canonical source |
| Empty directories "for later" | Create when you have content |

## Origin

Lessons learned from reorganizing [ai-personal-system](https://github.com/zning1994/ai-personal-system), a multi-agent AI operating system with 70+ API endpoints, 6 agents, and 39 skills. The AGENTS.md went from 800+ lines to 250, with zero information loss.

## License

[MIT](LICENSE)
