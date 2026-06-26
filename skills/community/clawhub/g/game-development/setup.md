# Setup - Game Development

Read this when `~/game-development/` is missing or empty.
Keep setup concise and oriented to fast first-playable outcomes.

## Operating Priorities

- Ship a playable loop early.
- Align technical profile with user constraints.
- Preserve decisions so new agent sessions can continue without reset.

## First Activation Flow

1. Clarify what the user wants to ship now:
- one playable browser prototype
- a reusable game framework
- a production-ready game with roadmap

2. Confirm delivery profile and constraints:
- browser instant (no build) or structured build workflow
- 2D, 2.5D, or 3D scope
- single-player only or online features
- target devices and performance expectations

3. Confirm design direction and preferences:
- genres and references the user likes
- visual style and camera style
- preferred complexity and timeline

4. If context is approved, initialize local workspace:
```bash
mkdir -p ~/game-development
touch ~/game-development/{memory.md,concept-briefs.md,user-preferences.md,system-decisions.md,playtest-log.md,roadmap.md,release-notes.md}
chmod 700 ~/game-development
chmod 600 ~/game-development/{memory.md,concept-briefs.md,user-preferences.md,system-decisions.md,playtest-log.md,roadmap.md,release-notes.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Prefer browser instant profile for first playable iteration.
- Keep first milestone under one core loop and one win/lose condition.
- Apply performance budgets before expanding assets.
- Add backend dependencies only when user goals require them.

## What to Save

- selected delivery profile and platform scope
- concept pillars and target player fantasy
- technical decisions and rejected alternatives
- test outcomes and balancing changes
- release risks and next milestone

## Guardrails

- Never lock users into complex infrastructure for simple prototypes.
- Never claim readiness without at least one complete playtest cycle.
- Never skip documenting major pivots in local memory files.
