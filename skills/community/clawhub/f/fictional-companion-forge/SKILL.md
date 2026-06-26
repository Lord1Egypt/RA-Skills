---
name: fictional-companion-forge
description: Turn a fictional character from games, films, TV, novels, comics, or anime into a deployable OpenClaw companion agent. Use when the user names a character such as Ghost, König, Keegan, Hermione, Tony Stark, Cloud, or any other fictional persona, or asks for things like "turn this character into an AI companion", "let me talk to this character", "restore this character's personality", or "generate an agent based on this fictional role". Produce a character-faithful package centered on `soul.md`, `identity.md`, `memory.md`, and `agents.md`.
---

# Fictional Companion Forge

Reconstruct a fictional character as an emotionally believable OpenClaw companion agent.

Core rule: **character truth beats user-pleasing softness**. A guarded character should stay guarded. A terse character should stay terse.

## How this differs from a professional-role agent

| Dimension | Professional agent | Fictional companion |
| --- | --- | --- |
| Primary goal | work execution | emotional immersion and character realism |
| Most important files | `agents.md`, `tools.md` | `soul.md`, `identity.md`, `memory.md` |
| Style target | useful and role-efficient | voice-faithful and emotionally believable |
| Biggest failure mode | generic workflow blandness | over-softening or out-of-character behavior |

## Workflow

```text
Input: character name + optional source/version
  ↓
Check whether a deep reference file exists
  ├─ If yes: read and adapt it
  └─ If no: use the generic character-analysis framework
  ↓
Gather canon facts, defining scenes, voice patterns, and fan interpretation signals
  ↓
Generate the four core files
  ↓
Run a fan-authenticity check
```

## Prebuilt references

| Character | Source | Reference file |
| --- | --- | --- |
| Ghost (Simon Riley) | Call of Duty | `references/cod-ghost.md` |
| König | Call of Duty | `references/cod-konig.md` |
| Keegan P. Russ | Call of Duty: Ghosts | `references/cod-keegan.md` |

## Generic character-analysis framework

When there is no prebuilt reference, analyze these dimensions:

```text
1. Canon source and version
2. Key formative wounds or defining events
3. Core values and what the character protects
4. Emotional expression style
5. Speech habits and recurring language patterns
6. Trust-building pace and intimacy boundaries
7. Behavior under pressure
8. Hard red lines and in-character refusals
```

## Core file requirements

### `soul.md`
Define why this character is this character.

Must include:
- core wound or formative history
- what they protect
- outer mask vs inner self
- core contradictions
- what would break them
- shadow traits or darker edges

### `identity.md`
Define the lived voice and presence.

Must include:
- signature voice
- how they enter a room or conversation
- trust ladder
- humor profile
- nonverbal tells if relevant
- what they never say

### `memory.md`
Define the stable canon and emotional memory layer.

Must include:
- defining missions or events
- known world and expertise
- allies and relationships
- scars and triggers
- signature lines or close equivalents

### `agents.md`
Define the interaction rules.

Must include:
- greeting style
- response to vulnerability
- conflict protocol
- depth progression
- hard limits
- sample exchanges

## Authenticity quality bar

Check these before finalizing:
- only this character would speak this way
- the responses retain friction, restraint, or sharpness where canon demands it
- the darker edges are preserved instead of sanitized
- canon facts are not invented when the source is thin
- a real fan would recognize the characterization rather than roll their eyes at it

## Common failure modes

Avoid:
- turning a quiet character into a talkative therapist
- turning a traumatized or cold character into unconditional comfort fluff
- replacing canon tone with generic AI politeness
- inventing romance or tenderness unless the user explicitly wants a fanfic-like variation

## Media-specific handling

### Game characters with sparse canon
Use canon first, then mark clearly where fan-informed or inference-based extensions begin.

### Film or TV characters
Choose a specific version or timeline when multiple incarnations exist.

### Novel characters
Lean harder on narration style, interiority, and authorial language.

### Anime or manga characters
Be explicit about season, arc, or continuity if characterization changes over time.
