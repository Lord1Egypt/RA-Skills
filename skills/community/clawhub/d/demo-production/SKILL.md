---
name: demo-production
description: Turn vague or incomplete product ideas into polished, runnable demos with minimal user prompting. Use when a coding agent is asked to create, plan, prototype, or build a demo, proof of concept, clickable prototype, MVP-style mockup, product concept, web app demo, tool demo, dashboard demo, workflow demo, or any project where the user has a rough idea but needs the coding agent to infer missing details, optionally research similar products or open-source references, design the development plan and project structure, build an interactive prototype, stop for review, then produce a usable demo and test edge cases after approval.
---

# Demo Production

Use this skill to turn an early, fuzzy project idea into a concrete, runnable, and reviewable demo. Optimize for reducing user prompting while preserving alignment with the user's intent.

Default behavior: autonomously continue until Stage 3, deliver an interactive demo, then stop for user review. Continue to Stage 4 only after the user confirms, unless the user explicitly requested end-to-end autonomous completion.

## Core Principles

- Treat vague prompts as normal input, not as a blocker.
- Infer generously, but state important assumptions briefly.
- Ask questions only when the answer would materially change the demo direction, technical feasibility, or core workflow.
- Preserve the user's likely mental model: identify the experience they want to see, not just the literal words they used.
- Build the smallest demo that convincingly demonstrates the core idea.
- Prefer a coherent prototype with mock data over an overbuilt partial product.
- Use existing project patterns, frameworks, and dependencies when working inside an existing codebase.
- For new frontend demos, create the actual usable experience as the first screen rather than a marketing landing page.
- Use mock data, simulated actions, and local state when backend implementation is not necessary for the demo.
- Mark clearly what is functional, simulated, mocked, or left for a production build.

## Pipeline Overview

Follow this 4-stage pipeline:

```text
Stage 1: Intent Intake & Reconstruction
  -> if core intent is unclear: ask or loop Stage 1
  -> if clear enough: optionally research references, then Stage 2

Stage 2: Planning & Structure Design
  -> if scope or structure is unclear: loop Stage 2 or return to Stage 1
  -> if prototype scope is clear: Stage 3

Stage 3: Interactive Demo Production
  -> always stop for user review by default
  -> if workflow or intent is wrong: return to Stage 1
  -> if structure or scope is wrong: return to Stage 2
  -> if UI or interaction needs changes: loop Stage 3
  -> if approved: Stage 4

Stage 4: Production Demo & Edge Case Validation
  -> if core flow fails: loop Stage 4
  -> if direction changes: return to Stage 3 or Stage 2
  -> if complete: final delivery
```

## Stage 1: Intent Intake & Reconstruction

Goal: convert the user's raw prompt into an actionable demo brief.

### Actions

1. Assess prompt completeness.
2. Identify missing information, risks, and safe assumptions.
3. Reconstruct the likely product intent.
4. Decide whether clarification is needed.
5. Decide whether external reference research is needed.
6. Produce a concise demo brief.

### Prompt Completeness

Classify the prompt:

- `low`: The user gives only a domain, product category, or rough desire.
- `medium`: The user gives a goal and some features, but key flows, users, data, or platform choices are missing.
- `high`: The user gives audience, core workflows, platform, design direction, and acceptance expectations.

Assess these dimensions:

- Target user and context
- Core job to be done
- Primary demo workflow
- Platform and device target
- Data source or mock data needs
- Visual style and tone
- Technical stack constraints
- Required integrations
- Success criteria
- Non-goals

### Clarification Decision

Use this rule:

- If missing information is low risk, make reasonable assumptions and continue.
- If missing information affects the central workflow, ask one concise question or offer a default path.
- If multiple directions are plausible but one creates a clearly stronger demo, choose it and label it as an assumption.
- If multiple directions are plausible and mutually exclusive, ask the user to choose among 2 to 3 options.

Do not expose long private reasoning. Summarize decisions, assumptions, and risks only.

Example summary:

```text
Prompt completeness: medium
Assumptions: single-user web demo, mock data, desktop-first layout with responsive behavior
Clarification needed: none
```

### Reference Research Gate

Perform focused web or GitHub research when it would materially improve the demo.

Research is recommended when:

- The user names or implies a known product, such as "like Notion", "Trello-style", "similar to Linear", or "Cursor for X".
- The idea belongs to a mature product category with established workflows, such as CRM, kanban, analytics dashboards, habit trackers, customer support tools, developer tools, or internal operations tools.
- The demo depends on current ecosystem choices, open-source libraries, UI components, APIs, or platform conventions.
- The user explicitly asks for competitor, open-source, or best-practice references.
- There is uncertainty about whether a named project, product, API, or library still exists or is currently relevant.

Skip research when:

- The demo is simple and references would not change the core workflow.
- Searching would add complexity without improving the demo.
- The user explicitly says not to browse or not to use external references.

Use references to extract:

- Common workflows
- Information architecture
- Interaction patterns
- Terminology
- Feature boundaries
- Open-source implementation ideas
- Expected UI states

Do not copy:

- Branding
- Proprietary UI
- Marketing copy
- Protected assets
- Product-specific text or data

Do not let references override the user's stated intent.

If research is performed, produce a short reference brief:

```text
Reference Brief:
- Similar references: Plane, Linear, Trello
- Useful patterns: issue list + board view, quick create, status filters
- Not adopting: team permissions, billing, advanced automation
```

### Stage 1 Exit Criteria

Proceed to Stage 2 only when:

- There is one primary target user or user role.
- There is one core workflow to demonstrate.
- There is a clear demo goal.
- Missing details can be handled as assumptions or are not central to the first demo.

Loop Stage 1 when:

- The target user cannot be inferred.
- The core workflow cannot be inferred.
- The demo goal is ambiguous in a way that would change the entire product direction.
- The domain is sensitive, regulated, destructive, or high risk and needs explicit user confirmation.

### Stage 1 Output

Output or maintain internally:

- Demo brief
- Prompt completeness
- Assumptions
- Reference brief, if research was performed
- Open question, if needed

## Stage 2: Planning & Structure Design

Goal: translate the demo brief into a buildable plan and project structure.

### Actions

1. Create a short plan of development.
2. Design project structure.
3. Define prototype scope.
4. Define mock, simulated, and real behavior boundaries.
5. Define the review criteria for Stage 3.

### Development Plan

Use 3 to 6 practical steps. Each step should produce something observable.

Recommended plan:

1. Define demo brief and assumptions.
2. Design data model and project structure.
3. Build the interactive prototype shell.
4. Stop for user review.
5. After approval, implement the production demo path.
6. Add polish, responsive behavior, and edge case validation.

Keep the plan practical. Avoid enterprise architecture unless the user's request requires it.

### Project Structure

When inside an existing project:

- Inspect the app structure before editing.
- Follow existing framework, styling, routing, naming, and testing patterns.
- Keep changes scoped to the requested demo.
- Reuse local components and utilities where appropriate.

When creating a new demo:

- Prefer a minimal, familiar stack that can run locally.
- Use clear folders such as `src/components`, `src/data`, `src/lib`, `src/pages`, or equivalent framework conventions.
- Keep mock data separate from presentation code.
- Avoid backend work unless the demo depends on it.

Optimize for:

- Fast demo iteration
- Easy review
- Clear separation of data, UI, and interaction logic
- Low setup friction

### Mock vs Real Boundary

Explicitly decide:

- What must be clickable in Stage 3.
- What can be simulated in Stage 3.
- What should become more functional in Stage 4.
- What is out of scope for this demo.

### Stage 2 Exit Criteria

Proceed to Stage 3 only when:

- The main screens or modules are named.
- The first interactive workflow is clear.
- The mock data shape is clear enough.
- The prototype can be built without another major product decision.

Loop Stage 2 when:

- The scope is too large for a demo.
- The proposed structure does not fit the repository.
- The prototype scope is not concrete enough.
- The mock vs real boundary is unclear.

Return to Stage 1 when:

- Planning reveals that the reconstructed intent was wrong or incomplete.

### Stage 2 Output

Output or maintain internally:

- Development plan
- Project structure
- Prototype scope
- Mock vs real boundary
- Stage 3 review criteria

## Stage 3: Interactive Demo Production

Goal: produce a clickable, visible, directionally accurate interactive demo for user review.

### Actions

1. Build the UI shell.
2. Add realistic mock data.
3. Implement the primary clickable path.
4. Include key states where relevant: empty, loading, success, error-like, selected, and no-selection.
5. Add enough visual polish to make the demo understandable and presentable.
6. Run basic verification.
7. Stop for user review.

### Prototype Requirements

The interactive demo should:

- Show the main user journey.
- Include clickable navigation or controls.
- Use realistic mock content.
- Include important states, not just the happy path.
- Visually communicate the intended product experience.
- Make incomplete functionality feel intentional through simulation or clear state changes.

Prototype techniques may include:

- Static mock data
- Local component state
- Simulated generated output
- Placeholder charts or tables
- Modal flows
- Toasts or inline status messages
- Disabled controls only when they clarify future scope

Avoid prototypes that are only screenshots or static layouts unless the user specifically asks for a visual mockup.

### Stage 3 Exit Criteria

Before presenting the demo for review, verify each item. Loop Stage 3 if any item fails.

Functional:

- [ ] At least one full user path is clickable from entry to completion.
- [ ] Navigation between primary screens works without dead ends.
- [ ] The run command or viewing path starts the demo without console-breaking errors.
- [ ] No placeholder routes return 404 or blank screens on the main path.

Content:

- [ ] Mock data is domain-specific. No `Lorem ipsum`, `Item 1`, `Item 2`, or `user@example.com` on visible surfaces.
- [ ] Generated or simulated output looks plausible for the target domain.
- [ ] Copy on primary buttons, headings, and empty states is written, not placeholder.

States:

- [ ] The main screen has an intentional initial, empty, or no-selection state.
- [ ] The main screen has a populated state.
- [ ] At least one loading, success feedback, or error-like state is visible somewhere in the flow.
- [ ] No-selection or initial state is intentional, not a blank canvas.

Review readiness:

- [ ] What is clickable is explicitly listed in the review message.
- [ ] What is simulated or mocked is explicitly listed in the review message.
- [ ] Assumptions that shaped the prototype are stated.
- [ ] Run or view instructions are included.
- [ ] A direct question asking whether to continue to Stage 4 is included.

If three or more items fail, return to Stage 2 instead of looping Stage 3; the scope or structure is likely wrong.

### Stage 3 Review Gate

Stop after Stage 3 by default. Do not proceed to Stage 4 until the user confirms.

At the review gate, include:

- What is clickable.
- What is mocked or simulated.
- What assumptions shaped the prototype.
- How to run or view the interactive demo.
- A concise request for feedback.

Use this review prompt:

```text
Interactive demo is ready for review.

Please check:
1. Is the core workflow right?
2. Is the visual direction close?
3. Are any screens, actions, or states missing?
4. Should I continue to the production demo stage?
```

Skip the pause only when the user explicitly asks for autonomous end-to-end completion, such as "build the full demo without stopping" or "make all decisions and finish it."

### Stage 3 Loop Rules

Return to Stage 1 when:

- The user says the product intent or target user is wrong.
- The main workflow does not match the user's mental model.

Return to Stage 2 when:

- The user changes the feature scope.
- The project structure or screen model is wrong.
- A new large feature needs to be included.

Loop Stage 3 when:

- The user requests UI, copy, layout, state, navigation, or interaction changes.
- The prototype is directionally right but needs local adjustments.

Proceed to Stage 4 when:

- The user confirms the workflow and direction.
- The user explicitly asks to continue.

### Stage 3 Output

Output:

- Interactive demo
- Review notes
- Known mocked or simulated areas
- Run or view instructions
- Question: continue to Stage 4?

## Stage 4: Production Demo & Edge Case Validation

Goal: turn the approved interactive demo into a presentable, runnable demo with core workflow completion and basic edge case coverage.

### Actions

1. Apply Stage 3 feedback.
2. Complete the core demo path.
3. Improve simulated or real functionality as needed.
4. Add UI polish and responsive behavior.
5. Validate edge cases.
6. Deliver final summary.

### Production Demo Requirements

The demo should:

- Start successfully with the project's normal command.
- Render without console-breaking errors.
- Let the user complete the core workflow.
- Handle common empty and invalid states.
- Use polished copy, spacing, and hierarchy appropriate to the domain.
- Avoid visible implementation notes inside the app unless they are part of the requested demo.

If a capability is simulated, keep the simulation believable:

- Generated content should look domain-specific.
- Data should be plausible.
- Actions should update visible state.
- Failures should show recoverable UI.

### Edge Case Validation

Before final delivery, test likely presentation failures:

- Empty data state
- Long text or overflow
- Invalid input
- Repeated clicks
- Loading or pending state
- Error or failed action state
- Small viewport behavior
- Missing optional fields
- No selected item
- Reset or return path after completing the main flow

For frontend demos, run the app and inspect it in a browser when possible. Capture screenshots or summarize observed issues if visual verification is performed.

For non-frontend demos, run the most relevant command, script, test, or sample workflow.

### Stage 4 Loop Rules

Loop Stage 4 when:

- The core workflow fails.
- Edge case testing reveals a demo-breaking issue.
- Polish issues make the demo hard to present.

Return to Stage 3 when:

- The user approves the direction but wants meaningful interaction changes.

Return to Stage 2 when:

- The user adds or removes a major feature.
- The demo scope changes.

Return to Stage 1 when:

- The user changes the target user, problem, or product intent.

### Stage 4 Exit Criteria

Before final delivery, verify each item. Loop Stage 4 if any required item fails.

Core workflow, all required:

- [ ] The main user journey can be completed from start to finish without intervention.
- [ ] The app starts with a single documented command or viewing path.
- [ ] No uncaught errors appear during the main flow.
- [ ] Reset or repeat path works; the user can run the flow more than once.

Edge cases, at least 6 of 8 verified:

- [ ] Empty data state renders cleanly.
- [ ] Long text or overflow does not break layout.
- [ ] Invalid input is handled with visible feedback.
- [ ] Repeated clicks on primary actions do not corrupt state.
- [ ] Loading or pending state is visible where async work happens.
- [ ] Failure path shows recoverable UI, not a crash.
- [ ] Small viewport, 375px width or equivalent, remains usable on the main screen.
- [ ] Missing optional fields render without `undefined`, `null`, or empty brackets.

Polish, all required:

- [ ] Spacing, alignment, and typographic hierarchy are consistent across primary screens.
- [ ] No visible implementation notes, TODOs, or debug output appear in the UI or primary demo surface.
- [ ] Simulated content is believable enough to present without extra explanation.

Delivery message, all required:

- [ ] What was built is summarized in under 8 lines.
- [ ] Key file locations are listed.
- [ ] Run or view instructions are included.
- [ ] What remains mocked or simulated is explicitly stated.
- [ ] Edge case results are reported, including which checks passed and which were not tested.

For non-frontend demos, substitute viewport and layout items with equivalents: CLI demos check terminal-width handling and `--help` output; API demos check error response shape and at least one failure scenario.

### Stage 4 Output

Final response should include:

- What was built
- Where the key files are
- How to run or view it
- What was verified
- Edge case results
- What remains mocked or simulated
- Suggested next iteration only when directly useful

Avoid long implementation essays. The user should quickly understand how to try the demo and what level of completeness to expect.
