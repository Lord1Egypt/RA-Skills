# Generation Contract

This contract defines the minimum viable output for a usable TypeScript agent application. It prevents half-formed demos.

## Before Writing Files

Confirm:

- target directory
- package manager
- runtime version expectations
- application type
- harness type
- provider pattern
- state and memory policy
- tool permission model
- validation commands

If any item is unknown, ask or propose defaults and wait for confirmation.

Read `modern-selection-policy.md` and produce a Modernity Rationale before implementation.

## Brief-to-File Mapping

Before implementation, produce a mapping like:

```markdown
| Brief requirement | Files/modules to create or change | Why this is needed |
| --- | --- | --- |
```

Rules:

- Every major module must trace to a user requirement, safety requirement, or validation requirement.
- Do not add frameworks, databases, queues, dashboards, multi-agent roles, or durable memory because they seem advanced.
- Include every selected advanced dependency or harness feature in the mapping.
- Prefer the simplest architecture that satisfies the brief and preserves future extension points.
- If a requested feature is too large for the current change, separate it into an explicit later milestone instead of adding a stub.

## Minimum Project Deliverables

Generate a real project only when the confirmed scope includes enough information to satisfy these deliverables.

### Package and Tooling

- `package.json` with scripts for `typecheck`, `test`, `build`, and at least one runnable entrypoint.
- `tsconfig.json` with strict TypeScript enabled.
- `.env.example` matching the selected provider pattern.
- `.gitignore` excluding secrets, dependency folders, build outputs, traces if appropriate, and local env files.
- Test framework setup when tests are part of validation.

### Configuration

- `src/config/env.ts` is the only module that reads `process.env`.
- Environment validation uses `zod`.
- Missing required provider config throws a named configuration error.
- Provider-specific variables are required only for the selected provider.

### Provider Layer

- Provider interface is typed and narrow.
- Real provider adapter is implemented for the confirmed provider.
- OpenAI-compatible adapters expose unsupported capability errors instead of assuming full parity.
- Mocks or fakes live only in test files or clearly named test support modules.

### Agent Harness

- Harness accepts a typed request and returns a typed result.
- Prompt assembly, model call, tool execution, trace capture, and final status are separate functions or modules.
- Tool calls are schema-validated before execution.
- Tool errors are surfaced in the result and trace.

### Tool Registry

- Each tool declares input schema, side-effect class, approval requirement, dry-run support, and handler.
- No destructive or external-mutation tool is enabled without an approval path.
- At least one real, harmless tool or no tools at all. Do not create fake tools to make the app look agentic.

### State, Memory, and Artifacts

- If stateless, state absence is explicit.
- If memory is selected, provide a real in-memory, file, or database-backed store according to the brief.
- If artifacts are produced, write an artifact ledger and validate produced artifacts.

### Entrypoint

- CLI, API, or UI entrypoint must exercise the real harness.
- Entrypoint must not bypass provider config, tool registry, approval policy, or trace capture.
- User-facing errors must distinguish config, provider, tool, approval, validation, and unexpected failures.

### Tests

- Test env parsing success and failure.
- Test provider-not-configured behavior.
- Test approval gate behavior for privileged tools when tools exist.
- Test at least one harness success path using a mock/test double that is clearly named and restricted to tests.
- Test artifact or trace contract when required.

## Refusal Conditions

Do not generate code when:

- the user has not confirmed the decision gate
- the requested provider/framework requires current API details but official docs cannot be checked and local package types are unavailable
- required permissions would be unsafe without approval
- the user asks to embed real credentials
- the requested output would be only a decorative demo

Instead, report what is missing and the next concrete decision needed.
