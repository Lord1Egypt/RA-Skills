# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An AI agent team collaboration tool consisting of two components:

1. **Plugin** (`integrations/openclaw/agent-team/`) - OpenClaw native plugin that auto-injects team information and collaboration rules into system context
2. **Skill** (`scripts/team.py`) - CLI tool for managing team member data (CRUD operations)

The plugin must be installed for the skill to work properly. It injects the PDCA workflow: Plan → Do → Check → Act, with leader-specific authority rules.

## Commands

```bash
# Team management
python3 scripts/team.py list
python3 scripts/team.py update --agent-id "id" --name "Name" --role "Role" --is-leader true --enabled true --tags "tag1,tag2" --expertise "skill1" --not-good-at "weakness1"
python3 scripts/team.py reset

# Run tests
python3 -m pytest tests/ -v

# Run specific test
python3 -m pytest tests/test_team.py::test_list_empty -v
```

## Key Patterns

- **Context-Aware Injection**: Plugin checks `ctx.agentId` and only injects "Leader Authority" section to the designated leader
- **Single-Leader Constraint**: Setting a new leader automatically removes leader status from all others
- **Graceful Degradation**: Both components handle missing/invalid data files gracefully (return empty state)

## Architecture

- `scripts/team.py` - Team member CRUD (stores in `~/.agent-team/team.json`)
- `integrations/openclaw/agent-team/index.ts` - Plugin that injects team context via `before_prompt_build` hook
- `integrations/openclaw/agent-team/openclaw.plugin.json` - Plugin metadata and config schema

Uses argparse subcommands, outputs YAML format for list commands, and supports `--data-file` for custom storage paths.

## Data File Paths

Default: `~/.agent-team/team.json`

Directory is auto-created. The script handles missing/invalid files gracefully.

## Key Files to Keep in Sync

When updating collaboration rules or workflow, ensure consistency between:
- `SKILL.md` - Skill documentation (source of truth)
- `integrations/openclaw/agent-team/index.ts` - Plugin injection logic
- `README.md` - Project documentation