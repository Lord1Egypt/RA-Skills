# Quality Review

## Scoring Categories

Evaluate the final mark across these seven dimensions. Score 1–10 for each.

### Distinctiveness

- **What to check**: Does this mark stand out from competitors? Would it be confused with another brand? Is it unique enough to trademark?
- **10**: Entirely novel, instantly recognizable, impossible to confuse.
- **5**: Competent but generic, could belong to several brands in the category.
- **1**: Direct copy or derivative of an existing well-known mark.
- **Common issues**: Overused symbols (generic swoosh, overused animal, common geometric shape without twist), category clichés (lightbulb for ideas, globe for international, puzzle piece for solutions).
- **Improvement path**: Introduce an unexpected element, twist the metaphor, combine two unrelated concepts, or simplify to an unusual silhouette.

### Memorability

- **What to check**: Will audiences recall this mark after a single glance? Can they describe it to someone else?
- **10**: Unforgettable, one glance and it's burned in. Can be described in words easily.
- **5**: Pleasant but forgettable. Might recognize it if seen again but couldn't describe it.
- **1**: So complex or generic that no impression is formed.
- **Common issues**: Too many elements, no clear focal point, overly abstract without a hook, complexity that overwhelms.
- **Improvement path**: Simplify to one strong idea, create a surprising negative space moment, or make the silhouette so bold it demands attention.

### Relevance

- **What to check**: Does this mark fit the brand name, industry, and audience? Does it feel appropriate, not forced?
- **10**: The mark is the perfect visual expression of the brand's identity and values.
- **5**: The mark is competent but doesn't strongly connect to the brand story.
- **1**: The mark contradicts the brand or confuses the audience.
- **Common issues**: Symbolism that doesn't map to the brand, style mismatch (luxury mark for a budget brand), archetype misalignment.
- **Improvement path**: Revisit the strategy brief, ensure visual metaphors map directly to brand values, check archetype and style alignment.

### Scalability

- **What to check**: Is it clear at 16×16? Does it hold up at 512×512? Does it work across all sizes without losing identity?
- **10**: Perfectly legible and recognizable from favicon to billboard. No detail lost, no silhouette broken.
- **5**: Readable at medium sizes but struggles at extremes (too detailed at small, too simple at large).
- **1**: Unrecognizable at either small or large sizes.
- **Common issues**: Hairlines that disappear, negative space that closes up, details that become noise, silhouette that breaks apart.
- **Improvement path**: Apply the icon simplification engine. Test at actual 16×16. Verify paths are clean and nodes are minimal.

### Versatility

- **What to check**: Does it work on light backgrounds? Dark backgrounds? Color? Monochrome? Embossed? Screen-printed? Social media avatar? App icon?
- **10**: Flawless in any context, any background, any reproduction method.
- **5**: Works in standard contexts but struggles in monochrome or at very small sizes.
- **1**: Only works in one specific context (e.g., only on white, only at large sizes, only in full color).
- **Common issues**: Gradients that don't convert to monochrome, colors that disappear on certain backgrounds, details that rely on color contrast instead of shape contrast.
- **Improvement path**: Generate monochrome and reverse versions. Test on black, white, and mid-gray. Ensure silhouette works without any color.

### Icon Readability

- **What to check**: Does the simplified icon version hold up? Is the favicon recognizable? Does the app icon version retain the brand identity?
- **10**: The icon version is as strong as the master mark. Favicon is instantly identifiable.
- **5**: The icon is recognizable but loses some brand personality or requires context.
- **1**: The icon version is a generic blob or completely unrecognizable.
- **Common issues**: Over-simplification that loses identity, under-simplification that becomes muddy, silhouette changed so much it no longer reads as the brand.
- **Improvement path**: Revisit icon simplification. Preserve the most distinctive silhouette element. Sometimes the icon version needs to be redrawn, not just scaled down.

### Craftsmanship

- **What to check**: Are the paths clean? Is the construction deliberate? Are curves smooth? Is the geometry intentional? Does it feel designed, not generated?
- **10**: Flawless construction. Every curve is intentional. Nothing could be removed or added without diminishing the mark.
- **5**: Competent but has unnecessary nodes, slightly rough curves, or minor construction issues.
- **1**: Obvious construction errors, rough paths, unintentional gaps, overlapping shapes not merged, messy anchor points.
- **Common issues**: Too many nodes, rough curves, misaligned elements, inconsistent stroke weights, floating shapes, overlapping paths that should be merged, decimal precision issues.
- **Improvement path**: Manually review paths. Remove unnecessary nodes. Ensure curves are smooth. Align elements precisely. Merge overlapping shapes.

## Review Process

1. **Score each dimension** 1–10 independently. Be honest. A "5" is not a failure; it's average.
2. **Calculate overall score**: Average of the seven dimensions.
3. **Identify strengths**: Which dimensions scored highest? What makes them work?
4. **Identify weaknesses**: Which dimensions scored lowest? What specifically is wrong?
5. **Write recommendations**: For each weakness below 8, specify exactly what to change. Not "improve scalability" but "merge the two thin lines in the top left so they don't disappear at 16×16."
6. **Regeneration threshold**: If overall score < 8.0, recommend refinement or regeneration with specific, actionable notes. If overall score < 6.0, recommend starting over with a revised strategy brief.

## Critique Structure

Present the quality review in this format:

```
## Quality Review

| Dimension | Score | Notes |
|-----------|-------|-------|
| Distinctiveness | X/10 | ... |
| Memorability | X/10 | ... |
| Relevance | X/10 | ... |
| Scalability | X/10 | ... |
| Versatility | X/10 | ... |
| Icon Readability | X/10 | ... |
| Craftsmanship | X/10 | ... |
| **Overall** | **X.X/10** | |

### Strengths
- ...
- ...

### Weaknesses
- ...
- ...

### Recommendations
- ...
- ...

### Verdict
[Refine / Regenerate / Approve]
```

## Score Thresholds

| Overall Score | Action |
|---------------|--------|
| 9.0–10 | Approve. Minor polish only if time allows. |
| 8.0–8.9 | Approve with notes. Address specific weaknesses. |
| 7.0–7.9 | Refine. Address the lowest-scoring dimensions with targeted changes. |
| 6.0–6.9 | Major refinement needed. Revisit the concept or strategy. |
| 5.0–5.9 | Regenerate. The concept is fundamentally flawed. |
| < 5.0 | Start over. New strategy brief, new concepts. |
