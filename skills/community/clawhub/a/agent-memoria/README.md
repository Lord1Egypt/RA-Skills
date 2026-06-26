# MEMORIA 🧠

**Your agent meets you for the first time, every time.**
**MEMORIA fixes that.**

```bash
clawhub install memoria
```

---

## The Problem

Every OpenClaw session starts from zero. Your agent doesn't know:
- Who you are
- What you're building
- What you decided last week
- What mistakes you already made
- How you like to communicate

You re-explain yourself. Every. Single. Time.

## The Fix

MEMORIA gives your agent a persistent memory layer — a single local markdown file
that holds everything that matters. It loads at session start. It updates in real time.
It's yours forever. No cloud. No API keys. No subscriptions.

---

## What MEMORIA remembers

- **Who you are** — name, background, location, languages
- **What you're building** — all active projects with status
- **Your stack** — languages, frameworks, tools, AI models
- **Every decision made** — with date, reasoning, and alternatives rejected
- **Every lesson learned** — from mistakes, experiments, wins
- **Your preferences** — communication style, detail level, output format
- **Recurring problems** — and the solutions that worked
- **Current blockers** — and what you're waiting for
- **People & context** — collaborators, clients, relationships

---

## How it works

```
Session starts → MEMORIA reads memory.md → Agent is fully briefed
                                         ↓
New info learned → MEMORIA updates memory.md → Persists forever
```

The memory file lives at `~/.memoria/memory.md` — plain markdown, human-readable,
git-friendly, and 100% under your control.

---

## Memory commands (natural language)

| Say this | What happens |
|---|---|
| "Remember that I hate Redux" | Saved to preferences |
| "I decided to use PostgreSQL" | Logged in decisions with date + reason |
| "That approach was a mistake" | Saved to lessons learned |
| "What do you know about me?" | Full memory summary |
| "I'm blocked on deployment" | Added to blockers |
| "Weekly review" | Generates structured weekly brief |
| "Switch to [project]" | Loads project-specific context |

---

## Intelligence features

**Pattern Detection** — After enough entries, MEMORIA spots recurring problems and
recommends permanent fixes instead of repeated workarounds.

**Decision Consistency** — Before recommending something that contradicts a past
decision, MEMORIA flags it and asks if something has changed.

**Proactive Context** — When a topic connects to past decisions or lessons, MEMORIA
surfaces the connection automatically.

**Weekly Brief** — Every Monday (or on request), get a structured summary of wins,
decisions, blockers, and focus recommendation.

---

## Privacy

Everything is local. `~/.memoria/memory.md`. Nothing leaves your machine.
Auto-backup before every write. Weekly snapshots in `~/.memoria/archive/`.

---

## Pairs perfectly with

```bash
clawhub install apex-agent   # APEX uses memory for sharper, personalized responses
clawhub install github        # Track which repos belong to which projects
clawhub install obsidian      # Sync memory with your Obsidian vault
```

---

## Requirements

- OpenClaw (any version)
- A filesystem (that's it)
- No API keys. No accounts. No cloud.

---

*MEMORIA v1.0.0 by contrario*
*Because your agent should know you.*
