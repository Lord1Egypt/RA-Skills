# Prompt Templates

Use these as templates when generating CRM/admin pages with UIUXProMax or similar AI design/build tools.

## General prompt

Design a B2B CRM/admin page using Ant Design-style semantics.

Requirements:
- professional, rational, structured admin UI
- high information density with strong readability
- primary color around `#1677FF`
- success `#00CA75`, warning `#FF8008`, error `#FF525C`
- text hierarchy based on `#333333`, `#545759`, `#8C8C8C`
- radius system: 10 / 6 / 4
- layout uses top business navigation + optional left nav/tree + main content area
- output must be implementation-friendly and suitable for desktop admin workflows

Forbid:
- marketing-site hero style
- heavy glassmorphism
- cyberpunk / glow-heavy style
- mobile-app-first visual language
- large decorative gradients across the full page

## Statistics page prompt

Design a CRM statistics page.

Include:
- page title
- search/filter/export area
- optional org tree or hierarchy panel
- time switching (today / yesterday / last 7 days / this month)
- 4~6 KPI cards
- 2-column chart area
- detail table or summary section

Use Ant Design-style admin structure and strong management readability.

## AI analytics page prompt

Design an AI analytics page for a CRM/admin system.

Include:
- title + subtitle
- time switching
- KPI area
- insight cards
- chart area
- risk / recommendation section
- ranking or detail section

Allow a light AI-enhanced visual tone, but keep the page within a realistic admin system aesthetic.

## List page prompt

Design a CRM/admin list page.

Include:
- page title
- filter bar
- action bar (add / export / batch operations)
- table section
- pagination

Prioritize information density, clarity, and realistic implementation.

## Configuration page prompt

Design a CRM/admin configuration page.

Include:
- left functional navigation
- right configuration content
- form controls
- select / input number / input / tooltip
- upload area if relevant
- config table if relevant
- submit/save action area

Do not style this like a dashboard.
Keep it tool-like, stable, and implementation-friendly.
