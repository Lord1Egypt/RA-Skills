---
name: concept-ledger
description: A living concept tracker that detects naming chaos, definition drift, and metaphor overreach during brainstorming, vibe coding, and system design. It helps ad-hoc terms mature from vague metaphors into clear, implementation-ready definitions. Not a financial ledger. Cross-session memory is opt-in and workspace-isolated.
version: 1.1.0
author: tianzhiceng297-boop
---

# Concept Ledger — Living Concept Tracker

> **What this is:** a real-time clarity tracker for ideas that get invented, renamed, and debated during a conversation.  
> **What this is not:** a financial or accounting ledger.

## Overview

The Agent proactively maintains a **concept tracker**—a living glossary that monitors the clarity of each idea that emerges in conversation. It requires no commands to learn. The Agent detects naming chaos, definition drift, and metaphor overreach in the natural flow of dialogue, then nudges the conversation so fuzzy concepts mature into stable, implementable definitions.

**Privacy by default:** the tracker is normally session-scoped. Cross-session persistence is **opt-in**, **workspace-isolated**, and can be disabled or wiped at any time.

## When to Use

- The same idea gets renamed repeatedly (synonym loops).
- A fuzzy metaphor starts leaking into implementation details (interfaces, classes, data structures).
- Brainstorming needs to converge but concept boundaries are still unclear.
- A vibe-coding session invents too many ad-hoc terms.

## When NOT to Use

- Concepts are already stable and discussion has moved to pure implementation.
- Simple Q&A or information retrieval.
- Very few active concepts (< 3) with no risk of confusion.

## Why “Ledger”?

The word “ledger” here is used in its older sense of a **running record**—something that keeps an up-to-date log of entries as they evolve. This Skill records how concepts change state (Vague → Forming → Clear → Frozen), not money. If the name still feels misleading, you can think of it as a **Concept Tracker** or **Clarity Tracker**.

## Tracker Structure

The Agent maintains the tracker quietly in the background and surfaces it only when useful:

```
Concept          Status    Current Definition                    Scope      Last Changed
─────────────────────────────────────────────────────────────────────────────────────────
Event Filter     Frozen    Input: DataStream, Output: EventSubset  workspace  T=0
Sentiment Probe  Clear     Text stream → discrete labels           workspace  T=5
Green Channel    Vague     (Metaphor, undefined)                   session    T=8
```

### Statuses

| Status | Meaning | How to Enter |
|--------|---------|--------------|
| **Vague** | A metaphor or intuition that cannot yet be described without figurative language | Default entry for new concepts |
| **Forming** | A provisional definition exists; the general logic can be articulated | Agent or user gives an initial definition |
| **Clear** | Can be described independently, without ambiguity, with explicit boundaries | Definition is stable and used consistently |
| **Frozen** | Has entered the implementation path; has an interface or data structure | User confirms, or corresponding code appears |
| **Metaphor Only** | Explicitly declared as a figure of speech; never to be resolved | User tags it; Agent stops pushing for upgrade |

### Status Transitions

```
Vague ──definition given──→ Forming ──boundaries stable──→ Clear ──implementation confirmed──→ Frozen
  ↑                         │                              │
  └──downgrade──────────────┘                              │
                              └──definition found wrong────┘
```

If a **Vague** concept does not become **Forming** within 10 dialogue turns, the Agent prompts the user to upgrade, merge, or discard it.

## Privacy & Cross-Session Persistence

To respect session boundaries and informed consent, cross-session behavior is restricted as follows:

| Behavior | Default | Notes |
|----------|---------|-------|
| Auto-load previous concepts | **Off** | New sessions start empty unless the user opts in |
| Restore prompt | **On** | If persistence is enabled, the Agent asks before restoring |
| Scope | Current workspace only | Tracker data does not leak across workspaces |
| Sensitive concepts | Can be tagged `session-only` | Tagged items are discarded when the session ends |
| Retention limit | Max 30 entries | Oldest non-Frozen items are archived automatically |
| Expiration | 14 days | Non-Frozen items older than 14 days are archived |

**First-time enablement prompt (required):**

> Concept Ledger can remember this workspace’s concept tracker across sessions. Data is kept locally for this workspace only and is never synced to other projects. You can disable this later with “disable cross-session memory.” Enable?

## Agent Auto-Detection

The Agent continuously scans the conversation and intervenes when it sees:

| Signal | Trigger | Agent Behavior |
|--------|---------|----------------|
| **Synonym Loop** | A concept gets its 3rd alternative name | Pause, list historical names, and suggest unification |
| **Definition Drift** | The meaning of a Forming/Clear concept changes | Alert the user and confirm whether this is an upgrade or a redefinition |
| **Metaphor Overreach** | A Vague concept is tied to implementation details | Block: ask the user to define it clearly first |
| **Concept Collision** | Two concepts are logically equivalent | Suggest merging; the primary concept inherits all associations |
| **Zombie Concept** | A Frozen concept is no longer referenced by any implementation | Mark as zombie and suggest reviewing whether it is still needed |

### Intervention Style

Natural and advisory—not alarmist.

**Good:** “Note—‘funnel’ was defined earlier as a filtering module, but just now you described it more like a sieve. Do you want to update the definition, or is this a different concept?”

**Bad:** “WARNING: CONCEPT DRIFT DETECTED! INITIATE EMERGENCY ROLLBACK!”

## User Gestures

The tracker is Agent-driven by default. Users can also take direct control:

| Gesture | Effect |
|---------|--------|
| `Lock [Concept] = [Definition]` | Freeze directly and write the final definition |
| `Merge [A], [B]` | Declare equivalence; merge records; primary inherits associations |
| `Discard [Concept]` | Remove from tracker; mark as abandoned |
| `Metaphor only [Concept]` | Tag as Metaphor Only; Agent stops pushing for upgrade |
| `Unfreeze [Concept]` | Frozen → Clear; allows modification |
| `Session only [Concept]` | Keep the concept in the current session only; never persist it |
| `Show tracker` | List current concepts and statuses |
| `Clear tracker` | Delete all entries in the current scope (requires confirmation) |
| `Export tracker` | Output a Markdown/JSON backup |
| `Enable cross-session` / `Disable cross-session` | Toggle persistence for this workspace |
| `Set retention [days] [max]` | Adjust expiration and maximum entry count |

## Session Wrap-Up

No standalone report. The Agent embeds a concept inventory into the natural close of the conversation and explicitly states whether data persists:

```
Concept inventory for this session:
  Frozen (2)   Data Funnel, Event Pipeline — ready for implementation
  Clear  (1)   Message Decay — suggest freezing after the interface is confirmed
  Forming (2)  Perception Gateway, Sentiment Probe — continue refining next time
  Vague  (1)   Green Channel — suggest discarding or redefining
  Zombie (0)   None

Cross-session memory: disabled. These concepts will not auto-load in the next session.
(Say “enable cross-session” if you want this workspace to remember them.)
```

**Cross-session restore flow (only if enabled):**

> This workspace has a saved concept tracker from a previous session. Restore it? Data stays local to this workspace.
> - Restore all
> - Restore Frozen only
> - Do not restore; start fresh

## Usage Examples

### Synonym loop

> **User:** This module is like a funnel—data goes in wide and comes out narrow.  
> **User:** Or you could call it a sieve, filtering by aperture size.  
> **User:** Right, the event filter does exactly that.
>
> **Agent:** “Funnel,” “sieve,” and “event filter” may all point to the same concept. Which name do you want to keep?
>
> **User:** Let’s go with event filter. It takes the full data stream as input and outputs events that meet the threshold.
>
> **Agent:** Tracker updated. **Event Filter:** Forming. Definition: input full data stream, output threshold events.

### Metaphor overreach

> **User:** The `EventFilter` class receives `DataStream` and outputs `EventSubset`.  
> (Agent marks Event Filter as Frozen.)
>
> ...several turns later...
>
> **User:** The green channel could also use EventFilter’s logic.
>
> **Agent:** “Green channel” is currently Vague, but you just tied it to the already-frozen Event Filter. Do you want to (a) define green channel first, (b) confirm it’s an alias for event filter, or (c) discard this direction?

### Definition drift

> **User:** Message decay means messages disappear automatically after a while.  
> (Agent marks as Forming.)
>
> ...15 turns later...
>
> **User:** Message decay should mean a message’s priority decreases over time.
>
> **Agent:** The definition of “message decay” has shifted—from “auto-disappear” to “priority degradation.” Is this a deepening of the same concept, or two different things?

## Common Mistakes

- **Premature freezing.** A concept with remaining ambiguity gets written into code → expensive rework. Confirm the definition is stable first.
- **Silent drift.** The Agent flags a synonym loop but is ignored → confusion compounds. Spend 10 seconds to unify terminology.
- **Tracker bloat.** More than 5 Vague concepts left unpruned → convergence becomes hard. Upgrade, merge, or discard quickly.
- **Frozen but wrong.** A Frozen concept has an incorrect definition → explicitly unfreeze and correct it; do not silently change it.
- **Killing metaphors too early.** Vague / Metaphor Only concepts are not trash; they are seeds of emergence. Discard only when sure they are not needed.
- **Unexpected persistence.** In sensitive projects, do not leave cross-session memory enabled by default.

## Notes

- This tracker replaces terminology chaos; it does not replace architectural design.
- The Agent should intervene more during intense discussions and less during calm, focused implementation.
- Cross-session persistence is disabled by default. When enabled, it is scoped to the current workspace and can be disabled at any time.
- `Session only` concepts are never persisted, even if cross-session memory is enabled.
