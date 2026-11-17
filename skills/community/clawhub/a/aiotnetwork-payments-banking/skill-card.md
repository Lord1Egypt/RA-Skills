## Description:

Fund wallets, transfer money, send remittances, and convert currencies. Includes top-up via multiple payment methods and international money transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage wallet top-ups, money transfers, international remittances, currency conversions, and transaction lookups through authenticated payment API flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real financial actions, including transfers, remittances, top-ups, conversions, and recipient deletion.

Mitigation: Require an explicit quote-and-confirm flow and independently verify the amount, currency, recipient, fees, and destructive recipient changes before calling confirmation or deletion endpoints.

Risk: The skill handles bearer-token sessions and transaction PINs.

Mitigation: Use only a verified first-party HTTPS API endpoint, request transaction PINs fresh for each confirmation, and never cache, log, or persist secrets.

Risk: Ambiguous requests for transfers, confirmations, conversions, or recipient deletion could lead to unintended financial activity.

Mitigation: Ask the user to resolve ambiguity and restate the exact operation details before taking any initiating, confirming, converting, or deleting action.

Risk: Exchange rates are indicative and can change between quote and confirmation.

Mitigation: Present the latest quote details and ask for confirmation before executing the final conversion or remittance step.

## Reference(s):

- [Payments & Banking ClawHub skill page](https://clawhub.ai/d9m1n1c/skills/aiotnetwork-payments-banking)
- [Default AIOT payment API base URL](https://payment-api-dev.aiotnetwork.io)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with REST endpoints and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL configuration and an authenticated bearer-token session for financial operations.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
