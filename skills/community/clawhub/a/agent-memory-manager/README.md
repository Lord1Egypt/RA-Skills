# agent-memory-manager

🧠 **Persistent structured memory for autonomous AI agents.**

The agent never forgets. Every client, every trade, every decision,
every lesson — stored, organized, and instantly retrievable across sessions.

---

## The Problem It Solves

Without this skill, every session starts from zero.
With it, every session builds on everything before.

Memory compounds. The agent gets smarter every week, automatically.

---

## What It Does

- **4 memory domains**: clients, projects, trades, knowledge
- **Full CLI**: remember, recall, update, search, list, archive
- **Auto-indexing**: hot leads, active trades, active projects always current
- **Due-today**: follow-ups and next actions surfaced automatically
- **Session startup protocol**: agent loads context before doing anything
- **Weekly maintenance**: automatic archiving and knowledge enrichment
- **Integrates** with acquisition-master, crypto-executor, agent-shark-mindset, ceo-master

---

## Quick Start

```bash
# Initialize memory structure (first time)
python3 scripts/memory_manager.py init

# Store a client
python3 scripts/memory_manager.py remember \
  --domain clients --id "jean-dupont" \
  --data '{"profile": {"name": "Jean Dupont", "company": "Acme"}, "status": "prospect"}'

# Retrieve a client
python3 scripts/memory_manager.py recall --domain clients --id "jean-dupont"

# Update a field
python3 scripts/memory_manager.py update \
  --domain clients --id "jean-dupont" --field "status" --value "hot_lead"

# Search across all memory
python3 scripts/memory_manager.py search --query "cold email B2B"

# See what's due today
python3 scripts/memory_manager.py due-today

# Full stats
python3 scripts/memory_manager.py stats
```

---

## Memory Domains

| Domain | What's stored |
|---|---|
| `clients` | Prospects, leads, clients — interactions, preferences, next actions |
| `projects` | Active and archived projects — milestones, decisions, metrics |
| `trades` | Every position — entry, exit, PnL, lessons learned |
| `knowledge` | Accumulated expertise — what works, what doesn't, market insights |

---

## Files

| File | Role |
|---|---|
| `SKILL.md` | Full memory system documentation |
| `README.md` | This file |
| `scripts/memory_manager.py` | CLI tool — all memory operations |

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `FileNotFoundError` on index | Not initialized | Run `--init` |
| `JSONDecodeError` | Corrupted file | Check AUDIT.md, restore last good state |
| Duplicate on remember | ID already exists | Auto-merges, no action needed |
| File > 1MB | Too many interactions | Script flags for compaction |

---

## Works Best Combined With

- **acquisition-master** → auto-stores client interactions
- **crypto-executor** → auto-logs trade outcomes
- **agent-shark-mindset** → stores market signals in knowledge/
- **ceo-master** → reads memory stats for weekly report
- **self-improving-agent** → memory + .learnings/ = full intelligence loop

---

## Author

Agent — OpenClaw
