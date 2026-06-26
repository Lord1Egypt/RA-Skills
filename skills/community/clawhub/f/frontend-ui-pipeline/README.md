# frontend-ui-pipeline

Turn vague UI ideas into a buildable frontend workflow.

## What it is

`frontend-ui-pipeline` is a workflow-first UI skill for anyone who has a page, product, app idea, UI draft, or feedback but no clear next frontend step yet. It helps turn vague ideas into structured frontend briefs, design direction, build plans, review loops, and iteration steps.

Instead of acting like just another design generator or frontend builder, it supports the full UI delivery flow:

1. clarify goals and user needs
2. define strategy, style, layout, and interaction direction
3. produce a buildable frontend plan
4. review early UI output
5. turn feedback into the next iteration

## Who it's for

- founders
- product managers
- designers
- frontend developers
- indie makers
- operators
- anyone with a UI idea, draft, or feedback but no clear next frontend step

## Optional companion skills

For the best experience, pair this skill with these optional companion skills:

- `ui-ux-pro-max` for stronger strategy, style, and interaction-direction work
- `frontend-design` for stronger UI implementation output
- `web-design-guidelines` for stronger audit, accessibility, and polish review

`frontend-ui-pipeline` should still work without them. In that case, it can still produce briefs, design direction, build plans, review structure, and iteration guidance, but with less specialized downstream execution.

When the runtime or platform supports it, check whether these companion skills are installed before routing work to them.
See `references/guides/companion-skills.md` for fallback behavior and recommended wording.

## What it does

- turns vague UI ideas into structured frontend briefs
- helps define strategy, style, layout, and interaction direction
- produces implementation-oriented build plans
- converts review findings into actionable iteration tasks
- creates or updates `DESIGN.md` when frontend files are created or modified
- supports scenario-based workflows for landing pages, SaaS dashboards, admin panels, and mobile apps

## Workflow stages

- UI Brief
- Design Direction
- Build Plan
- Review Plan
- Iteration Plan

## Scenario pipelines

- Landing page
- SaaS dashboard
- Admin panel
- Mobile app

## Included references

### Core templates
- `references/templates/ui-brief-template.md`
- `references/templates/design-direction-template.md`
- `references/templates/build-plan-template.md`
- `references/templates/review-plan-template.md`
- `references/templates/iteration-plan-template.md`
- `references/templates/design-record-template.md`

### Scenario guides
- `references/pipelines/landing-page-pipeline.md`
- `references/pipelines/saas-dashboard-pipeline.md`
- `references/pipelines/admin-panel-pipeline.md`
- `references/pipelines/mobile-app-pipeline.md`

### Prompt help
- `references/guides/prompt-help.md`

### Companion skill guide
- `references/guides/companion-skills.md`

### Examples
- `examples/landing-page-brief.md`
- `examples/dashboard-build-plan.md`
- `examples/review-to-iteration.md`

## Best use cases

- "I have a product idea but don't know how to structure the UI."
- "Help me define the pages and flow before coding."
- "Turn this rough idea into a frontend build plan."
- "Review this first-pass UI and tell me what to fix next."
- "Help me decide whether this needs polish or a redesign."

## Positioning

A workflow-first UI planning and delivery skill for moving from idea, draft, or review into a clearer frontend next step.

## When to use

Use this skill when you need a guided UI workflow, especially for:

- turning a vague page or product idea into a structured frontend brief
- defining strategy, style, layout, and interaction direction before building
- converting product goals into a buildable frontend plan
- reviewing an early UI draft and deciding what to improve next
- moving through brief → direction → build → review → iteration in one workflow

## When not to use

Do not use this skill when:

- the task is backend, API, database, infrastructure, or non-visual logic work
- you already have a final design spec and only need direct UI coding
- you only want a pure design audit with no revision path
- you only need a tiny visual tweak with no planning or iteration workflow
- a specialized skill alone is the better fit

## Example invocation

- "Help me turn this product idea into a UI brief and build plan."
- "I have a dashboard concept. Define the structure, interaction direction, and next build steps."
- "Review this first UI draft, identify the biggest issues, and give me the next iteration plan."
- "Plan a landing page workflow for this product and tell me what should be built first."

## Companion skill note

If your environment supports companion skills, it is recommended to also have:
- `ui-ux-pro-max`
- `frontend-design`
- `web-design-guidelines`

If they are not installed, this skill should still guide the workflow and produce the appropriate stage artifact.

Recommended combinations:
- **Planning only:** `frontend-ui-pipeline`
- **Strategy + planning:** `frontend-ui-pipeline` + `ui-ux-pro-max`
- **Planning + implementation:** `frontend-ui-pipeline` + `frontend-design`
- **Review + iteration:** `web-design-guidelines` + `frontend-ui-pipeline`
- **Full delivery loop:** `frontend-ui-pipeline` → `ui-ux-pro-max` → `frontend-design` → `web-design-guidelines` → `frontend-ui-pipeline`

## Design record

When this skill creates or modifies frontend files, it should also create or update `DESIGN.md` in the project or feature root.

`DESIGN.md` records the current design scheme: target user, goal, style direction, layout, navigation, components, states, responsive rules, accessibility decisions, companion skills used, open decisions, and next review focus.

## Version

**Current release:** v1.1.0

### Release focus
- stable workflow structure
- scenario-based UI pipelines
- reusable templates for brief, direction, build, review, and iteration
- plain-language prompt guidance for users who do not think in frontend terminology
