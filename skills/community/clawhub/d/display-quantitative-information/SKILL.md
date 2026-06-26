---
name: display-quantitative-information
description: "Use this skill when the user needs to design, critique, redesign, audit, generate, code, or explain quantitative graphics: charts, dashboards, tables, maps, scientific/statistical figures, visual evidence, or chart specifications. It helps choose display forms, avoid misleading encodings, compute lie factors, inspect CSV structure, generate simple SVG charts, check color contrast, and produce Tufte-informed but non-formulaic recommendations. Do not use for decorative illustration or general data cleaning unless a quantitative display is involved."
license: Proprietary. See LICENSE.txt for terms.
compatibility: Portable Agent Skill. Bundled scripts require Python 3.9+ and use only the standard library.
metadata:
  version: "2.0.0"
  category: data-visualization
  source-note: "Distilled from user-provided skill-authoring resources and OCR-derived study material from Edward R. Tufte's The Visual Display of Quantitative Information. Original source text and images are not bundled."
---

# Display Quantitative Information

Use this skill to help an agent create, critique, redesign, audit, or explain quantitative displays that let people reason from evidence. The default standard is truthfulness first, comparison power second, and visual economy third. Minimalism is not the goal; clear quantitative reasoning is.

## Activation boundaries

Use this skill for chart choice, data visualization code, dashboard review, statistical/scientific figures, misleading graphics, graph redesign, tables used as evidence, uncertainty displays, small multiples, map-based quantitative displays, or user language such as data-ink, chartjunk, graphical integrity, lie factor, Tufte, visual evidence, publication-ready figure, or dashboard critique.

Do not use it for decorative illustration, infographics with no measured quantities, brand-only design, slide aesthetics without data, or general data wrangling unless a display or visual explanation is part of the task.

## Working loop

1. Name the viewer's task: lookup, comparison, trend, relationship, distribution, part-to-whole, geography, uncertainty, monitoring, explanation, or persuasion.
2. Inspect the data structure: grain, units, denominators, time order, grouping, spatial structure, missingness, transformations, sample size, and uncertainty.
3. Choose the display from the task and data, not from a favorite chart type. Use `references/display-selection.md` when the choice is not obvious.
4. Audit integrity before aesthetics: baselines, scales, proportionality, encodings, transformations, omitted context, denominators, uncertainty, source, and accessibility. Use `references/integrity-audit.md` or `scripts/audit_visual_display.py` for structured specs.
5. Redesign by improving the intended comparison. Remove distracting marks, but keep labels, notes, reference lines, captions, and structure when they help interpretation.
6. Deliver the artifact requested: chart, code, SVG, design spec, critique, dashboard review, or short recommendation. Put the highest-impact fix first.

## Mode-specific guidance

For a quick critique, answer in plain language: what works, what may mislead, and the most valuable fix. Do not bury an integrity problem under cosmetic advice.

For a redesign, state the proposed display form, encodings, scale choices, labels, annotations, and integrity safeguards. Explain choices in terms of the viewer's comparison or decision.

For chart creation, produce the chart or code when tools permit. Add a short final check covering units, scale, baseline, source/context, uncertainty, and accessibility.

For dashboards, review the workflow first: whether panels answer a coherent decision, share compatible time windows and denominators, and show trends or distributions rather than isolated decorative KPIs.

For scientific figures, prioritize sample size, units, conditions, uncertainty, transformations, calibration, and comparison across panels. Avoid summary-only bars when raw observations or intervals are central.

## Non-negotiables

Never trade a misleading chart for a cleaner misleading chart. Preserve or restore units, source, definitions, sample size, denominators, relevant uncertainty, and methodological context whenever they affect interpretation.

Do not mechanically apply slogans. Data-ink discipline is an editing principle, not a license to remove explanation. A legend, gridline, note, or reference band is useful when it reduces ambiguity or supports comparison.

Avoid formulaic critique language. Across multiple outputs, vary the opener, recommendation order, examples, and vocabulary according to the dataset and audience. Use `references/language-and-variation.md` or `scripts/fingerprint_text.py` for long/batch deliverables.

## Reference map

Read only the files needed for the task.

- `references/principles.md` — core Tufte-informed judgment standards.
- `references/display-selection.md` — display choices by task and data structure.
- `references/integrity-audit.md` — distortion, lie factors, baselines, context, and uncertainty.
- `references/redesign-workflow.md` — practical redesign and handoff sequence.
- `references/chart-spec.md` — structured chart-spec fields and examples.
- `references/accessibility-and-output.md` — contrast, color, labels, alt text, and code/output defaults.
- `references/language-and-variation.md` — anti-fingerprint guidance for critiques.
- `references/rubric.md` — scoring rubric for reviews.
- `references/examples.md` — worked patterns; adapt, do not copy.

## Scripts and assets

Scripts are optional but useful when the user supplies data or a structured chart spec. They are non-interactive and print structured output.

- `scripts/suggest_display.py --csv data.csv --goal auto --format markdown` inspects a CSV and recommends display families.
- `scripts/audit_visual_display.py --spec chart.json --format markdown` audits a JSON chart spec.
- `scripts/lie_factor.py --data-before 18 --data-after 27.5 --visual-before 0.6 --visual-after 5.3` computes visual distortion.
- `scripts/contrast_check.py --foreground '#333333' --background '#ffffff' --format markdown` checks text/color contrast.
- `scripts/render_chart_svg.py --csv data.csv --x month --y defect_rate --chart line --group line --output chart.svg` creates a simple, honest SVG chart for handoff or review.
- `scripts/fingerprint_text.py --input draft.md --format markdown` flags repeated stock visualization language.

Assets:

- `assets/chart-spec-template.json` — starting point for structured audits.
- `assets/critique-note-template.md` — flexible critique handoff note.
- `assets/chart-handoff-template.md` — compact implementation spec.

## Completion check

Before finalizing, verify that the response names the analytical task, preserves units/context, justifies the display form, checks for misleading scales or encodings, and gives at least one concrete improvement to comparison, integrity, or accessibility.
