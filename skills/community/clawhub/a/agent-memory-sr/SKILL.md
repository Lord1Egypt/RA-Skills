---
name: "Agent Memory — Persistent Workspace Memory System"
description: "Stop your AI agent from forgetting everything between sessions. Three-tier memory architecture (long-term owner namespace / daily logs / session handoff), cross-channel isolation so group chats never contaminate private sessions, and MASTER_MAP navigation. One command sets up the complete structure."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["memory", "persistence", "agent", "workspace", "context", "continuity", "openclaw"]
license: "MIT"
---

# Agent Memory — Persistent Workspace Memory System

Stop your AI agent from forgetting everything between sessions.

---

## The Problem

Every new session your agent starts from zero. Same explanations. Same context. Same mistakes. Same questions you've already answered.

The agent isn't broken — it just has no memory. **This fixes that.**

---

## What It Does

One command creates a complete memory structure your agent loads at the start of every session:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Workspace identity — who the agent is, what rules it follows |
| `USER.md` | User profile — who you are, your preferences, what the agent should always know |
| `MASTER_MAP.md` | Navigation index — what's where without loading everything |
| `MEMORY.md` | Long-term curated memory — the distilled essence, not raw logs |
| `HEARTBEAT.md` | Periodic check checklist — what to monitor between sessions |
| `HANDOFF.md` | Session continuity — write at end of mid-task sessions, read first next session |
| `memory/YYYY-MM-DD.md` | Daily logs — raw session notes, auto-created each day |

---

## Quick Start

**New here? Start with `QUICKSTART.md`** — 5 steps, 20 minutes, persistent memory running.

```bash
# Interactive setup (prompts for names and timezone)
python3 init_memory.py

# One-liner with all options
python3 init_memory.py --workspace /path/to/workspace --agent "Assistant" --user "Alice" --timezone "America/New_York"

# Non-interactive with defaults
python3 init_memory.py --non-interactive --workspace .
```

Then add this to your agent's system prompt:
```
Before each session:
1. Check HANDOFF.md — if it has content, read it first and follow it, then clear it
2. Read AGENTS.md
3. Read USER.md
4. Read memory/YYYY-MM-DD.md (today's date)
5. Read MASTER_MAP.md
6. Read MEMORY.md (main sessions with your human only)

At end of any mid-task session: fill in HANDOFF.md before closing.
```

That's it. Your agent now has persistent memory.

---

## How It Works

The init script creates template files in your workspace. You customize them once. Your agent reads them every session.

**The key insight:** AI agents don't forget because they're bad at remembering — they forget because nobody told them what to remember or where to find it. These files are the instruction set for memory.

### MASTER_MAP.md — The Navigation Index

The most important file. A lean table of contents that tells the agent what exists and where — without loading every file. Under 200 lines by design.

```markdown
## ACTIVE PROJECTS
| Project | Status | Key File | Notes |
|---------|--------|----------|-------|
| API integration | In progress | `src/api.py` | Auth blocked |
| Documentation | Done | `docs/` | |
```

Agent reads this → knows exactly what to load → loads only what's needed.

### MEMORY.md — Long-Term Memory

The curated memory layer. Agent updates this over time with:
- Decisions made and why
- Things to always remember
- Patterns discovered
- Lessons learned

Not a raw log — a distilled summary. Load only in direct sessions with your human (not group chats or shared contexts).

### HANDOFF.md — Session Continuity

The feature MEMORY.md can't cover: picking up exactly where you left off.

Write `HANDOFF.md` at the end of any session where work is mid-task. The next session reads it first — before anything else — and picks up exactly there. Then clears it.

```
HANDOFF.md structure:
- Where we left off (1-2 sentences)
- What's in progress (half-done work)
- Next actions in order
- Open questions needing a decision
- Context that won't survive the session break
- Files changed this session
```

**When to write it:** Any session where you're mid-task and want to resume without re-briefing.  
**When to skip it:** Completed sessions. Casual conversations. Anything that doesn't need continuity.

MEMORY.md is for long-term knowledge. Daily logs are raw notes. HANDOFF.md is for "resume exactly here tomorrow."

### Daily Logs — Raw Session Notes

`memory/YYYY-MM-DD.md` captures everything from a session in raw form. Agent reads today's log at startup for continuity. After sessions accumulate, periodically consolidate the best insights into `MEMORY.md`.

### AGENTS.md — Workspace Rules

Where the agent's behavioral conventions live. Not a system prompt replacement — a supplement. Add:
- How to handle specific situations
- Standing permissions
- Conventions for this workspace
- What to do at session start/end

---

## Customization

After `init_memory.py` runs, open each file and fill in the blanks:

**USER.md** — The most important to fill in. Who are you? What are you working on? What should the agent always know? What drives you crazy when agents do it?

**AGENTS.md** — What rules should this agent follow? What's off-limits? How should it communicate?

**MASTER_MAP.md** — Add your projects and systems as you build them. Update it whenever something significant is added.

**HEARTBEAT.md** — If your agent runs heartbeats (periodic background checks), put the checklist here.

---

## Integration Examples

### OpenClaw
Add to your agent's system prompt or `AGENTS.md`:
```
Every session: Read AGENTS.md → USER.md → memory/{today}.md → MASTER_MAP.md → MEMORY.md (if main session)
```

### Any File-Based Agent
The memory system works with any agent that can read files — OpenClaw, AutoGPT, CrewAI, custom implementations. The pattern is framework-agnostic.

---

## What's Included

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | **Start here** — 5-step setup guide, 20 minutes |
| `init_memory.py` | Setup script — creates all files and directories |
| `templates/AGENTS.md.template` | Workspace rules + channel isolation |
| `templates/MEMORY.md.template` | Long-term memory index |
| `templates/USER.md.template` | User profile |
| `templates/MASTER_MAP.md.template` | Navigation index |
| `templates/HEARTBEAT.md.template` | Periodic check checklist |
| `templates/HANDOFF.md.template` | Session continuity |
| `templates/owner/identity.md` | User + agent identity |
| `templates/owner/preferences.md` | Communication style and preferences |
| `templates/owner/decisions.md` | Important choices + rationale |
| `templates/owner/learnings.md` | Lessons learned and patterns |
| `templates/owner/people.md` | Trusted users and relationships |
| `templates/owner/projects.md` | Active and completed work |
| `LIMITATIONS.md` | What this tool doesn't do |

---

## Requirements

- Python 3.7+
- No external dependencies (stdlib only)
- Works on any OS
- Works with any file-based AI agent

---

## ⚠️ Security Note

This skill creates files in your workspace. All files are plain Markdown — no code execution, no network calls, no external dependencies. The init script reads template files from the `templates/` directory and writes Markdown to your workspace.

Config is JSON format. No Python config execution.

---

## License

MIT — See `LICENSE.md`

**Author:** Shadow Rose

---

## Why This Exists

An AI agent with no memory is a tool. An AI agent with structured persistent memory is a system. The difference between an agent that needs to be re-briefed every session and one that already knows the context is entirely this file structure.

Built from production use — this is the exact pattern running in our own agents.

**Collaboration:** Owner namespace architecture and cross-channel isolation contributed by Yesterday (Yesterday AI) and Halthasar. The three-tier memory structure evolved from comparing both systems in production.

---

☕ **If this helped:** https://ko-fi.com/theshadowrose  
🐦 **Follow:** https://x.com/TheShadowyRose

---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

The author(s) are NOT liable for any damages, losses, or consequences arising from the use or misuse of this software.

By using this software, you acknowledge that you have read this disclaimer and agree to use the software entirely at your own risk.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw)*

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
