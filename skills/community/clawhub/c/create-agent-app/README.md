# create-agent-app

`create-agent-app` is a Codex skill for designing, generating, and refactoring production-grade TypeScript agent applications.

It is intended for real agent application bases, not toy demos. The skill forces Codex to clarify the user's requirements, select a fit-for-purpose modern TypeScript and agent harness architecture, map requirements to files, implement scoped code, and report real validation results.

## Install

```bash
npx skills add github:LeoGoat2004/create-agent-app
```

After installation, invoke it explicitly:

```text
Use $create-agent-app to create a TypeScript agent app in the target directory I specify.
```

## Skill Workflow

1. **Clarify the brief**
   - Application type: CLI, web app, API service, desktop/internal tool, or hybrid.
   - Harness type: single agent, planner-worker, multi-agent, workflow-first, or human-in-loop.
   - Runtime boundary: workspace, sandbox, shell, file access, network, database, browser, or MCP.
   - Provider pattern: OpenAI direct, OpenAI Agents SDK, Vercel AI SDK, Mastra, OpenAI-compatible endpoint, or custom adapter.
   - State model: stateless, thread memory, durable task store, or artifact ledger.
   - Safety policy: forbidden tools, approval-required tools, and dry-run-only tools.
   - Validation standard: typecheck, build, tests, live LLM smoke, tool trace, and artifact validation.

2. **Propose architecture candidates**
   - Compare 2-3 viable architectures.
   - Explain tradeoffs and rejected options.
   - Require user confirmation before editing files.

3. **Select modern technology deliberately**
   - Check current official SDK and framework docs before coding.
   - Use industry architecture signals from OpenAI, Anthropic, AWS, Google Cloud, and Microsoft only as design guidance.
   - Treat "advanced" as current, typed, testable, observable, maintainable, and fit-for-purpose.
   - Do not add frameworks, multi-agent layers, memory, queues, databases, dashboards, browser control, or computer-use tools unless the brief justifies them.

4. **Map requirements to implementation**
   - Produce a brief-to-file mapping before generation.
   - Every major module must trace to a user requirement, safety requirement, or validation requirement.
   - No decorative scaffolds, fake tools, silent fallback providers, or mock implementations in production paths.

5. **Generate and validate**
   - Generate the TypeScript project structure, env validation, provider adapter, harness, tool registry, approval gate, tests, and runnable entrypoint required by the confirmed brief.
   - Run the agreed validation commands.
   - Report exact pass, fail, or skipped status. If credentials are unavailable, mark live LLM smoke as not run.

## Skill Structure

```text
create-agent-app/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    architecture-patterns.md
    generation-contract.md
    grill-questions.md
    harness-contract.md
    industry-architecture-signals.md
    modern-selection-policy.md
    official-docs.md
    provider-patterns.md
    safety-policy.md
    validation-policy.md
```
