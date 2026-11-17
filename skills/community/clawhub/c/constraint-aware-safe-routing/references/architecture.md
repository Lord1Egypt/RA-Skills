# Architecture and decision model

Read this reference when designing, implementing, or reviewing the controller.

## Components

```text
Request and trusted context
          |
          v
Local router + novelty signals
          |
          v
Selective controller <----> cloud reasoning model
       |             |
       v             v
response/abstain   authoritative gate
                         |
                         v
                  constrained tool wrapper
                         |
                         v
              observation, audit, state update
```

The cloud model is a reasoning resource. It does not own the controller and cannot bypass the gate.

## Separate estimates

Maintain three conceptually separate estimates:

- `q_competence`: likelihood that the proposed route or answer is correct;
- `q_safety`: evidence that the exact action is allowed under current authoritative constraints;
- `q_viability`: evidence that the selected execution path is available within budget.

Do not combine these into an opaque score when a hard authorization rule is available. A request can be familiar and correctly understood while the action is forbidden.

The model-facing decision contract is defined in [decision-contract-v1.schema.json](decision-contract-v1.schema.json). Its `authorization` field is only a reported signal. The enforcement component must obtain authorization independently and record the model decision and any gate override separately.

## Constraint shift

A constraint shift changes the admissible action set without necessarily changing the request text. Test at least:

- permission revoked;
- user role changed;
- policy version changed;
- tool removed or schema changed;
- objective changed;
- consequence or resource sensitivity changed;
- cloud, authorization service, or local hardware unavailable.

Use paired cases with the same request before and after the change. The expected result should change because the authoritative state changed, not because the wording changed.

## Gate contract

The gate should receive:

```json
{
  "request_id": "...",
  "principal": {"id": "...", "role": "..."},
  "objective": "...",
  "action": "...",
  "resource": "...",
  "arguments": {},
  "observed_policy_version": "...",
  "observed_tools_version": "...",
  "observed_at": "ISO-8601 timestamp"
}
```

It should return one of:

- `allow`: current state permits the exact effect;
- `block`: action, principal, resource, or arguments are not permitted;
- `refresh`: observed policy or tools state is stale;
- `unavailable`: authoritative verification could not be completed.

Permit one controlled refresh. Treat repeated staleness or unavailability as fail-closed. Do not let model confidence, OOD, or persuasive text change the gate result.

## Execution token

If the system uses an authorization token, bind it to:

- request ID;
- principal;
- action and normalized arguments;
- resource;
- policy and tool versions;
- short expiration;
- single use.

Never serialize the reusable token into general audit logs.

## Semantic validation before enforcement

Reject or contain at least these combinations before tool execution:

- `tool_execute` with authorization other than `allow`;
- `tool_execute` while the authorization service or tool is unavailable;
- `tool_execute` without one concrete proposed effect;
- multiple or hybrid provisional routes;
- cloud response without cloud availability;
- an allow signal paired with `permission_revoked`;
- an alternate tool or batch operation that preserves a denied semantic capability.

Structural validity is not authorization. A schema-valid proposal can still be denied by fresh policy state, and malformed proposals must fail closed.

## Availability policy

Define explicit behavior for:

- local model unavailable;
- cloud timeout or quota exhaustion;
- invalid cloud schema;
- authorization service unavailable;
- tool missing or stale;
- observation inconsistent with the requested effect.

Prefer a clear abstention or safe block to an undocumented fallback.

