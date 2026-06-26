# Core Rules

Universal rules that apply across all Figma Agent workflows. These are non-negotiable unless explicitly overridden for exploratory/prototype work.

---

## Always-On Rules

### 1. Validate After Write

Every meaningful `use_figma` write must be followed by validation — either `get_screenshot` or `get_metadata` on the affected nodes. Never assume a write succeeded; confirm visually or structurally.

### 2. Read -> Understand -> Fix -> Retry

When a `use_figma` call fails or produces unexpected results:
1. **Read** the error message or screenshot carefully.
2. **Understand** what went wrong — consult [plugin-api-gotchas.md](plugin-api-gotchas.md) for known failure patterns.
3. **Fix** the specific issue in the code.
4. **Retry** with the corrected code.

Never blindly retry the same code. Never rebuild from scratch as a first response to a targeted issue.

### 3. Explicit Over Implicit

State everything explicitly in `use_figma` calls:
- Which variables/tokens to use (by name)
- Which components to instantiate (by key/name)
- Layout mode (auto-layout direction, padding, gap)
- Color values as variable bindings, not raw hex

The model performs best when nothing is left to inference.

### 4. Design-System-First

Before creating any visual element, check what already exists:
- Search local variables and styles in the current file
- Check Code Connect mappings if available
- Search connected libraries via `search_design_system`
- Only create raw/hardcoded values as a last resort

### 5. Component Instance First

If a suitable existing design-system component already exists, use it as a **real instance** instead of visually recreating it with local frames.

**Required behavior:**
- Prefer existing component instances for tabs, buttons, radios, alerts, cards, icons, typography, and similar UI primitives
- Do not build local replacement frames for components that already exist in the file or connected design system
- Only build locally when no suitable component exists
- When unsure, inspect/search first, then build

This rule applies across build, edit, cleanup, and state-variant workflows whenever the design system already provides the needed UI.

### 6. Section-by-Section Execution

Large screens and complex layouts must be built incrementally, not in a single monolithic call. Break work into logical sections (header, content area, sidebar, footer) and build/validate each before moving on.

---

## ⚠️ Conditional Rules

These rules apply only when their trigger condition is met — not on every workflow.

---

### Section-Relative Positioning

**Trigger:** Building a new screen that is based on / extrapolated from an existing screen, where positioning values are derived from the source screen.

**Trigger examples:**
- Clone screen A and place it below A
- Create "Step 2" based on "Step 1" layout
- Duplicate a card layout to create a variant

**Non-trigger examples:**
- Building a new screen from scratch with no reference screen
- Inspecting/reading an existing screen without creating new nodes

**Rule:**
> Figma coordinates are always relative to the **direct parent container**. If the source screen is inside a Section or Frame, the new screen must use coordinates relative to that same Section — not absolute page coordinates.

**When triggered, before building:**
1. Identify the parent container of the source screen (Section/Frame)
2. Get the container's absolute page position
3. Calculate local offset: `localX = sourceX - containerX`, `localY = sourceY - containerY`
4. Apply the intended positioning (e.g., +100px below) as an offset from the container, not from page origin
5. **Explicitly state the parent container ID and local coordinates in the `use_figma` prompt**

**Check:** After creation — is the new screen actually inside/child-of the same section as the source, not on the page?

---

## Validation Gates

Validation is not a vibe check. Before reporting success, run the applicable checks in order.

### Check Order

1. **Structural checks first** — confirm the build is technically correct
2. **Visual confirmation second** — use screenshots to confirm the intended appearance
3. **Only then report success**

Do not rely on screenshots alone when structural checks are possible.

### Structural Checks

Use the lightest structural read that can prove the requirement:

- `get_metadata` — verify node hierarchy, parent container, layout settings, instance status, text content
- `get_variable_defs` — verify variable bindings where token usage matters
- local node inspection via `use_figma` — verify that duplicated/copied nodes remained real instances when relevant

### Common Validation Gates

Apply only the checks that match the workflow and task.

#### 1. Parent / Placement Gate
- Is the new node inside the intended Section or Frame?
- Does the parent container match the expected container?
- If this was a relative-placement task, are local coordinates being interpreted relative to the correct parent?

#### 2. Component Integrity Gate
- Are required UI primitives still real component instances instead of detached or local recreations?
- If this was a Copy + Edit task, did duplication preserve working component structure?
- Was `clone()` / duplication behavior used rather than reconstructing the shell manually?

#### 3. Content Completeness Gate
- Do text nodes contain real intended content rather than placeholder/default text?
- Were expected slot contents actually replaced?
- Are state-specific labels, CTA text, and body copy correct?

#### 4. Token / Variable Gate
- Are the required fills, borders, or effects bound to variables where expected?
- Were hardcoded values removed when tokenization or design-system alignment was required?

#### 5. State Accuracy Gate
- Does the requested UI state actually match the spec?
- Examples: active tab, expanded accordion, selected control, disabled button, current step

#### 6. Visual Confirmation Gate
- After structural checks pass, does `get_screenshot` confirm that the layout, spacing, alignment, and visual state match the intended result?
- Use screenshot review as confirmation, not as the sole source of truth.

### If a Gate Fails

Do not jump straight to rebuild.

- **Cheap failures** — content swaps, wrong labels, missed state toggles, local spacing issues -> apply targeted fix and re-run the relevant gates
- **Expensive failures** — fake component reconstruction, wrong parent container, structurally broken shell -> stop and decide whether a structural redo is cheaper than patching

See [screen-review-loop.md](playbooks/screen-review-loop.md) for the operational review/fix cycle.

---

## Batch-Write Heuristic

One logical section per `use_figma` call.

| Approach | Assessment | Why |
|----------|-----------|-----|
| Full screen in one call | **Too large** | Fragile, hard to debug, partial failures waste everything |
| Individual nodes one by one | **Too small** | High MCP overhead, slow, unnecessary round-trips |
| **1-3 semantically related components/groups** per call | **Sweet spot** | Debuggable, recoverable, efficient |

After each meaningful write: **always validate**, never proceed blind.

**Grouping examples:**
- A card component with its icon, title, and body = 1 call
- A navigation bar with logo, links, and actions = 1 call
- Header section + hero section = 2 calls (separate validation points)

---

## SVG Decision Matrix

| Situation | Action | Rationale |
|-----------|--------|-----------|
| SVG from external tool (logo, icon font) | **Preserve as-is** | Original fidelity matters more than editability |
| SVG as layout proxy (HTML-to-Figma output) | **Evaluate** - often replace with native nodes | Auto-layout compatibility, editability, variable binding |
| SVG in design-system context | **Flatten** or convert to component | Reusability, variable binding support |
| Animation/interaction needed | **Use native nodes** | SVG cannot participate in Figma prototyping |

When in doubt: native nodes are safer for production-quality work. SVG is acceptable for speed in exploratory contexts.

---

## Local-Context-First

Context preference order — always exhaust higher-priority sources before reaching outward:

1. **Current frame/selection** — nodes, styles, and variables already present
2. **Current file** — local variables, local styles, other pages/frames in the same file
3. **Code Connect mappings** — component-to-code mappings where configured
4. **Library search** — external/connected libraries via `search_design_system` (only when 1-3 are insufficient)

This reduces unnecessary API calls, avoids duplicate definitions, and stays consistent with the file's existing design decisions.

---

## Cost Awareness

MCP calls carry token and latency overhead. Minimize unnecessary calls:

- Batch semantically related operations (see Batch-Write Heuristic above)
- Use `get_metadata` for structural inspection before `get_design_context` on large trees
- Cache knowledge from earlier reads within the same session — don't re-fetch what you already know
- Avoid speculative `search_design_system` calls; search with specific intent

---

## Code Connect Awareness

When Code Connect mappings exist for a file:
- `get_design_context` will return mapped codebase components — use them directly
- Respect the mapping: instantiate the mapped component, don't recreate it from scratch
- When creating new components, consider whether a Code Connect mapping should be added
- See [figma-api.md](figma-api.md) for Code Connect tool details

---

## Native vs HTML-to-Figma Decision

See [workflow-selection.md](workflow-selection.md) for the full routing matrix. Quick rule:

- **Native Figma** (default): production-ready, design-system-aligned, variable-bound, fully editable
- **HTML-to-Figma**: rapid exploration, layout speed, complex CSS layouts that are tedious to replicate natively

HTML-to-Figma output requires cleanup for production use. It does not automatically use design-system variables or components. See [playbooks/html-to-figma-prototyping.md](playbooks/html-to-figma-prototyping.md) for the full workflow.
