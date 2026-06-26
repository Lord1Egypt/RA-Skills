---
name: Agent Rule Pilot
description: "Say 'sync my agent configs' to write coding rules once and sync to Claude Code, Cursor, Copilot, Windsurf, and 4 more agents."
version: 3.0.0
metadata:
  openclaw:
    emoji: "🔄"
    homepage: https://github.com/SingggggYee/dotpilot
    os:
      - macos
      - linux
---

# Rule Pilot

You use Claude Code, Cursor, Copilot, and other AI agents — but each has its own config file. Edit one, the others go stale. This skill keeps them all in sync from a single `RULES.md`.

## Quick start

Just say:

- **"sync my agent configs"** — sync RULES.md to all your AI agents
- **"check config drift"** — see which configs have gone out of sync
- **"create RULES.md"** — generate a starter rules file for your project
- **"convert CLAUDE.md to cursorrules"** — one-off format conversion

## Supported agents (8)

| Agent | Config file |
|-------|------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Aider | `.aider.conf.yml` |
| Codex CLI | `AGENTS.md` |
| Cody | `.sourcegraph/cody.json` |
| Continue.dev | `.continuerc.json` |

## Links

- GitHub: [SingggggYee/dotpilot](https://github.com/SingggggYee/dotpilot)

---

*Below are instructions for Claude Code. You can ignore this section.*

## Instructions

Detect which agent configs exist, then pick the right mode:

**RULES.md exists** → Sync to all agent configs. Each agent gets common rules + agent-specific extensions (e.g., Claude Code gets "use Read not cat"). Show diff before writing.

**No RULES.md, but configs exist** → Reverse-extract common rules into a new `RULES.md`. Flag conflicts. Ask user to resolve.

**Nothing exists** → Detect language from package.json/Cargo.toml/pyproject.toml/go.mod, generate opinionated `RULES.md`.

**Drift check** → Compare configs against RULES.md or each other. Report which are in sync, which diverged.

**Per-agent overrides:** RULES.md supports `<!-- agent:xxx -->` / `<!-- /agent:xxx -->` markers for agent-specific rules.

**Rules:** Always show diffs before writing. Preserve agent-specific sections not in RULES.md. Only generate configs for agents the user actually uses. Validate output format (JSON, YAML).
