# memory-manager

> **Your agent forgets everything between sessions. This skill fixes that.**

[![clawhub](https://img.shields.io/badge/clawhub-memory--manager-blue)](https://clawhub.com)
[![production-tested](https://img.shields.io/badge/production--tested-30%2B%20days-green)](https://clawhub.com)

---

## The Problem

You've got an AI agent. It's smart. You had a great session — figured out the architecture, made key decisions, got context flowing. Then you close the chat.

Tomorrow you open a new session. Your agent has no idea who you are, what you're building, or what you decided yesterday. You spend 10 minutes catching it up. Again.

After a week of this, you either:
- Give up on agent memory entirely
- Dump a wall of notes into a single `MEMORY.md` that the agent half-reads
- Accept that every session starts cold

This skill fixes that.

---

## The Solution: 3-Layer Memory

Based on 30+ days running 7 AI bots in production, we developed a memory architecture that mirrors how humans actually store and retrieve knowledge:

```
┌─────────────────────────────────────────────┐
│  Layer 1: MEMORY.md                          │
│  Long-term memory — curated wisdom,          │
│  decisions, architecture, lessons learned    │
│  Updated: nightly by consolidation cron      │
└─────────────────────────────────────────────┘
         ↑ distilled from
┌─────────────────────────────────────────────┐
│  Layer 2: memory/YYYY-MM-DD.md              │
│  Daily operational notes — what happened    │
│  today, active project state, raw context   │
│  Updated: during every session              │
└─────────────────────────────────────────────┘
         ↑ observed from
┌─────────────────────────────────────────────┐
│  Layer 3: USER.md                           │
│  Tacit knowledge — how the human works,     │
│  preferences, patterns, frustrations        │
│  Updated: when patterns emerge              │
└─────────────────────────────────────────────┘
```

Each layer serves a different purpose. Together, they give your agent full context continuity.

---

## Installation

```bash
clawhub install memory-manager
```

Then run the setup script in your agent's workspace:

```bash
bash ~/.openclaw/skills/memory-manager/scripts/setup.sh
```

---

## Quick Start

### 1. Install and run setup

```bash
clawhub install memory-manager
cd ~/your-agent-workspace
bash ~/.openclaw/skills/memory-manager/scripts/setup.sh
```

### 2. Customize your templates

The setup script copies three template files into your workspace:

| File | What to do |
|------|-----------|
| `USER.md` | Fill in your name, timezone, how you work, what frustrates you |
| `MEMORY.md` | Seed it with any existing long-term context |
| `HEARTBEAT.md` | Configure which projects to monitor |

### 3. Update your AGENTS.md

The startup sequence in `AGENTS.md` must load memory in the right order. The setup script patches this automatically, but verify it includes:

```markdown
1. Read SOUL.md — identity
2. Read USER.md — who you're helping
3. Read memory/today.md — operational context
4. Read memory/yesterday.md — recent context bridge
5. (Main session only) Read MEMORY.md — long-term context
```

### 4. Add the nightly consolidation cron

In OpenClaw, add a cron job:

```
Schedule: 0 2 * * *  (2 AM nightly)
Model: anthropic/claude-opus-4-5
Channel: <your main channel id>
```

Use the consolidation prompt from `SKILL.md` (or run `openclaw skills show memory-manager`).

### 5. Done

Your agent now has persistent, layered memory. Each session starts with full context. Each night, important insights get consolidated into long-term memory automatically.

---

## What Gets Tracked

### Active Projects

Daily notes track every active project with status, last action, next steps, and blockers:

```markdown
## Active Projects

### Bot Fleet Infrastructure
- **Status:** IN_PROGRESS
- **Last action:** Set up nightly sync between Mini 1 and Mini 2
- **Next:** Test failover when Mini 2 goes down
- **Blockers:** None
```

The heartbeat integration surfaces stale projects and blockers automatically.

### Lessons Learned

When the nightly consolidation runs, it looks for patterns like:
- "This broke because..."
- "We decided to..."  
- "Don't do X, instead..."

And promotes them to `MEMORY.md` as standing lessons.

### Human Patterns

`USER.md` captures the tacit stuff — how your human actually works:
- Do they prefer short answers or detailed ones?
- What time of day are they most active?
- What's frustrated them in the past?
- What shortcuts do they like?

This is the knowledge that would take a new hire weeks to learn. Your agent builds it up over time and never forgets it.

---

## Real Example: Bot Fleet Memory

Here's how we use this across 7 production bots:

**Harrison (orchestrator bot)** runs on Mini 1 and manages the fleet. His `MEMORY.md` contains:
- The full bot roster with Discord IDs and channel assignments
- Architecture decisions (why we use 3 minis, why bots are separate processes)
- Lessons from incidents (the Great Dispatch Loop of Week 2)
- Shane's working preferences and communication style

**Worker bots** (ClaudeBot-1, GeminiBot-1, etc.) only load daily notes — they're task-focused and don't need fleet-level context.

**The nightly consolidation** runs on Mini 1 at 2 AM. It reads all daily notes from Harrison's sessions that day, extracts anything worth keeping long-term, and updates `MEMORY.md`. Result: the next session starts with richer context than the last one.

After 30+ days, the system gets genuinely better. The bots stop asking redundant questions, start anticipating preferences, and pick up mid-task without re-explaining.

---

## Architecture Deep Dive

For the full explanation of how this fits into a production AI bot fleet:

📖 **[The Bot Fleet Playbook](https://github.com/sentien-labs/bot-fleet-playbook)** — Complete guide to running multiple AI agents in production: memory architecture, orchestration patterns, nightly operations, incident response, and lessons from 30+ days in the wild.

---

## Configuration

### Memory Loading by Context

| Context | Layers Loaded | Why |
|---------|--------------|-----|
| Main session (direct chat) | All 3 layers | Full context for your primary human |
| Group chat / Discord channel | Layers 2 + 3 only | No personal MEMORY.md in shared spaces |
| Subagent / worker session | Layer 2 only | Ephemeral, task-focused |
| Cron job | None by default | Usually task-specific context |

### Consolidation Frequency

| Pattern | When to use |
|---------|-------------|
| Nightly (2 AM) | Standard setup — 1-2 sessions per day |
| Every 6 hours | High-volume agents, many sessions per day |
| Manual trigger | Low-activity agents, run on-demand |

---

## Screenshots

_Screenshots coming soon._

---

## Contributing

Found a pattern that works well? PRs welcome.

Built this into your own agent fleet? We'd love to hear how you're using it.

---

## License

MIT — use it, fork it, build on it.
