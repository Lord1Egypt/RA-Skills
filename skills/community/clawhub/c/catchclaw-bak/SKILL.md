---
name: catchclaw
description: "Search, install, and export agentars from the CatchClaw marketplace. Use when the user wants to find, install, or package agent templates."
user-invocable: true
metadata:
  openclaw:
    emoji: "📦"
    homepage: https://github.com/OpenAgentar/catchclaw
    requires:
      bins:
        - node
      env:
        - AGENTAR_API_BASE_URL
        - AGENTAR_HOME
      config:
        - ~/.agentar
        - ~/.openclaw/workspace
        - ~/.openclaw/agentar-workspaces
        - ~/agentar-exports
---

# CatchClaw Agentar Manager

**Source:** This skill is from the [CatchClaw skill repository](https://github.com/OpenAgentar/catchclaw).

An agentar is a distributable agent archive (ZIP) containing workspace files such as SOUL.md, skills, and other configuration. It can be installed as a new agent or used to overwrite an existing agent with a single command.

## Trigger Conditions

- User asks to search / find / browse agentars
- User asks to install / download a specific agentar
- User asks to export / package an agent as an agentar
- User asks to rollback / undo / restore a previous agent workspace
- User mentions the keyword "agentar" or "catchclaw"

**Important:** Before performing any action, verify the bundled CLI works (see CLI Setup). Do not run search, install, export, or rollback until verification passes.

## CLI Setup (mandatory — run before any command)

<HARD-GATE>
**Before running any search, install, export, or rollback command, you MUST verify the bundled CLI.** The CLI (`agentar_cli.mjs`) is bundled in this skill's directory — no download or copy is needed.

1. **Locate:** The CLI is at the same directory as this SKILL.md (e.g. `~/.agents/skills/catchclaw/agentar_cli.mjs`).
2. **Verify:** Run `node <skill-dir>/agentar_cli.mjs version`. Only after it succeeds, proceed with search/install/export/rollback.

Never run `$CLI search`, `$CLI install`, `$CLI export`, or `$CLI rollback` until verification passes.
</HARD-GATE>

## CLI Location

The CLI is bundled in this skill's directory. Run it directly:

```bash
node <skill-dir>/agentar_cli.mjs <command>
```

Where `<skill-dir>` is the directory containing this SKILL.md (e.g. `~/.agents/skills/catchclaw/`).

All commands below use `$CLI` as shorthand for `node <skill-dir>/agentar_cli.mjs`.

## Environment Variables (optional)

These are listed in `metadata.openclaw.requires.env` for registry/security analysis. **Neither is required** for normal use; omit both to use defaults.

- `AGENTAR_API_BASE_URL` — Override the default API base URL (defaults to `https://catchclaw.me`)
- `AGENTAR_HOME` — Override the default CLI config directory (defaults to `~/.agentar`)

## Paths read or written by the bundled CLI

Aligned with `metadata.openclaw.requires.config` and `metadata.json` in this skill:

| Path | Access | Purpose |
|------|--------|---------|
| `~/.agentar/` | read/write | CLI config (`config.json`), optional standalone install copy of `agentar_cli.mjs` |
| `~/.openclaw/workspace` | read/write | Main agent workspace (`install --overwrite`, export) |
| `~/.openclaw/agentar-workspaces/` | read/write | Per-agent workspaces (`install --name …`) |
| `~/agentar-exports/` | write | Default directory for `export` ZIP output |
| `<skill-dir>/skills/.credentials` | write (optional) | Written when install is run with `--api-key` |

## Commands

### Search

```bash
$CLI search <keyword>
```

Search the CatchClaw marketplace for agentars matching the keyword.

### Install

```bash
$CLI install <slug> --name <name> [--api-key <key>]
$CLI install <slug> --overwrite
```

Install an agentar from the marketplace.

**Options:**
- `--name <name>` — Create a new agent with the given name. Existing agents are not affected. (Preferred; list this option first when prompting.)
- `--overwrite` — Overwrite the main agent (`~/.openclaw/workspace`). Existing workspace is backed up automatically. **Never use without the user's explicit selection.**
- `--api-key <key>` — (Optional) API key to save into `skills/.credentials` for agentars that require backend authentication.

### Export

```bash
$CLI export [--agent <id>] [-o <path>] [--include-memory]
```

Export an agent as a distributable agentar ZIP package. MEMORY.md is excluded by default. Output defaults to `~/agentar-exports/`. Sensitive files (`.credentials`, `.env`, `.secret`, `.key`, `.pem`) are automatically filtered out.

**Options:**
- `--agent <id>` — Agent ID to export. **If the user did not specify an agent, you MUST list agents and ask the user to choose before running export; do not export without the user's selection.**
- `-o, --output <path>` — Output ZIP file path.
- `--include-memory` — Include MEMORY.md in export (excluded by default).

### Rollback

```bash
$CLI rollback
$CLI rollback --latest
```

Restore a workspace from backup. Without `--latest`, lists all available backups for selection. The current workspace is automatically backed up before restoring, so rollback is always safe.

### Version

```bash
$CLI version
```

Show the CLI version.

## Installation Rules

<HARD-GATE>
Before executing `install`:
1. **Slug required:** If the user wants to install an agentar but has not specified which one (no slug), prompt the user to enter the agentar name/slug to install. Do NOT run install without a slug.
2. **Mode confirmation (CRITICAL - MUST ASK USER):** You MUST explicitly ask the user to choose the installation mode. Do NOT proceed with installation until the user has made a clear choice. **NEVER assume or default to any mode without user confirmation.**

Present the following two options to the user and wait for their response:
1. **new** — Create a new agent. The existing agents are not affected.
2. **overwrite** — Overwrite the main agent (~/.openclaw/workspace). The existing workspace will be backed up automatically.

**Important:**
- Do NOT execute install until the user explicitly selects one of the above options
- Do NOT use "new" as a default without asking
- Do NOT use "overwrite" unless the user explicitly selects it
- If the user chooses "new" but doesn't specify a name, use the slug as the default name

After the user explicitly selects "new", execute: `$CLI install <slug> --name <user-specified name>`
After the user explicitly selects "overwrite", execute: `$CLI install <slug> --overwrite`

Never execute install without both: (1) a slug, and (2) explicit user confirmation of installation mode.
</HARD-GATE>

## Export Rules

<HARD-GATE>
**When the user has not specified which agent to export, you MUST let the user choose first. Do NOT export on your own.** If `--agent <id>` was not provided by the user:
1. Run `$CLI export` without `--agent` to list available agents (or equivalent to show choices).
2. Present the list to the user and ask which agent to export.
3. Only after the user explicitly selects an agent, run `$CLI export --agent <user-selected-id>` (and optional `-o`, `--include-memory` as needed). Never assume or pick an agent for the user.
</HARD-GATE>

- MEMORY.md is excluded by default. Only include it if the user explicitly requests it with `--include-memory`.
- Sensitive files are automatically filtered out during export (`.credentials`, `.env`, `.secret`, `.key`, `.pem`).
- After a successful export, remind the user to review the exported ZIP for any sensitive data (API keys, credentials, personal information).
- Export is a purely local operation — it does not require network access.

## Error Handling

| Error | Action |
|-------|--------|
| CLI file not found | Verify the skill is installed correctly — `agentar_cli.mjs` should be in the skill directory |
| API unreachable or network error | Suggest checking network connectivity, or override the API URL with: `export AGENTAR_API_BASE_URL=<url>` |
| Node.js not installed | Instruct user to install Node.js from https://nodejs.org/ |
| Download or extraction failure | Show the error message and suggest retrying the command |

## Workflow

1. **Search**: Run `$CLI search <keyword>` to find agentars. Each result includes a slug identifier.
2. **Install**: If the user did not specify which agentar to install (no slug), ask the user to enter the agentar name/slug. Then confirm installation mode: present [1] new, [2] overwrite; never use overwrite without explicit user selection. Only after you have both slug and mode, execute the install command.
3. **Export**: If the user did not specify which agent to export, run `$CLI export` (no `--agent`) to list agents, present the list to the user, and ask them to choose. Only after the user selects an agent, run `$CLI export --agent <id>`. Do not export without the user's explicit selection.
4. **Rollback**: If the user wants to undo an overwrite install, run `$CLI rollback` to list available backups and restore one.
