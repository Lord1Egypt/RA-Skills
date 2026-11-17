# Grill Questions

Use these questions to produce an Agent App Brief. Ask only what is needed, but do not skip a category unless the user already answered it.

## Agent App Brief Fields

- **Goal**: What concrete workflow should the agent complete?
- **Users**: Who runs it, and what permissions should they have?
- **Application type**: CLI, web app, API service, desktop/internal tool, or hybrid.
- **Harness type**: single agent, planner-worker, multi-agent, workflow-first, or human-in-loop.
- **Runtime boundary**: local workspace, sandbox, shell, file read/write, network, database, browser, MCP.
- **Model provider**: openai-direct, ai-sdk, mastra, openai-compatible, or custom provider adapter.
- **State and memory**: stateless, thread memory, durable task store, artifact ledger.
- **Tool safety**: forbidden tools, approval-required tools, dry-run-only tools.
- **Validation standard**: offline build/type/test, live LLM smoke, tool-call trace, artifact validation.
- **Deployment target**: local only, Docker, Vercel, Node service, internal server, or unspecified.

## Minimum Questions

Ask these first when the prompt is underspecified:

1. What application type should this be: CLI, web app, API service, desktop/internal tool, or hybrid?
2. Should the harness be single-agent, planner-worker, multi-agent, workflow-first, or human-in-loop?
3. Which model/provider pattern should be used: OpenAI SDK, Vercel AI SDK, Mastra, OpenAI-compatible endpoint, or custom adapter?
4. What tools may the agent use, and which actions require approval?
5. What must pass before the work counts as done: typecheck, build, tests, live LLM smoke, tool trace, artifact validation?

## Confirmation Format

Before generating code, summarize:

```markdown
## Agent App Brief
- Application type:
- Harness:
- Runtime boundary:
- Provider:
- State/memory:
- Tool safety:
- Validation:
- Deployment:

## Decision Required
Confirm one architecture candidate before I edit files.
```

