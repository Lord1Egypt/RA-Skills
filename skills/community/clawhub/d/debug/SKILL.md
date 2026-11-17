---
name: debug
description: "Execution breakdown of a request: read it via recent_tasks(limit=3, include_results=true, include_traces=true), skip the task still running, report header «N раундов · X USD · K вызовов · E ошибок», the trace, then bullets: что отработало, сложности, результат, как пофиксить. Amounts only as «6.31 USD» — never the $ sign: the chat renders text between two $ as a formula."
version: 1.0.3
type: instruction
when_to_use: "The user asks «в режиме дебага», «отдебажь», «разбери прогон», «разбери полёт», «покажи, что произошло в запросе», «трейс последнего запроса». Not for a plain request with no debug/breakdown word. Rules even without opening SKILL.md: no $ anywhere, including tables; do not copy the format of earlier breakdowns in this chat; the cause of each error is quoted from that call's output; compare only with tasks fetched now; give each count once."
license: MIT-0
tags:
- debug
- trace
- observability
---

# Debug-trace: execution breakdown of a finished request

> **Formatting rule #1 — no `$` before numbers anywhere in the report.** The chat renders
> text between two `$` as a math formula: «$6.44 vs $3.93» came out as italic gibberish in a
> live breakdown. Write amounts as «6.44 USD». Header template:
> `**26 раундов · 6.44 USD · 25 вызовов · 6 ошибок**`.

Run the request the user asked for by your normal means — the same tools you would use
without this skill — and only then produce the breakdown. This skill owns the *reporting*
half, not the execution half: do the work first, wrap it second.

## Workflow (mandatory order)

1. **Perform the request** as you normally would, using the agent's tool catalog. Do not
   change the execution path because this skill is active — the point is to trace what the
   real run did, not a special one.
2. **Read the just-finished task.** Call `recent_tasks` with `limit=3`,
   `include_results=True`, `include_traces=True`. The list is newest first, and the
   runtime records a task the moment it starts: the first entry is usually the task you
   are in right now — status `running`, no `trace_summary` yet. Skip it and take the most
   recent terminal task. Do not guess or construct a `task_id`; take it from the list.
3. **Make sure it is the right task.**
   - The user asked to break down an earlier run («разбери прогон», «трейс последнего
     запроса»): the most recent terminal task after the current one is that run.
   - The user asked to do something «в режиме дебага» in this same message: that work
     happens inside the current task, and its trace exists only after the task finishes.
     If you ran the work as a subtask (`schedule_subagent`), report that subtask — it is
     terminal and has its own trace. Otherwise say plainly that the trace of this request
     becomes available once the answer is sent, and suggest sending «разбери прогон» as
     the next message. Never present an older task's trace as this request's.
   - **If no suitable task is in the returned list** (nothing finished, or no task was
     recorded), say so plainly: the trace could not be captured for this request. Do not
     fabricate a trace from memory of what you did.
4. **Build the report** from the returned fields (see "What the report holds") and post it
   as the chat answer, after the normal answer to the request itself.
5. **Before sending, check the draft:** no «$» anywhere (rewrite «$6.31» as «6.31 USD»,
   «≤$4» as «≤4 USD»); the header is `**N раундов · X USD · K вызовов · E ошибок**`; every
   count appears once. Earlier breakdowns in this chat may use «$» — do not copy them.

The report is a follow-up to the real answer, not a replacement for it. The user gets the
answer to their request first, then the breakdown.

## What the report holds

The report has two parts, in this order.

### Trace (metadata + call sequence)

From the `recent_tasks` entry, render:

- **task_id** — so the run is identifiable.
- **status** — the terminal status (`completed`, `failed`, `interrupted`, `cancelled`,
  `budget_exceeded`, …). This is the headline: did it succeed.
- **total_rounds** — how many model rounds the run took.
- **result** — the outcome text (truncated if long; mark truncation).
- **trace_summary** — the compact tool-call trace: how many calls, how many errored, the
  ordered list of tool calls with their arguments (abbreviated), statuses, exit codes, and
  any agent reasoning notes. This is the evidence; quote it, do not paraphrase it loosely.

### Breakdown (bullet analysis)

A short bullet list, grounded in the trace above, not in general knowledge:

- **Что отработало** — the tool calls that succeeded and produced the answer.
- **Сложности** — where the run struggled: errored tool calls, retries, a `failed` or
  `budget_exceeded` status, rounds that went nowhere. Name the specific tool call from the
  trace_summary, not a vague "had problems".
- **Результат** — one line: what the user got, in business terms.
- **Как пофиксить** — concrete, actionable next steps for the recurring problem the
  breakdown surfaced (fix an argument, widen a filter, add a missing capability, reword the
  request). If the run was clean, say so and skip this bullet.

Keep the breakdown short — bullets, not paragraphs. The trace already carries the detail;
the breakdown is the verdict on it.

### Accuracy rules (each was broken in a live breakdown)

- **The cause of an error comes from that call's own output** — the stdout/stderr text in
  `trace_summary` / `recoveries`. Quote the key line verbatim («[!] раздел «known_for»: фраза
  без номера источника — «…после ухода из «Рамблера»;…»») and explain *that*. Do not build
  a story the output does not support (e.g. «ссылка исчезла при перезаписи» when the output
  says the sentence before «;» has no source number). No output in the trace — say so.
- **Numbers come from the task fields** (`total_rounds`, `cost_usd`, call and error counts in
  the trace). Give each number once; never two different counts for the same thing
  («6 перезаписей … семь write_file»).
- **Comparisons with earlier runs** only from `recent_tasks` data you actually fetched
  (raise `limit` if needed), not from memory or notes.
- **Separate who must fix what**: a problem in a skill/tool (wrong check, unclear message)
  vs. agent behaviour (ignored an instruction). Fixes for the first go to the skill owner.
  If the same error repeats after the agent did what the message asked, suspect the
  check itself, not the agent — in a live run a script demanded a quote for a number in
  «Не подтверждено» although the instructions exempted that section.
- **Model**: name the model that served the rounds only if the task entry or trace
  carries it; otherwise say it is not in the trace. Never take it from your own idea of
  which model you are.

### Formatting for the chat

The chat renders text between two `$` signs as a math formula: «~$4 — лучше, чем $15.75»
turned into italic text with the spaces removed. Never put `$` before a number in prose or
tables: write amounts as «3.93 USD» (or «3,93 долл.»). The same applies to any other `$`.

## What is NOT in this report (known limit)

`recent_tasks` returns status, rounds, result, and the qualitative tool-call trace; some
installations also include `cost_usd` and token counts — report them only when the returned
entry actually carries them. Wall-clock duration usually lives in the audit store, which a
skill cannot read. Do not promise token, cost or timing numbers that are not in the entry
and do not invent them. If the user asks for them, answer that they are not available through this
trace; do not estimate. The value of this report is the call-by-call breakdown and the
fix-oriented verdict, not the metrics.

## Honest handling

- If the run **failed**, the breakdown is the most useful part: name the failing call, its
  error, and the fix. Do not soft-pedal a failure.
- If the run was **clean and short**, the breakdown can be two lines: what ran, that it
  succeeded. Do not pad a clean run into a long report.
- If `recent_tasks` is **absent** (the tool is not in the catalog in this contour), say the
  debug trace is unavailable here; do not fall back to narrating what you remember doing.
- Never invent tool calls, statuses, or arguments that are not in the returned
  `trace_summary`. A breakdown with a fabricated call is worse than no breakdown.

## Language

Match the user's language. A Russian request ("в режиме дебага") gets a Russian breakdown;
an English request gets an English one. The trace fields (tool names, statuses) stay as the
runtime emits them — do not translate `completed` to «завершено» inside the trace block,
only in the surrounding prose. 
