# direction — Recommendation Cards

Dual-column cards with auto-matched icons and color themes. Ideal for recommendations, options, or categorized items.

```javascript
{
  type: "direction",
  title: "Recommendations",
  data: {
    rows: [
      { title:"Option Alpha", reason:"Strong baseline", detail:"Fits current profile", requirement:"Score >= 80%", outcome:"High success rate" },
      { title:"Option Beta", reason:"Cost effective", detail:"Moderate risk", requirement:"Budget < 50K", outcome:"Good ROI" },
    ]
  }
}
```

**Field descriptions:**
- `rows[].title` card title (auto-matched to icon and color theme via keyword matching — see JS for mapping rules)
- `reason` primary reason / `detail` supplementary note (optional) / `requirement` entry threshold / `outcome` expected outcome

**Rendering:** Dual-column cards, icon and color auto-matched by title keywords. Extend the `colorMap` and `iconMap` in `direction.js` to add new domain keywords.
