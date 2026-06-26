## Description: <br>
Generate paid ecommerce ad copy in batch with SkillPay billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingogx](https://clawhub.ai/user/wingogx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and ecommerce operators use this skill to generate five platform-adapted ad copy variants from a product name, selling points, and target audience after a SkillPay charge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each successful run may charge 0.10 USDT through SkillPay. <br>
Mitigation: Use the skill only when the user intends to run a paid generation and clearly account for the charge before execution. <br>
Risk: The billing request sends user ID, product name, and target audience to the configured SkillPay endpoint. <br>
Mitigation: Keep endpoint variables pointed only at trusted SkillPay URLs and avoid submitting sensitive product or audience data unless that sharing is acceptable. <br>
Risk: A SkillPay API key may be used for authorization. <br>
Mitigation: Store SKILLPAY_API_KEY only in environment variables and do not print or hardcode the token. <br>


## Reference(s): <br>
- [SkillPay API Contract](references/skillpay-api-contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wingogx/ecommerce-ad-copy-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Structured JSON containing pricing status, validated input, and five ad copy objects with platform, headline, body, and CTA fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns validation and billing error objects when input is invalid, billing fails, or balance is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
