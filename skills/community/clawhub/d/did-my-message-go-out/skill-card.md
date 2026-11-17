## Description:

Checks whether an agent's outbound message was actually delivered by comparing the runtime send result with the observed channel API request and status code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill after important message sends to decide whether they can report a message as sent, need receiving-side verification, or should avoid claiming delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate local ledger plugin to observe send outcomes and request metadata.

Mitigation: Before installing, confirm the environment is comfortable enabling the clawphylax plugin and review that plugin independently when request metadata, send history, or tool outcomes are sensitive.

Risk: Some channels deliver outside the agent process, so wire evidence may be unavailable.

Mitigation: Treat CLAIMED_ONLY as a receiving-side verification requirement and do not report the message as sent until delivery is independently confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/did-my-message-go-out)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style status report with an ACTION line and evidence sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts include DELIVERED, NOT_DELIVERED, CLAIMED_ONLY, CANCELLED, PENDING, and NO_SEND.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
