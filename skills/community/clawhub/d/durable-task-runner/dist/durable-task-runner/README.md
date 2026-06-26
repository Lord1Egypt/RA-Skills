# durable-task-runner

Run long-running, multi-step work in OpenClaw without losing it to resets: durable state, progress updates, smart "continue this" recovery, and optional subagent orchestration.

This skill is for long work that should survive interruption instead of vanishing with chat context.

## What it does

- persists task state to disk instead of relying on chat memory
- tracks milestones, progress, events, and verification
- survives resets with smart resume/bootstrap helpers
- supports an explicit **"continue this"** recovery model after interruption
- supports pause / stop / steer controls
- supports thin controller/worker subagent orchestration
- renders compact status output for longer-running work

## Process model

The design goal is simple: keep long work alive across resets without pretending there is magic.

In practice, the runner:
- scales its structure to the size/risk of the task
- records checkpoints, milestones, and verification explicitly
- keeps enough state on disk to recover after interruption
- refuses to leave ordinary tasks in fake `running` states forever

This is meant to be practical, not ceremonial.

## Visibility and progress

Visible progress is a core feature, not cosmetic fluff.

Task and project progress bars, milestone updates, and timed status messages exist to answer the most important operational question during long work: did the task die, or is it still moving?

The bars are intended to be real operational metrics, but not fake precision:
- the **project** bar reflects aggregate milestone completion recorded in durable task state
- the **task** bar reflects the currently active work slice or milestone progress
- both depend on the plan being scoped sanely and updated as the task evolves

So the bars are meaningful, but they are still model-based. They are best treated as liveness/progress indicators grounded in explicit milestone state, not as earned-value accounting or mathematically exact completion truth.

By default, reporting stays low-noise and milestone-oriented. The intended operating model is event-driven progress plus smart recovery after resets; recurring timed updates are optional, not the center of the design.


## Runtime requirements

- Python 3.8+
- no external Python dependencies; the scripts are stdlib-only
- OpenClaw runtime/auth is required only for live message delivery paths

## Security / operational notes

This skill is intentionally stateful.

What it does locally:
- writes task snapshots, event logs, and progress logs under `state/tasks/`
- can emit live updates through OpenClaw when a task uses delivery method `openclaw`
- can coordinate subagent worker lanes through the `task_subagent_*` helpers
- supports explicit post-reset recovery via `scripts/task_continue.py`

What it does **not** do by itself:
- it does not ask for API keys directly
- it does not require external Python packages
- it does not need network access for local-only reporting modes like `stdout`, `noop`, or `log-only`

Practical caution:
- do not use plaintext task state for secrets unless you control and secure the underlying storage appropriately
- review subagent flows if you plan to use worker lanes in higher-trust environments
- recurring ticks are optional; the primary recovery model is explicit smart resume after reset/interruption

## Recovery-first operation

The primary model is **explicit smart recovery**, not host-specific scheduler plumbing.

After a reboot, reset, or interrupted long task, the intended user move is:

```bash
python3 scripts/task_continue.py
```

That command:
- finds the most relevant durable task
- runs bootstrap classification
- honors explicit user intent to continue the task now
- applies only low-risk resume follow-through
- tells you what it resumed and why

By default, raw bootstrap analysis now prefers an explicit prompt after reset/interruption:
- *"I found an interrupted durable task. Do you want me to continue it from the last safe step?"*

You can also target a specific task:

```bash
python3 scripts/task_continue.py --task-id <task-id>
```

Immediate breadcrumbs are emitted automatically on meaningful task transitions when a task has a delivery binding.
If a task is still marked `running` but has no executable continuation hook, the sweep now pauses/reclassifies it instead of emitting endless misleading idle-heartbeat noise.

Delivery bindings now support safer explicit modes:
- `openclaw` — live message delivery through OpenClaw
- `stdout` — print rendered messages only
- `noop` — render but do not deliver
- `log-only` — record send attempts in durable task history without external delivery

Context-pressure guardrails are available via `scripts/task_context_guard.py`:
- below 45%: no action
- at 45%+: write a prepare/checkpoint breadcrumb
- at 50%+: pause the task, queue immediate post-reset resume, and emit a machine-readable handoff payload so the surrounding runtime can reset and continue cleanly

Optional recurring timed updates still exist for environments that want them:

```bash
python3 scripts/task_tick_all.py
scripts/task_install_tick_cron.sh --print
scripts/task_install_tick_cron.sh --apply
```

But that is now an optional layer, not the center of the product promise.

## Product stance

The core promise is **reset-safe durable state + explicit smart recovery**.
This skill should be presented as a practical recovery-first workflow, not as an always-on unattended scheduler.
Recurring timed ticks are optional extras, not the primary value proposition.

## Provenance

This project was developed with iterative OpenClaw/LLM assistance and critically reviewed during hardening, including Claude review passes. Final code selection, testing, integration, and publication decisions were curated by John Watson.

This project is original glue code and workflow design, but it openly credits the ClawHub skills that influenced parts of the model. See `ATTRIBUTION.md`.
