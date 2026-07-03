## Description: <br>
CloudBase WeChat integration guide for Mini Program WeChat Pay, Official Account JSAPI Pay, Native QR-code Pay, Official Account OAuth, openid handling, payment callbacks, and CloudBase Integration Center generated functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add, debug, or extend WeChat payment and Official Account OAuth flows in CloudBase applications while keeping merchant and app credentials out of source code and chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment-flow guidance can affect financial transactions if generated function names, order amounts, callback paths, or fulfillment logic are wrong. <br>
Mitigation: Verify generated function names and official CloudBase documentation, validate amounts and orders server-side, and test payment changes with a sandbox or low-value transaction before production use. <br>
Risk: Merchant credentials, AppSecret values, API keys, certificates, or private keys could be exposed if copied into chat or source code. <br>
Mitigation: Keep secrets in CloudBase console Integration Center configuration and review generated code to confirm credentials are not embedded in frontend code, repositories, or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binggg/skills/cloudbase-wechat-integration) <br>
- [CloudBase Integration Center overview](https://docs.cloudbase.net/integration/introduce/index.md) <br>
- [CloudBase Integration Center usage](https://docs.cloudbase.net/integration/usage/index.md) <br>
- [Mini Program WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-miniprogram/index.md) <br>
- [Official Account JSAPI Pay](https://docs.cloudbase.net/integration/wechat-pay-jsapi-h5/index.md) <br>
- [Native QR-code Pay](https://docs.cloudbase.net/integration/wechat-pay-native/index.md) <br>
- [Official Account OAuth](https://docs.cloudbase.net/integration/wechat-official-oauth/index.md) <br>
- [Overview reference](references/overview.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with inline code examples and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scenario-specific guidance for CloudBase WeChat Pay, OAuth, generated functions, callbacks, and troubleshooting.] <br>

## Skill Version(s): <br>
1.2.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
