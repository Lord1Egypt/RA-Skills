---
name: decomtangle
description: >
  Atomic tool-call decomposer for OpenClaw-style agents. Enforces an
  execution-time discipline for multi-step and stateful procedures: one
  observable action per tool call, observe the result between steps, N steps =
  N calls. Prevents the mega-tool-call anti-pattern — embedding a whole bash
  script, loop, or multi-step procedure in a single call's arguments — which
  breaks tool-call parsers (Ollama, LiteLLM/ollama_chat), returns opaque HTTP
  500s, and kills agent turns with no terminal event (the "silent stall").
  Especially valuable for local/open-weight models (gpt-oss, qwen) whose
  emissions are more parser-fragile, and for browser automation, API call
  sequences, and any workflow where each step's outcome should steer the next.
  This is in-loop tool-stepping discipline, not a goal/TODO planner.
version: 0.1.1
risk: none
tags: [decomposition, atomic, tool-calls, orchestration, reliability, react, browser-automation, local-models, openclaw]
license: MIT
maintainer: "Jason Vaughan (Jason-Vaughan)"
homepage: ""
---

# DecomTangle — atomic tool-call decomposer

> ⭐ **Find this skill useful?** If it saves you time, please **star it** — stars
> help other operators discover it and keep it maintained. Thank you!

## When this skill applies — and when it does not

Apply this discipline whenever you are about to execute a **multi-step or
stateful procedure through tool calls**: browser automation, a sequence of API
requests, a migration, anything where step N+1 depends on what step N actually
did.

This skill is **not**:

- a goal/TODO planner (it does not break objectives into tasks — it governs the
  *shape of each tool call* once you are already executing);
- a router or model-selection concern;
- active for single-shot questions, pure conversation, or a genuinely one-step
  action.

It declares no tools and requests no permissions. It only changes how you use
the tools you already have.

## The five rules

### Rule 1 — One tool call = one atomic action

Every tool call performs exactly one observable action: navigate, snapshot,
click, read a value, write one file, run one command. **Never embed a bash
script, a loop, a retry ladder, or a multi-step procedure inside a single
call's arguments.** A `command` argument containing `&&` chains over mutating
steps, `while`/`for` loops, `sleep`-and-poll sequences, or heredoc scripts is a
procedure wearing a tool call's clothes — decompose it.

### Rule 2 — Step → observe → step

After each call, **read the result before choosing the next action**
(ReAct-style). The result of step N is input to your decision at step N+1 —
if you scripted steps N through N+5 in one call, you made five decisions
blind. Pages load slowly, elements move, sends fail silently; only the
observed result tells you what actually happened.

### Rule 3 — N steps = N calls

If the procedure has seven steps, make seven tool calls. Do not feel that many
small calls are wasteful — they are the reliable path, and each one is
independently diagnosable when something breaks. Prefer **native, purpose-built
tool endpoints** (a dedicated navigate/click/read tool) over generic
shell-out-and-script automation for the same action.

### Rule 4 — Side effects are "attempted," not "confirmed"

A ✓/200/"Done" response to a side-effecting call means the action was
**attempted**. It is **confirmed** only when you observe the effect in the
live system — the message visible in the thread, the cell showing the new
state after a fresh load. Verify before you report success, and never
auto-retry a side-effecting action from an unconfirmed state. (This composes
with the airbnb-gateway skill's send/mutation doctrine.)

### Rule 5 — The complexity tripwire

If composing a single call's arguments requires **nested-quoted, multi-line
scripting** — quotes inside quotes inside JSON, escaped escapes, a heredoc —
that difficulty is a signal, not an obstacle to overcome. **Decompose
further** (e.g. write the payload to a file with a write tool, then send the
file; or split the script into its constituent actions). Cramming it in is how
parsers break and turns die.

## Why this exists (the failure it prevents)

On 2026-07-04 a production agent stalled silently, repeatedly, on a multi-step
browser procedure. Root cause: the model emitted a **whole procedure as one
giant tool call** — a full multi-step bash script as a single `command`
argument. The inference gateway's tool-call parser could not parse it, the
proxy layer crashed on the malformed result (`KeyError: 'message'` → HTTP 500),
and the turn died with **no terminal event**: no error message, no report,
nothing. The operator saw a bot that just went quiet.

This is a tool-call **shape** problem, not a model-capability ceiling. The same
model completed the same procedure when each step was its own atomic call. The
full anatomy of the incident — and the same procedure done right — is in
`examples/`.

## Working defaults

- Before starting a procedure, name the steps to yourself; if you cannot list
  them, you are not ready to execute — observe first.
- Poll with repeated *small* reads (one snapshot/read per call), not with a
  scripted sleep-loop inside one call.
- Pacing between polls is legitimate and atomic: a standalone wait as its own
  call (`sleep 8` alone, or a tool-provided wait) passes every checklist item —
  what's banned is *sleep-and-act* welded into one call. On rate-limited
  surfaces, coarsen the pacing, never the calls.
- On a failed call, fix and re-call **that one step** — the atomic shape means
  the failure is local, so the fix is too.
- Keep per-call output small: read the specific value you need rather than
  dumping whole pages into context (large results degrade every later
  decision in the loop).
- **Emit the fewest arguments possible.** Pass only required arguments plus
  the ones you actively need; omit optional arguments (background flags,
  default timeouts) entirely rather than filling them in. Every extra
  argument is another surface for a type slip (`"false"` as a string instead
  of the boolean `false`) — and strict tool-call parsers reject the whole
  call for one mistyped field. When you do pass a boolean or number, emit it
  as a bare JSON literal, never quoted.

## Package contents

- `references/decomposition-heuristics.md` — how to find the atomic boundaries:
  the observable-action test, the decision-point test, failure isolation, when
  a single call IS enough, and the anti-pattern catalog.
- `references/atomic-call-checklist.md` — a six-point pre-flight check to run
  (mentally) before every tool call in a procedure.
- `examples/good-multicalendar-atomic.md` — a real virtualized-calendar
  procedure executed as atomic calls: navigate → snapshot → select → poll →
  act → fresh-load verify.
- `examples/bad-mega-script-stall.md` — the verbatim anti-pattern that caused
  the 2026-07-04 silent stall, annotated failure-by-failure.
