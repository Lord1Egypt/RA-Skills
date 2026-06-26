---
name: data-visualization-studio
description: Create interactive and static data visualizations from datasets. Supports charts, graphs, dashboards, and statistical plots with multiple output formats (PNG, SVG, HTML, PDF).
---

# Data Visualization Studio

Create professional data visualizations from raw data or existing datasets.

## When to Use

- Creating charts and graphs from CSV, JSON, or database data
- Building interactive dashboards for data exploration
- Generating statistical plots and visual analytics
- Exporting visualizations in multiple formats (PNG, SVG, HTML, PDF)
- Creating publication-ready figures and reports

## Quick Start

### Basic Chart Creation
```python
# Example: Create a simple bar chart
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
plt.bar(data['category'], data['values'])
plt.savefig('chart.png', dpi=300, bbox_inches='tight')
```

### Interactive Dashboard
```python
# Example: Create interactive plot with Plotly
import plotly.express as px

df = pd.read_csv('data.csv')
fig = px.scatter(df, x='x_column', y='y_column', color='category')
fig.write_html('dashboard.html')
```

## Supported Libraries

- **Matplotlib**: Static plots, publication-quality figures
- **Plotly**: Interactive visualizations, web dashboards  
- **Seaborn**: Statistical graphics, beautiful default styles
- **Bokeh**: Interactive web plots, streaming data support
- **Altair**: Declarative visualization, Vega-Lite integration

## Output Formats

- **PNG/JPEG**: High-resolution static images
- **SVG**: Scalable vector graphics for web/print
- **HTML**: Interactive web pages with embedded JavaScript
- **PDF**: Publication-ready documents
- **JSON**: Data export for further processing

## Best Practices

1. **Data Preparation**: Clean and validate data before visualization
2. **Color Schemes**: Use accessible color palettes (avoid red-green)
3. **Labels**: Always include clear axis labels and titles
4. **Resolution**: Use appropriate DPI for intended use (72 for web, 300+ for print)
5. **File Size**: Optimize file sizes for web delivery when needed

## Advanced Features

- **Animation**: Create animated transitions and time-series visualizations
- **Geospatial**: Map-based visualizations with geographic data
- **3D Plots**: Three-dimensional data representation
- **Custom Styling**: Brand-consistent themes and styling
- **Real-time**: Live updating visualizations from streaming data

## References

For detailed examples and advanced usage patterns, see the bundled reference files:
- `references/chart-types.md` - Complete catalog of supported chart types
- `references/styling-guide.md` - Customization and branding guidelines  
- `references/performance.md` - Optimization for large datasets