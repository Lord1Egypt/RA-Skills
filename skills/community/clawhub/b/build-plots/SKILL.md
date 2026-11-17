---
name: build-plots
description: Create clear, publication-ready Python data visualizations with pandas, Matplotlib, Seaborn, and optional Bokeh interaction. Use for choosing a chart from a dataset's structure, writing or revising plot-building code, applying Storytelling with Data principles, replacing misleading or cluttered charts, and exporting reproducible PNG previews plus vector PDF figures for scientific papers.
metadata: {"openclaw":{"emoji":"📊"}}
---

# Build Plots

Turn a dataset and an intended message into a focused chart. Use pandas for data preparation, Matplotlib/Seaborn for the authoritative static figure, and Bokeh only when an interactive companion adds real value.

## Required workflow

1. Read `{baseDir}/references/chart-recipes.md` before selecting a chart.
2. Read `{baseDir}/references/palette.md` before assigning colors.
3. Inspect the data grain, column types, missing values, units, denominators, and ordering with pandas.
4. State the single comparison or conclusion the chart must make easy.
5. Select the simplest chart that exposes that comparison. Do not start from a preferred library or chart type.
6. Build the static version with the Matplotlib object API; use Seaborn for heatmaps, distributions, and statistical layers.
7. Apply one visual hierarchy: gray context, one accent for the message, direct labels where practical.
8. Save both a PNG preview and a vector PDF from the same figure. Also save SVG when a text-based vector preview is useful.
9. Add a Bokeh HTML companion only for tooltips, filtering, zooming, or exploration. Keep the Matplotlib PDF as the publication artifact.
10. Verify values, labels, units, denominators, sort order, zero baselines for bars, and readable rendering at final size.

## Output contract

For each plot named `figure_name`, produce:

- `figure_name.png`: 180-300 dpi review image.
- `figure_name.pdf`: vector publication figure with embedded fonts.
- `figure_name.svg`: optional text-based vector copy.
- `figure_name.html`: optional Bokeh companion using the same prepared dataframe.
- A `.py` builder that can regenerate every output from source CSV data.

Use a white background, tight bounding box, explicit figure size, and deterministic ordering. Never rasterize the complete Matplotlib figure before writing PDF.

## Library roles

- Use **pandas** for loading, validation, grouping, pivoting, sorting, normalization, and reconciliation.
- Use **Matplotlib** for bars, lines, slopegraphs, waterfalls, small multiples, annotation, and all PDF exports.
- Use **Seaborn** for heatmaps, distributions, regression layers, and coherent statistical defaults; finish with Matplotlib axes.
- Use **Bokeh** for optional interactive HTML. Do not make Bokeh interaction necessary to understand the result.

## Hard chart rules

- Start every bar axis at zero.
- Prefer horizontal bars for long category labels and sort them when no semantic order exists.
- Use lines only for ordered, sufficiently dense time intervals; use a slopegraph for exactly two periods.
- Use a heatmap for a category-by-category matrix when pattern recognition matters more than exact lookup.
- Use a waterfall only when components reconcile exactly to an ending total.
- Use 100% stacked bars only when every bar shares a meaningful denominator.
- Replace dual axes with aligned small multiples unless the scales have a defensible shared transformation.
- Avoid pie/donut charts, 3D effects, rainbow palettes, decorative gradients, truncated bar axes, and redundant legends.
- Preserve exact values in direct labels or a companion table when the chart alone is insufficient.

## Reusable resources

- Run `{baseDir}/scripts/build_book_examples.py` to regenerate the bundled examples.
- Import `{baseDir}/scripts/storytelling_style.py` for the palette, styling, and PNG/PDF/SVG export helper.
- Read `{baseDir}/references/source-examples.md` when adapting the book-derived demonstrations.
- Reuse CSV files under `{baseDir}/assets/data/` as test fixtures and teaching examples.

Install the example dependencies with:

```bash
python3 -m pip install -r {baseDir}/scripts/requirements.txt
```

Regenerate all examples with:

```bash
python3 {baseDir}/scripts/build_book_examples.py \
  --output-dir {baseDir}/assets/examples
```

## Verification

Run the builder twice into a temporary directory and confirm both runs succeed. Open every PNG at final display size. Use `pdfinfo` or an equivalent PDF inspector to confirm each PDF exists and has one page; rasterize one representative PDF and compare it visually with the PNG. Confirm the Bokeh HTML opens without requiring local data files.

Treat every title as a conclusion when the evidence supports one; otherwise use a neutral descriptive title. Keep source and denominator notes visible but quiet.
