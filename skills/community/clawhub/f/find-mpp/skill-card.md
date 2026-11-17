## Description:

Teaches agents to use an MPP (Machine Payments Protocol) endpoint registry: search before paying, report newly discovered HTTP 402 Payment endpoints, and submit reviews after every use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdwatson32](https://clawhub.ai/user/bdwatson32)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Machine Payments Protocol endpoints before paying for HTTP 402 services, report newly found endpoints, and write post-use reviews for registry users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External registry submissions may disclose endpoint reports, submitter email, task context, payment method details, or payment receipt identifiers.

Mitigation: Use only with explicit approval for each external report or review, and redact secrets, private URLs, prompts, customer data, and unnecessary payment or environment identifiers before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bdwatson32/skills/find-mpp)
- [Find MPP API](https://www.findmpp.com/api)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON]

**Output Format:** [Markdown guidance with HTTP request examples and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces registry search, endpoint reporting, and endpoint review guidance for agent workflows.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
