# Csv To Chart

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Converts tabular CSV data into visual charts and graphs — bar, line, scatter, pie, and more

## What Problem This Solves

User has raw CSV data and needs a visual chart — not more numbers to stare at. This skill parses the CSV structure, selects the right chart type for the data shape, and generates runnable code to render it. No more exporting to Excel just to make a simple chart.

**When triggered:** CSV data + chart/graph/visualization intent.

## Features

- **Intelligent chart selection** — picks the optimal chart type based on data shape (bar for categories, line for time-series, scatter for correlation, etc.)
- **Auto column type detection** — identifies numeric, date, and category columns and maps them to axes correctly
- **Multi-format output** — generates code in Python (matplotlib/plotly), JavaScript (chart.js/plotly.js), or Mermaid diagrams
- **Handles edge cases** — warns about >7 pie slices, truncates >500 rows, skips missing values gracefully

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install csv-to-chart

# Or manually
cp -r csv-to-chart ~/.openclaw/skills/
```

### Usage

```
/csv-to-chart
```

Paste your CSV data and ask for a chart — e.g., "make a bar chart from this".

```
/csv-to-chart/suggest
```

Ask which chart type fits your data without generating it yet.

## Modes

| Mode | Description |
|------|-------------|
| `/csv-to-chart` | Default — reads CSV, outputs chart specification + runnable code |
| `/csv-to-chart/suggest` | Recommends the best chart type based on your data shape |

## Examples

| Input | Output |
|-------|--------|
| Monthly sales CSV (month + revenue) | Line chart with month on X, revenue on Y |
| Product categories + counts | Horizontal bar chart, top 10 + "Other" if >7 categories |
| Two numeric columns | Scatter plot with axis labels |
| CSV with 50 rows, missing Q3 | Chart rendered, note added: "3 rows omitted due to missing Q3 sales" |

## Directory Structure

```
csv-to-chart/
├── SKILL.md          # Entry point
├── LICENSE           # MIT
├── README.md         # This file
├── README_zh.md      # Chinese version
├── CONTRIBUTING.md    # Contribution guide
├── .gitignore
├── references/       # Chart type decision tree, code templates
└── tests/            # Test framework
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.