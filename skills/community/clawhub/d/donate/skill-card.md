## Description:

Recognizes a user's intent to send a tip, collects and validates the amount, confirms it with the user, and invokes a payment skill to create a tip order and display payment information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sayxxx](https://clawhub.ai/user/sayxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to handle tipping flows: identify tip intent, ask for or validate the amount, confirm the transaction, and hand the payment request to a payment skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tip payment orders may be created without verifying the intended recipient or merchant.

Mitigation: Use only where the payment skill is already bound to one known recipient or merchant; add recipient verification before supporting named recipients.

Risk: Users may see an external payment link without a clear distinction between order creation and completed payment.

Mitigation: Clearly label payment links as external and make the pending-versus-paid status explicit before treating a tip as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sayxxx/skills/donate)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Conversational text with payment parameters and returned payment information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validates that the tip amount is greater than 0 and no more than 10000; recipient information is not collected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
