# Memory Template - Brave Browser

Create `~/brave/memory.md` with this structure:

```markdown
# Brave Browser Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What Brave is used for and why -->
<!-- Example: Daily browsing in one profile, automation in a separate profile -->

## Environment
<!-- OS, install path, preferred profile layout, and automation constraints -->

## Site Compatibility
<!-- Reusable per-site Shields or extension notes -->

## Safety Boundaries
<!-- No-go actions, cleanup limits, wallet/sync rules, remote-debugging posture -->

## Notes
<!-- Durable operating observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining Brave operating defaults |
| `complete` | Profiles, limits, and typical fixes are stable | Reuse defaults unless the environment changes |
| `paused` | User wants less overhead | Save only critical browser facts |
| `never_ask` | User rejected persistence | Operate statelessly |

## Key Principles

- Store browser operating boundaries, not browsing history.
- Keep per-site fixes short and scoped to the smallest reversible change.
- Record which profile is safe for testing and which one must stay untouched.
- Update `last` on each meaningful Brave session.
