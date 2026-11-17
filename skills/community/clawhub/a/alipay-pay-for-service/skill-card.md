## Description:

Handles Alipay payment-service flows by identifying cashier links, submitting payment requests through the Alipay CLI, and checking payment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill when a conversation includes an Alipay cashier link or a clear payment intent, so the agent can guide wallet authorization, submit payment, present the payment output, and later check payment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs external package code for payment handling.

Mitigation: Review before installing, run in a sandboxed environment, and approve installation only when the pinned Alipay package is trusted.

Risk: Payment links passed through shell-interpolated command strings can create command-injection exposure.

Mitigation: Use structured command arguments or robust escaping, and pass only validated Alipay cashier URLs from the current context.

Risk: Payment URLs and QR outputs can be sensitive even when time-limited.

Mitigation: Do not persist them in logs or caches, and show them only through the user-selected channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/alipay-pay-for-service)
- [Alipay payment-skills homepage](https://github.com/alipay/payment-skills)
- [Alipay agent-payment npm package](https://www.npmjs.com/package/@alipay/agent-payment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and CLI-derived text with payment links or QR media handling when returned by the payment tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit time-limited payment URLs or QR media paths that should be preserved exactly and not logged or redistributed.]

## Skill Version(s):

1.0.9-beta1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
