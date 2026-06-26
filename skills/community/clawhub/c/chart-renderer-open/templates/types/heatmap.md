# heatmap — Matrix Heatmap Table

Multi-row × multi-column numeric matrix with color-coded cells, change indicators, and trend badges.

```javascript
{
  type: "heatmap",
  title: "Sales Performance Overview (Q1-Q4)",
  data: {
    columns: ["Q1","Q2","Q3","Q4"],
    rows: [
      { name:"Product A", max:200, values:[120,155,130,175], trend:"steady growth" },
      { name:"Product B", max:200, values:[80,60,95,110], trend:"volatile" }
    ],
    totals: [200,215,225,285],     // optional summary row
    totalRate: "63.1%",            // summary row rate
    totalTrend: "up",              // "up"|"down"|"flat"
    totalTrendLabel: "strong recovery"
  }
}
```

**Field descriptions:**
- `rows[].name` row label / `max` reference max for rate calculation / `values` numeric values per column / `trend` trend description text
- `columns` column headers
- `totals` summary values array (optional)
- `totalRate` / `totalTrend` / `totalTrendLabel` summary row config (optional)

**Rendering:** Each cell is auto-colored by value-to-max ratio (dark red <30% → dark green >=70%, 5 levels). Last data column shows change with ▲▼ arrows. Trend badges are inline.

**Data requirements:** At least 2 rows + 2 columns.
