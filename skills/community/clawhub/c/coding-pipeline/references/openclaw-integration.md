# OpenClaw Integration

Complete setup for running `coding-pipeline` inside an OpenClaw workspace.

## Overview

OpenClaw uses workspace-based prompt injection — `SKILL.md` content is injected into every session automatically when the skill is installed. Unlike Claude Code, you don't need to configure hooks; the workspace engine handles it.

## Installation

**Via ClawdHub (recommended):**

```bash
clawdhub install coding-pipeline
```

This places the skill at `~/.openclaw/workspace/skills/coding-pipeline/` and registers it in the workspace manifest.

**Manual:**

```bash
mkdir -p ~/.openclaw/workspace/skills/coding-pipeline
cp -r ./coding-pipeline/* ~/.openclaw/workspace/skills/coding-pipeline/
```

Then rebuild the workspace index:

```bash
openclaw workspace reindex
```

## Workspace Structure

After installation:

```
~/.openclaw/workspace/
├── AGENTS.md                 # Multi-agent coordination patterns
├── SOUL.md                   # Behavioral guidelines, personality
├── TOOLS.md                  # Tool capabilities and gotchas
├── MEMORY.md                 # Long-term memory
├── memory/                   # Daily memory files
└── skills/
    └── coding-pipeline/      # This skill
        ├── SKILL.md          # Injected at session start
        ├── references/       # Loaded on demand
        ├── scripts/          # Accessible to the agent
        ├── assets/           # Templates
        └── hooks/openclaw/   # Hook manifest (empty by default)
```

## Promotion Targets

When a learning from `coding-pipeline` Phase 4 failures turns into a durable rule, promote it to the workspace files:

| Target | What Belongs There |
|--------|--------------------|
| `AGENTS.md` | Multi-agent workflows that use the pipeline (e.g. "spawn a phase-tracker sub-agent for long refactors") |
| `SOUL.md` | Behavioral rules like "Never skip Phase 1 even for obvious-looking fixes" |
| `TOOLS.md` | Pipeline-specific tool patterns (e.g. "use phase-check.sh to track state across session pauses") |

Promotion example:

A learning emerges from 3 repeated Phase 4 failures on NestJS DI issues. Promote it to `SOUL.md`:

> **NestJS DI debugging:** Phase 1 hypothesis for any DI error must explicitly name the module boundary where injection fails. Cross-module DI issues are almost always missing `exports:` in the providing module.

Future sessions now get this rule at session start and skip the dead end.

## Inter-Session Coordination

If you run multiple OpenClaw sessions in parallel (e.g. one pairs with Telegram, another does local dev), they share the same `.learnings/` directory. This means Phase 4 failures logged in session A become visible to session B on next task start.

Use `sessions_history` and `sessions_send` to coordinate:

- Session A: exhausts Phase 4, logs to `.learnings/ERRORS.md`
- Session B (invoked later): reads `.learnings/ERRORS.md` at Phase 1, sees the dead ends, starts with a better hypothesis

## Pipeline State Directory

The skill uses `.pipeline-state/` to track phase progression during a task:

```
.pipeline-state/
├── current-phase              # Contains "1" | "2" | "3" | "4"
├── activity.log               # Timestamped phase transitions
└── attempts-<task>.md         # Per-task attempt log (Phase 4)
```

This directory is created on first use by `scripts/phase-check.sh`. Add to `.gitignore` by default — it's local session state, not shared repository content.

```gitignore
.pipeline-state/
```

## Hook Manifest

`hooks/openclaw/HOOK.md` and `hooks/openclaw/handler.js` are present but empty by default. OpenClaw's workspace injection makes hooks unnecessary for this skill — the SKILL.md is already loaded. If you want phase-start reminders beyond the description match, you can populate `handler.js` with a custom hook, but it's not required.

## Comparing with Claude Code

| Aspect | Claude Code | OpenClaw |
|--------|-------------|----------|
| Activation | Hook via `.claude/settings.json` + skill description | Workspace injection at session start |
| Reminder overhead | ~80 tokens per prompt (hook) | 0 tokens per prompt (baseline injection) |
| Cross-session state | Per project | Shared workspace (inter-session messaging) |
| Promotion targets | `CLAUDE.md` | `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md` |
| Best for | Single-project discipline | Multi-project consistent behavior |

If you use both, install via ClawdHub in OpenClaw and configure the hook in `~/.claude/settings.json` so Claude Code sessions get the reminder too.
