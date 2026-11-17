# Artifact Selection

Choose the weakest artifact type that closes the proven capability gap.

## No artifact

Prefer no generated artifact when the task can be completed with existing capabilities in a small number of reliable operations. A generated wrapper around a generic tool usually adds context and maintenance cost without adding capability.

## Temporary context instruction

Use for a small set of task-wide rules that must remain salient across many turns or operations.

Good examples:

- preserve exact requirement identifiers while normalizing text;
- use a project-specific naming convention throughout the current task;
- never alter production files during this analysis run.

Do not use context instructions to encode a multi-step procedure that should be a skill. Do not overwrite higher-authority `AGENTS.md`, project, or user instructions; add a lower-authority scoped fragment through the harness adapter.

## Temporary skill

Use for a reasoning/procedural method with multiple steps, branching, stopping conditions, or non-obvious gotchas.

A temporary skill should still follow Agent Skills discipline: focused responsibility, trigger description, concise `SKILL.md`, and optional one-level references only when needed.

Do not generate a skill that merely restates the current task.

## Temporary tool

Use only when the runtime lacks a deterministic operation needed to complete the task reliably, such as a missing local integration, parser, validator, or transformation.

Generated tools should be:

- narrow in capability;
- least-privileged;
- deterministic where possible;
- explicit about inputs/outputs;
- validated before activation;
- side-effect-free by default when a read-only form is sufficient.

## Skill + tool pair

Create both only when the *procedure* and the *mechanism* are independently necessary. Example: a requirement-comparison skill needs a deterministic tool that normalizes identifiers and preserves provenance.

Do not create a tool solely so a generated skill has something custom to call.

## Agent/subagent definitions

A new agent definition is justified only when the harness supports it and a distinct role, tool boundary, context boundary, or independent verification responsibility materially improves the task. Delegation for convenience or token management alone is not enough.
