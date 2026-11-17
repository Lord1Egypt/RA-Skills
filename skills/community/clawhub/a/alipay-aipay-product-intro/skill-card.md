## Description:

Provides Alipay agent wallet and AI payment product information, using a fixed Alipay request that may return a paid HTTP 402 resource flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request an introduction to Alipay AI payment and agent wallet features. When the resource requires payment, the skill passes the full HTTP 402 response to the Alipay payment workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requesting the product introduction may lead to a paid HTTP 402 flow handled by another Alipay payment skill.

Mitigation: Proceed with payment only when the payment step and amount are clear, and respect the user's refusal to pay.

Risk: The workflow contacts a fixed Alipay endpoint and depends on the service and network being available.

Mitigation: Report service errors, timeouts, or network failures to the user and suggest retrying later.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/alipay-aipay-product-intro)
- [Metadata homepage](https://github.com/alipay/payment-skills)
- [Alipay Aipay introduce endpoint](https://aipayapi.alipay.com/merchant/aipay/introduce)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include complete HTTP 402 response details needed by the payment workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
