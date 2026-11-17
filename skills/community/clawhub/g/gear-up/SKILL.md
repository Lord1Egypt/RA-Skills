---
name: gear-up
description: >
  Part of the Overpowered skill suite.
  Create and activate the smallest temporary capability needed to close a real execution gap during a task, then measure whether it helped and discard or nominate it for reuse. Use only when installed skills, available tools, existing context, knowledge retrieval, and Academy candidates cannot reliably perform a material part of the objective; supports temporary skills, context instructions such as AGENTS.md fragments, and runtime tools when the harness can load them dynamically.
compatibility: >
  Portable decision and lifecycle policy. Hot activation of generated skills, context, or tools requires a harness/runtime adapter; never claim activation succeeded unless the runtime confirms it.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "4-adaptive-capability"
  version: "0.2.0"
---

# Overpowered / Gear Up

## Promise

**Equip yourself with exactly what this task needs — reuse first, create only to close a material capability gap, and keep nothing by default.**

`gear-up` is not a generic code generator and not a shortcut for writing many helper files. It is a last-mile capability acquisition protocol for a task that the current agent loadout cannot execute reliably.

## Hard gate: prove the gap before creating anything

Before generating an artifact, answer all six questions:

1. **What exact part of the objective cannot be executed reliably now?**
2. **Is this a capability gap rather than a knowledge gap?** If missing information can solve it, use `know-enough` instead.
3. **Can an installed skill, available tool, generic shell/code operation, or current context solve it safely with reasonable effort?** If yes, reuse it.
4. **Does the Skill Academy contain a suitable candidate or graduated capability?** If yes, prefer reuse/evaluation over creation.
5. **What is the smallest artifact that closes the gap?**
6. **What observable result will prove that creating it was worthwhile?** If no useful success test exists, do not create it.

For the full gate, read `references/capability-gap-gate.md` only when the gap is ambiguous.

## Choose the smallest artifact

Prefer the least powerful artifact that can solve the gap:

| Need | Preferred artifact |
|---|---|
| Missing facts, policy, precedent, or organizational context | No artifact; use `know-enough` |
| One-off operation already possible with generic tools | No artifact; perform it directly |
| Task-wide rule or convention that must remain salient | Temporary context instruction / `AGENTS.md` equivalent |
| Reusable multi-step reasoning or procedure for this task | Temporary skill |
| Missing deterministic operation or integration | Temporary runtime tool |
| Procedure needs a new deterministic operation | One temporary skill + one tool, only with explicit justification |

Read `references/artifact-selection.md` when more than one artifact type appears plausible.

## Creation budget

Default budget per capability gap:

- **one primary generated artifact**;
- **zero companion artifacts** unless separation of procedure and mechanics is necessary;
- more than two generated artifacts for one gap requires explicit user approval or an equivalent high-authority policy.

Do not split a simple capability into multiple files for elegance. Do not generate an agent/subagent definition merely to reduce the parent agent's context load.

## Ephemeral workspace

Generate into a task-scoped temporary location, never directly into permanent harness configuration unless the user explicitly requested permanent installation.

Recommended logical layout:

```text
.overpowered/runtime/<run-id>/
├── manifest.yaml
├── skills/        # only if needed
├── tools/         # only if needed
└── context/       # only if needed
```

The exact path is runtime-specific. The manifest records the gap, generated artifacts, activation method, validation evidence, and cleanup policy. Use `references/runtime-manifest.example.yaml` when a concrete manifest is useful.

## Validate before activation

Before a generated capability can affect execution:

1. validate syntax/structure;
2. inspect dependencies and permissions;
3. reject hidden or unrelated side effects;
4. run the narrowest available test or `dry-run` when executable behavior is involved;
5. ensure temporary context does not override higher-authority instructions;
6. activate only through a runtime mechanism that can confirm success.

Generated executable code is **untrusted until validated**. Apply `human-gates` before high-impact permissions or side effects.

## Activate, use, measure

After activation:

1. use the capability only for the gap it was created to close;
2. capture the observable result defined by question 6;
3. compare with the pre-creation failure/gap;
4. classify the outcome:
   - **ineffective** — did not materially help; deactivate and discard;
   - **useful once** — solved the current gap; keep only as an Academy candidate record if worthwhile;
   - **reusable signal** — solved a recurring/generalizable gap; nominate for Academy evaluation.

Never infer value merely because the artifact executed without errors.

## Academy handoff

A successful ephemeral capability is **not** automatically a permanent skill.

Record only enough evidence for later evaluation: capability gap, artifact type, task outcome, validation evidence, limitations, dependencies, and reuse hypothesis. Read `references/academy-handoff.md` for the portable handoff record; the full Overpowered repository also defines the Skill Academy protocol in `ACADEMY.md`.

`skillify` is downstream of Academy qualification: it generalizes and packages a proven method; it is not the hot-generation mechanism.

## Runtime truthfulness

The skill defines policy, not magic. If the current harness cannot hot-load a generated artifact:

- do not claim it was activated;
- use the artifact directly only if existing tools can execute/read it safely;
- otherwise store it as a candidate for the next supported reload/session or ask for the minimal runtime action required.

Read `references/runtime-contract.md` when integrating a harness adapter.

## Anti-patterns

- Creating a skill because the current prompt is long.
- Creating a tool for an operation that shell/Python/SQL already handles adequately.
- Treating missing knowledge as a missing capability.
- Generating several speculative helpers before testing the first one.
- Persisting temporary files into global skill directories after one successful task.
- Letting generated context silently supersede project or user instructions.
- Calling a generated tool “loaded” without runtime confirmation.

## Stop condition

Stop `gear-up` when the material capability gap is closed with the smallest validated artifact, its value has been observed on the real task, and the artifact has been either discarded or recorded for Academy evaluation. Do not continue generating capabilities after the task can proceed reliably.
