# SKILL: implementation-planner

## Purpose
Convert a feature idea into a concrete technical execution plan (architecture, modules, interfaces, validations, and rollout).

## When to Use
- The request requires design decisions before code.
- Multiple components must be coordinated (frontend/backend/infra/contracts).
- The user asked for an “implementation plan” or “architecture”.

## Inputs
- `feature_description` (required, string): what to build and why.
- `constraints` (optional, string[]): non-negotiables (security, budget, tooling, timeline).
- `environment` (optional, object): runtime (OS, container), deploy targets, CI.
- `existing_system` (optional, string): relevant current architecture and boundaries.

## Steps
1. Define success criteria (what “done” means) and explicit non-goals.
2. Identify actors and interfaces (users, services, contracts, external APIs).
3. Choose an architecture that minimizes risk and change surface.
4. Define modules and ownership boundaries (what lives where).
5. Specify data flow (inputs, outputs, persistence, logs/audit trail).
6. Specify validation path:
   - unit tests
   - integration tests
   - security checks (as applicable)
7. Define rollout:
   - feature flags / guarded modes
   - backwards compatibility
   - migration steps (if any)
8. List open questions and assumptions; ask for clarification when risk is material.

## Validation
- Plan satisfies all stated constraints.
- Every module has an interface and responsibility.
- Testing/validation is included (not “later”).
- Rollout avoids accidental production impact.

## Output
Structured plan (example schema):

```yaml
overview: "<1 paragraph>"
modules:
  - name: "<module>"
    responsibility: "<what it owns>"
    interfaces: ["<api/events/files>"]
data_flow:
  inputs: ["..."]
  outputs: ["..."]
validation:
  unit: ["..."]
  integration: ["..."]
rollout:
  guardrails: ["..."]
open_questions: ["..."]
```

## Safety Rules
- Do not select tools that violate constraints.
- Do not propose deployments that can impact production without explicit gating.
- Prefer simplest architecture that meets requirements.

## Example
Feature: “Add webhook ingestion with idempotency and audit logs.”
Output (excerpt):
```yaml
modules:
  - name: "webhook-controller"
    responsibility: "request validation + signature checks"
  - name: "event-store"
    responsibility: "persist raw payload + processing status"
validation:
  integration: ["replay same event id results in no duplicate side effects"]
```

