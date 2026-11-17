---
name: "dr-runtime-contract"
description: "Runtime configuration changes: propagate, detect stale declarations, and prove capability across enabled execution paths."
---

# DR Runtime Contract

Use when a Daniel-owned digital employee changes a session-persistent runtime setting: credentials, endpoints, policies, provider settings, or tool/API-client configuration. Use it before declaring the change complete.

This skill owns configuration propagation and cross-path proof. dr-agent-secrets owns secret storage, permissions, redaction, and restart safety.

## Boundaries

- Keep secret values out of prompts, manifests, logs, receipts, memory, and this skill.
- Keep host-specific paths, identifiers, and delivery targets in a manifest, not in the skill.
- Do not create, rotate, relocate, or reveal secrets here.
- Do not reload or restart a live service without the approval required by the secret/service procedure.
- Do not assume all employees use the same execution paths.

## Procedure

### 1. Define the runtime contract

Create or update a non-secret manifest for the affected employee and environment. For every changed key group, record:

- environment and owner;
- canonical source reference, such as a SecretRef ID, protected file path, or managed configuration field;
- declared consumers and enabled execution paths;
- active precedence order;
- reload/restart requirement;
- safe, read-only capability probe;
- expected non-secret revision or source identifier.

Completion criterion: every changed key group has one canonical source and one declared environment.

### 2. Inspect effective sources and duplicates

Inspect each declared source, service override, scheduler definition, alternate workspace/config path, and known legacy/cache location that can supply the key group. Record key names, source identifiers, and precedence only; never print values.

Classify each declaration as canonical, inactive historical, or conflicting. A sensitive key group with two active sources and no documented precedence fails this step.

Completion criterion: no unresolved active duplicate or stale declaration remains.

### 3. Apply through the owning procedure

Use the owner procedure for the change:

- use dr-agent-secrets for SecretRefs, protected env fragments, permissions, redaction, and restart safety;
- use dr-schedule-manager for any scheduled runtime, manifest, trigger, and registered-payload change;
- use the platform-specific procedure for non-secret configuration.

Record the new non-secret source/revision in the runtime contract. Keep dev and prod contracts separate.

Completion criterion: the canonical source is updated through its owner procedure and the intended reload state is known.

### 4. Control reload and cache state

Determine whether each consumer reads configuration at process start, per request, or from a cache. Perform only the approved reload/restart action. When interruption risk is unclear, stop for approval before restarting a live service.

Completion criterion: each affected consumer has either reloaded or is explicitly marked pending reload.

### 5. Verify every enabled path

Build a matrix from the manifest. Test only enabled paths, but include every enabled applicable path:

- running Gateway process;
- fresh direct session;
- isolated child/subagent execution;
- scheduled or automation runtime;
- gateway-exec, tool, or API-client path.

For each path, first confirm it resolved the expected non-secret source/revision, then run the contract's safe authenticated read-only probe. A variable-presence check alone does not pass.

Completion criterion: every applicable cell passes source provenance and capability verification.

### 6. Issue a redacted receipt

Report environment, key group, canonical source identifier, paths tested, reload state, probe name, timestamp, and pass/fail. Do not include values, bearer tokens, headers, request bodies, response bodies, or secret-derived hashes.

Mark the configuration change **complete** only when the whole applicable matrix passes. Otherwise mark it incomplete and identify failed or untested paths.

## Acceptance Criteria

A runtime configuration change passes only when:

1. each key group has one canonical source and explicit precedence;
2. duplicate/stale active declarations are resolved or documented inactive;
3. secret handling stayed within dr-agent-secrets;
4. required reload/restart handling followed its approval gate;
5. every enabled path passed the read-only capability probe;
6. the receipt is complete and redacted.

## References

- Invoke dr-agent-secrets for persistent secret or environment changes.
- Invoke dr-schedule-manager when a scheduled/automation runtime is enabled.
- Follow dr-checkpoint-implementation for fleet rollout, production-risk changes, or validation that cannot be completed in one safe checkpoint.
- Add this trigger to dr-agent-baseline and fleet onboarding: session-persistent runtime configuration changes require this skill.
