---
name: crm-antdesign-admin-spec
description: Design, structure, review, and generate B2B CRM or admin pages using an Ant Design-style system with page taxonomy, reusable layout rules, token guidance, component mapping, and AI-generation constraints. Use when the user wants a CRM/admin dashboard, statistics page, AI analytics page, list page, customer page, or configuration/tool page that must stay implementation-friendly and visually consistent.
---

# CRM Ant Design Admin Spec

## What this skill is for

Use this skill when the user needs help with:
- designing a B2B CRM / admin page
- generating a page spec before UI or frontend work starts
- reviewing whether a page matches Ant Design-style admin semantics
- keeping dashboard, list, and config pages from drifting into inconsistent styles
- creating prompts for UIUXProMax or similar AI page-generation workflows

This skill is especially useful when:
- the page belongs to a CRM, SaaS admin, analytics, or operations system
- the output needs strong structure and good information density
- the page should feel realistic to implement with Ant Design
- the user wants a reusable design system instead of one-off pretty mockups

## What this skill is NOT for

Do **not** use this as the main skill for:
- marketing websites
- landing pages
- mobile-app-first interfaces
- expressive visual branding projects
- illustration-heavy storytelling pages
- highly experimental visual design where implementation realism is secondary

## Default design direction

Prefer:
- Ant Design-style admin UI
- strong hierarchy and structure
- realistic implementation paths
- compact but readable information organization
- reusable page skeletons
- light AI-enhanced visual language only when the page truly needs it

Avoid:
- marketing-site aesthetics
- heavy glassmorphism
- cyberpunk / glow-heavy visuals
- mobile-first interaction patterns for desktop admin tasks
- decorative gradients across the entire page

## Core operating rule

First classify the page type, then apply the matching structure and constraints.

Do **not** treat every page like a dashboard.

## Page type decision

Choose one of these before designing:

1. **Statistics page**
   - KPI cards
   - charts
   - time filters
   - org tree / left filter panel
   - management overview

2. **AI analytics page**
   - analytics dashboard
   - insights / risks / recommendations
   - KPI + charts + AI summary blocks
   - slightly enhanced visual tone allowed

3. **List page**
   - customer lists
   - operational tables
   - search / filters / pagination
   - CRUD-oriented workflow

4. **Configuration / tool page**
   - parameter setup
   - upload areas
   - forms + tables
   - left functional menu + right config content

If uncertain, default to the simplest page type that matches the task.

## How to use this skill

### For design tasks
- identify the page type first
- outline the page skeleton
- specify major regions: header, filters, actions, KPI, charts, table, side nav, config form, empty state
- keep the result implementation-friendly

### For review tasks
Check for:
- wrong page type choice
- inconsistent spacing / radius / color hierarchy
- non-Ant-Design-like controls
- excessive decoration
- weak information density
- weak admin usability
- dashboard thinking forced onto list/config pages

### For AI generation tasks
Use prompt patterns from `references/prompt-templates.md`.

### For design-system alignment
Use `references/token-and-components.md`.

### For page skeleton and visual rules
Use `references/admin-guidelines.md`.

### For concrete examples
Use `references/examples.md`.

## Recommended output pattern

When generating a page spec or design direction:

1. Identify the page type
2. Pick the matching skeleton
3. Apply token / color / radius / typography rules
4. Map to likely Ant Design components
5. Add AI-specific enhancement only if the page truly needs it
6. State what should *not* be done for this page type

## Deliverable styles this skill can support

This skill can guide outputs such as:
- page strategy notes
- page information architecture
- UI section breakdowns
- component recommendations
- prompt templates for AI design/build tools
- design review comments
- implementation-friendly HTML / React / admin page planning prompts

## References

- Read `references/admin-guidelines.md` for visual system, page taxonomy, and page skeletons.
- Read `references/token-and-components.md` for token mapping and Ant Design component mapping.
- Read `references/prompt-templates.md` when creating prompts for UIUXProMax or other AI page generators.
- Read `references/examples.md` for example page interpretations and output patterns.
