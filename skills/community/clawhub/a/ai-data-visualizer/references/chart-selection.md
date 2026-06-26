# Chart Selection Rules

## Data Type Detection

The script automatically detects 4 column types:

| Type | Criteria | Examples |
|------|----------|----------|
| **numeric** | ≥80% of values parse as numbers | Sales, Temperature, Quantity |
| **datetime** | ≥80% match date patterns (YYYY-MM-DD, etc.) | Date, Time |
| **categorical** | ≤30 unique values, ≤50% of total rows | Category, Region, Status |
| **text** | Everything else | Description, Notes |

## Chart Selection Strategy

### 1. Time Series (datetime + numeric)
- Chart: **Line chart** (filled area)
- Creates one chart per numeric column (max 3)
- Sorted by time dimension
- Best for: sales trends, stock prices, temperature changes

### 2. Category Comparison (categorical + numeric, ≤15 categories)
- Chart: **Bar chart** + optional **Doughnut chart**
- Aggregates using mean (bar) or sum (doughnut)
- Creates up to 2 bar charts + 1 doughnut
- Best for: regional sales, product performance, demographics

### 3. Correlation Analysis (2+ numeric, no datetime)
- Chart: **Scatter plot**
- Uses first two numeric columns
- Best for: price vs quantity, age vs income

### 4. Fallback (numeric only)
- Chart: **Bar chart** (index-based)
- One chart per numeric column (max 5)
- Best for: standalone metric visualization

## Chart Type Cheat Sheet

| Data Pattern | Recommended Chart | Why |
|---|---|---|
| Date + Value | Line / Area | Shows trend over time |
| Category + Value (few) | Bar + Doughnut | Compare + show proportions |
| Category + Value (many) | Horizontal Bar | Better readability for long labels |
| Value + Value | Scatter / Bubble | Show correlation |
| Single Value Set | Histogram | Distribution |
| Parts of Whole | Pie / Doughnut | Proportion (≤6 slices) |
| Ranked Data | Horizontal Bar | Rankings naturally read top to bottom |
| 3+ Variables | Bubble / Radar | Multi-dimensional comparison |

## Color Palette

- **category10**: 10-color palette for categorical data (ECharts-inspired)
- **default**: 10-color palette for single-series data