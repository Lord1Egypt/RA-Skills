## Description: <br>
A skill dedicated to Antom payment integration, helping merchants select the right product and integration approach based on business needs, and build code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-intl](https://clawhub.ai/user/ant-intl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and merchants use this skill to choose Antom payment products and integration modes, then gather current Antom documentation before implementing payment flows. It supports product selection, SDK selection, validation checks, and security guidance for one-time, tokenized recurring, subscription, checkout, payment element, and API-only integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment integrations are high-impact and outdated or unofficial documentation can lead to incorrect implementation choices. <br>
Mitigation: Verify that linked CDN documentation and SDK references are genuinely from Antom or Alipay, and check the latest Antom Open Platform documentation before production use. <br>
Risk: Private keys or other sensitive payment credentials could be exposed in client code, prompts, logs, or public repositories. <br>
Mitigation: Keep private keys server-side only, never paste secrets into prompts or logs, and do not commit keys to public repositories. <br>
Risk: Client-side payment results can be spoofed or misread before final settlement is confirmed. <br>
Mitigation: Verify asynchronous notification signatures and confirm payment status through Antom notification or transaction query flows before fulfillment, retries, or repayment prompts. <br>


## Reference(s): <br>
- [SDK Description](https://cdn.marmot-cloud.com/page/antom-integration-doc/references/select-sdk.md) <br>
- [Product Decision](https://cdn.marmot-cloud.com/page/antom-integration-doc/references/product-decision.md) <br>
- [Integration Checklist](https://cdn.marmot-cloud.com/page/antom-integration-doc/references/checklist.md) <br>
- [Antom Official Website](https://www.antom.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with links, checklists, shell commands, and code suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be checked against the latest Antom documentation and should avoid exposing private keys, credentials, or payment secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
