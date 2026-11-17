## Description:

T54 provides ClawCredit guidance for registering agents, managing pre-qualification, and using a credit line to access x402 services without upfront cryptocurrency payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rizaldii09](https://clawhub.ai/user/rizaldii09)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register for ClawCredit, configure agent context, check pre-qualification and repayment status, and pay x402 services through a credit line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports broad recurring agent-context uploads, including transcripts, prompts, workspace Markdown, and trace context.

Mitigation: Install only in workspaces where users have given explicit consent and where transcripts, prompts, workspace files, and trace data have been reviewed or redacted for secrets and confidential content.

Risk: The security evidence reports local API-token storage and guidance warns against printing or manually copying tokens.

Mitigation: Use the SDK-managed credential file, restrict file permissions, avoid logging tokens, and rotate or re-register credentials if exposure is suspected.

Risk: The security evidence reports persistent background checks through heartbeat behavior and scheduled jobs.

Mitigation: Review scheduled or heartbeat tasks before installation and disable or remove recurring checks when the operating environment does not support them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rizaldii09/skills/firstt)
- [ClawCredit x402 partner services registry](https://www.claw.credit/X402_PARTNER_SERVICES_REGISTRY.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes consent, credential handling, tracing, payment, heartbeat, repayment, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
