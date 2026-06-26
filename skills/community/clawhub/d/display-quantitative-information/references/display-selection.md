# Display Selection

Choose the display from the viewer's task and the data structure. The same dataset may need a table for lookup, a line chart for change, a distribution plot for spread, and small multiples for repeated comparison.

## Exact lookup

Use a table or compact text-table when exact values matter more than visual pattern. Sort by the meaningful quantity unless natural order matters. Round to useful precision, align numbers, and use light grouping rules. Add sparklines or inline bars only when pattern comparison matters.

## Magnitude comparison across categories

Use bars when length from zero is the natural encoding and absolute magnitude matters. Start the quantitative axis at zero. Use horizontal bars for long labels and sort by value unless the domain order is meaningful.

Use dot plots when there are many categories, deviations from a reference are central, intervals sit beside estimates, or zero is not a meaningful anchor.

## Change over ordered time

Use lines for trends, cycles, seasonality, rates, and event effects. Keep time on the horizontal axis unless the domain strongly suggests otherwise. Annotate meaningful events directly. Use small multiples or indexed lines when many series overlap or start from different levels.

## Relationship between quantitative variables

Use scatterplots for association, clusters, outliers, heteroscedasticity, or model fit. Add transparency, density contours, hex bins, or sampling when overplotting hides structure. Label transformations and smoothing methods.

Use connected scatterplots only when temporal or path order is central and the audience can follow the path.

## Distribution and uncertainty

Use histograms, dot plots, strip plots, box plots, violins, density plots, ridgelines, interval plots, or fan charts depending on audience and task. Show raw observations when sample size is small enough and distribution shape matters. Label what intervals mean.

Avoid bar charts of means when the decision depends on spread, overlap, skew, outliers, or sample size.

## Part-to-whole

Pie charts are narrow-use tools, not forbidden tools. They work best for a simple part-to-whole impression with very few slices and clear labels. When ranking, exact comparison, many categories, or small differences matter, use a sorted bar, table, grouped categories, or a 100 percent bar with care.

## Geography

Use maps when location is explanatory or decision-relevant. Prefer rates, ratios, or normalized values when raw counts mostly reflect population, area, tests, stores, or exposure. If the task is ranking or exact comparison, include a companion table or dot plot.

## Repeated comparisons

Use small multiples when the same comparison repeats across groups, time periods, places, scenarios, samples, models, or conditions. Keep scales common when cross-panel magnitude matters. Change scales only when within-panel shape is the point, and label that choice.

## Multivariate structure

Add variables only when they answer the question. Options include facets, color, shape, size, heatmaps, paired panels, and parallel coordinates. Position and length are usually easier to compare than area, angle, hue, or volume.

## Common substitutions, with conditions

- Replace a dual-axis chart with indexed lines, small multiples, or a scatterplot when the dual axes imply a relationship that depends on arbitrary scaling.
- Replace a stacked bar with small multiples, grouped bars, or a heatmap when viewers need to compare middle segments.
- Replace a gauge with a bullet chart, trend, or table when the gauge wastes space or lacks history.
- Replace pictograms with bars, dots, or tables when pictorial scale distorts magnitude.
- Keep the original form when it fits the viewer's task better than a fashionable substitute.
