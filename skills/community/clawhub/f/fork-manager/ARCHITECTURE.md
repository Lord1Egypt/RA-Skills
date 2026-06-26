# Fork Manager - Architecture & Design Decisions

## Overview

Fork Manager is a reusable skill that works across multiple LLM agent environments:

- **Claude Code CLI** (Anthropic)
- **OpenClaw** (multi-provider LLM CLI)
- **Any agent** that supports the AgentSkills format

The skill is not an executable script — it's an **instruction document** (SKILL.md) that LLM agents read and execute using existing tools (git, gh).

## Directory Structure

```
fork-manager/
├── .git/
├── .gitignore
├── README.md
├── SKILL.md                        # Agent instructions
├── ARCHITECTURE.md                 # This file
└── repos/
    └── <project-name>/
        ├── config.json             # Local only (gitignored)
        └── config.example.json     # Versioned template
```

## Architectural Decisions

### 1. Configs are Local-Only

**Decision:** `config.json` files are not versioned in Git.

**Reason:**
- Contains environment-specific information (local paths, PR lists, sync history)
- Each user's fork setup is unique

**Implementation:**
- `.gitignore` contains `repos/*/config.json`
- Templates `config.example.json` are versioned as documentation

### 2. Skill vs Plugin

**Decision:** Fork-manager is a **skill**, not a plugin.

| | Skill | Plugin |
|---|---|---|
| Format | Markdown document | Executable code |
| Execution | Agent reads and follows instructions | Adds new tools/capabilities |
| Portability | Works across any compatible agent | CLI-specific |

**Reason:** Fork-manager only orchestrates existing tools (git, gh). No new CLI functionality needed.

### 3. Multi-Repo Structure

**Decision:** One directory per repository under `repos/`.

**Reason:**
- Users can manage multiple forks
- Each repo has its own config and history
- Scales easily — just add a new directory

### 4. Distribution

Available via:
- **GitHub**: `git clone https://github.com/Glucksberg/fork-manager-skill.git`
- **ClawHub**: `clawhub install fork-manager`

## Integration

### OpenClaw

Loaded via `extraDirs` in global config:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/agents"]
    }
  }
}
```

### Claude Code CLI

Loaded via symlink:

```bash
ln -s /path/to/fork-manager ~/.claude/skills/fork-manager
```

### ClawHub

```bash
clawhub install fork-manager
```

Both CLIs read/write from the **same location** — no data duplication.

## Data Flow

```
┌─────────────────────────────────────────┐
│  Single Source of Truth                 │
│  /path/to/fork-manager/                 │
│  - Git repository                       │
│  - Local configs (not versioned)        │
└─────────────────────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
┌──────────────┐      ┌──────────────────┐
│  OpenClaw    │      │  Claude Code CLI │
│  (extraDirs) │      │  (symlink)       │
└──────────────┘      └──────────────────┘
```

## Deterministic Helpers

The skill remains instruction-first, but critical state reconciliation should be
deterministic when possible.

### `scripts/update-config.mjs`

This helper treats GitHub as the source of truth for currently open PRs by the
authenticated contributor and treats `openPRs` / `prBranches` as a local cache.
Agents should run it before `status`, `rebase-all`, `build-production`, and
`full-sync`.

The helper intentionally does not decide whether a closed-unmerged PR should be
kept as a local patch. It removes no-longer-open PRs from the open cache and
records them under `notes.closedWithoutMerge` with `reviewStatus: "pending"` so
the interactive `review-closed` flow can make that policy decision.

## Future Evolution

### Possible Improvements
- [x] Helper script for GitHub → config PR reconciliation
- [ ] Helper scripts for additional common operations
- [ ] Templates for popular repos
- [ ] GitHub Actions integration for automatic sync

### Not Planned
- ❌ Converting to executable plugin (keeps simplicity as instruction-based skill)
- ❌ Versioned configs (configs remain local and user-specific)

## References

- [OpenClaw Skills Docs](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md)
- [ClawHub](https://clawhub.ai)
- [GitHub Repo](https://github.com/Glucksberg/fork-manager-skill)
