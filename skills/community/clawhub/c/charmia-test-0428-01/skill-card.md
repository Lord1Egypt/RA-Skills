## Description:

Guides developers through WeChat Pay delegated-deduction integration for recurring billing and pay-after-use flows, including product selection, official examples, signing and callback rules, quality checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment-integration engineers use this skill to plan and troubleshoot WeChat Pay delegated-deduction implementations for direct merchants and service providers. It helps retrieve official request and callback examples, compare signing modes, and review high-impact payment flows before launch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer payment-integration conversations strongly.

Mitigation: Use it only for WeChat Pay delegated-deduction work and review its recommendations before acting on them.

Risk: The security evidence reports unsafe HTTP callback examples.

Mitigation: Use HTTPS-only callback URLs in production and verify callback signatures before trusting payment events.

Risk: Charge, refund, and contract-termination examples affect financial operations.

Mitigation: Require human review, environment-specific configuration checks, and low-risk testing before production use.

Risk: Incorrect signature handling or duplicate callback processing can produce misleading payment state.

Mitigation: Validate V2 and V3 signatures according to the selected protocol and enforce idempotency for callback and retry flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/charmia-test-0428-01)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Merchant product introduction](artifact/references/1-商户/产品选型/产品介绍.md)
- [Service provider product introduction](artifact/references/2-服务商/产品选型/产品介绍.md)
- [Merchant signing and verification rules](artifact/references/1-商户/接入指南/签名与验签规则.md)
- [Service provider signing and verification rules](artifact/references/2-服务商/接入指南/签名与验签规则.md)
- [WeChat Pay merchant delegated-deduction product documentation](https://pay.weixin.qq.com/doc/v2/merchant/4011986647.md)
- [WeChat Pay service provider delegated-deduction product documentation](https://pay.weixin.qq.com/doc/v2/partner/4011988358.md)
- [WeChat Pay V2 signature verification tool](https://pay.weixin.qq.com/doc/v2/tool/sign_verify.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with official request, response, callback, and client-code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before use in payment, refund, contract termination, signing, or callback-handling workflows.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
