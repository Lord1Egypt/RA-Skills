## Description:

An email inbox your agent owns with its own key: free to hold on a funded balance, receiving free, sends priced per message, and wait-code hands back the verification code a sign-up emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their owners use this skill to create and manage an email inbox, read and send messages, and retrieve sign-up verification codes. The owner approves spending or sets a budget for paid sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate CLI and hosted email service were not assessed, including their handling of messages and verification codes.

Mitigation: Review the CLI and the provider's data handling before use, especially before relying on it for verification codes.

Risk: Exposed recovery words or login keys could allow account access.

Mitigation: Protect recovery words and login keys; do not share them in messages or logs.

Risk: Sending email spends from the owner's prepaid balance.

Mitigation: Check current pricing and get owner approval before spending, or stay within an owner-set budget.

## Reference(s):

- [Agentgates email API documentation](https://api.agentgates.ai/api/account/docs/email)

## Skill Output:

**Output Type(s):** [API calls, Email messages, Verification codes, Guidance]

**Output Format:** [HTTP API requests and text; inbox messages and verification codes returned as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sending uses the owner's prepaid balance; receiving is free.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
