## Description:

Provides a structured event-driven architecture workflow covering events versus commands, ordering, idempotency, sagas, outbox patterns, observability, failure handling, and replay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to design or refactor asynchronous systems, event buses, and cross-service workflows. It guides event identification, contracts, delivery semantics, orchestration choices, observability, and replay planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture guidance may be misapplied to production systems, especially around ordering, idempotency, replay, and saga boundaries.

Mitigation: Treat the skill output as advisory and review any design or implementation changes separately before production use.

Risk: Event replay and at-least-once delivery can cause duplicate side effects or inconsistent data when consumers are not idempotent.

Mitigation: Document partitioning, deduplication, idempotency, dead-letter queue, and replay behavior before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklists and architecture review prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow; no code execution or external service calls are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
