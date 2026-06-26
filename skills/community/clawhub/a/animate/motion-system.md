# Motion System - Animate

Use this file when the request is still vague and needs a motion contract before implementation.

## Motion Brief

Capture these facts first:
- Stack and platform
- Surface being animated
- Trigger and user goal
- Tone: calm, direct, playful, premium, utility-first
- Accessibility and performance constraints

If any of those are unknown, resolve them before choosing effects.

## Intent Map

| Intent | What motion should do | Typical patterns |
|--------|------------------------|------------------|
| Orientation | Explain where content came from or went | shared element, slide on axis, container transform |
| Feedback | Confirm an input was registered | press state, pulse, icon morph, subtle color shift |
| Continuity | Smooth abrupt state changes | crossfade, size transform, animated content swap |
| Emphasis | Draw attention to one change | brief scale, highlight, controlled bounce substitute |
| Delight | Add character without harming speed | light stagger, tasteful flourish, celebratory success |

## Token Ladder

Default duration ranges:
- Micro feedback: 100-160ms
- State changes: 180-280ms
- Layout or overlays: 240-360ms
- Screen transitions: 300-450ms

Rules:
- Exit is usually faster than enter.
- Stagger only when hierarchy becomes clearer.
- Long motion needs a stronger reason than short motion.

## Motion Contract

Every deliverable should define:
- Trigger
- Initial state
- End state
- Duration and easing or spring
- Delay or stagger
- Cancellation and interruption behavior
- Reduced-motion fallback
- Acceptance criteria

## Acceptance Criteria

Use objective checks:
- Acknowledges input fast enough
- Preserves hierarchy and readability
- Does not trap navigation or focus
- Works under interrupted or async states
- Stays smooth on target devices
