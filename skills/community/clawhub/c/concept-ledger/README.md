# Concept Ledger — Living Concept Tracker

A lightweight ClawHub Skill that stops naming chaos before it becomes technical debt.

```bash
openclaw skills install @tianzhiceng297-boop/concept-ledger
```

## What it does

During brainstorming, vibe coding, or system design, conversations invent a lot of ad-hoc terms. The same idea gets renamed three times. A fuzzy metaphor becomes a class name. Yesterday’s “funnel” becomes today’s “filter” and tomorrow’s “pipeline.”

**Concept Ledger** keeps a live tracker of those ideas, watches for trouble signals, and nudges the conversation so vague metaphors mature into clear, implementation-ready definitions.

## What it is NOT

- Not a financial or accounting ledger.
- Not an architecture design tool.
- Not a replacement for a real glossary or documentation system.

Think of it as a **clarity coach** that sits in the background and speaks up only when terminology starts drifting.

## Key signals it catches

| Signal | What it means |
|--------|---------------|
| **Synonym Loop** | The same concept gets renamed repeatedly |
| **Definition Drift** | A previously defined concept starts meaning something else |
| **Metaphor Overreach** | A vague metaphor is pushed into code or interfaces before it is defined |
| **Concept Collision** | Two different names turn out to describe the same thing |
| **Zombie Concept** | A frozen concept is no longer referenced anywhere |

## Privacy by default

- Cross-session memory is **disabled by default**.
- If enabled, it is **workspace-isolated** and asks before restoring.
- Sensitive concepts can be marked `session only` so they are never persisted.
- You can wipe, export, or disable the tracker at any time.

## Quick gestures

- `Show tracker` — see current concepts and their status
- `Lock [Concept] = [Definition]` — freeze a definition
- `Merge [A], [B]` — merge two equivalent concepts
- `Discard [Concept]` — remove a concept
- `Session only [Concept]` — keep a concept in the current session only
- `Enable cross-session` / `Disable cross-session` — toggle persistence
- `Export tracker` — back up the tracker as Markdown/JSON

## Learn more

See `SKILL.md` for the full behavior specification, status machine, examples, and privacy controls.
