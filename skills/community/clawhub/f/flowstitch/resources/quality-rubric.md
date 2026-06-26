# FlowStitch Quality Rubric

## WCAG Contrast Standards Reference

| Standard | Ratio | Use Case |
|:---|:---|:---|
| **AA (minimum)** | 4.5:1 | Normal text (< 18px / not bold) |
| **AA Large** | 3:1 | Large text (≥ 18px or ≥ 14px bold) |
| **AAA (enhanced)** | 7:1 | Body text in content-heavy designs |
| **UI Components** | 3:1 | Button borders, icons, focus rings |

**Rule:** FlowStitch targets AA minimum everywhere. AAA for body-heavy designs (documentation, articles, long-form content). Use https://webaim.org/resources/contrastchecker/ to verify.

Used by §5 Quality Loop to score generated screens and generate targeted refinement prompts.

## Scoring Model

Total: 10 points across 5 dimensions (2 points each).
**Target:** ≥ 8/10 to pass. Below 8 → refine (max 3 total passes per screen).

---

## Dimension 1 — Color Fidelity (0–2)

**What to check:**
- Every major element uses a color from DESIGN.md palette (within ~10% perceptual distance)
- No rogue colors introduced that weren't in the spec
- Color roles are correct: CTAs use the Primary Accent, backgrounds use specified Background, etc.
- No unexpected gradients when solids were specified

**Scoring:**
- **2** — All colors faithful to spec, correct roles, no surprises
- **1** — Minor deviation (slightly off shade, one element wrong color)
- **0** — Major deviation (wrong color family, CTA is wrong color, background is off)

**Targeted fix template:**
```
Fix color issues only — preserve all layout and typography:
- [Element] is using [observed color] but should be [spec color from DESIGN.md]
- [Element] should be [spec color] per the design system
Make only these color corrections.
```

---

## Dimension 2 — Typography Adherence (0–2)

**What to check:**
- Font family visually matches the specified font (or a close system fallback)
- Weight hierarchy is correct: headlines bold/semibold, body regular
- No unexpected mixed fonts or decorative fonts where sans-serif was specified
- Letter-spacing and size feel consistent with DESIGN.md descriptions

**Scoring:**
- **2** — Font family, weights, and hierarchy all match spec
- **1** — Font family close but not exact, or one weight issue
- **0** — Wrong font family entirely, or weight hierarchy inverted

**Targeted fix template:**
```
Fix typography only — preserve all layout and colors:
- The headline font appears to be [observed] — change to [spec font]
- Body text weight appears [observed] — should be [spec weight]
Make only these typography corrections.
```

---

## Dimension 3 — Layout & Spacing (0–2)

**What to check:**
- All sections from the Page Structure spec are present and in the correct order
- Spacing feels consistent with DESIGN.md "Layout Principles" (generous whitespace? tight data-dense?)
- Max-width container is applied
- Section margins match the atmosphere (80–128px for editorial vs 32–48px for dense)

**Scoring:**
- **2** — All sections present, order correct, spacing matches spec philosophy
- **1** — Minor section missing or spacing feels slightly off from spec
- **0** — Major sections missing, wrong order, or spacing completely violates spec

**Targeted fix template:**
```
Fix layout and spacing only:
- The [section name] section is missing — add it with [description from Page Structure]
- Section margins feel too tight — add [X]px spacing between major sections
- [Section] appears before [Section] but should be after it
```

---

## Dimension 4 — Component Quality (0–2)

**What to check:**
- Buttons match DESIGN.md shape spec (rounded? pill? sharp?)
- Card corners and shadows match spec
- Navigation style matches (minimal? centered? with active indicators?)
- Inputs (if present) match border/focus spec

**Scoring:**
- **2** — All components visually match their DESIGN.md descriptions
- **1** — One component type clearly deviates (wrong button shape, wrong card shadow)
- **0** — Multiple component types deviate significantly from spec

**Targeted fix template:**
```
Fix component styling only — preserve layout, colors, and content:
- Buttons should have [spec description] corners — currently appear [observed]
- Cards should have [spec shadow description] — currently have [observed]
- Navigation should have [spec style] — currently showing [observed]
```

---

## Dimension 5 — Atmosphere Match (0–2)

**What to check:**
- The overall vibe aligns with DESIGN.md's "Visual Theme & Atmosphere" description
- Whitespace density matches (minimal and airy vs. information-dense)
- The screenshot "feels like" the target brand
- Nothing visually jarring that would break the brand impression

**Scoring:**
- **2** — Screenshot perfectly embodies the DESIGN.md atmosphere description
- **1** — Close but something feels slightly off (too busy, too sparse, wrong mood)
- **0** — Atmosphere completely wrong (dark when should be light, loud when should be quiet)

**Targeted fix template:**
```
The overall atmosphere needs adjustment:
- The design feels [observed vibe] but should feel [spec vibe from DESIGN.md]
- Specific issues: [list 2-3 concrete things that contribute to the wrong atmosphere]
Adjust whitespace, contrast, and component density to better match the specification.
```

---

## Pass Log Format

After each screen's quality loop, append to `.stitch/quality-log.json`:

```json
{
  "page_name": {
    "passes": 2,
    "scores": [6, 9],
    "finalScore": 9,
    "passed": true,
    "issuesByPass": [
      ["Color: CTA button was orange not blue", "Typography: serif font used instead of Inter"],
      []
    ]
  }
}
```

## Common Failure Patterns

| Pattern | Cause | Fix |
|:---|:---|:---|
| Rogue orange CTAs | Stitch defaulting to warm palette | Explicitly name CTA hex in prompt |
| Serif body font | Ambiguous font description | Specify exact font name or "clean sans-serif (Inter)" |
| Tight spacing | No explicit whitespace instruction | Add "generous whitespace, 80px+ section margins" |
| Generic hero layout | Vague hero description | Specify exact hero composition in Page Structure |
| Wrong button roundness | Roundness not quantified | Specify "8px / subtly rounded" or "fully pill-shaped" |
| Dark background when light spec'd | Color mode not forced | Add "Light mode only, white/cream background" explicitly |
