## Description:

Manage customer expectations, order changes, and post-purchase support for long-lead custom products such as engraved necklaces, custom pet portraits, and personalized gifts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents and DTC store operators use this skill to answer post-purchase questions about long-lead custom orders, including order status, modification requests, quality issues, returns, and realistic timeline expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ETA calculations or rush-order assumptions may conflict with a store's actual production policy.

Mitigation: Confirm the ETA calculator defaults and rush handling against the store's policy before using generated timelines with customers.

Risk: Milestone updates, SMS, email marketing, or third-party loyalty automation may involve customer order data and consent requirements.

Mitigation: Complete privacy review and obtain the required customer consent before using customer data for SMS, email marketing, or third-party automation.

## Reference(s):

- [Custom Order Support on ClawHub](https://clawhub.ai/rijoyai/skills/custom-order-support)
- [Custom Product FAQ](references/faq.md)
- [Custom Product Post-Purchase & Change Policy](references/policy.md)
- [Rijoy](https://www.rijoy.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response templates with optional plain-text ETA calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ETA ranges rather than fixed delivery promises and may include policy-aware next steps for modifications, remakes, refunds, or goodwill gestures.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
