# Language and Variation

Agents are prone to producing the same critique shape repeatedly. That makes reviews feel generic and can obscure the actual diagnosis.

## Vary by evidence

Each critique should sound like it came from the chart being reviewed. Mention the actual variables, units, denominator, visual encoding, scale choice, audience, and medium. Domain vocabulary should replace generic phrasing, not decorate it.

A public-health chart may need incidence, population denominator, confidence interval, age adjustment, and reporting lag. A materials or imaging figure may need scale bars, calibration, voxels, segmentation, sample preparation, registration, and measurement uncertainty.

## Avoid fixed replacement habits

Do not recommend the same substitute for every flaw. A pie chart does not always become a bar chart; a multi-line chart does not always become small multiples; a legend does not always become direct labels. Diagnose the task first, then choose.

Good recommendations have a mechanism: "use an interval dot plot because the zero baseline is not meaningful and the uncertainty intervals need comparison" is stronger than "replace bars with dots."

## Make examples non-pasteable

Examples in this skill show patterns, not text to reuse. When adapting an example, change the domain nouns, numerical context, chart type, evidence, and recommendation order.

## Response-shape variation

Pick a shape that fits the task:

- A fast verdict can be two short paragraphs.
- A detailed critique can use sections for integrity, comparison, and redesign.
- A dashboard review can group issues by workflow or panel family.
- A code handoff can start with a spec and end with checks.
- A teaching answer can explain the design principle first, then the example.

Avoid using the same numbered structure in every output unless the user asked for standardization.

## Stock-phrase check

For long or repeated deliverables, run:

```bash
python3 scripts/fingerprint_text.py --input draft.md --format markdown
```

Treat warnings as prompts to revise, not automatic failures. Technical terms can repeat when they are genuinely needed.
