# Workflow Selection

Routing matrix for selecting the right workflow path based on user intent and job characteristics.

---

## Primary Routing Matrix

| User Intent | Workflow Path | Key Decision |
|-------------|--------------|--------------|
| Build a production-ready screen | [Native Screen Generation](playbooks/native-screen-generation.md) | Design-system-first, section-by-section |
| Rapid UI exploration / prototype | [HTML-to-Figma Prototyping](playbooks/html-to-figma-prototyping.md) | Speed over polish, cleanup later |
| Fix/adjust an existing design | [Screen Review Loop](playbooks/screen-review-loop.md) | Screenshot -> isolate -> targeted fix |
| Tokenize/bind colors to variables | [Color Tokenization](playbooks/color-tokenization.md) | Audit -> map -> bind -> validate |
| Clean up Stitch/HTML import | [Stitch Import Cleanup](playbooks/stitch-import-cleanup.md) | Text sizing, decimal fixes |
| Discover variables/tokens | [Variable Discovery](playbooks/variable-discovery.md) | Local first, then library search |
| Clean up hardcoded values | [Design System Cleanup](playbooks/design-system-cleanup.md) | Incremental migration to variables |
| Inspect/review a design (read-only) | Read workflow: `get_design_context` / `get_screenshot` / `get_metadata` | No write tools needed |
| Map components to code | Code Connect workflow via `figma:figma-code-connect` skill | Load skill first |
| Create design system rules | Load `figma:figma-create-design-system-rules` skill | Load skill first |
| Build/update a design library | Load `figma:figma-generate-library` + `figma:figma-use` skills | Load skills first |

---

## Screen State Variants: Copy + Edit vs Rebuild

When creating a new screen that is mostly a different **state/step/variant** of an existing screen, default to **Copy + Edit** instead of rebuilding from scratch.

### Choose Copy + Edit When:

- The new screen keeps the same overall layout structure
- Most sections remain the same and only content/states change
- You are creating a next step, alternate state, or close variant of an existing screen
- Duplicating and editing is lower risk than rebuilding

### Choose Rebuild When:

- The information architecture changes substantially
- The layout structure is materially different
- The source screen is technically poor and should not be propagated
- The new screen is only loosely related to the original

### Copy + Edit Rule

If roughly 60 to 90 percent of the screen is the same, prefer:
1. duplicate/copy the reference screen
2. place it correctly relative to its parent container
3. edit only the delta
4. validate the changed result

This avoids unnecessary rebuilds and preserves working component structure, tokens, and layout decisions.

---

## Task Ticket Output

Workflow selection should produce a small internal task ticket before execution begins.

This ticket is not user-facing. It is the controller artifact that drives the execution brief and the done gate.

### Required fields

- `workflow` — selected workflow/playbook
- `execution_mode` — e.g. read-only, rebuild, copy-edit, targeted-fix, tokenization
- `risks[]` — only the risks that actually matter for this task
- `validation_checks[]` — only the gates that actually apply to this task

### Example

```text
workflow: Native Screen Generation
execution_mode: copy-edit
risks:
- section-relative positioning
- component integrity during duplication
validation_checks:
- parent / placement gate
- component integrity gate
- state accuracy gate
- visual confirmation gate
```

The point is simple: routing should decide not only how to execute, but also what must be proven before the work can be called done.

---

## Native vs HTML-to-Figma Decision

### Choose Native When:

- The output must be **production-ready** and design-system-aligned
- Design-system variables, components, and tokens should be used
- The result needs to be **fully editable** in Figma (auto-layout, variable bindings)
- The screen will be iterated on by designers
- Prototyping interactions will be added later

### Choose HTML-to-Figma When:

- **Speed** matters more than polish — rapid concept validation
- The layout involves **complex CSS** that would be tedious to replicate natively (grids, complex positioning)
- The source is an **existing web page** or HTML/CSS prototype
- The output is a **starting point** that will be cleaned up or rebuilt
- You need a **quick visual reference**, not a design-system-integrated artifact

### After HTML-to-Figma:

HTML-to-Figma output is never production-ready by default. Expect:
- Hardcoded colors instead of variable bindings
- Fixed text boxes instead of auto-resizing text (see [plugin-api-gotchas.md#text-autoresize](plugin-api-gotchas.md#text-autoresize))
- SVGs where native nodes would be better
- No design-system component usage
- Potential decimal/sub-pixel dimension values

---

## SVG Decision Logic

When encountering SVG in any workflow:

1. **Is it an imported asset (logo, icon)?** -> Preserve as-is
2. **Is it a layout element from HTML-to-Figma?** -> Evaluate; prefer native nodes for editability
3. **Does it need variable bindings or design-system integration?** -> Flatten or convert to component
4. **Will it need interaction/prototyping?** -> Must use native nodes

Full matrix in [core-rules.md](core-rules.md) — SVG Decision Matrix.

---

## Variable Resolution Strategy

Follow the Local-Context-First order in [core-rules.md](core-rules.md): local variables → local styles → Code Connect → library search. Only reach outward when local sources are insufficient.

---

## Code Connect Consultation

Check Code Connect mappings when:

- Building screens that use **design-system components** — the mapping tells you which code component corresponds to which Figma component
- The user asks to **implement** a design — Code Connect provides the bridge
- **Reviewing** whether a Figma file has code coverage

Do not check Code Connect when:
- Working on pure exploration/prototyping
- The file has no connected codebase
- Doing variable/token-only operations

---

## Batch Size Selection

The right batch size depends on the operation type:

| Operation | Recommended Batch | Why |
|-----------|------------------|-----|
| Building a new screen section | 1-3 related components per call | Debuggable, validates cleanly |
| Binding variables to existing nodes | 5-10 nodes per call (same variable type) | Repetitive operation, low risk per node |
| Fixing a specific node | 1 targeted fix per call | Precision matters |
| Creating a component set | Entire set in 1 call | Semantic unit, must be consistent |
| Stitch cleanup (text resize) | 5-10 text nodes per call | Repetitive, low risk |

General rule: see [core-rules.md](core-rules.md) — Batch-Write Heuristic.

---

## Read-Only Inspection

Not everything requires writes. For pure inspection:

| Need | Tool | Notes |
|------|------|-------|
| Visual check | `get_screenshot` | Quick layout verification |
| Layer structure | `get_metadata` | Sparse XML, good for large files |
| Code + context | `get_design_context` | Full code output, heavier |
| Variables/tokens | `get_variable_defs` | Scoped to selection |
| Library search | `search_design_system` | Cross-library |
| Auth check | `whoami` | Token validity |

Always start with `get_metadata` for large files to understand structure before requesting heavier tools.
