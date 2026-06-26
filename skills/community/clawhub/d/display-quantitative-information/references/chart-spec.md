# Chart Specification

Use a structured spec when auditing, handing off, or asking another tool to render a chart. `assets/chart-spec-template.json` is compatible with `scripts/audit_visual_display.py`.

## Minimum fields

- `title`: working title, not marketing copy.
- `purpose`: viewer task or decision.
- `chart_type`: bar, dot, line, scatter, map, table, small_multiples, etc.
- `data_points`: approximate count of visible observations.
- `variables`: field names and derived variables.
- `data_grain`: one row means what.
- `encodings`: x, y, color, size, shape, facet, label.
- `axes`: labels, units, zero baseline, scale type, axis breaks, dual axes, panel scales.
- `labels`: direct labels, legend, source, definitions, annotations.
- `context`: denominator, uncertainty, sample size, comparison baseline, time range.
- `design`: grid, decorations, 3D, area/volume encodings, color count, color-only identification.
- `integrity_measurements`: data and visual percent effects where measurable.
- `medium`: destination, color reliance, minimum text size.

## Spec-first workflow

1. Draft the spec before rendering.
2. Run `python3 scripts/audit_visual_display.py --spec spec.json --format markdown`.
3. Fix severe and warning findings.
4. Render the chart or provide implementation guidance.
5. Add final notes for source, units, uncertainty, and accessibility.

## Do not overfit to the template

The template is a forcing function, not a bureaucracy. Skip irrelevant fields in the user-facing answer, but keep enough structure that another agent or developer can implement the display without guessing.
