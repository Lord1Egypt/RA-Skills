# P1 / P3 / P4 Shell, module pages, discussion pages and visuals

Applies to all kinds of IT projects. Combine page patterns by project type (see intake.md §3).

## 1. Project skeleton (M0)

- Stack: Vite + React + TS (strict) + Tailwind. Check current versions with `npm view <pkg> version` before starting; don't casually add UI, chart or xlsx libraries.
- Hash routing (`#/path?tab=x`) and `base: './'`, so the build can be hosted as static files in a portal without server-side routing. Pages load with `React.lazy`; the toB example's first load is about 105 KB gzip.
- State uses `createStore(key, initial, { persist, version })` (see `assets/flow-kit/src/lib/store.ts`):
  - `useSyncExternalStore` + localStorage, with every read and write wrapped in try/catch.
  - Demo flow state uses `persist: false`.
  - When demo data changes incompatibly, bump `version`: a new storage key is used and the old one removed, so stale browser data never mixes with new data.
- Fix the port in `package.json` (e.g. `--port 5273 --strictPort`) and add it to `.claude/launch.json` for `preview_start`. Add a second port for the dist preview.
- The portal shell has:
  - Top bar: system name + **demo role switcher**, simulating the user signed in via single sign-on or the portal.
  - Left menu: filtered by role.
  - Page header: large title, breadcrumb, description, "this page in the whole flow" tags.
  - Main scroll region: `<main id="main">`; the demo cursor's scroll positioning depends on this id.
- Reserve mount points in the shell for four demo components, filled in P6:
  - Demo cursor
  - Floating navigator
  - "Flow · Data" dock
  - Hotkeys

## 2. Design tokens and visual rules

- Colors, type sizes, radii and shadows are tokens (Tailwind 4 `@theme`); components don't hard-code colors. Check that a color step actually exists before using it: the original project used a nonexistent `seal-400`, which rendered no color at all and the build didn't complain.
- Semantic colors are fixed across the site. Outcomes: pass / done green, problem / rejected red, needs human attention amber, actions in the primary blue. Execution modes: rule / system, external, agent. **Actor colors** are a separate set (`--color-act-*`) and never mixed with outcome colors.
- Readability floor (when the original user said "make the overall structure more comfortable to read", this is what they meant):
  - Minimum font size 12px.
  - Secondary text contrast at least about 4.5:1.
  - Looser line height for small text.
  - No negative letter-spacing for CJK body text.
  - Sticky section navigation on long pages.
  - Content moves aside when a floating panel expands instead of being covered.
- Motion only expresses state change (150–260 ms, strong ease-out) and respects `prefers-reduced-motion`; no emoji as icons.
- Default: a light, professional style. The original user explicitly chose an Apple-like light style:
  - Light gray canvas + white cards
  - Frosted-glass sidebar and top bar
  - #0071e3 accent
  - Large-radius borderless panels
  - Pill buttons, segmented controls
  - System fonts (SF Pro / PingFang)
  - Large titles
- **Consumer projects** can carry more brand: a warm primary color, rounded cards, product imagery drawn as SVG, micro-interactions. Motion must stay smooth — animate only `transform` and `opacity`, aim for 60 fps, and still respect `prefers-reduced-motion`.
- **External-system mocks keep that system's own look** (e.g. a legacy portal, a payment gateway page) and carry a permanent "simulated environment" watermark, to separate in-house systems from external ones and to avoid being mistaken for a real system.

### 2.1 Switchable appearance: palette × light / dark × style

Every prototype lets the viewer switch its overall look at any time, including in the middle of a run. The user asked for it: the same prototype is shown to clients with their own brand, on projectors and in dark rooms, and to people who prefer a denser, squarer UI. It is cheap only if colors were tokens from day one, so build it in P1 with the design tokens, not at the end.

What the viewer can switch (an "外观" (appearance) button in the top bar opens the panel):

| Axis | Options | How it works |
|---|---|---|
| Palette (配色) | The prototype's own palette (default) + a few presets (business blue, jade, violet, graphite) + **brand color** (品牌色): pick the client's color and the whole palette is generated from it | `lib/palette.ts` generates the primary scale and tinted neutrals in OKLCH, then corrects text and link steps against WCAG contrast. A too-light brand color is darkened just enough for white button text (≥ 3:1) |
| Light / dark (明暗) | Light, dark, follow the system | Dark inverts the neutral scale and regenerates primary, semantic and actor colors for readability |
| Style (风格) | Soft (rounded, soft shadows) / sharp (small radii, hairline borders instead of shadows) | Shadows are tokens; radii are clamped by one CSS rule on `html[data-style='sharp']` |

Implementation (flow-kit has the engine; the examples have the panel, `src/components/ui/ThemeSwitcher.tsx`):

- `lib/palette.ts` is pure and unit-tested: `buildVars(defaults, choice)` returns token overrides. Light + default palette returns nothing, so the hand-tuned original is untouched.
- `lib/theme.ts` reads the original `@theme` tokens from the stylesheet, writes overrides into one `<style>` on `:root`, sets `data-mode` / `data-style` / `data-palette` on `<html>`, and persists the choice per machine. Call `initTheme()` in `main.tsx` before rendering, so the first paint is already right.
- **Islands keep their original look.** Content shown "as it really is" — apps inside phone frames, map illustrations, file and format samples (Excel, tables, payloads, forms, documents), external-system pages — carries `class="theme-island"`; `theme.ts` restores the original tokens inside it. A dark prototype with light phone screens and light spreadsheets reads naturally; a dark spreadsheet would not be its original format any more.
- Rules for component code, all enforced by a source-scan test (`palette.test.ts`):
  - No raw colors outside islands: no `#hex`, no `bg-white` (use `bg-surface`), no white gradient stops (`to-surface`), no `black/` tints (use `ink-950/`; modal backdrops may stay black).
  - Mix with the surface, not with white: `color-mix(in srgb, <color> 11%, var(--color-surface))`.
  - **White text only on fills that stay mid-dark in both modes** (primary and semantic 500). On fills that invert in dark mode — dark ink steps used as "inverse" pills, actor colors — use `text-surface`.
  - SVG colors through `style={{ fill: 'var(--color-ink-500)' }}`, charts through token-derived scales (`color-mix` between surface, primary and ink), never fixed hex ramps.
  - A block that must stay fixed on purpose (a dark hero banner) is wrapped in `theme-fixed:start` / `theme-fixed:end` comments, with the reason.
- Contrast tests run over every preset × mode × style plus a few brand colors (including a light yellow): body text ≥ 7:1, secondary text ≥ 4.5:1 on both paper and surface, links ≥ 4.5:1, white on primary ≥ 3:1, semantic text ≥ 4.5:1. In the toB example this caught a secondary gray that passed on white but failed (4.3:1) on the gray canvas.

## 3. Visualization patterns for module pages

Combine these patterns for each module according to the project type (intake.md §3):

| Pattern | Purpose | Key points | Common in |
|---|---|---|---|
| Form and validation | Where input comes from | Field groups, required and format checks, a "fill example" button (the demo cursor clicks it) | Approvals, admin |
| Upload dialog | Where input comes from | Several built-in demo files (success / wrong category / non-standard format); a real file can also be picked and is parsed only locally; a "file format" link next to it | Data processing |
| List + detail | Finding objects | Filters, status pills, to-dos; the detail is a document-style field view with problem fields in red | All |
| State transitions / approval history | Where the object is now | Timeline: state, actor, time, comment; current node highlighted; reject or send-back branches visible | Approvals, tickets |
| Staged processing | What the system is doing | Parse → normalize → rules → statistics → summary, each stage labeled with actor and duration; can compare run modes (batch / per record) | Data processing |
| API call panel | How we talk to external systems | Verbatim request / response, call sequence, retries, receipt write-back | Integration |
| External-system mock + RPA replay | How data comes in from outside | Login → menu → list → detail rebuilt from screenshots; "simulated environment" watermark; replay with cursor animation, execution log and live captured data; default 1× (2× is too fast to read the detail page) | RPA, integration |
| Linked multi-app stage | Several parties acting on one object in real time | Side-by-side phone frames (e.g. customer / merchant / courier) around a shared state machine; a stylized SVG map with a moving marker; all apps refresh together on each transition; push banners slide into the receiving phone; an order timeline with actual minutes; a platform event stream. When operated by hand, machine steps run by themselves (e.g. dispatch fires shortly after the merchant accepts). See `examples/toc-food-delivery` | Consumer apps |
| Result summary and drill-down | What the result is, and why | Distribution by category or rule; single-object detail drawer: per-rule / per-check details, lineage, human confirmation | Data processing, risk |
| Agent workbench | What the model is thinking | Reasoning trace expanding step by step, verdict stream, confidence; human accept / reject flows back to the case library | AI / agents |
| Configuration maintenance | How rules / parameters change | Catalog (by category), detail (basis, parameters, pseudo-code, sample hits), change diff + per-item confirmation, version history | Admin, data processing |
| Export | What is produced | Confidentiality notice first, then a real file (not downloaded during demos); a "file format" preview next to it | Data processing, reports |
| Retention and data scope | Where results go, who can see them | Lists, details and review with a role-based data scope | Admin, data processing |
| Dashboard / reports | What management sees | Aggregation by hierarchy with drill-down; KPIs, trends, organization × category heatmap; metric definitions written out | Reports |

Before drawing charts, read the `dataviz` skill if it is available. Lessons from the original project:

- No legend for a single series.
- Thin bars, with values at the bar ends.
- Tooltips on hover.
- Text never uses series colors.

## 4. Discussion pages (P4)

The spec has no section for these, but they decide whether the prototype can be used for discussion:

- **Scenario tour (home page)**:
  - "Understand this business in five minutes": a few cards explaining the structure of the documents or objects, the coding scheme, the business path, and where the system steps in.
  - A business map.
  - Demo scripts: each has a "start" button that switches role and opens the right page.
  - The "run the whole flow" entry.
- **Solution discussion page**: pick the design questions the user cares about most — run mode, performance and capacity, cost, interface design, deployment and integration, AI run mode. Structure:
  - Evidence from the samples (aggregate numbers).
  - The recommended option.
  - An estimator with adjustable parameters, marking which values are assumptions.
  - Option comparison.
  - Recommended practice and control points for rollout.
  - Where useful, one simulated run, e.g. an overnight batch or reconciliation.
- **Assumptions and open questions page**: render the groups in `notes.ts` directly, plus a "reset demo data" button.
- **Whole-flow overview page** (built in P6). Sections:
  - DAG / swimlanes
  - Division of work between actors
  - Lineage (including state transitions)
  - File and data formats
  - Data object catalog
  - Automation points and human checkpoints
  - Human–AI loop (if any)

### Phone-sized entry (when the user asks for a mobile app)

Build it as a second entry of the same project (e.g. `app.html`), sharing the simulated world, the workflow and the step scripts, so both entries demo the same business. What worked in the toC example:

- **One phone, several apps.** A home screen with one icon per party; during playback the visible app follows the actor of the current sub-step (machine sub-steps follow the step's demo role), with an app-open transition and a short "switched to …" hint.
- **Register step scripts at the phone-OS level**, not inside app screens: app components unmount when the phone switches apps, and the scripts must survive that. The scripts find their targets through the same `data-demo` names on every entry.
- **Demo controls**: a capsule at the top (current step, sub-step, progress, play / pause) that opens a bottom sheet with the big controls, speed, mode, sub-steps, a mini DAG, data format samples and the event stream. Reserve a band for the capsule by raising the top safe-area variable while a demo runs, instead of covering headers. A touch dot replaces the mouse cursor.
- **Two presentations of one page**: full screen on a phone (safe areas from `env(safe-area-inset-*)`, a manifest so it can be added to the home screen); inside a device frame with side panels on a desktop, scaled to the window height.
- Verify at iPhone 16's 393×852 CSS viewport first (and the framed mode at 1920×1080 if it is used for presenting).

## 5. Layout and occlusion (recurring problems)

- An expanding floating panel covers the content. Either move the content aside (e.g. add left padding to `main`), or make the panel **part of the layout**, docked at the bottom of the main area, so the visible area shrinks accordingly.
- Drawers, dialogs, backdrops and toasts stop above the docked panel: the dock writes its own height into `--flow-dock-h` with a ResizeObserver, and these overlays use that variable for `bottom`.
- A centered absolutely positioned element (`left: 50%`) only gets half of the containing block's width and its content wraps vertically; add `w-max`.
- Drawers are narrow: a four-column document layout breaks every character onto its own line, so use two columns. Fix table column widths so short columns like "item / before" don't wrap. With `table-fixed`, keep the sum of the fixed column widths below the table's `min-width`, or the flexible column gets squeezed to nothing.
- Details of finished stages make columns long and push the next stage below the fold. Collapse finished stages or cap their height.
- Cursor labels and bubbles must flip near the viewport edge or they get clipped.

## 6. Performance and bundle size

- Load heavy modules such as demo-data reset, format samples and the rule catalog with dynamic `import()`, outside the first load. In the original project, the director statically importing `resetDemo` once grew the first load from about 80 KB to 131 KB gzip.
- Look at the first-load chunk size in every milestone's build output and record it in the progress log.
