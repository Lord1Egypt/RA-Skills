# Dashboard Design Rules

## Color Palette

### Dark Mode (Default)
| Element | Color |
|---------|-------|
| Background | `#0f172a` |
| Card | `#1e293b` |
| Text | `#e2e8f0` |
| Accent | `#3b82f6` |

### Light Mode
| Element | Color |
|---------|-------|
| Background | `#f8fafc` |
| Card | `#ffffff` |
| Text | `#1e293b` |
| Accent | `#2563eb` |

## Typography

| Element | Size | Weight |
|---------|------|--------|
| KPI value | 48-72px | Bold |
| KPI label | 14px | Normal |
| Section header | 20px | Semibold |
| Body text | 14px | Normal |

## Spacing

Use multiples of 4px:
- Card padding: 16px
- Section gap: 24px
- Dashboard margin: 32px

## Cards

```css
.card {
  border-radius: 8px;
  padding: 16px;
  background: var(--card-bg);
}
```

## Charts

- Use ECharts or Chart.js consistently
- Always include axis labels
- Use color palette accent for primary data
- Gray for secondary/comparison data
