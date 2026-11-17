---
name: agentdots-sync
description: Use when users ask to sync, restore, apply, back up, push, or roll back local agent instructions, rules, or skills for Codex, Claude Code, OpenCode, Grok Build, CodeBuddy Code, WorkBuddy, or another Agent Skills-compatible platform.
license: MIT
---

# agentdots-sync

Safely synchronize explicitly selected local agent assets with a Git remote. This Skill copies files; it does not translate `AGENTS.md`, `CLAUDE.md`, platform rules, or configuration formats into one another.

## Platform selection

Use `--platform` to select safe defaults. Run `--list-platforms` when the platform or defaults are uncertain. Built-in profiles cover `codex`, `claude-code`, `opencode`, `grok-build`, `codebuddy-code`, `workbuddy`, and `custom`; aliases such as `claude`, `grok`, and `codebuddy` resolve to canonical names.

WorkBuddy and `custom` require an explicit `--root`; `custom` also requires one or more `--asset`. For project-level assets, override both `--root` and `--asset` rather than assuming that global and project layouts match. Use this Skill only where the agent can access the local filesystem and execute Python; browser-only chat surfaces cannot synchronize local configuration directories.

## Safety contract

Default to read-only inspection. Before a write, replacement, rollback, or push:

1. Resolve the canonical platform, direction, local root, backup directory, remote, branch, and every selected asset.
2. Show those exact targets and obtain explicit authorization for this run. “Sync it” is not permission to choose a direction or overwrite files.
3. Execute only the approved command with `--yes`. Stop on any Git, validation, lock, or permission failure.

Never use cross-platform defaults to copy one platform's instruction file over another platform's differently named file. If the user wants format conversion, treat that as a separate transformation task.

Resolve the script from this loaded Skill's actual directory. Replace `<skill-root>` below with that absolute path.

## Workflow

```bash
python3 <skill-root>/scripts/sync.py --list-platforms
python3 <skill-root>/scripts/sync.py --platform <platform> --doctor
python3 <skill-root>/scripts/sync.py --platform <platform> --plan
python3 <skill-root>/scripts/sync.py --platform <platform> --apply --plan --remote <url> --branch <branch>
```

After the user approves the exact plan, use one mutation mode:

```bash
python3 <skill-root>/scripts/sync.py --platform <platform> --restore --yes --remote <url> --branch <branch>
python3 <skill-root>/scripts/sync.py --platform <platform> --apply --yes --remote <url> --branch <branch>
python3 <skill-root>/scripts/sync.py --platform <platform> --push --yes --remote <url> --branch <branch> --message <text>
python3 <skill-root>/scripts/sync.py --platform <platform> --rollback --yes
```

Repeat `--asset <path>` to override profile assets. Use `--root <path>` or `--backup-dir <child-path>` only when the resolved profile defaults do not match the user's real layout.

`--apply` and `--restore` back up existing selected local assets before replacement. A first apply with no existing selected asset has nothing to back up. Rollback protects current requested assets, then restores only the requested intersection recorded in the selected backup manifest. Push stages only selected paths and never force-pushes.

## Stop conditions

Never install or authenticate Git tooling, create or guess repositories or branches, resolve conflicts automatically, synchronize a home directory, bypass target validation, remove an unverified lock, or run concurrent mutations against the same root.
