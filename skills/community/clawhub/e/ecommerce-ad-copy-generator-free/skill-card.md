## Description:

Free basic ecommerce ad-copy generator that creates three platform-specific ad copy variants from product information and reserves premium upgrade guidance for batch, multilingual, and A/B variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingogx](https://clawhub.ai/user/wingogx)

### License/Terms of Use:


## Use Case:

Ecommerce operators and marketing teams use this skill to generate initial Facebook, Google, and TikTok ad-copy drafts from a product name, selling points, and target audience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upgrade response includes a payment link whose destination depends on payment URL configuration and the supplied user_id.

Mitigation: Use trusted payment URL configuration and validate or encode user_id values before using generated links.

Risk: The free generator outputs Chinese ad copy that may need market, brand, or compliance review before publication.

Mitigation: Review generated copy before campaign launch and adapt language, claims, and calls to action to the target market.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wingogx/skills/ecommerce-ad-copy-generator-free)
- [SkillPay API Contract](artifact/references/skillpay-api-contract.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON response with generated ad-copy text, validated input echo, tier status, and upgrade guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free tier returns three copies for Facebook, Google, and TikTok; premium requests return upgrade-required guidance with a payment link.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
