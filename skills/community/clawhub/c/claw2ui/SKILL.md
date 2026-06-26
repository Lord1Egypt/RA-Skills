---
name: claw2ui
description: 'Generate interactive web pages (dashboards, charts, tables, reports) and serve them via public URL. Use this skill when the user explicitly asks for data visualization, dashboards, analytics reports, comparison tables, status pages, or web-based content. Also triggers for: "draw me a chart", "make a dashboard", "show me a table", "generate a report", "visualize this data", "render this as a page", "publish a page", "claw2ui". If the response would benefit from charts, sortable tables, or rich layout, **suggest** using Claw2UI and wait for user confirmation before publishing. Chinese triggers: "做个仪表盘", "画个图表", "做个报表", "生成一个页面", "做个dashboard", "数据可视化", "做个网页", "展示数据", "做个表格", "做个图", "发布一个页面", "做个看板". Additional English triggers: "create a webpage", "show analytics", "build a status page", "make a chart", "data overview", "show me stats", "create a board", "render a page", "comparison chart", "trend analysis", "pie chart", "bar chart", "line chart", "KPI dashboard", "metrics overview", "weekly report", "monthly report".'
license: MIT
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - node
        - claw2ui
      optionalBins:
        - cloudflared
    install:
      - id: claw2ui-npm
        kind: npm
        package: claw2ui
        bins: ["claw2ui"]
        label: "Install Claw2UI CLI (npm install -g claw2ui)"
        verify: "https://github.com/0xsegfaulted/claw2ui"
      - id: cloudflared-brew
        kind: brew
        formula: cloudflared
        bins: ["cloudflared"]
        label: "Install cloudflared (optional, for self-hosted tunnels)"
    sideEffects:
      - "Writes ~/.claw2ui.json (server URL and API token for authentication)"
      - "Publishes page content to a public URL (default: https://0xsegfaulted-claw2ui.hf.space)"
      - "Requires explicit user confirmation before every publish"
    permissions:
      - "network: POST page content to Claw2UI server API"
      - "filesystem: write ~/.claw2ui.json (auth token), /tmp/*.ts (temp spec files)"
---

# Claw2UI - Agent-to-UI Bridge

Generate interactive web pages from TypeScript DSL specs and serve them via a public URL. Pages include Tailwind CSS, Alpine.js, and Chart.js out of the box, with pluggable themes, type checking, and mobile-responsive layouts.

> **Source**: [GitHub](https://github.com/0xsegfaulted/claw2ui) · [npm](https://www.npmjs.com/package/claw2ui) · [HF Space](https://huggingface.co/spaces/0xsegfaulted/claw2ui) · License: MIT

## Data Safety & User Confirmation

**Every published page is accessible via a public URL. Never publish without explicit user approval.**

- **Always confirm with the user** before publishing — describe what will be published and wait for explicit "yes"/"go ahead". Silent publishing is never acceptable
- **Never include** secrets, credentials, API keys, tokens, PII, or internal endpoints in page content
- **Sanitize** all user-provided data before embedding — the `html` component is sanitized server-side, but avoid passing raw untrusted input to other components
- **Use TTL** for ephemeral or sensitive data so pages auto-expire: `--ttl 3600000` (1 hour)
- **Review content** before publishing — check that no sensitive information leaks through table rows, stat values, or chart labels

## Setup

Claw2UI uses the public server at `https://0xsegfaulted-claw2ui.hf.space` by default. No local server needed.

```bash
npm install -g claw2ui
claw2ui register --server https://0xsegfaulted-claw2ui.hf.space
# Done! Token saved to ~/.claw2ui.json automatically.
```

> **Self-hosting**: To run your own Claw2UI server (local, Docker, or HF Space), see the [self-hosting guide](ref/self-hosting.md).

## Workflow

### Step 1: Ensure Connection

```bash
# Register once (token saved to ~/.claw2ui.json)
claw2ui register --server https://0xsegfaulted-claw2ui.hf.space
```

### Step 2: Write a TypeScript DSL Spec

Write a `.ts` file. Always wrap content in a `container`. The file is type-checked automatically.

```bash
cat > /tmp/claw2ui_page.ts << 'SPECEOF'
import { page, container, header, row, stat, card, chart, dataset } from "claw2ui/dsl"

export default page("Page Title", [
  container(
    header("Title", "Description"),
    row(3,
      stat("Metric 1", "100", { change: 5.2, icon: "trending_up" }),
      stat("Metric 2", "200"),
      stat("Metric 3", "300"),
    ),
    card("Trend",
      chart("line", {
        labels: ["Jan", "Feb", "Mar"],
        datasets: [dataset("Value", [10, 20, 15], { borderColor: "#3b82f6", tension: 0.3 })],
      }),
    ),
  ),
], { style: "anthropic" })
SPECEOF
```

### Step 3: Confirm with User

Before publishing, tell the user what will be published and confirm they want to proceed. The page will be accessible via a **public URL**. Example:

> "I've prepared a dashboard with [summary of content]. Ready to publish it to a public URL? (Use `--ttl 3600000` for auto-expiry in 1 hour.)"

### Step 4: Publish

Only after user confirmation:

```bash
claw2ui publish --spec-file /tmp/claw2ui_page.ts --title "Dashboard"
# For sensitive/temporary data, always set a TTL:
claw2ui publish --spec-file /tmp/claw2ui_page.ts --title "Dashboard" --ttl 3600000
# Skip type checking for faster publish (not recommended):
claw2ui publish --spec-file /tmp/claw2ui_page.ts --title "Dashboard" --no-check
```

Outputs the public URL.

### Step 5: Share the URL

Include the URL in your response to the user.

## CLI Commands

```bash
# Connection
claw2ui register --server <url>         # Self-service registration
claw2ui init --server <url> --token <t> # Manual config

# Publish
claw2ui publish --spec-file <file.ts> --title "Title"    # From TS DSL (type-checked)
claw2ui publish --spec-file <file.ts> --no-check         # Skip type checking
claw2ui publish --spec-file <file.json> --title "Title"  # From JSON spec (legacy)
claw2ui publish --html "<h1>Hi</h1>" --title "Test"      # Raw HTML
claw2ui publish --spec-file <file> --style anthropic     # With theme
claw2ui publish --spec-file <file> --ttl 3600000         # With TTL (ms)

# Themes
claw2ui themes                          # List available themes

# Manage pages
claw2ui list                            # List all pages
claw2ui delete <page-id>               # Delete a page
claw2ui status                          # Check server status
```

## DSL Function Reference

All functions are imported from `"claw2ui/dsl"`.

### Page Entry

```typescript
page(title, components[], opts?)  // opts: { theme?: "light"|"dark"|"auto", style?: "anthropic"|"classic" }
```

### Layout (accept `...children`)

```typescript
container(...children)              // Outermost wrapper, always use this
row(cols, ...children)              // Grid row: row(3, stat(...), stat(...), stat(...))
column(span, ...children)           // Grid column within a row
card(title, ...children)            // Card with border/shadow
list(direction, ...children)        // "vertical" or "horizontal"
modal(title, ...children)           // Dialog popup
```

### Special Containers

```typescript
tabs(                               // Tabbed sections
  tab("id", "Label", ...children),
  tab("id2", "Label 2", ...children),
)

accordion(                          // Collapsible sections
  section("Title", ...children),
  section("Title 2", ...children),
)
```

### Data Display

```typescript
stat(label, value, opts?)           // opts: { change?: number, icon?: string }
chart(chartType, data, opts?)       // opts: { height?, options?, legendPosition?, title? }
table(columns, rows, opts?)         // opts: { searchable?, perPage? }
```

### Helpers (for chart/table)

```typescript
dataset(label, data[], opts?)       // Chart.js dataset: dataset("Rev", [1,2,3], { borderColor: "red" })
col(key, label?, format?)           // Column def: col("name", "Name", "currency")
badge(key, label, badgeMap)         // Badge column: badge("status", "Status", { Active: "success" })
months(n)                           // Month labels: months(6) → ["Jan","Feb","Mar","Apr","May","Jun"]
```

### Input

```typescript
button(label, variant?)             // variant: "primary"|"secondary"|"danger"|"outline"
textField(label?, opts?)            // opts: { placeholder?, value?, inputType? }
select(label, options)              // options: [{ value: "a", label: "Option A" }]
checkbox(label, value?)
choicePicker(label, options, opts?) // opts: { value?, variant?, displayStyle? }
slider(label, opts?)                // opts: { min?, max?, value? }
dateTimeInput(label, opts?)         // opts: { value?, enableDate?, enableTime?, min?, max? }
```

### Media & Text

```typescript
markdown(content)                   // Renders markdown to styled HTML (preferred for rich text)
text(content, opts?)                // opts: { size?, bold?, class? }
code(content, language?)            // Code block with syntax highlighting
html(content)                       // Raw HTML (sanitized server-side)
icon(name, size?)                   // Material Icon: icon("settings", 24)
image(src, alt?)
video(url, poster?)
audioPlayer(url, description?)
divider()
spacer(size?)
```

### Navigation

```typescript
header(title, subtitle?)            // Page header
link(href, label?, target?)         // Hyperlink
```

### Available Themes (`style` field)

| Theme | Description |
|-------|-------------|
| `anthropic` | **(default)** Warm editorial aesthetic — Newsreader serif headings, terracotta accents, cream backgrounds |
| `classic` | Original Tailwind look — blue accents, system fonts, gray surfaces |

## Best Practices

### Always use TypeScript DSL, not JSON

The DSL is type-checked, uses ~60% fewer tokens, and supports logic. JSON specs are still supported but considered legacy.

### Use loops and conditionals

```typescript
// Generate stats from data
const metrics = [
  { label: "CPU", value: "42%", icon: "monitor" },
  { label: "Memory", value: "6.2 GB", icon: "memory" },
  { label: "Disk", value: "120 MB/s", icon: "storage" },
]
row(3, ...metrics.map(m => stat(m.label, m.value, { icon: m.icon })))

// Conditional rendering
container(
  header("Report"),
  data.length > 0
    ? card("Trend", chart("line", chartData))
    : text("No data available"),
)

// Filter falsy values
container(
  header("Dashboard"),
  showMetrics && row(3, stat("A", "1"), stat("B", "2"), stat("C", "3")),
  card("Details", table(cols, rows)),
)
```

### Prefer `col()` / `badge()` / `dataset()` helpers

```typescript
// Good — concise and readable
table(
  [col("name", "Name"), col("rev", "Revenue", "currency"), badge("status", "Status", { Active: "success" })],
  rows,
)

// Avoid — verbose raw objects
table(
  [{ key: "name", label: "Name" }, { key: "rev", label: "Revenue", format: "currency" }, { key: "status", label: "Status", format: "badge", badgeMap: { Active: "success" } }],
  rows,
)
```

### Use `markdown()` for rich text

```typescript
card("About",
  markdown(`
## Features
- **Fast** — sub-second rendering
- **Secure** — sanitized HTML output
- **Responsive** — mobile-first layouts

> Built with Claw2UI
  `),
)
```

### Use `months()` for chart labels

```typescript
chart("bar", {
  labels: months(6),
  datasets: [dataset("Revenue", [100, 200, 150, 300, 250, 400])],
})
```

## Design Patterns

### Dashboard

```typescript
import { page, container, header, row, stat, card, chart, table, col, badge, dataset } from "claw2ui/dsl"

export default page("Dashboard", [
  container(
    header("Dashboard", "Overview"),
    row(3,
      stat("Revenue", "$1.2M", { change: 15.3, icon: "payments" }),
      stat("Orders", "8,432", { change: 8.1, icon: "shopping_cart" }),
      stat("Customers", "2,847", { change: -2.5, icon: "group" }),
    ),
    card("Trend",
      chart("line", {
        labels: months(6),
        datasets: [dataset("Revenue", [320, 410, 380, 450, 480, 520], {
          borderColor: "#3b82f6", tension: 0.3, fill: true,
          backgroundColor: "rgba(59,130,246,0.1)",
        })],
      }, { height: 280 }),
    ),
    card("Details",
      table(
        [col("name", "Name"), col("value", "Value", "currency"), badge("status", "Status", { Active: "success", Inactive: "error" })],
        [
          { name: "Product A", value: 450000, status: "Active" },
          { name: "Product B", value: 320000, status: "Active" },
          { name: "Product C", value: 0, status: "Inactive" },
        ],
      ),
    ),
  ),
], { style: "anthropic" })
```

### Report with Tabs

```typescript
import { page, container, header, row, stat, card, chart, table, tabs, tab, text, markdown, col, dataset, months } from "claw2ui/dsl"

export default page("Monthly Report", [
  container(
    header("Monthly Report", "March 2026"),
    tabs(
      tab("overview", "Overview",
        row(3,
          stat("Users", "12,847", { change: 18.5, icon: "group" }),
          stat("Revenue", "$89K", { change: 24.3, icon: "payments" }),
          stat("Churn", "3.2%", { change: -1.1, icon: "trending_down" }),
        ),
        card("Growth",
          chart("line", {
            labels: months(6),
            datasets: [
              dataset("Users", [8000, 9200, 10100, 11000, 11800, 12847], { borderColor: "#3b82f6" }),
              dataset("Revenue", [52, 58, 65, 72, 81, 89], { borderColor: "#10b981", yAxisID: "y1" }),
            ],
          }),
        ),
      ),
      tab("details", "Details",
        table(
          [col("page", "Page"), col("views", "Views"), col("bounce", "Bounce", "percent")],
          [
            { page: "/", views: "23,456", bounce: 28 },
            { page: "/pricing", views: "12,567", bounce: 22 },
            { page: "/docs", views: "9,876", bounce: 18 },
          ],
        ),
      ),
      tab("notes", "Notes",
        markdown("## Key Takeaways\n\n- Revenue up **24.3%** MoM\n- Churn improved by 1.1pp\n- `/pricing` page has lowest bounce rate"),
      ),
    ),
  ),
], { style: "anthropic" })
```

### Comparison

```typescript
import { page, container, header, row, card, stat, text, table, col } from "claw2ui/dsl"

export default page("Plan Comparison", [
  container(
    header("Plan Comparison", "Choose the right plan"),
    row(3,
      card("Starter",
        stat("Price", "$9/mo"),
        text("5 users, 10 GB storage"),
      ),
      card("Pro",
        stat("Price", "$29/mo", { icon: "star" }),
        text("25 users, 100 GB storage"),
      ),
      card("Enterprise",
        stat("Price", "Custom", { icon: "business" }),
        text("Unlimited users, 1 TB storage"),
      ),
    ),
    card("Feature Matrix",
      table(
        [col("feature", "Feature"), col("starter", "Starter"), col("pro", "Pro"), col("enterprise", "Enterprise")],
        [
          { feature: "Users", starter: "5", pro: "25", enterprise: "Unlimited" },
          { feature: "Storage", starter: "10 GB", pro: "100 GB", enterprise: "1 TB" },
          { feature: "Support", starter: "Email", pro: "Priority", enterprise: "Dedicated" },
        ],
      ),
    ),
  ),
], { style: "anthropic" })
```
