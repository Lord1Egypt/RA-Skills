# Charting

Charting is a separate step from data export.

## Weekly created vs closed trend

Expected input fields:

- `createdDate`
- `closedDate`

The chart process should:

1. Read exported CSV or JSON data.
2. Group `createdDate` values by week start.
3. Group `closedDate` values by week start.
4. Merge both weekly series on a common week axis.
5. Plot a trend graph with two lines:
   - Created tickets per week
   - Closed tickets per week

Use charting only when the user explicitly asks for visualization.
