---
name: chartjs
description: Chart.js charting skill. Used to generate visual charts such as line charts, bar charts, pie charts, radar charts, scatter plots, etc.
---

# Chart.js

Chart.js is a popular open-source charting library supporting 8 chart types, rendered via Canvas with responsive design.

## Trigger Scenarios

- User requests to create/generate/draw a chart
- User mentions Chart.js or data visualization
- User requests to visualize data with a chart
- User uploads data and requests visualization

## Installation

**npm:**
```bash
npm install chart.js
```

**CDN (Script Tag):**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

**Webpack/Rollup (recommended for tree-shaking):**
```javascript
import Chart from 'chart.js/auto';  // Full features, no manual registration needed
```

## Chart Types and Required Components

Each chart type has minimal dependencies; importing on demand optimizes bundle size:

| Chart Type | Controller | Element | Default Scale |
|---------|-----------|---------|-----------|
| Bar | BarController | BarElement | CategoryScale(x) + LinearScale(y) |
| Line | LineController | LineElement + PointElement | CategoryScale(x) + LinearScale(y) |
| Pie | PieController | ArcElement | — |
| Doughnut | DoughnutController | ArcElement | — |
| PolarArea | PolarAreaController | ArcElement | RadialLinearScale |
| Radar | RadarController | LineElement + PointElement | RadialLinearScale |
| Scatter | ScatterController | PointElement | LinearScale(x/y) |
| Bubble | BubbleController | PointElement | LinearScale(x/y) |

## Basic Usage

**HTML:**
```html
<div style="max-width: 600px">
  <canvas id="myChart"></canvas>
</div>
```

**JavaScript:**
```javascript
const ctx = document.getElementById('myChart');
new Chart(ctx, {
  type: 'bar',  // Chart type
  data: {
    labels: ['January', 'February', 'March'],
    datasets: [{
      label: 'Sales (10k)',
      data: [12, 19, 3],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { beginAtZero: true }
    }
  }
});
```

## Common Configurations

### Responsive (auto-adapts to container width)
```javascript
options: {
  responsive: true,
  maintainAspectRatio: false
}
```

### Fill Line Chart (Area)
```javascript
datasets: [{
  fill: true,        // or 'origin'/'start'/'end'
  tension: 0.4       // Curve smoothness 0-1
}]
```

### Multiple Datasets
```javascript
datasets: [
  { label: '2023', data: [1, 2, 3], borderColor: 'red' },
  { label: '2024', data: [3, 2, 1], borderColor: 'blue' }
]
```

### Quick Color Settings
```javascript
backgroundColor: [
  'rgba(255, 99, 132, 0.5)',
  'rgba(54, 162, 235, 0.5)',
]
```

## Interaction Events

Click to get data point values (requires helpers import):
```javascript
import Chart from 'chart.js/auto';
import { getRelativePosition } from 'chart.js/helpers';

options: {
  onClick: (e) => {
    const pos = getRelativePosition(e, chart);
    const x = chart.scales.x.getValueForPixel(pos.x);
    const y = chart.scales.y.getValueForPixel(pos.y);
    console.log(x, y);
  }
}
```

## Time Scale

Requires a date adapter (e.g., chartjs-adapter-moment):
```javascript
import moment from 'moment';
import 'chartjs-adapter-moment';
// Then configure scales with type: 'time'
```

## Output Methods

After generation, there are two output paths:

1. **Render directly in an HTML page** — Generate a complete HTML file containing canvas + Chart.js CDN, open with a browser
2. **Screenshot/PDF** — Take a screenshot using the browser tool, or generate an image file using puppeteer/canvas

**Tip:** Generating HTML is the simplest and most reliable output method; let Chart.js handle responsive layout itself.

## More References

For detailed API and examples, see `references/api.md`.