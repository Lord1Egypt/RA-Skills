# Companion Skills

`frontend-ui-pipeline` works on its own, but it produces stronger results when paired with a few optional companion skills.

These are **optional enhancements**, not hard dependencies.

## Recommended companion skills

### 1. `ui-ux-pro-max`
Use for stronger:
- product strategy
- style direction
- layout decisions
- navigation patterns
- interaction framework selection

Best fit when:
- the user says the UI should feel more premium, modern, clear, or professional
- the structure exists but the experience direction is still weak
- the product needs more consistent design thinking across screens

If missing:
- `frontend-ui-pipeline` should still produce a `Design Direction`
- style and interaction recommendations may be less specialized

---

### 2. `frontend-design`
Use for stronger:
- page implementation output
- component design output
- polished frontend structure
- production-style UI generation

Best fit when:
- the brief and design direction are already clear
- the next step is building pages, sections, or components
- the user wants actual UI output rather than only planning

If missing:
- `frontend-ui-pipeline` should still produce a `Build Plan`
- implementation guidance may remain planning-oriented instead of design-output-oriented

---

### 3. `web-design-guidelines`
Use for stronger:
- UX audit
- accessibility checks
- polish review
- consistency review
- usability-focused critique

Best fit when:
- the user already has a draft, mockup, prototype, or code
- the goal is to identify issues before the next pass
- the team needs a structured review and fix priority list

If missing:
- `frontend-ui-pipeline` should still produce a `Review Plan` and `Iteration Plan`
- review findings may be less specialized or less rigorous

## Expected behavior

When the environment supports companion-skill checks:

1. Check whether these companion skills are available.
2. If available, route the appropriate stage to the relevant companion skill.
3. If unavailable, continue the workflow without failing.
4. Briefly note which optional companion skill would improve the result.

## Recommended combinations

### Planning only
Use:
- `frontend-ui-pipeline`

Best when:
- the user needs a brief, design direction, build plan, review plan, or iteration plan
- no file creation or implementation is requested yet

Output:
- one current-stage artifact
- assumptions and open questions
- next recommended action

### Strategy + planning
Use:
- `frontend-ui-pipeline`
- `ui-ux-pro-max`

Best when:
- style, hierarchy, navigation, or interaction direction is unclear
- the user wants the UI to feel more premium, trustworthy, modern, or professional

Output:
- design direction
- strategy rationale
- next build or review route

### Planning + implementation
Use:
- `frontend-ui-pipeline`
- `frontend-design`

Best when:
- the brief and direction are clear enough to build
- the user wants actual frontend UI files, pages, sections, or components

Output:
- build plan
- frontend builder handoff
- created or modified files
- `DESIGN.md` recording the current design scheme

### Review + iteration
Use:
- `web-design-guidelines`
- `frontend-ui-pipeline`

Best when:
- the user already has a UI draft, prototype, or implementation
- the goal is to decide what to fix first

Output:
- review findings
- fix priority plan
- iteration plan
- updated `DESIGN.md` if files or design decisions change

### Full delivery loop
Use:
- `frontend-ui-pipeline`
- `ui-ux-pro-max`
- `frontend-design`
- `web-design-guidelines`
- `frontend-ui-pipeline`

Best when:
- the user wants to move from vague idea to implementation and review

Output:
- UI Brief
- Design Direction
- Build Plan
- implemented UI
- Review Plan
- Iteration Plan
- `DESIGN.md`

## Fallback behavior

If none of the companion skills are available, `frontend-ui-pipeline` should still be able to:

- clarify the request
- produce a UI Brief
- define a Design Direction
- create a Build Plan
- structure a Review Plan
- turn findings into an Iteration Plan

In other words:
- with companion skills → stronger execution quality
- without companion skills → still usable as a workflow and planning skill

## Suggested wording when companions are missing

Examples:

- "I can continue with the workflow and produce the build plan directly. If `frontend-design` is available, it would strengthen the implementation output."
- "I can structure the review and next iteration now. If `web-design-guidelines` is installed, the audit can be more specialized."
- "I can define the direction from here. If `ui-ux-pro-max` is available, it would improve strategy and interaction guidance."
