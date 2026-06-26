# text — Text Block

Colored callout block for summaries, warnings, conclusions, or key takeaways.

```javascript
{
  type: "text",
  data: { title:"Summary", content:"...text content...", level:"success" }
}
```

**Field descriptions:**
- `title` heading / `content` body text (supports HTML)
- `level` color theme: `success` (green) / `warning` (yellow) / `danger` (red)
