# Design Eval Rubric (2025/2026)

Score each view 0–5 on every dimension. A view's score is the **weighted
average**; the whole-app score is the weighted average across views plus the
cross-view dimension. The bar for "pass" is **5.0** unless the user relaxes it.

These are the things that actually separate shipped-quality from prototype-grade
today — not taste alone, but enforceable checks.

| # | Dimension | Weight | What 5/5 looks like |
|---|---|---|---|
| 1 | **Reference fidelity** | 1.0 | If matching a reference (e.g. ChatGPT, Claude, Material 3, Apple HIG), the language reads true — spacing, type, nav model, motion all match. No tells that it's an imitation. |
| 2 | **Visual hierarchy & typography** | 1.0 | One obvious focal point per view. Optical letter-spacing on display sizes, `text-wrap: pretty` on prose, deliberate scale steps. No competing weights. |
| 3 | **Spacing & layout rhythm** | 1.0 | Consistent spacing scale, aligned grids, panels feel intentional not flat. No cramped or floating elements. |
| 4 | **Color & contrast (WCAG)** | 1.5 | All text ≥ AA (4.5:1 body, 3:1 large). Status colors legible in both themes. No sub-AA "faint" meta text. **Verify actual ratios, don't eyeball.** |
| 5 | **Touch ergonomics** | 1.5 | Every interactive target ≥ 44px (iOS) / 48dp (Android). No 38px icon buttons. Adequate spacing between tap targets. |
| 6 | **Motion & micro-interactions** | 1.0 | Purposeful entrance/transition motion on a real easing curve, press feedback (`:active`), one decisive flourish. Not static, not over-animated. |
| 7 | **Accessibility (focus / RM / live)** | 1.5 | `:focus-visible` rings on all controls (shape-correct), `prefers-reduced-motion` override, `aria-live`/`role=log` for dynamic content, `role`+`aria-checked`/`aria-selected` state on toggles/segments, focus-trap + `inert` on overlays, Escape closes top overlay. |
| 8 | **Depth & detail polish** | 1.0 | Hairline elevation where it helps, scroll affordances (fade masks), focus glow on inputs, no flat/unfinished surfaces. |

## Whole-app dimension (Phase 5 only)

| # | Dimension | Weight | What 5/5 looks like |
|---|---|---|---|
| 9 | **Cross-view consistency & coherence** | 2.0 | Shared theme/accent applies everywhere, navigation is coherent, no orphan surfaces, every destination reachable, state persists, no dead items anywhere. |

## Scoring discipline

- **Score against the file, not the description.** Open the artifact, trace the
  actual markup/JS — don't grade the intent.
- **Name the blocker.** Every sub-score under 5 must come with the specific thing
  keeping it down (selector, missing attribute, measured ratio), so the fix is
  actionable.
- **Common real bugs that silently cap scores:** undefined CSS custom properties
  (token renders colorless), occluded panels (wrong z-index / stacking), dead
  chevrons (row with no destination), focus ring forcing wrong `border-radius`
  on round buttons, `fill` set on the SVG element so a descendant recolor misses.
- **No false 5/5.** If the ceiling is a structural rewrite (native controls,
  focus-trap, swipe-to-dismiss) that's out of scope, report the honest score and
  the named gap. Do not round up.
