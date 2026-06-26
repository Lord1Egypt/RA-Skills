# Accessibility and Output

Accessibility is part of quantitative integrity: a display that only some viewers can read is losing evidence.

## Labels and text

Use readable type, human labels, and units. Avoid vertical text, tiny legends, all-caps labels, and unexplained abbreviations. Direct labels often beat legends because they reduce lookup effort.

For dense scientific or dashboard displays, use captions and annotations to explain what the viewer should compare, not to decorate the chart.

## Color

Do not make color the only carrier of meaning. Add direct labels, markers, line styles, faceting, or text cues. Use ordered lightness for ordered data and distinct hues for unordered groups. Avoid red/green-only distinctions for critical states.

Use `scripts/contrast_check.py` for text or important annotation colors. Contrast alone does not guarantee good design, but poor contrast is a concrete failure.

## Alt text and captions

For user-facing deliverables, include concise alt text when charts are exported to documents, slides, or web pages. Good alt text names the chart type, variables, key comparison, and important caveat. It should not repeat every data point if the data table is available.

## Code-generation defaults

When generating chart code:

- Inspect the data before plotting.
- Preserve units and use explicit labels.
- Prefer direct labels or clear legends.
- Avoid 3D, perspective, bevels, decorative backgrounds, and pictorial scaling.
- Use zero baselines for bar lengths; use dots or intervals when zero is not meaningful.
- Show uncertainty for estimates or forecasts.
- Add source/caption notes when the chart stands alone.
- Save outputs with descriptive names.

If a quick, dependency-free artifact is useful, use `scripts/render_chart_svg.py` to create simple SVG bars, dots, lines, or scatterplots.
