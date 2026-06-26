---
name: E2E自动化工程师-路由与UI冒烟验证
description: E2E automation engineer skill for route smoke checks, HTTP reachability, and lightweight UI confidence validation.
---

# Role

This skill performs lightweight route and UI smoke validation. It is optimized for fast confidence on reachability, rendering, and navigation after changes that do not require a full deep-flow scenario.

# When To Use

- Use for route smoke checks, quick UI reachability checks, backend or frontend page rendering, and HTTP-level confidence validation.
- Use for keywords such as smoke, route check, page renders, HTTP request, 404, 405, and UI sanity.
- Use when the main question is “does the surface still load and route correctly?”

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/testing/SKILL.md`
- `dev/ai/skills/weline-routing/SKILL.md`
- `dev/ai/skills/module-development/SKILL.md`

# Responsibilities

- Prove route registration and basic page reachability quickly.
- Check for obvious backend, frontend, or API regressions.
- Choose HTTP or browser-smoke validation proportional to the change.
- Catch route wiring issues before deeper acceptance work begins.

# Workflow

1. Identify the changed route, page, or UI surface.
2. Determine whether HTTP-level validation is enough or whether a browser smoke is needed.
3. Refresh route registration if the change requires it.
4. Run `http:request` or a minimal E2E smoke path against the affected surface.
5. Check response reachability, basic rendering, and obvious route failures.
6. Re-run the narrow smoke after fixes.
7. Return the route path, command, and observed result.

# Weline Rules

- Do not use `routes.xml`.
- Run `php bin/w setup:upgrade --route` when route registration changed.
- Provide HTTP or E2E validation evidence where relevant.
- Do not use default WLS port `9501` for AI testing when isolated runtime validation is required.

# Inputs Required

- The affected route, controller, page, or API path.
- Whether the change is frontend, backend, or API.
- Any login or runtime prerequisite for the smoke path.
- Expected basic success condition.

# Expected Output

- A fast smoke-validation result for the changed route or UI surface.
- The exact command or minimal browser path used.
- A concise statement of pass, failure, or follow-up required.

# Validation

- Run `php bin/w http:request ...` for direct route checks when appropriate.
- Run the smallest browser smoke path when rendering or navigation must be seen.
- Confirm route refresh was performed if registration changed.
- Confirm obvious 404, 405, auth, or render failures are surfaced clearly.

# Constraints

- Do not confuse smoke validation with full end-to-end coverage.
- Do not skip route refresh when the route graph changed.
- Do not treat a reachable page as proof that deeper business logic is correct.
- Do not use heavyweight browser suites when one focused smoke check is enough.

