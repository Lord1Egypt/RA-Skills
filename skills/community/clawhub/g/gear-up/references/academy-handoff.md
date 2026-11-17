# Academy Handoff

Use this reference when a temporary capability materially helped and may deserve reuse.

## Do not promote directly

A successful ephemeral artifact has proven only this:

> it helped on the current task under the current conditions.

That is enough to justify a **candidate record** when reuse is plausible. It is not enough to call the capability general, trusted, or graduated.

## Candidate record minimum

Capture:

```yaml
id: <stable-id>
status: candidate
artifact_type: skill | tool | context | agent | composite
summary: <one sentence>
capability_gap: <what existing capabilities could not do>
value_test:
  before: <observed failure/gap>
  after: <observed result>
origin_task: <task/run identifier>
dependencies: []
permissions: []
limitations: []
reuse_hypothesis: []
```

Also retain the generated artifact and enough evidence to reproduce the result when policy permits.

## Reuse rule

On later tasks, search Academy metadata before generating again. If a candidate matches:

1. keep its candidate status visible;
2. validate it against the current task/runtime;
3. stage it experimentally;
4. observe the result;
5. update evidence instead of creating a near-duplicate artifact.

## Qualification default

A reasonable default bar is successful use in at least two distinct task contexts plus suitable correctness/behavioral eval evidence and no unresolved critical issue. Project policy may strengthen or relax this depending on risk and artifact type.

## Graduation

For a procedural capability, use `skillify` after qualification to remove accidental context, sharpen triggers, add regression/boundary evals, and create the durable Agent Skill package. Permanent deployment remains an explicit authority decision.
