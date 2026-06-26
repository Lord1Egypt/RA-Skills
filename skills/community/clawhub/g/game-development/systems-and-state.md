# Systems and State Design

Use this file when moving from prototype code to robust architecture.

## State Layers

- Session state: current run variables, score, transient events
- Meta progression state: unlocks, upgrades, persistent profile
- Configuration state: tunables and content references

Keep these layers separate so balancing changes do not break persistence.

## Deterministic System Order

Per-frame update order should be explicit:
1. consume input snapshot
2. update simulation systems
3. resolve collisions and effects
4. apply scoring and progression
5. emit events for UI/audio/VFX
6. render current frame

Changing order silently is a common source of bugs and inconsistent feel.

## Event Strategy

Use events for cross-system notifications:
- player_hit
- objective_completed
- run_failed
- reward_granted

Do not let UI modules mutate simulation truth directly.

## Save and Recovery

- Save only deterministic and necessary data.
- Version save schema from the first persisted release.
- Add migration logic when changing saved structures.
- Keep one backup snapshot to reduce corruption losses.

## Debuggability

Maintain a debug overlay that can display:
- current state name
- frame time
- entity counts
- active modifiers
- last event stream

This turns balancing and bug triage into objective work.
