# Contract-First Development Guide

## What is Contract-First?

Contract-first means you define the API interface **before** writing any implementation code. The contract (OpenAPI spec, shared types, error codes) becomes the single source of truth that both frontend and backend must conform to.

## Why Contract-First for AI Development?

When AI agents write code, they tend to "invent" interfaces on the fly. Without a pre-agreed contract:
- Frontend agent assumes one response format, backend agent implements another
- Error handling diverges silently
- Integration testing becomes a game of "find the mismatch"

Contract-first eliminates this by giving all agents the same blueprint.

## The Contract Stack

### 1. OpenAPI Spec (`contracts/api-spec.yaml`)
The authoritative definition of every HTTP endpoint:
- Request parameters, headers, body schemas
- Response schemas for every status code
- Authentication requirements

### 2. Shared Types (`contracts/shared-types.ts`)
TypeScript interfaces that mirror the OpenAPI schemas:
- Used directly by frontend code
- Used by backend for type-safe responses
- Can be auto-generated from the OpenAPI spec

### 3. Error Codes (`contracts/errors.yaml`)
Centralized error code registry:
- Every error code used in the project must be defined here
- Includes HTTP status, default message, and description
- Both frontend and backend reference this for error handling

## Contract Change Protocol

Contracts are immutable during a sprint unless explicitly changed through review:

1. Agent discovers the contract needs to change
2. Agent submits a **Contract Change Request** (not a direct edit):
   - What needs to change
   - Why the current contract doesn't work
   - Impact on other modules
3. Lead reviews the request
4. If approved: lead updates the contract, notifies all agents
5. If rejected: agent must implement within existing contract constraints

This protocol exists because a contract change can cascade across the entire project. One unreviewed change can break multiple agents' work.

## Best Practices

- **Start minimal** — Define only the endpoints you need now
- **Version from day one** — Include version in the spec
- **Use $ref liberally** — DRY your schemas
- **Document edge cases** — What happens on empty input? Null fields?
- **Keep error codes specific** — `USER_NOT_FOUND` > `NOT_FOUND`
