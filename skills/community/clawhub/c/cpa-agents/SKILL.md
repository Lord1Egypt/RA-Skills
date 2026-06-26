# CPA Agents for OpenClaw

Version: 2.0.0

Use concurrent process algebra for practical multi-agent orchestration in OpenClaw.
This skill is focused on production workflows: parallel execution, branch-fix loops,
model fan-out, and session status introspection.

## Install

### 1) Install library dependency

```bash
npm install cpa-agents
```

### 2) Create skill entrypoint

```ts
import { createOpenClawSkill } from "cpa-agents/adapters/openclaw";

export default createOpenClawSkill();
```

### 3) Runtime prerequisites

- OpenClaw Gateway is running and reachable.
- Skill host supports async command handlers.
- Session context provides `appendEvent` for trace streaming.

## Advanced operators

Use these when you need stronger control over failures, rollback, and data lineage.

### Undo / rollback (`invertible` + `saga`)

- `invertible(forward, undo)` defines a step plus compensating action.
- `saga([...steps])` executes steps in order; on failure, runs undo in reverse order.
- Best for workflows with side effects (branch creation, file writes, merges, etc.).

Pattern:

```ts
import { invertible, saga } from "cpa-agents";

const workflow = saga([
  invertible(createBranch, deleteBranch),
  invertible(writeCode, revertCode),
  invertible(runValidation, cleanupValidation),
]);
```

### Provenance (`converse`)

- `converse(R, inverseFn)` is relational provenance, not operational undo.
- Use it to answer: "which input(s) could have produced this output?"
- Keep this separate from rollback logic (`invertible`/`saga`).

Pattern:

```ts
import { rel, converse } from "cpa-agents";

const generate = rel("generate", async (prompt: string) => [prompt + "-out"]);
const provenance = converse(generate, async (output: string) => [output.replace("-out", "")]);
```

### Guarded flow (`guard`, `guardValue`, `ifThenElse`)

- Use `guard(...)` to block unsafe execution.
- Use `guardValue(...)` when a required value must exist.
- Combine with `ifThenElse(...)` for conditional routing.

### Reliability (`retryWithBackoff`, `timeout`, `or`)

- `retryWithBackoff` for transient failures.
- `timeout(ms, process)` to bound execution.
- `or(primary, fallback)` for fallback routing when primary fails.

## Practical guidance: undo vs converse

- Use **undo** (`invertible` + `saga`) when you must reverse side effects.
- Use **converse** for provenance/audit and lineage queries.
- Typical production setup uses both:
  - `saga` during execution
  - `converse` for post-run explainability

## Commands

### `parallel`

Run independent tasks concurrently.

```json
{
  "tasks": [
    "analyze failing tests",
    "draft fix proposal",
    "write migration notes"
  ],
  "timeout": 300000
}
```

### `branch-fix`

Run one task, and if errors are returned, branch into fix flow and continue.

```json
{
  "task": "implement auth middleware and resolve lint issues",
  "timeout": 300000
}
```

### `fan-out`

Run the same task across multiple models and merge outputs.

```json
{
  "task": "propose API surface for agent orchestration",
  "models": ["model-a", "model-b"],
  "timeout": 300000
}
```

### `status`

Return the current CPA process tree/status for the session.

```json
{}
```

## Recommended prompts

- "Run parallel: audit security risks, propose patch plan, generate tests"
- "Branch-fix this refactor until no type errors remain"
- "Fan-out this architecture question across two models and compare"
- "Show cpa status"
- "Execute as saga: create branch, patch files, validate, rollback on failure"
- "Show provenance: what input likely produced this output?"

## Troubleshooting

- Gateway not connected:
  - Start OpenClaw Gateway and retry.
- Unknown command:
  - Use one of: `parallel`, `branch-fix`, `fan-out`, `status`.
- Timeout:
  - Increase `timeout` in command args.
- Missing session events:
  - Ensure session context is present and `appendEvent` is enabled.
- Rollback did not occur:
  - Verify steps are wrapped with `invertible(...)` and executed with `saga(...)`.
- Provenance unclear:
  - Provide an explicit `inverseFn` when defining `converse(...)`.
