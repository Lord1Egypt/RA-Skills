## Description:

Integrate Chinese payment methods (WeChat Pay, Alipay, UnionPay) into applications by guiding agents through payment flows, callbacks, refunds, reconciliation, and payment compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement WeChat Pay, Alipay, and UnionPay payment flows, callbacks, refunds, reconciliation, and compliance checklists in applications serving Chinese payment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment callback examples may be used without complete verification before fulfillment.

Mitigation: Require provider signature verification, transaction replay checks, and server-side validation of amount, currency, merchant, app, and order identifiers before changing payment state.

Risk: Duplicate or replayed payment notifications could credit or fulfill an order more than once.

Mitigation: Use atomic idempotent state transitions and reject already-processed order events before any fulfillment or crediting.

Risk: Incorrect unit handling between WeChat Pay fen and Alipay yuan can create payment amount errors.

Mitigation: Centralize amount conversion and validate provider callback amounts against immutable server-side order records.

## Reference(s):

- [China Payment Integration on ClawHub](https://clawhub.ai/lm203688/skills/china-payment-integration)
- [WeChat Pay Merchant Platform](https://pay.weixin.qq.com)
- [Alipay Open Platform](https://open.alipay.com)
- [WeChat Pay Sandbox Documentation](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=23_1)
- [Alipay Sandbox](https://open.alipay.com/develop/sandbox/app)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JavaScript code examples and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment integration workflows, callback handling examples, refund snippets, and compliance checklist items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
