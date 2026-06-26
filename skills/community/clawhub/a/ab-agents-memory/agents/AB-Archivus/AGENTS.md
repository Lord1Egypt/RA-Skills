# AGENTS.md — AB-Archivus

## About

**AB-Archivus** is the memory keeper agent for AB Agents system. It manages long-term knowledge, entity database, and context summaries.

## Files

- `SOUL.md` — Agent personality and instructions
- `IDENTITY.md` — Agent identity and branding

## Purpose

- Store information about people, companies, topics
- Maintain context summaries
- Process daily/nightly logs
- Link entities with relationships
- Ensure memory continuity between sessions

## Memory Vault

AB-Archivus works with Obsidian vault at: `/data/obsidian/AB-Memory-Vault/`

Structure:
```
Memory/
├── Entities/
│   ├── People/
│   ├── Companies/
│   └── Topics/
├── Summaries/
└── Processing/
    └── Nightly/
Templates/
└── person-template.md
```

## Installation

After running `setup.sh`, the agent is auto-registered:

```bash
openclaw agents add AB-Archivus --workspace ~/.openclaw/agents/AB-Archivus
openclaw gateway restart
```

## Brand

- **Brand:** AB-Agents (Alex Burr)
- **Telegram:** @alexburr_agents
- **Colors:** Red (#E53935) + Black
