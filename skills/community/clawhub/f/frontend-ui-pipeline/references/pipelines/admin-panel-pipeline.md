# Admin Panel Pipeline

Use this when the user wants an internal operations panel, CMS, moderation system, back-office tool, or configuration-heavy interface.

## Recommended strategy
- Default to **efficiency-first**
- Add **clarity-first** for operational correctness
- Add **accessibility-first** when operators spend long hours in the tool

## Step 1. Clarify essentials
- Who operates this panel?
- What objects are they managing? users / orders / content / permissions / inventory / settings
- What actions are sensitive or irreversible?
- What information must always remain visible?
- What mistakes are most costly?

## Step 2. Define design direction
- Common style choices: flat / minimal / enterprise-functional
- Typical layout: sidebar + dense content area
- Typical navigation: sidebar + breadcrumbs + utility topbar
- Key interaction goal: speed with low error risk

## Step 3. Build page/module plan
Typical modules:
1. Resource list or table
2. Search / filter / bulk actions
3. Detail view or edit form
4. Status badges and audit indicators
5. Permissions / role visibility states
6. Confirmation dialogs for destructive actions
7. Logs, history, or activity surfaces

## Step 4. Build plan requirements
- Very clear action hierarchy
- Safe handling for destructive operations
- Dense but readable tables and forms
- Persistent context when navigating between list and detail
- Strong empty/error/loading state behavior

## Step 5. Review priorities
Focus review on:
- Error prevention
- Clarity of destructive vs safe actions
- Form quality and validation
- Auditability and status visibility
- Table readability and bulk workflows
- Accessibility for repeated data entry and keyboard use

## Common risks
- Ambiguous destructive buttons
- Cramped forms and tables
- Missing confirmation or undo paths
- Weak distinction between primary and dangerous actions
- Overcomplicated navigation for routine tasks

## Next prompt shape
"Design an admin panel for managing [resources], optimized for [top tasks], with clear operational safety, efficient tables/forms, and a [style] enterprise UI direction."
