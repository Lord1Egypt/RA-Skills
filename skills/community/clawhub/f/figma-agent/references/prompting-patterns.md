# Prompting Patterns

Operational prompt patterns for the Figma Agent. These are agent-facing. They define how the controller should compose a lean execution brief for write/build work, not how to talk to the user.

The goal is simple:
- keep always-needed guidance short and stable
- add extra instructions only when a real trigger condition applies
- define completion criteria before execution starts

---

## Execution Brief Template

This is the controller artifact that should be produced before write/build execution.

```text
GOAL: [one sentence]
CONSTRAINTS:
- [2-4 task-specific constraints only]
CONTEXT:
- [file key, node IDs, parent container, component names, variable names, or state facts that matter]
DONE WHEN:
- [explicit completion criteria tied to the selected validation gates]
```

A good execution brief is specific, short, and weighted. It should not dump every known rule into the prompt.

---

## Always-In Prompt Elements

These elements should be present in most write/build briefs unless the task is purely exploratory.

### 1. Explicit Design-System Usage

Never assume the model will use design-system tokens. State them explicitly.

**Pattern:** Name the exact variables, components, and styles to use.

```text
Use component 'Button/Primary' with fill bound to variable 'colors/primary/500'.
```

**Why:** Implicit references resolve inconsistently. Exact names reduce drift.

---

### 2. Existing Components Check

Before any build/edit write, explicitly decide whether the UI should be instantiated from existing components or built locally.

**Brief insert:**
```text
Use existing design-system components as real instances wherever available.
Do not visually recreate existing components with local frames.
Only build locally if no suitable component exists.
```

**Why:** Without this constraint, the model often recreates the look of existing components instead of using actual instances.

---

### 3. Variable-First Behavior

Resolve variables before creating visual elements.

**Pattern:** Load variables first, then create/bind nodes.

**Why:** Front-loading variable resolution prevents mid-block failures and makes the code self-documenting.

See [plugin-api-gotchas.md#paint-binding](plugin-api-gotchas.md#paint-binding).

---

### 4. Local-Context-First Prompting

Before reaching for external search, explicitly query the local file.

**Pattern:**
```text
Check local variables/styles/components first.
Only search the library if the current file does not already provide what is needed.
```

**Why:** Local context is the ground truth for the current file.

---

## Conditional Prompt Inserts

These inserts should only appear when their trigger condition is actually met.

### 5. Section-Relative Positioning

**Trigger:** New screen/node is based on an existing screen/node inside a Section or Frame, and placement is derived from that reference.

**Brief insert when triggered:**
```text
Positioning rule:
This new screen/node is based on an existing one inside a parent container.
Use coordinates relative to the same parent container, not absolute page coordinates.
State the parent container ID and local offsets explicitly before writing.
```

**Why:** This catches the repeated failure case of screens landing on the page instead of inside the section.

---

### 6. Copy + Edit

**Trigger:** The requested screen is mostly a state/step/variant of an existing screen.

**Brief insert when triggered:**
```text
This is a state/step variant of an existing screen.
Do not rebuild from scratch.
Duplicate the source screen, keep it in the same parent container, then edit only the delta.
Preserve working component instances, variables, and auto-layout unless a specific change is required.
```

**Why:** This keeps good structure intact and reduces regressions from unnecessary rebuilds.

---

### 7. HTML-to-Figma Framing

**Trigger:** The chosen workflow is HTML-to-Figma.

**Brief insert when triggered:**
```text
Treat this output as exploratory, not production-ready.
Expect cleanup afterward: variable binding, text resize, SVG review, and layout normalization.
```

**Why:** HTML-to-Figma is useful for speed, but it should not be mistaken for finished design-system output.

---

### 8. Error Recovery Framing

**Trigger:** A write failed or validation exposed a specific issue.

**Brief insert when triggered:**
```text
Read the exact failure first.
Fix only the identified issue.
Do not retry the same code blindly.
Do not rebuild from scratch unless the structure is fundamentally wrong.
```

**Why:** Recovery should be surgical, not chaotic.

---

## Completion Criteria Blocks

Completion criteria should be chosen from the task ticket and placed into the `DONE WHEN` section of the execution brief.

### 9. Build Completion Criteria

Use when creating a new screen/section.

```text
DONE WHEN:
- required nodes exist in the intended parent container
- required components remain real instances where expected
- required variables are bound where expected
- screenshot confirms the intended layout and visual state
```

---

### 10. Review / Fix Completion Criteria

Use when adjusting an existing design.

```text
DONE WHEN:
- the requested issue is actually fixed
- no placeholder/default content remains in the touched area
- no new regression was introduced
- screenshot confirms the corrected result
```

---

### 11. State Variant Completion Criteria

Use for Copy + Edit / next-step / alternate-state work.

```text
DONE WHEN:
- the duplicated screen remains inside the intended parent container
- only the required delta changed
- target state matches the spec exactly
- working component instances and layout structure remain intact
- screenshot confirms the correct final state
```

---

### 12. Tokenization Completion Criteria

Use when migrating hardcoded values to variables/tokens.

```text
DONE WHEN:
- required fills, borders, and effects are bound to variables
- hardcoded values targeted by the task are removed
- metadata/variable checks confirm the bindings
- screenshot confirms no visual regression
```

---

## Keep Briefs Lean

Do not stack all patterns into every execution brief.

Bad:
- one giant blended prompt containing routing logic, every conditional rule, every hard rule, and every review checklist

Good:
- one clear goal
- only the 2-4 constraints that matter for this task
- only the context facts needed for execution
- only the completion criteria needed for the applicable done gate

The controller should do the selection work. The executor should receive a compact brief.