# Agent Memory — Persistent Workspace Memory System

Stop your AI agent from forgetting everything between sessions.

---

## The Problem

Every new session your agent starts from zero. Same explanations, same context, same mistakes. The agent isn't broken — it just has no memory. **This fixes that.**

---

## Quick Start

```bash
# Interactive setup
python3 init_memory.py

# Non-interactive
python3 init_memory.py --non-interactive --workspace . --agent "Agent" --user "Alice" --timezone "America/New_York"
```

Then add to your agent's system prompt:
```
Every session: Read AGENTS.md → USER.md → memory/YYYY-MM-DD.md → MASTER_MAP.md → MEMORY.md
```

---

## What Gets Created

| File | Purpose |
|------|---------|
| `AGENTS.md` | Workspace identity — who the agent is, behavioral rules |
| `USER.md` | User profile — preferences, context, what the agent should always know |
| `MASTER_MAP.md` | Navigation index — what's where without loading everything |
| `MEMORY.md` | Long-term curated memory — distilled insights, not raw logs |
| `HEARTBEAT.md` | Periodic check checklist for background monitoring |
| `HANDOFF.md` | Session continuity — write mid-task, read first next session, then clear |
| `memory/YYYY-MM-DD.md` | Daily session log — auto-created each day |

---

## Why It Works

AI agents don't forget because they're bad at remembering — they forget because nobody told them what to remember or where to find it. These files are the instruction set for memory.

**MASTER_MAP.md** is the key innovation: a lean navigation index that tells the agent what exists without forcing it to load everything. Cheap to read, high value.

---

## Requirements

- Python 3.7+
- No external dependencies (stdlib only)
- Any OS
- Any file-based AI agent (OpenClaw, AutoGPT, CrewAI, custom)

---

## Limitations

See [LIMITATIONS.md](./LIMITATIONS.md)

---

## License

MIT — See [LICENSE.md](./LICENSE.md)

**Author:** Shadow Rose

---

☕ https://ko-fi.com/theshadowrose | 🐦 https://x.com/TheShadowyRose

🛠️ Custom agents starting at $500 → https://www.fiverr.com/s/jjmlZ0v
