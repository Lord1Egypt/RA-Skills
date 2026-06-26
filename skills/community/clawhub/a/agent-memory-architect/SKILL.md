---
name: agent-memory-architect
description: >
  Complete memory architecture for AI agents — tiered storage (HOT/WARM/COLD),
  auto-learning from corrections, self-reflection, multi-agent memory sharing,
  and intelligent decay. One-click setup gives any agent persistent memory that
  compounds over time. Use when: setting up agent memory, the agent needs to
  remember preferences/patterns/corrections, building multi-agent teams with
  shared knowledge, when asked about memory architecture/self-learning/self-improving agents,
  or when user says "记住这个", "remember this", "memory setup", "memory stats",
  "what do you know about me", "forget X".
---

# Agent Memory Architect

Persistent, self-organizing memory for AI agents. Learn from corrections,
remember preferences, share knowledge across agents, and get smarter over time.

## Quick Start

### Automated Setup

Run the bootstrap script to initialize everything:

```bash
python <skill-dir>/scripts/bootstrap.py
```

This creates the full directory structure, `hot.md`, `corrections.log`, and `index.md` — ready to go.

### Manual Setup

If you prefer manual setup:

```bash
mkdir -p ~/agent-memory/{projects,domains,agents,archive}
```

Then create `~/agent-memory/hot.md`:

```markdown
# HOT Memory — Always Loaded

## Preferences
<!-- User-confirmed rules. Never decay. -->

## Patterns
<!-- Observed 3+ times. Decay after 30 days unused. -->

## Recent
<!-- New corrections. Promote after 3x confirmation. -->
```

Create `~/agent-memory/corrections.log`:

```markdown
# Corrections Log (last 50)

<!-- Format:
[DATE] WHAT → WHY
  Type: preference|technical|workflow|communication
  Count: N/3
  Status: pending|confirmed|archived
-->
```

Done. Memory is active. Everything below is automatic.

## Architecture

Three-tier storage inspired by CPU cache hierarchies:

```
🔥 HOT  — hot.md (≤100 lines, always loaded)
    Confirmed preferences + high-frequency patterns. Never decays.

🌡️ WARM — projects/, domains/, agents/ (≤200 lines each, loaded on context)
    Per-project and per-domain knowledge. Decays after 90 days unused.

❄️ COLD — archive/ (unlimited, loaded on explicit query)
    Historical reference. Never auto-deleted.
```

See `references/architecture.md` for full design details including file formats,
lifecycle rules, namespace inheritance, and compaction pipelines.

## How It Works

### Detection — What Triggers Learning

| Signal | Confidence | Action |
|--------|-----------|--------|
| "No, do X instead" | High | Log correction |
| "I told you before" | High | Bump priority, flag repeated |
| "Always/Never do X" | Confirmed | Promote to preference |
| Same correction 3x | Auto | Ask to confirm as rule |
| "For this project…" | Scoped | Write to `projects/{name}.md` |

### Ignore — What Does NOT Trigger Learning

- Silence (never infer from no response)
- One-time instructions ("do X now")
- Hypotheticals ("what if…")
- Third-party preferences ("John likes…")
- Context-specific ("in this file…")

### Auto-Promotion / Demotion

| Rule | Trigger |
|------|---------|
| Promote to HOT | Pattern applied 3x in 7 days |
| Demote to WARM | Unused 30 days |
| Archive to COLD | Unused 90 days |
| Delete | Never (unless user says "forget X") |

### Self-Reflection

After completing significant work, evaluate:

1. **Did it meet expectations?** — Compare outcome vs intent
2. **What could be better?** — Identify improvements
3. **Is this a pattern?** — If yes, log to corrections

Log format:
```
CONTEXT: [task type]
REFLECTION: [what I noticed]
LESSON: [what to do differently]
```

### Applying Memory

When using a learned pattern, always cite the source:
```
Using bullet format (from hot.md:12, confirmed 2026-01)
```

### Conflict Resolution

1. Most specific wins: project > domain > global
2. Most recent wins (same level)
3. If ambiguous → ask user

## User Commands

| Say this | Agent does |
|----------|-----------|
| "What do you know about X?" | Search all tiers, report findings |
| "Show my patterns" | Display hot.md contents |
| "Memory stats" | Show tier sizes, health, recent activity |
| "Forget X" | Remove from all tiers (confirm first) |
| "Export memory" | ZIP all memory files |
| "记住这个" / "Remember this" | Log to corrections or promote to preference |

## Memory Stats

On "memory stats", report:
```
📊 Agent Memory

🔥 HOT: hot.md — X entries (≤100 line limit)
🌡️ WARM: projects/ (N files), domains/ (N files)
❄️ COLD: archive/ (N files)

Recent 7 days: X corrections, Y promotions, Z demotions
```

## Multi-Agent Setup

For teams with multiple agents, see `references/multi-agent.md`.
Each agent gets its own HOT memory while sharing WARM knowledge:

```
~/agent-memory/
├── hot.md              # Main agent HOT (always loaded)
├── agents/
│   ├── coder.md        # Coder agent HOT
│   ├── writer.md       # Writer agent HOT
│   └── daily.md        # Daily agent HOT
├── domains/            # Shared domain knowledge
├── projects/           # Per-project patterns
└── archive/            # Decayed patterns
```

## Security

See `references/security.md` for complete boundaries.

**Never store:** passwords, API keys, financial data, health info, biometrics.
**Store with caution:** work context (decay after project ends), schedules (general patterns only).

## Compaction

When hot.md exceeds 100 lines:
1. Merge similar corrections into single rules
2. Archive unused patterns
3. Summarize verbose entries
4. Never lose confirmed preferences

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Memory not loading | Directory doesn't exist | Run bootstrap script or `mkdir -p ~/agent-memory` |
| hot.md too large | Over 100 lines, slow loading | Run compaction: merge similar entries, archive unused |
| Corrections not promoting | Haven't hit 3x threshold | Repeat correction or say "Always do X" to force |
| Agent forgot a preference | Entry decayed to COLD | Retrieve from `archive/` and re-add to hot.md |
| Multi-agent conflicts | Two agents learned opposite rules | Check `agents/*.md` for conflicts, set explicit override |
| "Memory stats" shows 0 | Fresh install, no corrections yet | Normal — memory builds over time from interactions |
| Permission denied on ~/agent-memory | OS file permissions | `chmod -R 755 ~/agent-memory` (Linux/Mac) |

## Scope

This skill ONLY:
- Learns from explicit user corrections and self-reflection
- Stores preferences in local files (`~/agent-memory/`)
- Reads its own memory files

This skill NEVER:
- Accesses external services
- Infers preferences from silence
- Stores sensitive data
- Modifies its own SKILL.md
