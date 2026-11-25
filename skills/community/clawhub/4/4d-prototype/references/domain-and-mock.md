# P2 Domain core and mock backend

Whether a prototype survives business questioning depends on its domain core, not its pages. When business logic really runs, states really change and the numbers add up everywhere, the business side is willing to discuss details with it. The prototype has no real backend, but the "backend" is not fake: it is a deterministic implementation in the browser, layered separately from the pages.

## Contents

1. Layers
2. Four ways to simulate backend processing: business logic and state machines / external systems and APIs / scheduled and batch jobs / AI and agents (optional)
3. Configuration, multiple organizations and versions
4. Mock scenarios: every scenario is a business story
5. Local replay of real samples
6. History and retention: seeds must recompute deterministically
7. Material for solution discussions
8. File I/O and export layouts

## 1. Layers

```
src/domain/   Domain model: business objects and state enums, field mappings (raw header / payload field → standard field), code dictionaries, organizations and roles, permission matrix
src/logic/    Business logic: validation rules, calculations, state machines (allowed transitions and conditions), approval paths / dispatch rules (name it rules/, engine/, etc. per project)
src/mock/     Mock backend and external systems: mock services (payloads, latency, failures and retries), fictitious data generators and scenarios, history seeds, sample-replay aggregates
src/state/    Persistable demo state: business data, configuration and versions, retained results, session
src/agent/    (If the project has AI) the knowledge the model is expected to have, simulated verdicts and reasoning traces
src/lib/      Router, store, file I/O, export layouts
```

Pages only call functions exposed by `logic` / `state`; no business logic inside components. Unit tests then cover the logic directly, and format samples and lineage views can reuse the same execution results.

## 2. Four ways to simulate backend processing

Label every processing step with one of these. Pages use a fixed color per kind, separate from actor colors.

### 2.1 Business logic and state machines (almost every project)

- For each business object — request, ticket, order, batch — write down the **state enum** and the **allowed transitions**. The transition table states: from which state, triggered by which action, under which condition, to which state, performed by whom. The transition function is the only way to change state, and every transition appends a trace entry: time, actor, action, comment.
- Validation and calculations are plain TypeScript. Deterministic rules include required fields, formats, cross-field consistency, thresholds, deadlines, enum consistency and permissions.
- A rule record should contain:
  - `id`, name
  - Category: following the section structure of the policy or rule document
  - Basis: clause number, policy section
  - Level: error / question, or block / warn
  - Whether it is mandatory (cannot be disabled)
  - Scope
  - Tunable parameters
  - Pseudo-code / DSL for display
  - The implementing function
- **Batch-level rules** need statistics over the whole batch before they can judge a record, e.g. "within one batch, the same counterparty must map to a single country/region". The engine first builds an index over the batch and puts it in the context; per-record rules look it up. When a single record is checked on its own, these rules return "not applicable".

### 2.2 External systems and APIs

- Write one mock service per external system, with interface functions that return **realistically structured payloads** — request, response, error codes — and simulate latency with the virtual clock (`vSetTimeout`). Preset several outcomes: success, business failure, timeout then retry.
- Pages must show the payloads verbatim (request and response) and the call sequence. The "Flow · Data" dock shows them as `json` or `form` format samples.
- Page mocks of external systems (a third-party portal, an ERP screen, a payment gateway page) are rebuilt from screenshots, keep that system's own look, and carry a permanent "simulated environment" watermark. RPA scraping is shown as a replay: cursor animation, execution log, data captured live.
- The interface design itself is discussion material: URL, authentication, idempotency key, callback vs polling, compensation. Everything the prototype shows is a *proposal* and is registered as an open question.

### 2.3 Scheduled and batch jobs

- Overnight batches, reconciliation, sync and aggregation jobs become their own steps in the workflow with the trigger "scheduled". They are usually `walk` steps advanced by the director on a timer, while the page runs one simulated execution showing progress and output.
- When the user asks "is this step required?", label it "required by the spec" or "prototype addition · optional" with its basis (see flow-orchestration.md §12).

### 2.4 AI and agents (only if the project has them)

- Do not call a model. A "simulated judge" reproduces the verdict the model is expected to reach, using heuristic rules plus a keyword knowledge base. Return shape:
  ```ts
  { verdict: 'pass' | 'fail' | 'review' | 'na', confidence: number, trace: TraceStep[] }
  ```
  `trace` is the reasoning trace — step by step, what was read, which piece of knowledge it was compared with, what was concluded — shown as a timeline on the page.
- When the judge cannot decide, return `na` or `review`, never `pass`.
- A simulation of **maintaining configuration in natural language** must cover five expected behaviors, each with an example sentence that a button fills in:
  1. Split into several changes, each with a before/after diff and its effect on the demo data.
  2. Detect duplicates.
  3. Insufficient data — cannot be implemented.
  4. Ask back when information is incomplete.
  5. Block changes that violate policy.

  The UI lets the user confirm changes one by one or all at once, then publish; versions can be reviewed later.
- Agent intervention points and human checkpoints come in pairs: the agent "reads and judges", humans decide to accept, publish or send back. Human feedback can flow back into a case library, closing the human–AI loop.

### 2.5 One simulated world (consumer and multi-party flows)

When several parties act on one object in real time (customer, merchant, courier, platform), model the backend as **one world plus pure actions**:

- `World` holds everything the demo needs: configuration, the order with its state machine, payment messages, the dispatch decision, a precomputed plan (arrival, ready, pickup and delivery times, route legs), track points, settlement and refund results, plus a list of system events and push notifications with business timestamps.
- Each stage is one pure function `World → World` (`publishCoupon`, `submitOrder`, `payOrder`, `runDispatch`, `pickup`, `settle` …) built on the domain functions; `next(w)` runs the next stage and `advanceTo(w, stage)` runs up to a stage.
- Pages, the 4D director scripts, format samples, lineage and tests all call the same actions. "Supply your own upstream" becomes `advanceTo(initWorld(scenario), stageBefore)`; scenario tests become `runScenario(key)` plus assertions.
- Keep a business clock (minutes since midnight, next day ≥ 1440) separate from the virtual playback clock: the business clock is what the story says ("11:52 order, 12:20 delivered"), the virtual clock is how fast the demo plays.
- Order the stages the way `STEPS` is ordered (business time). Where the DAG has parallel branches over these linear stages, a step run early "supplies its own upstream" by advancing through the other branch's stages silently; the other branch then replays instead of rewinding (see `flow-orchestration.md` §4, point 7).

The toC example implements this in `src/sim/world.ts`.

## 3. Configuration, multiple organizations and versions

When the spec says "each organization / tenant maintains its own configuration":

- **Separate the implementation pool from configuration**: the pool contains every rule or feature implementation. Each organization's configuration only stores which ones are selected, on/off state, parameters and category overrides. Adding = selecting from the pool.
- **The user–organization table** (e.g. employee id → organization, role) decides two things: which configuration the current user uses, and which data they can see. The prototype simulates the signed-in user with a demo role switcher in the top bar; in production this usually comes from single sign-on or a portal cookie, which goes on the open-question list.
- **Versions**: every publish increments the version and records the change list. Each change has a type, before, after, the original wording or rationale, and whether it was confirmed. Only confirmed changes enter the new version; unconfirmed ones are kept on record too.
- **Data scope** is one function, e.g. `scopeOrgs(user)`, returning own organization, own region or all. List pages, detail pages and dashboards share it, and it has tests.

## 4. Mock scenarios: every scenario is a business story

- Generate a batch of fictitious data (a few hundred records is typical) and plant **scenarios** in it, covering normal, abnormal, edge and permission cases. Each scenario has:
  - A one-sentence business story the business side can understand.
  - The fields involved.
  - The expected result: which rules fire, which approval path, which state it ends in.
  - The expected explanation text.
- Make the fiction thorough:
  - Company names, people, accounts, phone numbers and organization codes are all fictitious; use obviously fake number ranges (e.g. `000-0000-xxxx`).
  - Coding schemes are self-consistent.
  - Dates avoid weekends where it matters.
  - Data matches the demo organizations.
- Two non-negotiable unit-test floors: every scenario's result matches expectations **exactly**; normal data produces **zero** false findings. Every later change must keep both.
- When a redesign changes the expectations across the board, first write a temporary probe test that prints every scenario's actual result, confirm each one is reasonable, then update the assertions.

## 5. Local replay of real samples (for calibration, never committed)

- Tests check whether `refer/<sample>` exists. If it does, run a smoke test and print statistics; otherwise skip.
- Use the replay to calibrate false positives of rules and simulated verdicts — in the original project this cut one semantic rule's false positives by more than half. Do not force-tune a rule whose definition is clearly off; register it as an open question instead (a deadline rule that fires on a fifth of all records is a sign the definition needs confirming, not tuning).
- Freeze the aggregate numbers in `src/mock/sampleReplay.ts` and reference them from rule-detail and solution-discussion pages.

## 6. History and retention: seeds must recompute deterministically

- Never hand-write history records or dashboard numbers. Use seed parameters (id, organization, date) to deterministically sample from the fictitious data and recompute with the **initial configuration**. List statistics then always match the details, and configuration changes made during a demo never alter history.

## 7. Material for solution discussions

Discussion pages answer the design questions the user cares about most, with data. Common ones:

- Run mode: per-record online vs offline batch. The original project used the "number of distinct combinations" in the samples to argue for a semantic cache plus batched calls.
- Performance and capacity: peak volume, time estimates.
- Cost: call volume, resources. Build an estimator with adjustable parameters and mark which values are assumptions.
- Interface design: sync vs async, push vs pull, compensation on failure.
- Deployment and integration: authentication, portal integration, data retention.

## 8. File I/O and export layouts

- Excel I/O: the examples use a zero-dependency implementation (zip + XML) to keep "react is the only runtime dependency". Ask the user before adding a library.
- On export, first build a layout model (rows, column widths, styles, frozen panes, red rows), then write it to a file. Format previews render **the same model**, so what you see is what you download. Payload and table samples work the same way and are generated from real execution results.
- Layout unit tests assert: the summary first row, the type column, only problem rows included, remaining columns are the original fields, sheet count and names.
