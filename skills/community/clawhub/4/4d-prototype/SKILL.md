---
name: 4d-prototype
description: Turn an IT project's requirement materials (PRD, specs, Word / PDF / Excel samples, sketches, screenshots, API docs) into a 4D prototype — a traditional clickable prototype plus a fourth dimension, time. The business becomes a timeline that plays by itself at business time (scheduled and overnight jobs, callbacks and parallel branches included), with pause, 0.25–2× speed, jump to any step and replay; anyone can take over at any moment, and every moment shows who is acting, which step of the workflow DAG is running and what the data looks like (original formats, state changes, lineage). Backends and external systems are deterministic mocks. Fits most IT projects — approvals, data processing, integrations, admin consoles, dashboards, RPA, consumer apps, AI agents. Use whenever the user wants a prototype, demo, clickable walkthrough or discussion mockup built from a requirement doc, even if they never say 4D. 中文触发词：基于需求文档做原型、带时间轴的原型、可播放的业务流程演示、情景演示、讨论样板、一键运行完整流程、全局流程导航、操作方泳道、数据结构变化、演示播放控制。
---

# 4D Prototype

A traditional prototype has three dimensions: screens laid out in space. You can look at them and click through them, but they hold still — nothing happens until someone clicks, the backend, schedulers and other parties never visibly act, and "what happens at 02:00 tomorrow" exists only in the presenter's narration. A **4D prototype adds the fourth dimension, time**: the whole business becomes a timeline that plays on its own from the first event to the last, and anyone can pause it, change its speed, jump to any moment, or take over and click.

The method was distilled from the complete development log of a real requirements prototype (17 milestones, 11 rounds of user feedback). Nothing in it depends on that domain; it applies to most IT projects. "Lessons" below are things that actually went wrong or were explicitly requested there. Two worked examples live in this skill's repository (see [Worked examples](#worked-examples)).

## The fourth dimension: time

### Traditional prototype vs 4D prototype

| | Traditional prototype (3D: screens in space) | 4D prototype (+ time) |
|---|---|---|
| Unit | A screen | A moment on the business timeline, e.g. "11:52, the customer pays" |
| What moves it | The presenter clicking | The timeline plays itself, start to finish, with one click; anyone can take over and click |
| Backend, schedulers, external systems | Invisible, or described in words | Act at their own business time as visible actors, e.g. "next day 01:00, the reconciliation job downloads the channel statement" |
| Parallel work | Cannot be shown | Branches run at the same time and visibly wait for each other where they join |
| Data | Static placeholder text | Real values from deterministic mocks, in their original format, changing from moment to moment |
| "What happens next?" | Narrated | Play on, or jump there |
| A question in the meeting | "Imagine that…" | Pause on that moment and point at it; replay the step |
| Is the flow itself right? | Checked by eye, if at all | The flow is structured data (steps, dependencies, data hand-offs, state machines, business times), so it is **formally verified** by tests on every change: no cycles, every hand-off matches both ends, any step can start and the rest still completes, required steps never depend on optional ones, illegal state transitions are rejected, money adds up |

### What the time axis is made of

- **Business time on every step**: time of day (or "next day 02:00", "T+1") and trigger (manual / auto-chained / scheduled / external submission). Together they are the timeline.
- **A workflow DAG sorted by business time**: its order is the order of the timeline; parallel branches are concurrent tracks that join where the business actually waits.
- **A director and a virtual clock**: the director plays the DAG; every delay and animation in the prototype runs on the virtual clock, so pausing freezes everything and the speed (0.25× / 0.5× / 1× / 2×) scales everything.
- **Playback controls**: one-click run, autoplay or step mode, pause, speed, previous / next, jump to or replay any step — also after the run has finished.

### What every moment shows

Stop the timeline anywhere and the prototype answers three questions about that moment. These are the readouts of the time axis:

| Readout | Question about this moment | How it shows up in the prototype |
|---|---|---|
| **Who** (actors) | Who is acting right now? | Actor catalog: human roles, backend services, schedulers, external systems, RPA bots, agents (pick per project). The demo cursor is labeled "role · name" and appears only when a human acts; demo role switching follows the timeline. Swimlanes show who acts when. Permissions and data scope |
| **What** (workflow) | Which step is running, what did it wait for, what comes next? | A DAG of phases → steps → sub-steps with the current node lit. Every dependency edge names the data or timing it carries. Every step is marked "required by the spec" or "prototype addition · optional", with the basis written down |
| **Data** | What does the data look like at this moment, and how did it change? | Data object catalog. Files, tables, API payloads and forms rendered in their original look, following the current sub-step. State transitions of business objects (e.g. a request going from "draft" to "ordered"). Field-by-field changes of one object across stages (lineage) |

## Deliverables

1. **A runnable prototype project.** Default stack: Vite + React + TypeScript + Tailwind, with `react` and `react-dom` as the only runtime dependencies if at all possible. Hash routing and relative build paths (`base: './'`) so `dist/` can be deployed as static files.
2. **Business module pages.** One page or tab group per requirement module. Make visible what the system does at each step and with what result: backend processing, external calls, state transitions, and agent reasoning (if the project has AI).
3. **Discussion pages** for working with the business side:
   - Scenario tour: domain primer + demo scripts.
   - Solution discussion: e.g. run mode, performance and cost, API design, deployment.
   - Assumptions and open questions, with a "reset demo data" button.
4. **Switchable appearance**: palette presets + the client's brand color, light / dark, and two UI styles (soft / sharp), switchable at any time from the top bar. Content shown in its original look (apps in phone frames, file and format samples, external-system pages) keeps its own colors. See [references/pages-and-ux.md](references/pages-and-ux.md) §2.1.
5. **The time axis (the 4D orchestration layer)**: business times in the workflow definition, demo director, virtual clock, playback controls, demo cursor, global flow navigator, the "Flow · Data" dock, and a whole-flow overview page.
6. **Docs**:
   - `README.md`
   - A prototype notes document under `docs/` (written in the UI language), generated from the same source as the assumptions page, with a test that keeps the two in sync.
   - `memory-bank/`, if the user's global instructions ask for one.
7. **Tests**:
   - Business-logic scenarios: every designed scenario produces exactly the expected result; normal data produces zero false findings.
   - Workflow DAG invariants.
   - Data lineage.
   - Export and payload layouts.
   - Docs sync.
   - Appearance: contrast across palettes × modes × styles, and no raw colors outside islands.

## Core principles

Each principle comes from a real failure or an explicit user request. Understand the reason so you can judge new situations.

- **Time is the core, so design it from day one.** The timeline is what separates this from a clickable mockup. Extract the business timeline in P0 (every event's business time, trigger and actor; what runs in parallel; what crosses days), write it as data in P2 (`when` and `trigger` on every step, steps sorted by business time), and put every delay on the virtual clock from the first animation. Why: in the original project the flow layer arrived at M8 and the clock was unified at M10, and both forced rewrites of pages, pipelines and replayers.
- **A prototype is a discussion tool, not a product.** Backends, external systems and scheduled jobs are designed, deterministic mocks: business logic really runs and data really flows, but nothing connects to a real system. If the project involves AI or agents, preset the results to what the model *should* do and show the full reasoning trace and confidence; do not call a real model unless the user explicitly asks. Why: the demo must be reproducible, testable and offline so the discussion stays on the business.
- **Fill gaps yourself, but register every one.** Where the spec is silent, fill in along the spec's general direction, and record each addition in the assumption register: id, content, handling, where it shows up, who must confirm. The prototype has a page for it too. Why: the user takes the prototype to the business and must be able to tell spec text from prototype inference.
- **Real materials never enter the repo.** Requirement materials and real samples go in `refer/`, which is added to `.gitignore` before the first commit. Samples are only used to infer structure and patterns; only aggregate numbers are committed. All people, companies and accounts in the prototype are fictitious. Real files may only be parsed and replayed locally in the browser.
- **Organise the flow so it can be verified.** Writing the timeline as data is not only for playback: it turns "is the process right?" into checks a machine can run. Keep invariant tests (`flow.test.ts`, see flow-orchestration.md §2) and scenario tests green on every change, and treat a failing invariant as a finding about the requirement, not a test to loosen. Why: in both examples the invariants caught real gaps — a step consuming data no upstream produced, a required step hanging off an optional one, a parallel branch rewinding another.
- **Single source of truth, guarded by tests.** Concretely:
  - The workflow definition drives the navigator, the DAG, the swimlanes, the dock, the overview page and the docs.
  - The export module's layout model is used both for format previews and for real downloads.
  - The assumption register generates both the page and the document.

  Why: the prototype gets changed over and over, and any hand-written second copy drifts.
- **Any step can start at any time.** Each step's page script must be able to supply its own demo input when upstream output is missing. Why: in discussions people click into random steps. The user explicitly required "every node must be switchable, including after the whole flow has finished".
- **Colors are tokens, and the appearance is switchable.** Components use token names only (`bg-surface`, `text-ink-900`, `bg-primary-500` …), never raw colors, so palette, light / dark and style can be switched at any time and the client's brand color can be dropped in. Original-look content (phones, file samples, external pages) is an island that keeps its own colors. Why: the user asked for switchable colors and UI style, and retrofitting it means touching every component — in the examples, several hundred hard-coded colors.
- **Demos have no real side effects.** No real downloads (show a toast instead), no real API calls, no real notifications. Mock pages of external systems keep that system's own look and carry a permanent "simulated environment" watermark.
- **Small milestones; tag before structural changes.** Every milestone ends runnable, verified and committed. Before a structural change — linear flow to DAG, merging or deleting modules, changing a data source — tag the current version, e.g. `v0.8-linear-flow`, `v0.15-pre-redesign`.

## The whole process

| Phase | Goal | Output | Details |
|---|---|---|---|
| P0 Intake | Understand the materials; list modules, roles, business objects and states, data, **the business timeline**, external systems, rules and gaps; classify the project type | Requirement inventory, first assumption register, specs, milestone plan | [references/intake.md](references/intake.md) |
| P1 Skeleton and design system (M0) | The project runs; shell, routing, state, design tokens and the appearance switcher in place | A bootable skeleton, first commit | [references/pages-and-ux.md](references/pages-and-ux.md) |
| P2 Domain core and mock backend (M1) | Domain model, business logic / rules / state machines, external-system mocks, mock scenarios, unit tests; also the **timeline as data**: actors, data objects, and the workflow with business times | Core logic with passing tests | [references/domain-and-mock.md](references/domain-and-mock.md) |
| P3 Module pages (M2…Mn) | One milestone per requirement module: processing made visible, results traceable | Business pages that work end to end | [references/pages-and-ux.md](references/pages-and-ux.md) |
| P4 Discussion pages | Scenario tour, solution discussion, assumptions and open questions, reset | Pages for discussion | [references/pages-and-ux.md](references/pages-and-ux.md) |
| P5 Acceptance and docs | Scripted check of every page, production build, business notes document, README | First deliverable version | [references/verification.md](references/verification.md) |
| P6 The time axis (4D orchestration layer) | Director, DAG scheduling, virtual clock, playback controls, cursor, navigator, "Flow · Data" dock, overview page, requirement-status labels, any-step switching | A complete prototype whose timeline plays with one click | [references/flow-orchestration.md](references/flow-orchestration.md), [assets/flow-kit/](assets/flow-kit/README.md) |
| P7 Iterate on feedback | Find the real need behind each round of feedback; update every affected view and keep them consistent | One milestone per round | [references/iteration-playbook.md](references/iteration-playbook.md) |

### P0 Intake (before writing code)

1. Inventory the materials:
   - Word: `scripts/docx_to_text.py` extracts body text, tables, embedded images and attachments.
   - PDF: `scripts/pdf_to_text.py`.
   - Excel samples: `scripts/xlsx_inspect.py`. `dump` shows the layout; `profile` shows statistics only, and sensitive columns are printed as shapes.
   - Sketches and screenshots: look at every one; they are often the acceptance criteria.
2. **Classify the project type** to decide where the prototype puts its weight. See the table in intake.md §3. Common types:
   - Approvals / tickets
   - Data processing / audit
   - System integration
   - Admin console / SaaS
   - Reports / dashboards
   - RPA / automation
   - Consumer app (multi-party, real-time)
   - AI / agents

   Most projects combine several.
3. List the requirement inventory in `memory-bank/specs.md` (or the project's equivalent):
   - Functional modules
   - Roles and permissions
   - Business objects and states
   - External systems and interfaces
   - Input and output files, data and payloads
   - Rules
   - **The business timeline**: each event's business time, trigger and actor; what runs in parallel; what crosses days (T+1, overnight, next cycle). See intake.md §4.
   - Non-functional requirements
   - Explicit constraints
4. Start the assumption register. Group everything that was inferred rather than stated, plus doubts and typos in the spec.
5. Ask only questions that change direction; take defaults for the rest and record them:
   - Desktop first, with a 1920×1080 viewport as the primary acceptance baseline (unless the user asks for mobile).
   - UI language = the language of the user and the requirement documents.
   - A light, professional style by default. The original user chose an Apple-like light style.
   - Ask before pushing, unless the user has said "don't ask again".
6. Present a milestone plan and start working without waiting for approval, unless the user asked to see the plan first.

### P1–P5 Build the "space" first, with the timeline already in the data

The pages are the three-dimensional part; the timeline gets wired in at P6, but it must already exist as data. The three things that matter most:

- **Write the timeline as data in P2.** Write `flow/actors.ts`, `flow/dataObjects.ts` and `flow/workflow.ts` (every step with its business time and trigger, sorted by business time) first; the director can come later. While building pages, mark clickable elements with `data-demo="…"` and highlight regions with `data-flow-anchor="…"`. Lesson: the flow layer was added only at M8, so every page had to be revisited; in this order, P6 is just wiring.
- **Use the virtual clock from the first animation.** Every demo delay goes through `vSetTimeout`: processing-stage animations, API call replays, RPA replays, typing effects. Lesson: this was unified only at M10, and the pipeline and replayers had to be rewritten.
- **Every module page shows "what the system is doing".** Specifically:
  - The processing stages, with the actor of each stage.
  - A timeline of state transitions or approval history.
  - API requests and responses.
  - A result summary that drills down to a single object: a document-style field view with problem fields in red, plus per-rule or per-check details.
  - Real file export.
  - An agent workbench showing the reasoning trace, if the project has agents.

### P6 The time axis: the 4D orchestration layer

This is the heart of the skill — the fourth dimension. The spec is [references/flow-orchestration.md](references/flow-orchestration.md). A reusable TypeScript reference implementation lives in [assets/flow-kit/](assets/flow-kit/README.md), with a "purchase request approval + ERP integration" example. It is verified: type check and 60 tests pass (flow invariants, clock, appearance), and a 2× one-click run completes 8/8 steps without errors. It contains:

- State store and router
- Virtual clock
- Cursor and sub-step spotlight
- Workflow definition and DAG utilities
- Director and the page hook `useFlowStep`
- Playback controls and hotkeys
- Workflow invariant tests
- A minimal integration example

Copy this implementation into a new project and adapt it to the domain; do not write it from scratch. For the UI components that flow-kit only specifies (navigator, DAG views, dock, format previews, lineage, swimlanes, overview page), adapt the implementations in the worked examples: start from the toB example for back-office and data-heavy projects, and from the toC example for consumer, multi-party and real-time projects.

Recommended order; each step can be accepted on its own:

1. Workflow definition (with business times) + director + pages wired with `useFlowStep` + global floating navigator + one-click run. Acceptance: the timeline plays from start to finish unattended, in business-time order.
2. DAG scheduling: schedule by dependencies; choose a branch in step mode; when jumping, mark ancestors as "assumed done".
3. Demo cursor and click animation; playback speed adjustable at any time.
4. File and data format samples: original look first, JSON only as a supplement. Add the data object catalog and lineage (including state transitions).
5. The "Flow · Data" dock: detailed DAG + the data format of the current sub-step. The dock sits at the bottom as part of the layout; it can be resized and collapsed.
6. Playback controls: a centered floating capsule with big buttons; Space pauses or resumes globally; clicking a node while paused switches to it and stays paused.
7. Requirement-status labels with their basis. A test guarantees that non-optional steps never depend on optional ones.
8. Any step can be switched to at any time, and replayed on its own after the flow has finished.

In the original project these 8 steps took 8 milestones because they emerged from feedback one by one. With flow-kit and the examples, a new project can do them in 2–3 milestones.

### P7 Iterate on feedback

Handle every round the same way: first work out the real need behind the literal request, then update **every** related view together — DAG, navigator, dock, swimlanes, overview, docs and assumption register. Afterwards, prove consistency with tests and the browser. Common feedback patterns and responses are in [references/iteration-playbook.md](references/iteration-playbook.md).

## The loop for every milestone

1. Implement. Touch only files related to this milestone.
2. `npm run typecheck`
3. `npm test`. Add tests for this milestone: scenarios, invariants, sync.
4. `npm run build`. Check the first-load bundle size; move heavy modules out of the first load with dynamic `import()`.
5. Make sure the dev server runs the latest code, then check at 1920×1080:
   - Interaction: the in-app browser.
   - Full-resolution screenshots, long autoplay runs, console error collection: drive headless Chrome with `scripts/cdp_run.mjs`.
   - Checklist: [references/verification.md](references/verification.md).
6. Update `memory-bank/` (if used):
   - overall-progress
   - specs: the user's words for this round and how you interpreted them.
   - todo, architecture, module-*, nav
   - Sync the docs and the assumption register.
7. Commit locally, only this task's changes; never commit `refer/`, `dist/` or `.env`. Push only with authorization; if the user said "keep pushing, don't ask", push directly. Never force-push.
8. Report:
   - What changed and where to see it.
   - Measured evidence, e.g. "at 2×, 10/10 steps finished in 72 s with no console errors".
   - New assumptions that need the user's confirmation.
   - Finally, answers to any side questions the user asked.

## Talking with the user

- Reply in the user's language; keep code, commands and identifiers as they are.
- Give a one-line plan or milestone list at the start. During the work, update only at milestones, on risks, or when a decision is needed.
- Answer business questions in business language, not implementation terms. For example: "this step is required by section 2.4 of the spec, because the data warehouse is T+1".
- For a vague request, consider several readings, state your interpretation, implement it, and explain the trade-off in the report. Example: "make the fonts bigger overall" can mean "not just font size, but readability, contrast, hierarchy and navigation".

## Worked examples

The examples live in the repository that contains this skill, at `../../examples/` relative to this skill's real directory. When the skill is a symlink into a checkout, resolve it first (`realpath ~/.claude/skills/4d-prototype`). Installs from npm, ClawHub or a packaged `.skill` file contain only the skill: read the examples in the public repository https://github.com/advnljs/4d-prototype-skill (clone it into the scratchpad if you need to run them), or follow the specs in `references/` instead.

| Example | Type | What to look at |
|---|---|---|
| `examples/tob-doc-audit` | toB: data processing + rules engine + simulated agent + RPA / API upload and write-back + per-organization configuration fed by a daily master-data sync + rectification loop + dashboard (14 steps, 4 lanes) | The complete 4D UI: `src/components/flow/` (FlowNavigator, FlowDag, FlowDock, FormatPreview, LineageView, Swimlane, PlaybackControls, DemoCursor), `src/flow/` (workflow, director, clock, formats, lineage), `src/pages/FlowOverview.tsx`; scenario tests in `src/rules/engine.test.ts`; the assumption register in `src/content/notes.ts` and its generated document |
| `examples/toc-food-delivery` | toC: three linked apps (customer / merchant / courier) + capacity forecast + order state machine + explainable dispatch scoring + payment-callback idempotency + channel reconciliation + T+1 settlement split + payout + partial refund with next-cycle offset (17 steps, 4 lanes, two parallel branches that join) | A deterministic simulated world as pure actions (`src/sim/world.ts`, with `advanceTo` for "supply your own upstream"); the linked-apps stage `src/pages/LivePage.tsx` + `src/components/live/` (phone frames, apps, stylized SVG map with riders moving on the virtual clock, dispatch board, state strip, timeline, event log); scenario tests in `src/sim/scenarios.test.ts`; `app` format samples; a solution page with live weight sliders (`src/pages/DesignPage.tsx`); a phone-sized second entry (`app.html`, `src/mobile/`) where one phone holds all four apps and switches between them during playback |

## Glossary (UI labels in Chinese prototypes)

Both examples have a Chinese UI. Use these labels to keep new prototypes consistent; the verification scripts also poll some of them.

| Term in this skill | Chinese UI label |
|---|---|
| step / phase / sub-step | 环节 / 阶段 / 子步骤 |
| actor | 操作方 |
| data object / lineage | 数据对象 / 数据流转 |
| time axis / business clock | 时间轴 / 业务时钟 |
| appearance / palette / light–dark / style / brand color | 外观 / 配色 / 明暗 / 风格 / 品牌色 |
| run the whole flow (one click) | 一键运行完整流程 |
| autoplay / step mode | 自动连播 / 逐步 |
| assumed done | 视为完成 |
| finished N/N | 已完成 N/N |
| playback control toolbar (`aria-label`) | 演示播放控制 |
| "Flow · Data" dock | 流程 · 数据 |
| required by the spec / prototype addition · optional | 需求必需 / 原型补充 · 可选 |
| assumptions and open questions | 假设与待确认 |
| simulated environment (watermark) | 模拟环境 |

## File map

| File | When to read |
|---|---|
| [references/intake.md](references/intake.md) | Starting a new prototype, receiving new materials, or after a big requirement change; classifying the project type |
| [references/domain-and-mock.md](references/domain-and-mock.md) | Designing the domain model, business logic or rules, state machines, external-system and API mocks, mock scenarios, configuration and versions, AI simulation |
| [references/pages-and-ux.md](references/pages-and-ux.md) | Building the shell, module pages or discussion pages; defining design tokens; fixing layout overlap |
| [references/flow-orchestration.md](references/flow-orchestration.md) | Implementing or changing any part of the time axis (the 4D orchestration layer) |
| [references/verification.md](references/verification.md) | Verifying every milestone; writing headless-browser scripts; debugging unreadable screenshots or stuck scripts |
| [references/iteration-playbook.md](references/iteration-playbook.md) | Receiving user feedback, doing a structural change, migrating data globally |
| [assets/flow-kit/](assets/flow-kit/README.md) | Copy it when implementing P6 |
| `scripts/docx_to_text.py`, `scripts/pdf_to_text.py`, `scripts/xlsx_inspect.py` | Reading materials in P0. Run with `python3 -I`; write output to the scratchpad |
| `scripts/cdp_run.mjs` | Full-resolution 1920×1080 screenshots, polling long flows, collecting console errors |
