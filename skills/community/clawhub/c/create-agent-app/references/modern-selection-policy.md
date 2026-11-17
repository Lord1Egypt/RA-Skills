# Modern Selection Policy

"Advanced" means the generated app uses current, fit-for-purpose TypeScript and agent architecture that can be validated. It does not mean adding more frameworks.

## Decision Order

Choose technology in this order:

1. **User need**: workflow, surface, latency, deployment, safety, state, tool scope, and validation requirements.
2. **Official support**: prefer libraries with current official documentation and maintained TypeScript support.
3. **Industry architecture signal**: consult `industry-architecture-signals.md` for production patterns when the brief involves scale, governance, orchestration, observability, or long-running work.
4. **Runtime fit**: match the app surface: Node CLI/service, Next.js app, edge/serverless, desktop/internal, or hybrid.
5. **Harness fit**: choose the smallest harness that supports the required planning, tools, memory, approvals, trace, and evaluation.
6. **Verification fit**: choose dependencies and patterns that can be typechecked, tested, built, and smoke-tested in the target workspace.

If a choice fails any step, do not use it just because it is newer.

## TypeScript Baseline

Use these defaults unless the user or repo requires otherwise:

- strict TypeScript
- ESM or the repository's existing module mode; do not mix module systems casually
- `zod` for runtime input and env validation
- typed provider interface instead of SDK calls scattered through the app
- typed tool registry with explicit side-effect and approval metadata
- `vitest` or the repo's existing test runner
- package manager and workspace conventions already present in the target repo

Avoid adding:

- ORM/database libraries unless durable state requires them
- queues unless tasks must survive process or request lifetimes
- UI component kits unless the user is building a UI and the repo already supports one or the user confirms it
- observability stacks unless trace/export requirements justify them

## Agent Harness Selection

Use this rubric:

- **Single agent**: choose when one loop and a bounded tool registry can solve the task.
- **Planner-worker**: choose when task decomposition must be inspectable or resumable.
- **Workflow-first**: choose when deterministic gates, retries, approvals, or artifact validation matter more than open-ended autonomy.
- **Multi-agent**: choose only when independent roles, handoffs, or review gates reduce real complexity. Do not use it for branding.
- **Human-in-loop**: choose when tools can mutate files, accounts, databases, external APIs, or cost money.

## Harness Modernity Checklist

Before selecting a harness shape, evaluate:

- Does the app need an agent loop, or would one structured model call plus deterministic code be better?
- Who owns turn execution: local harness code, OpenAI Agents SDK, AI SDK, Mastra, or another confirmed framework?
- Are tools typed, schema-validated, permissioned, and traceable?
- Are handoffs explicit, typed, and testable when multi-agent behavior is selected?
- Are guardrails attached to input, tool use, output, or all three?
- Can runs be cancelled, retried, resumed, or audited according to the brief?
- Can the harness be validated offline and smoke-tested live without fake success?
- Are MCP/computer/browser capabilities used only when the brief needs that boundary?

## Provider Selection

- **openai-direct**: choose for CLI/API/backend apps needing direct OpenAI Responses API control.
- **OpenAI Agents SDK**: choose when the user needs first-class agents, tools, guardrails, handoffs, sandbox agents, or multi-agent orchestration using OpenAI's agent framework.
- **ai-sdk**: choose for TypeScript apps needing provider abstraction, streaming UI, tool calling, structured generation, or Vercel/Next.js integration.
- **mastra**: choose when the user needs an agent/workflow framework with explicit workflows, memory, RAG, MCP, evals, or local dev studio behavior.
- **openai-compatible**: choose for ARK, vLLM, LiteLLM, gateways, or self-hosted compatible endpoints; verify capability gaps.
- **custom adapter**: choose only when the target provider has no appropriate maintained SDK or abstraction.

## Fit-to-Need Guardrails

Before coding, write:

```markdown
## Modernity Rationale
- Current official docs checked:
- Industry architecture signals checked:
- Selected TS/runtime stack:
- Selected agent harness:
- Why this is advanced for this user's brief:
- What was intentionally not added:
```

Every "advanced" element must answer:

- What user requirement does it satisfy?
- What simpler option was rejected, and why?
- How will it be validated?
- What failure mode does it make clearer or safer?

If there is no concrete answer, remove that element.

## Anti-Overbuild Examples

- Do not add Mastra when a single OpenAI Responses API call plus a typed tool registry satisfies the CLI.
- Do not add OpenAI Agents SDK when the app needs only one direct model call and no managed turns, handoffs, sessions, or guardrails.
- Do not add durable memory when the user asked for stateless extraction.
- Do not add multi-agent roles when planner-worker with checkpoints is enough.
- Do not add a web dashboard for an internal CLI unless review, approval, or monitoring is a user requirement.
- Do not add database persistence when a file-backed artifact ledger satisfies validation.
- Do not add computer/browser control when a typed API, MCP connector, or shell command can satisfy the task safely.
