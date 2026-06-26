# Context Guardian

`context-guardian` is a production-ready continuity layer for long-running autonomous agent work.

## What it does
- measures context pressure,
- writes checkpoints and summaries to disk,
- restores the important task state before the next action,
- stops autonomous execution when fidelity is too low,
- keeps the runtime bundle ahead of stale chat history.

## Files
- `SKILL.md` — skill entrypoint and workflow
- `scripts/context_guardian.py` — reference implementation
- `scripts/test_context_guardian.py` — tests
- `references/task-state-schema.md` — canonical state model
- `references/summary-template.md` — summary format
- `references/config-example.yaml` — configuration example
- `references/persisted-task-state.example.json` — saved state example
- `references/summary-example.md` — saved summary example
- `references/integration-checklist.md` — integration checklist

## Usage
1. Add the module to the host agent loop.
2. Load `task_state.json` and the latest summary at session start.
3. Rebuild the working bundle before each major action.
4. Check pressure before each major action.
5. Checkpoint before destructive work and at critical pressure.
6. Stop and recover when pressure is critical; do not soften the halt with confidence-based exceptions.

## OpenClaw-style integration pattern
For OpenClaw-like hosts, the easiest reliable integration is a thin workspace-level wrapper CLI around the reference module.

Recommended command surface:
- `status` — inspect current task/summary availability and safe next step
- `ensure` — initialize canonical state if missing, or validate existing state
- `checkpoint` — write a fresh checkpoint and refresh the latest summary alias
- `bundle` — build the working bundle for the next major action

Integration note for the reference implementation:
- `SafetyGate.evaluate(...)` now accepts `action_changed_state`, `phase_or_goal_changed`, and `summary_conflict`.
- Pass `action_changed_state=True` when the guarded action mutated durable task state so non-critical turns still write the required checkpoint.
- Pass `phase_or_goal_changed=True` or `summary_conflict=True` when those conditions are true so normal-pressure turns still refresh the structured summary and latest-summary alias as required by the runtime contract.

Weak-model integration tips:
- Prefer a session-level root default (for example `CG_ROOT=/workspace`) so weaker models do not depend on fragile global-option ordering.
- Keep a stable `summaries/latest-summary.md` alias for runtime reads, even if timestamped summaries also exist.
- If the host may already contain legacy task-state shapes, detect and archive them explicitly before canonical initialization.
- Keep field names aligned: `phase` in the runtime contract maps to schema `current_phase`; `last_successful_action` maps to `last_action.summary` or `last_action.outcome`; `touched_files` and `relevant_artifacts` map to artifact `path` values.

## Enable it
- Copy the reference module into the host project.
- Wire `ContextMonitor` into the agent loop.
- Wire `CheckpointStore` into planner/tool events.
- Wire `MemoryAssembler` before major model calls.
- Wire `SafetyGate` before autonomous continuation, pass `action_changed_state=True` whenever the guarded action mutated durable task state, and pass `phase_or_goal_changed=True` or `summary_conflict=True` whenever those conditions are true so summary refreshes are not skipped at normal pressure.
- Configure paths and thresholds in the host project.

## Tests
From the skill root, run:

```bash
python3 scripts/test_context_guardian.py
```

The test script is shipped with the skill, creates temporary directories during execution, and should exit with code 0 when the current artifact is valid.
