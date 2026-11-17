## Description:

Gate Pay Payment Skill helps agents execute prepared Gate Pay merchant order payments after user intent, required payment details, and Gate payment authorization are verified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to complete prepared merchant Gate Pay charges in pay-first checkout flows. It produces localized receipts or actionable failure guidance after payment execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate irreversible Gate Pay charges from an authenticated account.

Mitigation: Require the assistant to show the merchant, order ID, exact amount, currency, and payment method, then obtain fresh explicit approval for those exact details before any charge.

Risk: Broad payment-intent triggers could route ambiguous checkout requests into a payment execution flow.

Mitigation: Block execution unless the user selected Gate Pay, all required charge fields are present, authorization is valid, and current payment intent is explicit.

Risk: Some runtime rules are referenced from mutable external documents rather than fully bundled in the reviewed package.

Mitigation: Review the referenced runtime rules at install and update time, and revalidate behavior before enabling authenticated payment execution.

Risk: A status-check request could be mistaken for permission to charge again.

Mitigation: Do not call the payment tool to infer status; direct the user to Gate payment history or merchant support when no status query tool is available.

## Reference(s):

- [Gate Pay MCP Specification](references/mcp.md)
- [Gate Pay Payment Scenarios](references/scenarios.md)
- [Gate Pay Payment Skill on ClawHub](https://clawhub.ai/gate-exchange/skills/gate-exchange-pay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Localized Markdown receipts and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include merchant order ID, amount, currency, payment status, timestamp, and payment method; voucher fields should appear only when returned by the payment API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
