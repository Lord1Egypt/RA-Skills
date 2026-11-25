# flow-kit: reference implementation of the time axis (4D orchestration layer)

A generic implementation of the layer that turns a prototype's pages into a business timeline that plays, pauses, changes speed and jumps, with a "purchase request approval + ERP integration" example business. Stack: React 18/19 + TypeScript strict + Tailwind, path alias `@/* → src/*`. Copy it into a new project and rewrite the example parts for your domain.

Comments are in English. UI copy and example data are in Chinese, matching the worked examples; replace them with your project's language.

## Files

| File | Generic / example | Purpose |
|---|---|---|
| `src/lib/store.ts` | Generic (change `PREFIX`) | Lightweight global state with optional localStorage persistence (`persist`) and data versioning (`version`) |
| `src/lib/router.ts` | Generic | Hash router: `useRoute / navigate / setQuery` |
| `src/flow/clock.ts` + `clock.test.ts` | Generic | Virtual clock: `vSetTimeout`, 0.25–2× speed, freeze on pause, read-only `vNow()` for rAF animations, injectable time source, unit-tested |
| `src/flow/cursor.ts` | Generic | Demo cursor logic: find element → scroll into view → move → click → run action |
| `src/flow/director.ts` | Generic | Demo director: DAG scheduling, autoplay / step mode, jumps and "assumed done", pause and keepPaused, leaving the page, watchdog; the `useFlowStep` page hook |
| `src/flow/workflow.ts` | Types and utilities generic; `PHASES/STEPS/EDGES/DAG_POS` are the example | Workflow definition (single source of truth) |
| `src/flow/actors.ts`, `src/flow/dataObjects.ts` | Structure generic, content is the example | Actor catalog, data object catalog (with lifecycle states) |
| `src/flow/flow.test.ts` | Generic | Workflow invariants: data objects, page wiring, anchors, topological order, edge data consistency, layout, scheduling, requirement status |
| `src/state/session.ts` | Structure generic, roles are the example | Demo roles (simulating the portal's signed-in user) |
| `src/state/reset.ts`, `src/state/requests.ts` | Example | Demo data reset; example business state where every delay uses the virtual clock, and `ensureRequestAt` shows "supply your own upstream" |
| `src/flow/spotlight.ts` | Generic | `useFlowSpotlight`: sub-step anchor scrolling and highlight, hide the cursor while machines act, cursor hover in walk steps, hide the cursor when the demo ends |
| `src/components/flow/DemoCursor.tsx` | Generic | Cursor rendering: popover top layer, rAF following, ripple, label flipping |
| `src/components/flow/PlaybackControls.tsx` | Generic (neutral styling) | Big buttons, speed, play mode, the centered `PlaybackCapsule`, hotkeys `usePlaybackHotkeys` |
| `src/pages/ExampleApp.tsx` | Example | Minimal integration: 5 page steps, 3 walk steps, a minimal step list (any step switchable) |
| `src/styles/flow-kit.css` | Generic | Cursor keyframes, `--flow-dock-h`, sub-step highlight `.flow-spotlight`, the "sharp" style's radius rule and `.theme-island` |
| `src/styles/tokens.css` | Starting point | Design tokens (`@theme`: ink, paper / surface, primary, semantic families, actor colors, shadows). Copy into the global CSS and adjust; components use only these names |
| `src/lib/palette.ts` + `palette.test.ts` | Generic | Appearance engine: OKLCH scales for palette presets and a brand color, dark mode, styles, WCAG contrast correction (`buildVars`). The test checks contrast over every preset × mode × style and scans the source for raw colors outside islands (set `ISLAND_FILES`) |
| `src/lib/theme.ts` | Generic (change the store prefix in `store.ts`) | Applies the appearance: reads the original tokens, writes overrides to `:root` and the originals to `.theme-island`, sets `data-mode` / `data-style` on `<html>`, persists per machine; `initTheme()` before the first render |

## UI you implement per project

These components are tightly coupled to each project's visual system, so flow-kit only specifies them (`references/flow-orchestration.md` §7–11). Complete implementations live in the worked examples in this skill's repository (see SKILL.md, "Worked examples"). The table points to the toB example; `examples/toc-food-delivery` has the same files restyled for a consumer brand, plus an `app` format kind and a linked multi-app stage (`src/components/live/`):

| Component | Spec | Implementation in the toB example |
|---|---|---|
| `FlowNavigator`: global floating navigator + start dialog (calls `useFlowSpotlight()`) | §7 | `src/components/flow/FlowNavigator.tsx` |
| `FlowDag`: DAG (row = branch, column = dependency depth; data on edges; requirement-status tags), plus the dock version `DagDetail` and the thumbnail `MiniDag` | §1, §12 | `src/components/flow/FlowDag.tsx` |
| `FlowDock`: the "Flow · Data" dock (docked layout, drag to resize, maximize / collapse, ResizeObserver writes `--flow-dock-h`), embedding `PlaybackCapsule` | §8 | `src/components/flow/FlowDock.tsx`, `PlaybackControls.tsx` |
| `FormatPreview` + `flow/formats.ts`: sheet / table / doc / form / trace / code / json samples | §9 | `src/components/flow/FormatPreview.tsx`, `src/flow/formats.ts` |
| `LineageView` + `flow/lineage.ts`: per-stage field changes and state transitions of one object | §10 | `src/components/flow/LineageView.tsx`, `src/flow/lineage.ts` |
| `Swimlane`: actor swimlanes | §11 | `src/components/flow/Swimlane.tsx` |
| `FlowOverview` page: all overview sections | §11 | `src/pages/FlowOverview.tsx` |
| `ThemeSwitcher`: the "外观" panel in the top bar (palette presets + brand color, light / dark / system, soft / sharp) | pages-and-ux.md §2.1 | `src/components/ui/ThemeSwitcher.tsx` |

## Integration steps

1. Copy the files under `src/` into the matching places in your project, merge `tokens.css` and `flow-kit.css` into the global styles, and call `initTheme()` in `main.tsx` before rendering. From here on, use token names only (see pages-and-ux.md §2.1).
2. Rewrite `session.ts` (roles), `actors.ts` (actors), `dataObjects.ts` (data objects) and `workflow.ts` (`PHASES / STEPS / EDGES / DAG_POS / DAG_ROWS / DAG_COLS / DEFAULT_TAB`).
3. In each page step's page, call `useFlowStep` the way `ExampleApp.tsx` does:
   - Supply your own upstream.
   - Track progress by nonce.
   - Put `data-demo` on clickable elements and `data-flow-anchor` on highlight regions.
4. In the shell, mount `<DemoCursor />`, the playback capsule, `usePlaybackHotkeys(active)` and `useFlowSpotlight()`, and make the main scroll region `<main id="main">`.
5. Put `flow.test.ts`, `clock.test.ts` and `palette.test.ts` in your test directory (list your island files in `palette.test.ts`) and run `npm test`.
6. At 1920×1080, run the whole flow with one click until "finished N/N", then go through the checklist in `references/verification.md`.

## Self-check

This directory can be type-checked and tested on its own:

1. In a temporary directory, create a `package.json` (dependencies: react, react-dom, typescript, vitest, @types/react) and a `tsconfig.json` (`paths: {"@/*": ["./src/*"]}`, `jsx: react-jsx`, `strict`).
2. Copy `src/` into it.
3. Run `tsc --noEmit` and `vitest run`. vitest needs `resolve.alias` for `@` in its config.
