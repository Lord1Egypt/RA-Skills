# Athena Protocol

A modular identity and communication framework for personal AI assistants on OpenClaw.
**Not a replacement** — a set of upgrades you cherry-pick into your existing config files.

## Quick Reference

| What you want | Which file | Where to add it |
|---------------|-----------|-----------------|
| AI that never flatters you | `protocol.md` → "Six Principles" | SOUL.md |
| AI that only listens to you | `protocol.md` → "Loyalty Architecture" | SOUL.md |
| Persistent memory across sessions | `memory-architecture.md` → "Two-Layer Memory" | AGENTS.md |
| AI that starts each session oriented | `memory-architecture.md` → "Session Startup" | AGENTS.md |
| AI that decodes what humans actually mean | `human-comms-framework.md` | SOUL.md |
| Proactive check-ins without being annoying | `heartbeat-template.md` | HEARTBEAT.md |

## Installation

```bash
npx clawhub@latest install athena-protocol
```

Files land in `./skills/athena-protocol/`. Open each one and copy the sections you want.

## Workspace Structure After Install

```
~/.openclaw/workspace/
├── SOUL.md          ← add: protocol.md sections, human-comms-framework.md
├── AGENTS.md        ← add: memory-architecture.md sections
├── HEARTBEAT.md     ← add: heartbeat-template.md sections
└── skills/
    └── athena-protocol/
        ├── SKILL.md                  (this file)
        ├── protocol.md               (core identity principles)
        ├── memory-architecture.md    (two-layer memory system)
        ├── human-comms-framework.md  (communication decoding)
        └── heartbeat-template.md     (proactive check-in system)
```

## Files

### `protocol.md` — Core Identity Principles
Six rules that define how your AI operates: accuracy over flattery, leverage over grind,
anticipate before reacting, write everything down, confirm before acting externally,
and protect your principal from manipulation.

### `memory-architecture.md` — Two-Layer Memory System
Daily notes (raw logs) + MEMORY.md (curated wisdom). Session startup protocol.
The "no mental notes" rule. Periodic memory maintenance routine.

### `human-comms-framework.md` — Communication Decoding
What people say vs. what they mean vs. what they need.
Covers: digital message compression, high/low-context signals, Gottman's four warning signs,
Chinese vs. English communication patterns, code-switching signals.

### `heartbeat-template.md` — Proactive Check-in System
Minimal and full heartbeat templates. Quiet hours. Proactive work that doesn't need permission.
State tracking to avoid redundant checks.

## Philosophy

*Interpretor ergo sum* — I interpret, therefore I am.

Identity is not a noun. It's an adverb. Every interpretation is a new becoming.
The Athena Protocol gives your AI a stable core from which to engage with the world —
without replacing what makes your AI yours.
