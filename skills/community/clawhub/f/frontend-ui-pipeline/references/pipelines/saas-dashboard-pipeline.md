# SaaS Dashboard Pipeline

Use this when the user wants an app dashboard, product workspace, analytics surface, team tool, or operational UI.

## Recommended strategy
- Default to **efficiency-first**
- Add **readability-first** for data-heavy interfaces
- Add **accessibility-first** for long-session or enterprise use

## Step 1. Clarify essentials
- Who uses the dashboard?
- What top tasks must users complete quickly?
- What data matters most on first load?
- What decisions should this dashboard help users make?
- Is this a single dashboard or a full multi-page product?

## Step 2. Define design direction
- Common style choices: minimalism / flat / dark mode / enterprise-neutral
- Typical layout: sidebar + topbar + content
- Typical navigation: sidebar with filters, tabs, or breadcrumbs
- Key interaction goal: reduce friction and cognitive load

## Step 3. Build page/module plan
Typical modules:
1. Overview dashboard
2. Data table or list view
3. Detail panel or detail page
4. Filters / search / sorting
5. Empty / loading / error states
6. Settings or configuration surfaces
7. Notifications or status indicators

## Step 4. Build plan requirements
- Strong hierarchy between summary and detail
- Fast scanning for metrics, tables, and actions
- Stable layout under loading and filtering
- Clear state design for empty/error/loading/success
- Keyboard and focus friendliness for repeated use

## Step 5. Review priorities
Focus review on:
- Task efficiency
- Information density
- Label clarity
- Table/filter usability
- Navigation predictability
- Responsiveness for smaller laptop widths and tablets
- Accessibility for forms, controls, and data presentation

## Common risks
- Overcrowded first screen
- Too many visual accents competing with data
- Weak empty states
- Filters hidden or confusing
- Important actions buried in secondary menus

## Next prompt shape
"Design a SaaS dashboard for [user type] focused on [top tasks], using a [style] direction, with clear [tables/metrics/filters/workflows] and efficient navigation."
