# P6 The time axis (4D orchestration layer): workflow, director, clock, cursor, navigator, "Flow · Data" dock

Everything in this document serves one idea: the prototype's fourth dimension is **time**. The pages are the three-dimensional part (screens in space); this layer turns them into a business timeline that plays by itself and can be paused, sped up, slowed down, jumped and replayed. How each part maps onto the time axis:

| Part | Its role on the time axis |
|---|---|
| Workflow definition (§1) | The script of the timeline: every step's business time (`when`), trigger, actor and data, sorted by business time; parallel branches are concurrent tracks |
| Director (§3) and page contract (§4) | The playhead: plays the DAG in business-time order, jumps to any moment, replays a step |
| Virtual clock (§5) | Playback time: pause freezes every motion, speed scales every motion |
| Demo cursor (§6) | Who is acting at this moment |
| Navigator (§7), dock and capsule (§8) | Where the playhead is: current step and sub-step, actor, business time, data in and out; the controls |
| Formats (§9) and lineage (§10) | What the data looks like at this moment, and how it changed since the previous one |
| Overview page (§11) | The whole timeline at a glance: DAG, swimlanes (who acts when), data flow |

This document is the **semantic spec** of each part of the orchestration layer — why each behavior is designed the way it is. A copyable implementation is in `assets/flow-kit/`. Complete UI implementations (navigator, DAG views, dock, format previews, lineage, swimlanes, overview page) are in the worked example `examples/tob-doc-audit/src/components/flow/` and `src/pages/FlowOverview.tsx` (see SKILL.md, "Worked examples", for locating the repository).

## Contents

1. Data model: actors, data objects, workflow (phases / steps / sub-steps / edges / layout)
2. Invariant tests
3. Director: state, scheduling, play modes, jumps, pause, leaving the page, watchdog
4. Page contract `useFlowStep`
5. Virtual clock
6. Demo cursor
7. Global floating navigator
8. The "Flow · Data" dock and the playback capsule
9. File and data format samples
10. Lineage
11. Whole-flow overview page
12. Requirement-status labels
13. Common pitfalls

---

## 1. Data model

### Actors `flow/actors.ts`

```ts
type ActorKind = '人工' | '机器' | '外部';   // human | machine | external (display labels)
interface ActorDef { key; label; short; icon; kind; desc; color /* CSS variable --color-act-* */ }
```

- Human roles map one-to-one to system permissions. In the toB example: checker, reviewer, regional admin, group admin; in the flow-kit example: applicant, department approver, finance, admin. Machine actors are chosen per project: backend service, scheduler, RPA, message queue, agent. External actors are the systems you integrate with; in the prototype they are all simulated.
- "Actor" and "execution mode" (rule code / human judgment / external call / LLM) are two separate dimensions. One backend job can contain both code rules and model calls.
- The `HUMAN` list decides when the cursor appears: it shows when a sub-step is performed by a human actor and hides when a machine performs it.

### Data objects `flow/dataObjects.ts`

```ts
interface DataObj { key; name; type /* type name in code */; carrier /* medium and location */; sensitivity: '高'|'中'|'低' /* high|medium|low */; sensNote; producer: ActorKey; desc; states?: string[]; fields: { name; type; desc }[] }
```

Fields must correspond one-to-one with the TypeScript types in `src`, so business and engineering agree on "what the data looks like".

### Workflow `flow/workflow.ts`

```ts
interface FlowStep {
  id; phase; title; short /* ≤ ~10 CJK chars, for swimlanes and nodes */;
  actor; with: ActorKey[];            // owner and collaborators
  role;                               // demo role to switch to
  route;                              // page route, may include ?tab=
  when; trigger: '人工触发'|'自动衔接'|'定时调度'|'外部提交';   // manual | auto-chained | scheduled | external submission
  narration;                          // what happens in business terms
  machine?; human?;                   // what the system / external system / agent does; where a human checks
  inputs: DataKey[]; outputs: DataKey[];
  subs: { title; actor; data: DataKey /* data this sub-step produces or uses */; anchor? /* data-flow-anchor */; ms? /* dwell for walk steps */ }[];
  drive: 'page' | 'walk';             // page: the page runs it and reports; walk: the director advances by ms, the page only prepares
  chain?: boolean;                    // continuation of the same backend job: enter immediately after the previous step
  necessity?: 'required' | 'optional'; basis?: string;
}
interface Edge { from; to; data?: DataKey /* no data = timing dependency, drawn dashed */; label }
DAG_POS: Record<StepId, { col; row }>  // row = business branch, col = dependency depth
```

- `when` is mandatory: the business time of the step as the story tells it ("10:30", "11:52", "next day 02:00", "T+1 09:00"). It is what the timeline shows on nodes, swimlane columns, the navigator and the capsule.
- The order of `STEPS` must be a topological order **sorted by business time**, with optional steps at the end — it is exactly the order of a run from the start, i.e. the timeline.
- Every edge says what it carries, e.g. "rule library v+1", "three Excel files", "case library", or which timing relation it is, e.g. "T+1 feed". This is the first thing the business side asks when looking at the DAG.
- Utilities: `depsOf / succOf / ancestorsOf / readySteps / orderReady / levelOf / stepById / stepsForRoute`.

### Shaping a rich DAG

A first DAG is usually a chain with one parallel pair. Discussions get better when the DAG shows the real structure; both examples were enriched this way (toB 10 → 14 steps, toC 11 → 17):

- **Rows are business lanes, not phases**: 3–4 rows such as "rules / UI upload / API upload / master data · governance" or "marketing / transaction · merchant / dispatch · courier / money · settlement". Give each row a 2–4 character label and a very short description.
- **Split steps that hide parallel work**: a step whose sub-steps alternate between two parties (merchant cooks while the courier rides to the store) becomes two parallel branches that join (`cook ∥ arrive → pickup`). Each branch keeps its own actor, and the join is where the business actually waits.
- **Look for the usual missing steps**: master data or capacity that several steps depend on (a root that fans out: org sync → rule maintenance + both upload paths); write-backs to the source system after a machine step (RPA writes results back and holds suspicious payment requests); closure steps that turn a finding into an outcome (rectification, payout) and feed the summary; reconciliation before settlement; and next-cycle adjustments that join an optional branch with the main one.
- **Feedback loops are terminal steps**: a DAG has no cycles, so "false positives feed the next rule version" is an optional terminal step whose narration says where the result goes, not an edge back.
- **Place nodes at their true dependency depth**: a step that only needs an early upstream but runs late (channel reconciliation needs only the payment flow, runs the next morning) sits early in its own lane, so its long edge runs along the lane instead of cutting across other nodes; its `when` shows the time.
- **Keep it readable at 1920 wide**: about 9 columns at most. Node width adapts to the column count, and when "actor label + time + state" does not fit, the actor chip falls back to its icon (the left border already carries the actor color). Put the merge zone after the main join.

## 2. Invariant tests (`flow.test.ts`, mandatory)

Because the workflow is structured data, its properties can be verified formally rather than reviewed by eye. Present them that way in discussions: "the DAG has no cycles, every hand-off matches, any step can start, removing the optional steps leaves a working main flow". These tests also keep the workflow definition consistent with pages and docs. Every time the flow changed in the original project, they caught something:

- Steps are ordered by phase, ids are unique; every step's route, actors and data objects exist.
- Each sub-step's `data` belongs to the step's inputs or outputs.
- Every `drive: 'page'` step has `useFlowStep('<id>'` somewhere in the source. Every anchor referenced by a sub-step exists in the source, as `data-flow-anchor="x"` or `anchor="x"`.
- `chain` is only used when the previous step is on the same page.
- Edges: reference valid steps, no duplicates, no self-loops; `STEPS` is a topological order; `data` carried along an edge is in the upstream step's outputs and the downstream step's inputs.
- Layout: a downstream step's column is greater than all of its upstream steps' columns; nodes don't overlap; nothing exceeds the column count.
- Scheduling: repeatedly taking "the first ready step" visits every step exactly once; starting from any step also finishes, with "executed + assumed done = total".
- Requirement status: every step with `necessity` has a `basis`; **no non-optional step depends on an optional step**, i.e. remove the optional steps and the main flow still holds.

## 3. Director `flow/director.ts`

### State (in memory only; a reload ends the demo)

```ts
{ active, mode: 'auto'|'step', idx, sub, status: 'idle'|'running'|'step-done'|'finished',
  nonce /* +1 on each step entry, invalidates stale callbacks */, paused, left /* user navigated away mid-step */,
  completed: StepId[], assumed: StepId[] /* assumed done */, trail: StepId[] /* actual entry order */ }
```

Plus persisted preferences `flowPrefs`: panel open state, speed, dock open state and height.

### Scheduling

- **Ready** = not done, and every upstream step is in `completed ∪ assumed`.
- Ordering (`orderReady`): ready steps in `STEPS` order (business time); **optional steps last**, so they never interrupt the main flow. A run from the start yields exactly the `STEPS` order. Do not prefer "downstream of the step that just finished": with one parallel pair it looks coherent, but once parallel branches have several steps each it plays a 12:05 step before an 11:53 one.
- **Autoplay**: after a step finishes, dwell about 1.6 s, then enter the first ready step. **Step mode**: list all ready steps (parallel branches) and let a person choose. `chain` steps auto-continue after about 0.5 s in both modes.
- When nothing is ready, the status becomes `finished`.

### Jumps and "assumed done"

- Clicking any DAG node in any view, or "start from this step", enters the target step directly. The target's unfinished ancestors are added to `assumed` — meaning existing or preset demo data is used and they were not actually executed — so the DAG dependencies still hold.
- **Do not** put redirects such as "clicking ⑦ first jumps back to ⑥" into the workflow definition. The original project once had a `needs` field for this; the user then required "every node must be switchable", so pages were changed to prepare their own upstream output instead (see §4).
- After `finished`, clicking a node replays that step on its own and returns to `finished` afterwards.
- Re-entering a step removes it from `completed / assumed` first; `trail` is appended only if it differs from its last element.
- "Previous step" = the second-to-last entry of `trail`, re-executed via the jump logic. "Next step" = mark the current step done and enter the first ready step.

### Pause

- Pause = clear the director's timers + **freeze the virtual clock**. Page scripts, pipelines, RPA replays and the cursor all stop together.
- Clicking a node or previous / next while paused enters the new step with `keepPaused`, staying paused. A walk step records `pendingWalk` and starts advancing only on resume.
- `togglePlay` (Space / big button): running → pause; paused → resume; waiting in step mode → next step.

### Leaving the page mid-demo

- If the user navigates to another page while a step is executing: set `paused + left` and **unfreeze the clock** so the user can use other pages normally. On resume, re-execute the step, because its page state is gone.
- If the step had already finished and the director is waiting for the next one: don't interrupt, just record `left`.
- A pause caused by `left` is not a user pause: clicking a node plays immediately.

### Watchdog

- If a page step reports no progress for 30 s of virtual time, it is treated as done so the demo never hangs. **The watchdog must not fire while paused**: clear it on pause, re-arm it on resume.

### Starting a demo

The start dialog offers three choices: play mode, speed, and whether to reset demo data first. The reset is loaded with a dynamic import so heavy modules stay out of the first-load bundle.

## 4. Page contract `useFlowStep(stepId, onEnter)`

```ts
const ctl = useFlowStep('check-run', (c) => {
  // called once on entering the step; may return a cleanup function
  let input = loadedRef.current ?? demoInput();   // ① supply your own upstream output
  c.click('[data-demo="check-run"]', () => { run.current = { nonce: c.nonce, id: start(input).id }; });
});
useEffect(() => {                                   // ② judge completion by progress — only for the task started by this entry
  if (!ctl || run.current.nonce !== ctl.nonce || state?.id !== run.current.id) return;
  ctl.sub(player.stage);
  if (player.done) ctl.done();
}, [ctl, state, player]);
```

`ctl` provides:

- `sub(i)`: report the current sub-step; also re-arms the watchdog.
- `done()`: declare the step complete.
- `later(ms, fn)`: runs on the virtual clock; cancelled automatically when the step changes or the page unmounts.
- `click(sel, fn)`: cursor moves → click ripple → action runs.
- `hover(sel, then)`.
- `nonce`.

Key points of the contract:

1. **Supply your own upstream**: if the page just opened and upstream output is missing, fill it with demo data. E.g. "no results yet: run the check, skip the animation, show the results"; "no file yet: load the demo file". Show a hint such as "upstream not replayed" where useful.
2. **Judge completion by nonce**: any step that decides completion by "the player has finished" must record the id of the task started by *this* entry. Otherwise, on re-entry, the previous finished result completes the step instantly.
3. Read the latest state in callbacks through a `ref` (`stateRef.current`), not a stale closure.
4. The hook defers `onEnter` with `setTimeout(0)`, so React StrictMode's mount → unmount → mount in development executes it only once.
5. Every cursor click is nonce-guarded: after the step changes, stale click callbacks do nothing.
6. No real downloads during a demo: check `flowActive()` and show a toast such as "not actually downloaded during the demo".
7. **Parallel steps over one linear simulation**: when the backend is simulated as one linear sequence of stages but the DAG runs branches in parallel, a step entered after its parallel sibling must not rewind the state the sibling already advanced. Give every script one helper, `prepareStep(id, pre, out)`: if the world has already reached the step's output stage `out`, some step that comes *later* in `STEPS` and is neither an ancestor nor a descendant is done, and none of this step's descendants is done, **replay** the sub-steps (highlight their anchors) without touching the state; otherwise prepare the world at `pre` (rewinding is right for a genuine re-run). The toC example's `src/state/liveFlow.ts` implements it for every step.

## 5. Virtual clock `flow/clock.ts`

- Principle: virtual time = Σ(real elapsed × speed), not accumulated while frozen; due callbacks are fired by a lightweight ~16 ms ticker that runs only while callbacks are pending.
- API: `vSetTimeout / vClearTimeout / setClockSpeed / freezeClock / useSpeed / useClockFrozen`.
- Changing speed mid-wait takes effect immediately: elapsed time counts at the old speed, the rest at the new speed.
- Steps `0.25 / 0.5 / 1 / 2` — the set the original user finally settled on. If saved preferences contain a removed step, fall back to the nearest available one.
- **All** demo time goes through it: the director, `ctl.later`, pipeline stages, RPA replays, typing effects. Scale CSS animation durations by speed too, e.g. `650 / speed` ms.
- The `VirtualClock` class takes an injectable time source, so it can be unit-tested: 1×, 2×, mid-wait speed change, freeze, clear.
- Continuous animations (a courier moving along a route, a progress bar) compute progress from `vNow()` inside a rAF loop: `p = (vNow() - startV) / durV`. `vNow()` must be **read-only** (`peekV`): it must not advance the clock or fire due callbacks, because it is called during render. Pausing then freezes the animation for free.

## 6. Demo cursor `flow/cursor.ts` + `DemoCursor.tsx`

- `cursorClick(target, actor, fn, guard)`: find the element (it may not have rendered yet; retry for about 2 s) → scroll it into view (the visible area is the main scroll region minus `--flow-dock-h`) → move for about 700 ms → ripple → run the action about 180 ms later; if the element is never found, run the action directly.
- Cursor color and label = "actor short name · demo user name". If the sub-step's actor is a machine, hide the cursor after the click, e.g. after clicking "run check" the backend batch takes over. In walk steps the cursor hovers over the anchor.
- Rendering: put it in the browser's top layer with `popover="manual"`, and re-raise it after dialogs open or close so it stays above `<dialog>`. Follow the target with rAF exponential smoothing, including while scrolling; stop while the clock is frozen; flip the label near the right or bottom edge; `pointer-events: none`.
- Clickable elements carry `data-demo="xxx"`, shared by the cursor and test scripts.

## 7. Global floating navigator `FlowNavigator`

- Bottom-left, collapsible. Expanded, it shows:
  - The current step and sub-step progress.
  - Actor and time of day.
  - Input / output data.
  - A DAG thumbnail (hidden while the dock is open, to avoid duplication).
  - The step list with states: running / done / assumed done / ready / waiting for upstream.
  - Branch choice in step mode.
  - Upstream and downstream of the selected step.
- When a sub-step has an `anchor`, the page scrolls to that region and highlights it.
- Useful outside demos too: clicking a step switches role and opens its page (browse mode).
- Every page header shows "this page in the whole flow" step tags, computed by `stepsForRoute`.

## 8. The "Flow · Data" dock `FlowDock` and the playback capsule

- **Position**: docked at the bottom of the main column as part of the layout, not an overlay. The original project compared "dock on the right"; that covered the execution log, the agent workbench and the buttons the cursor clicks, so the bottom won.
- Shown only during playback, with two panes:
  - Left: the detailed DAG. Nodes show number, short title, state and actor color; edges into and out of the current step are highlighted; a caption under the graph says what data flows in from upstream and out to downstream.
  - Right: the format sample of the current sub-step's `data`, following the demo automatically. The user can pick and pin another data object of this step; a "resume auto-follow" button switches back.
- **Size**:
  - Drag the top edge to resize (about 180 px up to 68% of the viewport); the height is remembered.
  - Double-click the top edge or press a button to maximize / restore.
  - Collapsed, the dock has height 0, i.e. `--flow-dock-h = 0`, and takes no layout space.
- **Playback controls live in exactly one place**: a centered floating capsule (`role="toolbar"`, an `aria-label` such as 演示播放控制, `w-max`). It contains:
  - The current step.
  - Four big buttons: previous, pause / resume, next, stop.
  - Speed, play mode, progress.
  - Maximize / collapse.

  With the dock open, the capsule floats just above the dock's top edge; collapsed, it floats at the bottom center of the main area. Nothing sits on either side of it, to minimize occlusion. During a demo, keep about 84 px of empty space at the bottom of the main area so content can scroll above the capsule. In step mode, the ready branches appear as a small capsule above the control capsule.
- **Hotkeys** (handled in the capture phase, so a focused button doesn't fire twice; never intercepted inside inputs):
  - Space: `togglePlay`.
  - `[` `]`: change speed.
- Drawers, dialogs and their backdrops, and toasts all stop above the dock: `bottom: var(--flow-dock-h)`.

## 9. File and data format samples `flow/formats.ts` + `FormatPreview`

- Every data object has at least one sample. **Show the original look by default** (the original user said explicitly: "show files in their original look, not as JSON"):

| kind | For | Rendering |
|---|---|---|
| `sheet` | Excel files | **Reuse the export module's sheet model**: summary row, header, red rows, frozen line, column widths; downloadable |
| `table` | Database tables | Table name, database, column name / type / description, sample rows, plus "proposed table name, to be confirmed by engineering" |
| `doc` | Policy documents, official notices | Centered title, issuing info, rule line, clause text, plus "illustrative summary" |
| `form` | Business forms, external-system pages, review panels | Laid out with the system's own fields, supports full-width long text |
| `trace` | Processing history, approval history, agent reasoning | The same timeline as on the page |
| `code` | Rule DSL | Code block |
| `json` | API payloads (request / response), in-memory structures | The primary look for payload objects; only a supplementary tab for everything else |
| `app` (consumer projects) | App screens, push notifications, order cards | A phone-frame card in the app's own style |

- Samples are generated from **real execution results**: run the engine once with the demo role and demo data; no hand-written static samples.
- Three entry points:
  - The "file and data formats" section of the overview page.
  - The "format sample" tab of the data object dialog.
  - A "file format" link next to upload, export and download buttons on business pages.
- Load the sample module on demand.

## 10. Lineage `flow/lineage.ts`

- Follow **one business object** (one record / one document / one payload) through every stage, e.g. uploaded row → normalized → configuration loaded → batch statistics → semantic key → verdict → result → export → retention. For each stage write the actor, type name, summary and fields.
- Mark how each field changed: `keep` / `map` (renamed, ← original header) / `derive` / `new` / `mask` / `drop`.
- For objects with a lifecycle, write the **state transition** at each stage, e.g. "submitted → in department approval", with the triggering action and actor.
- Also **computed from real execution results**. Besides one record, you can add the lineage of one entity, e.g. one counterparty's records of three kinds → cleaning → merging → distribution → findings → worksheet.
- Shown in two places: a "lineage" section in the single-record detail drawer, and per path on the overview page. Add unit tests asserting the stage sequence and key field changes.

## 11. Whole-flow overview page `#/flow`

Sections, with a sticky section nav:

- Workflow DAG (default view) / actor swimlanes (second view) + details of the selected step: narration, what automation does, the human checkpoint, upstream and downstream, why it is required or optional.
- Division of work between actors.
- Lineage.
- File and data formats.
- Data object catalog: clicking a row opens its format sample and field structure.
- Automation points and human checkpoints: what the system, external systems and agents each do, and where humans decide to accept, publish or send back. For agents, add confidence and reasoning traces. Describe any human–AI loop (case library, feedback) separately.

During a demo, clicking a node on the overview DAG or swimlanes also switches the demo.

## 12. Requirement-status labels

- `necessity: 'required'` (required by the spec) / `'optional'` (prototype addition · optional); unlabeled = a normal step within the spec's scope. `basis` states the reason, e.g. "section 2.4 requires screening all records in the data warehouse; the warehouse is T+1, so this can only run afterwards".
- Show it everywhere:
  - DAG: optional steps get a dashed frame + a tag placed above the node's top edge, never covering the title.
  - Dock DAG, navigator thumbnail, swimlanes, navigator step rows and details.
  - The current step on the capsule.
  - Overview step cards, stating "why required / why optional".
- The legend says "unlabeled steps are within the spec's scope".
- When the user asks "is this step necessary?", answer, then **put the answer into the prototype** as this label.

## 13. Common pitfalls (all actually hit)

| Symptom | Cause | Fix |
|---|---|---|
| First-load bundle balloons | The director statically imported the reset function and pulled in many modules | Use dynamic `import()` |
| A step is skipped after pausing | The watchdog kept counting during the pause | Clear on pause, re-arm on resume |
| Re-entering a step completes it instantly | It read the previous run's finished result | Record this entry's task id by nonce |
| A click happens after the step changed | Stale cursor callback | Guard with the nonce |
| onEnter runs twice | StrictMode double mount | Defer with `setTimeout(0)` |
| Cursor hidden behind a dialog | Cursor layer not in the top layer | Use a popover and re-raise when dialogs change |
| Cursor label clipped | Near the viewport edge | Flip by position |
| Capsule content wraps vertically | An absolutely positioned `left: 50%` box only gets half the width | Add `w-max` |
| Dock covers drawers or cursor targets | The dock is an overlay | Dock it in the layout + `--flow-dock-h` |
| Old data lingers in the browser after changing organizations / data | Stale localStorage | Bump the store `version` |
| Clicking a node first jumps to another step | A redirect in the workflow definition | Remove redirects; pages supply their own data |
| An optional step interrupts the main flow | Scheduling ignored requirement status | `orderReady` puts optional steps last |
| React warns "cannot update a component while rendering a different component" during an animation | Reading virtual time during render advanced the clock and fired due timers | Read time with a side-effect-free `vNow()` / `peekV()` |
| Step mode: choosing the second parallel branch first wipes the first branch's result | The entered step rewound the shared simulated world | Replay without rewinding when the parallel sibling already ran (§4, point 7) |
| Autoplay shows a 12:05 step before an 11:53 one after the DAG gained parallel branches | `orderReady` preferred the branch that just finished | Order ready steps by `STEPS` (business time), optional last |
| "Maximum update depth exceeded" as soon as a demo starts | A store selector returned a new object on every call (`useSyncExternalStore` sees a change each time) | Select primitives, or the stored object itself |
| A step's script stops when the UI switches screens or apps | The `useFlowStep` registration lived inside a component that unmounted | Register scripts in a component that stays mounted (shell / phone OS) |
