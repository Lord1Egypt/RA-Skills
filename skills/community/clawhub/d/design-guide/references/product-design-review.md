# Existing Product Design Review

Use this when the user asks to evaluate, review, audit, critique, or improve an existing product/page design and expects strengths, weaknesses, and practical optimization recommendations.

This workflow covers screenshots, URLs, local HTML files, live app routes, prototypes, repository surfaces, and design exports. It is diagnostic by default: do not implement changes unless the user explicitly asks for implementation or approves a redesign direction.

## Accepted Inputs

Accept any useful combination of:

- Product context: audience, business goal, primary workflow, usage frequency, brand constraints.
- Artifact: URL, screenshot, local HTML file, app route, prototype, image export, repository path, or component path.
- Review target: whole product, single page, flow, responsive layout, visual direction, accessibility, interaction behavior, conversion path, or redesign readiness.
- Constraints: platform, framework, existing design system, implementation budget, rollout risk, analytics dependencies, SEO constraints, and deadline.
- Comparison target: competitor, reference product, previous version, proposed redesign, or accepted design contract.

If context is missing, infer what is safe from the artifact and state assumptions. Ask only when the missing context would materially change the evaluation, such as whether the page is an operational tool or a marketing page.

## Scope Gate

Before running a product design review, confirm the explicit scope requested by the user. Do not default to a full audit.

State one line at the start of your response:

```text
Review scope: <what the user explicitly asked for>
Not included by default: <items not mentioned by the user, e.g. mobile audit, implementation, redesign, social media use>
```

### When to pause and confirm

Pause before expanding scope when any of these is true:

- The user only says "evaluate this URL / screenshot / page" without naming the review target.
- The user did not mention mobile / responsive, but you are about to include mobile findings.
- The user did not mention accessibility, but you are about to run an accessibility audit.
- The user did not ask for redesign or implementation, but you are about to propose one.
- The user did not mention downstream goals (blog post, social media, case study, pitch deck, etc.), but you are about to tailor the output for them.

If any of these is true, confirm the expanded scope with the user first.

### Default safe scope

When the user gives a single URL or screenshot and says only "evaluate this", default to:

- Primary viewport: desktop only, unless the artifact is clearly a mobile screen.
- Review target: single page, visual hierarchy, task flow basics, craft, and obvious usability issues.
- Output: scorecard, strengths, top issues, and prioritized actionable improvements.
- Excluded by default: mobile audit, tablet audit, full accessibility audit, redesign, implementation, and any downstream publishing goal.

### Mobile / responsive review trigger conditions

Include mobile or responsive review only when at least one of these is true:

- The user explicitly asks for mobile, responsive, tablet, or narrow-screen evaluation.
- The product is clearly a mobile-first or mobile-heavy surface (app, webview, miniprogram, mobile site).
- The provided artifact itself is a mobile screenshot or mobile frame.
- The task or workflow being evaluated is primarily used on mobile devices.
- The user has previously confirmed mobile as in scope for this specific review.

When mobile is not in scope, do not list mobile-only findings as P0 or P1 issues. You may note them as a single out-of-scope observation.

### No inherited side goals

Do not carry unrelated goals from earlier conversation history into the current review unless the user explicitly re-states them for this task.

Examples of side goals that must not be inherited by default:

- Publishing a blog post, WeChat article, social media post, or video.
- Preparing a pitch deck, case study, or marketing asset.
- Implementing the improvements, building a redesign, or shipping code.
- Syncing to another tool, repository, or AIDE environment.

If you are unsure whether a historical goal still applies, treat it as out of scope.

## Review Mode Routing

First classify the artifact. Use one primary mode and optional secondary modes:

| Mode | Use When | Extra Checks |
|---|---|---|
| Marketing/conversion page | Landing page, homepage, campaign page, pricing page | Message clarity, proof, trust, hero fit, CTA path, copy quality, SEO/OG risk |
| SaaS/admin/product workbench | Dashboard, admin panel, internal tool, editor, creator console | Task speed, data density, table/list operations, state coverage, reversibility, permissions |
| Data visualization/dashboard | Metrics, charts, monitoring, analytics | Data hierarchy, chart legibility, comparison model, freshness, filters, empty/error data states |
| Form/wizard/checkout | Multi-step input, onboarding, application flow | Field order, validation, recovery, progress, autofill, error location, destructive exits |
| Mobile/webview | Narrow-screen or embedded mobile surface | Thumb reach, bottom actions, reflow, fixed elements, keyboard viewport, safe areas |
| Redesign audit | Existing surface will be changed | Preserve IA, route slugs, analytics hooks, brand tokens, accessibility wins, SEO baseline |
| Accessibility audit | User asks for inclusive/accessibility review | Keyboard path, focus order, labels, contrast, semantics, reduced motion, zoom/reflow |
| Competitive/reference comparison | User provides competitor/reference | What to borrow, what to reject, differentiation, parity gaps, verification needed |

## Specialized Review Templates

Use exactly the relevant templates; do not expand the review scope merely because a template exists:

- `references/review-templates/data-tables.md`: tables, queues, inventories, CRM/admin grids.
- `references/review-templates/dashboards.md`: analytics, monitoring, KPIs, and decision dashboards.
- `references/review-templates/complex-forms.md`: onboarding, applications, checkout, configuration, and multi-step editors.
- `references/review-templates/mobile-navigation.md`: mobile-first navigation or explicitly requested mobile review.
- `references/review-templates/high-risk-batch-actions.md`: destructive, permissioned, financial, publishing, and multi-record operations.

For operational tools, prefer the SaaS/admin/product workbench mode over marketing-page heuristics. Do not penalize a dense tool merely because it is not airy or editorial.

## Evidence Protocol

Every P0/P1 finding must include explicit evidence. Prefer this compact format:

```text
Evidence:
- artifact: <URL / screenshot / file / route / component>
- viewport: <1440x900 / 1024x768 / 390x844 / unknown>
- location: <page region or component>
- observation: <what is visible or what happened>
- impact: <which user task or business goal is harmed>
- confidence: <high / medium / low>
```

When reviewing live or local pages, capture evidence only for viewports in scope. If mobile or tablet is in scope, capture those too; otherwise start with desktop. If evidence is incomplete, label the missing verification step instead of overstating certainty.

## Product UI Deep Audit

For dashboards, tools, editors, and admin panels, check these product-specific dimensions in addition to `references/review-rubric.md`:

- Information architecture: navigation, grouping, naming, current location, and task entry points.
- Primary workflow length: steps to complete the most common job, avoidable context switches, and repeated decisions.
- Data density: whether the density fits daily use, not whether it looks spacious.
- Table/list operations: filtering, sorting, search, saved views, bulk selection, pagination, column priority, long text, and row actions.
- Decision safety: destructive actions, batch operations, confirmation, undo, audit trail, role gating, and recovery.
- State coverage: loading, empty, partial, stale, error, permission, offline, long-running, optimistic, rollback, and success states.
- Data trust: source, freshness, confidence, calculation explanation, sampling, and uncertainty.
- Feedback quality: status announcements, progress, validation, inline errors, and post-action results.
- Accessibility: keyboard path, focus management, accessible names, contrast, zoom/reflow, and reduced-motion behavior.
- Maintainability: component consistency, token use, layout primitives, responsive rules, and dependency fit.

## Anti-AI Design Tell Check

Read `references/anti-ai-design-tells.md` when the review target includes visual polish, redesign, landing pages, dashboards, or user dissatisfaction with generic AI-looking UI.

Use those checks as evidence, not taste absolutism. A pattern is a problem only when it harms product fit, trust, originality, clarity, or task completion.

## Review Workflow

1. Define the product role, target user, primary job, review mode, and success criteria.
2. Inspect the artifact. Capture or request responsive evidence when possible.
3. Score the design with `references/review-rubric.md` and add mode-specific checks from this file.
4. Identify what works well before listing problems.
5. Classify issues by priority:
   - `P0`: blocks the primary workflow, causes serious misunderstanding, fails essential accessibility, risks data loss, or makes the page unusable on a required device.
   - `P1`: materially reduces efficiency, comprehension, trust, conversion, safety, or maintainability.
   - `P2`: polish, consistency, minor discoverability, or optional enhancement.
6. Convert findings into actionable recommendations with target area, evidence, rationale, implementation hint, tradeoff, effort, acceptance criteria, and required verification.
7. Offer improvement tracks:
   - Low-cost fix: can usually be implemented without changing IA or core components.
   - Medium improvement: requires layout, component, state, or content restructuring.
   - Structural redesign: requires design artifact presentation, confirmation, implementation contract, and QA.
8. If the user asks for redesign or implementation, continue through the normal design-guide design-depth, artifact presentation, confirmation, contract, implementation, and QA gates.

## Before/After Comparison

When evaluating an existing version against a redesign, prototype, or proposed change:

- Score both versions with the same rubric and review mode.
- List improved categories, regressed categories, and unchanged risks.
- Reject changes that look more polished but make the primary workflow slower, less safe, or less understandable.
- Require evidence for claimed improvement: screenshot comparison, flow-step count, task timing estimate, fewer visible decisions, fewer errors, or clearer acceptance criteria.

## Competitive Or Reference Comparison

When a competitor/reference is in scope:

- Use current evidence for current products; verify with browsing when the reference could have changed and the user has not supplied screenshots.
- Separate parity gaps from differentiation opportunities.
- State what should be borrowed, what should be rejected, and what requires product/business validation.
- Do not copy brand assets, proprietary layouts, or distinctive trade dress.

## Report Template

```markdown
# Product Design Review: <product/page>

## Executive Summary

- Review mode: <marketing / product workbench / data dashboard / form flow / mobile / redesign / accessibility / competitive>
- Overall judgment: <fit / partially fit / does not fit>
- Biggest strength: <specific strength>
- Highest-risk issue: <specific issue>
- Recommended next move: <low-cost fix / medium improvement / structural redesign>

## Assumptions And Evidence

- Product role:
- Target user:
- Primary job:
- Artifacts reviewed:
- Viewports checked:
- Missing evidence:

## Scorecard

| Category | Score / 10 | Evidence |
|---|---:|---|
| Direction fit |  |  |
| Task flow |  |  |
| Visual hierarchy |  |  |
| Craft |  |  |
| Usability |  |  |
| Responsiveness |  |  |
| Originality |  |  |

## Mode-Specific Findings

- <product UI, marketing, data, form, mobile, redesign, accessibility, or competitive finding>

## What Works Well

- <specific strength and why it matters>

## Issues By Priority

### P0

- <issue>
  Evidence:
  - artifact:
  - viewport:
  - location:
  - observation:
  - impact:
  - confidence:

### P1

- <issue with evidence and impact>

### P2

- <issue with evidence and impact>

## Actionable Improvements

| Area | Problem | Evidence | Recommendation | Implementation Hint | Tradeoff | Effort | Acceptance Criteria | Verification |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | S/M/L |  |  |

## Improvement Tracks

### Low-Cost Fixes

1. <safe change>

### Medium Improvements

1. <component, layout, state, or content restructure>

### Structural Redesign

1. <requires design artifact, confirmation, contract, and QA>

## Responsive, Accessibility, And State Risks

- Responsive:
- Accessibility:
- States:
- Data trust:
- Decision safety:

## Before/After Or Competitive Delta

- Improved:
- Regressed:
- Still unresolved:
- Borrow:
- Reject:

## Suggested Implementation Plan

1. <highest-leverage change>
2. <second change>
3. <verification>

## Verification Checklist

- [ ] Primary workflow is faster or clearer.
- [ ] Required breakpoints have no overlap, clipping, or accidental horizontal scroll.
- [ ] Keyboard and screen-reader basics remain usable.
- [ ] Text, data, and actions survive realistic long-content cases.
- [ ] Destructive and batch actions are protected and recoverable.
- [ ] Data source, freshness, confidence, and uncertainty are visible where decisions depend on them.
- [ ] Changes preserve or improve the scorecard categories that were already strong.
```

## Chinese Report Template

When the user is working in Chinese, keep the same structure and use these headings:

- 设计评估摘要
- 假设与证据
- 评分表
- 模式专项发现
- 做得好的地方
- 按优先级排列的问题
- 可落地优化建议
- 改良路径
- 响应式、可访问性与状态风险
- 前后对比或竞品差距
- 建议实施计划
- 验收清单

## Quality Rules

- Ground every major finding in observable evidence: screenshot region, route, component, user flow, copy, state, or breakpoint.
- Do not give vague advice such as "make it cleaner", "modernize the UI", or "improve hierarchy" without a concrete target and acceptance criterion.
- Every recommendation must say what to change, why it matters, how to change it, which user task it affects, what risk it carries, how to accept it, and how to verify it.
- Separate diagnosis from redesign and implementation. A review can recommend a redesign, but it must not silently become implementation work.
- Include tradeoffs when a recommendation improves one metric while risking another, such as density versus readability.
- For operational tools, prioritize workflow efficiency, data clarity, reversibility, keyboard behavior, and failure states over decorative visual novelty.
- For marketing or conversion pages, prioritize message clarity, proof, trust, hierarchy, responsiveness, and conversion path.
- If evidence is incomplete, label the confidence level and the missing verification step.
