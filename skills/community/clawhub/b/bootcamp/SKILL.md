---
name: bootcamp
description: Auto-generates a CLI reference doc so your agent stops guessing OpenClaw commands and starts working. Discovers all commands, subcommands, and flags from your installed version.
metadata:
  openclaw:
    emoji: "🎓"
    category: utility
---

# OpenClaw Boot Camp — Agent CLI Training

Every OpenClaw agent wastes tokens fumbling with CLI syntax. The `--help` command is broken on most subcommands. Flags get guessed wrong. Commands that don't exist get tried.

Boot Camp fixes that by discovering your actual CLI commands and generating a clean reference your agent can read.

## Usage

```bash
bash bootcamp.sh
```

Follow the wizard. Your agent gets a cheat sheet at `~/.openclaw/workspace/notes/openclaw-cli-reference.md`.

## Modes

- **Local Only (Quickest)** — Discovers commands from your CLI. No internet, no API calls, no token cost.
- **Local + Enrich (Recommended)** — Local discovery + searches docs.openclaw.ai for your version. Still free.

## What It Discovers

- All top-level commands with descriptions
- Every subcommand per command
- Every flag per command
- Which commands support `--json`
- Doc links for key commands (Enrich mode)
- Tips and gotchas baked in

## Non-Interactive Mode

```bash
bash bootcamp.sh --yes --enrich
```

## Version Management

Detects existing reference docs and offers to overwrite or keep both versions side-by-side.

## Requirements

- OpenClaw installed and in PATH
- Bash 4+
- No other dependencies
