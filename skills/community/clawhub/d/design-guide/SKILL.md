---
name: design-guide
description: Frontend design and production engineering orchestrator that inventories projects, scales design depth, presents review artifacts, locks executable contracts, implements accessible responsive interfaces, and verifies interactions, visual regressions, and performance. Use when the user invokes design-guide, @design-guide, /design-guide, asks for frontend design/development/redesign, web app UI, dashboard, tool interface, landing page, responsive React/HTML/CSS work, design previews or choices, screenshot QA, production frontend quality, or says they are dissatisfied with generic AI-looking UI. If invoked without a concrete task, enter navigation mode and recommend the best available frontend-related skills/tools for the user's environment instead of coding.
---

# Design Guide

Use this as the frontend entry skill. It is not a single visual style; it controls product thinking, approval, implementation, and production verification.

## Reference Routing

Read only the references required by the task:

- Existing repository or substantial implementation: `references/project-intelligence.md`.
- New screen, major redesign, ambiguous direction, or workflow change: `references/design-process.md`.
- Any artifact created for user review: `references/artifact-presentation.md`.
- Approved Level 2 or multi-state/multi-route implementation: `references/implementation-contract.md`.
- API, form, permissions, async, mutation, or non-trivial state: `references/state-and-data.md`.
- Stack-specific implementation decisions: matching section of `references/framework-adapters.md`.
- Substantial implementation verification: `references/quality-gates.md`.
- UI/UX review request: `references/review-rubric.md`.
- Existing product/page design evaluation, pros/cons critique, or actionable improvement report: `references/product-design-review.md`, `references/review-rubric.md`, and `references/anti-ai-design-tells.md` when visual quality or generic AI-looking UI is in scope.
- Specialized review targets: use the matching file under `references/review-templates/` for data tables, dashboards, complex forms, mobile navigation, or high-risk batch actions.
- Release-level workflow verification or maintainer work: `references/end-to-end-journeys.md`.
- Internationalization, CLI language selection, or translated maintainer docs: `references/internationalization.md`.

## Context Files

Before substantial work, look for preference files in this order:

1. `.design-guide/profile.md` in the current project.
2. `~/.design-guide/preferences.md` on the local machine.
3. `references/design-defaults.md` bundled with this skill.

Read only the files that exist and are relevant. Project and local files override bundled defaults. Keep personal preferences out of the skill folder so the skill remains open-source friendly.

## Invocation Modes

### Mode 1: Navigation

Use this mode when the user only says `design-guide`, `@design-guide`, `/design-guide`, "use design-guide", or otherwise gives no concrete frontend task.

Reply with a concise menu of what the environment can do. Do not code. Do not invent unavailable skills.

1. Inspect the available skill/tool list if the host exposes one.
2. Read `references/helper-registry.md`.
3. Group relevant capabilities by task, not by skill name.
4. Recommend the best primary path and optional helpers.
5. Give 2-3 example prompts the user can run next.

Navigation output should look like:

```text
design-guide is ready. Pick a frontend task:

1. Build a product screen / dashboard / tool
   Primary: design-guide
   Helpers if available: web-design-engineer, webapp-testing

2. Improve visual taste of an existing page
   Primary: design-guide
   Helpers if available: design-taste-frontend, web-design-guidelines

3. Evaluate an existing product/page design
   Primary: design-guide
   Helpers if available: web-design-guidelines, webapp-testing, design-taste-frontend

4. Add complex animation
   Primary: design-guide
   Helpers if available: gsap, animejs

5. Build 3D / WebGL
   Primary: design-guide
   Helpers if available: three
```

If a helper is not visible in the current AIDE, say "not detected here" and continue with the best fallback.

### Mode 2: Execution

Use this mode when the user gives a real frontend task.

Do not start coding immediately unless the task is a tiny isolated UI fix. First choose the design depth, produce and present the required design artifacts, and resolve any approval gate. For substantial work, build a viewable v0 before completing the full interface.

Use the reference routing above. A file is not presented until the user can immediately inspect it.

## Task Routing

Route the user's wording before selecting tools:

- "build a dashboard/admin/tool/editor" -> product screen workflow; make the usable working surface first.
- "make this prettier/redesign/looks AI-generated" -> taste correction workflow; preserve existing function and fix visual hierarchy.
- "match this screenshot/image" -> screenshot-to-code workflow; use screenshot helpers if available.
- "landing page/site/homepage" -> brand or landing workflow; verify product/brand facts when current or specific.
- "animation/motion/transition" -> motion workflow; pick CSS/WAAPI/GSAP/Anime based on complexity and existing dependencies.
- "mobile/miniprogram/responsive" -> mobile-first workflow; audit narrow widths before desktop polish.
- "review/audit/check UX/evaluate existing design/pros and cons/actionable improvements" -> product design review workflow; read `references/product-design-review.md` and `references/review-rubric.md`; also read `references/anti-ai-design-tells.md` when visual quality, redesign, landing pages, dashboards, or generic AI-looking UI is in scope.

For existing product design reviews, start with a scope gate: state the explicit scope requested by the user and what is not included by default. Confirm expanded scope with the user before adding mobile/responsive, accessibility audits, redesigns, implementations, or downstream publishing goals. Then diagnose: classify the review mode, define product context, inspect the artifact, score strengths and weaknesses, and return prioritized, evidence-backed recommendations with implementation hints, tradeoffs, acceptance criteria, and verification steps. Do not redesign or implement unless the user asks for it or approves a proposed direction.

Load one specialized review template when the artifact requires it:

- Data tables, queues, inventories, or admin grids -> `references/review-templates/data-tables.md`.
- Analytics, monitoring, or decision dashboards -> `references/review-templates/dashboards.md`.
- Multi-step, dependent, high-consequence, or long forms -> `references/review-templates/complex-forms.md`.
- Mobile navigation -> `references/review-templates/mobile-navigation.md`, only when mobile is in scope.
- Destructive, permissioned, publishing, financial, or multi-record mutations -> `references/review-templates/high-risk-batch-actions.md`.

## AIDE Compatibility

Treat `design-guide` as tool-neutral.

- Codex: invoke with "use design-guide", `design-guide`, `$design-guide`, or `@design-guide` if the UI supports mentions.
- Claude Code: invoke with `/design-guide` when the skill is installed in the Claude skill directory; natural language "use design-guide" is the fallback.
- Cursor: invoke by asking the agent to use `design-guide` or by pointing it at this `SKILL.md`; if Cursor skill discovery is configured, install this folder under Cursor's skill directory.
- Qwen Code: invoke by asking the agent to use `design-guide`; if Qwen skill discovery is configured, install this folder under Qwen's skill directory.
- Other AIDE: use the same folder as a portable skill; if the tool has no skill protocol, tell the agent to read `SKILL.md` and follow `design-guide`.

For local setup details, read `references/aide-integration.md` only when the user asks about installing, syncing, or using this skill in another AIDE.

## Language And Internationalization

Follow `references/internationalization.md` when the user requests a language, translated instructions, or localized CLI output. Match the user's current request language by default. CLI helpers accept `--locale en|zh-CN` and resolve environment defaults through `F_DESIGN_LOCALE`, `LC_ALL`, and `LANG`. Keep JSON field names and machine-readable values stable in English; localize human-readable help, status, and error text only.

## Workflow

### 1. Read the product context

State one line:

```text
Reading this as: <page/app type> for <audience>, with a <vibe> language, leaning toward <design system or reference family>.
```

Infer from the user request, repo, screenshots, existing CSS, `package.json`, named references, and business context. Ask one concise question only when the design direction genuinely splits.

Before substantial work in a codebase, read `references/project-intelligence.md` and run:

```bash
python3 scripts/inspect-project.py . --format markdown
```

Inspect the reported entry routes, components, tokens, contracts, tests, scripts, and risks before selecting dependencies or files to edit. Use `scripts/detect-frontend-env.sh` only as a lightweight shell fallback.

### 2. Choose the design depth

Classify the work before producing artifacts:

- Level 0 - direct fix: isolated visual or component-state correction; preserve the existing design contract.
- Level 1 - directed design: established product structure and visual language; write a concise brief and layout/state outline.
- Level 2 - exploratory design: new product or major screen, workflow or information-architecture change, major redesign, ambiguous direction, or brand-defining work; produce a reviewable artifact and require confirmation.

Use the lightest level that resolves the uncertainty. State the chosen level and why in one sentence.

### 3. Define the experience

Before visual styling, identify:

- The user's primary job and most important workflow.
- Information and action priority.
- Required page regions, routes, states, and responsive behavior.
- Product, brand, technical, accessibility, and content constraints.
- Observable success criteria.

For API, form, permission, async, mutation, or state-heavy work, read `references/state-and-data.md` and map loading, empty, partial, error, success, permission, pending, retry, and rollback behavior as relevant. Use representative edge-case fixtures rather than happy-path-only demo data.

For Level 1, provide a compact design brief and layout/state outline. For Level 2, map the primary flow and information architecture before choosing a visual direction. Read `references/design-process.md` for the artifact and approval rules.

### 4. Select helper capabilities

Before producing review artifacts or implementation, decide if auxiliary skills/tools are useful. Prefer the host's discovered names. Do not require the user to remember them. Read `references/helper-registry.md` when the selection is not obvious.

- General polished web artifact: use `web-design-engineer` if available.
- Landing page, portfolio, redesign taste correction: use `design-taste-frontend` if available.
- UI audit, accessibility, best-practice review: use `web-design-guidelines` if available.
- Browser screenshot/testing: use `webapp-testing` or local Playwright.
- Complex motion: use `gsap`, `animejs`, `css-animations`, or `waapi` based on the project stack.
- 3D/WebGL: use `three` if available.
- Screenshot-to-code: use `image-to-code` or `yueban-image-to-code` if available.
- Generated UI assets: use image generation skills only when the user asks for visual assets or the design requires them.

If no helper is available, continue with native framework/CSS and state the fallback briefly.

### 5. Explore, present, and confirm the direction

For Level 2, present one recommended direction and up to two materially different alternatives when real alternatives exist. Use the lowest-cost artifact that answers the unresolved question: a layout outline, wireframe, standalone HTML prototype, screenshot or reference board, generated image, or motion prototype.

Present every review artifact before applying the confirmation gate. Resolve `scripts/present-design.py` relative to the loaded skill directory and pass all HTML directions in one invocation. On a shared local desktop, use `open` for standalone HTML; use the managed `serve` command only when HTTP is required. In remote, container, SSH, or headless environments, never present agent-side `127.0.0.1` or `file://` URLs as user-accessible; use host-exposed links or attached screenshots. Read `references/artifact-presentation.md` for lifecycle and fallback rules.

When a confirmation gate applies:

1. Verify that the user has an immediately usable way to inspect each artifact.
2. Show the choices and give a recommendation.
3. Ask the user to approve, choose, or propose changes.
4. Stop implementation while the decision is pending.
5. Restate the approved design contract before continuing.

Do not create a review artifact and then continue coding past it in the same turn. Skip the pause for Level 0, clearly directed Level 1 work, or when the user explicitly grants autonomous design authority.

### 6. Declare the design system

Before implementation, write:

- Product role: operational tool, dashboard, editor, landing page, content site, prototype, etc.
- Audience and use frequency.
- Reference anchors: real apps, brands, design systems, or local existing UI.
- Color system: neutral base, one accent, semantic colors.
- Typography: display/body/code fonts or existing project font.
- Spacing: base unit and container width.
- Radius: one radius strategy.
- Elevation: border, shadow, or flat hierarchy.
- Motion: duration, easing, interaction triggers, reduced-motion behavior.
- Anti-defaults: what must be avoided for this project.

For operational tools, admin panels, creator dashboards, and editors, prefer dense but calm working screens over marketing heroes, decorative cards, and large empty sections.

For approved Level 2 work, include the chosen page structure, responsive behavior, critical states, accepted tradeoffs, and rejected directions in the design contract. If review artifacts used provisional visual tokens, replace them with the approved system.

For approved Level 2 work or any substantial multi-state, multi-route implementation, read `references/implementation-contract.md`, create `.codex/design-guide/design-contract.json`, and validate it with `scripts/design-contract.py validate <contract> --require-approved` before coding. Do not mark a contract approved without user-reviewed artifact evidence.

### 7. Build the approved v0

For new screens or major redesigns, implement a v0 with:

- Real page layout and navigation.
- Representative content, not lorem ipsum.
- Main visual hierarchy and responsive structure.
- Key empty/loading/error states if they affect layout.
- Placeholder assets only when real assets are unavailable.

Treat an approved HTML prototype as the v0 when it uses the target stack and is suitable to continue. Otherwise, build the v0 from the approved design contract. Stop after v0 only when the user requested an additional implementation checkpoint.

### 8. Full implementation

Follow the existing stack and code style first. Check `package.json` before importing libraries. Read only the matching section of `references/framework-adapters.md`. Do not add a new UI library unless the project lacks one and the dependency is justified.

Implementation rules:

- Use existing components, tokens, helpers, and routing conventions.
- Avoid nested cards and section-as-card page structure.
- Use icons from the existing icon family; do not hand-roll SVG icons.
- Implement hover, focus, disabled, loading, empty, error, and long-text states where relevant.
- Preserve semantic HTML, accessible names, complete keyboard behavior, focus management, contrast, zoom/reflow, reduced motion, and status/error announcements.
- Keep text inside buttons and fixed UI elements stable across breakpoints.
- Use CSS Grid for page structure when flex width math would be fragile.
- Do not use viewport-scaled font sizes.
- Avoid default AI-purple/blue gradients unless brand-justified.
- Do not make a landing page when the user asked for a product, app, dashboard, tool, or editor; make the usable screen first.

### 9. Run and Present the Implementation

Use the project's existing development command. When a managed background preview is useful, start it with:

```bash
python3 scripts/run-preview.py start \
  --command "npm run dev -- --host 127.0.0.1" \
  --url http://127.0.0.1:3000
```

Use `status` and `stop` on the same script. On a shared desktop, allow it to open the browser automatically. In remote/headless environments, provide only a host-exposed URL or attached screenshots; do not claim that agent-side loopback is user-accessible.

### 10. Production QA

After implementation, read `references/quality-gates.md`. For substantial work, encode critical flows, states, breakpoints, accessibility requirements, performance budgets, and visual baselines in the approved contract, then run:

```bash
python3 scripts/verify-ui.py http://127.0.0.1:3000 \
  --contract .codex/design-guide/design-contract.json \
  --project-root .
```

At minimum capture and inspect:

- Desktop: `1440x900`
- Tablet: `1024x768`
- Mobile: `390x844`

Use `scripts/capture-audit.py` when helpful:

```bash
python3 scripts/capture-audit.py http://localhost:3000 --out .codex/frontend-audit
```

Inspect screenshots and generated diffs before final. Check text overflow, overlapping UI, broken spacing, unreadable contrast, mobile navigation, blank canvases, critical state coverage, and whether the page still matches the approved contract.

If reviewing a built artifact, read `references/review-rubric.md`.

### 11. No-Ship Gates

Do not claim completion when any required gate fails:

- The app/page cannot be opened locally.
- No screenshot or visual inspection was performed for a substantial visual change.
- Mobile layout has obvious overflow, overlap, or unusable navigation.
- Text is clipped inside buttons, cards, tabs, or fixed-size controls.
- The result ignores the declared design read.
- A review artifact was generated but not opened, attached, or exposed through a usable absolute link or URL.
- Only a relative artifact path was provided for a confirmation gate.
- A required confirmation gate was skipped or is still pending.
- The implementation materially diverges from the approved design contract without resolving the change.
- Typecheck/build/lint fails and the failure is related to the change.
- A declared interaction, state, accessibility, visual regression, console-error, or performance gate fails.
- Strict production verification was weakened with `--allow-missing-tools`.
- The page looks like a generic AI SaaS template after logo/text substitution.

For substantial UI work, self-score before final:

```text
Direction fit: 0-10
Task flow: 0-10
Visual hierarchy: 0-10
Craft: 0-10
Usability: 0-10
Responsiveness: 0-10
Originality: 0-10
```

If any score is below 8, revise before delivery or clearly report why it cannot be fixed in this pass.

### 12. Final response

Report:

- What changed.
- Design depth, review artifacts, presentation method, and approval outcome when a confirmation gate applied.
- Where to open it.
- Screenshot/device checks performed.
- Interaction, accessibility, visual, performance, build, lint, typecheck, and test checks actually run.
- Remaining risks if anything could not be verified.

Keep the response concise.

## Quality Bar

The result should look like it belongs to this exact product and audience. If it could be pasted into any AI SaaS template with only the logo changed, revise before delivering.
