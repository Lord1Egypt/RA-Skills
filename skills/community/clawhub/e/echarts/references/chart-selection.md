# Chart Selection

Use the smallest chart that answers the question without forcing the reader to decode extra structure.

## Fast Mapping

| Goal                                             | Preferred Chart | Required Shape                                          | Avoid                                               |
| ------------------------------------------------ | --------------- | ------------------------------------------------------- | --------------------------------------------------- |
| Compare categories                               | Bar             | One label field, one or more numeric fields             | Pie when precise comparison matters                 |
| Emphasize ranked categories with shaped bars     | Pictorial Bar   | One label field, one or more numeric fields             | Standard bar when exact comparison is primary       |
| Show ranked categories in a radial layout        | Polar Bar       | One label field, one or more numeric fields             | Pie when precise ranking matters                    |
| Show change over time                            | Line or Area    | Ordered x field plus numeric series                     | Bar when the story is continuous trend              |
| Show share of total                              | Pie, Donut, or Rose Pie | One label field, one numeric field               | More than 6 to 8 slices without grouping            |
| Show sequential positive and negative deltas     | Waterfall       | Ordered label field and one signed numeric field        | Stacked bar when running totals are the point       |
| Show relationship between two metrics            | Scatter         | Two numeric fields, optional group field                | Line if points do not imply sequence                |
| Compare several metrics across the same entities | Radar           | One entity field plus 3 to 6 comparable numeric metrics | Radar when metrics do not share a common scale      |
| Show intensity across two categorical axes       | Heatmap         | X field, Y field, and one numeric value field           | Dense tables with no visual prioritization          |
| Show daily intensity across calendar dates       | Calendar        | Date field and one numeric value field                  | Line charts when only sequential trend matters      |
| Show category composition over time as streams   | ThemeRiver      | Date field, series label field, and one numeric value   | Stacked area when exact baseline comparison matters |
| Show stage drop-off                              | Funnel          | Ordered stage label plus one numeric field              | Bar charts when the point is conversion loss        |
| Show progress toward a target or cap             | Gauge           | One or more numeric values with a known max             | Pie when there is no part-to-whole story            |
| Show nested share or grouped hierarchy           | Treemap         | Label field, numeric field, optional parent field       | Flat bar charts when grouping is the main story     |
| Show radial hierarchy and contribution           | Sunburst        | Label field, numeric field, optional parent field       | Treemap when long labels need more room             |
| Show OHLC movement over time                     | Candlestick     | Ordered x field plus open, close, low, and high fields  | Line charts when intraperiod range matters          |
| Show distribution summary by group               | Boxplot         | Category plus low, q1, median, q3, and high values      | Bars when spread and skew matter                    |
| Show flow between sources and outcomes           | Sankey          | Source, target, and one numeric value field             | Funnel when paths branch or rejoin                  |
| Show relationship network between entities       | Graph           | Source, target, and optional weight or node metadata    | Sankey when directional flow is the main story      |
| Show explicit node hierarchy                     | Tree            | Label field, numeric field, optional parent field       | Treemap when node paths matter less                 |
| Compare many metrics across the same entities    | Parallel        | One entity field plus 4 or more numeric metrics         | Radar when too many axes become unreadable          |

## Practical Rules

- Use `bar` for rankings and category comparisons.
- Use `line` for time series and ordered sequences.
- Use `pictorialBar` when visual emphasis or block styling matters more than raw precision.
- Use `polarBar` when the ranking should feel radial but exact ordering still matters.
- Use `area` only when emphasizing cumulative shape or relative magnitude over time.
- Use `pie`, `donut`, or `rosePie` only for part-to-whole views with a small number of slices.
- Use `waterfall` when the story is stepwise net change, especially when values include both gains and losses.
- Use `scatter` for correlation, clustering, or outlier hunting.
- Use `heatmap` when both axes are categorical and intensity matters more than individual labels.
- Use `calendar` when daily patterns, streaks, and missing days matter.
- Use `themeRiver` for changing category composition over time when the story is about flow rather than exact stacked baselines.
- Use `funnel` for strictly ordered stage loss.
- Use `gauge` for a small number of target-tracking KPIs.
- Use `treemap`, `sunburst`, or `tree` for hierarchy; prefer treemap for label density, sunburst for radial path awareness, and tree for explicit parent-child reading.
- Use `graph` for collaboration maps, dependency networks, or entity relations when the layout should be force-directed.
- Use `parallel` when you need to compare many numeric dimensions and radar axes would become cluttered.
- Use `candlestick` for trading or OHLC snapshots, not simple trend lines.
- Use `boxplot` when spread, median, and quartiles matter more than raw points.
- Use `sankey` for branch-and-merge flows across stages or systems.
- Use `radar` only when every axis means the same thing for every entity.

## Cleanup Heuristics

- If a pie chart has more than 6 slices, aggregate the tail into `Other`.
- If category labels exceed about 12 rows, turn on `dataZoom` or use a horizontal bar chart.
- If two numeric series have different units, do not fake comparability. Split the chart or clearly annotate units.
- If the audience needs exact values, add labels or pair the chart with a small table.
- If the story is about a single moment, avoid building a dashboard just because multiple charts are possible.
