# Multi-Agent Protocol

## The Challenge

When multiple AI agents work on the same project in parallel (e.g., one on frontend, one on backend), they need coordination. Without it, they'll drift apart — building to different assumptions.

## Architecture

```
                 ┌──────────────┐
                 │  Lead Agent   │
                 │ (Forge)       │
                 │ Holds contract│
                 └──────┬───────┘
                        │
           ┌────────────┼────────────┐
           │            │            │
     ┌─────▼─────┐ ┌───▼───┐ ┌─────▼─────┐
     │  Agent A   │ │Contract│ │  Agent B   │
     │ (Frontend) │ │  Repo  │ │ (Backend)  │
     └───────────┘ └───────┘ └───────────┘
```

## Rules

### 1. Shared Contract, No Direct Communication
- All agents receive the same contract files
- Agents never communicate directly with each other
- All coordination goes through the lead agent + contract

### 2. No Unilateral Contract Changes
- Any agent needing a contract change must file a Change Request
- Lead reviews, approves, and propagates the change
- Other agents are notified of the change before continuing

### 3. Recommended Implementation Order
```
Contract defined
  → Backend implements API
  → Contract tests verify backend conforms
  → Frontend implements against contract
  → Integration test validates both sides
  → E2E test validates user flows
```

### 4. Conflict Resolution
When two agents have conflicting needs:
- Lead evaluates both perspectives against the Design Brief
- Contract is updated to resolve the conflict
- Both agents receive the updated contract

## Dispatch Template

When dispatching to an agent in multi-agent mode, include:

```markdown
## Context
You are working on: {module}
Other agent is working on: {other module}

## Contract (Source of Truth)
- API: contracts/api-spec.yaml
- Types: contracts/shared-types.ts
- Errors: contracts/errors.yaml

## ⚠️ Contract Rules
- You MUST implement according to the contract
- You MUST NOT change contract files directly
- If you need a contract change, output a Change Request section at the end of your response

## Your Scope
Only modify files in: {allowed directories}
Do NOT touch: {forbidden directories}
```

## Cross-Workspace Architecture

When frontend and backend live in **separate workspaces** (different repos, different agents), the protocol changes:

### Dedicated Contract Repository

```
contracts-repo/                  ← Independent Git repo, all agents pull from here
├── api-spec.yaml                ← OpenAPI 3.1 (authoritative)
├── shared-types.ts              ← Auto-generated (DO NOT EDIT)
├── errors.yaml                  ← Error code registry
├── events.schema.json           ← Async event definitions
└── CHANGELOG.md                 ← All contract changes logged
```

### Integration Methods

| Method | Best For | How |
|--------|----------|-----|
| **Git Submodule** | Stable contracts | `git submodule add <url> contracts/` |
| **Package Registry** | Typed languages | `npm install @project/contracts` |
| **Copy-Sync by Lead** | Small teams, quick start | Lead copies latest files before dispatch |

### Cross-Workspace Dispatch Template

```markdown
## Workspace Architecture: Cross-Workspace

You are the {frontend|backend} agent. The other side is developed by a
separate agent in a separate workspace. You cannot see their code.

## Contract (Source of Truth — External Repository)
Your local copy is in `contracts/`. It is **read-only**.
- DO NOT modify any file in `contracts/`
- All types must be imported from `contracts/shared-types.ts`
- If the contract is insufficient, write a Change Request in `CHANGE_REQUEST.md`

## Your Scope
Only modify files in: {allowed directories}
DO NOT touch: contracts/, {other forbidden dirs}
```

### Contract Test Isolation

Each side runs contract tests independently:
- **Backend:** Validate API responses against OpenAPI spec
- **Frontend:** Type-check against `shared-types.ts` + mock server from spec
- **Integration:** Orchestrated externally by Lead or CI (docker-compose combining both services)
