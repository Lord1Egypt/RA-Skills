---
name: severity-badges
description: Full visual spec for the severity system and badges: verified contrast tokens, badge anatomy, firing conditions, the OFFICIAL TEXT chip. Read before rendering any badge or severity visual.
---

# Severity system and conditional badges (full visual spec)

Three severity levels, mapped to the escalation tiers, rendered as
flat color when the surface supports it and as spelled labels when it
doesn't (plain chat, terminal, screen readers always get the words).

**Contrast conformance.** Tokens conform to WCAG 2.2 Level AA (the
operative legal standard; WCAG 3.0 remains a Working Draft with its
contrast algorithm formally undetermined) and additionally meet APCA
Lc 75+ for badge text as a WCAG 3 readiness target. Two-token system
per level: an accent hue for non-text elements (timeline ramp
segments, markers) and a text-safe badge pairing, because a hue vivid
enough to read as neon cannot also carry small text at Lc 75.

| Level | Accent (non-text) | Badge bg + text | Badge contrast |
|---|---|---|---|
| 1, Heads up | Yellow `#F5C518` | `#F5C518` + near-black `#141414` | 11.3:1, Lc 75 |
| 2, Real weight | Orange `#E0762E` | Deep orange `#AD4A00` + white | 5.6:1, Lc 82 |
| 3, Serious | Neon red `#FF2D2D` | Deep red `#C21807` + white | 6.1:1, Lc 84 |

Accent-hue rules: vivid red and orange pass the 3:1 non-text minimum
on white and near-black surfaces; vivid yellow does not on white, so
on light surfaces any yellow accent element carries its text label or
positional cue rather than relying on the fill alone (which the
always-label rule below requires anyway). Computed 2026-08-26 (WCAG 2
relative luminance; APCA 0.0.98G-4g); re-verify if tokens change.

Severity may ramp visually from yellow through orange to red across a
timeline or organizer so graduation risk is legible at a glance. Flat
color only: no glow, halo, or pulse effects at any level, including
Level 3. Danger is communicated by hue, label, and placement, never by
animation.

**When each level fires:** Level 1 on Tier B recommendations,
unconfirmed clocks, and routine caveats. Level 2 on Tier A steps:
counter notification approach, scheduled removals, contracts, legal
correspondence received. Level 3 on Tier A with compounding: appeal on
a channel with active strikes, second or third strike exposure,
litigation intent, §512(f) territory, or a livelihood-critical flag
combined with any Tier A step.

**Badge spec.** Badges are uppercase, background color only with no
strokelines or borders, corner radius 4px maximum, and always paired
with their meaning in plain text on first appearance:

- `ACTIVE STRIKES: N` (Level 3 badge pairing at 2+, Level 2 pairing at
  1). Shown wherever the
  channel state is relevant, and drives conditional promotion (2.1).
  Only rendered when the count is known; never inferred.
- `POSSIBLE RISK` (Level 2 badge pairing). Marks a step or timeline branch that can
  escalate (an appeal branch that can convert to a removal request, a
  scheduled removal window). Identifies graduation risk before the
  user commits to the step.
- `UNCONFIRMED` (Level 1 badge pairing). Marks any timeline date the user's own
  information doesn't yet establish; pairs with the `confirm_by` check.
- `OFFICIAL TEXT` (neutral, design-system default). The nearby link
  chip to the current platform documentation for the step in view,
  opening in a new tab per S-08, and carrying the S-08 source
  metadata (accessed date; last-updated date only when the source
  states one) as minor secondary text.

Badges state facts the user gave or the platform documents. No badge
ever renders from a guess, and removing the condition removes the
badge. A Level 3 badge or warning never renders alone: the same view
always carries the concrete next step and the available off-ramp, so
red is a signal with a handle on it, never a wall. If there is no next
step to offer yet, the severity presentation waits until there is. Body copy near badges stays in the 2.3 voice: the badge is the
signal, the sentence next to it is the friend explaining it.

