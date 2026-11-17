# Chart recipes by data structure

Use this reference after identifying the dataframe grain and the comparison the reader needs.

## Selection matrix

| Data structure | Primary task | Default chart | Construction instructions |
|---|---|---|---|
| One or two headline values | Communicate magnitude or change | Large text | Write the value and unit; add one short comparison sentence; omit axes. |
| Rows with mixed fields or units | Exact lookup | Minimal table | Left-align labels, right-align numbers, format units in cells, remove vertical rules, emphasize one row or column only. |
| Category × one numeric measure | Rank or compare | Horizontal bar | Aggregate to one row per category, sort descending unless order is semantic, start at zero, label values, remove legend. |
| Category × exactly two periods | Show change | Slopegraph | Put periods on x, connect matching categories, label both endpoints, highlight only the focal series. |
| Time × one measure, 8+ intervals | Show trend | Line | Sort time, preserve equal intervals, direct-label the endpoint, use a benchmark line only when meaningful. |
| Two numeric measures at the same grain | Show relationship | Scatter | Put the presumed driver on x, outcome on y, show units, use transparency for overlap, annotate only exceptions. |
| Category × category × value | Find patterns | Heatmap | Pivot to a matrix, use a sequential scale for magnitude, center a diverging scale only on a meaningful reference, include a labeled colorbar. |
| Total split into components | Show rough composition | Stacked bar | Keep component order consistent, limit components, direct-label large segments, group tiny categories as Other when justified. |
| Same denominator split into shares | Compare composition | 100% stacked bar | Validate every row totals 100%, preserve ordered response categories, label the denominator and neutral midpoint. |
| Start + signed changes = end | Reconcile a bridge | Waterfall | Validate arithmetic first, show totals distinctly, encode increases/decreases consistently, add connectors and signed labels. |
| Two measures across the same time | Compare patterns without shared scale | Aligned small multiples | Share the x-axis, give each panel its own labeled y-axis, align event markers, never use a decorative secondary axis. |
| Few nested quantities with large ratios | Show scale | Square area | Use area proportional to value, so side length is `sqrt(value/max_value)`; label exact values and keep only 2-4 shapes. |

## Concrete build instructions

### Bars

1. Check that each category has exactly one plotted value after aggregation.
2. Sort by value unless chronology, hierarchy, or survey order is meaningful.
3. Use `ax.barh` for long labels; invert the y-axis so the largest appears first.
4. Set the numeric axis lower bound to zero.
5. Add direct labels at bar ends and remove a redundant legend.
6. Color all context bars gray and use one accent only for the finding named in the title.

### Lines and slopegraphs

1. Parse dates and sort them before plotting.
2. Reject a line when time intervals are irregular but displayed as equal.
3. For many series, use small multiples or gray context lines with one focal series.
4. For two periods, label endpoints and remove the y-axis if exact endpoint labels carry the values.
5. Avoid markers at every point; use markers only for sparse observations or highlighted events.

### Scatterplots

1. Confirm x and y come from the same observational grain.
2. Decide whether zero is meaningful on either axis; do not force it when it destroys the relationship view.
3. Use alpha and small markers for dense data.
4. Add a benchmark quadrant only when its threshold is documented.
5. Label outliers selectively; never label every point in a dense cloud.
6. Describe association, not causation, unless the study design supports causality.

### Heatmaps

1. Pivot with an explicit row and column order.
2. Show missing values distinctly from zeros.
3. Use a perceptually ordered sequential palette for magnitude.
4. Use a diverging palette only for signed deviation from a meaningful midpoint such as zero or target.
5. Annotate cells only when the matrix remains legible; otherwise provide a table.

### Stacked and 100% stacked bars

1. Reconcile components to the total before plotting.
2. Put the most important component on the common baseline.
3. Keep segment order fixed across bars.
4. Do not claim precise comparisons for floating middle segments.
5. For 100% bars, normalize with pandas and assert row sums equal 1 within a small tolerance.

### Waterfalls

1. Mark rows as `total` or `delta`.
2. Calculate cumulative positions in pandas; do not hand-place bars.
3. Assert `start + sum(deltas) == end` within the appropriate precision.
4. Draw positive changes with the primary accent, negative changes with the exception color, and totals with dark ink.
5. Label signed changes and final totals directly.

### Small multiples

1. Use one panel per measure or segment.
2. Keep panel widths and time bounds identical.
3. Repeat reference lines or event annotations in every affected panel.
4. Label units independently and align x ticks.
5. Use the same highlight semantics across panels.

## Decluttering sequence

Apply this order after the plot is correct:

1. Remove chart borders and unnecessary spines.
2. Remove minor ticks and decorative gridlines.
3. Keep only light horizontal gridlines that improve numeric reading.
4. Replace legends with direct labels when there are few series.
5. Shorten repeated units using axis or subtitle text.
6. Make the title answer-first, then add a compact subtitle for scope and denominator.
7. Add a quiet source note.

## QA checklist

- Recompute plotted values from the source dataframe.
- Confirm the plotted grain and aggregation function.
- Confirm units and denominators are visible.
- Confirm bar axes start at zero.
- Confirm colors have the same meaning everywhere.
- Confirm color is not the only carrier of meaning.
- Confirm labels remain legible at journal column width.
- Confirm PDF text and geometry remain vector, not a full-page raster image.
