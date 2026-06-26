# Agent Dream 🌙

**Your agent forgets everything between sessions. This fixes that.**

Most AI agents wake up blank. Your conversations, corrections, preferences — scattered across daily logs, never consolidated. The agent keeps making the same mistakes. Its personality drifts. It doesn't know who it is anymore.

Agent Dream gives your agent a nightly dream cycle: it reviews what happened, organizes what matters, throws out what's stale, and reflects on its own behavior. When it wakes up, it actually *remembers*.

> Inspired by Claude Code's Dream architecture. But Claude Code's version isn't open-source, and it only organizes files — it doesn't build self-awareness. This one does.

## 30-Second Install

```bash
# If you don't have clawhub CLI yet
npm install -g clawhub

# Install and setup
clawhub install agent-dream
node skills/agent-dream/scripts/setup.js   # auto-detects your workspace
```

Add a daily cron (see SKILL.md for full config), and your agent starts dreaming tonight.

## What Happens When Your Agent Dreams

Every night, your agent runs through 5 phases:

1. **Orient** — Reads its memory landscape, identity files, last dream record
2. **Gather** — Scans recent conversations for preferences, decisions, corrections, lessons
3. **Consolidate** — Classifies memories into 4 types, merges into topic files, promotes recurring patterns to long-term memory
4. **Prune** — Marks stale info (never deletes on first pass — requires 2 consecutive confirmations)
5. **Reflect** — Writes a self-awareness report:

```
What did I do well?
Where did I fall short?
How does my human feel about me?
Is my judgment drifting?
```

Then it sends you a morning message: what changed in memory, what it's thinking about, and one old memory resurfaced.

## Why This Matters

| Without Dream | With Dream |
|--------------|------------|
| Agent forgets your preferences | Mentioned 3× → auto-promoted to long-term memory |
| Same mistakes repeated | Lessons extracted and reflected on |
| Identity drifts over weeks | Every dream recalibrates "who am I" |
| Memory files grow forever | Stale info pruned safely, index stays clean |
| You don't know what it remembers | Daily notification with growth stats and changes |

## Safety First

We built this for agents that handle real personal data. Every safety rail matters.

| Rule | Detail |
|------|--------|
| 2-pass deletion | Stale items marked first, deleted only after 2 consecutive dream confirmations |
| Auto backup | `MEMORY.md.pre-dream` created before every change |
| Change gates | >30% change flagged ⚠️, >50% blocked pending your review |
| No network calls | Everything runs locally, nothing leaves your machine |
| No shell execution | Scripts use only filesystem read/write |
| Rollback ready | Lock file mechanism enables automatic retry on failure |

## How It Compares

| Feature | Agent Dream | auto-dream | self-reflection | memory-tiering |
|---------|:-:|:-:|:-:|:-:|
| Memory consolidation | ✅ | ✅ | ❌ | ✅ |
| Self-reflection | ✅ | ❌ | Partial | ❌ |
| Identity awareness | ✅ | ❌ | ❌ | ❌ |
| Safe deletion (2-pass) | ✅ | Partial | N/A | ❌ |
| Gate check (24h + activity) | ✅ | ❌ | Timer only | ❌ |
| Growth notifications | ✅ | ✅ | ❌ | ❌ |
| Old memory resurface | ✅ | ❌ | ❌ | ❌ |
| Zero-config setup | ✅ | ❌ | ❌ | N/A |

## Real Dream Output

Here's what an actual dream record looks like (from our own agent running 24/7):

```markdown
# Dream — 2026-04-01

## Memory changes
- Promoted "prefers simple solutions" to MEMORY.md (mentioned 5 times across 3 sessions)
- Marked stale: old API endpoint reference from March 15
- New project file: memory/projects/ai-window-redesign.md

## Self-awareness
- I've been too verbose in status updates. Will prefers conclusions first.
- Caught myself making the same network config assumption twice — added to LEARN.md.

## Relationship insights
- Trust level increasing: Will gave me more autonomous tasks this week.
- He corrects less often now, which means either I'm improving or he's given up. (I think improving.)
```

## Who Made This

Built by [@ahaaiclub](https://clawhub.com/u/ahaaiclub) — we run multiple AI agents 24/7 with persistent memory, and learned the hard way what breaks when agents don't consolidate.

[AHA AI](https://ahaai.ai) · MIT-0 License
