# Contributing to claw3d-skill

Thanks for your interest in contributing! This repo contains the AI agent instructions that tell the agent how to use claw3d for 3D printing workflows.

## How skills work

A skill is a set of markdown files that get assembled into a single `SKILL.md` prompt. The agent reads this prompt to understand what tools it has, how to use them, and how to interact with the user.

## Directory structure

```
src/
  00-frontmatter.md   — System prompt header, identity, capabilities
  01-core.md          — Core tool definitions (exec, message, etc.)
  02-ai-forger.md     — AI model creation workflows (text/image → 3D)
  03-directory.md     — Model search (Thingiverse)
  04-slicing.md       — Slicing and preview workflows
  05-printing.md      — Printer control (Moonraker)
scripts/
  build-skill.sh      — Assembles src/ modules into SKILL.md
```

## How to contribute

1. Fork the repo and create a branch from `main`
2. Edit the relevant `src/*.md` file
3. Run `./scripts/build-skill.sh` to rebuild `SKILL.md`
4. Test by deploying the skill to a local OpenClaw instance
5. Open a pull request with a clear description

## Guidelines

- Be precise — the agent follows instructions literally. Ambiguous wording causes wrong behavior.
- Use imperative language ("Run X", "Send Y") not suggestions ("You might want to...")
- Include examples with exact CLI commands where possible
- When a workflow has multiple steps, number them explicitly
- If changing CLI behavior, coordinate with [claw3d](https://github.com/makermate/claw3d) to keep them in sync

## Testing changes

Deploy the updated skill to your local Clarvis instance:

```bash
./scripts/build-skill.sh
cp -r . ~/.clarvis/workspace/skills/claw3d
```

Then restart the gateway and test the affected workflow via Telegram/Discord.

## Reporting issues

If the agent does something unexpected, open an issue with:
- What you asked the agent to do
- What it did instead
- The relevant session logs (if available)
