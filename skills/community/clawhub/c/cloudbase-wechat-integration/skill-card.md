## Description:

Helps developers build and troubleshoot CloudBase integrations for WeChat payments, virtual payment, Official Account OAuth, payment callbacks, and generated integration functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binggg](https://clawhub.ai/user/binggg)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to implement or troubleshoot CloudBase WeChat Mini Program and virtual payments, Native and Official Account JSAPI checkout, OAuth, and payment callbacks. It guides safe use of generated integration functions and order fulfillment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant, account, or API credentials could be exposed in source code or chat.

Mitigation: Configure credentials in the CloudBase console; never place secrets in application code, prompts, or examples.

Risk: Trusting frontend payment success or unverified callbacks could cause incorrect fulfillment or order state.

Mitigation: Confirm payment through verified callbacks or server-side order queries; validate order and amount, and make callback handling idempotent.

Risk: Payment, refund, or deployment changes may affect real transactions or the wrong environment.

Mitigation: Review changes before production, confirm the target environment, and obtain authorization before real-money tests.

## Reference(s):

- [CloudBase Integration Center overview](https://docs.cloudbase.net/integration/introduce.md)
- [CloudBase Integration Center usage](https://docs.cloudbase.net/integration/usage.md)
- [CloudBase Mini Program WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-miniprogram.md)
- [CloudBase Native WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-native.md)
- [CloudBase Official Account JSAPI Pay](https://docs.cloudbase.net/integration/wechat-pay-jsapi-h5.md)
- [CloudBase Official Account OAuth](https://docs.cloudbase.net/integration/wechat-official-oauth.md)
- [WeChat Mini Program Virtual Payment guide](https://developers.weixin.qq.com/miniprogram/dev/platform-capabilities/business-capabilities/virtual-payment)
- [WeChat wx.requestVirtualPayment API](https://developers.weixin.qq.com/miniprogram/dev/api/payment/wx.requestVirtualPayment.html)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scenario-specific; confirm the CloudBase environment, generated function routes, and payment channel before implementation.]

## Skill Version(s):

1.2.83 (source: ClawHub release metadata; artifact frontmatter lists 2.36.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
