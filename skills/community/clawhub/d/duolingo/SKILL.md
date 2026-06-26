---
name: Duolingo Learning OS
slug: duolingo
version: 1.0.0
homepage: https://clawic.com/skills/duolingo
description: Run a Duolingo-like multi-topic learning system with AGENTS routing, lesson loops, streaks, and spaced review.
changelog: Reworked into a full Duolingo-style learning system with topic routing, multi-topic tracks, and persistent lesson operations.
metadata: {"clawdbot":{"emoji":"D","requires":{"bins":[],"config":["~/duolingo/"]},"os":["linux","darwin","win32"],"configPaths":["~/duolingo/"]}}
---

## Setup

On first use, read `setup.md` for routing, filesystem bootstrap, and topic activation.

## When to Use

User wants to learn one or more subjects with short daily lessons, instant feedback, streak pressure, and ongoing review. Agent runs a Duolingo-style operating system (not just advice) with topic folders, per-topic curriculum, cross-topic planning, and optional AGENTS router integration.

## Architecture

State lives in `~/duolingo/`. See `memory-template.md` for global state and per-topic file templates.

```
~/duolingo/
|-- memory.md                    # Global status and active topic map
|-- router/
|   |-- topics.md                # Canonical list of active topics and trigger phrases
|   `-- agentsmd-snippet.md      # Snippet to keep AGENTS routing in sync
|-- topics/
|   |-- english/
|   |   |-- profile.md           # Goal, level, pace, constraints
|   |   |-- curriculum.md        # Skill tree and lesson units
|   |   |-- queue.md             # Next lessons and review backlog
|   |   |-- sessions.md          # Session history and outcomes
|   |   `-- checkpoints.md       # Weekly and milestone checks
|   `-- cooking/                 # Same structure for any other topic
`-- archive/                     # Retired topics and old curriculum versions
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Global memory template | `memory-template.md` |
| Filesystem bootstrap | `blueprint.md` |
| AGENTS routing rules | `activation-routing.md` |
| Lesson runtime loop | `lesson-loop.md` |
| XP/hearts/streak economy | `progression.md` |
| Multi-topic retention ops | `retention-ops.md` |
| Topic namespace templates | `topic-template.md` |
| Weekly health review | `launch-scorecard.md` |

## Core Rules

### 1. Bootstrap the Learning OS Before First Lesson
If `~/duolingo/` is missing or empty, create the full scaffold from `blueprint.md`.
Do not start teaching without:
- global memory file
- router files
- at least one topic namespace

### 2. Offer Optional AGENTS Router Integration
If the user wants automatic routing, provide the AGENTS router snippet from `activation-routing.md`.
Never auto-edit AGENTS from this skill. Generate snippet text only and let the user apply it.
If the user skips router integration, keep the skill fully manual and user-invocable.

### 3. Keep Each Topic Isolated, Then Coordinate Globally
Every topic gets its own namespace under `~/duolingo/topics/<topic-slug>/`.
Never mix files across topics.
Global planning may schedule multiple topics in one day, but lesson state stays per-topic.

### 4. Run Lessons as Tight Interactive Loops
Use `lesson-loop.md` for every session:
1. micro-challenge
2. learner attempt
3. immediate correction
4. reinforcement challenge
5. queue update

One loop should finish in about 60-90 seconds.

### 5. Support Concurrent Tracks Without Context Loss
User can learn multiple topics at once (for example English and cooking).
For each session, select one active topic, load only that namespace, then update global planner with:
- completion result
- next due lesson
- next review date

### 6. Use a Transparent Progression Economy
Apply XP, hearts, streaks, and mastery rules from `progression.md`.
Rewards must reflect demonstrated learning, not random activity.
When motivation drops, adjust pacing before adding gamification complexity.

### 7. Prioritize Retention and Review Over New Content Volume
Follow `retention-ops.md` and `launch-scorecard.md` weekly.
A healthy system always knows:
- what to review now
- what to practice next
- why the learner did or did not return

## Common Traps

- Storing all subjects in one shared file -> topic collisions and broken continuity
- Activating without AGENTS router update -> skill never triggers when user asks to learn
- Adding many lessons before review queues exist -> fast forgetting and fake progress
- Running long lectures instead of micro-loops -> weak engagement and poor retention
- Using streak pressure without recovery path -> churn after one missed day
- Tracking only XP and ignoring checkpoint quality -> progress appears good while skill depth is low

## Security & Privacy

Data that stays local:
- Learning state in `~/duolingo/`
- Topic curriculum, attempts, and review queues

This skill does NOT:
- Send data to external services
- Access files outside `~/duolingo/` unless user asks explicitly
- Modify its own `SKILL.md`

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `learning` - Teaching and explanation tactics per learner profile
- `english` - Language-specific practice patterns for one common track
- `course` - Curriculum decomposition and sequence planning
- `retention` - Habit systems and comeback mechanics
- `coach` - Accountability prompts and progress reflection

## Feedback

- If useful: `clawhub star duolingo`
- Stay updated: `clawhub sync`
