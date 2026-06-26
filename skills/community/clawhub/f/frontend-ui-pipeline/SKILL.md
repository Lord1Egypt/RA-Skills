---
name: frontend-ui-pipeline
description: "Frontend UI workflow for turning vague ideas, UI drafts, and feedback into buildable frontend plans and iteration steps."
---

# Frontend UI Pipeline

Use when the user has a page, app, or product idea but cannot yet define the UI, structure, or implementation path.

Orchestrate:
- UI brief
- design direction
- build plan
- review plan
- iteration plan
- design record

## Trigger when

- the user has a vague UI, page, app, or product idea and needs structure
- the user wants help defining layout, flow, style, or interaction direction before building
- the user needs a buildable frontend plan, not just inspiration
- the user has an early UI draft and needs review plus next-step iteration planning
- the user wants to move from idea → structure → build → review in one guided workflow

## Skip when

- the task is backend, API, database, infra, or non-visual logic work
- the user already has a complete implementation brief or final design spec and only needs coding
- the task is a tiny visual polish request with no planning, review, or iteration need
- the request is critique-only with no intention to build, revise, or prioritize next steps
- a specialized skill alone is clearly the better fit:
  - `frontend-design` for direct UI implementation
  - `web-design-guidelines` for pure UI audit
  - `ui-ux-pro-max` for pure design-system or style-direction work

## Optional companion skills

Best experience comes from pairing this skill with these optional companions:

- `ui-ux-pro-max` for stronger strategy, style, and interaction-direction work
- `frontend-design` for stronger UI implementation output
- `web-design-guidelines` for stronger audit, accessibility, and polish review

This skill should still produce briefs, plans, review structure, and next-step guidance even when companion skills are unavailable.

When the environment allows, check whether these companion skills are available before routing work to them. If they are missing, continue with the workflow using built-in planning and review structure, and note that companion skills would improve output quality.

See `references/guides/companion-skills.md` for expected fallback behavior and recommended wording.

## Recommended skill combinations

- **Planning only:** use `frontend-ui-pipeline` alone to produce the current stage artifact.
- **Strategy + planning:** use `frontend-ui-pipeline` first, then `ui-ux-pro-max` when style, hierarchy, navigation, or interaction direction needs stronger design judgment.
- **Planning + implementation:** use `frontend-ui-pipeline` to create the brief, direction, and build plan, then route the build handoff to `frontend-design`.
- **Review + iteration:** use `web-design-guidelines` for audit depth, then use `frontend-ui-pipeline` to convert findings into an iteration plan.
- **Full loop:** `frontend-ui-pipeline` → `ui-ux-pro-max` → `frontend-design` → `web-design-guidelines` → `frontend-ui-pipeline`.

## Workflow

1. Classify the request.
2. Clarify goal, user, main action, scope, and constraints.
3. Define strategy, style, layout, and interaction direction.
4. Produce the next artifact.
5. Route to build or review.
6. If files are created or modified for a frontend UI, create or update `DESIGN.md`.

## Default path

- vague idea → `references/templates/ui-brief-template.md`
- unclear UX/style → `references/templates/design-direction-template.md`
- ready to build → `references/templates/build-plan-template.md`
- existing UI to improve → `references/templates/review-plan-template.md`
- post-review changes → `references/templates/iteration-plan-template.md`

## Output standard

Every invocation should end with one clear next-stage artifact or decision.

When possible, produce exactly one primary artifact for the current stage.

### UI Brief
Must include:
- product or page type
- target user
- primary goal
- main action or CTA
- scope and constraints
- open questions

### Design Direction
Must include:
- strategy
- style direction
- layout pattern
- navigation pattern
- interaction principles

### Build Plan
Must include:
- pages or screens
- key components
- required states
- responsive rules
- accessibility requirements
- implementation target

### Review Plan
Must include:
- major issues
- medium issues
- review priorities
- fix-now items
- recommended path: polish or redesign

### Iteration Plan
Must include:
- what stays
- what changes
- priority order
- next implementation step
- next review focus

### DESIGN.md
When this workflow creates or modifies frontend files, also create or update `DESIGN.md` in the project or feature root.

Must include:
- current design direction
- target user and primary goal
- layout and navigation decisions
- color, typography, spacing, and component rules
- key screens, states, and interactions
- responsive and accessibility decisions
- companion skills used or recommended
- open decisions and next review focus

Use `references/templates/design-record-template.md` as the preferred structure.

### Required ending

End each run with one of:
- the primary artifact for this stage
- a prioritized next action
- 3-5 focused questions if critical information is still missing

### Question limit

- Ask only for missing details that materially change the next artifact.
- Prefer 3-5 focused questions, not open-ended discovery dumps.
- If enough is already clear, proceed with assumptions and state them briefly.

## Scenario routes

- landing page → `references/pipelines/landing-page-pipeline.md`
- SaaS dashboard → `references/pipelines/saas-dashboard-pipeline.md`
- admin panel → `references/pipelines/admin-panel-pipeline.md`
- mobile app → `references/pipelines/mobile-app-pipeline.md`

## Skill routing

- `ui-ux-pro-max` when style, hierarchy, or interaction direction is unclear
- `frontend-design` when structure is clear and the next step is implementation
- `web-design-guidelines` when existing UI/code needs audit, polish, or accessibility review

Treat these as optional companion skills, not hard dependencies.

## Prompt help

- use `references/guides/prompt-help.md` when the user cannot describe the request well
- prefer plain language over frontend jargon
- ask only for missing details that change the next step
- if companion skills are unavailable, continue with the workflow and say which optional companion would strengthen the result
- use `references/guides/companion-skills.md` for fallback and companion-skill guidance
- use `examples/` when the user wants to see what a good output looks like

## Anti-patterns

- too many discovery questions
- jumping into code before hierarchy is clear
- continuing style discussion when the user is asking to build
- treating review findings as final instead of turning them into the next pass
