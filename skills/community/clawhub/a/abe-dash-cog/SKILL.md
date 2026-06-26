---
name: dash-cog
description: Interactive dashboards and apps powered by SkillBoss API Hub. Data visualization, analytics dashboards, KPI trackers, charts and graphs, interactive HTML apps, data explorers, games. Build web apps with AI.
metadata:
  openclaw:
    emoji: "📊"
author: SkillBoss
dependencies: []
requires.env: [SKILLBOSS_API_KEY]
---

# Dash Cog - Interactive Dashboards & Apps Powered by SkillBoss API Hub

Build interactive dashboards, data visualizations, and web apps with AI.

---

## Prerequisites

This skill uses the SkillBoss API Hub (`/v1/pilot`) for all AI-powered dashboard and app generation.

```bash
pip install requests
```

Set your environment variable:
```bash
export SKILLBOSS_API_KEY=your_key_here
```

**Quick pattern:**
```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

def generate_dashboard(prompt: str, complex_app: bool = False) -> str:
    """Generate a complete self-contained interactive HTML app via SkillBoss API Hub."""
    system_prompt = (
        "You are an expert frontend developer. Generate complete, self-contained interactive HTML "
        "with embedded CSS and JavaScript. Use Chart.js for charts (load from CDN), CSS variables "
        "for theming, responsive layout. No external dependencies beyond CDN links. "
        "Output only the full HTML code, no explanation."
    )
    if complex_app:
        system_prompt += (
            " For complex apps: plan the component structure first, then implement each section "
            "with full interactivity, animations, and polished UX."
        )
    result = requests.post(
        "https://api.heybossai.com/v1/pilot",
        headers={
            "Authorization": f"Bearer {SKILLBOSS_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "type": "chat",
            "inputs": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            },
            "prefer": "quality"
        },
        timeout=120
    ).json()
    return result["result"]["choices"][0]["message"]["content"]

# Standard dashboards and visualizations
html_code = generate_dashboard("[your dashboard/app request]")

# Complex interactive apps and games
html_code = generate_dashboard("[your complex app request]", complex_app=True)
```

---

## What You Can Build

### Analytics Dashboards

Interactive dashboards for data analysis:

- **Sales Dashboard**: "Create an interactive sales analytics dashboard with revenue trends, top products, regional breakdown, and monthly comparisons"
- **Marketing Dashboard**: "Build a marketing performance dashboard showing campaign ROI, channel attribution, and conversion funnels"
- **Financial Dashboard**: "Create a financial overview dashboard with P&L, cash flow, and key financial ratios"
- **HR Dashboard**: "Build an employee analytics dashboard with headcount trends, attrition, and department breakdowns"

### KPI Trackers

Monitor key performance indicators:

- **Business KPIs**: "Create a KPI tracker showing MRR, churn rate, CAC, LTV, and growth metrics"
- **Project KPIs**: "Build a project health dashboard with timeline, budget, resource allocation, and risk indicators"
- **SaaS Metrics**: "Create a SaaS metrics dashboard with activation, retention, and expansion revenue"

### Data Visualizations

Interactive charts and graphs:

- **Time Series**: "Visualize stock price history with interactive zoom and technical indicators"
- **Comparisons**: "Create an interactive bar chart comparing market share across competitors"
- **Geographic**: "Build a map visualization showing sales by region with drill-down"
- **Hierarchical**: "Create a treemap showing budget allocation across departments"
- **Network**: "Visualize relationship data as an interactive network graph"

### Data Explorers

Tools for exploring datasets:

- **Dataset Explorer**: "Create an interactive explorer for this CSV data with filtering, sorting, and charts"
- **Survey Results**: "Build an interactive tool to explore survey responses with cross-tabulation"
- **Log Analyzer**: "Create a log exploration tool with search, filtering, and pattern detection"

### Interactive Apps

Web applications beyond dashboards:

- **Calculators**: "Build an interactive ROI calculator with adjustable inputs and visual output"
- **Configurators**: "Create a product configurator that shows pricing based on selected options"
- **Quizzes**: "Build an interactive quiz app with scoring and result explanations"
- **Timelines**: "Create an interactive timeline of company milestones"

### Games

Simple web-based games:

- **Puzzle Games**: "Create a word puzzle game like Wordle"
- **Memory Games**: "Build a memory matching card game"
- **Trivia**: "Create a trivia game about [topic] with scoring"
- **Arcade Style**: "Build a simple space invaders style game"

---

## Dashboard Features

SkillBoss API Hub generated dashboards can include:

| Feature | Description |
|---------|-------------|
| **Interactive Charts** | Line, bar, pie, scatter, area, heatmaps, treemaps, and more |
| **Filters** | Date ranges, dropdowns, search, multi-select |
| **KPI Cards** | Key metrics with trends and comparisons |
| **Data Tables** | Sortable, searchable, paginated tables |
| **Drill-Down** | Click to explore deeper levels of data |
| **Responsive Design** | Works on desktop, tablet, and mobile |
| **Dark/Light Themes** | Automatic theme support |

---

## Data Sources

You can provide data via:

1. **Inline data in prompt**: Small datasets described directly
2. **File upload**: CSV, JSON, Excel files via SHOW_FILE
3. **Sample/mock data**: "Generate realistic sample data for a SaaS company"

---

## Mode Selection for Dashboards

Choose based on complexity:

| Scenario | Recommended Mode |
|----------|------------------|
| Standard dashboards, KPI trackers, data visualizations, charts | `generate_dashboard(prompt)` |
| Complex interactive apps, games, novel data explorers | `generate_dashboard(prompt, complex_app=True)` |

**Default to standard mode** for most dashboard requests. SkillBoss API Hub's quality LLM routing handles charts, tables, filters, and interactivity efficiently.

Reserve `complex_app=True` for truly complex applications requiring significant design thinking—like building a novel game mechanic or a highly customized analytical tool with multiple interconnected features.

---

## Example Dashboard Prompts

**Sales analytics dashboard:**
```python
html_code = generate_dashboard(
    """Create an interactive sales analytics dashboard with:
- KPI cards: Total Revenue, Orders, Average Order Value, Growth Rate
- Line chart: Monthly revenue trend (last 12 months)
- Bar chart: Revenue by product category
- Pie chart: Sales by region
- Data table: Top 10 products by revenue

Include date range filter. Use this data: [upload CSV or describe data]
Modern, professional design with blue color scheme."""
)
```

**Startup metrics dashboard:**
```python
html_code = generate_dashboard(
    """Build a SaaS metrics dashboard for a startup showing:
- MRR and growth rate
- Customer acquisition funnel (visitors → signups → trials → paid)
- Churn rate trend
- LTV:CAC ratio
- Revenue by plan tier

Generate realistic sample data for a B2B SaaS company growing from $10K to $100K MRR over 12 months."""
)
```

**Interactive data explorer:**
```python
html_code = generate_dashboard(
    """Create an interactive explorer for this employee dataset [upload CSV]. Include:
- Searchable, sortable data table
- Filters for department, location, tenure
- Charts: headcount by department, salary distribution, tenure histogram
- Summary statistics panel

Allow users to download filtered data as CSV."""
)
```

**Simple game:**
```python
html_code = generate_dashboard(
    """Create a Wordle-style word guessing game. 5-letter words, 6 attempts, color feedback
(green = correct position, yellow = wrong position, gray = not in word).
Include keyboard, game statistics, and share results feature. Clean, modern design.""",
    complex_app=True
)
```

---

## Tips for Better Dashboards

1. **Prioritize key metrics**: Don't cram everything. Lead with the 3-5 most important KPIs.

2. **Describe the data**: What columns exist? What do they mean? What time period?

3. **Specify chart types**: "Line chart for trends, bar chart for comparisons, pie for composition."

4. **Include interactivity**: "Filter by date range", "Click to drill down", "Hover for details."

5. **Design direction**: "Modern minimal", "Corporate professional", "Playful and colorful", specific color schemes.

6. **Responsive needs**: "Desktop only" vs "Must work on mobile."
