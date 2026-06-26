---
name: apache-echarts
description: Apache ECharts charting skill.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "homepage": "https://echarts.apache.org/"
      }
  }
---

# ECharts Skill

Generate high-quality interactive visual HTML chart pages based on user-provided two-dimensional data or time series data. Automatically select the most appropriate chart type, supporting 20+ chart types including bar charts, line charts, pie charts, scatter plots, maps, etc. Supports one-click PNG image export.

## Trigger Scenarios

- Draw a chart
- Generate a chart
- Use ECharts
- Visualize data
- Plot the data

## Workflow

1. **Analyze Data**: Identify data type (categorical/time series/numeric/geographic)
2. **Select Chart**: Recommend the most suitable chart type based on data structure
3. **Generate HTML**: Generate a complete interactive HTML file based on ECharts 5.x CDN

## CDN Import

Always use ECharts 5.x CDN (no download required):
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
```

## Standard HTML Template

The generated HTML contains a chart rendering area.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chart Title</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 24px; background: #f0f2f5; }
    .container { max-width: 1200px; margin: 0 auto; }
    .chart-title { text-align: center; font-size: 22px; font-weight: 600; color: #1f2329; margin-bottom: 16px; }
    #chart { width: 100%; height: 480px; background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .toast {
      position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
      padding: 10px 20px; background: rgba(30,35,41,0.9); color: #fff;
      border-radius: 8px; font-size: 14px; pointer-events: none;
      opacity: 0; transition: opacity 0.3s; z-index: 9999;
    }
    .toast.show { opacity: 1; }
  </style>
</head>
<body>
  <div class="container">
    <div class="chart-title">Chart Title</div>
    <div id="chart"></div>
  </div>
  <div class="toast" id="toast"></div>
  <script>
    var chart = echarts.init(document.getElementById('chart'));
    var option = {
      // ... user's chart configuration ...
      // === Export tool (appended directly to option) ===
      toolbox: {
        right: 16,
        top: 0,
        feature: {
          saveAsImage: {
            type: 'png',
            pixelRatio: 2,       // 2=high definition, can be set to 3 for ultra HD
            title: 'Export PNG Image',
            name: 'chart'        // Download file name
          }
        }
      }
    };
    chart.setOption(option);
    window.addEventListener('resize', function() { chart.resize(); });

    // Listen for export completion event, show toast notification
    chart.on('download', function() {
      var t = document.getElementById('toast');
      t.textContent = 'Image saved'; t.classList.add('show');
      setTimeout(function() { t.classList.remove('show'); }, 2000);
    });
  </script>
</body>
</html>
```

## Chart Type Selection

| Data Scenario | Recommended Chart | series.type |
|---------|---------|------------|
| Compare categorical data | Bar chart | bar |
| Trends over time | Line chart | line |
| Part-to-whole proportion | Pie chart | pie |
| Relationship between two variables | Scatter plot | scatter |
| Multi-series trend comparison | Multi-line chart | line |
| Geographic distribution | Map | map |
| Distribution density | Heatmap | heatmap |
| Level/progress | Gauge | gauge |
| Relationships/flows | Sankey/Radar | sankey / radar |
| Mixed scenarios | Combo chart | multiple series |

## Core Configuration

```js
var option = {
  title: { text: 'Title', subtext: 'Subtitle', left: 'center' },
  tooltip: { trigger: 'axis' },
  legend: { data: ['Series Name'], top: 30 },
  grid: { left: '10%', right: '10%', bottom: '15%', containLabel: true },
  xAxis: { type: 'category', data: ['x-axis data'] },
  yAxis: { type: 'value' },
  series: [{ name: 'Sales', type: 'bar', data: [5, 20, 36] }]
};
```

## Complete Examples for Common Charts

### Bar Chart
```js
xAxis: { type: 'category', data: ['Shirts','Sweaters','Chiffon','Pants','Heels','Socks'] },
yAxis: { type: 'value' },
series: [{ name: 'Sales', type: 'bar', data: [5, 20, 36, 10, 10, 20] }]
```

### Line Chart
```js
xAxis: { type: 'category', data: ['Jan','Feb','Mar','Apr','May'], boundaryGap: false },
series: [
  { name: 'Revenue', type: 'line', data: [12, 25, 18, 30, 42], smooth: true },
  { name: 'Expenses', type: 'line', data: [8, 15, 12, 20, 28], smooth: true }
]
```

### Pie Chart
```js
series: [{
  type: 'pie', radius: '55%',
  data: [
    { value: 335, name: 'Direct Visit' },
    { value: 310, name: 'Email Marketing' },
    { value: 234, name: 'Affiliate Ads' },
    { value: 135, name: 'Search Engine' }
  ],
  label: { show: true, formatter: '{b}: {d}%' }
}]
```

### Scatter Plot
```js
xAxis: { type: 'value', name: 'Height (cm)' },
yAxis: { type: 'value', name: 'Weight (kg)' },
series: [{ type: 'scatter', symbolSize: 12, data: [[172,68],[168,62],[177,75],[159,55],[180,82]] }]
```

## Export Functionality (toolbox.saveAsImage)

ECharts has built-in export capability. Simply add the following configuration to your option to see the export icon in the top-right corner of the chart:

```js
toolbox: {
  right: 16,   // Distance from right edge
  top: 0,      // Distance from top edge
  feature: {
    saveAsImage: {
      type: 'png',       // or 'jpeg'
      pixelRatio: 2,     // Pixel density: 1=standard 2=high definition 3=ultra high
      title: 'Export PNG Image',
      name: 'chart'      // Download file name (without extension)
    }
  }
}
```

**Show a notification after export:**
```js
chart.on('download', function() {
  // Show Toast "Image saved"
});
```

**Console API:**
```js
window.__echarts_export__.getPngUrl(2);   // Get PNG dataURL
window.__echarts_export__.resize();       // Trigger redraw
```

## Style Themes

```js
echarts.init(dom, 'dark');   // Dark theme
echarts.init(dom, 'light'); // Light theme (default)
```

Custom color palette: `color: ['#5470C6','#91CC75','#FAC858','#EE6666','#73C0DE','#3BA272','#FC8452','#9A60B4']`

## Output File

Generate a complete .html file, save it to the workspace, including:
- ECharts 5.x CDN import (no local files required)
- Built-in export icon in the top-right corner of the chart (toolbox.saveAsImage)
- Toast notification after export completion
- Responsive resizing (window.resize)
- `window.__echarts_export__` console API

For detailed API and examples, see [references/api.md](references/api.md)