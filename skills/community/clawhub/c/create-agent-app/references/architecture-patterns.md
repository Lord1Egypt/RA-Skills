# Architecture Patterns

Use these patterns as starting points. Adapt to the target repository, but keep module boundaries explicit.

## Application Types

- **CLI**: Best for local workspace agents, code/document automation, deterministic artifact generation, and operator approval prompts.
- **Web app**: Best for human-facing chat, streaming UI, task dashboards, and browser-based review.
- **API service**: Best for integrating an agent into other systems with durable requests, auth, queues, and observability.
- **Desktop/internal tool**: Best for local enterprise workflows, file-heavy tasks, and controlled operator environments.
- **Hybrid**: Use only when there is a real need for more than one surface; keep shared harness code in a package.

## Harness Types

- **Single agent**: One model loop with a tool registry. Use for focused workflows with limited branching.
- **Planner-worker**: Planner produces steps; worker executes bounded tasks. Use when decomposition and traceability matter.
- **Multi-agent**: Multiple roles with explicit handoff contracts. Use only when role separation adds real value.
- **Workflow-first**: Deterministic state machine with model calls in selected nodes. Use for regulated or repeatable processes.
- **Human-in-loop**: Include approval checkpoints and resumable state. Use when tools can mutate data, cost money, or damage files.

## Candidate Selection

Offer 2-3 candidates. Each candidate must state:

- app type and harness type
- provider pattern
- state/memory choice
- tool safety posture
- validation plan
- why it fits
- what it gives up

## Recommended Module Shape

Use or adapt this TypeScript layout:

```text
src/
  config/env.ts
  providers/
    index.ts
    openai.ts
    openai-compatible.ts
  agent/
    harness.ts
    prompts.ts
    types.ts
  tools/
    registry.ts
    approvals.ts
  memory/
    store.ts
  artifacts/
    ledger.ts
  validation/
    smoke.ts
```

Keep framework entrypoints thin:

- CLI command parses input, loads env, invokes harness, prints results.
- API route validates request, invokes harness, returns structured response.
- UI component streams state from an API or server action; it does not own tool execution policy.

