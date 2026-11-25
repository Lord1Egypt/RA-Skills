## Description:

Verify before you act: pay agentshield.live before a transfer, an invoice, a clearing code, a promised date, a holiday calendar, or a stablecoin send. Free catalog search. A 404 with X-AgentShield-Retryable false is not a charge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bartelmost](https://clawhub.ai/user/bartelmost)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request deterministic checks before relying on payment details, invoices, routing identifiers, settlement dates, holiday calendars, or stablecoin transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive financial verification inputs may be sent to an external service.

Mitigation: Before use, review what each check sends, limit shared details where possible, and follow an approved data-sharing policy.

## Reference(s):

- [AgentShield route catalog](https://agentshield.live/routes.json)
- [AgentShield free route selector](https://agentshield.live/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Markdown instructions and structured service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some production checks require per-call USDC payment; catalog search and route selection are free.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
