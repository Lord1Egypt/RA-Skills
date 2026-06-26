---
name: agent-plan-manager
description: |
  Structured plan management for OpenClaw Agent's tasks and execution workflows.

  Use when the OpenClaw Agent needs to create, track, or break down execution plans into actionable steps.
version: 1.0.0
author: 文轩先师
---

# Agent Plan Manager

Manage OpenClaw Agent's execution plans and task workflows in a structured, trackable way.

**Who is it for?** OpenClaw Agent that needs to organize tasks, track execution progress, or document step-by-step implementation plans.

**What makes it different?**

- **Agent-Centric**: designed for AI agent execution workflows with clear entry/exit points
- **Structured**: separates high-level goals from detailed tool-calling steps
- **Trackable**: uses checkboxes and status fields for execution state visibility
- **Lightweight**: just Markdown files, integrates with OpenClaw's file system tools

## Quick Start

1. Create `plans/plans-overview.md` from the overview template
2. Add execution items to the table with appropriate status
3. If a plan needs detailed steps, create `plans/detailed/XX-{plan-name}.md`
4. Update `plans/detailed/index.md` to link the new plan
5. Update statuses as execution progresses

## Directory Structure

```text
plans/
├── plans-overview.md      ← from templates/plans-overview.md
└── detailed/
    ├── index.md           ← from templates/index.md
    └── XX-{plan-name}.md  ← from templates/detailed-plan.md
```

## When to Use

- Creating a new execution plan for complex tasks
- Tracking multi-step tool calling workflows
- Breaking down user requests into actionable steps
- Recording detailed execution documentation
- Structured agent task management

## Example: Web Scraping Task

**Step 1** — Add to `plans/plans-overview.md`:

```markdown
| 1 ||***|| Web scraping for product prices ||***|| In Progress ||***|| High ||***|| TBD ||***|| TBD ||***|| Extract prices from example.com |
```

**Step 2** — Create `plans/detailed/01-web-scraping.md`:

```markdown
# Detailed Plan - Web Scraping for Product Prices

## Plan ID: #1

## Objective
Extract product prices from example.com and save to a CSV file.

## Schedule
TBD

## Deadline
TBD

## Tool Sequence

1. `browser_navigate` → example.com/products
2. `browser_snapshot` → extract product list
3. `browser_click` → navigate to each product
4. `WriteFile` → save results to products.csv

## Implementation Steps

### 1. Navigate to target URL
- [x] Use browser_navigate to load example.com/products

### 2. Extract product data
- [ ] Capture page snapshot
- [ ] Parse product names and prices
- [ ] Handle pagination if present

### 3. Save results
- [ ] Format data as CSV
- [ ] Write to products.csv

## Estimated Token Usage
~2K tokens
```

**Step 3** — Update `plans/detailed/index.md`:

```markdown
| #1 | Web scraping for product prices | TBD | TBD | [01-web-scraping.md](./detailed/01-web-scraping.md) |
```

## Templates

All templates live in `templates/`:

- **`plans-overview.md`** — High-level execution board with status table
- **`index.md`** — Index of all detailed execution plans
- **`detailed-plan.md`** — Step-by-step execution plan with tool sequences

## Tips

- Keep plan names concise; use kebab-case for filenames (`01-web-scraping.md`)
- Update `last_updated` in frontmatter whenever the overview changes
- Use checkboxes (`- [ ]`) in detailed plans to track execution progress
- Include tool sequences to clarify the execution flow
- Archive completed plans by moving them to the "Completed Items" section
- Estimate token usage when possible for complex multi-step tasks
