# Memory Template - Animate

Create `~/animate/memory.md` with this structure:

```markdown
# Animate Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Product Context
<!-- Primary products, platform stacks, and target users -->
<!-- Surfaces animated often: navigation, sheets, lists, forms, gestures -->

## Motion Goals
<!-- Intent priorities: orientation, feedback, continuity, emphasis, delight -->
<!-- Tone choices and places where motion should stay restrained -->

## Token Defaults
<!-- Approved duration tiers, easing families, spring presets, stagger limits -->
<!-- Reduced-motion substitutions and low-end device fallbacks -->

## Approved Patterns
<!-- Navigation, modal, list, loading, feedback, and gesture patterns that work -->
<!-- Notes on parity vs platform-native exceptions -->

## Risk Register
<!-- Known interruption points, performance hazards, and accessibility constraints -->
<!-- Libraries or surfaces that need extra caution -->

## QA Notes
<!-- Devices, states, and regressions that must be checked before shipping -->

## Notes
<!-- Stable insights worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining motion defaults from real work |
| `complete` | Stable motion language established | Reuse defaults unless user overrides |
| `paused` | User wants fewer setup prompts | Ask only when a critical constraint is missing |
| `never_ask` | User rejected setup prompts | Stop prompting and work silently |

## Integration Values

| Value | Meaning |
|-------|---------|
| `pending` | Activation preference not confirmed |
| `done` | Activation preference confirmed |
| `declined` | User wants manual activation only |

## Key Principles

- Store decisions that improve future motion outputs, not chat transcripts.
- Keep memory concise and implementation-oriented.
- Redact sensitive identifiers before saving notes.
- Update `last` whenever memory is edited.
