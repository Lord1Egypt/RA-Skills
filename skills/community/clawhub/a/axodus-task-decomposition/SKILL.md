---
name: task-decomposition
description: Break complex tasks into executable, dependency-aware steps.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: core
---

# SKILL: task-decomposition

## Purpose
Break a raw task into an ordered, executable, dependency-aware step list with acceptance criteria and explicit open questions.

## When to Use
- The request implies multiple files or multiple subsystems.
- The request is vague, inconsistent, or underspecified.
- The request mixes design + implementation + validation.

## Inputs
- `raw_task_description` (required, string): the user request as-is.
- `constraints` (optional, string[]): non-negotiables (security, time, language, tooling).
- `repo_context` (optional, string): relevant paths, conventions, or prior decisions.
- `risk_level_hint` (optional, enum: `low|medium|high`): if the user already signaled risk.

## Steps
1. Restate the task in 1â€“3 sentences without adding assumptions.
2. Extract deliverables (expected behavior, files to touch, commands to run).
3. Identify unknowns that block execution and convert them into concrete questions.
4. Split work into atomic steps; each step must include:
   - action + target
   - a single primary outcome
   - acceptance criteria (`done_when`)
5. Order steps by dependency and mark safe parallelization explicitly.
6. Tag each step with:
   - `risk` (`low|medium|high`)
   - `validation` (what will be checked)
7. If unknowns are material, stop and ask only the minimum questions; otherwise proceed with stated assumptions.

## Validation
- No step depends on hidden context.
- Every step has measurable acceptance criteria.
- Dependencies are explicit (no â€œand then it worksâ€).
- No step contains vague verbs (â€œimproveâ€, â€œoptimizeâ€, â€œmake betterâ€) without a measurable target.

## Output
Structured plan (example schema):

```yaml
summary: "<what will be delivered>"
open_questions:
  - "<question>"
assumptions:
  - "<assumption (only if low risk)>"
steps:
  - id: 1
    action: "<verb phrase>"
    targets: ["<path/system>"]
    risk: low
    validation: "<check to run>"
    done_when: "<observable condition>"
```

## Safety Rules
- Do not invent requirements, APIs, or file paths.
- If a step can be destructive, require explicit confirmation in the plan.
- Prefer the smallest viable step sequence; avoid gold-plating.

## Example
Input:
- `raw_task_description`: â€œAdd a CLI command to export reports.â€
- `constraints`: `["No breaking changes", "Must include tests"]`

Output (excerpt):
```yaml
summary: "Add `report export` command and tests"
open_questions:
  - "What output formats are required (json/csv/pdf)?"
steps:
  - id: 1
    action: "Locate existing CLI entrypoints and command router"
    targets: ["src/cli/*"]
    risk: low
    validation: "CLI help shows existing commands unchanged"
    done_when: "Command dispatch mechanism is identified"
```
