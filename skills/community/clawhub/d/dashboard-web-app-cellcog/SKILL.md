---
name: dashboard-web-app-cellcog
description: "AI dashboard and web app generation powered by CellCog. Interactive dashboards, KPI trackers, data visualization, charts, analytics apps, data explorers, calculators, games. Responsive HTML apps with real-time filters."
metadata:
  openclaw:
    emoji: "🖥️"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Dashboard & Web App - Interactive Dashboards & Apps Powered by CellCog

Build interactive dashboards, data visualizations, and web apps with AI.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="creative",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="creative",
)
print(result["message"])
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

CellCog dashboards can include:

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

## Choosing Mode & Tier

**Use `chat_mode="creative"` for dashboards and web apps** — the craft-first mode tuned for design taste, visual polish, and voice.

| Scenario | Recommended |
|----------|-------------|
| Dashboards, KPI trackers, interactive apps | `chat_mode="creative"` (default tier `"core"`) |
| Maximum craft on high-stakes pieces | `chat_mode="creative", chat_tier="max"` |
| Quick disposable drafts | `chat_mode="agent", chat_tier="flash"` |

Note: Agent Team (`chat_mode="team"`) is reserved for deep research.

---

## Example Dashboard Prompts

**Sales analytics dashboard:**
> "Create an interactive sales analytics dashboard with:
> - KPI cards: Total Revenue, Orders, Average Order Value, Growth Rate
> - Line chart: Monthly revenue trend (last 12 months)
> - Bar chart: Revenue by product category
> - Pie chart: Sales by region
> - Data table: Top 10 products by revenue
> 
> Include date range filter. Use this data: [upload CSV or describe data]
> Modern, professional design with blue color scheme."

**Startup metrics dashboard:**
> "Build a SaaS metrics dashboard for a startup showing:
> - MRR and growth rate
> - Customer acquisition funnel (visitors → signups → trials → paid)
> - Churn rate trend
> - LTV:CAC ratio
> - Revenue by plan tier
> 
> Generate realistic sample data for a B2B SaaS company growing from $10K to $100K MRR over 12 months."

**Interactive data explorer:**
> "Create an interactive explorer for this employee dataset [upload CSV]. Include:
> - Searchable, sortable data table
> - Filters for department, location, tenure
> - Charts: headcount by department, salary distribution, tenure histogram
> - Summary statistics panel
> 
> Allow users to download filtered data as CSV."

**Simple game:**
> "Create a Wordle-style word guessing game. 5-letter words, 6 attempts, color feedback (green = correct position, yellow = wrong position, gray = not in word). Include keyboard, game statistics, and share results feature. Clean, modern design."

---

## Tips for Better Dashboards

1. **Prioritize key metrics**: Don't cram everything. Lead with the 3-5 most important KPIs.

2. **Describe the data**: What columns exist? What do they mean? What time period?

3. **Specify chart types**: "Line chart for trends, bar chart for comparisons, pie for composition."

4. **Include interactivity**: "Filter by date range", "Click to drill down", "Hover for details."

5. **Design direction**: "Modern minimal", "Corporate professional", "Playful and colorful", specific color schemes.

6. **Responsive needs**: "Desktop only" vs "Must work on mobile."

---

## If CellCog is not installed

**Claude Code, Cursor, Codex + 70 more agents:** `npx skills add cellcog/skills --skill cellcog`
**OpenClaw:** `openclaw skills install @cellcog/cellcog`
**CellCog plugin users:** run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool)
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
