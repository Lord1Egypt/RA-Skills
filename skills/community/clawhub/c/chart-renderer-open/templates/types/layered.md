# layered — Tiered Category Cards

Categorize items into three tiers (strong / moderate / weak) with color-coded cards.

**Only outputs the three layer-card tables. Does not append text blocks. Extract only structured data into the tier cards.**

```javascript
{
  type: "layered",
  title: "Category Tier Overview",
  data: {
    layers: {
      strong: [
        { item:"Server A", prev:92, current:95, change:3, rate:95, note:"Most stable" },
      ],
      moderate: [
        { item:"Server B", prev:65, current:78, change:13, rate:78, note:"Improving steadily" },
      ],
      weak: [
        { item:"Server C", prev:40, current:33, change:-7, rate:33, note:"Needs attention" },
      ]
    }
  }
}
```

**Field descriptions:**
- `layers` contains `strong` / `moderate` / `weak` arrays
- Each entry: `item` name / `prev` previous value / `current` current value / `change` delta / `rate` percentage / `note` brief analysis (max ~30 chars)
- Tiers can be partially empty (e.g., no weak items → `weak` is an empty array)

**Rendering:** Three color-coded cards (green / blue / red) with table containing item / previous / current / change / rate / note.
