---
name: context-guardian
description: Production-ready context continuity skill for autonomous AI agents. Use when tasks may outlive a single LLM context window, when you need durable checkpoints, structured summaries, restart recovery, pressure-aware trimming, or when the agent must stop safely instead of continuing blindly after context loss.
---

# Context Guardian

Use this skill to keep long-running agent work resumable, loss-aware, and safe.
Use it when a task may outlive one model context window or when a host must stop safely before context loss causes bad decisions.

## Execution

## For the Agent — Mandatory Runtime Contract

Follow this order.
Do not skip steps.

### Required startup reads
Read these before acting:
1. `references/task-state-schema.md` — required task-state fields.
2. `references/summary-template.md` — required summary shape.
3. The host-configured durable task state file.
4. The host-configured structured summary file, if it exists.

### Required host capabilities
The host must provide all of these:
- a way to read the durable task state file,
- a way to write the durable task state file,
- a way to read the structured summary file,
- a way to write the structured summary file,
- a numeric context-pressure value in range `0.0` to `1.0` before each major action,
- a real stop path for emitted status signals.

If the host cannot provide the durable task-state read/write path, emit `STATUS:MISSING_STATE` and stop.

### Defined terms
- **Major action** = any LLM call that can materially change the plan, any tool call that writes or deletes data, any code or file edit, or any step that consumes meaningful context.
- **Fresh checkpoint** = a durable task-state write that happened after the latest state-changing action.
- **Safe recovery** = the durable task state exists, required fields are present, and `next_action` is non-empty.
- **Relevant artifacts** = files listed in durable state, such as `touched_files`, or files explicitly required by `next_action`.
- **Field alignment note** = `phase` in this document corresponds to `current_phase` in `references/task-state-schema.md`; `last_successful_action` corresponds to `last_action.summary` or `last_action.outcome`; `touched_files` and `relevant_artifacts` correspond to the `path` values inside the `artifacts` array.

### Startup branch
1. Read the latest durable task state from disk.
2. If no durable task state exists:
   - If the structured summary file also does not exist, initialize from `references/task-state-schema.md`, set `next_action` to `START`, write the initial durable state, write an initial summary from `references/summary-template.md`, and continue.
   - If the structured summary file exists but durable task state is missing, emit `STATUS:MISSING_STATE` and stop.
3. If the durable task state exists but required fields are missing, emit `STATUS:MISSING_STATE` and stop.
4. If `next_action` is empty, emit `STATUS:MISSING_STATE` and stop.
5. If `next_action` is `DONE`, `COMPLETE`, or `FINISH`, write final durable state + summary, emit `STATUS:COMPLETE`, and stop.
6. Read the latest structured summary from disk.
7. After startup completes, the structured summary file must exist.
8. If the summary is missing, emit `STATUS:MISSING_STATE` and stop.
9. If the summary conflicts with the durable task state, trust the durable task state, rewrite the summary immediately, and continue.

### Pressure thresholds
Default thresholds. Override them through host configuration when available:
- `warning_threshold = 0.55`
- `compress_threshold = 0.70`
- `critical_threshold = 0.85`

### Quick reference
- `< 0.55` → continue normally
- `0.55 to < 0.70` → continue, but expect fresher state/summary discipline
- `0.70 to < 0.85` → continue only with a fresh summary before the next major action
- `>= 0.85` → write checkpoint + summary, emit `STATUS:HALT_CONTEXT_LIMIT`, stop autonomous execution

### Pressure fallback rule
This skill requires a host-provided numeric pressure value.
Do not estimate pressure from characters, words, or token guesses in production hosts.
Use this fallback only when the host cannot provide a reliable pressure value:
1. On the first turn only, assume `pressure = 0.0`.
2. On any later turn, treat missing pressure as critical and run the Halt Rule.

**Reference implementation note:** `scripts/context_guardian.py` includes a character-based pressure estimator for reference/test environments only. Production hosts must prefer explicit host-owned pressure reporting over that estimator, and the reference `SafetyGate.evaluate(...)` accepts a host pressure override plus explicit integration flags such as `action_changed_state`, `phase_or_goal_changed`, and `summary_conflict` so integrations can follow the contract directly and avoid suppressing required checkpoints or summaries during low-pressure state transitions.

### Runtime loop
Repeat this loop before every major action.

1. **Read fresh state**
   - Re-read the latest durable task state from disk.
   - Re-read the latest structured summary from disk.
   - If `next_action` is `DONE`, `COMPLETE`, or `FINISH`, write final durable state + summary, emit `STATUS:COMPLETE`, and stop.
   - If the structured summary is missing, emit `STATUS:MISSING_STATE` and stop.
   - Do not rely on stale in-memory state when a newer disk version may exist.
2. **Check pressure**
   - Read the numeric pressure value from the host.
   - If pressure is below `warning_threshold`, continue to Step 3.
   - If pressure is at or above `warning_threshold` but below `compress_threshold`, continue to Step 3.
   - If pressure is at or above `compress_threshold` but below `critical_threshold`, continue to Step 3 and write a fresh summary in Step 5 before the next major action.
   - If pressure is at or above `critical_threshold`, go to the Halt Rule.
3. **Build the working bundle**
   - If the host already has a context-assembly helper, pass it these exact inputs: `goal`, `phase`, `next_action`, `last_successful_action`, `constraints`, and `relevant_artifacts`.
   - Otherwise include exactly these fields in the working context: `goal`, `phase`, `next_action`, `last_successful_action`, `constraints`, and all file paths listed in `touched_files` or explicitly named in `next_action`.
   - Do not include the full durable state file by default.
   - Include the latest structured summary only when it materially helps the next major action.
   - Do not guess missing fields.
4. **Execute one major action**
   - Execute exactly one checkpointable major action.
   - If the action fails, record the failure in durable state, write the durable task state immediately, and restart the loop from Step 1.
   - Do not chain multiple risky actions when one checkpointable step is enough.
5. **Persist state**
   - If the action changed state, write the durable task state immediately.
   - Write a fresh summary immediately if any of these are true: pressure is at or above `warning_threshold`, pressure is at or above `compress_threshold`, the summary conflicted with durable state, or the action changed phase or goal.
6. **Repeat**
   - Start the loop again from Step 1 before the next major action.

### Halt rule
This rule overrides everything else.

If pressure is at or above `critical_threshold`, or required pressure is missing after the first turn, do this immediately:
1. write checkpoint + summary,
2. emit `STATUS:HALT_CONTEXT_LIMIT`,
3. stop autonomous execution,
4. wait for explicit human or system override.

Do not soften this halt with confidence-based exceptions.

Do not continue autonomously after `STATUS:HALT_CONTEXT_LIMIT`.

### Summary rule
When you write a summary, preserve:
- goal,
- current phase,
- completed steps,
- failed attempts,
- decisions,
- files touched,
- important tool outputs,
- blockers,
- next action,
- invariants,
- constraints.

Do not depend on raw chat history alone for recovery.
Do not guess missing durable state that should be read from storage.
Do not invent missing tool outputs.

## For the Developer Only — Integration Notes

Ignore this section if you are the runtime agent executing a task.
Use this section only when wiring the module into a host agent loop.

### Minimum safe integration order
1. Read `references/integration-checklist.md` to identify the smallest safe integration point.
2. Represent task continuity with `references/task-state-schema.md`.
3. Keep task state in durable JSON.
4. Keep summaries in human-readable markdown.
5. Rebuild the working bundle before each major model call.
6. Write checkpoints after state mutations, before destructive actions, at or above warning pressure when required by the runtime loop, before run end, and after failures that change the plan. When wiring the reference implementation, pass `action_changed_state=True` whenever the guarded action mutated durable task state so below-critical turns still produce the required checkpoint. Also pass `phase_or_goal_changed=True` or `summary_conflict=True` whenever those conditions are true so the reference implementation emits the fresh summary required by the runtime contract even at normal pressure.
7. Reuse an existing planner, tool runner, or memory module when one already exists instead of duplicating storage.
8. Ensure the host treats `STATUS:MISSING_STATE`, `STATUS:HALT_CONTEXT_LIMIT`, and `STATUS:COMPLETE` as real state signals.
9. Keep pressure reporting numeric and host-owned. Do not push token estimation onto the model.
10. If the host uses a helper CLI, keep it thin and repetitive: `status`, `ensure`, `checkpoint`, `bundle` is usually enough.
11. If weak models will call that CLI directly, prefer a session-level root default (for example an environment variable) instead of repeating a fragile `--root ...` flag in every command.
12. Prefer a stable summary alias such as `summaries/latest-summary.md` for runtime reads, even when timestamped summaries are also stored.
13. If legacy task-state files may already exist in the host, detect that shape before mutation and require explicit archival/reinitialization instead of silent overwrite.

### Reference file purposes
- `references/task-state-schema.md` — canonical task-state fields.
- `references/summary-template.md` — canonical summary format.
- `references/config-example.yaml` — config shape, paths, thresholds.
- `references/persisted-task-state.example.json` — persisted state example.
- `references/summary-example.md` — concrete markdown summary example.
- `references/integration-checklist.md` — host-loop integration checklist, including weak-model-safe wrapper rules.
- `references/implementation-notes.md` — practical wrapper and runtime integration notes.

## Deterministic implementation reference

Use `scripts/context_guardian.py` as the source-of-truth reference implementation when the host project uses Python or when behavior is ambiguous.
If wording and the reference implementation diverge, `scripts/context_guardian.py` governs the deterministic integration contract, while `SKILL.md` governs the mandatory agent execution behavior.
Use `scripts/test_context_guardian.py` to validate checkpoint creation, summary generation, restart recovery, critical-threshold stop behavior, and trimming policy.

## Developer guardrails
- Do not continue blindly after context loss.
- Do not guess missing state that should be loaded from durable storage.
- Do not keep stale checkpoints when a fresh one is required.
- Do not let the host ignore halt statuses.

## Completion standard

A valid implementation must:
- persist durable task state outside the LLM context,
- recreate a working bundle before each major action,
- checkpoint and summarize on pressure or on progress,
- stop when context fidelity is too low,
- recover from restart using the latest durable state,
- keep thresholds and paths configurable,
- include tests and examples.
