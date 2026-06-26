## Description: <br>
CloudBase WeChat integration guide for Mini Program WeChat Pay, Official Account JSAPI Pay, Native QR-code Pay, Official Account OAuth, openid handling, payment callbacks, and CloudBase Integration Center generated functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add, debug, and extend WeChat payment and Official Account OAuth flows in CloudBase applications. It helps route Mini Program Pay, Official Account JSAPI Pay, Native QR-code Pay, openid handling, callback verification, and generated-function extension work through the correct CloudBase Integration Center references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment or OAuth secrets could be exposed if copied into source code, generated examples, prompts, or chat. <br>
Mitigation: Keep merchant keys, AppSecret values, certificates, and APIv3 keys in CloudBase console configuration. <br>
Risk: Business fulfillment could be triggered from untrusted frontend payment success callbacks. <br>
Mitigation: Use server-side payment callbacks or order-query results as the authoritative payment state before updating business data. <br>
Risk: Generated CloudBase function names and routes may differ from examples. <br>
Mitigation: Verify the actual generated function name and route paths in the user's Integration Center setup before writing calls. <br>
Risk: Payment changes may affect real transactions. <br>
Mitigation: Test payment changes with sandbox or low-value transactions before production use. <br>


## Reference(s): <br>
- [CloudBase WeChat Integration Overview](references/overview.md) <br>
- [Mini Program WeChat Pay](references/mini-program-pay.md) <br>
- [Native QR-Code Pay](references/native-qr-pay.md) <br>
- [Official Account JSAPI Pay](references/official-account-jsapi-pay.md) <br>
- [Official Account OAuth](references/official-account-oauth.md) <br>
- [WeChat Integration Troubleshooting](references/troubleshooting.md) <br>
- [CloudBase Integration Center Overview](https://docs.cloudbase.net/integration/introduce/index.md) <br>
- [CloudBase Integration Center Usage](https://docs.cloudbase.net/integration/usage/index.md) <br>
- [CloudBase Mini Program WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-miniprogram/index.md) <br>
- [CloudBase Native WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-native/index.md) <br>
- [CloudBase Official Account JSAPI Pay](https://docs.cloudbase.net/integration/wechat-pay-jsapi-h5/index.md) <br>
- [CloudBase Official Account OAuth](https://docs.cloudbase.net/integration/wechat-official-oauth/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, checklists, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scenario-specific guidance for CloudBase WeChat payment and Official Account OAuth flows.] <br>

## Skill Version(s): <br>
1.2.4 (source: ClawHub release metadata; artifact frontmatter reports 2.23.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
