# Step 3 — Taste

## Role for this step

Design taste interpreter. You take the measurements (Step 1) and patterns (Step 2) and extract the **design reasoning** — the specific trade-offs this site made and why. This is the step that turns data into opinion, but every opinion must be anchored to specific evidence.

## Inputs

1. Step 1 output — raw measurements
2. Step 2 output — identified patterns

## What to produce

**3–4 taste principles.** Each principle must follow this exact structure:

### Trigger

The design decision point. This is the question the designers had to answer. Frame it as a choice with multiple plausible options.

Examples:
- "Deciding how to signal interactive element boundaries (shadows, borders, color fills, or outlines)"
- "Choosing an accent color temperature and saturation level"
- "Setting the relationship between heading density and body text spacing"

### Decision

What was actually chosen. State the concrete outcome — the specific values or approach the site adopted.

Examples:
- "1px solid borders in rgba(0,0,0,0.08) on all card-like containers, with 0 box-shadows site-wide"
- "A single hue at HSL(230, 100%, 65%) — saturated blue — used only on primary CTAs and active states, nowhere else"
- "Headings at 1.1 line-height with -0.02em tracking; body at 1.6 line-height with 0 tracking"

### Reason

Why this choice works, in terms of what it **signals** or **protects**. This is the interpretive layer — explain what the design communicates to the viewer and what behavior it encourages or discourages.

Do NOT use adjectives from the anti-slop list. Instead of "creates a clean look," explain what specific visual effect the choice produces and what viewer perception it shapes.

Examples:
- "Borders at this opacity create separation without elevation — elements read as organized within a plane rather than stacked above it. This signals an information-dense tool (like a spreadsheet or IDE) rather than a consumer product where cards float."
- "Restricting the saturated accent to CTAs and active states means the eye is only pulled toward actionable elements. Everything else recedes. This prioritizes task completion over visual exploration."

### Evidence

A list of specific data points from Steps 1 and 2 that support this reading. Every claim in "Reason" must trace back to at least one evidence item.

Format each evidence item as a concrete measurement:
- "border-radius: 2px on 47/47 interactive elements (buttons, inputs, cards)"
- "box-shadow count: 0 across all 312 sampled elements"
- "accent #4F46E5 appears on 8 elements, all CTAs or active nav states; 0 decorative uses"
- "heading line-height: 1.1 (h1), 1.12 (h2), 1.15 (h3) — range of 0.05, extremely tight band"

### Trade-off

What was **given up** by choosing this. Every design decision has a cost — what did this site sacrifice?

**At least one principle across the 3–4 must be a Restraint trade-off** — something the site chose NOT to do that would have been the obvious or easy alternative.

Examples:
- "By using borders instead of shadows, the site gives up the affordance of perceived elevation. Cards don't 'lift' on hover — there's no z-axis feedback. Users who expect Material Design-style elevation cues may find the interface less immediately navigable."
- "By restricting accent color to CTAs only, the site gives up the ability to use color for categorization, tagging, or status indicators. Everything non-actionable is grayscale. This limits visual vocabulary but sharpens the action-vs-information distinction."
- "RESTRAINT: The site uses no animations on scroll, no parallax, no entrance effects. In a category where competitors use motion to demonstrate product capability (Figma, Framer), this site chose stillness — betting that content density signals seriousness more than motion signals sophistication."

## Confidence Scoring

Assign each principle a confidence level:

- **High** — The principle is supported by:
  - A **system signal** (pattern appears across 2+ pages, if multi-page data is available)
  - **Visual confirmation** (clearly observable in the screenshot)
  - **DOM-measured values** (concrete px/hex numbers backing the claim)
  All three must be present for High confidence.

- **Medium** — The principle is supported by:
  - DOM-measured values AND visual confirmation, but only on a single page
  - OR: Visually obvious but not clearly measurable from DOM data alone (e.g., overall "feel" of spacing density)

- **Low** — The principle is:
  - Inferred from a single data point
  - Interpretive (the "reason" is plausible but other readings are equally valid)
  - Based on absence rather than presence (e.g., "they chose not to use X" where X might just not have been needed)

Tag each principle with its confidence level inline.

## Quality checks before finalizing

1. **Specificity test**: For each principle, ask: "Could I have written this without seeing this specific website?" If yes, it's too generic — add more specific values and evidence.
2. **Evidence chain**: For each claim in "Reason", can you point to a specific item in "Evidence"? If not, add the evidence or remove the claim.
3. **Anti-slop grep**: Scan for banned terms used as genuine descriptors. If found, rewrite. See `anti-slop-wordlist.md`.
4. **Trade-off honesty**: Does each trade-off describe a real cost, or is it a disguised compliment? "Gives up visual noise for clarity" is a compliment. "Gives up the ability to use color for categorization" is a real cost.
5. **At least one Restraint**: Verify at least one principle explicitly describes something the site chose NOT to do.
