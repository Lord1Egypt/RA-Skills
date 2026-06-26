# table — Styled Table

Clean white-background table for any structured data.

```javascript
{
  type: "table",
  title: "Risk Summary",
  data: {
    headers: ["Dimension","Level","Status","Action"],
    rows: [
      ["Stability","🔴","High volatility","Stabilize first"],
      ["Coverage","🟡","Partial","Fill gaps"]
    ]
  }
}
```

**Field descriptions:**
- `headers` column header array / `rows` row data, each row is an array of cell values
- Cells starting with `↑` are auto-colored green; cells starting with `↓` are auto-colored red
