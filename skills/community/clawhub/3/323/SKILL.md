---
name: bytedance-find-skills
description: "Manage AI agent skills using the @tiktok-fe/skills CLI (binary: ai-skills). Use when the user asks to find, search, install, add, remove, update, publish, list, or manage AI skills across coding agents (Cursor, Claude Code, GitHub Copilot, Windsurf, etc.), or mentions ai-skills, skill hub, or @tiktok-fe/skills."
---

# AI Skills CLI

`@tiktok-fe/skills` (`ai-skills`) discovers, installs, and manages AI agent skills across 30+ platforms.

```bash
npm install -g @tiktok-fe/skills
# or: npx @tiktok-fe/skills [command]
```

## Pure Mode (Required)

The CLI defaults to interactive CLI mode with colors, spinners, arrow-key navigation, and confirmation prompts. **This WILL hang/block when called by an AI agent.** Always use `--pure` to switch to non-interactive plain-text mode.

### What `--pure` changes

| Behavior        | CLI mode (default)                 | Pure mode (`--pure`)                                            |
| --------------- | ---------------------------------- | --------------------------------------------------------------- |
| Output          | ANSI colors, spinners, animations  | Plain `console.log`, no escape codes                            |
| Prompts         | Interactive confirmation dialogs   | **Skipped** — operations that need confirmation silently fail   |
| Overwrite       | Asks "overwrite?" prompt           | Always returns `false` — use `--force` to overwrite             |
| Search          | Real-time Ink UI with keyboard nav | Paginated text output                                           |
| Scope selection | Interactive multi-select           | **Fails** if not specified — always pass `-p`/`-g`/`-t`/`--dir` |
| Manage          | Ink-based React terminal UI        | Falls back to `list` output                                     |

### Preventing hangs

Commands that block without proper flags:

```bash
# WRONG — will hang on scope selection prompt
ai-skills add my-skill --source local --pure

# CORRECT — scope specified, no prompt
ai-skills add my-skill --source local --project --pure

# WRONG — will silently skip existing skill (shouldOverwrite=false)
ai-skills add my-skill --source local --project --pure

# CORRECT — force overwrite
ai-skills add my-skill --source local --project --pure --force

# WRONG — will hang on confirmation prompt
ai-skills update --project --pure

# CORRECT — auto-confirm
ai-skills update --project --pure -y

# WRONG — will hang on clean confirmation
ai-skills clean --project --pure

# CORRECT — force clean
ai-skills clean --project --pure --force
```

### Complete flag checklist

Every command invoked by an AI agent must include:

1. **`--pure`** — plain-text output, no ANSI codes, no interactive prompts
2. **Scope flag** — `-p` (project), `-g` (global), `-t <dir>`, or `--dir <dir>`
3. **Confirmation skip** — `-y` (for update/publish) or `--force` (for add/remove/clean)
4. **`--source`** — `local`, `github`, `gitlab`, `codebase`, `wellknown`

## Quick Reference

### Find skills

```bash
ai-skills find "query" --pure --page 1
ai-skills find react --source github --pure
ai-skills find --tag typescript --filter community --pure
```

### Install skills

```bash
# From internal registry
ai-skills add skill-name --source local --project --pure -y

# From GitHub (specific skill)
ai-skills add owner/repo --source github --skill skill-name --project --pure -y

# All skills from a repo
ai-skills add owner/repo --source github --project --pure -y

# Force overwrite
ai-skills add skill-name --source local --project --pure --force
```

### List / Remove / Update

```bash
ai-skills list --project --pure
ai-skills remove skill-name --project --pure --force
ai-skills update --project --pure -y
ai-skills update --list --project --pure          # check only
```

### Auth & Config

```bash
ai-skills whoami --json
ai-skills login --pure
ai-skills config --json
```

### Create & Publish

```bash
ai-skills init --name my-skill --template basic --pure
ai-skills publish --dir ./my-skill --pure -y
ai-skills unpublish user/skills/name --version 1.0.0 --pure --force
```

### Other

```bash
ai-skills agents --pure                           # list supported agents
ai-skills clean --project --pure --force           # remove all skills
```

## Output Parsing

| Command | Success                             | Error                                             |
| ------- | ----------------------------------- | ------------------------------------------------- |
| add     | `Installed: name`                   | `Error:`, `Already installed:`, `No agents found` |
| remove  | `Removed: name`                     | `not found`, `Cannot remove:`                     |
| update  | `Updated: N, Skipped: N, Failed: N` | —                                                 |
| publish | `Published: name@ver`               | `Not logged in`                                   |
| clean   | `Cleaned: N skill(s) removed`       | —                                                 |
| login   | `Login successful:`                 | `Login failed:`                                   |
| init    | `Created: /path/SKILL.md`           | `Error:`                                          |

## Common Workflows

### Install a skill for a project

```bash
ai-skills find typescript --pure --page 1
ai-skills add typescript-config --source local --project --pure -y
ai-skills list --project --pure
```

### Update all project skills

```bash
ai-skills update --list --project --pure
ai-skills update --project --pure -y
```

### Publish a new skill

```bash
ai-skills whoami --json
ai-skills init --name my-skill --template basic --pure
# (edit SKILL.md)
ai-skills publish --dir ./my-skill --pure -y
```

## Detailed References

For command-specific options, arguments, and output formats, read the corresponding file under `llms/`:

| Topic             | File                                                                   |
| ----------------- | ---------------------------------------------------------------------- |
| CLI overview      | [llms/cli-overview.txt](llms/cli-overview.txt)                         |
| **Commands**      |                                                                        |
| add (install)     | [llms/commands/add.txt](llms/commands/add.txt)                         |
| find (search)     | [llms/commands/find.txt](llms/commands/find.txt)                       |
| list              | [llms/commands/list.txt](llms/commands/list.txt)                       |
| remove            | [llms/commands/remove.txt](llms/commands/remove.txt)                   |
| update            | [llms/commands/update.txt](llms/commands/update.txt)                   |
| init              | [llms/commands/init.txt](llms/commands/init.txt)                       |
| publish           | [llms/commands/publish.txt](llms/commands/publish.txt)                 |
| unpublish         | [llms/commands/unpublish.txt](llms/commands/unpublish.txt)             |
| clean             | [llms/commands/clean.txt](llms/commands/clean.txt)                     |
| config            | [llms/commands/config.txt](llms/commands/config.txt)                   |
| login             | [llms/commands/login.txt](llms/commands/login.txt)                     |
| whoami            | [llms/commands/whoami.txt](llms/commands/whoami.txt)                   |
| agents            | [llms/commands/agents.txt](llms/commands/agents.txt)                   |
| manage            | [llms/commands/manage.txt](llms/commands/manage.txt)                   |
| **Guides**        |                                                                        |
| AI best practices | [llms/guides/ai-best-practices.txt](llms/guides/ai-best-practices.txt) |
| SKILL.md format   | [llms/guides/skill-format.txt](llms/guides/skill-format.txt)           |
| Source platforms  | [llms/guides/source-platforms.txt](llms/guides/source-platforms.txt)   |
| Supported agents  | [llms/guides/agents-list.txt](llms/guides/agents-list.txt)             |

Read these files only when detailed information is needed for a specific command or topic.
