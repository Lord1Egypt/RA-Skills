# ClawHub Skill Card — Concept Ledger

## Short description (one-line pitch)

A living concept tracker that turns naming chaos, synonym loops, and fuzzy metaphors into clear, implementation-ready definitions.

## Full description

**Concept Ledger** is a clarity tracker for conversations that invent a lot of terminology—brainstorming, system design, and vibe coding.

The Agent watches for five common failure modes:

- **Synonym loops** — the same idea gets renamed over and over
- **Definition drift** — a concept quietly changes meaning
- **Metaphor overreach** — a fuzzy metaphor is pushed into code before it is defined
- **Concept collisions** — two names describe the same thing
- **Zombie concepts** — a frozen idea is no longer used

Each concept moves through a simple maturity model: **Vague → Forming → Clear → Frozen**, with an optional **Metaphor Only** state for figures of speech that should never be resolved.

**Not a financial ledger.** “Ledger” here means a running record of how ideas evolve, not bookkeeping. You can also read it as a **Concept Tracker** or **Clarity Tracker**.

**Privacy-first:** cross-session memory is opt-in and workspace-isolated. By default, nothing persists after the session ends.

## Install command

```bash
openclaw skills install @tianzhiceng297-boop/concept-ledger
```

## Tags / keywords

concept tracker, clarity tracker, naming, terminology, brainstorming, vibe coding, system design, glossary, metaphor detection, definition drift

## Best for

- Brainstorming sessions that need to converge
- Vibe coding with lots of invented terms
- System design discussions where metaphors leak into interfaces

## What users should know before installing

This Skill intervenes in the natural flow of conversation when it detects terminology problems. It does not replace architecture work or documentation. Cross-session memory is disabled by default and must be explicitly enabled per workspace.
