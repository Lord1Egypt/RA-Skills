# Dispatch Protocol — Aegis-Enhanced CC Task Dispatch

When dispatching a coding task to Claude Code under Aegis, inject the following context into the prompt. This ensures CC builds according to design and contract, not freestyle.

## Prompt Structure Template

```
## Task
{Task description — what to build, acceptance criteria}

## Design Reference
Read `docs/designs/{NNN-feature}.md` — this is the approved design. Follow it.
Key decisions from the brief:
- {Decision 1}: {choice} (rationale: {why})
- {Decision 2}: {choice}

## Contracts (MUST READ BEFORE CODING)
- API spec: `contracts/api-spec.yaml` — all endpoints must conform
- Shared types: `contracts/shared-types.ts` — import from here, never redefine
- Error codes: `contracts/errors.yaml` — use defined codes only
- Events: `contracts/events.schema.json` — if applicable

## Hard Constraints
{Extract from CLAUDE.md — the ⛔ section. Include only constraints relevant to this task.}

## Acceptance Criteria
1. {Specific criterion}
2. {Specific criterion}
3. All contract tests pass
4. No lint/type errors
5. New endpoints have contract tests

## Code Quality Rules
{From code-lessons.md — filter by project language/framework}

## Testing Requirements
{From Design Brief testing strategy — which layers need tests for this task}
```

## What to Include vs. Skip

| Always Include | Include if Relevant | Skip |
|----------------|---------------------|------|
| Task description | Design Brief reference | Unrelated design docs |
| Contract file paths | Code lessons | Full CLAUDE.md (too long) |
| Hard constraints | Integration test setup | PM/Jira details |
| Acceptance criteria | Multi-agent coordination notes | Historical gaps |
| Testing requirements | | |

## Multi-Agent Dispatch

When dispatching frontend and backend in parallel:

### Backend Agent
```
## Coordination
You are implementing the BACKEND. A separate agent handles frontend.
- DO NOT implement frontend code
- Your contract: `contracts/api-spec.yaml` — implement exactly what it defines
- If you need a contract change, write a Change Request in `docs/contract-changes/` — do NOT modify the contract directly
```

### Frontend Agent
```
## Coordination
You are implementing the FRONTEND. Backend is being built separately.
- DO NOT implement backend code
- Import types from `contracts/shared-types.ts`
- API base URL will be configured via environment variable
- Mock API responses using contract-defined schemas (not invented data)
- If contract seems incomplete, write a Change Request in `docs/contract-changes/`
```
