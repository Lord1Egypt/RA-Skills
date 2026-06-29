## Description: <br>
CloudBase WeChat Integration guides agents through Mini Program WeChat Pay, Official Account JSAPI Pay, Native QR-code Pay, Official Account OAuth, openid handling, payment callbacks, and CloudBase Integration Center generated functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add, debug, or extend WeChat payment and Official Account OAuth flows in CloudBase applications while preserving Integration Center boundaries and credential handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified payment and OAuth code can affect order state, fulfillment, or user authentication if reviewed superficially. <br>
Mitigation: Review payment changes carefully, confirm generated function names and paths, and rely on server-side callbacks or order queries before fulfillment. <br>
Risk: Merchant keys, certificates, AppSecret values, and APIv3 keys could be exposed if copied into chat, source code, or frontend files. <br>
Mitigation: Keep secrets in CloudBase console configuration and preserve generated credential handling when extending Integration Center functions. <br>


## Reference(s): <br>
- [CloudBase WeChat Integration Overview](references/overview.md) <br>
- [Mini Program WeChat Pay](references/mini-program-pay.md) <br>
- [Official Account JSAPI Pay](references/official-account-jsapi-pay.md) <br>
- [Native QR-Code Pay](references/native-qr-pay.md) <br>
- [Official Account OAuth](references/official-account-oauth.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [CloudBase Integration Center overview](https://docs.cloudbase.net/integration/introduce/index.md) <br>
- [CloudBase Integration Center usage](https://docs.cloudbase.net/integration/usage/index.md) <br>
- [CloudBase Mini Program WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-miniprogram/index.md) <br>
- [CloudBase Native WeChat Pay](https://docs.cloudbase.net/integration/wechat-pay-native/index.md) <br>
- [CloudBase Official Account JSAPI Pay](https://docs.cloudbase.net/integration/wechat-pay-jsapi-h5/index.md) <br>
- [CloudBase Official Account OAuth](https://docs.cloudbase.net/integration/wechat-official-oauth/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with scenario-specific code snippets and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on payment and OAuth implementation guidance, generated function integration, troubleshooting, and safety checks for credential and callback handling.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata; artifact frontmatter reports 2.23.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
