# Memory Template - Game Development

Create `~/game-development/memory.md` with this structure:

```markdown
# Game Development Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Project Snapshot
project_name: pending
delivery_profile: browser_instant | browser_structured | engine_path
genre: pending
camera_style: pending
target_platforms: browser_desktop | browser_mobile | mixed
project_phase: concept | prototype | vertical_slice | production | polish | launch

## Player Promise
- Core fantasy this game should deliver
- Who the game is for
- Why this concept should exist

## User Preferences
- Themes and aesthetics to prioritize
- Mechanics they enjoy
- Mechanics to avoid
- Time and complexity constraints

## Core Loop
- Moment-to-moment action
- Objective and fail state
- Progression hook

## System Decisions
- State architecture approach
- Physics/collision approach
- Rendering pipeline choice
- Save/persistence strategy

## Performance Budgets
- Frame target and frame-time budget
- Draw-call and memory targets
- Asset limits by type

## Playtest Log Summary
- Latest playtest date
- Main friction points
- Main balancing changes

## Roadmap
- Current milestone
- Next milestone
- Blockers

## Risks
- Technical risks
- Design risks
- Scope risks

## Notes
- Stable assumptions
- Useful references and constraints

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Work is active | Keep gathering context and shipping increments |
| `complete` | Goal reached for this scope | Focus on polish or handoff |
| `paused` | User paused work | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Skip setup questions unless user asks |

## File Templates

Create `~/game-development/playtest-log.md`:

```markdown
# Playtest Log

## YYYY-MM-DD
- Build/version:
- Test objective:
- Session type:
- Observed friction:
- Balance action taken:
- Follow-up task:
```

Create `~/game-development/system-decisions.md`:

```markdown
# System Decisions

## YYYY-MM-DD - Decision Title
- Context:
- Decision:
- Alternatives considered:
- Tradeoffs:
- Revisit trigger:
```

## Key Principles

- Keep notes short, factual, and reusable.
- Track decisions and outcomes, not brainstorming noise.
- Update `last` whenever status or milestone changes.
