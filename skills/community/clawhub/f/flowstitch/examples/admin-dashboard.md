# Example: Admin Dashboard Design

This shows FlowStitch §2A in action — generating a premium admin dashboard with the correct prompt structure and design system.

---

## Input

**User:** "I need an admin dashboard for FlowMetrics, our SaaS analytics tool. Dark theme, professional."

---

## Generated DESIGN.md

```markdown
# Design System: FlowMetrics Admin
**Project ID:** [generated on first Stitch call]

## 1. Visual Theme & Atmosphere
FlowMetrics Admin is a **precision instrument** — the Bloomberg Terminal of analytics dashboards. The dark canvas creates visual silence so data speaks louder than chrome. Every pixel earns its place: no decorative elements, only information with purpose. The atmosphere is calm authority — a tool used by professionals who know what they're looking for.

## 2. Color Palette & Roles
- **Obsidian Canvas** (#0D1117) — Primary page background, the foundation
- **Midnight Panel** (#161B27) — Elevated surfaces: cards, panels, data tables
- **Slate Divider** (#1E293B) — Borders, table separators, subtle structure
- **Aurora Violet** (#7C3AED) — Primary accent: active nav, KPI highlights, primary buttons
- **Lavender** (#A78BFA) — Secondary accent: links, hover states, chart line 1
- **Glacier White** (#F8FAFC) — Primary text: values, headlines
- **Fog Gray** (#94A3B8) — Secondary text: labels, metadata, timestamps
- **Emerald** (#10B981) — Positive trend indicators, success states
- **Rose** (#F43F5E) — Negative trend indicators, error states
- **Amber** (#F59E0B) — Warning states, neutral trends

## 3. Typography Rules
- **Font:** Inter — engineered for data readability at small sizes
- **Large Values (KPI):** Bold (700), 2.5rem, letter-spacing -0.02em
- **Section Headers:** Semibold (600), 0.875rem, uppercase, letter-spacing 0.06em, Fog Gray
- **Data Values:** Medium (500), 0.875rem, tabular-nums (monospace numbers for alignment)
- **Labels:** Regular (400), 0.75rem, Fog Gray
- **Body/Descriptions:** Regular (400), 0.875rem, line-height 1.5

## 4. Component Stylings
* **KPI Cards:** Midnight Panel background, 1px Slate Divider border, 12px corner, 24px padding.
  Value in Glacier White (2.5rem bold). Label in Fog Gray (0.75rem uppercase). 
  Trend: +X% in Emerald with ↑ arrow / -X% in Rose with ↓ arrow.
* **Data Table:** Midnight Panel background. Alternating rows: transparent / #1a2234 (barely visible).
  40px row height. Fog Gray header text (uppercase, 0.75rem). Values in Glacier White.
  Hover row: Slate Divider background.
* **Sidebar:** 240px expanded (icon + label). 60px collapsed (icon only). 
  Active item: Aurora Violet (#7C3AED) at 15% opacity, left 2px accent bar in full violet.
  Nav labels in Fog Gray, active in Glacier White.
* **Charts:** Area/line charts use Lavender (#A78BFA) as primary line, 20% opacity fill below.
  Bar charts use Aurora Violet. Grid lines at 20% opacity Slate Divider.
* **Filter Bar:** Search input (Midnight Panel bg, Slate Divider border, 8px radius).
  Filter chips: Slate Divider background, Fog Gray text — active: Aurora Violet 15% bg, Lavender text.
* **Buttons:** Aurora Violet fill, Glacier White text, 8px radius. Secondary: Slate Divider border.

## 5. Layout Principles
- **Sidebar:** Fixed left, 240px expanded / 60px collapsed. Full viewport height.
- **Main content:** Left margin = sidebar width. Top bar = 64px fixed.
- **Content area padding:** 24px all sides
- **KPI row:** 4 equal columns, 16px gap
- **Table:** Full width, fixed header on scroll
- **Section spacing:** 24px between major sections (data-dense vs. editorial spacing)
- **Max content width:** None — fill available space (dashboard paradigm)

## 6. Design System Notes for Stitch Generation

**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first, data-dense, admin panel
- Theme: Dark, professional, utilitarian, precision-instrument aesthetic
- Background: Obsidian Canvas (#0D1117) — primary canvas
- Surface: Midnight Panel (#161B27) — cards, panels, table background
- Border: Slate Divider (#1E293B) — all borders and separators
- Primary Accent: Aurora Violet (#7C3AED) — active states, primary CTA, KPI highlights
- Secondary Accent: Lavender (#A78BFA) — links, hover states, chart primary line
- Text Primary: Glacier White (#F8FAFC) — values, headlines
- Text Secondary: Fog Gray (#94A3B8) — labels, metadata, section headers
- Success: Emerald (#10B981) — positive trends
- Error: Rose (#F43F5E) — negative trends, errors
- Font: Inter, 700 for KPI values, 600 semibold for headers, 400 for labels
- Sidebar: Fixed left, 240px expanded (icon+label) / 60px collapsed (icon-only)
- KPI Cards: 12px corners, Midnight Panel bg, subtle 1px border
- Tables: 40px row height, alternating subtle rows, Fog Gray header labels
- Charts: Lavender primary line, violet bars, barely-visible grid lines
- Layout: Fixed sidebar + fixed top bar + scrollable content area, 24px content padding
```

---

## Example Page Structure — Main Dashboard

```markdown
A professional dark-themed analytics dashboard — the main overview page.

**DESIGN SYSTEM (REQUIRED):**
[paste Section 6 block from above]

**Page Structure:**
1. **Fixed Sidebar (left):** FlowMetrics logo, navigation: Overview (active), Analytics, Reports, Customers, Settings. User avatar + name at bottom. Collapse toggle at top.
2. **Fixed Top Bar:** "Overview" page title (left), date range picker (center), "New Report" primary button + notification bell + user avatar (right)
3. **KPI Cards Row (4 columns):** 
   - Total Revenue: $48,291 (+12.3% from last month, Emerald)
   - Active Users: 2,847 (+5.1%, Emerald)  
   - Conversion Rate: 3.42% (-0.8%, Rose)
   - Avg Session: 4m 32s (+15%, Emerald)
4. **Charts Row (2/3 + 1/3 split):**
   - Left: Revenue trend — area chart, 12-month view, Lavender line with fill
   - Right: Traffic sources — donut chart with legend
5. **Data Table:** "Recent Transactions" — Date, Customer, Amount, Status (pill badge), Actions
6. **Activity Feed (right sidebar panel):** Recent system events, timestamps, small icons
```

---

## React Components Generated

```
src/
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx           # Collapsible sidebar with nav items
│   │   └── TopBar.tsx            # Fixed top bar with title + actions
│   ├── dashboard/
│   │   ├── KPICard.tsx           # Metric card with trend
│   │   ├── RevenueChart.tsx      # Area chart wrapper
│   │   ├── TrafficDonut.tsx      # Donut chart wrapper
│   │   └── TransactionsTable.tsx # Sortable data table
│   └── ui/                       # shadcn components (Button, Badge, etc.)
├── data/
│   └── mockData.ts               # Sample transactions, metrics
└── hooks/
    └── useMetrics.ts             # Data fetching / transformation logic
```
