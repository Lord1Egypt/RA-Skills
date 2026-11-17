## Description:

Define order lifecycle states, transition guards, and recovery paths for A2A transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design A2A order orchestration from quote acceptance through payment, fulfillment, completion, cancellation, and exception handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order orchestration generated from this scaffold could mishandle payment, reputation, timeout recovery, or terminal-state behavior if adopted without review.

Mitigation: Review generated implementation and tests before deployment, with specific attention to payment transitions, reputation triggers, timeout recovery, and terminal states.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/luoqianchenguni-max/skills/a2a-market-order-state-machine)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with implementation contracts and code path examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on order states, legal transition checks, event triggers, timeout recovery, and runtime validation expectations.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
