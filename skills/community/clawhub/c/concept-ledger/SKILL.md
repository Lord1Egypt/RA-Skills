---
name: concept-ledger
description: Use when conversations produce many ad-hoc terms, metaphors get reused with shifting meanings, or the same idea gets renamed multiple times. Triggers: term confusion, synonym loops, vague concepts entering implementation, naming chaos in brainstorming, vibe coding, or system design sessions.
---

# Concept Ledger

## Overview

The Agent proactively maintains a concept ledger—a living glossary that tracks the clarity of every concept. No user commands to learn. The Agent automatically detects naming chaos, intervenes at the right moment in natural conversation rhythm, and helps concepts evolve from vague to implementable.

## When to Use

- The same concept gets renamed repeatedly (synonym loops)
- Fuzzy metaphors appear in implementation contexts such as interfaces or data structures
- Brainstorming needs to converge, but concept boundaries are unclear
- Vibe coding sessions generate a large number of ad-hoc terms

## When NOT to Use

- Concepts are already stable; discussion has moved to pure technical implementation
- Simple Q&A or information retrieval
- Very few active concepts (<3), no tracking needed

## Ledger Structure

The Agent maintains this in the background, invisible to the user. Displays on demand when needed:

```
Concept          Status    Current Definition                    Last Changed
─────────────────────────────────────────────────────────────────────────────
Event Filter     Frozen    Input: DataStream, Output: EventSubset     T=0
Sentiment Probe  Clear     Text stream → discrete sentiment labels    T=5
Green Channel    Vague     (Metaphor, undefined)                      T=8
```

### Statuses

| Status | Meaning | How to Enter |
|--------|---------|--------------|
| Vague | Metaphor or intuition; cannot be described without figurative language | Default entry for new concepts |
| Forming | Has a provisional definition; general logic can be articulated | Agent or user provides an initial definition |
| Clear | Can be described independently and without ambiguity; boundaries are explicit (you know what it is *not*) | Definition is stable and used consistently |
| Frozen | Entered implementation path; has an interface or data structure | User confirms, or corresponding implementation appears in code |
| Metaphor Only | Explicitly declared as a figure of speech; never to be resolved | User tags it; Agent will not push for upgrade |

### Status Transition Conditions

```
Vague ──definition given──→ Forming ──boundaries stable──→ Clear ──implementation confirmed──→ Frozen
  ↑                         │                              │
  └──downgrade──────────────┘                              │
                              └──definition found wrong────┘
```

If a vague concept fails to become Forming within 10 dialogue turns, the Agent prompts the user to decide: upgrade, merge, or discard.

## Agent Auto-Detection

The Agent continuously scans the conversation. When the following signals appear, it intervenes:

| Signal | Trigger Condition | Agent Behavior |
|--------|-------------------|----------------|
| Synonym Loop | A concept gets its 3rd alternative name | Pause, list historical names, suggest unification |
| Definition Drift | The meaning of a Forming/Clear concept changes | Alert: meaning shift detected; confirm whether this is an upgrade or a redefinition |
| Metaphor Overreach | A vague concept is tied to implementation details | Block: please define clearly before entering implementation |
| Concept Collision | Two concepts are logically equivalent | Suggest merging; the primary concept inherits all associations |
| Zombie Concept | A Frozen concept is no longer referenced by any implementation | Mark as zombie; suggest reviewing whether it is actually needed |

### Intervention Style

Natural conversational tone. The Agent is an advisor, not a referee.

**Good**: "Note—'funnel' was previously defined as a filtering module, but just now you said it works more like a sieve. Do you want to update the definition, or is this a different concept?"

**Bad**: "WARNING: FOSSIL LAYER DRIFT! RECOMMEND IMMEDIATE ROLLBACK TO WORKING LAYER FOR RE-AUDIT!"

## User Gestures (Optional)

The ledger is Agent-driven by default. Users may also take active control:

| Gesture | Effect |
|---------|--------|
| `Lock [Concept] = [Definition]` | Freeze directly; write the final definition |
| `Merge [A], [B]` | Declare equivalence; merge records; primary concept inherits all associations |
| `Discard [Concept]` | Remove from ledger; mark as abandoned direction |
| `Metaphor only [Concept]` | Tag as Metaphor Only; Agent stops pushing for upgrade |
| `Unfreeze [Concept]` | Frozen → Clear; allow modification |

## Session Wrap-Up

Does not generate a standalone report. Embeds a concept inventory into the natural closing:

```
Concept inventory for this session:
  Frozen (2)   Data Funnel, Event Pipeline — ready for implementation
  Clear  (1)   Message Decay — suggest freezing after confirming the interface next time
  Forming (2)  Perception Gateway, Sentiment Probe — continue refining next time
  Vague  (1)   Green Channel — suggest discarding or redefining
  Zombie (0)   None
```

This inventory also serves as the entry point for the next session. At the start of the next conversation, the Agent automatically loads the previous session's Clear / Forming / Frozen items.

## Usage Examples

### Agent proactively detects a synonym loop

> User: This module is like a funnel—data goes in wide and comes out narrow.
> User: Or you could call it a sieve, filtering by aperture size.
> User: Right, the event filter does exactly that.
>
> Agent: "Funnel," "sieve," and "event filter" may all point to the same concept. I suggest unifying the name—which do you think is most accurate?
>
> User: Let's go with event filter. It takes the full data stream as input and outputs events that meet the threshold.
>
> Agent: Ledger updated. Event Filter: Forming. Definition: input full data stream, output threshold events.

### Metaphor overreach

> User: The EventFilter class receives DataStream and outputs EventSubset.
> (Agent marks Event Filter as Frozen)
> ... several turns later ...
> User: The green channel could also use EventFilter's logic.
>
> Agent: "Green channel" is currently Vague in the ledger, yet it was tied to the already-frozen Event Filter. Do you want to: (a) first define what green channel is, (b) confirm it's just an alias for event filter, or (c) discard this direction?

### Definition drift

> User: Message decay means messages disappear automatically after a while.
> (Agent marks as Forming)
> ... 15 turns later ...
> User: Message decay should mean a message's priority decreases over time.
>
> Agent: The definition of "message decay" has shifted—from "auto-disappear" to "priority degradation." Is this a deepening of the same concept, or two different things?

## Common Mistakes

- **Premature freezing**: A concept with remaining ambiguity gets written into code → rework cost is extremely high. Confirm the definition is stable before freezing.
- **Silent drift**: The Agent flagged a synonym loop but was ignored → confusion doubles in the next conversation. Spend 10 seconds to unify terminology.
- **Ledger bloat**: More than 5 vague concepts left unpruned → convergence becomes difficult. Vague items should be upgraded, merged, or discarded quickly.
- **Frozen but wrong**: A Frozen concept is found to have an incorrect definition → explicitly unfreeze and correct it; do not silently change it (lineage will be lost).
- **Eliminating metaphors**: Vague / Metaphor Only concepts are not trash; they are seeds of emergence. Only discard when you are sure they are not needed.

## Notes

- The ledger replaces terminology chaos; it does not replace architectural design.
- The Agent's intervention frequency should adapt to conversation density—intervene more during intense discussions, less during calm ones.
- Across sessions, the Agent automatically restores the previous session's Clear / Forming / Frozen items. Vague items are not retained across sessions unless the user marks them for retention.
