# Redesign Workflow

Use this when the user asks to improve an existing chart, dashboard, or figure.

## Sequence

1. State the viewer's task in one sentence.
2. Name the current obstacle: misleading scale, wrong display form, missing denominator, hidden uncertainty, weak comparison, excess decoration, or too little data.
3. Preserve or restore context: units, source, denominator, sample size, transformations, uncertainty, filters, and definitions.
4. Choose the display form using `display-selection.md` if needed.
5. Improve comparison through ordering, alignment, common scales, direct labels, reference lines, paired differences, or facets.
6. Remove marks that compete with evidence. Keep non-data marks that make interpretation easier.
7. Add annotations where they explain events, thresholds, outliers, definitions, or methods.
8. Stop when the next edit would polish rather than clarify.

## Editing moves

Use only the moves that fit the case.

- Sort categories by value, change, domain order, or viewer workflow.
- Align comparable quantities on a common baseline.
- Use common scales across comparable panels.
- Replace remote legends with direct labels when labels fit near the data.
- Replace overplotted series with small multiples, context bands, or a highlighted focus series.
- Replace summary-only charts with raw observations plus summaries when distribution matters.
- Add reference ranges, targets, baselines, and event annotations tied to decisions.
- Lighten heavy grids, frames, backgrounds, bevels, shadows, and decorative fills.
- Make captions and annotations do explanatory work.

## Dashboard-specific moves

Group panels by decision or workflow, not by data source. Replace isolated headline numbers with trends, targets, distributions, or prior periods. Make time windows and denominators consistent unless differences are deliberate and labeled. Put alerts next to the evidence that justifies them.

## Scientific-figure moves

Show sample size, units, conditions, and uncertainty. Avoid summary bars when raw observations or intervals are central. Keep panel labels, captions, and methods-relevant transformations close to the data. Use consistent scales for comparable panels.

## Handoff structure

For a redesign handoff, include:

- purpose: the question answered;
- current obstacle: the specific failure;
- proposed display: chart type and layout;
- encodings: fields mapped to position, length, color, size, shape, facets, labels;
- integrity safeguards: scale, baseline, units, source, denominator, uncertainty;
- annotation plan: events, thresholds, outliers, definitions;
- expected improvement: what comparison becomes easier or more honest.

Adapt the shape to the user's task; do not force this as a rigid template in every response.
