# Agent Memory Protocol

<p align="center">
  <strong>A structured memory management skill for OpenClaw agents — three-layer density, session reflection, and flush protocol</strong>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/clawhub-agent--memory--protocol-brightgreen?style=for-the-badge" alt="ClawHub">
  <img src="https://img.shields.io/badge/OpenClaw-skill-orange?style=for-the-badge" alt="Skill">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License">
</p>

An [OpenClaw](https://github.com/openclaw/openclaw) skill that gives your agents a consistent, structured memory system. Defines where and how to write information, how to retrieve it efficiently, and when to flush to avoid context loss — all in one protocol that all agents in a multi-agent stack can follow.

## Why

As agents handle more tasks and sessions accumulate, memory becomes fragmented. Without a protocol:
- The same fact is written in multiple places and drifts out of sync
- Important decisions get buried in session logs and lost after compaction
- Agents waste tokens reading everything instead of navigating to the right file

This skill solves all three.

## What's Inside

### Three-Layer Density Structure

| Layer | File | Purpose |
|-------|------|---------|
| **L0** | `MEMORY.md` | Minimal index — 1-3 sentences per category + path pointers. Always read first. |
| **L1** | `memory/INDEX.md` | Category overview navigation (~500-1000 words). |
| **L2** | `memory/user/` `memory/agent/` | Full details, read on demand. |

Retrieval cost scales with need: L0 is always fast; only drill to L2 when you need the detail.

### Six-Category Write Spec

```
New information → classify
  ├── User identity/background → user/profile.md
  ├── Preferences/habits → user/preferences/[topic].md
  ├── Projects/tools/people → user/entities/[type].md
  ├── Key decisions/events → user/events/YYYY-MM-[name].md  (append-only)
  ├── New task type handled → agent/cases/[name].md          (append-only)
  └── Reusable pattern found → agent/patterns/[name].md
```

### Session Reflection

At session end, extract one pattern if the session contained corrections, failures, or better-approach discoveries. Patterns promoted to instincts after ≥3 occurrences.

### Flush Checklist

Six items to scan before session end or compaction — catches what's easy to forget:
preferences, project progress, decisions, entity updates, patterns, corrections.

### Context Pressure Protocol

Thresholds at 50 / 70 / 85% context usage, each with escalating flush urgency.

### Sub-Agent Write Rules

Clear rules for which agent writes what, and how the orchestrator syncs L0/L1 indexes.

## Installation

```bash
clawhub install agent-memory-protocol
```

Or clone directly:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/OttoPrua/openclaw-memory-manager.git memory-manager
```

## Usage

The skill activates automatically when any memory-related operation is triggered. Load it manually when needed:

```
Read the memory-manager skill and follow its protocol for this write.
```

Trigger words: `remember this`, `update memory`, `memory write`, `flush memory`

## Directory Layout (after setup)

```
memory/
├── INDEX.md                    ← L1 navigation
├── user/
│   ├── profile.md
│   ├── preferences/
│   │   ├── learning.md
│   │   ├── lifestyle.md
│   │   ├── tech.md
│   │   └── communication.md
│   ├── entities/
│   │   ├── tools.md
│   │   └── people.md
│   └── events/
└── agent/
    ├── cases/
    └── patterns/
```

## External Tools & Integration

The skill protocol defines the write/read rules. The actual retrieval infrastructure uses two external tools:

- **[qmd](https://github.com/tobilen/qmd)** — local semantic search over `memory/` and `blackboard/` Markdown files (powers `memory_search`)
- **[LosslessClaw](https://github.com/martian-engineering/lossless-claw)** — DAG-based context compression; stores compressed session summaries recoverable via `lcm_grep` / `lcm_expand`

Full setup guide → **[MEMORY-STACK.md](MEMORY-STACK.md)**

## Related

- [OpenClaw](https://github.com/openclaw/openclaw) — the core gateway
- [OpenClaw Docs](https://docs.openclaw.ai) — full documentation
- [ClawHub: agent-memory-protocol](https://clawhub.ai/OttoPrua/agent-memory-protocol) — install from ClawHub
- [Discord](https://discord.gg/clawd) — community

## License

MIT
