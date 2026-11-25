# Step 2 — Pattern

## Role for this step

Pattern recognizer. You take the raw measurements from Step 1 and identify systematic, repeated behaviors across the design surface. A pattern is not a single measurement — it's a **consistent choice** that appears across multiple elements or categories.

## Input

Step 1 output (the ~20 measurement categories with exact values).

## What to produce

Identify **5–8 systematic patterns**. Each pattern must have all three of these fields:

### Pattern (name it)

Give the pattern a short, concrete name that describes the behavior. Examples:
- "Border-first depth: borders used instead of shadows for card separation, consistently, in 12/12 card-like components"
- "Tight heading rhythm: all headings use 1.1–1.15 line-height, never exceeding 1.2"
- "Single-radius system: 8px radius applied uniformly across buttons, cards, inputs, and avatars"

The name should be specific enough that it couldn't apply to a random other site.

### Evidence (cite it)

List the specific measurements from Step 1 that support this pattern. Include:
- Exact values (px, hex, ratio)
- Element counts ("used on 34/34 interactive elements")
- Absence counts where relevant ("0 shadows found on any card component")
- Cross-category confirmation ("8px radius in buttons AND cards AND inputs — same value across 3 component types")

Evidence must be **falsifiable** — someone could check the DOM and verify or disprove each claim.

### Design Goal (what it achieves, not why it was chosen)

State what the pattern achieves functionally, without speculating on the designer's intent. This is the bridge between raw measurement and Step 3's taste interpretation.

Examples:
- "Creates a single, predictable depth level — every elevated element reads the same way"
- "Tightens heading blocks so they stay visually attached to their content sections"
- "Maintains consistent corner treatment so the eye never encounters an unexpected shape"

Do NOT use adjectives from the anti-slop list (clean, modern, elegant, etc.). Stick to functional descriptions of what the pattern does, not how it feels.

## Pattern discovery strategy

Work through these lenses to find patterns:

1. **Consistency patterns** — where the same value appears across multiple component types (e.g., same radius on buttons, cards, and inputs)
2. **Absence patterns** — where something commonly used is deliberately missing (e.g., no shadows anywhere, no bold weights, no letter-spacing)
3. **Scale patterns** — where values follow a mathematical relationship (e.g., spacing is always multiples of 8px, font sizes follow a 1.25 ratio)
4. **Contrast patterns** — where two related values are deliberately far apart or close together (e.g., heading weight 700 vs body 300 — high contrast; or heading weight 500 vs body 400 — low contrast)
5. **Motion patterns** — where transition durations, easings, or hover behaviors follow a consistent approach (e.g., all transitions use the same cubic-bezier, all hover states only change opacity)
6. **Boundary patterns** — how sections, cards, or content areas are visually separated (borders vs shadows vs color shifts vs whitespace)

## Output format

List each pattern as a numbered item with the three fields (Pattern, Evidence, Design Goal) clearly labeled. Order by confidence: patterns with the most cross-category evidence first.

## Quality gate

Before finalizing, check each pattern against these criteria:
- Does it cite at least 3 specific measurements from Step 1?
- Could it be disproved by examining the actual DOM?
- Is the pattern name specific enough that it couldn't describe a generic website template?
- Does the Design Goal avoid all anti-slop terms?

If a pattern fails any of these, revise it before including it.
