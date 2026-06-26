# Contract-First Development Guide

## Why Contract-First?

In AI-assisted development, the contract is the only reliable coordination mechanism between:
- Multiple coding agents working in parallel
- Frontend and backend that can't talk to each other during development
- Humans who need to understand what AI is building

Without a contract, each agent invents its own version of the API. Both sides pass their tests. Integration day arrives and everything explodes.

## The Contract Stack

```
api-spec.yaml          ← REST API definitions (OpenAPI 3.1)
shared-types.ts        ← TypeScript interfaces (auto-generated from spec)
errors.yaml            ← Error code registry
events.schema.json     ← Async event definitions (WebSocket, queues)
```

### api-spec.yaml

The primary contract. Defines every endpoint: path, method, parameters, request body, response schemas, error responses.

**Rules:**
- Every endpoint must have `operationId` (used for code generation)
- Response schemas must reference `components/schemas/` (not inline)
- Use `$ref` for shared types
- Include realistic `example` values in schemas
- Document error responses (400, 401, 404, 500) for each endpoint

### shared-types.ts

Auto-generated from `api-spec.yaml` using `scripts/generate-types.sh`. **Never edit manually.**

Both frontend and backend import from this file. This guarantees type consistency at compile time.

### errors.yaml

Central error code registry. Every error response in the API must use a code defined here.

Benefits:
- Frontend can build error handling for known codes
- Backend can't invent ad-hoc error formats
- Easy to grep for error handling coverage

### events.schema.json

For projects with WebSocket or async events. Uses JSON Schema to define event payloads.

## Workflow

```
1. Write api-spec.yaml (define endpoints + schemas)
2. Run generate-types.sh → shared-types.ts
3. Add error codes to errors.yaml
4. Backend implements → contract test validates responses
5. Frontend implements → imports shared-types.ts
6. Integration test verifies both sides work together
```

## Contract Change Protocol

When any agent needs to modify the contract:

1. **Do not modify directly.** Write a Change Request:
   - What endpoint/schema to change
   - Why the change is needed
   - Which modules are affected
2. Lead (Forge) reviews the request
3. If approved: lead updates the contract, regenerates types, notifies all agents
4. If rejected: agent must work within the existing contract

This prevents one agent from silently breaking another agent's assumptions.
