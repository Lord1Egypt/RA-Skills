# Admin Guidelines

## Positioning

This skill is for B2B CRM / admin systems with:
- high information density
- operational efficiency
- strong structure
- Ant Design-style semantics
- optional light AI-enhanced visual tone

## Visual direction

Preferred traits:
- professional
- rational
- credible
- clean
- data-oriented
- light-tech, not flashy

Avoid:
- marketing-site layouts
- mobile-app-first styling
- large decorative hero sections without utility
- style-first decisions that reduce readability

## Core visual rules

### Color system
Suggested baseline:
- primary: `#1677FF`
- success: `#00CA75`
- warning: `#FF8008`
- error: `#FF525C`
- text primary: `#333333`
- text secondary: `#545759`
- text tertiary: `#8C8C8C`
- border: `#EBECED`
- dark nav: `#292E33`
- soft page bg: `#EBF2FF`
- hint bg: `#F2FAFF`

Optional gradient for AI-focused areas only:
- `#2586FF -> #2874FC`

### Typography
Recommended font stack:
```css
font-family: PingFang SC, Segoe UI, Helvetica Neue, Arial, sans-serif;
```

Recommended scale:
- page title: 18 / 26
- section title: 16 / 24
- body + table text: 14 / 22
- secondary body: 13 / 21
- helper text: 12 / 18
- tiny labels: 11 / 16
- KPI numbers: 24~32 / 32~40

### Radius system
- panel / major container: 10px
- card / modal / section: 6px
- button / input / tag: 4px

## Layout rules
Common admin shell:
```text
Top business nav
  ├─ left local nav or tree/filter area
  └─ main content area
       ├─ page header
       ├─ filter / action bar
       ├─ KPI / chart / card area
       └─ table / detail / config area
```

Spacing guidance:
- page padding: 16~24px
- card gap: 16px
- vertical block gap: 16~24px
- inline filter gap: 8~12px

## Page taxonomy

### 1. Statistics page
Use for:
- org / department statistics
- management overview
- KPI + charts + trend pages

Typical structure:
```text
Page title
Search / filter / org tree / export
Time tabs
KPI cards
Chart grid
Detail table / summary block
```

### 2. AI analytics page
Use for:
- insight dashboards
- AI analysis overview
- risks / recommendations / trends

Typical structure:
```text
Title + subtitle
Time tabs
KPI cards
Insight cards
Chart area
Risk / recommendation blocks
Ranking or detail area
```

Note:
- allow light AI-enhanced visuals
- still keep admin consistency
- do not turn it into a big-screen visual demo

### 3. List page
Use for:
- customer lists
- records / operations / management tables

Typical structure:
```text
Page title
Filter bar
Action bar
Table
Pagination
```

### 4. Configuration / tool page
Use for:
- parameter setup
- uploads
- report config
- AI config pages
- tool/workbench pages

Typical structure:
```text
Left functional menu
Right content panel
Form controls
Upload area
Config table
Save / submit actions
```

This page type is important. Do not force these tasks into dashboard-style layouts.

## Component expectations

Prefer:
- clear filters
- compact action bars
- KPI cards with restrained styling
- table-first operational design
- tree / left navigation where hierarchy matters
- realistic empty, loading, and error states

## State design

### Empty state
- concise copy
- useful next step
- light illustration optional

### Loading state
- local skeleton/spin over content blocks
- avoid long blank screens

### Error state
- clear and compact
- retry or refresh path
- avoid exposing raw technical errors to business users
