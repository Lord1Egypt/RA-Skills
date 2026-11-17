## Description:

China Shopping Assistant helps users compare JD, Taobao, Tmall, PDD, Vipshop, SHEIN, and related Chinese shopping options by visible price, seller trust, review risk, promotion caveats, and after-sales fit without login, checkout, order submission, or payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to compare Chinese marketplace options from a product name or link and produce buy, wait, or switch-platform advice based on visible prices, trust signals, review risks, promotion caveats, and after-sales fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may treat visible prices, discounts, or promotions as guaranteed final payable prices.

Mitigation: Present prices as decision inputs and require the user to confirm final payable price, shipping, taxes, discounts, and return terms directly on the platform before purchase.

Risk: A user may ask the agent to handle credentials, identity checks, addresses, checkout confirmation, or payment details.

Mitigation: Keep the skill limited to shopping research and comparison; the user must complete login, checkout, order confirmation, and payment manually outside the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/china-shopping-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown shopping comparison and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes visible-price caveats and excludes login, checkout, order submission, and payment handling.]

## Skill Version(s):

1.1.0 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
