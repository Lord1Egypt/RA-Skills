---
name: designing-tuis
description: Design, replicate, or iterate terminal user interfaces from screenshots, descriptions, layout sketches, or existing .tui files. Generate framework code (BubbleTea/Ink/Textual) directly or via .tui Schema intermediate representation.
---

# Designing TUIs

Use this skill to turn conversation, screenshots, or existing `.tui` files into practical terminal UI designs and runnable framework code. Two routes are available depending on the use case.

Trigger for welcome screens, dashboards, wizards, CLI launch screens, tool panels, lazygit/k9s/btop-style layouts, pane descriptions, or terminal UI visuals even when the user does not say “TUI”.

## Architecture: Dual-Route Design

```
Default route:  Screenshot/Description → 3-Phase Decomposition → Framework Code → Preview/Compare/Iterate
Advanced route: Screenshot/Description → 3-Phase Decomposition → .tui Schema → Schema→Code Converter → Framework Code
```

### Default Route (Screenshot → Code)

Preferred for most tasks. TUI's simplicity (no Z-axis overlap, ~20 component types, strict orthogonal grid layout) means the intermediate schema layer has low marginal benefit. Direct code generation is faster with no precision loss.

### Advanced Route (Screenshot → Schema → Code)

Use when:
- **Multi-framework output**: one `.tui` Schema generates BubbleTea (Go) + Ink (JS) + Textual (Python) simultaneously
- **Design asset persistence**: team needs versioned, editable TUI design files
- **Cross-role collaboration**: designers produce `.tui` files, developers consume code
- **Batch generation**: CI/CD generates multi-platform code from `.tui` source

## Operating Modes

Identify the mode before acting:

- **Screenshot replication**: apply the 3-phase decomposition protocol (see below) before generating code or schema.
- **Text-to-layout**: restate the intended structure, primary interaction, and target terminal size, then apply 3-phase protocol.
- **Existing `.tui` edit**: inspect the current tree and patch only the requested nodes.
- **Code export (default route)**: generate framework code directly after 3-phase decomposition and user approval.
- **Schema export (advanced route)**: generate `.tui` file, then convert to framework code using schema-to-code mapping.

## 3-Phase Decomposition Protocol

Both routes share Phases 1-2. Phase 3 diverges by route.

### Phase 1 — Grounding

**Goal:** Identify top-level structural regions and establish the global skeleton.

1. Scan screenshot boundaries — determine if a global border wraps the entire terminal
2. Identify top-level partitions:
   - Horizontal separators → top/bottom regions (header / main / footer / status-bar)
   - Vertical separators → left/right regions (sidebar / main-content / detail-panel)
3. Record for each region:
   - Border style (single / double / rounded / none / ASCII art)
   - Size proportion (as character row/col counts) — e.g., sidebar 30%, main 70%
   - Background color differences and separator line positions

**Output:** Top-level region list (typically 2-5 regions) with direction and proportion annotations.

### Phase 2 — Planning

**Goal:** Recursively analyze each top-level region, build a hierarchical layout tree, and lock proportions.

1. For each top-level region, determine internal layout direction (row / column / grid)
2. Quantify child element proportions (see Proportion Mechanism below) — use percentages, not absolute column counts
3. Determine if each child is a container or atomic component (refer to `references/layout-inference-rules.md`)
4. Record spacing: padding / gap
5. Annotate responsive constraints: min sizes for each proportional region, degradation strategy for narrow terminals

**Output:**
- Hierarchical layout tree (indented outline format)
- Responsive proportion annotations (e.g., "sidebar 30% min 20col / main fill min 40col")

### Phase 3 — Generation (Route Divergence)

**Default route (→ Code):**
- Generate target framework code (BubbleTea / Ink / Textual) directly
- Map proportions to framework-native layout mechanisms (flex ratio / percentage width)
- Must implement responsive behavior: listen to terminal resize, use proportions not hardcoded sizes, set min size fallbacks

**Advanced route (→ Schema → Code):**
- Generate `.tui` file with `{ version: "1", meta, tree }` structure
- Use percentages + min constraints for responsive intent
- Convert to framework code using `references/schema-to-code-mapping.md`

## Proportion Mechanism

### Extraction (Phase 2)

TUI proportions are precisely quantifiable via character counting (no sub-pixel ambiguity):

- Horizontal: count columns per region
- Vertical: count rows per region
- Express as: fixed (N rows/cols), percentage (30%), or fill (remaining space)

### Proportion Categories

| Type | When to Use | Example |
|------|-------------|---------|
| Fixed | Semantically fixed areas | status bar (1-2 rows), divider (1 col), title (1 row) |
| Percentage | Proportional areas | sidebar 30%, main 70% |
| Fill | Takes all remaining space | main content area |

### Responsive Layout Rules

- **Prefer percentages and fill** over hardcoded absolute column counts
- **Set minimum sizes** for proportional areas (prevent content crushing)
- **Narrow terminal degradation**: row layouts should degrade to column stacking when width < threshold

### Framework Mapping

| Type | BubbleTea (Go) | Ink (React) | Textual (Python) |
|------|----------------|-------------|------------------|
| Fixed N | `lipgloss.Width(N)` | `<Box width={N}>` | `min-width: N` |
| Percentage | Compute from `tea.WindowSizeMsg` | `<Box width="30%">` | `width: 30%` / `fr` units |
| Fill | `totalWidth - fixedChildren` | `<Box flexGrow={1}>` | `width: 1fr` |
| Min size | `max(calculated, minW)` | `<Box minWidth={20}>` | `min-width: 20` |

**BubbleTea note:** No native percentage/flex. Must store window dimensions in model, recalculate on `tea.WindowSizeMsg`.

## Rendering Stability Requirements

TUI rendering is character-by-character overwrite. Improper handling causes ghosts (old frame characters lingering). Generated code must follow:

- **Full-screen redraw**: each render outputs the complete frame (BubbleTea `View()` is naturally full-return; Ink React reconciler naturally full-diff; Textual compositor naturally full-compose)
- **Clear on resize**: clear screen before redraw after resize to prevent border remnants from mismatched sizes
- **Alternate screen buffer**: use alt screen (BubbleTea `tea.WithAltScreen()`, Ink default, Textual default) to avoid mixing with shell output
- **Hide cursor**: hide cursor during render to prevent mid-position blinking
- **Character width consistency**: avoid mixing half-width/full-width characters causing column misalignment; use `runewidth` (Go) / `string-width` (JS) / `wcwidth` (Python) for CJK text

## Comparison and Iteration Protocol

When a rendered preview or original screenshot is available, perform structured comparison:

### Comparison Dimensions (by fix priority)

| Priority | Dimension | Check | Fix Cost |
|----------|-----------|-------|----------|
| P0 | layout-error | Layout direction wrong, nesting level wrong | High |
| P0 | proportion-error | Component proportion deviates >10% from target, or layout breaks on resize | High |
| P0 | render-ghost | Render ghosts, lingering characters, screen flicker | High |
| P1 | component-mismatch | Component type misidentified (e.g., List should be Table) | Medium |
| P2 | content-missing | Text content omitted, list items missing | Low |
| P3 | style-drift | Color, border style, bold attribute deviation | Low |
| P4 | spacing-off | Padding/gap inconsistency | Low |

### Iteration Rules

- Fix P0 deviations first (layout + proportion) — they propagate downstream
- Each iteration round fixes only one category of deviation — avoid cross-edits causing regressions
- After fix, re-preview and re-compare until no P0-P1 deviations remain

### Proportion Fix Protocol

- Calculate actual rendered component proportions vs Phase 2 target proportions
- Deviation > 10% → fix: adjust width/height values or flex ratios
- Deviation ≤ 10% → acceptable (terminal character grid minimum unit constraint)

### Responsive Validation

- Validate layout at minimum two terminal sizes (e.g., 80×24 and 120×40)
- Confirm proportions hold after resize, no content overflow/truncation
- Confirm narrow terminal degradation strategy (e.g., sidebar collapse) works

### Render Stability Validation

- Rapid resize produces no ghosts (lingering characters/border fragments) or flicker
- Scroll, tab switch, tree expand/collapse — screen is complete after interaction, no remnants
- High-frequency updates (live logs, progress bars) produce no tearing

## Accuracy Expectations

TUI's character grid nature makes it easier to reproduce precisely than Web UI — no element overlap, no component crossing, layout is naturally an orthogonal tree.

| Complexity | Typical Examples | Expected Fidelity | Iterations |
|------------|-----------------|-------------------|------------|
| Simple | 2-3 panels, clear borders | High — usable on first generation | 0-1 |
| Medium | Multi-panel nesting, tab navigation, lists/tables | Medium-high — structure correct, proportions need tuning | 1-2 |
| Complex | lazygit/k9s/btop level | Medium — multiple iterations, layout and proportions first | 2-3 |

### Known Difficulties

- Dynamic/stateful content (blinking cursor, animations, live data)
- Low-resolution screenshots causing border character blur
- Highly customized Unicode box-drawing variants
- Responsive degradation at extreme terminal sizes (screenshot reflects only one size)
- Render ghosts: old frame characters lingering after resize/interaction (requires full-screen redraw + clear)

### Reproduction Priority Order

1. Layout structure (pane partitioning and nesting relationships)
2. Component proportions (width/height ratios of each region)
3. Component types (correct identification of List/Table/Tree etc.)
4. Text content (labels, titles, data items)
5. Colors and styles
6. Precise spacing

## Reference Loading

Load only what is needed:

- Read `references/components-cheatsheet.md` before creating or editing components. It is the field/default/visual-signature source of truth.
- Read `references/layout-inference-rules.md` during Phase 1-2 decomposition for layout direction, component identification, spacing, and proportion rules.
- Read `references/color-accessibility.md` when choosing colors, designing status indicators, or any time color conveys meaning. Ensures WCAG compliance and color-blind safety.
- Read `references/schema-to-code-mapping.md` when using the advanced route (Schema → Code conversion) or when generating multi-framework output.
- Read `references/known-quirks.md` before debugging rendering problems or using edge-case layout behavior.
- Read `references/workflow-examples.md` when the task resembles screenshot replication, multi-framework output, or iterative refinement.

This repository is documentation-only. Do not assume render or export tools ship with it.

## Workflow

### Default Route (→ Code)

1. **Align on intent**
   - For screenshots: apply Phase 1 (Grounding), describe the layout, and wait for confirmation
   - For text prompts: confirm the panes, emphasis, interaction model, and target framework
2. **Decompose (Phase 2 — Planning)**
   - Build hierarchical layout tree with proportions
   - Annotate responsive constraints
   - Confirm with user if ambiguous
3. **Generate code (Phase 3)**
   - Produce framework code (BubbleTea / Ink / Textual) with responsive layout
   - Include rendering stability measures (alt screen, full redraw, cursor hide)
4. **Preview and compare**
   - Render at target terminal size
   - Apply comparison protocol (P0 → P4 priority)
5. **Iterate surgically**
   - Fix one deviation category per round
   - Preserve unrelated structure
   - Re-preview after each fix

### Advanced Route (→ Schema → Code)

1. **Align on intent** (same as default)
2. **Decompose** (same as default)
3. **Draft the `.tui`**
   - Save to `designs/<name>.tui` unless user specifies another path
   - Use `{ version: "1", meta, tree }`
   - Prefer theme color names over hardcoded hex colors
   - Use percentage + min constraints for responsive intent
4. **Convert Schema → Code**
   - Follow `references/schema-to-code-mapping.md` for target framework
   - Generate one or more framework outputs
5. **Preview and compare** (same as default)
6. **Iterate** (same as default)

## Output Contract

When delivering a design update, include:

- The file path(s) created or changed (code file and/or `.tui` file)
- A brief layout summary with proportion annotations
- Route used (default or advanced) and target framework(s)
- Preview status, including any missing renderer/exporter blocker
- Responsive behavior summary (how the layout adapts to different sizes)
- Specific follow-up questions only when needed to continue

## Guardrails

Stop and re-check before any of these:

- Using `"fill"` on a non-main flex axis
- Guessing whether a field belongs in `props` or `layout`
- Using unavailable components: `Popover`, `Tooltip`, or `TextArea`
- Generating code or `.tui` directly from a screenshot without confirming intent
- Rewriting an entire existing design for a small requested edit
- Hardcoding absolute column/row counts instead of percentages (except for semantically fixed areas)
- Omitting `tea.WithAltScreen()` (BubbleTea) or equivalent alternate screen usage
- Generating BubbleTea code without `tea.WindowSizeMsg` handling for responsive layout
- Mixing half-width and full-width characters without width calculation library
- Using color as the sole indicator of state (success/error/warning/selected) without symbol or text label (WCAG 1.4.1)
- Using red-green color pairs as sole differentiator between states (color-blind unsafe)
- Using `dim` text on dark backgrounds without verifying contrast ≥ 4.5:1 (WCAG 1.4.3)
