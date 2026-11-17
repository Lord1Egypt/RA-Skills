## Description:

Generates five paid, platform-adapted ecommerce ad copies from product details after a SkillPay billing check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingogx](https://clawhub.ai/user/wingogx)

### License/Terms of Use:


## Use Case:

External ecommerce operators and developers can use this skill to generate ready-to-use Facebook, Google, and TikTok ad copy from a product name, selling points, and target audience. It is intended for paid workflows that require structured JSON output and billing failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing checks may approve paid generation without verified payment.

Mitigation: Review before installing in a paid workflow and require an explicit successful billing response with a transaction id before generation.

Risk: The billing endpoint and token handling are under-scoped for use with SKILLPAY_API_KEY.

Mitigation: Restrict the billing endpoint to the expected SkillPay service and keep API keys in environment variables.

Risk: Generated copy appears scoped to Chinese-language output unless locale behavior is expanded or documented.

Mitigation: Confirm the target locale before use and add locale controls if non-Chinese ad copy is required.

## Reference(s):

- [SkillPay API Contract](references/skillpay-api-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/wingogx/skills/ecommerce-ad-copy-generator)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Structured JSON with generated ad copy, pricing metadata, and billing or validation error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs return exactly five ad copy items across Facebook, Google, and TikTok.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
