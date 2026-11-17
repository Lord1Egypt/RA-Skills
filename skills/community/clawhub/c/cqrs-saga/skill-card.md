## Description:

Orchestrates a python-cqrs saga whose finished steps compensate on failure, with persistent state and recovery. Use when a flow crosses services or databases and a completed step must be undone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vadikko2](https://clawhub.ai/user/vadikko2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to implement multi-step workflows across services or databases, with compensation for completed steps and persistent recovery after failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference checking was partial, and the bundle includes an executable Python example.

Mitigation: Review linked and referenced material and inspect the example code before using it in an application.

Risk: A saga checkpoint can be stored before the business transaction commits, leaving recovery to skip an effect that rolled back.

Mitigation: Keep the step effect in the same transaction as its checkpoint, or reconcile effects that did not commit before recovery skips the step.

## Reference(s):

- [Saga recovery guidance](references/recovery.md)
- [Order saga example](assets/order_saga.py)
- [ClawHub release](https://clawhub.ai/vadikko2/skills/cqrs-saga)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Markdown guidance with Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes saga setup, compensation, and recovery guidance.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
