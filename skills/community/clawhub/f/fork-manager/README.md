# Fork Manager Skill

Manage forks where you contribute PRs but also use improvements before they're merged upstream. Includes support for local patches — fixes kept in the production branch even when the upstream PR was closed/rejected.

## Structure

```
fork-manager/
├── SKILL.md              # Full agent instructions
├── scripts/
│   └── update-config.mjs # Deterministic GitHub → config reconciliation
├── README.md             # This file
├── ARCHITECTURE.md       # Design decisions and architecture
└── repos/
    └── <project-name>/
        ├── config.json             (local only - not versioned)
        └── config.example.json     (versioned template)
```

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Glucksberg/fork-manager-skill.git /path/to/fork-manager

# 2. Create local configs from examples
cd /path/to/fork-manager
cp repos/<project>/config.example.json repos/<project>/config.json

# 3. Edit with your info
vim repos/<project>/config.json

# 4. Configure for OpenClaw (global for all agents)
openclaw config set skills.load.extraDirs '["/path/to/parent/directory"]'

# 5. Configure for Claude Code CLI
ln -s /path/to/fork-manager ~/.claude/skills/fork-manager
```

### Via ClawHub

```bash
clawhub install fork-manager
```

## Integration

### OpenClaw

The skill is loaded via `extraDirs` in the global config:

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

The skill is loaded via symlink:

```bash
~/.claude/skills/fork-manager → /path/to/fork-manager
```

## Available Commands

- `status` - Check current fork state
- `sync` - Sync main with upstream
- `rebase <branch>` - Rebase a specific branch
- `rebase-all` - Rebase all PR branches
- `update-config` - Update config with current PRs
- `build-production` - Create production branch with all PRs + local patches
- `review-closed` - Review recently closed PRs (keep/drop/resubmit)
- `review-patches` - Re-evaluate existing local patches
- `audit-open` - Audit open PRs for redundancy/obsolescence
- `full-sync` - Full sync (all of the above in sequence)

## Usage

```bash
# Via OpenClaw or Claude Code CLI:
# "Use fork-manager to do a full-sync of my-project"
# "Check the status of my fork"
# "Sync and rebase all PR branches"
```

See `SKILL.md` for complete agent instructions.

### Deterministic Config Refresh

`openPRs` and `prBranches` are a local cache. Refresh them from GitHub before
rebasing or rebuilding a production branch:

```bash
node scripts/update-config.mjs --repo-name claude-mem
node scripts/update-config.mjs --repo-name claude-mem --check
node scripts/update-config.mjs --repo-name claude-mem --dry-run
```

The script adds new open PRs, updates changed head branches, restores reopened
PRs, removes no-longer-open PRs from the open cache, and records merged/closed
PRs in `notes` for the review steps. By default it uses the owner from
`config.fork` as the GitHub PR author filter, with `@me` as a fallback.

## Documentation

- **[SKILL.md](SKILL.md)** - Complete agent instructions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Design decisions and architecture
