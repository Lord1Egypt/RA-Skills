## Description:

Asserts python-cqrs handlers with cqrs.testing.test_harness across commands, queries, events, notifications, messaging, sagas, chains, streams, fallbacks, and middleware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vadikko2](https://clawhub.ai/user/vadikko2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write focused tests for python-cqrs handlers and inspect recorded requests, events, notifications, invocations, inboxes, and outboxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tests wrapping an application mediator may send messages to its real broker.

Mitigation: Pass CapturingMessageBroker() without an inner broker to test_harness.around so messages are captured instead of sent externally.

Risk: Database-backed tests can leave changes in the test database.

Mitigation: Use a test database and roll back database-backed tests.

## Reference(s):

- [Example test_order.py](assets/test_order.py)
- [ClawHub skill page](https://clawhub.ai/vadikko2/skills/cqrs-testing)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
