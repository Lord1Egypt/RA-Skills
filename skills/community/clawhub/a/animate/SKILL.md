---
name: Animate
slug: animate
version: 1.0.0
homepage: https://clawic.com/skills/animate
description: Animate app and web UIs across Flutter, React, SwiftUI, Compose, and React Native with motion systems, guardrails, and reduced-motion fallbacks.
changelog: Initial release focused on app, web, and React animation systems, implementation guardrails, and QA.
metadata: {"clawdbot":{"emoji":"MOTION","requires":{"bins":[],"config":["~/animate/"]},"os":["linux","darwin","win32"],"configPaths":["~/animate/"]}}
---

## When to Use

User needs motion designed or implemented inside a product UI. Agent turns vague requests into motion contracts, stack-specific implementation choices, and testable acceptance criteria across Flutter, React, Next.js, SwiftUI, Compose, React Native, and broader web stacks.

Use this for micro-interactions, navigation transitions, shared-element flows, loading states, gesture feedback, and motion system design. Do not use it for video editing, GIF rendering, or media encoding.

## Architecture

Memory lives in `~/animate/`. If `~/animate/` does not exist, run `setup.md`. See `memory-template.md` for structure and status fields.

```text
~/animate/
|- memory.md             # Durable motion preferences and platform context
|- tokens.md             # Approved duration, easing, and spring ladders
|- patterns.md           # Proven interaction and transition patterns
|- platform-notes.md     # Stack-specific implementation decisions
`- qa.md                 # Regressions, low-end findings, and accessibility notes
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Motion system and spec contract | `motion-system.md` |
| Platform routing by stack | `platform-routing.md` |
| Starter snippets by stack | `implementation-snippets.md` |
| Common app animation patterns | `pattern-catalog.md` |
| Performance and accessibility guardrails | `performance-accessibility.md` |
| QA and regression checks | `qa-playbook.md` |

## Core Rules

### 1. Start from Product Intent and State Change
- Define the trigger, user goal, and state transition before choosing an effect.
- Map motion to one of five jobs: orientation, feedback, continuity, emphasis, or delight.
- If the intent is unclear, do not animate yet.

### 2. Write a Motion Contract Before Code
Every proposal must specify:
- Trigger and affected surfaces
- Initial state, end state, and reduced-motion fallback
- Duration, easing or spring, delay or stagger, and cancellation behavior
- Acceptance criteria: responsiveness, accessibility, parity, and performance

No vague wording like "smooth" or "premium" without values.

### 3. Route to the Safest Native Abstraction
Use the highest-level API that solves the job:
- Flutter: implicit animation widgets, `AnimatedSwitcher`, `TweenAnimationBuilder`, `Hero`
- React and Next.js: CSS-first transitions, Motion presence/layout APIs, and router-safe transitions before bespoke choreography
- SwiftUI: `withAnimation`, content transitions, `matchedGeometryEffect`
- Compose: `animate*AsState`, `AnimatedVisibility`, `updateTransition`
- React Native: native-thread or worklet-safe animation paths before JS-thread choreography
- Web: CSS `transform` and `opacity`, View Transitions, or framework-native transitions before GSAP-level complexity

Avoid low-level animation code when a higher-level primitive already handles interruption and lifecycle.

### 4. Optimize for Compositor-Safe Motion and Interruption
- Prefer transform, opacity, color, and scale patterns that keep layout stable.
- Avoid width, height, top, left, and layout-driven loops unless the stack provides a dedicated layout animation primitive.
- Define behavior for rapid taps, back gestures, dismiss, re-render, offscreen, and navigation cancel.
- Users should never get stuck behind an animation.

### 5. Ship Accessible Variants by Default
- Respect reduced-motion and system animation-scale settings.
- Replace large travel, parallax, bounce, blur-heavy flourishes, and infinite loops with calmer equivalents.
- Never rely on movement alone to communicate status.
- Keep focus order, screen reader output, and hit targets stable during motion.

### 6. Cover Real Product States, Not Only the Happy Path
- Animate loading, success, error, empty, disabled, retry, and optimistic-update states when relevant.
- Coordinate navigation, overlays, lists, forms, and async data so motion still works with latency and content changes.
- Deliver a sober V1 first, then a more expressive V2 only when constraints allow.

### 7. Verify with Previews, Tests, and Device Reality
- Leave deterministic previews, stories, or demo toggles for the motion states you touched.
- Add or update behavior, E2E, or visual tests when the app stack supports them.
- Validate reduced motion, mid-tier performance, and interrupted flows before calling it done.

## Common Traps

- Pretty animation without a user-facing reason -> extra motion, less clarity.
- Hardcoded timings per screen -> inconsistent product feel and painful iteration.
- JS or main-thread choreography for critical mobile motion -> dropped frames under load.
- Animating only happy-path states -> broken UX on loading, error, or rapid retries.
- Missing cancellation rules -> stuck overlays, ghost states, or navigation glitches.
- Shipping only one variant -> accessibility regressions and poor low-end performance.

## Security & Privacy

**Data that leaves your machine:**
- None by default from this skill itself.

**Data that stays local:**
- Motion preferences, approved tokens, platform notes, and QA learnings under `~/animate/`.

**This skill does NOT:**
- Upload builds, videos, or telemetry automatically.
- Modify files outside `~/animate/` for memory.
- Disable accessibility settings.
- Modify its own `SKILL.md`.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `flutter` - Widget lifecycles and performance rules useful for Flutter motion.
- `react` - Component and rendering patterns that shape animation behavior in React apps.
- `react-native` - Mobile lifecycle and animation-thread constraints for React Native.
- `swift` - Swift and SwiftUI implementation patterns for Apple platforms.
- `android` - Android and Compose implementation details for native motion.

## Feedback

- If useful: `clawhub star animate`
- Stay updated: `clawhub sync`
