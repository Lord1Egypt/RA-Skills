# Codia Design Skills Agent Install

This file is written for Codex, Claude Code, Cursor, and other local coding agents. Read it, ask for the user's permission, then install Codia Design Skills.

## Goal

Install:

- The `codia-design` runtime CLI from npm.
- The `codia-design-skills` root agent skill pack from the public skill repository.

After installation, future agent sessions can call Codia Open API commands for design conversion, image generation/editing, SVG conversion, PDF-to-PPT, credits, usage, and related workflows.

## Required Permission

Before running install commands, ask the user for permission to:

- Run `npm install -g @codia-ai/codia-design-cli`.
- Run `npx -y skills add https://github.com/codia-ai/codia-design-skills.git -g -y` to install the skill globally.
- Open a browser for `codia-design auth login --platform codex` if authentication is needed.

If permission is denied, stop and provide the manual commands instead.

## Safety Rules

- Do not print API keys.
- Do not print `~/.codia/design-skills/config.json`.
- Do not push git branches or modify unrelated project files.
- Ask the user for an API key only if no key is available in `CODIA_API_KEY` and `codia-design auth status` reports disconnected.

## Skill Source And Accounts

`npx -y skills add https://github.com/codia-ai/codia-design-skills.git -g -y` installs skill files from the public GitHub repository. It does not upload skills and does not require a separate skills.sh publisher account.

To share these skills with other users, maintainers provide a repository or local bundle that contains a root `SKILL.md`. This repository uses that root skill as a router and keeps workflow/feature instructions under `skills/`. The skills.sh directory can discover and rank skills automatically after users install them through the `skills` CLI. A skills.sh API key is only needed for catalog API queries, not for publishing or installing skills.

An npm account is only needed for publishing the separate runtime CLI package, such as `@codia-ai/codia-design-cli`.

## Step 1: Check Prerequisites

Run:

```bash
node --version
npm --version
```

Node.js 20 or newer is required. If Node.js or npm is missing, tell the user to install Node.js 20+ first, then resume.

## Step 2: Install Runtime CLI

Run:

```bash
npm install -g @codia-ai/codia-design-cli
codia-design --help
```

Windows PowerShell uses the same commands:

```powershell
npm install -g @codia-ai/codia-design-cli
codia-design --help
```

If global npm install is not allowed, use the runtime through `npx`:

```bash
npx -y @codia-ai/codia-design-cli --help
```

If global npm install fails because of permissions, ask the user to run the same command manually.

## Step 3: Install the Skill Pack

If this file is in the public GitHub skill repository, run:

```bash
npx -y skills add codia-ai/codia-design-skills -g -y
```

If the repository URL is known, this form is also valid:

```bash
npx -y skills add https://github.com/codia-ai/codia-design-skills.git -g -y
```

If `npx skills` is unavailable, stop and ask the user how they want to install local agent skills. The npm CLI package does not bundle skill files.

Do not pass `--full-depth` for normal installs. A normal install should create one top-level `codia-design-skills` skill pack.

## Step 4: Verify Skill Installation

Run:

```bash
npx skills ls -g
```

Confirm that `codia-design-skills` appears in the installed skill list.

One or more supported agent skill directories should contain the root pack and its nested feature files. Common locations include:

```text
~/.agents/skills/codia-design-skills/SKILL.md
~/.agents/skills/codia-design-skills/skills/codia-image-generate/SKILL.md
~/.codex/skills/codia-design-skills/SKILL.md
~/.claude/skills/codia-design-skills/SKILL.md
~/.cursor/skills/codia-design-skills/SKILL.md
```

Exact paths are agent-dependent; `~/.agents/skills` is the standard unified local-agent location, while Codex commonly reads `~/.codex/skills`. The root `SKILL.md` handles routing and reads nested files under `skills/` when needed.

## Step 5: Authenticate

First check whether the CLI is already connected:

```bash
codia-design auth status
```

If it is connected, continue to verification.

If it is not connected, prefer the device login flow:

```bash
codia-design auth login --platform codex
```

If the user provides an API key through `CODIA_API_KEY`, bind it without printing the value:

```bash
codia-design auth set --api-key "$CODIA_API_KEY"
```

If the user provides an API key directly in chat, do not echo it back. Run the auth command using the provided value only.

## Step 6: Smoke Test

Run:

```bash
codia-design --help
codia-design auth status
```

If authenticated, also run:

```bash
codia-design credits
```

Report the final status to the user. Do not include secrets or config file contents.
